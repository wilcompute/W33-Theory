"""Exact 17-class Clifford vacuum orbital intersection algebra.
Schreier transversals and pair-orbit partition give all 17^3
nonnegative integer intersection numbers without dense 1440 matrices.
"""
from __future__ import annotations
import collections,itertools,json
from pathlib import Path
import numpy as np
from w33_20261019_round8_clifford_vacuum_orbit import mapping
from w33_20261019_nextfive_optics_su9 import GENERATORS
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round11_vacuum_intersection_algebra.json"
def run():
    pairs=[(9*h+a,9*h+b) for h in range(40) for a,b in itertools.combinations(range(9),2)]
    ix={p:i for i,p in enumerate(pairs)}
    gs=[]
    for key,U in GENERATORS.items():
        m,_=mapping(key,U)
        gs.append(np.array([ix[tuple(sorted((int(m[a]),int(m[b]))))] for a,b in pairs],np.int16))
    n=len(pairs)
    unit=np.arange(n,dtype=np.int16)
    tx=[None]*n;tx[0]=unit
    queue=collections.deque([0])
    while queue:
        v=queue.popleft()
        for g in gs:
            u=int(g[v])
            if tx[u] is None:
                tx[u]=g[tx[v]]
                queue.append(u)
    assert all(t is not None for t in tx)
    inv=np.empty((n,n),np.int16)
    for v,t in enumerate(tx):inv[v,t]=unit
    parent=np.arange(n)
    def rt(i):
        while i!=parent[i]:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(a,b):
        a,b=rt(a),rt(b)
        if a!=b:parent[a]=b
    for v,t in enumerate(tx):
        for g in gs:
            u=int(g[v])
            h=inv[u,g[t]]
            assert h[0]==0
            for a,b in enumerate(h):union(a,int(b))
    roots=sorted(set(rt(i) for i in range(n)),key=lambda r:min(i for i in range(n) if rt(i)==r))
    ids={r:i for i,r in enumerate(roots)}
    cls=np.array([ids[rt(i)] for i in range(n)],np.int8)
    ncls=len(roots);assert ncls==17
    memberships=[np.where(cls==i)[0] for i in range(ncls)]
    reps=[int(m[0]) for m in memberships]
    valencies=[len(m) for m in memberships]
    diagonal=int(cls[0]);assert valencies[diagonal]==1
    intersection=np.zeros((ncls,ncls,ncls),dtype=np.int32)
    for k,y in enumerate(reps):
        yzclass=cls[inv[:,y]]
        for i,m in enumerate(memberships):
            counts=np.bincount(yzclass[m],minlength=ncls)
            intersection[i,:,k]=counts
    # A_i A_j = Σ_k p_ij^k A_k.
    comm=max(abs(int(intersection[i,j,k])-int(intersection[j,i,k]))
             for i in range(ncls) for j in range(ncls) for k in range(ncls))
    pairsizes=[]
    inversecls=[]
    for i,y in enumerate(reps):
        # (y,0) conjugate by t_y^-1 to (0,t_y^-1(0)).
        j=int(cls[inv[y,0]])
        inversecls.append(j)
        pairsizes.append([i,j])
    identity_err=max(abs(int(intersection[diagonal,j,k])-int(j==k))
      +abs(int(intersection[j,diagonal,k])-int(j==k))
       for j in range(ncls) for k in range(ncls))
    row_err=max(abs(int(intersection[i,:,k].sum())-valencies[i])
                   for i in range(ncls) for k in range(ncls))
    col_err=max(abs(int(intersection[:,j,k].sum())-valencies[j])
                   for j in range(ncls) for k in range(ncls))
    # A_i A_j associativity on every invariant orbital.
    # Build L_i matrices with (L_i)[k,j]=p_ij^k.
    L=np.transpose(intersection,(0,2,1)).astype(np.int64)
    assoc=max(np.max(abs(L[i]@L[j]-np.einsum('k,kab->ab',intersection[i,j,:],L)))
              for i in range(ncls) for j in range(ncls))
    # Algebra's center dimension via simultaneous commutators.
    # Solve c_i [L_i,L_j]=0 for every j in the regular representation.
    equations=np.concatenate([np.column_stack([(L[i]@L[j]-L[j]@L[i]).reshape(-1)
                                               for i in range(ncls)]) for j in range(ncls)])
    rank=np.linalg.matrix_rank(equations,tol=1e-8)
    center=ncls-rank
    # Prove center dimension over Q rather than relying on floating rank:
    # choose independent rows by numerical pivoting, then verify their
    # exact integer nullspace against ALL commutator equations.
    import sympy as sp
    from scipy.linalg import qr
    piv=qr(equations.T,mode='economic',pivoting=True)[2][:rank]
    M=sp.Matrix(equations[piv,:].tolist())
    assert M.rank()==rank
    null=M.nullspace()
    assert len(null)==center
    for v in null:
        denom=sp.ilcm(*[int(z.q) for z in v])
        ints=np.array([int(z*denom) for z in v],dtype=np.int64)
        assert not np.any(equations@ints)
    checks={"17_exact_pair_classes":ncls==17,
       "partition_of_1440":sum(valencies)==1440,
       "identity_convolution":identity_err==0,
       "intersection_row_sums_match_valency":row_err==0,
       "intersection_column_sums_match_valency":col_err==0,
       "all_structure_constants_integral_nonnegative":bool(np.min(intersection)>=0),
       "associativity_exact":assoc==0,
       "exact_rational_center_dimension_8":len(null)==8 and center==8,
       "noncommutative_orbital_algebra":comm>0,
       "transpose_orbit_pairing_involution":all(inversecls[inversecls[i]]==i and valencies[i]==valencies[inversecls[i]] for i in range(ncls))}
    out={"schema":"w33.round11.full17_orbital_intersection_algebra.v1",
       "method":"Compute orbit pair (x,y) using t_x^-1 y and stabilizer orbit of base 0. For each relation k represented by (0,y_k), compute p_ij^k=# {z: cls(z)=i and cls(t_z^-1 y_k)=j}. All maps are EXACT integer permutations.",
       "number_classes":ncls,"valencies":valencies,"representative_partner_indices":reps,
       "identity_orbit_index":diagonal,"transpose_orbits":inversecls,
       "intersection_numbers_p_i_j_k":intersection.tolist(),
       "intersection_count":ncls**3,
       "commutator_max_integer":comm,"association_algebra_commutative":comm==0,
       "left_regular_associativity_max_integer":int(assoc),
       "center_dimension":int(center),
       "interpretation":"Schurian coherent-configuration/orbital adjacency algebra. Product A_i A_j=Σ_k p_ij^k A_k. If commutator_max_integer>0 it is a noncommutative adjacency algebra, NOT a commutative symmetric association scheme. Coupling coefficients are physically unspecified. This does not make a unique vacuum.",
       "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"valencies":[int(x) for x in valencies],"commutator":int(comm),"center":int(center),"associativity":int(assoc)},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
