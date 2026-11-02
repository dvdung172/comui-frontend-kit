import importlib.util
import json
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('comui_trial', Path(__file__).with_name('trial.py'))
trial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trial)


class TrialTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='comui tests ')
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo with spaces'
        self.repo.mkdir()
        (self.repo / 'card.js').write_text('export const card = 1;\n')
        self.out = self.root / 'run output'

    def tearDown(self):
        self.temp.cleanup()

    def fake(self, code):
        script = self.root / 'fake codex.py'
        script.write_text(code)
        return patch.object(trial, 'build_command', return_value=[sys.executable, str(script)])

    def test_command_enforces_readonly_without_shell_interpolation(self):
        command = trial.build_command('/bin/codex', self.repo, self.out / 'report.md')
        self.assertEqual(command[:4], ['/bin/codex', '--ask-for-approval', 'never', 'exec'])
        self.assertEqual(command[command.index('--sandbox') + 1], 'read-only')
        self.assertEqual(command[command.index('--cd') + 1], str(self.repo))
        self.assertIn('--ephemeral', command)
        self.assertNotIn('--dangerously-bypass-approvals-and-sandbox', command)

    def test_snapshot_ignores_dependencies_secrets_and_external_symlinks(self):
        (self.repo / '.env').write_text('private')
        (self.repo / 'node_modules').mkdir()
        (self.repo / 'node_modules' / 'dependency.js').write_text('dep')
        outside = self.root / 'outside.txt'
        outside.write_text('private')
        (self.repo / 'outside-link').symlink_to(outside)
        self.assertEqual(set(trial.snapshot(self.repo)), {'card.js'})

    def test_explicit_model_is_per_invocation(self):
        command = trial.build_command('/bin/codex', self.repo, self.out / 'report.md', model='gpt-5.5')
        self.assertEqual(command[command.index('--model') + 1], 'gpt-5.5')
        self.assertNotIn('--model', trial.build_command('/bin/codex', self.repo, self.out / 'report.md'))

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'requires POSIX FIFO')
    def test_snapshot_skips_nonregular_files_without_blocking(self):
        os.mkfifo(self.repo / 'pipe')
        code = (f'import runpy\n'
                f'from pathlib import Path\n'
                f'm=runpy.run_path({str(Path(trial.__file__))!r})\n'
                f'print(list(m["snapshot"](Path({str(self.repo)!r}))))\n')
        process = subprocess.run([sys.executable, '-B', '-c', code], timeout=1,
                                 capture_output=True, text=True, check=True)
        self.assertEqual(process.stdout.strip(), "['card.js']")

    def test_output_cannot_be_inside_repo_or_reuse_existing_directory(self):
        for output in [self.repo, self.repo / 'reports']:
            with self.assertRaises(ValueError):
                trial.run_audit(self.repo, 'cards', output, 3, '/bin/codex')
        self.out.mkdir()
        with self.assertRaises(FileExistsError):
            trial.run_audit(self.repo, 'cards', self.out, 3, '/bin/codex')

    def test_success_saves_evidence_usage_and_pending_quality_review(self):
        code = (f'from pathlib import Path\n'
                f'Path({str(self.out / "report.md")!r}).write_text("Audit with source evidence")\n'
                'print(\'{"type":"turn.completed","usage":{"input_tokens":12,"cached_input_tokens":4,"output_tokens":5}}\')\n')
        with self.fake(code):
            result = trial.run_audit(self.repo, 'cards; $() literal', self.out, 3, '/bin/codex')
        self.assertEqual(result['status'], 'completed')
        self.assertTrue(result['source_unchanged'])
        self.assertEqual(result['usage']['input_tokens'], 12)
        self.assertEqual(result['quality_review'], 'not_reviewed')
        self.assertIn('cards; $() literal', (self.out / 'prompt.txt').read_text())
        self.assertEqual(json.loads((self.out / 'run.json').read_text())['status'], 'completed')
        self.assertTrue((self.out / 'review.md').is_file())

    def test_nonzero_exit_and_partial_logs_are_retained(self):
        with self.fake('import sys\nprint("partial event")\nprint("failure", file=sys.stderr)\nsys.exit(2)\n'):
            result = trial.run_audit(self.repo, 'cards', self.out, 3, '/bin/codex')
        self.assertEqual(result['status'], 'failed')
        self.assertIn('failure', (self.out / 'stderr.log').read_text())
        self.assertIsNone(result['usage'])

    def test_timeout_retains_record(self):
        with self.fake('import time\nprint("started", flush=True)\ntime.sleep(10)\n'):
            result = trial.run_audit(self.repo, 'cards', self.out, 0.1, '/bin/codex')
        self.assertEqual(result['status'], 'timeout')
        self.assertIn('started', (self.out / 'events.jsonl').read_text())
        self.assertTrue((self.out / 'run.json').exists())

    def test_zero_exit_without_report_is_not_success(self):
        with self.fake('print("done")\n'):
            result = trial.run_audit(self.repo, 'cards', self.out, 3, '/bin/codex')
        self.assertEqual(result['status'], 'missing_report')

    def test_changed_source_is_reported_without_rollback(self):
        code = (f'from pathlib import Path\n'
                f'Path({str(self.repo / "card.js")!r}).write_text("changed")\n'
                f'Path({str(self.out / "report.md")!r}).write_text("report")\n')
        with self.fake(code):
            result = trial.run_audit(self.repo, 'cards', self.out, 3, '/bin/codex')
        self.assertEqual(result['status'], 'source_changed')
        self.assertEqual(result['changed_paths'], ['card.js'])
        self.assertEqual((self.repo / 'card.js').read_text(), 'changed')

    def test_event_failure_overrides_successful_process_exit(self):
        code = (f'from pathlib import Path\n'
                f'Path({str(self.out / "report.md")!r}).write_text("report")\n'
                'print(\'{"type":"turn.failed","error":{"message":"provider unavailable"}}\')\n')
        with self.fake(code):
            result = trial.run_audit(self.repo, 'cards', self.out, 3, '/bin/codex')
        self.assertEqual(result['status'], 'failed')


if __name__ == '__main__':
    unittest.main()
