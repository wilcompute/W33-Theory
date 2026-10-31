#!/usr/bin/env python3
"""Exact common ambient 2/3/5 subgroup and its seven-dimensional GF5 action.

This is not automatically a canonical integral-torsion module; rational
kernel reduction must be checked against the saturated integer null lattice.
"""
from __future__ import annotations
import itertools,json,math,sys
from pathlib import Path
import numpy as np
import networkx as nx
from sympy import Matrix
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
sys.path.insert(0,str(ROOT/"analysis/search_drivers_12466"))
from symmetric_fast import fast_build
from w33_20261031_torsion_order5_probe import rk,ker
from w33_20261031_eight_quantum_fronts_round2 import finite_solve
OUT=ROOT/"data/w33_20261031_full_subgroup_GF5_representation.json"

def build():
    lifts=json.loads((ROOT/"data/w33_20261031_same_subgroup_ambient_lift_audit.json").read_text())["lifts"]
    fixed=json.loads((ROOT/"data/w33_20261031_torsion_order5_probe.json").read_text())
    _,lines=fast_build(9)
    selected=json.loads((ROOT/"analysis/search_drivers_12466/icosa_even_q9.json").read_text())["results"][0]["chosen"]
    sets=[set(lines[j])for j in selected]
    G=nx.Graph()
    G.add_nodes_from(range(48))
    G.add_edges_from((i,j) for i in range(48)for j in range(i+1,48)if sets[i]&sets[j])
    part=nx.bipartite.color(G)
    left=sorted(x for x in G if part[x]==0)
    right=sorted(x for x in G if part[x]==1)
    B=np.array([[int(G.has_edge(x,y))for y in right]for x in left],dtype=np.int64)
    K=ker(B);assert K.shape==(24,13)
    L=[]
    for v in Matrix(B.tolist()).nullspace():
        den=math.lcm(*[int(z.q)for z in v])
        u=[int(x*den)for x in v];d=math.gcd(*u)
        L.append([x//d%5 for x in u])
    L=np.array(L,dtype=np.int64).T
    assert L.shape==(24,6)and rk(L)==6
    basis=L.copy();idx=[]
    for j in range(K.shape[1]):
        if rk(np.column_stack([basis,K[:,j]]))>basis.shape[1]:
            basis=np.column_stack([basis,K[:,j]]);idx.append(j)
    assert basis.shape==(24,13)and len(idx)==7
    T=K[:,idx]
    ri={x:i for i,x in enumerate(right)}
    acts={};perms={}
    for order in (2,3,5):
        assert lifts[str(order)]["status"]=="LIFT_FOUND"
        p=fixed["other_orders"][str(order)]["mapping"]
        assert all(part[i]==part[p[i]]for i in range(48))
        P=np.zeros((24,24),dtype=np.int64)
        for j,x in enumerate(right):P[ri[p[x]],j]=1
        assert np.array_equal(np.linalg.matrix_power(P,order),np.eye(24,dtype=np.int64))
        assert np.all(B@P@K%5==0)
        mat=np.column_stack([finite_solve(basis,P@T[:,j]%5)[6:]for j in range(7)])%5
        assert np.array_equal(np.linalg.matrix_power(mat,order)%5,np.eye(7,dtype=np.int64))
        acts[order]=mat;perms[order]=tuple(p)
    pg=PermutationGroup([Permutation(list(perms[k]))for k in (2,3,5)])
    order=int(pg.order())
    derived=int(pg.derived_subgroup().order())
    centergroup=pg.center()
    center=int(centergroup.order())
    perfect_derived_order=int(pg.derived_subgroup().derived_subgroup().order())
    derived_center_order=int(pg.derived_subgroup().center().order())
    Iperm=tuple(range(48));I=np.eye(7,dtype=np.int64)
    def prod(p,q):return tuple(p[q[i]]for i in range(48))
    states={Iperm:I};todo=[Iperm]
    for perm in todo:
        for gen in (2,3,5):
            nextp=prod(perms[gen],perm)
            nextA=acts[gen]@states[perm]%5
            if nextp in states:
                assert np.array_equal(states[nextp],nextA), "Generator maps inconsistent with a 7D linear representation"
            else:states[nextp]=nextA;todo.append(nextp)
    assert len(states)==order
    image_order=len({tuple(a.flatten())for a in states.values()})
    nontrivial_center=[tuple(int(x)for x in p.array_form)for p in centergroup.generate_schreier_sims() if not p.is_Identity]
    assert len(nontrivial_center)==1 and len(nontrivial_center[0])==48
    central_action=states[nontrivial_center[0]]
    assert np.array_equal(central_action@central_action%5,I)
    center_plus_dim=ker((central_action-I)%5).shape[1]
    center_minus_dim=ker((central_action+I)%5).shape[1]
    assert center_plus_dim+center_minus_dim==7
    assert order==120 and derived==perfect_derived_order==60 and center==2 and derived_center_order==1
    fixed_vectors=ker(np.vstack([acts[k]-I for k in (2,3,5)]))
    fixed_covectors=ker(np.vstack([acts[k].T-I for k in (2,3,5)]))
    fixed_dim=fixed_vectors.shape[1]
    covector_dim=fixed_covectors.shape[1]
    pairing=(fixed_covectors.T@fixed_vectors)%5
    trivial_summand_splits=(fixed_dim==covector_dim==1 and bool(pairing[0,0]))
    assert trivial_summand_splits
    even3=ker(np.vstack([(central_action-I)%5,fixed_covectors.T]))
    odd3=ker((central_action+I)%5)
    assert even3.shape==odd3.shape==(7,3)
    assert rk(np.column_stack([fixed_vectors,even3,odd3]))==7
    derived_generators=[tuple(int(x)for x in p.array_form)for p in pg.derived_subgroup().generators]
    def restrict(S):
        matrices=[]
        for p in derived_generators:
            A=states[p]
            M=np.column_stack([finite_solve(S,A@S[:,j]%5)for j in range(3)])%5
            assert np.array_equal(S@M%5,A@S%5)
            matrices.append(M)
        assert rk(np.vstack([M-np.eye(3,dtype=np.int64)for M in matrices]))==3
        assert rk(np.vstack([M.T-np.eye(3,dtype=np.int64)for M in matrices]))==3
        # A5 is perfect, so all its 1D representations are trivial. Lack
        # of fixed vectors and fixed dual covectors excludes dimensions 1 and 2.
        return matrices
    even3acts=restrict(even3)
    odd3acts=restrict(odd3)
    hom_equations=[]
    for A,B0 in zip(even3acts,odd3acts):
        hom_equations.append(np.kron(np.eye(3,dtype=np.int64),A)-np.kron(B0.T,np.eye(3,dtype=np.int64)))
    hom_dimension=9-rk(np.vstack(hom_equations))
    comm=[]
    for k in (2,3,5):
        A=acts[k]
        comm.append((np.kron(np.eye(7,dtype=np.int64),A)-np.kron(A.T,np.eye(7,dtype=np.int64)))%5)
    centralizer_dim=49-rk(np.vstack(comm))
    # Sanity: order-5 Jordan blocks preserved under common subgroup.
    nil=(acts[5]-I)%5
    ranks=[rk(np.linalg.matrix_power(nil,j)%5)for j in range(6)]
    assert ranks==[7,4,2,0,0,0]
    assert image_order<=order
    return {"status":"PASS_ACTUAL_120_ELEMENT_GF9_SUBGROUP_AND_GF5_MODULE",
      "projective_group_order":order,"derived_subgroup_order":derived,
      "perfect_derived_subgroup_order":perfect_derived_order,
      "derived_subgroup_center_order":derived_center_order,
      "group_center_order":center,
      "exact_group_identification":"A5 direct-product C2: order120, derived A5 order60 perfect center-free, group central C2 and trivial intersection",
      "central_element_GF5_action":central_action.tolist(),
      "central_even_module_dimension":center_plus_dim,
      "central_odd_module_dimension":center_minus_dim,
      "GF5_representation_image_order":image_order,
      "GF5_invariant_vector_dimension":fixed_dim,
      "GF5_invariant_covector_dimension":covector_dim,
      "GF5_trivial_vector_covector_pairing":pairing.tolist(),
      "GF5_trivial_one_dim_summand_splits":trivial_summand_splits,
      "even3_irreducible_over_GF5":True,
      "odd3_irreducible_over_GF5":True,
      "even3_odd3_derived_A5_hom_dimension":hom_dimension,
      "actual_three_block_decomposition":"1_even + 3_even + 3_odd as irreducible GF5 modules; central C2 parity distinguishes the two three-dimensional sectors",
      "GF5_commutant_dimension":centralizer_dim,
      "GF5_generator_actions":{str(k):acts[k].tolist()for k in (2,3,5)},
      "order5_nilpotent_ranks":ranks,
      "all_group_products_verified":len(states)*3,
      "group_identification_hint":"The order120 group is generated by three actual projective GF9 symplectic similitudes. Derived subgroup and center distinguish S5, A5xC2 and binary icosahedral possibilities; do not assume A5 by order.",
      "canonical_5torsion_identification_verified":True,
      "canonical_5torsion_proof":"Let S=ker_Z(B), a saturated rank-6 sublattice of Z^24 because its quotient is im(B), which is torsion-free. Six cleared-denominator integer kernel vectors have rank 6 after mod5 reduction, therefore their mod5 span equals S/5S inside ker_F5(B). The universal-coefficient exact sequence identifies ker_F5(B)/(S/5S) canonically with coker(B)[5] (seven-dimensional, matching the seven 5 factors in SNF). No full integral unimodular kernel basis is required for this prime-specific assertion.",
      "scope":"An actual 120-element A5 x C2 projective subgroup with faithfully computed 7D canonical characteristic-five torsion action; not a physical particle multiplet or complete entire ambient PGSp orbit classification."}
if __name__=="__main__":
    d=build()
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:d[k]for k in ("status","projective_group_order","derived_subgroup_order","group_center_order","GF5_representation_image_order","GF5_invariant_vector_dimension","GF5_commutant_dimension","all_group_products_verified")}))
