#!/usr/bin/env python3
"""Idempotently promote the shared Pass 1420 insert into both root manuscripts."""
from __future__ import annotations
import argparse
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TARGETS=[ROOT/'w33_paper.tex',ROOT/'photonic_holonet.tex']
INPUT='\\input{analysis/BT1420_frame_signed_turn_bridge_insert}'
ANCHOR='\\tableofcontents'

def patched(text:str)->str:
    if INPUT in text:return text
    if ANCHOR not in text:raise ValueError('missing table-of-contents anchor')
    return text.replace(ANCHOR,ANCHOR+'\n\n% Passes 1416--1420 shared exact bridge and evidence firewall\n'+INPUT,1)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
    changed=[]
    for path in TARGETS:
        if not path.exists():raise SystemExit(f'missing manuscript: {path}')
        old=path.read_text();new=patched(old)
        if a.check:
            if old!=new:raise SystemExit(f'Pass 1420 insert missing from {path.name}')
        elif old!=new:
            path.write_text(new);changed.append(path.name)
    print({'status':'PASS','changed':changed,'targets':[p.name for p in TARGETS]})
if __name__=='__main__':main()
