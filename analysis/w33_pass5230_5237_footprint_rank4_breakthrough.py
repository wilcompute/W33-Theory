#!/usr/bin/env python3
"""Pass5230-5237 exact q=5 footprint-code breakthrough replay.

Reconstruct W(3,5), its 325 polar-pair dual-grid carriers, the footprint matrix F,
then certify:
  * the complete weight-8 dual shell is one symplectic orbit of size 24375;
  * every weight-8 support is K8 minus a perfect matching and covers 48 points twice;
  * the shell span has rank 259;
  * one weight-9 dual word raises the sparse parity-check rank to 260;
  * weight-8 pair cooccurrence refines NO_5^+(5) to a 3-class association scheme;
  * the Pass5212 Hoffman 13-cover is a systematic quotient of C_F.

No q=5 primal minimum-distance theorem is asserted here.
"""
from collections import Counter, deque
from itertools import product
import numpy as np

P = 5

def inv(a): return pow(int(a) % P, -1, P)
def canon(v):
    v = tuple(int(x) % P for x in v)
    for x in v:
        if x:
            z = inv(x)
            return tuple((z*y) % P for y in v)
    raise ValueError("zero vector")
def add(u,v): return tuple((u[i]+v[i])%P for i in range(4))
def mul(a,u): return tuple((a*u[i])%P for i in range(4))
def sp(u,v):
    return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1]) % P

def gf2_rank(A):
    A = A.copy().astype(np.uint8)
    r = 0
    for c in range(A.shape[1]):
        q = np.flatnonzero(A[r:,c])
        if not len(q):
            continue
        i = r + q[0]
        A[[r,i]] = A[[i,r]]
        for j in range(A.shape[0]):
            if j != r and A[j,c]:
                A[j] ^= A[r]
        r += 1
        if r == A.shape[0]: break
    return r

pts = sorted({canon(v) for v in product(range(P), repeat=4) if any(v)})
assert len(pts) == 156
pi = {v:i for i,v in enumerate(pts)}

lines = {}
for i,u in enumerate(pts):
    for j in range(i+1,len(pts)):
        v = pts[j]
        S = {canon(add(mul(a,u),mul(b,v))) for a,b in product(range(P),repeat=2) if a or b}
        if len(S) == 6:
            lines[tuple(sorted(pi[x] for x in S))] = (u,v)
assert len(lines) == 806

carriers = {}
for H,(u,v) in lines.items():
    if sp(u,v):
        perp = [i for i,x in enumerate(pts) if sp(x,u)==0 and sp(x,v)==0]
        C = tuple(sorted(set(H)|set(perp)))
        assert len(C) == 12
        carriers[C] = 1
C = sorted(carriers)
ci = {c:i for i,c in enumerate(C)}
assert len(C) == 325
F = np.zeros((156,325),dtype=np.uint8)
for j,c in enumerate(C): F[list(c),j] = 1
assert set(F.sum(0)) == {12}
assert set(F.sum(1)) == {25}
assert gf2_rank(F) == 65

I = F.T.astype(np.int16) @ F.astype(np.int16)
A = (I == 2)
np.fill_diagonal(A,False)
assert set(A.sum(1)) == {144}

# Pass5230: weight-8 structure and complete shell orbit.
w8 = (119,124,183,188,209,302,317,318)
assert np.all((F[:,w8].sum(1) % 2) == 0)
assert Counter(F[:,w8].sum(1)) == Counter({0:108,2:48})

def transvection_block_perm(v):
    pp=[]
    for x in pts:
        a=sp(x,v)
        y=canon(tuple((x[i]+a*v[i])%P for i in range(4)))
        pp.append(pi[y])
    bp=[]
    for c in C:
        bp.append(ci[tuple(sorted(pp[i] for i in c))])
    return np.array(bp,dtype=int)

gens=[transvection_block_perm(v) for v in [
    (1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,0,1)
]]

def orbit(start):
    start=tuple(sorted(start)); seen={start}; Q=deque([start])
    while Q:
        s=Q.popleft()
        for g in gens:
            t=tuple(sorted(int(g[j]) for j in s))
            if t not in seen:
                seen.add(t); Q.append(t)
    return seen

O8=orbit(w8)
assert len(O8)==24375
assert sum(0 in s for s in O8)==600

# Exact fixed-block enumeration using the forced double-cover structure.
C0=set(C[0]); full=(1<<12)-1; list0=sorted(C0); idx0={p:i for i,p in enumerate(list0)}
fixed0=0
for m in [x for x in range(325) if x and not A[0,x]]:
    Cm=set(C[m]); listm=sorted(Cm); idxm={p:i for i,p in enumerate(listm)}
    data=[]
    for x in range(325):
        if x in (0,m) or not (A[0,x] and A[m,x]): continue
        a=C0 & set(C[x]); b=Cm & set(C[x])
        if len(a)==2 and len(b)==2:
            ma=sum(1<<idx0[p] for p in a); mb=sum(1<<idxm[p] for p in b)
            data.append((x,ma,mb))
    byp={i:[] for i in range(12)}
    for t in data:
        for i in range(12):
            if (t[1]>>i)&1: byp[i].append(t)
    def rec(chosen,u0,um):
        if len(chosen)==6:
            if u0!=full or um!=full: return 0
            s=(0,m)+chosen
            return int(np.all((F[:,s].sum(1)%2)==0))
        unc=(~u0)&full
        if not unc: return 0
        i=(unc & -unc).bit_length()-1
        ans=0
        for x,ma,mb in byp[i]:
            if x in chosen or ma&u0 or mb&um: continue
            ans += rec(chosen+(x,),u0|ma,um|mb)
        return ans
    fixed0 += rec(tuple(),0,0)
assert fixed0==600

# Shell span rank.
H8=np.zeros((len(O8),325),dtype=np.uint8)
for i,s in enumerate(O8): H8[i,list(s)]=1
assert gf2_rank(H8)==259

# Pass5231: one odd local check completes the dual parity-check rank.
w9=(15,20,38,44,139,164,197,278,311)
assert np.all((F[:,w9].sum(1)%2)==0)
H=np.vstack([H8,np.eye(1,325,0,dtype=np.uint8)])
H[-1]=0; H[-1,list(w9)]=1
assert gf2_rank(H)==260

# Pass5232/5236: pair-codegree refinement and rank-4 association scheme.
pair=np.zeros((325,325),dtype=np.int16)
for s in O8:
    for ii,a in enumerate(s):
        for b in s[ii+1:]: pair[a,b]+=1; pair[b,a]+=1
assert Counter(pair[np.triu(A,1)]) == Counter({25:23400})
non=[]
for i in range(325):
    for j in range(i+1,325):
        if not A[i,j]: non.append(int(pair[i,j]))
assert Counter(non)==Counter({5:19500,0:9750})
R0=np.eye(325,dtype=np.int16)
R1=A.astype(np.int16)
R2=(pair==5).astype(np.int16); np.fill_diagonal(R2,0)
R3=(pair==0).astype(np.int16); np.fill_diagonal(R3,0)
assert np.all(R0+R1+R2+R3==1)
assert set(R2.sum(1))=={120} and set(R3.sum(1))=={60}
rels=[R0,R1,R2,R3]
expected={
 (1,1):[144,68,60,60], (1,2):[0,50,54,60], (1,3):[0,25,30,24],
 (2,2):[120,45,45,40], (2,3):[0,25,20,20], (3,3):[60,10,10,15],
}
for (i,j),want in expected.items():
    M=rels[i].astype(np.int32)@rels[j].astype(np.int32)
    got=[]
    for k in range(4):
        u=np.unique(M[rels[k].astype(bool)])
        assert len(u)==1; got.append(int(u[0]))
    assert got==want,(i,j,got)

# Pass5235/5237: Hoffman 13-cover systematic quotient.
cover=[6,30,73,111,128,140,157,189,193,226,254,277,320]
assert Counter(F[:,cover].sum(1))==Counter({1:156})
assert gf2_rank(F[:,cover])==13
comp=[j for j in range(325) if j not in cover]
assert gf2_rank(F[:,comp])==65

print("PASS5230-5237 OK")
print("weight8_shell=24375 fixed_coordinate=600 span_rank=259")
print("sparse_dual_basis=259x8+1x9 rank=260")
print("association_scheme_valencies=144,120,60")
print("hoffman13_projection_rank=13 shortened_dimension=52")
print("FIREWALL: primal d(C_F)=25 and q5 leader36 remain open")
