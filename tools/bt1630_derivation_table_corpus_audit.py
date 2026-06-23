#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1630_derivation_table_corpus_audit.json'
MD = ROOT / 'analysis' / 'BT1630_derivation_table_corpus_audit.md'
TEX = ROOT / 'analysis' / 'BT1630_derivation_table_corpus_audit.tex'

CANDIDATES = [
    {'path':'exploration/w33_complete_sm_derivation.py','format':'py','priority':'canonical_extracted','reason':'current BT1621 source for 19 SM rows'},
    {'path':'src/COMPLETE_SOLUTION.py','format':'py','priority':'high','reason':'search hit for SM/CKM/PMNS/Higgs table-like derivations'},
    {'path':'UNIFIED_MASTER_THEOREM.py','format':'py','priority':'high','reason':'search hit for master theorem / physics derivation content'},
    {'path':'docs/COMPLETE_SUMMARY.md','format':'md','priority':'high','reason':'markdown summary likely contains consolidated derivation tables'},
    {'path':'docs/ARXIV_PREPRINT_DRAFT.md','format':'md','priority':'medium','reason':'preprint draft may duplicate or supersede tables'},
    {'path':'W36_PAPER_DRAFT.md','format':'md','priority':'medium','reason':'paper draft with potential physics tables'},
    {'path':'docs/w33_complete_theory.html','format':'html','priority':'high','reason':'HTML complete theory page with tables'},
    {'path':'docs/w33_website.html','format':'html','priority':'high','reason':'website HTML table source'},
    {'path':'docs/qutrit_foundation.html','format':'html','priority':'medium','reason':'qutrit HTML table source'},
    {'path':'docs/w33_q_integers_complete.html','format':'html','priority':'medium','reason':'q-integer HTML table source'},
    {'path':'docs/w33_monster_landauer.html','format':'html','priority':'medium','reason':'Landauer/Monster HTML tables'},
    {'path':'docs/w33_monster_landauer_final.html','format':'html','priority':'medium','reason':'final Landauer/Monster HTML tables'},
    {'path':'docs/temporal_spectral_toroidal_computer.html','format':'html','priority':'medium','reason':'temporal/spectral/toroidal computer tables'},
    {'path':'w33_closure_package_v2/previous_bundle_contents/w33_tables_full.jsonl','format':'jsonl','priority':'high','reason':'bundled extracted table corpus'},
    {'path':'w33_closure_package_v2/previous_bundle_contents/w33_theorems_695.csv','format':'csv','priority':'medium','reason':'theorem table corpus'},
]

NEXT_ACTIONS = [
    {'action':'table_inventory','description':'count tables/rows/headers in html, markdown, csv, and jsonl candidates'},
    {'action':'formula_deduplication','description':'normalize formulas and compare against BT1621 canonical rows'},
    {'action':'claim_tier_assignment','description':'mark each discovered row as exact, algebraic-source-only, duplicate, obsolete, speculative, or blocked'},
    {'action':'promotion_queue','description':'only promote nonduplicate rows into canonical parameter/observable tables after audit'},
]

def main() -> None:
    fmt_counts = {}
    for c in CANDIDATES:
        fmt_counts[c['format']] = fmt_counts.get(c['format'], 0) + 1
    checks = {
        'fifteen_candidates': len(CANDIDATES) == 15,
        'has_html_candidates': fmt_counts.get('html', 0) >= 6,
        'has_markdown_candidates': fmt_counts.get('md', 0) >= 3,
        'has_python_candidates': fmt_counts.get('py', 0) >= 3,
        'has_table_bundle': any(c['format'] == 'jsonl' for c in CANDIDATES),
        'has_index_related_html': any('w33_complete_theory.html' in c['path'] or 'w33_website.html' in c['path'] for c in CANDIDATES),
        'four_next_actions': len(NEXT_ACTIONS) == 4,
    }
    result = {
        'bt': 1630,
        'title': 'Derivation/table corpus audit',
        'verified': all(checks.values()),
        'candidate_rows': CANDIDATES,
        'format_counts': fmt_counts,
        'next_actions': NEXT_ACTIONS,
        'interpretation': 'The SM bridge cannot rely only on exploration/w33_complete_sm_derivation.py. Search results show additional derivation/table reservoirs in Python, markdown, HTML, and prior bundle files. These must be inventoried and deduplicated before promotion into canonical rows.',
        'honesty_boundary': 'Audit inventory only; it does not claim the listed candidates are correct, current, or nonduplicative.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    lines = ['# BT1630 Derivation/Table Corpus Audit', '', 'Candidate derivation/table reservoirs:']
    for c in CANDIDATES:
        lines.append(f"- `{c['path']}` ({c['format']}, {c['priority']}): {c['reason']}")
    lines += ['', 'Next actions:']
    for a in NEXT_ACTIONS:
        lines.append(f"- **{a['action']}**: {a['description']}")
    MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1630: derivation/table reservoirs across Python, Markdown, HTML, CSV, and JSONL are inventoried before any new canonical promotion.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1630,'verified':result['verified'],'candidates':len(CANDIDATES)}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__': main()
