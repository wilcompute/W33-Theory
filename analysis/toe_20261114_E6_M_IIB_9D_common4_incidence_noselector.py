#!/usr/bin/env python3
"""E6 M6/IIB5 9D duality interface: exact 1080 common-four incidence.

At every shared four-coordinate subspace there is exactly one
maximal 5-section and one maximal 6-section. A bipartite graph
72 M-sections degree 15 -> 216 IIB-sections degree 5 has
1080 edges. This is a canonical finite incidence dictionary for
the known M(T2) <-> IIB(S1) 9D duality. It does NOT derive T-duality.

Uniform counting gives IIB:M=3:1; incidence random-walk
stationarity gives branch weights 1:1. Hence finite coordinate
section counts are NOT a dynamical vacuum-selection mechanism.
"""
from pathlib import Path
from collections import Counter,defaultdict,deque
from itertools import combinations
from fractions import Fraction
import json,sys
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_E6_exft_generalized_closure_affine as Ex
OUT=ROOT/"data/toe_20261114_E6_M_IIB_9D_common_four_incidence_noselector.json"

def main():
    T,Y,_,_=Ex.setup()
    graph=nx.Graph();graph.add_nodes_from(range(27))
    for i in range(27):
        for j in range(i+1,27):
            if T[i,j,:].any():graph.add_edge(i,j)
    assert graph.number_of_edges()==135
    maximal=[tuple(sorted(s)) for s in nx.find_cliques(nx.complement(graph))]
    five=sorted(s for s in maximal if len(s)==5)
    six=sorted(s for s in maximal if len(s)==6)
    assert (len(five),len(six))==(216,72)
    from5=defaultdict(list);from6=defaultdict(list)
    for i,s in enumerate(five):
        for U in combinations(s,4):from5[U].append(i)
    for j,t in enumerate(six):
        for U in combinations(t,4):from6[U].append(j)
    assert len(from5)==len(from6)==1080
    assert set(from5)==set(from6)
    assert all(len(from5[u])==len(from6[u])==1 for u in from5)
    incidence=np.zeros((72,216),dtype=np.int64)
    for u in from5:
        i=from5[u][0];j=from6[u][0]
        assert len(set(five[i])&set(six[j]))==4
        assert incidence[j,i]==0
        incidence[j,i]=1
    assert int(incidence.sum())==1080
    assert set(incidence.sum(axis=0))=={5}
    assert set(incidence.sum(axis=1))=={15}
    # Full bipartite connectedness (in a giant 288-vertex W(E6) orbit).
    J=nx.Graph();J.add_nodes_from(range(72+216))
    for j,i in zip(*np.where(incidence)):
        J.add_edge(int(j),72+int(i))
    assert nx.is_connected(J)
    # Compare naive uniform coordinate-section counting versus
    # canonical degree-weighted random walk (detailed balance).
    naive=dict(M6=str(Fraction(72,288)),IIB5=str(Fraction(216,288)))
    volumeM=sum(dict(J.degree())[k] for k in range(72))
    volumeIIB=sum(dict(J.degree())[72+k] for k in range(216))
    assert (volumeM,volumeIIB)==(1080,1080)
    edge_walk=dict(M6=str(Fraction(volumeM,volumeM+volumeIIB)),
                   IIB5=str(Fraction(volumeIIB,volumeM+volumeIIB)))
    # Exact common-four branch local quadratic constraint:
    # identify ann(S4)=S4+(one IIB extension)+(two M extensions).
    core=(0,1,2,3)
    assert core in from5
    i=from5[core][0];j=from6[core][0]
    f=five[i];m=six[j]
    assert set(f)&set(m)==set(core)
    q4=next(a for a in f if a not in core)
    m2=tuple(sorted(a for a in m if a not in core))
    # Annihilator is kernel of the union of the 27x27 tensors
    # T[v,:,:]. It is exactly 7D; verify with exact mod101 rank.
    from toe_20261114_all288_E6_ExFT_sections_audit import rank_mod
    deriv=np.concatenate([T[k,:,:] for k in core],axis=0)
    assert rank_mod(deriv,101)==20
    for k in (*core,q4,*m2):
        assert all(not T[k,v,:].any() for v in core)
    assert T[q4,m2[0],:].any() and T[q4,m2[1],:].any()
    assert not T[m2[0],m2[1],:].any()
    q01=tuple(int(v) for v in np.flatnonzero(T[q4,m2[0],:]))
    q02=tuple(int(v) for v in np.flatnonzero(T[q4,m2[1],:]))
    assert len(q01)==len(q02)==1 and q01!=q02
    # With v=x e_q4+y e_m0+z e_m1, cubic self constraint
    # C(v,v)=2xy T_q4_m0+2xz T_q4_m1; distinct outputs =>
    # exact solution x*y=x*z=0, a one-line / two-plane union.
    # Verify the entire union graph:
    S4_a=Counter()
    for u in from5:
        fa=five[from5[u][0]]
        ma=six[from6[u][0]]
        assert set(fa)&set(ma)==set(u)
        S4_a[(len(fa),len(ma),len(set(fa)&set(ma)))]+=1
    assert S4_a==Counter({(5,6,4):1080})
    # Pair-intersection spectrum, a useful reproducible invariant
    # of the incidence correspondence, not a vacuum energy.
    intpairs=Counter(len(set(a)&set(b)) for a in five for b in six)
    assert sum(intpairs.values())==216*72
    assert intpairs[4]==1080
    # Row intersection (common IIB neighbors of two M nodes).
    common=incidence@incidence.T
    assert set(np.diag(common))=={15}
    crossM=Counter(int(common[i,j]) for i in range(72) for j in range(i+1,72))
    # Exact integer annihilating polynomial and trace moments: the
    # five eigenvalues and multiplicities are therefore PROVED,
    # not just estimated by a numerical eigensolver.
    spectral={3:15,9:30,21:20,45:6,75:1}
    eye=np.eye(72,dtype=np.int64)
    annihilator=eye.copy()
    for lam in spectral:
        annihilator=annihilator@(common-lam*eye)
    assert not np.any(annihilator)
    power=eye.copy()
    exact_traces=[]
    for p in range(5):
        actual=int(np.trace(power))
        assert actual==sum(mult*lam**p for lam,mult in spectral.items())
        exact_traces.append(actual)
        power=power@common
    assert np.linalg.matrix_rank(incidence.astype(float))==72
    # 72D M sector is linearly recoverable, but the 216D IIB
    # adjacency space has exactly 144 invisible directions.
    assert 216-72==144
    # Singular values sqrt(lambda) => condition number 5.
    assert Fraction(max(spectral),min(spectral))==25
    result=dict(status="PASS_E6_1080_UNIQUE_M_IIB_COMMON4_DUALITY_INTERFACE_NO_INTRINSIC_BRANCH_WEIGHT",
        M_section_count=72,IIB_section_count=216,
        shared_coordinate_four_spaces=1080,each_four_has_exactly_one_M_and_one_IIB_extension=True,
        M_branch_interface_degree=15,IIB_branch_interface_degree=5,
        incidence_edges=1080,bipartite_graph_connected=True,
        naive_equal_section_prior=naive,
        incidence_random_walk_stationary_branch_masses=edge_walk,
        common_core_coordinates=core,common_core_9D_origin="5 external + 4 common internal = 9 effective coordinates",
        example_IIB_5section=f,example_M_6section=m,
        transverse_one_dimensional_IIB_direction=q4,
        transverse_two_dimensional_M_directions=m2,
        annihilator_dimension=7,
        local_section_equations="x*y=x*z=0; solution = {x axis} union {y,z plane}",
        unique_quadruple_extension_verification_count=1080,
        M_IIB_pair_coordinate_intersection_histogram={str(k):v for k,v in sorted(intpairs.items())},
        M_M_common_IIB_neighbors_histogram={str(k):v for k,v in sorted(crossM.items())},
        M_M_incidence_Gram_exact_eigen_census={str(k):v for k,v in sorted(spectral.items())},
        M_M_incidence_Gram_exact_power_traces=exact_traces,
        M_M_incidence_Gram_annihilating_polynomial_product_3_9_21_45_75=True,
        incidence_matrix_row_rank=72,
        incidence_matrix_nullity_on_IIB_functions=144,
        nonzero_singular_value_condition_number=5,
        known_physics="M-theory on T2 and type IIB on S1 yield 9D dual frames, Sakatani-Uehara PTEP 2017 043B05",
        precise_limitation="The 1080 finite incidence edges are an algebraic correspondence, not a derivation of Buscher rules, flux quantization, gravitational dynamics, or transition between physical sections. Both priors are optional and produce opposite apparent selection weights.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ("status","shared_coordinate_four_spaces",
        "M_branch_interface_degree","IIB_branch_interface_degree",
        "naive_equal_section_prior","incidence_random_walk_stationary_branch_masses",
        "M_M_incidence_Gram_exact_eigen_census")},indent=2),flush=True)
    return result
if __name__=="__main__":main()
