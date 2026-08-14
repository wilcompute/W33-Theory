#!/usr/bin/env python3
"""Pass5139 (bonkers): all-q minimum distance/classification of the chamber dependency code.

Pass5110 identified the kernel of chamber stars with the F2 cut space of the
Levi incidence graph.  The Levi graph is (q+1)-regular, girth 8, with second
adjacency eigenvalue sqrt(2q).  We prove every nontrivial edge cut has size
>q+1, so the minimum cuts are exactly vertex stars.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5139_ALLQ_CHAMBER_DEPENDENCY_MINIMUM.json'

def anchor(q):
    d=q+1;n=2*(q+1)*(q*q+1);E=(q+1)**2*(q*q+1);dim=n-1
    small_min=(d-2)*2+2 # forest bound at |S|=2; increases with |S|
    spectral_at_8=4*(d-math.sqrt(2*q))
    assert small_min>d and spectral_at_8>d
    return {'q':q,'length_chambers':E,'dimension_cut_space':dim,'minimum_distance':d,
            'minimum_words':n,'spectral_lower_bound_at_size8':spectral_at_8}

def main():
    A={str(q):anchor(q) for q in (2,3,4,5,7,11)}
    out={'pass':5139,'status':'THEOREM_ALL_Q_CHAMBER_DEPENDENCY_CODE_MINIMUM',
      'code_parameters':'[(q+1)^2(q^2+1), 2(q+1)(q^2+1)-1, q+1]_2',
      'minimum_word_count':'2(q+1)(q^2+1)',
      'minimum_word_classification':'Every minimum dependency is exactly the q+1 chambers incident with one Levi vertex (one point or one line panel star).',
      'proof':[
        'Pass5110 identifies the chamber-generator kernel with Cut(Levi;F2). The Levi graph is connected and (q+1)-regular, so vertex stars give cuts of size q+1.',
        'If 2<=|S|<=7, girth 8 makes the induced subgraph a forest, so |delta S| >= (q+1)|S|-2(|S|-1)=(q-1)|S|+2 > q+1.',
        'If 8<=|S|<=n/2, the Levi spectrum is ±(q+1), ±sqrt(2q),0. The Laplacian Rayleigh bound gives |delta S| >= (q+1-sqrt(2q))|S|(1-|S|/n) >= 4(q+1-sqrt(2q)) > q+1.',
        'The last strict inequality is equivalent after squaring to 9(q+1)^2>32q, i.e. 9q^2-14q+9>0, true for all q. Complements handle |S|>n/2.'
      ],
      'anchors':A,
      'connection':'This promotes the q=4 [425,169,5] A5=170 observation and q=2,3 anchors to the complete finite-generalized-quadrangle family.',
      'boundary':'This theorem concerns dependencies among chamber-star generators, not the minimum distance q^4 of the apartment code itself.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
