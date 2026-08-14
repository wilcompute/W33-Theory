#!/usr/bin/env python3
"""Pass5162 (bonkers): all-q second weight of the chamber-dependency/cut code.

Pass5139 proves the chamber-generator dependency code is the binary cut space of
the Levi graph and that its minimum q+1 words are exactly vertex/panel stars.
The next shell is also uniform: the cut of two adjacent Levi vertices has weight
2q.  Girth eight excludes every other cut supported on at most seven vertices,
and the exact Levi spectral gap excludes all supports of size at least eight.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5162_ALLQ_DEPENDENCY_SECOND_WEIGHT.json'


def anchor(q):
    n=2*(q+1)*(q*q+1);k=q+1;E=(q+1)**2*(q*q+1)
    lam2=k-math.sqrt(2*q)
    spectral8=lam2*8*(1-8/n)
    assert spectral8>2*q
    return {'q':q,'Levi_vertices':n,'Levi_edges':E,'minimum_weight':q+1,
            'second_weight':2*q,'second_weight_words':E,
            'spectral_cut_lower_at_t8':spectral8}


def main():
    A={str(q):anchor(q) for q in (2,3,4,5,7,11)}
    out={'pass':5162,'status':'THEOREM_ALL_Q_DEPENDENCY_CODE_SECOND_WEIGHT',
      'statement':'For every finite q>=2, the binary chamber-dependency code Cut(Levi(W(3,q))) has minimum q+1 and second nonzero weight 2q. The weight-2q words are exactly cuts delta({u,v}) of adjacent point-line Levi vertex pairs.',
      'second_shell_multiplicity':'(q+1)^2(q^2+1), one word for each Levi edge/chamber.',
      'small_support_proof':'Choose the smaller shore S. For 2<=|S|<=7, Levi girth 8 implies the induced graph is a forest, so |delta S|=(q+1)|S|-2e(S)>2q except when |S|=2 and the two vertices are adjacent, where equality 2q holds.',
      'large_support_proof':'For 8<=t<=n/2, the Laplacian bound gives |delta S| >= (q+1-sqrt(2q))*t*(1-t/n). Since sqrt(2q)<=q/2+1, the gap is >=q/2; monotonicity on [0,n/2] gives |delta S|>=4q(1-8/n)>2q because n=2(q+1)(q^2+1)>16.',
      'uniqueness':'In a connected graph the binary cut map has kernel {empty,V}; hence a cut determines its shore up to complement, so the adjacent-pair cuts are distinct codewords.',
      'anchors':A,
      'boundary':'This is the chamber dependency/cut code, not the apartment code. It does not advance the q5 apartment-code minimum-distance theorem directly.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
