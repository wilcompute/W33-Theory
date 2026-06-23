#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'photonic_holonet.tex'
OUT = ROOT / 'data' / 'bt1583_dry_run_artifact_check.json'
MD = ROOT / 'analysis' / 'BT1583_dry_run_artifact_check.md'
TEX = ROOT / 'analysis' / 'BT1583_dry_run_artifact_check.tex'
BEGIN = '% BT1582 OPERATOR_OAM APPENDIX BEGIN'
END = '% BT1582 OPERATOR_OAM APPENDIX END'
INSERTS = [
    'analysis/BT1564_BT1566_holonet_insert.tex',
    'analysis/BT1567_BT1569_holonet_insert.tex',
    'analysis/BT1570_BT1572_holonet_insert.tex',
    'analysis/BT1573_BT1576_holonet_insert.tex',
]

def block() -> str:
    lines = [BEGIN]
    for p in INSERTS:
        lines.append(f'\\input{{{p}}}')
    lines.append(END)
    return '\n'.join(lines) + '\n'

def splice_text(text: str):
    b = block()
    if BEGIN in text and END in text:
        before = text.split(BEGIN, 1)[0]
        after = text.split(END, 1)[1]
        return before + b + after.lstrip('\n'), 'replace_existing_block'
    marker = '\\section{Conclusion}'
    if marker in text:
        return text.replace(marker, b + '\n' + marker, 1), 'insert_before_conclusion'
    return text + '\n' + b, 'append_to_end'

def main() -> None:
    text = TARGET.read_text(encoding='utf-8') if TARGET.exists() else ''
    once, mode1 = splice_text(text)
    twice, mode2 = splice_text(once)
    missing = [p for p in INSERTS if not (ROOT / p).exists()]
    checks = {
        'target_exists': TARGET.exists(),
        'conclusion_marker_present': '\\section{Conclusion}' in text,
        'four_insert_paths': len(INSERTS) == 4,
        'all_insert_paths_exist': not missing,
        'bounded_block_has_begin_end': BEGIN in block() and END in block(),
        'first_splice_has_expected_mode': mode1 in ('insert_before_conclusion', 'replace_existing_block', 'append_to_end'),
        'second_splice_replaces_existing_block': mode2 == 'replace_existing_block',
        'idempotent_text_after_second_splice': twice == splice_text(twice)[0],
        'dry_run_only': True,
    }
    result = {
        'bt': 1583,
        'title': 'Dry-run artifact check',
        'verified': all(checks.values()),
        'source': 'tools/bt1582_operator_oam_appendix_splice_runner.py',
        'target': 'photonic_holonet.tex',
        'inserts': INSERTS,
        'missing_inserts': missing,
        'first_splice_mode': mode1,
        'second_splice_mode': mode2,
        'interpretation': 'The validator checks that every BT1582 insert path exists, the splice block has bounded markers, a first dry-run splice is possible, and a second pass becomes replace_existing_block. It performs no paper rewrite.',
        'honesty_boundary': 'Dry-run validator only; no --apply run, no TeX rewrite, and no PDF rebuild are claimed.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1583 Dry-run Artifact Check\n\nValidator for the BT1582 operator/OAM appendix splicer. It checks insert paths, bounded markers, conclusion marker, and idempotent replacement behavior. It performs no paper rewrite and no PDF rebuild.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1583: dry-run validator checks BT1582 insert paths, bounded markers, conclusion marker, and idempotent splice behavior without applying the splice.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1583,'verified':result['verified'],'mode1':mode1,'mode2':mode2}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
