#!/usr/bin/env python3
"""Exact 51D E6-adjoint leakage test for the H27-address 132D carrier.

Uses the standard Z3 grading of e6: g0=sl3^3 (dim24),
g1=3 tensor 3 tensor 3 (dim27), g2=3bar tensor 3bar tensor 3bar (dim27).
We calculate ranks of [g1,g1] -> g2 and [g1,g2] -> g0 on elementary tensors,
using integer epsilon contractions and traceless marginal projections.
These ranks show the 27D chosen adjoint piece cannot be E6-invariant.
"""
from __future__ import annotations
from itertools import combinations,product
from pathlib import Path
import json
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/toe_20261122_round5_e6_grade_leakage.json'
labels=list(product(range(3),repeat=3))

def eps(a,b,c):
    if len({a,b,c})<3:return 0
    return 1 if (a,b,c) in ((0,1,2),(1,2,0),(2,0,1)) else -1

def rank_g1_g1():
    # Basis e_abc wedge e_def of wedge²(27), image in dual27.
    M=sp.zeros(27,351)
    for k,(i,j) in enumerate(combinations(range(27),2)):
        a,b,c=labels[i];d,e,f=labels[j]
        for r,(x,y,z) in enumerate(labels):
            M[r,k]=eps(a,d,x)*eps(b,e,y)*eps(c,f,z)
    return int(M.rank()),M

def rank_g1_g2():
    # [e_abc,e^def] has three traceless 3x3 contractions. Use
    # off-diagonals (6) plus two diagonal differences for each sl3.
    # Integer times three makes all entries integral.
    M=sp.zeros(24,729)
    for col,(v,w) in enumerate(product(range(27),repeat=2)):
        x=labels[v];y=labels[w]
        for factor in range(3):
            if any(x[k]!=y[k] for k in range(3) if k!=factor):continue
            a,b=x[factor],y[factor]
            if a!=b:
                off=[(i,j) for i in range(3) for j in range(3) if i!=j]
                M[factor*8+off.index((a,b)),col]=3
            else:
                # row 6: (diag0-diag1), row7: (diag1-diag2)
                M[factor*8+6,col]=int(a==0)-int(a==1)
                M[factor*8+7,col]=int(a==1)-int(a==2)
    return int(M.rank()),M

def verify():
    rank_gg,U=rank_g1_g1()
    rank_gh,V=rank_g1_g2()
    assert (U.shape,V.shape)==((27,351),(24,729))
    assert rank_gg==27 and rank_gh==24
    # Intertwiner's neutral adjoint slice is 27D g1; its E6 orbit
    # generates all 27 g2 and all 24 g0, hence 51 extra dimensions.
    assert 27+rank_gg+rank_gh==78
    return dict(status='PASS_E6_Z3_GRADED_51_DIRECTION_LEAKAGE_CERTIFICATE',
      target='132 = adjoint78 + fundamental27 + antifundamental27bar',
      adjoint_grading={'g0_sl3_cubed':24,'g1_tensor333':27,'g2_dual_tensor333':27},
      rank_bracket_g1_wedge_g1_to_g2=rank_gg,
      rank_bracket_g1_tensor_g2_to_g0=rank_gh,
      total_generated_e6_adjoint_dimension=27+rank_gg+rank_gh,
      necessary_adjoint_extra_directions=rank_gg+rank_gh,
      proof='Nonzero epsilon-epsilon-epsilon antisymmetric contraction spans g2, and traceless partial contractions of g1 x g2 span each of sl3 factors. The computed integer matrices have ranks 27 and 24 over Q.',
      physical_boundary='This is an E6 Lie-algebra irreducibility/leakage witness, NOT a dynamical leakage rate. No gauge Hamiltonian, energetic gap or error-correcting mechanism follows from representation containment.')
if __name__=='__main__':
 d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(d['status'],d['rank_bracket_g1_wedge_g1_to_g2'],d['rank_bracket_g1_tensor_g2_to_g0'])
