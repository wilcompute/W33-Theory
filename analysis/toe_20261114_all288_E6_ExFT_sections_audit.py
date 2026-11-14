#!/usr/bin/env python3
"""Exact E6 ExFT: all 288 coordinate sections satisfy strong constraint,
are linearly maximal, and form two finite signed-Clifford orbits.
Reuses independently committed exact quadratic gauge-closure/Jacobiator
tests on representative 5D and 6D sections, and a bad-section witness.
"""
from itertools import combinations
from collections import Counter,deque
from pathlib import Path
import numpy as np,networkx as nx,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_E6_exft_generalized_closure_affine as L
import toe_20261114_exact_gaussian_us8_pauli_clock as E
import toe_20261113_e6_root_matching_projection_clock as R
OUT=ROOT/"data/toe_20261114_all288_E6_ExFT_sections_clifford_gauge.json"

def rank_mod(A,p=101):
    M=np.array(A,dtype=np.int64)%p
    m,n=M.shape;r=0
    for col in range(n):
        pivot=next((i for i in range(r,m) if M[i,col]),None)
        if pivot is None:continue
        if pivot!=r:M[[r,pivot]]=M[[pivot,r]]
        M[r]=(M[r]*pow(int(M[r,col]),-1,p))%p
        for row in range(r+1,m):
            if M[row,col]:M[row]=(M[row]-int(M[row,col])*M[r])%p
        r+=1
        if r==n:break
    return r

def main():
    T,Y,S5,S6=L.setup()
    _,terms,_,_,_=R.load()
    pauli,quad,nonquad,_=E.pauli_data()
    dic=json.loads((ROOT/"data/toe_20261114_exact_gaussian_integer_USp8_pauli_Albert_intertwiner.json").read_text())
    labels={int(i):v for i,v in dic["coordinate_to_pauli_label"].items()}
    inv={v:i for i,v in labels.items()}
    flips=set(dic["coordinate_negative_sign_indices"])
    P=[(-1 if i in flips else 1)*pauli[labels[i]] for i in range(27)]
    assert np.array_equal(np.einsum("imn,jmn->ij",T,T),10*np.eye(27,dtype=np.int64))
    G=nx.Graph();G.add_nodes_from(range(27))
    for t in terms:G.add_edges_from(combinations(t,2))
    maximal=[tuple(sorted(c)) for c in nx.find_cliques(nx.complement(G))]
    census=Counter(map(len,maximal))
    assert census=={5:216,6:72},census
    bysize={5:{s for s in maximal if len(s)==5},6:{s for s in maximal if len(s)==6}}
    assert S5 in bysize[5] and S6 in bysize[6]
    prime_rank_checks=0
    for S in maximal:
        assert all(not np.any(T[i,j,:]) for i in S for j in S)
        M=np.concatenate([T[i,:,:] for i in S],axis=0)
        assert M.shape==(27*len(S),27)
        assert rank_mod(M,101)==27-len(S),(S,"not linearly maximal")
        prime_rank_checks+=1
    action=[]
    for a in nonquad:
        mapping=[];signs=[]
        for i in range(27):
            v=labels[i]
            v2=v^a if E.omega(a,v) else v
            j=inv[v2]
            mat=1j*pauli[a]@P[i] if E.omega(a,v) else P[i]
            if np.array_equal(mat,P[j]):sg=1
            else:
                assert np.array_equal(mat,-P[j])
                sg=-1
            mapping.append(j);signs.append(sg)
        assert len(set(mapping))==27
        for tri,s in terms.items():
            im=tuple(sorted(mapping[i] for i in tri))
            assert im in terms
            assert terms[im]*np.prod([signs[i] for i in tri])==s
        action.append(mapping)
    orbits={}
    for dim in (5,6):
        available=set(bysize[dim]);sizes=[]
        while available:
            seed=min(available);orbit={seed};available.remove(seed);todo=deque([seed])
            while todo:
                curr=todo.popleft()
                for perm in action:
                    nxt=tuple(sorted(perm[i] for i in curr))
                    assert nxt in bysize[dim]
                    if nxt not in orbit:
                        orbit.add(nxt);available.remove(nxt);todo.append(nxt)
            sizes.append(len(orbit))
        orbits[str(dim)]=sorted(sizes)
    assert orbits=={"5":[216],"6":[72]}
    # Committed E6 cubic-compatible generalized Lie-derivative tests:
    # Exact polynomial arithmetic; out-of-section counterexample.
    r5=L.main()
    assert all(v["exact_integer_closure_residual_max"]==0 for v in r5["section_cases"].values())
    assert r5["bad_pair_control"]["closure_residual_max_integer"]>0
    # Quadratic previously certified and reviewed. Verify snapshot rather than
    # regenerating expensive samples here.
    quadcert=json.loads((ROOT/"data/toe_20261113_E6_ExFT_quadratic_closure_Jacobiator.json").read_text())
    assert quadcert["status"]=="PASS_QUADRATIC_E6_EXFT_CLOSURE_AND_TRIVIAL_JACOBIATORS"
    for rec in quadcert["records"].values():
        assert rec["closure_max_integer_residual"]==0
    result=dict(status="PASS_ALL_288_E6_COORDINATE_SECTIONS_STRONG_MAXIMAL_W_E6_ORBITS",
        max_coordinate_sections={"5":216,"6":72},
        all_288_section_self_annihilator_verified_via_rank_mod101=prime_rank_checks,
        all_288_strong_section_constraints=True,
        signed_clifford_generators=36,
        signed_cubic_preserving_actions_verified_36_times_45=True,
        five_section_orbits=orbits["5"],six_section_orbits=orbits["6"],
        Y="Y^{MK}{}_{NL}=C^{MKR} C_{NLR}; 10 d^MKR d_NLR with C contracted C=10I",
        affine_generalized_gauge_tests=r5["section_cases"],
        quadratic_closure_jacobiator_reused_certified=True,
        explicit_off_section_nonzero_closure_residual=r5["bad_pair_control"]["closure_residual_max_integer"],
        conclusion="All 288 maximal coordinate sections satisfy full bilinear strong E6 ExFT constraint and lie in exactly two signed Clifford orbits; existing exact affine and quadratic gauge tests cover one representative per orbit; published ExFT closure theorem extends to smooth constrained fields, not derived here.",
        limitations="Not a classification of all non-coordinate sections or gauge-fixing dynamics; not independent physical derivation of ExFT equations or spacetime dimension.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ("status","max_coordinate_sections","all_288_section_self_annihilator_verified_via_rank_mod101","five_section_orbits","six_section_orbits","explicit_off_section_nonzero_closure_residual")},indent=2),flush=True)
    return result
if __name__=="__main__":main()
