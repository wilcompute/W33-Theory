#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1612_empty_artifact_and_backfill_audit.json'
MD = ROOT / 'analysis' / 'BT1612_empty_artifact_and_backfill_audit.md'
TEX = ROOT / 'analysis' / 'BT1612_empty_artifact_and_backfill_audit.tex'

FILES = [
    'BREAKTHROUGH_BT1607_BT1609_ENTROPY_DUAL.md',
    'BT1607_witting_entropy_budget.json',
    'BT1607_witting_entropy_budget.py',
    'BT1608_self_calibrating_feedback.json',
    'BT1608_self_calibrating_feedback.py',
    'BT1609_algebraic_dual_stack.json',
    'BT1609_algebraic_dual_stack.py',
]

def main() -> None:
    rows = []
    for p in FILES:
        path = ROOT / p
        exists = path.exists()
        size = path.stat().st_size if exists else None
        rows.append({'path': p, 'exists': exists, 'size_bytes': size, 'empty_or_missing': (not exists) or size == 0})
    checks = {
        'seven_files_checked': len(rows) == 7,
        'all_paths_accounted': all(r['path'] for r in rows),
        'empty_or_missing_detected': any(r['empty_or_missing'] for r in rows),
        'claim_must_be_blocked_until_backfilled': True,
    }
    result = {
        'bt': 1612,
        'title': 'Empty artifact and backfill audit',
        'verified': all(checks.values()),
        'source_commit': 'fd90bad5f790b8f6401b2c96af5956842a95b2ad',
        'artifact_rows': rows,
        'interpretation': 'The BT1607-BT1609 entropy/feedback/dual-stack commit appears as a set of empty or missing placeholder artifacts in the current connector view. Its ideas may be valuable, but the claims must remain blocked until content is backfilled and validated.',
        'honesty_boundary': 'This audit does not delete or repair the placeholders. It flags them as non-evidence until backfilled.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1612 Empty Artifact and Backfill Audit\n\nThe BT1607-BT1609 entropy/feedback/dual-stack commit currently appears as empty placeholder artifacts in the connector view. These ideas may be valuable, but they are not evidence until backfilled and validated. Claims based on them remain blocked.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1612: BT1607--BT1609 entropy/feedback/dual-stack placeholders are flagged as non-evidence until backfilled and validated.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1612,'verified':result['verified'],'empty_or_missing':sum(r['empty_or_missing'] for r in rows)}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
