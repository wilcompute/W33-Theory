#!/usr/bin/env python3
"""Pass5203: P-component blocks form a 2-geometric SRG with Delsarte point cliques.

Use the point/P-component incidence matrix F from Pass5201/5202.  Two distinct
P-component point blocks intersect in either 0 or 2 W-points; declare two
components adjacent exactly in the latter case.  Since every block has
2(q+1) points and every W-point lies in q^2 blocks, the block graph has

  n = q^2(q^2+1)/2,
  k = (q+1)(q^2-1).

Pass5201 gives the integer point Gram

  FF^T=(q^2-1)I+(q-1)A_W+J.

The W point graph has eigenvalues q(q+1), q-1, -(q+1).  On the block side,

  F^T F = 2(q+1)I + 2 A_B,

so A_B has three eigenvalues

  k_B=(q+1)(q^2-1),
  r_B=q^2-2q-1,
  s_B=-(q+1).

Hence the block graph is strongly regular with

  lambda=3q^2-q-2,  mu=2q(q+1).

For any W-point p, its q^2 P components form a clique: two blocks through p
cannot intersect in one point, so they intersect in two and are adjacent.
The Delsarte clique bound is

  1-k_B/s_B=q^2,

so every point footprint is a maximum Delsarte clique.  Every block-graph edge
joins two blocks meeting in exactly two W-points, and therefore lies in exactly
two point-footprint cliques.  Thus the P-component block graph is a canonical
2-geometric SRG over the W-point clique family.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5203_P_COMPONENT_BLOCK_SRG_DELSARTE_CLIQUES.json'


def params(q):
    n=q*q*(q*q+1)//2;k=(q+1)*(q*q-1)
    lam=3*q*q-q-2;mu=2*q*(q+1)
    r=q*q-2*q-1;s=-(q+1)
    assert r+s==lam-mu and r*s==mu-k
    clique=1-k//s
    assert clique==q*q
    return {'q':q,'vertices_P_components':n,'degree':k,'lambda':lam,'mu':mu,
      'nontrivial_eigenvalues':[r,s],'Delsarte_clique_bound':clique,
      'point_footprint_clique_size':q*q,'edge_clique_ownership':2}

def main():
    A={str(q):params(q) for q in (3,5,7)}
    out={'pass':5203,'status':'THEOREM_P_COMPONENT_BLOCK_SRG_DELSARTE_POINT_CLIQUES',
      'family_parameters':'SRG(q^2(q^2+1)/2, (q+1)(q^2-1), 3q^2-q-2, 2q(q+1))',
      'spectrum':'k=(q+1)(q^2-1), r=q^2-2q-1, s=-(q+1)',
      'Delsarte_cliques':'The q^2 P components in a W-point footprint form a maximum clique attaining 1-k/s=q^2.',
      'two_geometric':'Every block-graph edge is contained in exactly two point-footprint Delsarte cliques, namely the two W-points in the 2-point intersection of its endpoint blocks.',
      'anchors':A,
      'q5':'SRG(325,144,68,60), spectrum 144^1,14^90,(-6)^234; 156 distinguished maximum 25-cliques from W-points.',
      'code_connection':'The Pass5201 footprint code is the binary span of the incidence vectors of these distinguished Delsarte cliques. Pass5202 identifies its generator-kernel quotient on the W-point side.',
      'boundary':'This identifies the exact block graph and maximum-clique carrier. It does not by itself prove that the binary clique-span has minimum distance 25, nor that the 156 distinguished point cliques are all maximum cliques.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
