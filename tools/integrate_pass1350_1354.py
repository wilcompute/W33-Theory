#!/usr/bin/env python3
"""Idempotently integrate Passes 1340--1344 and 1350--1354 into both papers.

Also repairs the pre-existing unescaped-underscore fatal error in Part XXII.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGETS=[ROOT/'w33_paper.tex',ROOT/'photonic_holonet.tex']
INPUTS=[r'\input{analysis/BT1340_BT1344_cartan_atlas_selector_padic}',r'\input{analysis/BT1350_BT1354_brauer_basic_atlas_geometry_pdf}']
PART22=ROOT/'manuscripts/tex/part22_fano_synthesis.tex'

def ensure_once(path:Path,line:str):
    text=path.read_text()
    text=text.replace(line+'\n','').replace(line,'')
    marker=r'\end{document}'
    if marker not in text: raise RuntimeError(f'{path}: no end document marker')
    text=text.replace(marker,'\n'+line+'\n\n'+marker,1)
    path.write_text(text)

def repair_part22():
    text=PART22.read_text()
    bad='PASS1150_SHIFTED_ADJACENCY_RETRACTION'
    good=r'PASS1150\_SHIFTED\_ADJACENCY\_RETRACTION'
    if bad in text:text=text.replace(bad,good)
    PART22.write_text(text)
    assert good in PART22.read_text()

def main():
    repair_part22()
    for target in TARGETS:
        for line in INPUTS: ensure_once(target,line)
        text=target.read_text()
        for line in INPUTS: assert text.count(line)==1
    print('PASS 1354: repaired Part XXII and integrated both theorem packets exactly once')
if __name__=='__main__':main()
