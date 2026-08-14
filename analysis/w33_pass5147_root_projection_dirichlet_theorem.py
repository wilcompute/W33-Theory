#!/usr/bin/env python3
"""Pass5147: all-q root-coset projection / Dirichlet mean-value theorem.

Let P_i be averaging over right cosets of the four positive-root subgroups H_i
of U(q).  Each P_i is the orthogonal projection onto right-H_i-invariant
functions.  Since each root-coset is a K_q in the Pass5132 theta Cayley graph,

    A_theta = q(P_0+P_1+P_2+P_3) - 4I,
    L_theta = q(4I-P_0-P_1-P_2-P_3).

Thus the theta Dirichlet form is exactly the sum of four root-direction
conditional variances.  This is the finite noncommutative mean-value/coarea
identity suggested by the chamber controller program.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5129_allq_intrinsic_unipotent_controller import roots,mm,I4

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5147_ROOT_PROJECTION_DIRICHLET_THEOREM.json'


def anchor(q):
    U,H,F=roots(q);idx={g:i for i,g in enumerate(U)};n=len(U)
    by_dir=[]
    all_edges=set()
    for R in H:
        cosets=set()
        for g in U:cosets.add(frozenset(idx[mm(g,h,F)] for h in R))
        assert len(cosets)==q**3 and {len(C) for C in cosets}=={q}
        # Cosets partition U for one root direction.
        seen=set()
        for C in cosets:
            assert not (seen&C);seen|=C
            for a in C:
                for b in C:
                    if a<b:all_edges.add((a,b))
        assert len(seen)==n
        by_dir.append(sorted(cosets,key=lambda C:tuple(sorted(C))))
    assert len(all_edges)==2*q**4*(q-1)

    # Exact integer Dirichlet identity on two deterministic nonconstant vectors.
    tests=[]
    vectors=[[(i%7)-3 for i in range(n)], [1 if (i*17+3)%11<5 else 0 for i in range(n)]]
    for x in vectors:
        lhs=sum((x[a]-x[b])**2 for a,b in all_edges)
        rhs=0
        for cosets in by_dir:
            for C in cosets:
                vals=[x[u] for u in C];s=sum(vals)
                rhs+=q*sum(v*v for v in vals)-s*s
        assert lhs==rhs
        tests.append(lhs)
    return {'q':q,'vertices':n,'root_directions':4,'cosets_per_direction':q**3,
            'theta_edges':len(all_edges),'dirichlet_test_values':tests,'identity_verified':True}


def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={
      'pass':5147,
      'status':'THEOREM_ALL_Q_ROOT_PROJECTION_DIRICHLET_MEAN_VALUE',
      'operator_identity':'A_theta = q(P0+P1+P2+P3)-4I; L_theta=q(4I-P0-P1-P2-P3)',
      'projection_definition':'Pi is conditional expectation/averaging on right cosets of the i-th positive-root subgroup Hi.',
      'dirichlet_identity':'<f,L_theta f> = q sum_i ||(I-Pi)f||^2 = sum_{theta edges {u,v}} |f(u)-f(v)|^2.',
      'indicator_coarea':'For S subset U(q), |delta_theta S| = q sum_i ||1_S-Pi 1_S||^2. Equivalently, each root-coset contributes k(q-k) when it contains k selected states.',
      'spectral_gap_reduction':'On mean-zero f, gap(A_theta)>=q is equivalent to sum_i ||Pi f||^2 <= 3||f||^2. Pass5137 proves the q^2-dimensional linear-character sector has equality at eigenvalue 3q-4; the nonlinear inequality remains the exact open target.',
      'anchors':A,
      'connection':'Pass5144 gives HH^T=4I+A_theta. This pass normalizes the four coset blocks into orthogonal conditional expectations and turns the same incidence geometry into an exact root-direction variance calculus.',
      'boundary':'The mean-value identity is all-q and exact. It does not by itself prove the all-q nonlinear spectral gap q, nor the all-q apartment-code distance theorem.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
