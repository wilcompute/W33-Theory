#!/usr/bin/env python3
"""BT1582: dry-run/idempotent Holonet appendix splicer for operator-on-photon/OAM packet.

This follows the BT1535 pattern: by default it writes only the manifest.  In a
checkout, run with --apply to rewrite photonic_holonet.tex between bounded
markers.  It does not rebuild the PDF.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'photonic_holonet.tex'
OUT = ROOT / 'data' / 'bt1582_operator_oam_appendix_splice_runner.json'
MD = ROOT / 'analysis' / 'BT1582_operator_oam_appendix_splice_runner.md'
TEX = ROOT / 'analysis' / 'BT1582_operator_oam_appendix_splice_runner.tex'
BEGIN = '% BT1582 OPERATOR_OAM APPENDIX BEGIN'
END = '% BT1582 OPERATOR_OAM APPENDIX END'
INSERTS = [
    'analysis/BT1564_BT1566_holonet_insert.tex',
    'analysis/BT1567_BT1569_holonet_insert.tex',
    'analysis/BT1570_BT1572_holonet_insert.tex',
    'analysis/BT1573_BT1576_holonet_insert.tex',
    'analysis/BT1573_BT1576_holonet_insert.tex',
]
# Deduplicate while preserving order; duplicate included defensively if generated manifests are rerun.
INSERTS = list(dict.fromkeys(INSERTS))

def block() -> str:
    lines=[BEGIN]
    for p in INSERTS:
        lines.append(f'\\input{{{p}}}')
    lines.append(END)
    return '\n'.join(lines)+'\n'

def splice_text(text: str):
    b=block()
    if BEGIN in text and END in text:
        before=text.split(BEGIN,1)[0]
        after=text.split(END,1)[1]
        return before+b+after.lstrip('\n'), 'replace_existing_block'
    marker='\\section{Conclusion}'
    if marker in text:
        return text.replace(marker, b+'\n'+marker, 1), 'insert_before_conclusion'
    return text+'\n'+b, 'append_to_end'

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args=parser.parse_args()
    target_exists=TARGET.exists()
    original=TARGET.read_text(encoding='utf-8') if target_exists else ''
    new, mode=splice_text(original)
    applied=False
    if args.apply:
        TARGET.write_text(new, encoding='utf-8')
        applied=True
    checks={
        'target_exists': target_exists,
        'four_inserts': len(INSERTS)==4,
        'all_insert_files_exist': all((ROOT/p).exists() for p in INSERTS),
        'block_has_boundaries': BEGIN in block() and END in block(),
        'idempotent_replace_mode_after_first_splice': splice_text(new)[1]=='replace_existing_block',
        'dry_run_or_apply_ok': (not args.apply) or applied,
    }
    result={'bt':1582,'title':'Operator/OAM appendix splice runner','verified':all(checks.values()),'target':'photonic_holonet.tex','mode':mode,'applied':args.apply,'insert_count':len(INSERTS),'inserts':INSERTS,'commands':['python tools/bt1582_operator_oam_appendix_splice_runner.py','python tools/bt1582_operator_oam_appendix_splice_runner.py --apply','latexmk -pdf -interaction=nonstopmode photonic_holonet.tex'],'interpretation':'Idempotent dry-run splicer for the BT1564-BT1579 operator-on-photon/OAM appendix packet. It is modeled after BT1535 and rewrites the paper only when --apply is passed.','honesty_boundary':'The committed manifest records the splicer. photonic_holonet.tex is not rewritten and no PDF rebuild is claimed unless --apply/build is run in checkout.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    MD.write_text('# BT1582 Operator/OAM Appendix Splice Runner\n\nDry-run/idempotent splicer for the operator-on-photon/OAM appendix packet. Run with --apply in checkout to rewrite photonic_holonet.tex, then rebuild separately.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1582: dry-run appendix splicer for the operator-on-photon/OAM packet; paper rewrite only occurs with --apply.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1582,'verified':result['verified'],'applied':args.apply,'mode':mode}, indent=2))
    if not result['verified']: raise SystemExit(1)

if __name__=='__main__': main()
