#!/usr/bin/env python3
"""Exact rank-3 Sp(4,3) centralizer/commutant obstruction on W33 points.

Generate the projective symplectic action from all 40 F3 transvections.
Ordered point-pair orbits have sizes 40 (diagonal), 480 (collinear),
1080 (non-collinear). Therefore ANY full-group-invariant 40x40
complex point-space operator is a linear combination of those 3
orbit indicator matrices, equivalently a polynomial of degree<=2
in A=BB.T-4I. W33 point irreducible eigenspaces are 1,24,15.
Thus an invariant one-body mass operator cannot single out an
exact 3-dimensional generation subspace without extra structure.
"""
import json,sys,collections
from pathlib import Path
import numpy as np
from w33_20261109_five_fronts import geometry,normalize,symplectic

def action():
    pts,lines,inc=geometry()
    idx={p:i for i,p in enumerate(pts)}
    gen=[]
    for u in pts:
        perm=[]
        for v in pts:
            omega=symplectic(v,u)
            w=normalize(tuple((v[i]+omega*u[i])%3 for i in range(4)))
            perm.append(idx[w])
        assert len(set(perm))==40
        gen.append(tuple(perm))
    return pts,lines,inc,gen

def orbit(pair,gen):
    visited={pair}
    queue=collections.deque([pair])
    while queue:
        a,b=queue.popleft()
        for g in gen:
            t=(g[a],g[b])
            if t not in visited:
                visited.add(t);queue.append(t)
    return visited

def main(path=None):
    pts,lines,inc,gen=action()
    B=np.zeros((40,40),int)
    for i,li in enumerate(inc):
        for j in li:B[i,j]=1
    A=B@B.T-4*np.eye(40,dtype=int)
    assert np.all(np.diag(A)==0)
    assert np.all((A==0)|(A==1))
    assert np.all(A.sum(axis=1)==12)
    # Symplectic collinearity is a permutation-invariant relation.
    for g in gen:
        # check all automorphism generators preserve adjacency
        assert np.array_equal(A[np.ix_(g,g)],A)
    p=0
    col=next(j for j in range(1,40) if A[p,j]==1)
    noncol=next(j for j in range(1,40) if A[p,j]==0)
    odiag=orbit((p,p),gen)
    ocol=orbit((p,col),gen)
    onon=orbit((p,noncol),gen)
    assert [len(x) for x in (odiag,ocol,onon)]==[40,480,1080]
    assert len(odiag|ocol|onon)==1600
    assert not (odiag & ocol or odiag & onon or ocol & onon)
    assert all(A[a,b]==1 for a,b in ocol)
    assert all(a!=b and A[a,b]==0 for a,b in onon)
    # Strongly regular graph intersection counts and 3-dimensional algebra.
    assert np.array_equal(A@A,12*np.eye(40,dtype=int)+
            2*A+4*(np.ones((40,40),dtype=int)-np.eye(40,dtype=int)-A))
    eigen=np.linalg.eigvalsh(A)
    assert sum(abs(eigen-12)<1e-8)==1
    assert sum(abs(eigen-2)<1e-8)==24
    assert sum(abs(eigen+4)<1e-8)==15
    I=np.eye(40)
    J=np.ones((40,40))
    E1=(A+4*I)@(A-2*I)/(16*10)
    E2=(A-12*I)@(A+4*I)/(-10*6)
    E3=(A-12*I)@(A-2*I)/(-16*-6)
    # Build projectors with unambiguous Lagrange interpolation instead.
    eigs=[12.,2.,-4.]
    projections=[]
    for x in eigs:
        P=np.eye(40)
        for y in eigs:
            if y!=x:P=P@(A-y*I)/(x-y)
        assert np.max(abs(P@P-P))<1e-12
        projections.append(P)
    assert [round(np.trace(P)) for P in projections]==[1,24,15]
    assert np.max(abs(sum(projections)-I))<1e-12
    # Distinct projectors all G-invariant and span 3D algebra.
    for P in projections:
        assert max(np.max(abs(P[np.ix_(g,g)]-P)) for g in gen)<1e-12
    # The 3 eigenmodules of the multiplicity-free rank-3 permutation
    # representation are irreducible by the commutant/Schur lemma.
    out={
     "status":"PASS_EXACT_PROJECTIVE_SYMPLECTIC_RANK3_COMMUTANT_NO_NATIVE_3_GENERATIONS",
     "generators_used":len(gen),
     "ordered_pair_orbits":[{"relation":"same point","size":len(odiag)},
                            {"relation":"symplectically collinear","size":len(ocol)},
                            {"relation":"distinct noncollinear","size":len(onon)}],
     "full_ordered_pair_count":1600,
     "native_collinearity_graph_SRG_parameters":[40,12,2,4],
     "native_collinearity_adjacency_eigenspaces":[{"eigenvalue":12,"dimension":1},
          {"eigenvalue":2,"dimension":24},{"eigenvalue":-4,"dimension":15}],
     "full_Sp4F3_point_commutant_dimension":3,
     "commutant_basis":"I40, A, J40-I40-A; equivalently I40,A,A²",
     "consequence":"Any one-body operator invariant under this FULL projective symplectic point action is a polynomial in the collinearity adjacency and acts as scalar on irreducible 1,24,15 eigenspaces. It cannot single out a nontrivial 3D invariant subspace in the native 40-point module; an observed three-generation label would need extra spaces, symmetry breaking, or a different representation.",
     "scope":"Exact finite invariant-subspace obstruction on the 40-point permutation module only, not a no-go theorem for all W33 derived higher tensors, all interactions, chirality, spontaneous symmetry breaking or the physical SM."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS Sp4 rank3",json.dumps({"orbits":[len(x) for x in (odiag,ocol,onon)],
           "dims":[round(np.trace(P)) for P in projections],
           "commutant":3}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
