#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1629_pdf_table_release_manifest.json'
MD = ROOT / 'analysis' / 'BT1629_pdf_table_release_manifest.md'
TEX = ROOT / 'analysis' / 'BT1629_pdf_table_release_manifest.tex'

PDF = {
    'filename':'BT1621_BT1626_SM_bridge_comparator_table.pdf',
    'sha256':'aa8e74d5da2f37a0ceb1c63b391797bb32593abfeb546ac679c0de00176b3668',
    'bytes':4208,
    'pages':1,
    'artifact_scope':'chat artifact and release manifest, not committed binary',
}
CLAIMS = [
    {'row':'canonical_sm_table','status':'source_only','firewall':'not ABI-validated'},
    {'row':'observable_schema','status':'schema_only','firewall':'observable implementations incomplete'},
    {'row':'comparator_v2','status':'guarded','firewall':'zero PASS verdicts'},
    {'row':'pdf_table','status':'rendered_artifact','firewall':'visual summary only'},
]

def main() -> None:
    checks = {
        'pdf_filename_present': PDF['filename'].endswith('.pdf'),
        'sha256_len_64': len(PDF['sha256']) == 64,
        'one_page': PDF['pages'] == 1,
        'bytes_positive': PDF['bytes'] > 0,
        'four_claim_rows': len(CLAIMS) == 4,
        'zero_pass_firewall': any('zero PASS' in c['firewall'] for c in CLAIMS),
    }
    result = {
        'bt': 1629,
        'title': 'PDF/table release manifest',
        'verified': all(checks.values()),
        'pdf': PDF,
        'claim_firewall_rows': CLAIMS,
        'source_packets': {'table':'data/bt1626_sm_comparator_v2_untested_vs_missing.json','analysis':'analysis/BT1624_BT1626_sm_observable_comparator_v2.md'},
        'interpretation': 'The chat PDF table is tracked by filename, size, page count, and checksum. It is a visual release artifact for the guarded comparator, not a binary repo commit or validation claim.',
        'honesty_boundary': 'Manifest only; the PDF is a chat artifact and the table has zero PASS verdicts.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1629 PDF/Table Release Manifest\n\nThe SM bridge comparator PDF table is recorded by filename, size, page count, and SHA-256 checksum. It is a visual release artifact for the guarded comparator and does not validate any SM parameter. The comparator remains zero-PASS.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1629: SM bridge comparator PDF is recorded as a guarded release artifact with checksum and zero-PASS firewall.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1629,'verified':result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__': main()
