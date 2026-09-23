#!/usr/bin/env python3
"""Audit whether the Hesse36 compiler lifts directly to frozen E8 matter81 roots.

The 36 compiler acts on non-fiber tritangent/control channels, not on the 81
root basis. This file builds the exact incidence maps in the same H27 x C3
address chart and asks how much of root space those channels see.

Results:
  * 27 x 36 ordinary-tritangent incidence has rank 21.
  * Tensoring/lifting through all six external phase permutations gives the
    81 x 216 ordinary E8-cubic incidence matrix of rank 73.
  * Adding the 54 fiber cubics does not increase rank: full 81 x 270 incidence
    still has rank 73, hence an 8-dimensional dark root complement.
  * Canonical E6 cubic signs and SU(3) epsilon parities only rescale columns by
    nonzero scalars, so they cannot change this rank.

Thus the 36 Fourier compiler does NOT define an invertible 81x81 root basis
change through cubic incidence alone. It does preserve the source-level scalar
selection rules (total Qpsi zero, matter parity even, one external phase of each
kind) because those hold on every cubic column, but an objectwise root action
requires additional target-side root/support data.
"""
from __future__ import annotations
import importlib.util,itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_hesse36_e8_matter81_root_lift_boundary.json"

def load_parent():
    path=ROOT/"analysis/w33_maximal_compiler_symmetry_pappus.py"
    s=importlib.util.spec_from_file_location("rootlift_parent",path); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def rank_q(M):
    A=[[Fraction(x) for x in row] for row in M]
    if not A:return 0
    m,n=len(A),len(A[0]); r=0
    for c in range(n):
        pivot=next((i for i in range(r,m) if A[i][c]),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r]
        z=A[r][c]; A[r]=[x/z for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                z=A[i][c]; A[i]=[A[i][j]-z*A[r][j] for j in range(n)]
        r+=1
        if r==m:break
    return r

def main(write=True):
    p=load_parent()
    directions=((0,0,1),(0,1,1),(1,0,1),(1,1,0),(1,2,2))
    def cyc(d): return frozenset((p.ID,d,p.hmul(d,d)))
    def cosets(d):
        S=cyc(d)
        return sorted({frozenset(p.hmul(g,h) for h in S) for g in p.H},
                      key=lambda X:tuple(sorted(X)))

    fiber=cosets(directions[0])
    ordinary=sorted({L for d in directions[1:] for L in cosets(d)},
                    key=lambda X:tuple(sorted(X)))
    full=sorted(set(fiber)|set(ordinary),key=lambda X:tuple(sorted(X)))
    assert (len(fiber),len(ordinary),len(full))==(9,36,45)

    H=sorted(p.H); hi={g:i for i,g in enumerate(H)}
    A36=[[0]*36 for _ in range(27)]
    A45=[[0]*45 for _ in range(27)]
    for j,L in enumerate(ordinary):
        for g in L:A36[hi[g]][j]=1
    for j,L in enumerate(full):
        for g in L:A45[hi[g]][j]=1
    r36=rank_q(A36); r45=rank_q(A45)
    assert r36==r45==21

    roots=[(g,q) for g in H for q in range(3)]
    ri={x:i for i,x in enumerate(roots)}
    def lift(lines):
        out=[]
        for L in lines:
            pts=sorted(L)
            for perm in itertools.permutations(range(3)):
                out.append(tuple((pts[k],perm[k]) for k in range(3)))
        return out
    ord216=lift(ordinary); fib54=lift(fiber); all270=ord216+fib54
    assert (len(ord216),len(fib54),len(all270))==(216,54,270)

    def incidence(instructions):
        B=[[0]*len(instructions) for _ in range(81)]
        for j,T in enumerate(instructions):
            for x in T:B[ri[x]][j]=1
        return B
    B216=incidence(ord216); B54=incidence(fib54); B270=incidence(all270)
    r216=rank_q(B216); r54=rank_q(B54); r270=rank_q(B270)
    assert (r216,r54,r270)==(73,45,73)

    ordinary_per_root=Counter(x for T in ord216 for x in T)
    fiber_per_root=Counter(x for T in fib54 for x in T)
    full_per_root=Counter(x for T in all270 for x in T)
    assert set(ordinary_per_root.values())=={8}
    assert set(fiber_per_root.values())=={2}
    assert set(full_per_root.values())=={10}
    assert all({q for _,q in T}=={0,1,2} for T in all270)

    carrier=json.loads((ROOT/"data/w33_e8_matter81_frame_qutrit_tensor_carrier.json").read_text())
    qpsi=json.loads((ROOT/"data/w33_qpsi_matter_parity_e8_d8_bridge.json").read_text())
    pauli=json.loads((ROOT/"data/w33_e8_matter81_pauli243_restriction.json").read_text())
    fullcompiler=json.loads((ROOT/"data/w33_hesse36_full_clifford648_fourier_compiler.json").read_text())
    assert carrier["cubic_lift"]["zero_sum_E8_triples"]==270
    assert carrier["cubic_lift"]["allowed_phase_multiset"]==[0,1,2]
    assert qpsi["E6_cubic"]["all_cubics_matter_parity_even"] is True
    assert all(sum(row["Qpsi"])==0 for row in qpsi["E6_cubic"]["patterns"])
    assert pauli["projective_weight_rays"]["orbit_count"]==9
    assert pauli["projective_weight_rays"]["orbit_size"]==9
    assert fullcompiler["compiler"]["rank"]==36

    out={
      "schema":"w33.hesse36_e8_matter81_root_lift_boundary.v1",
      "status":"PASS_DIRECT_81_ROOT_LIFT_THROUGH_CUBIC_INCIDENCE_HAS_RANK73_BOUNDARY",
      "headline":"The exact 36-state Fourier compiler does not become an invertible 81x81 root-coordinate compiler by incidence lifting. The ordinary 27x36 tritangent incidence has rank 21. Its 216 E8 cubic lifts already span rank 73 in the frozen 81-root chart; adding all 54 fiber cubics leaves rank 73, so cubic incidence has an intrinsic 8-dimensional dark complement. Canonical cubic signs and SU3 epsilon parities are nonzero column rescalings and cannot remove that defect.",
      "incidence":{"base_27x36_rank":r36,"base_27x45_rank":r45,
                   "ordinary_81x216_rank":r216,"fiber_81x54_rank":r54,
                   "full_81x270_rank":r270,"dark_root_dimension":81-r270,
                   "ordinary_cubics_per_root":8,"fiber_cubics_per_root":2,
                   "all_cubics_per_root":10},
      "selection_rules":{"all_270_are_zero_sum_E8_root_triples":True,
                         "external_phase_multiset_each_cubic":[0,1,2],
                         "all_E6_cubics_total_Qpsi_zero":True,
                         "all_E6_cubics_matter_parity_even":True,
                         "canonical_signs_cannot_change_incidence_rank":True},
      "pauli243_firewall":{"matter_rays":"9 projective orbits of size 9",
                           "compiler_carrier":"36 tritangent/control channels",
                           "direct_objectwise_identification":False},
      "verdict":"A root-level compiler needs extra target-side root/support data beyond the Hesse36 control transform. The exact finite lift currently closes on cubic instruction amplitudes, not on all 81 root basis vectors.",
      "boundary":"The numerical coincidence dark dimension 8 = rank(E8) is recorded only as a dimension count; no Cartan identification is asserted.",
      "checks":{"rank21_base":True,"rank73_ordinary_lift":True,"rank73_full270":True,
                "eight_plus_two_cubics_per_root":True,"phase_rule":True,
                "Qpsi_and_parity_selection_rules":True,"direct_81x81_lift_rejected":True}
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out
if __name__=="__main__":print(json.dumps(main(True),indent=2))
