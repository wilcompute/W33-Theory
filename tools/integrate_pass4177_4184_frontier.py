#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"analysis/W33_CURRENT_FRONTIER_MANIFEST.tex"
LINE=r"\input{analysis/BT4177_BT4184_af_nogo_twobody_hodge_pdk_interval_bonkers_insert}%"
NEXT=r"\input{analysis/BT4185_BT4192_adaptive_c2_hawking_hysteresis_3local_cover_holonomy_ihara_heat_insert}%"
PREV=r"\input{analysis/BT4169_BT4176_discrete_c2_hawking_backreaction_gray_levi_casimir_axion_insert}%"
def reconciled(text:str)->str:
    lines=[x for x in text.splitlines() if x.strip()!=LINE]
    try:i=next(i for i,x in enumerate(lines) if x.strip()==NEXT)
    except StopIteration:
        try:i=next(i for i,x in enumerate(lines) if x.strip()==PREV)+1
        except StopIteration:i=len(lines)
    lines.insert(i,LINE)
    return "\n".join(lines)+"\n"
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true");args=ap.parse_args()
    old=MANIFEST.read_text();new=reconciled(old)
    if args.check:
        if old!=new:raise SystemExit("frontier manifest requires reconciliation")
    else:MANIFEST.write_text(new)
if __name__=="__main__":main()
