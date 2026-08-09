#!/usr/bin/env python3
"""Pass 4523 -- primitive-six Ihara tomography for every thick GQ(s,t).

For a line-signed point graph of a finite generalized quadrangle GQ(s,t), let
C6(sigma) be the signed sum over oriented primitive nonbacktracking prime classes
of length six.  Its degree-two Walsh coefficient for a pair of geometric lines
has exactly two values:

  c_dis = s(s+1)(s-1)^2,
  c_adj = s^2(s-1)^2(2t+1).

Proof decomposition. A length-six prime with parity support on exactly two line
labels is either:
  (i) a simple hexagon supported by an apartment containing the pair, or
  (ii) for an intersecting pair only, a figure-eight made from one triangle on
       each line.
For a fixed pair the apartment counts are alpha=s^2 t if the lines intersect
and beta=s(s+1)/2 if they are disjoint.  Every apartment contributes
2(s-1)^2 oriented primitive classes to that parity pair; the figure-eight adds
s^2(s-1)^2 for an intersecting pair.  Therefore the formulas above follow.
The imprimitive double traversal of a triangle has zero parity support and does
not enter degree two.

Their difference is s(s-1)^2(2st-1)>0 for every thick GQ, so the degree-two
Walsh coefficient matrix of C6 reconstructs the line-intersection graph exactly.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4523_GENERAL_GQ_C6_TOMOGRAPHY.json'


def coefficients(s:int,t:int):
    assert s>1 and t>1
    beta=s*(s+1)//2
    alpha=s*s*t
    apartment_factor=2*(s-1)**2
    simple_dis=apartment_factor*beta
    simple_adj=apartment_factor*alpha
    figure8=s*s*(s-1)**2
    c_dis=simple_dis
    c_adj=simple_adj+figure8
    gap=c_adj-c_dis
    assert c_dis==s*(s+1)*(s-1)**2
    assert c_adj==s*s*(s-1)**2*(2*t+1)
    assert gap==s*(s-1)**2*(2*s*t-1)>0
    return {'s':s,'t':t,'disjoint':c_dis,'adjacent':c_adj,'gap':gap,
            'simple_disjoint':simple_dis,'simple_adjacent':simple_adj,
            'figure_eight_adjacent':figure8}


def main()->int:
    regressions=[coefficients(*st) for st in [(2,2),(3,3),(5,5),(3,9),(9,3)]]
    expected={(2,2):(6,20),(3,3):(48,252),(5,5):(480,4400),(3,9):(48,684),(9,3):(5760,36288)}
    for r in regressions:
        assert (r['disjoint'],r['adjacent'])==expected[(r['s'],r['t'])]
    out={
      'pass':4523,
      'theorem':'primitive length-six degree-two Walsh tomography reconstructs the line graph of every thick finite GQ(s,t)',
      'coefficients':{
        'disjoint':'s(s+1)(s-1)^2',
        'adjacent':'s^2(s-1)^2(2t+1)',
        'difference':'s(s-1)^2(2st-1)>0'},
      'derivation':{
        'apartments_per_intersecting_pair':'alpha=s^2 t',
        'apartments_per_disjoint_pair':'beta=s(s+1)/2',
        'oriented_simple_hexagons_per_apartment_pair':'2(s-1)^2',
        'extra_adjacent_figure_eights':'s^2(s-1)^2',
        'imprimitive_triangle_twice':'zero parity support'},
      'matrix_reconstruction':'off-diagonal M6 = c_dis*(J-I) + (c_adj-c_dis)*A_line',
      'regressions':regressions,
      'boundary':'Finite graph-zeta theorem. It reconstructs incidence/line adjacency, not a physical gauge field.'}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__': raise SystemExit(main())
