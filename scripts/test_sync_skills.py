"""Verify the public promise: complete fixed flows, identical shared rules, portable copies."""

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FLOWS = ('Audit', 'Build', 'Refactor')
COMMON = ('Shared execution rules', 'Establish the baseline', 'Completion and blocked checks')
RESOURCES = ('references/core.md', 'references/repo-profile.md',
             'references/component-analysis.md', 'references/verification.md',
             'templates/repo-profile.md', 'templates/component-contract.md',
             'templates/audit-and-refactor.md')


def sections(text):
    matches = list(re.finditer(r'^## (.+)$', text, re.M))
    return {m.group(1): text[m.start():matches[i + 1].start() if i + 1 < len(matches)
                            else len(text)].strip() for i, m in enumerate(matches)}


class SkillMappingTests(unittest.TestCase):
    def test_complete_selected_flow_and_common_stages_match_canonical_source(self):
        canonical = sections((ROOT / 'references/workflow.md').read_text())
        for flow in FLOWS:
            with self.subTest(flow=flow):
                actual = sections((ROOT / f'skills/comui-{flow.lower()}/references/workflow.md').read_text())
                self.assertEqual(list(actual), [*COMMON[:2], flow, COMMON[2]])
                for heading in (*COMMON, flow):
                    self.assertEqual(actual[heading], canonical[heading])

    def test_shared_guidance_and_templates_are_full_copies(self):
        for flow in FLOWS:
            for path in RESOURCES:
                with self.subTest(flow=flow, path=path):
                    self.assertEqual((ROOT / f'skills/comui-{flow.lower()}' / path).read_bytes(),
                                     (ROOT / path).read_bytes())

    def test_each_copied_skill_has_a_closed_local_reference_graph(self):
        with tempfile.TemporaryDirectory(prefix='comui standalone ') as tmp:
            for flow in FLOWS:
                skill = (Path(tmp) / f'comui-{flow.lower()}').resolve()
                shutil.copytree(ROOT / 'skills' / skill.name, skill)
                self.assertTrue((skill / 'references/workflow.md').is_file())
                for file in skill.rglob('*.md'):
                    text = re.sub(r'```.*?```', '', file.read_text(), flags=re.S)
                    for target in re.findall(r'\]\(([^)]+)\)', text):
                        if target.startswith(('https://', 'http://', '#')):
                            continue
                        target = (file.parent / target.split('#')[0]).resolve()
                        self.assertTrue(target.is_relative_to(skill), (file, target))
                        self.assertTrue(target.is_file(), (file, target))

    def test_check_detects_drift_without_rewriting_and_write_repairs_it(self):
        with tempfile.TemporaryDirectory(prefix='comui mapping ') as tmp:
            copy = Path(tmp) / 'kit'
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '__pycache__', '.DS_Store'))
            script = copy / 'scripts/sync_skills.py'
            def run(*args):
                return subprocess.run([sys.executable, '-B', str(script), *args],
                                      capture_output=True, text=True)
            self.assertEqual(run('--check').returncode, 0)
            target = copy / 'skills/comui-audit/references/verification.md'
            target.write_text(target.read_text() + '\nLocal drift\n')
            drifted = target.read_bytes()
            self.assertEqual(run('--check').returncode, 1)
            self.assertEqual(target.read_bytes(), drifted)
            self.assertEqual(run('--write').returncode, 0)
            self.assertEqual(target.read_bytes(), (copy / 'references/verification.md').read_bytes())
            target.unlink()
            self.assertEqual(run('--check').returncode, 1)
            self.assertFalse(target.exists())
            self.assertEqual(run('--write').returncode, 0)
            self.assertEqual(run('--check').returncode, 0)


if __name__ == '__main__':
    unittest.main()
