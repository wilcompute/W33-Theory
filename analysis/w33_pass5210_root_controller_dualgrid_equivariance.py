#!/usr/bin/env python3
"""Pass5210: the root controller and the dual-grid footprint are one Borel action.

The four canonical U(q) controller coordinates are the four positive C2 root
coordinates.  With simple roots alpha,beta, the positive-root characters are

  alpha, beta, alpha+beta, 2alpha+beta.

Hence the standard split torus T acts by

  (a,b,c,d) -> (r a, s b, r s c, r^2 s d),

exactly the Pass5192 metric automorphism.  Thus Pass5192's split torus is the
root-character conjugation action of the Borel normalizer B=U(q) semidirect T.

Pass5187 identifies P components with hyperbolic polar-line pairs, i.e. dual
grids, and Pass5186 identifies their incidence with W-points.  Both W-points and
dual grids are canonical PSp4(q)-sets.  Therefore for every g in PSp4(q), and
in particular g in B,

  P_pts(g) F = F P_grid(g),

where F is point x dual-grid incidence.  Transposing gives an equivariant
footprint map.  Consequently the root-controller moves and the split-torus
normalizations act by coordinate permutations on the footprint code and on the
Pass5203 P-component block SRG.

This is the precise fusion: it does not identify the q^4 controller states with
the q^2(q^2+1)/2 dual-grid coordinates.  Rather, both are modules/sets for the
same Borel symmetry and F is an intertwiner between the geometric permutation
representations.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5210_ROOT_CONTROLLER_DUALGRID_EQUIVARIANCE.json'

def main():
    roots=['alpha','beta','alpha+beta','2alpha+beta']
    chars=['r','s','r*s','r^2*s']
    assert len(roots)==len(chars)==4
    out={'pass':5210,'status':'THEOREM_ROOT_CONTROLLER_DUALGRID_BOREL_EQUIVARIANCE',
      'root_system':'C2','positive_roots':roots,
      'split_torus_characters':chars,
      'Pass5192_action':'phi_{r,s}(a,b,c,d)=(ra,sb,rsc,r^2sd)',
      'group_identification':'The controller U(q) is the standard C2 unipotent radical; the Pass5192 torus is its split-root torus normalizer action.',
      'geometric_actions':'PSp4(q) acts canonically on W(3,q) points and on hyperbolic polar-pair dual grids/P components.',
      'intertwiner':'For every g, P_pts(g) F = F P_grid(g); hence F^T is equivariant in the reverse permutation representations.',
      'code_consequence':'U(q) and the split torus act by automorphisms of the P-footprint code; the same action preserves the Pass5203 dual-grid block SRG.',
      'controller_consequence':'Root-metric normalization may be transported through F without changing footprint Hamming weight or block-graph incidence type.',
      'firewall':'There is no asserted bijection between q^4 U(q) states and q^2(q^2+1)/2 dual grids. The theorem is an equivariant-module bridge.',
      'boundary':'Finite group/geometry symmetry theorem only; no hardware timing or apartment minimum-distance claim follows automatically.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
