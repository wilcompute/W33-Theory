"""TOE86 track II: exact modular H27 intertwiners H2 -> H1.

Builds 26-dimensional H1 from graph fundamental cycles and the TOE83
99 oriented 2-face boundaries. Computes equivariant Hom over F3.
"""
from __future__ import annotations
from collections import deque
from itertools import product
import json
import numpy as np
from analysis.w33_20261015_toe85_h2_relation_module import (
    geometry, nullspace, action_on_kernel, rank_and_basis, ROOT
)
from analysis.w33_20261015_toe86_geometry_integral_routing import (
    native, H, IDX, mul
)
P=3

def independent_ordered(rows,p=3):
    piv={}
    chosen=[]
    for row in rows:
        w=[int(v)%p for v in row]
        while True:
            j=next((k for k,x in enumerate(w) if x),None)
            if j is None:break
            if j in piv:
                m=w[j];v=piv[j]
                w=[(a-m*b)%p for a,b in zip(w,v)]
            else:
                inv=pow(w[j],-1,p)
                piv[j]=[(v*inv)%p for v in w]
                chosen.append([int(v)%p for v in row])
                break
    return chosen

def cycle_basis(edges,ei):
    adj={v:set() for v in range(27)}
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    parent={0:None};queue=deque([0]);tree=set()
    while queue:
        u=queue.popleft()
        for v in sorted(adj[u]):
            if v not in parent:
                parent[v]=u;queue.append(v)
                tree.add(tuple(sorted((u,v))))
    assert len(parent)==27 and len(tree)==26
    def path(u,v):
        anc=set();x=u
        while x is not None:anc.add(x);x=parent[x]
        y=v;tail=[]
        while y not in anc:tail.append(y);y=parent[y]
        prefix=[];x=u
        while x!=y:prefix.append(x);x=parent[x]
        return prefix+[y]+list(reversed(tail))
    def oriented(walk):
        v=[0]*135
        for u,w in zip(walk,walk[1:]):
            v[ei[tuple(sorted((u,w)))]]+=(1 if u<w else -1)
        return v
    return [oriented(path(u,v)+[u]) for u,v in edges
            if (u,v) not in tree]

def decompose_constructor(basis):
    """Coordinate elimination with exact field-3 row-echelon operations."""
    piv={}
    n=len(basis)
    for i,row in enumerate(basis):
        w=[x%3 for x in row];coef=[int(j==i) for j in range(n)]
        while True:
            k=next((j for j,t in enumerate(w) if t),None)
            if k is None:raise AssertionError("dependent basis")
            if k in piv:
                old,c=piv[k];scale=w[k]
                w=[(a-scale*b)%3 for a,b in zip(w,old)]
                coef=[(a-scale*b)%3 for a,b in zip(coef,c)]
            else:
                scale=pow(w[k],-1,3)
                piv[k]=([(x*scale)%3 for x in w],
                         [(x*scale)%3 for x in coef])
                break
    def coords(row):
        w=[x%3 for x in row];coef=[0]*n
        while True:
            k=next((j for j,t in enumerate(w) if t),None)
            if k is None:break
            if k not in piv:raise ValueError("input vector not a cycle")
            old,c=piv[k];scale=w[k]
            w=[(a-scale*b)%3 for a,b in zip(w,old)]
            coef=[(a+scale*b)%3 for a,b in zip(coef,c)]
        return coef
    return coords

def h1_action():
    H2,faces,actions=geometry()
    triangles,edges,ei,perms,orbits=native()
    cycles=cycle_basis(edges,ei)
    assert len(cycles)==109
    boundary=independent_ordered(faces)
    assert len(boundary)==83
    chosen=boundary[:]
    selected=[]
    # append candidates one by one; tiny 135-column exact elimination.
    r=83
    for cyc in cycles:
        if len(independent_ordered(chosen+[cyc]))>r:
            chosen.append([x%3 for x in cyc]);selected.append(cyc);r+=1
    assert len(chosen)==109 and len(selected)==26 and r==109
    coords=decompose_constructor(chosen)
    mats={}
    for g,perm in zip(H,perms):
        q=[ei[tuple(sorted((perm[u],perm[v])))] for u,v in edges]
        sign=[1 if perm[u]<perm[v] else -1 for u,v in edges]
        def act(row):
            out=[0]*135
            for i,v in enumerate(row):
                if v:out[q[i]]=(sign[i]*v)%3
            return out
        M=[]
        for cycle in selected:
            image=act(cycle)
            c=coords(image)
            M.append(c[83:])
        mats[g]=M
    eye=[[int(i==j) for j in range(26)] for i in range(26)]
    assert mats[(0,0,0)]==eye
    for g in H:
        for h in H:
            gh=mul(g,h)
            assert all([sum(mats[g][j][k]*mats[h][i][j]
                            for j in range(26))%3 for k in range(26)]==mats[gh][i]
                       for i in range(26))
    return mats

def mod3_kernel_info(A):
    """Vectorized echelon with explicit verified nullvector."""
    a=np.array(A,dtype=np.int16)%3
    m,n=a.shape
    piv=[];r=0
    for col in range(n):
        pos=np.flatnonzero(a[r:,col])
        if pos.size==0:continue
        k=r+int(pos[0])
        if k!=r:a[[r,k]]=a[[k,r]]
        if a[r,col]==2:a[r,:]=(a[r,:]*2)%3
        mask=np.flatnonzero(a[r+1:,col])+r+1
        if len(mask):
            co=a[mask,col].copy()
            a[mask,col:]=(a[mask,col:]-co[:,None]*a[r,col:])%3
        piv.append(col);r+=1
        if r==m:break
    free=next((i for i in range(n) if i not in set(piv)),None)
    null=None
    if free is not None:
        null=np.zeros(n,dtype=np.int16)
        null[free]=1
        for row in range(r-1,-1,-1):
            col=piv[row]
            null[col]=(-int(np.dot(a[row,col+1:].astype(np.int64),
                                    null[col+1:].astype(np.int64))))%3
        assert np.all(np.asarray(A,dtype=np.int16)@null%3==0)
    return {"rank":r,"nullity":n-r,
            "first_nullvector":None if null is None else null.tolist()}

def equivariant_hom(H1,H2):
    # Each matrix lists images of basis vectors as rows.
    n1=26;n2=16
    n=n1*n2
    equations=[]
    for g in ((1,0,0),(0,1,0)):
        A=H1[g];B=H2[g]
        for i in range(n2):
            for k in range(n1):
                eq=[0]*n
                for j in range(n1):eq[i*n1+j]=(eq[i*n1+j]+A[j][k])%3
                for l in range(n2):eq[l*n1+k]=(eq[l*n1+k]-B[i][l])%3
                equations.append(eq)
    result=mod3_kernel_info(equations)
    if result["first_nullvector"] is not None:
        v=result["first_nullvector"]
        support=[{"H2_basis_index":i,"H1_basis_index":j,"coeff":v[i*26+j]}
                 for i in range(16) for j in range(26) if v[i*26+j]]
        result["example_intertwiner_support"]=support
        # Verify all 27 group elements using the candidate matrix.
        for g in H:
            A=H1[g];B=H2[g]
            for i in range(16):
                for k in range(26):
                    lhs=sum(A[j][k]*v[i*26+j] for j in range(26))%3
                    rhs=sum(B[i][l]*v[l*26+k] for l in range(16))%3
                    assert lhs==rhs
    result.pop("first_nullvector")
    return result

def certificate():
    H2_elements,faces,actions=geometry()
    A=[[faces[j][i] for j in range(99)] for i in range(135)]
    kernel,free,r=nullspace(A,3)
    assert r==83 and len(kernel)==16
    H2={g:action_on_kernel(kernel,free,action,3)
        for g,action in actions.items()}
    H1=h1_action()
    hom=equivariant_hom(H1,H2)
    return {"field":"F3","logical_H1_dimension":26,
            "face_relation_H2_dimension":16,"source_boundary_rank":83,
            "equivariance_generators":[[1,0,0],[0,1,0]],
            "constraint_rows":2*26*16,
            "hom_H2_to_H1":hom,
            "chain_boundary_restriction_on_H2":"d2 restricted to H2 equals zero, hence no nonzero canonical map arises from d2.",
            "physical_temporal_interpretation":"An algebraic homomorphism cannot establish clock dynamics."}

if __name__=="__main__":
    d=certificate()
    p=ROOT/"data/w33_20261015_toe86_hom_intertwiners.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("H2->H1 Hom(F3)",{k:v for k,v in d["hom_H2_to_H1"].items()
                                if k!="example_intertwiner_support"})
    print("nonzero example coefficient count",
          len(d["hom_H2_to_H1"].get("example_intertwiner_support",[])))
    print("WROTE",p)
