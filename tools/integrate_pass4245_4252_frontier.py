#!/usr/bin/env python3
"""Numerically ordered frontier reconciler for Passes 4245-4252."""
from __future__ import annotations
import argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'
LINE=r'\input{analysis/BT4245_BT4252_residual_symmetry_ghz_hodge_route_lattice_outside_box_insert}%'
NEXT=r'\input{analysis/BT4253_BT4260_girth16_faultaware_su4_hysteresis_clock_channel_scrambling_modular_capacity_insert}%'

def reconciled(text:str)->str:
    lines=[x for x in text.splitlines() if x.strip()!=LINE]
    try:i=next(i for i,x in enumerate(lines) if x.strip()==NEXT)
    except StopIteration:i=len(lines)
    lines.insert(i,LINE)
    return '\n'.join(lines)+'\n'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
    old=MANIFEST.read_text();new=reconciled(old)
    if args.check:
        if old!=new:raise SystemExit('frontier manifest requires reconciliation')
    else:MANIFEST.write_text(new)
if __name__=='__main__':main()
