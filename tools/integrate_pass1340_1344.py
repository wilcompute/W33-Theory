#!/usr/bin/env python3
"""Idempotently integrate the Passes 1340--1344 theorem insert."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TARGETS=(ROOT/'w33_paper.tex',ROOT/'photonic_holonet.tex')
LINE=r'\input{analysis/BT1340_BT1344_cartan_atlas_selector_padic}'
START='% BEGIN PASS1340-1344 EXACT INSERT'
END='% END PASS1340-1344 EXACT INSERT'
BLOCK=f'{START}\n{LINE}\n{END}\n'


def integrate(path:Path)->None:
    text=path.read_text()
    while START in text:
        a=text.index(START);b=text.index(END,a)+len(END)
        if b<len(text) and text[b]=='\n':b+=1
        text=text[:a]+text[b:]
    marker=r'\end{document}'
    if marker not in text:raise RuntimeError(f'{path} has no end document marker')
    text=text.replace(marker,BLOCK+marker,1)
    path.write_text(text)
    assert path.read_text().count(LINE)==1


def main():
    for path in TARGETS:integrate(path)
    print('PASS: Passes 1340-1344 integrated exactly once into both manuscripts')

if __name__=='__main__':main()
