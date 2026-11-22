#!/usr/bin/env python3
"""Independent 40-ray/40-context Kochen-Specker uncolorability certificate.

This is REPOSITORY/LITERATURE PRIOR ART as a theorem: Penrose dodecahedron
and Witting 40-40 contextuality are known. Here the point is an executable
exact-cover proof and its relation to W(3,3) ovoid nonexistence and the
qutrit MUB/SIC orbit partition. Also checks why parity-only proofs fail.
"""
from __future__ import annotations
import itertools,json,functools
from pathlib import Path
import networkx as nx
import numpy as np
import toe_20261122_witting_one_phase_three_fixed as W
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_witting_KS_ovoid_firewall.json'


def dot(v,w):
    out=W.Z
    for x,y in zip(v,w):out=W.add(out,W.mul(W.conj(x),y))
    return out


def gf2_rank(A):
    M=A.copy().astype(np.uint8);k=0
    for j in range(M.shape[1]):
        if k==len(M):break
        nz=np.flatnonzero(M[k:,j])
        if not len(nz):continue
        t=k+int(nz[0]);M[[k,t]]=M[[t,k]]
        for t in range(len(M)):
            if t!=k and M[t,j]:M[t]^=M[k]
        k+=1
    return k


def verify():
    rays=W.all_rays();G=nx.Graph();G.add_nodes_from(range(40))
    G.add_edges_from((i,j) for i,j in itertools.combinations(range(40),2)
                     if dot(rays[i],rays[j])==W.Z)
    assert G.number_of_edges()==240
    bases=sorted(tuple(sorted(c)) for c in nx.find_cliques(G))
    assert len(bases)==40 and all(len(b)==4 for b in bases)
    incidence=np.zeros((40,40),dtype=np.uint8)
    for i,b in enumerate(bases):incidence[i,list(b)]=1
    assert np.all(incidence.sum(axis=0)==4)
    assert np.all(incidence.sum(axis=1)==4)
    # A noncontextual 0/1 valuation assigning one true ray per basis is
    # precisely a set of ten ray-stars partitioning 40 basis contexts.
    # This is the definition of an ovoid of the underlying W(3,3) GQ.
    cover=[sum(1<<i for i,b in enumerate(bases) if j in b) for j in range(40)]
    assert all(k.bit_count()==4 for k in cover)
    context_candidates=[[r for r in range(40) if c in bases[i]] for i,c in enumerate([])] # no-op
    candidates=[[r for r in range(40) if (cover[r]>>i)&1] for i in range(40)]
    assert all(len(q)==4 for q in candidates)
    states=0;edges=0
    @functools.lru_cache(maxsize=None)
    def solve(remaining):
        nonlocal states,edges
        states+=1
        if not remaining:return ()
        unfilled=[i for i in range(40) if remaining>>i&1]
        chosen=min(unfilled,key=lambda c:sum(cover[j]&remaining==cover[j] for j in candidates[c]))
        options=[j for j in candidates[chosen] if cover[j]&remaining==cover[j]]
        for j in options:
            edges+=1
            sol=solve(remaining^cover[j])
            if sol is not None:return (j,*sol)
        return None
    sol=solve((1<<40)-1)
    assert sol is None
    B=incidence.copy()
    rank=gf2_rank(B)
    parity_augmented_rank=gf2_rank(np.column_stack((B,np.ones(40,dtype=np.uint8))))
    assert rank==25 and parity_augmented_rank==25
    # Explicit parity-1 intersection witness in ray space: each context
    # meets this 12-point selection in 1 or 3 points, not necessarily 1.
    parity_witness=[3,7,17,20,22,24,26,27,29,33,36,38]
    intersections=incidence[:,parity_witness].sum(axis=1)
    assert set(intersections)=={1,3}
    assert np.all(intersections%2==1)
    return dict(status='PASS_EXACT_WITTING_40_40_KS_UNCOLORABILITY_OVOID_AND_PARITY_FIREWALL',
       ray_count=40,orthogonality_edges=240,orthogonal_complete_bases=40,
       incidence_per_ray=4,incidence_per_basis=4,
       ovoid_would_require_true_rays=10,
       exact_cover_ovoid_exists=False,
       exhaustive_dynamic_programming_distinct_states=states,
       exhaustive_dynamic_programming_branch_tests=edges,
       GF2_context_point_incidence_rank=rank,
       GF2_augmented_with_context_parity_rank=parity_augmented_rank,
       parity_only_context_proof_exists=False,
       explicit_12_ray_parity_odd_transversal=parity_witness,
       parity_transversal_context_intersection_histogram={str(int(k)):int(v) for k,v in zip(*np.unique(intersections,return_counts=True))},
       explanation='Exactly one selected ray in each basis implies an ovoid of W(3,3); exhaustive bitset exact-cover search proves none. The parity augmented matrix rank does not increase, so no odd number of context rows has even ray multiplicities. An explicit 12-ray GF2 valuation meets every context oddly but sometimes in three rays.',
       literature_prior='Witting/Penrose 40-40 KS is known (V. Waegell and P. K. Aravind, 2017, arXiv:1701.06512); W(3,q) odd-q ovoid obstruction is known. New here only the code-level tie-in to the explicit 30-effect SIC/MUB Witting partition.',
       physical_boundary='Contextuality is a theorem about potential quantum measurements, not a physical demonstration or a unique explanation of observed physics.')


def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print(d['status'],d['exhaustive_dynamic_programming_distinct_states'],d['exhaustive_dynamic_programming_branch_tests'])
if __name__=='__main__':main()
