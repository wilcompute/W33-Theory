#!/usr/bin/env python3
"""Pass 4632 -- periodic cubic-incidence homology is not the same as the equal-dimensional W33 point modules.

The Pass4575 27x36 matrix R[s,a]=B(s,a) gives a two-periodic complex over F2.
This verifier reconstructs the natural O^-(6,2) six-space, its index-two derived
subgroup G=PSp(4,3), the two homologies

  H36 = ker(R)/im(R^T), dim 24,
  H27 = ker(R^T)/im(R), dim 15,

and the point-side 40-object W33 module obtained from the 40 compatible F4
structures {J,J^2}.  If A is the degree-12 orbital graph on that 40-set, then
rank_2(A)=16 and the equal-dimensional comparison layers are

  Q24 = F2^40 / row(A),
  Q15 = row(A) / <1>.

Exact equivariance equations show that equal dimensions do NOT give module
isomorphisms.  The unique maps H36->Q24 and H27->Q15 have ranks 9 and 14;
the reverse unique maps have rank 1 in both cases.
"""
from __future__ import annotations
import itertools, json
from collections import deque, Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4632_PERIODIC_HOMOLOGY_MODULE_SEPARATION.json'

# F4 model copied from the certified paired-axis construction.
def f4_mul(x,y):
    a,b=x&1,(x>>1)&1; c,d=y&1,(y>>1)&1
    return (a*c ^ b*d) | (((a*d)^(b*c)^(b*d))<<1)
def q(x):
    return sum(((x>>(2*i))&3)!=0 for i in range(3))&1
def B(x,y): return q(x^y)^q(x)^q(y)

def mat_apply(M,x):
    y=0
    for j in range(6):
        if (x>>j)&1:
            for i in range(6): y^=(int(M[i,j])&1)<<i
    return y

def symmetry(v):
    M=np.eye(6,dtype=np.uint8)
    for j in range(6):
        e=1<<j
        if B(e,v):
            for i in range(6): M[i,j]^=(v>>i)&1
    return M

def mkey(M): return bytes(np.asarray(M,dtype=np.uint8).ravel())
def mmul(A,Bm): return (A@Bm)%2

def closure(gens):
    I=np.eye(6,dtype=np.uint8); seen={mkey(I):I}; Q=deque([I])
    while Q:
        x=Q.popleft()
        for g in gens:
            y=mmul(g,x); k=mkey(y)
            if k not in seen: seen[k]=y; Q.append(y)
    return list(seen.values())
def inv6(M):
    A=np.concatenate([M.copy(),np.eye(6,dtype=np.uint8)],axis=1); r=0
    for c in range(6):
        z=np.flatnonzero(A[r:,c]); assert len(z)
        k=r+int(z[0]); A[[r,k]]=A[[k,r]]
        for i in np.flatnonzero(A[:,c]):
            if i!=r:A[i]^=A[r]
        r+=1
    return A[:,6:]
def comm(a,b): return mmul(mmul(mmul(a,b),inv6(a)),inv6(b))

def small_full_generators():
    anis=[x for x in range(1,64) if q(x)]
    chosen=[]; order=1
    for v in anis:
        trial=closure(chosen+[symmetry(v)])
        if len(trial)>order:
            chosen.append(symmetry(v));order=len(trial)
        if order==51840:break
    assert order==51840
    return chosen

def derived_generators(fullgens):
    cand=[comm(a,b) for a in fullgens for b in fullgens]
    chosen=[];order=1
    for g in cand:
        trial=closure(chosen+[g])
        if len(trial)>order:
            chosen.append(g);order=len(trial)
        if order==25920:break
    assert order==25920
    return chosen

# bit-vector linear algebra
def rank(rows,n):
    piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)
def basis(rows,n):
    out=[];r=0
    for x in rows:
        if rank(out+[int(x)],n)>r:out.append(int(x));r+=1
    return out
def solver(B,n):
    rows=[]
    for i,b in enumerate(B): rows.append([int(b),1<<i])
    piv={}
    for y,c in rows:
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p][0];c^=piv[p][1]
            else:piv[p]=(y,c);break
    def f(x):
        y=int(x);c=0
        while y:
            p=y.bit_length()-1
            if p not in piv:return None
            y^=piv[p][0];c^=piv[p][1]
        return c
    return f
def nullspace(rows,n):
    B=basis(rows,n); piv=[]; R=[]
    for x in B:
        y=x
        for p,z in R:
            if (y>>p)&1:y^=z
        p=y.bit_length()-1
        for i,(p0,z) in enumerate(R):
            if (z>>p)&1:R[i]=(p0,z^y)
        R.append((p,y));R.sort(reverse=True);piv.append(p)
    pset={p for p,_ in R}; free=[j for j in range(n) if j not in pset]; out=[]
    for f in free:
        x=1<<f
        for p,z in sorted(R):
            if ((z & x).bit_count()&1):x|=1<<p
        out.append(x)
    assert all(all(((r&x).bit_count()&1)==0 for r in rows) for x in out)
    return basis(out,n)
def perm_mask(x,p):
    y=0
    while x:
        b=x&-x;i=b.bit_length()-1;y|=1<<p[i];x-=b
    return y

def quotient_actions(ambient_basis, subdim, perms, n):
    # ambient_basis begins with a basis for the subspace being quotiented out.
    sol=solver(ambient_basis,n); d=len(ambient_basis)-subdim; acts=[]
    for p in perms:
        cols=[]
        for b in ambient_basis[subdim:]:
            c=sol(perm_mask(b,p)); assert c is not None
            cols.append(c>>subdim)
        acts.append(cols_to_np(cols,d))
    return acts
def cols_to_np(cols,d):
    M=np.zeros((d,d),dtype=np.uint8)
    for j,c in enumerate(cols):
        for i in range(d):M[i,j]=(c>>i)&1
    return M

def subquotient_actions(space_basis, sub_basis, perms, n):
    sb=basis(sub_basis,n); assert rank(space_basis,n)==len(space_basis)
    full=sb[:]
    for x in space_basis:
        if rank(full+[x],n)>len(full):full.append(x)
    assert len(full)==len(space_basis)
    return quotient_actions(full,len(sb),perms,n)

def nullspace_matrix(A):
    A=np.asarray(A,dtype=np.uint8); rows=[]
    for r in A: rows.append(sum(int(r[j])<<j for j in range(A.shape[1]) if r[j]))
    ns=nullspace(rows,A.shape[1]); M=np.zeros((len(ns),A.shape[1]),dtype=np.uint8)
    for i,x in enumerate(ns):
        for j in range(A.shape[1]):M[i,j]=(x>>j)&1
    return M

def hom_space(Sgens,Tgens):
    ds=Sgens[0].shape[0];dt=Tgens[0].shape[0]; eq=[]
    for S,T in zip(Sgens,Tgens):
        for i in range(dt):
            for j in range(ds):
                row=0
                for k in range(dt):
                    if T[i,k]:row^=1<<(k*ds+j)
                for k in range(ds):
                    if S[k,j]:row^=1<<(i*ds+k)
                eq.append(row)
    ns=nullspace(eq,dt*ds); maps=[]
    for x in ns:
        M=np.zeros((dt,ds),dtype=np.uint8)
        for i in range(dt):
            for j in range(ds):M[i,j]=(x>>(i*ds+j))&1
        maps.append(M)
    return maps

def rank2(M):
    rows=[sum(int(M[i,j])<<j for j in range(M.shape[1]) if M[i,j]) for i in range(M.shape[0])]
    return rank(rows,M.shape[1])

def cyclic_dims(gens,d):
    out=[]
    for i in range(d):
        seen=basis([1<<i],d); changed=True
        while changed:
            changed=False
            for x in list(seen):
                for G in gens:
                    y=0
                    for j in range(d):
                        if (x>>j)&1:y^=sum(int(G[k,j])<<k for k in range(d) if G[k,j])
                    if rank(seen+[y],d)>len(seen):seen.append(y);changed=True
        out.append(len(seen))
    return Counter(out)

def main()->int:
    fullgens=small_full_generators(); ggens=derived_generators(fullgens); G=closure(ggens);assert len(G)==25920
    sing=[x for x in range(1,64) if not q(x)]; anis=[x for x in range(1,64) if q(x)];assert (len(sing),len(anis))==(27,36)
    si={x:i for i,x in enumerate(sing)};ai={x:i for i,x in enumerate(anis)}
    R=np.array([[B(s,a) for a in anis] for s in sing],dtype=np.uint8)
    assert rank2(R)==6 and not np.any((R@R.T)%2) and not np.any((R.T@R)%2)
    sperms=[[si[mat_apply(g,x)] for x in sing] for g in ggens];aperms=[[ai[mat_apply(g,x)] for x in anis] for g in ggens]
    rowR=basis([sum(int(R[i,j])<<j for j in range(36) if R[i,j]) for i in range(27)],36)
    kerR=nullspace([sum(int(R[i,j])<<j for j in range(36) if R[i,j]) for i in range(27)],36)
    colR=basis([sum(int(R[i,j])<<i for i in range(27) if R[i,j]) for j in range(36)],27)
    kerRt=nullspace([sum(int(R[i,j])<<i for i in range(27) if R[i,j]) for j in range(36)],27)
    H36=subquotient_actions(kerR,rowR,aperms,36);H27=subquotient_actions(kerRt,colR,sperms,27)
    assert H36[0].shape==(24,24) and H27[0].shape==(15,15)

    # Compatible F4 structures {J,J^2}; conjugation gives the point-side W33 carrier.
    full=closure(fullgens); I=np.eye(6,dtype=np.uint8);Z=np.zeros((6,6),dtype=np.uint8)
    oriented=[M for M in full if np.array_equal((M@M+M+I)%2,Z)];assert len(oriented)==80
    pairs={tuple(sorted((mkey(J),mkey((J@J)%2)))) for J in oriented};pairs=sorted(pairs);assert len(pairs)==40
    pidx={P:i for i,P in enumerate(pairs)}
    def pairperm(g):
        gi=inv6(g);out=[]
        for a,b in pairs:
            J=np.frombuffer(a,dtype=np.uint8).reshape(6,6);K=mmul(mmul(g,J),gi);K2=(K@K)%2
            out.append(pidx[tuple(sorted((mkey(K),mkey(K2))))])
        return out
    pperms=[pairperm(g) for g in ggens]
    # stabilizer suborbits identify the unique valency-12 orbital.
    allpperms=[pairperm(g) for g in G]; stab=[p for p in allpperms if p[0]==0]
    unseen=set(range(40));orbs=[]
    while unseen:
        s=min(unseen);O={p[s] for p in stab};orbs.append(sorted(O));unseen-=O
    assert sorted(map(len,orbs))==[1,12,27]; neigh=[O for O in orbs if len(O)==12][0]
    A=np.zeros((40,40),dtype=np.uint8)
    for p in allpperms:
        for y in neigh:A[p[0],p[y]]=1
    assert np.all(A.sum(axis=1)==12) and rank2(A)==16
    rowA=basis([sum(int(A[i,j])<<j for j in range(40) if A[i,j]) for i in range(40)],40);assert len(rowA)==16
    Q24basis=rowA[:]
    for i in range(40):
        if rank(Q24basis+[1<<i],40)>len(Q24basis):Q24basis.append(1<<i)
    Q24=quotient_actions(Q24basis,16,pperms,40)
    one=(1<<40)-1;assert rank(rowA+[one],40)==16
    Q15=subquotient_actions(rowA,[one],pperms,40)

    comparisons={}
    for name,S,T in [('H36_to_Q24',H36,Q24),('Q24_to_H36',Q24,H36),('H27_to_Q15',H27,Q15),('Q15_to_H27',Q15,H27)]:
        H=hom_space(S,T); comparisons[name]={'hom_dimension':len(H),'nonzero_map_ranks':[rank2(M) for M in H if np.any(M)]}
    assert comparisons=={
      'H36_to_Q24':{'hom_dimension':1,'nonzero_map_ranks':[9]},
      'Q24_to_H36':{'hom_dimension':1,'nonzero_map_ranks':[1]},
      'H27_to_Q15':{'hom_dimension':1,'nonzero_map_ranks':[14]},
      'Q15_to_H27':{'hom_dimension':1,'nonzero_map_ranks':[1]}}
    cyc={'H36':dict(cyclic_dims(H36,24)),'Q24':dict(cyclic_dims(Q24,24)),'H27':dict(cyclic_dims(H27,15)),'Q15':dict(cyclic_dims(Q15,15))}
    out={'pass':4632,'group':'PSp(4,3)','periodic_homology':{'H36_dimension':24,'H27_dimension':15},'point_side_W33_modular_layers':{'rank_A_mod2':16,'Q24':'F2^40/row(A)','Q15':'row(A)/<1>'},'equivariant_map_comparison':comparisons,'standard_seed_cyclic_dimension_census':cyc,'theorem':'The 24D and 15D periodic cubic-incidence homologies are not isomorphic to the equal-dimensional point-side W33 modular layers. The unique comparison maps have ranks 9/1 in dimension 24 and 14/1 in dimension 15, exposing shared subquotients but inequivalent extensions.','boundary':'Finite F2 PSp(4,3)-module theorem. Equal dimensions are explicitly rejected as an identification.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
