#!/usr/bin/env python3
"""Pass 4583 -- first equivariant nonlinear protected-to-exceptional-six bridge.

Pass 4556 proved Hom_G(H10,U6)=0.  Here the middle protected V8 is sent through
its alternating square.  The contraction hyperplane K27=ker(B:Lambda^2 V8->F2)
contains a 15D invariant core K15 and

    K27/K15 = U6 direct-sum U6.

The three 6D invariant submodules of that 12D quotient are exhaustive, simple,
faithful PSp(4,3)-modules with nonzero vector orbits 27+36, hence the same
O^-(6,2) carrier as the Schlaefli/double-six lane.  Thus an orthogonal pair
(v,w) has an equivariant bilinear image through v wedge w.  Choosing two of the
three invariant 6-spaces gives an equivariant projection onto one U6 factor.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,transvection_matrix
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4583_WEDGE2_EXCEPTIONAL_SIX_BRIDGE.json'

def rref(rows,n):
    A=[int(x) for x in rows if x];r=0
    for c in range(n):
        p=next((i for i in range(r,len(A)) if (A[i]>>c)&1),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r]
        for i in range(len(A)):
            if i!=r and ((A[i]>>c)&1):A[i]^=A[r]
        r+=1
        if r==len(A):break
    return tuple(A[:r])
def rank(rows,n):return len(rref(rows,n))
def solver(basis):
    d={}
    for i,v in enumerate(basis):
        y=int(v);c=1<<i
        while y:
            p=y.bit_length()-1
            if p in d:y^=d[p][0];c^=d[p][1]
            else:d[p]=(y,c);break
    def f(v):
        y=int(v);c=0
        while y:
            p=y.bit_length()-1
            if p not in d:raise ValueError
            y^=d[p][0];c^=d[p][1]
        return c
    return f
def choose_basis(sub,superrows,n):
    B=[]
    for x in list(sub)+list(superrows):
        if rank(B+[x],n)>len(B):B.append(int(x))
    assert len(B)==rank(superrows,n);return B
def apply(cols,x):
    y=0
    for i,c in enumerate(cols):
        if (x>>i)&1:y^=int(c)
    return y
def cyclic(seed,gens,n):
    B=list(rref([seed],n))
    while True:
        old=len(B);B=list(rref(B+[apply(g,x) for x in B for g in gens],n))
        if len(B)==old:return tuple(B)
def subactions(basis,gens,n):
    sol=solver(basis);return [[sol(apply(g,b)) for b in basis] for g in gens]
def quotient_actions(basis,subdim,gens,n):
    sol=solver(basis);return [[sol(apply(g,b))>>subdim for b in basis[subdim:]] for g in gens]
def compose_perm(p,q):return tuple(p[q[i]] for i in range(len(p)))
def perm_group(gens,n=40):
    I=tuple(range(n));S={I};Q=deque([I])
    while Q:
        a=Q.popleft()
        for g in gens:
            z=compose_perm(g,a)
            if z not in S:S.add(z);Q.append(z)
    return S
def pmask(mask,p):
    y=0
    for i in range(len(p)):
        if (mask>>i)&1:y|=1<<p[i]
    return y
def compose_lin(g,h):return tuple(apply(g,h[i]) for i in range(len(h)))
def lin_group(gens,n):
    I=tuple(1<<i for i in range(n));S={I};Q=deque([I]);gg=[tuple(g) for g in gens]
    while Q:
        a=Q.popleft()
        for g in gg:
            z=compose_lin(g,a)
            if z not in S:S.add(z);Q.append(z)
    return S
def orbit(seed,gens):
    S={seed};Q=deque([seed])
    while Q:
        x=Q.popleft()
        for g in gens:
            y=apply(g,x)
            if y not in S:S.add(y);Q.append(y)
    return S

def main()->int:
    pts,pidx,lines,lidx,_,A,_,_,_=build_geometry();A=np.asarray(A,dtype=np.uint8);j=(1<<40)-1
    cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(A[:,c]):m|=1<<int(r)
        cols.append(m)
    edges=[(i,k) for i in range(40) for k in range(i+1,40) if A[i,k]]
    # V9 basis with fixed j first, then eight protected edges.
    B9=[j]
    for i,k in edges:
        x=cols[i]^cols[k]
        if rank(B9+[x],40)>len(B9):B9.append(x)
        if len(B9)==9:break
    assert len(B9)==9;sol9=solver(B9)
    def v8(v):return sol9(v)>>1
    # PSp generators from transvections.
    cand=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    pgens=[];G={tuple(range(40))}
    for g in cand:
        if g in G:continue
        pgens.append(g);G=perm_group(pgens)
        if len(G)==25920:break
    assert len(G)==25920
    G8=[]
    for p in pgens:G8.append([v8(pmask(b,p)) for b in B9[1:]])
    assert all(rank(g,8)==8 for g in G8)
    # Quadratic polarization in the chosen V8 basis.
    def q(mask):
        x=0
        for i,b in enumerate(B9[1:]):
            if (mask>>i)&1:x^=b
        return (x.bit_count()//4)&1
    P=np.zeros((8,8),dtype=np.uint8)
    for i in range(8):
        for k in range(i+1,8):P[i,k]=P[k,i]=q((1<<i)^(1<<k))^q(1<<i)^q(1<<k)
    assert np.array_equal(P,np.kron(np.eye(4,dtype=np.uint8),np.array([[0,1],[1,0]],dtype=np.uint8)))
    pairs=[(i,k) for i in range(8) for k in range(i+1,8)];idx={p:i for i,p in enumerate(pairs)}
    def wedge(v,w):
        z=0
        for a,b in pairs:
            bit=(((v>>a)&1)&((w>>b)&1))^(((v>>b)&1)&((w>>a)&1))
            if bit:z|=1<<idx[(a,b)]
        return z
    WG=[]
    for g in G8:
        WG.append([wedge(g[i],g[k]) for i,k in pairs])
    # Standard cyclic spans expose invariant 16D and contraction-kernel 27D spaces.
    spans={}
    for i in range(28):
        S=cyclic(1<<i,WG,28);spans.setdefault(len(S),S)
    assert set(spans)=={16,27};K16,K27=spans[16],spans[27]
    contraction=sum(1<<idx[(2*i,2*i+1)] for i in range(4))
    assert all(((x&contraction).bit_count()&1)==0 for x in K27) and len(K27)==27
    # K16 has a 15D invariant submodule; it is exactly K16 intersect K27.
    G16=subactions(list(K16),WG,28);S15=None
    for i in range(16):
        S=cyclic(1<<i,G16,16)
        if len(S)==15:S15=S;break
    assert S15 is not None
    K15=[apply(list(K16),x) for x in S15];assert len(rref(K15,28))==15 and all(rank(list(K27)+[x],28)==27 for x in K15)
    B27=choose_basis(K15,K27,28);Q12=quotient_actions(B27,15,WG,28)
    # Exhaust the 12D quotient.
    prof=Counter();sub6=set()
    for x in range(1,1<<12):
        S=cyclic(x,Q12,12);prof[len(S)]+=1
        if len(S)==6:sub6.add(rref(S,12))
    assert prof==Counter({12:3906,6:189}) and len(sub6)==3
    six=sorted(sub6);assert all(rank(list(six[i])+list(six[k]),12)==12 for i in range(3) for k in range(i+1,3))
    G6=subactions(list(six[0]),Q12,12)
    assert all(len(cyclic(x,G6,6))==6 for x in range(1,64))
    assert len(lin_group(G6,6))==25920
    rem=set(range(1,64));orbits=[]
    while rem:
        O=orbit(min(rem),G6);orbits.append(len(O));rem-=O
    assert sorted(orbits)==[27,36]
    # Choose first six-space as target and second as invariant complement; projection is equivariant.
    direct=list(six[0])+list(six[1]);sol12=solver(direct);sol27=solver(B27)
    def project_u6(z):
        q12=sol27(z)>>15;return sol12(q12)&63
    def pol(v,w):
        z=0
        for i in range(8):
            if (v>>i)&1:
                for k in range(8):
                    if ((w>>k)&1) and P[i,k]:z^=1
        return z
    images=Counter();npairs=0
    for v in range(1,256):
        for w in range(v+1,256):
            if pol(v,w):continue
            z=wedge(v,w);assert z and rank(list(K27)+[z],28)==27
            images[project_u6(z)]+=1;npairs+=1
    assert npairs==16065 and len(images)==64 and images[0]==945
    assert Counter(images[u] for u in range(1,64))==Counter({240:63})
    out={'pass':4583,'alternating_square':{'dimension':28,'contraction_kernel_dimension':27,'core_dimension':15,
      'quotient':'K27/K15','quotient_dimension':12,'structure':'U6 direct-sum U6','six_submodules':3,'cyclic_profile_nonzero':dict(sorted(prof.items()))},
      'U6_factor':{'dimension':6,'irreducible_exhaustive':True,'PSp_image_order':25920,'nonzero_orbits':[27,36]},
      'bridge':{'domain':'unordered distinct orthogonal pairs (v,w) in nonzero V8','pair_count':16065,
        'map':'(v,w) -> v wedge w in K27 -> K27/K15 -> chosen invariant U6 factor','image_size':64,
        'zero_preimages':945,'each_nonzero_U6_preimages':240,'equivariance':'exact for PSp(4,3)'},
      'theorem':'Although no nonzero equivariant linear H10<->U6 map exists, the orthogonal-pair alternating square gives an exact PSp-equivariant bilinear bridge from protected V8 pairs onto the exceptional O-(6,2) six-space.',
      'boundary':'The bridge is bilinear and pair-valued; it is not a canonical unary map from one protected state to one cubic-surface object, and choosing one of the three U6 factors is an additional equivariant splitting choice.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
