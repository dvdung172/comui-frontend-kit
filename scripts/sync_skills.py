#!/usr/bin/env python3
"""Generate/check complete, portable single-flow skills from the canonical ComUI kit."""

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SHARED = ('Shared execution rules', 'Establish the baseline', 'Completion and blocked checks')
RESOURCES = ('references/core.md', 'references/repo-profile.md',
             'references/component-analysis.md', 'references/verification.md',
             'templates/repo-profile.md', 'templates/component-contract.md',
             'templates/audit-and-refactor.md')
MODES = {
    'audit': {
        'title': 'Audit',
        'description': "Use when reviewing existing frontend source, assessing component reuse, or proposing a UI refactor against a repository's own standards. Executes the full Audit flow only and produces findings and a plan without implementing changes.",
        'short': 'Rà soát frontend và đề xuất refactor',
        'prompt': 'Dùng $comui-audit rà soát frontend trong repo hiện tại và đề xuất cải thiện có bằng chứng.',
    },
    'build': {
        'title': 'Build',
        'description': "Use when implementing a frontend page, feature, or component using a repository's existing stack, design system, and reusable UI. Executes the full Build flow only; a prior audit is not required.",
        'short': 'Xây frontend theo stack và chuẩn repo',
        'prompt': 'Dùng $comui-build thực hiện yêu cầu frontend của tôi theo chuẩn repo hiện tại.',
    },
    'refactor': {
        'title': 'Refactor',
        'description': 'Use when implementing a scoped frontend refactor or consolidating compatible UI duplication while preserving public behavior. Executes the full Refactor flow only; a prior audit or written plan is optional.',
        'short': 'Refactor frontend và giữ hành vi hiện có',
        'prompt': 'Dùng $comui-refactor thực hiện refactor frontend tôi yêu cầu và kiểm chứng hành vi liên quan.',
    },
}


def workflow_sections(text):
    matches = list(re.finditer(r'^## (.+)$', text, re.M))
    result = {}
    for i, match in enumerate(matches):
        title = match.group(1)
        if title in result:
            raise ValueError(f'Duplicate workflow section: {title}')
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        result[title] = text[match.start():end].strip()
    return result


def digest(data):
    return hashlib.sha256(data).hexdigest()


def outputs(root):
    workflow_path = root / 'references/workflow.md'
    sections = workflow_sections(workflow_path.read_text(encoding='utf-8'))
    resources = {path: (root / path).read_bytes() for path in RESOURCES}
    result = {}
    for mode, meta in MODES.items():
        name, title = f'comui-{mode}', meta['title']
        prefix = Path('skills') / name
        headings = (*SHARED[:2], title, SHARED[2])
        selected = {heading: sections[heading] for heading in headings}
        numbers = re.findall(r'^(\d+)\. ', selected[title], re.M)
        if not numbers or numbers != [str(i) for i in range(1, len(numbers) + 1)]:
            raise ValueError(f'{title}: numbered steps must be consecutive from 1')
        audit_template_row = (
            '| Optionally organize an audit report | [Audit template](templates/audit-and-refactor.md) |\n'
            if mode == 'audit' else '')
        body = f'''---
name: {name}
description: {meta['description']}
---

# ComUI {title}

Fixed flow: **{title}**. This package is the complete {title} projection of `comui-frontend-kit`, including the shared stages and full operational references. It is generated from the canonical kit and works as a standalone installed folder.

Read the complete [shared contract](references/core.md) and [workflow](references/workflow.md) before working. Execute the shared rules, baseline, every numbered {title} step and completion checks. Read the operational references when the workflow names them; their requirements are not replaced by this entrypoint. Account for every stage/step with evidence or an explicit applicability/blocking reason.

Remain in {title}. Do not start another ComUI flow, call another ComUI skill or require a prior ComUI task. If the request belongs to a different flow, explain the mismatch and ask the user to choose before taking out-of-flow action. Natural-language requests are sufficient; prompt examples, a prior audit, a written plan and fixed report forms are optional.

| Need | Full local resource |
| --- | --- |
| Establish repo standards, source snapshot, scope and checks | [Repo profile](references/repo-profile.md) |
| Map UI blocks, state/consumers and evaluate reuse | [Component analysis](references/component-analysis.md) |
| Establish evidence, perform checks and report gaps | [Verification](references/verification.md) |
{audit_template_row}| Optionally capture a reusable profile | [Profile template](templates/repo-profile.md) |
| Optionally describe a component API | [Contract template](templates/component-contract.md) |

The optional templates do not select or launch a workflow. Follow the user's language and requested presentation while fulfilling all applicable steps of {title}.
'''
        result[prefix / 'SKILL.md'] = body.encode('utf-8')
        result[prefix / 'references/workflow.md'] = (
            '# Workflow\n\n' + '\n\n'.join(selected.values()) + '\n').encode('utf-8')
        for path, data in resources.items():
            result[prefix / path] = data
        interface = {'display_name': f'ComUI {title}', 'short_description': meta['short'],
                     'default_prompt': meta['prompt']}
        yaml = 'interface:\n' + ''.join(
            f'  {key}: {json.dumps(value, ensure_ascii=False)}\n' for key, value in interface.items())
        result[prefix / 'agents/openai.yaml'] = yaml.encode('utf-8')
        manifest = {
            'generated_by': 'scripts/sync_skills.py',
            'canonical_workflow': 'references/workflow.md',
            'flow': mode,
            'stage_ids': ['shared', 'baseline', *[f'{mode}.{i}' for i in numbers], 'completion'],
            'section_sha256': {heading: digest(text.encode('utf-8'))
                               for heading, text in selected.items()},
            'resource_sha256': {path: digest(data) for path, data in resources.items()},
        }
        result[prefix / 'mapping.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='Report drift without changing files (default).')
    mode.add_argument('--write', action='store_true', help='Regenerate managed files in skills/comui-*.')
    args = parser.parse_args()
    try:
        expected = outputs(ROOT)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f'Cannot project canonical workflow: {error}\n')
    changed = []
    for path, data in expected.items():
        dest = ROOT / path
        if not dest.is_file() or dest.read_bytes() != data:
            changed.append(str(path))
            if args.write:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
    if changed:
        print(('Updated' if args.write else 'Drift detected in') + f' {len(changed)} file(s):')
        print('\n'.join(changed))
        return 0 if args.write else 1
    print(f'All {len(expected)} generated files match canonical flows and references.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
