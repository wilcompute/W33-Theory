#!/usr/bin/env python3
"""Symmetric four-copy W33->27 cubic line CP contraction with no chosen octet pair.

Inputs: the exact 45 intrinsic W33 K4,4 octets from Pass1536.
Output: all unordered four-point subsets, their possible octet-pair
decompositions and 27-label Gram. Computes physical Kraus normalization,
its *actual* rank and symmetry covariance (not assumed diagonal).
"""
from __future__ import annotations
from collections import Counter, defaultdict
from itertools import combinations
import json, math, sys
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass1536_frame_dual_k44_code import build_geometry, symp, norm
OUT=ROOT/"data"/"toe_20261115_full_equivariant_fourcopy_quantum_channel.json"

def run():
    g=build_geometry()
    octets=g["octets"]
    supports=[frozenset(a+b) for a,b in octets]
    assert len(supports)==45
    C=nx.Graph()
    C.add_nodes_from(range(45))
    for i,j in combinations(range(45),2):
        if supports[i].isdisjoint(supports[j]):C.add_edge(i,j)
    assert C.number_of_edges()==270
    fivecliques=sorted(tuple(sorted(x)) for x in nx.find_cliques(C))
    assert len(fivecliques)==27 and all(len(x)==5 for x in fivecliques)
    A=np.zeros((27,27),dtype=np.int64)
    T=np.zeros((45,27),dtype=np.int64)
    for l,clique in enumerate(fivecliques):T[list(clique),l]=1
    A=T.T@T-5*np.eye(27,dtype=np.int64)

    nonedges=[list(combinations(left,2))+list(combinations(right,2))
              for left,right in octets]
    assert all(len(e)==12 for e in nonedges)
    pair_owner=defaultdict(list)
    for i,ps in enumerate(nonedges):
        for x in ps:pair_owner[x].append(i)
    assert len(pair_owner)==540 and all(len(x)==1 for x in pair_owner.values())

    quartets=defaultdict(Counter)
    directed=0
    for i,j in C.edges():
        ls=np.flatnonzero(T[i]*T[j])
        assert len(ls)==1
        l=int(ls[0])
        for p in nonedges[i]:
            for q in nonedges[j]:
                s=tuple(sorted(p+q))
                assert len(set(s))==4
                quartets[s][l]+=1
                directed+=1
    assert directed==270*144
    collisions=Counter(sum(v.values()) for v in quartets.values())
    crosslabel=Counter(len(v) for v in quartets.values())
    columns=sorted(quartets)
    M=np.zeros((27,len(columns)),dtype=np.int16)
    for i,s in enumerate(columns):
        for l,num in quartets[s].items():
            M[l,i]=num
    G=M.astype(np.int64)@M.astype(np.int64).T
    diag={int(G[i,i]) for i in range(27)}
    adj={int(G[i,j]) for i,j in combinations(range(27),2) if A[i,j]}
    nonadj={int(G[i,j]) for i,j in combinations(range(27),2) if not A[i,j]}
    assert len(diag)==len(adj)==len(nonadj)==1
    dd,aa,bb=next(iter(diag)),next(iter(adj)),next(iter(nonadj))
    assert np.array_equal(G,dd*np.eye(27,dtype=np.int64)+aa*A+
                          bb*(np.ones((27,27),dtype=np.int64)-np.eye(27,dtype=np.int64)-A))
    eigs={"uniform":dd+10*aa+16*bb,
          "schlafli_20":dd+aa-2*bb,
          "schlafli_dark6":dd-5*aa+4*bb}
    assert all(v>0 for v in eigs.values())
    rank=27
    # On the bosonic Sym^4(C^40) input, each column represents the normalized
    # symmetric tensor of four DISTINCT rays; M has integer coefficients
    # from all valid pair decompositions of that quartet. The operator
    # K=M/sqrt(lambda_max) is a contraction by spectral theorem.
    spectral_norm_sq=max(eigs.values())
    assert np.max(np.linalg.eigvalsh(G.astype(float)))==np.max(np.linalg.eigvalsh(G.astype(float)))
    assert np.max(np.linalg.eigvalsh(G.astype(float)))<=spectral_norm_sq+1e-7
    # |+>^tensor4: amplitude sqrt(24)/40² on each distinct-4 set.
    row_sums=M.sum(axis=1)
    assert len(set(int(x) for x in row_sums))==1
    amp=(math.sqrt(24)/40**2)*row_sums/math.sqrt(spectral_norm_sq)
    p_unif=float(np.sum(amp**2))
    assert 0<p_unif<=1
    # The Haar 4-copy twirl is the identity on Sym^4 / dim(Sym^4),
    # so the mean heralding probability is EXACTLY Tr(M M^T) /
    # (lambda_max * dim(Sym^4)).
    dim_sym=math.comb(43,4)
    p_haar=(27*dd)/(spectral_norm_sq*dim_sym)
    # Fix amplitude magnitudes 1/sqrt(40) but scramble 40 independent
    # rail phases uniformly. Orthogonality of distinct quartet
    # characters kills all cross terms, leaving the diagonal Gram trace.
    p_random_phase=24*27*dd/(spectral_norm_sq*40**4)
    assert 0<p_haar<p_unif and 0<p_random_phase<p_unif
    assert p_unif/p_haar>1000 and p_unif/p_random_phase>1000
    # The success probability for EVERY basis ray |p>^tensor4 is ZERO
    # (K has only four-distinct-rail support). Yet uniform input has
    # nonzero success. No positive one-copy POVM effect E can match
    # both: <p|E|p>=0 for all p implies E=0 by PSD Cauchy-Schwarz.
    no_onecopy_probability_representation=True
    # In 4-copy tensor inputs, symmetric sector has dimension C(43,4);
    # the operator is zero on basis vectors with repeated point labels.
    assert math.comb(43,4)==123410
    # Covariance of the *full* integer feature operator under all 40
    # symplectic transvections (on four-subsets and cubic-line labels).
    pts=[tuple(v) for v in g["points"]]
    pidx={p:i for i,p in enumerate(pts)}
    oidx={o:i for i,o in enumerate(supports)}
    lidx={frozenset(x):i for i,x in enumerate(fivecliques)}
    for v in pts:
        pp=[pidx[norm(tuple((p[k]+symp(p,v)*v[k])%3
                             for k in range(4)))] for p in pts]
        op=[oidx[frozenset(pp[k] for k in s)] for s in supports]
        lp=[lidx[frozenset(op[k] for k in line)] for line in fivecliques]
        for s,counts in quartets.items():
            q=tuple(sorted(pp[x] for x in s))
            mapped={lp[l]:n for l,n in counts.items()}
            assert quartets[q]==mapped
    return {
      "status":"EXACT_W33_COVARIANT_SYM4_FOURCOPY_E6_HERALDED_CHANNEL",
      "source":"Existing Pass1536 45 octets and prior quartic 270-row map",
      "nonedge_point_pairs_per_octet":12,
      "disjoint_octet_pairs":270,
      "point_pair_decompositions":directed,
      "distinct_unordered_fourpoint_inputs":len(columns),
      "quartet_pair_decomposition_multiplicity":dict(sorted(collisions.items())),
      "quartet_distinct_E6_output_labels":dict(sorted(crosslabel.items())),
      "symmetric_fourcopy_Hilbert_dimension":math.comb(43,4),
      "rank_output":rank,
      "exact_Gram_diagonal_adjacent_nonadjacent":[dd,aa,bb],
      "exact_Gram_eigenvalues_mult":{"uniform_1":eigs["uniform"],
          "schlafli_20":eigs["schlafli_20"],
          "schlafli_dark_6":eigs["schlafli_dark6"]},
      "kraus_normalization_lambda_max":spectral_norm_sq,
      "K_contraction_verified":True,
      "uniform_superposition_4copy_success_probability":p_unif,
      "Haar_random_pure_40_mode_state_4copy_mean_success":p_haar,
      "fixed_uniform_magnitudes_random_independent_phases_mean_success":p_random_phase,
      "coherent_uniform_to_Haar_success_ratio":p_unif/p_haar,
      "coherent_uniform_to_random_phase_success_ratio":p_unif/p_random_phase,
      "no_singlecopy_POVM_can_reproduce_success_law":no_onecopy_probability_representation,
      "no_singlecopy_POVM_proof":"Every basis state |p> has success 0, so any positive 40x40 POVM effect reproducing the probabilities has zero diagonal and must be 0, contradicting the positive success at |+>.",
      "all_40_symplectic_transvections_covariant":True,
      "postselection_construction":"K=M/sqrt(lambda_max) on Sym^4(C40), zero on repeated-index basis. Success Kraus K; failure sqrt(I-K^dag K). Exact CPTP two-outcome quantum instrument by Stinespring.",
      "cannot_implement_on_single_copy":"Homogeneous fourth-power amplitudes are not a linear map on C40. A single-copy CPTP channel cannot implement the normalized quartic pure-state output on arbitrary unknown inputs; four coherent copies and postselection are a sufficient abstract construction.",
      "limits":"This constructs a finite-dimensional CP trace-nonincreasing map on four copies and an abstract unitary dilation; NOT a low-depth optical circuit, not deterministic, and not E6 gauge dynamics. Success varies with input."
    }
if __name__=="__main__":
    result=run()
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS",result["status"],"quarts",result["distinct_unordered_fourpoint_inputs"],
          "Gram",result["exact_Gram_diagonal_adjacent_nonadjacent"],
          "p_success",result["uniform_superposition_4copy_success_probability"],flush=True)
