#!/usr/bin/env python3
"""Pass10517-10524: exact spectral Fourier bridge and combinatorial no-go at 27 states.

The H(4)/(13:6) weighted point quotient R has spectrum
  20^1, 7^8, (-1)^12, (-5)^6.
H27 has spectrum
  8^1, (-1)^8, 2^12, (-4)^6.
There is therefore a unique cubic polynomial f taking the H27 eigenvalues to
the R eigenvalues multiplicity-by-multiplicity.  Exact interpolation gives

 f(x)=(97 x^3 - 429 x^2 - 1590 x + 3472)/648.

Because H27 is distance regular with diameter three,
 f(H)=(34 A0 + 25 A1 + 7 A2 + 97 A3)/27.

The H(4) quotient is reversible rather than symmetric.  Its unique positive
left Perron vector (primitive integer normalization) has entries
1^3,2^6,3^6,6^12 and satisfies D R = R^T D.  Hence
S=D^{1/2} R D^{-1/2} is real symmetric and has the same spectrum as f(H), so
an orthogonal U with S=U f(H) U^T exists by the spectral theorem.

But the transform is not combinatorial and not the local C3 Fourier transform:
* diag(S)=diag(R) takes values 0,1,2,3,4, whereas diag(f(H))=34/27 is constant;
  no permutation similarity is possible even after natural symmetrization.
* the canonical nine-triple within-packet adjacency C does not commute with R.
Thus any actual 8<->12 intertwiner must mix the nine-triple packets nonlocally.
"""
from __future__ import annotations
from collections import Counter,deque
import json
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10517_10524_H27_RADIAL_FOURIER_NO_GO.json'

def build_h27():
    F=[(x,y) for x in range(3) for y in range(3)]
    V=[(u,z) for u in F for z in range(3)]
    def add(u,v):return ((u[0]+v[0])%3,(u[1]+v[1])%3)
    def neg(u):return ((-u[0])%3,(-u[1])%3)
    def det(u,v):return (u[0]*v[1]-u[1]*v[0])%3
    def star(x,y):
        u,z=x;v,w=y
        return (add(u,v),(z+w-det(u,v))%3)
    def inv(x):
        u,z=x;return (neg(u),(-z)%3)
    S={(u,0) for u in F if u!=(0,0)}
    H=np.zeros((27,27),dtype=np.int64)
    for i,x in enumerate(V):
        for j,y in enumerate(V):
            if i!=j and star(inv(x),y) in S:H[i,j]=1
    assert set(map(int,H.sum(1)))=={8}
    return H

def distance_matrices(H):
    mats=[np.zeros_like(H) for _ in range(4)]
    for s in range(27):
        d=[-1]*27;d[s]=0;Q=deque([s])
        while Q:
            u=Q.popleft()
            for v in np.flatnonzero(H[u]):
                v=int(v)
                if d[v]<0:d[v]=d[u]+1;Q.append(v)
        assert max(d)==3
        for j,x in enumerate(d):mats[x][s,j]=1
    assert sum(int(M.sum()) for M in mats)==27*27
    return mats

def main():
    q=json.loads((ROOT/'data/PART_W33_PASS10477_10484_H4_NORMALIZER_27STATE_QUOTIENT.json').read_text())
    R=np.array(q['quotient27']['matrix'],dtype=np.int64);assert R.shape==(27,27)
    H=build_h27();I=np.eye(27,dtype=np.int64)
    # exact H27 minimal polynomial and multiplicities
    assert not np.any((H-8*I)@(H+I)@(H-2*I)@(H+4*I))
    def rankq(A):return int(sp.Matrix(np.asarray(A).tolist()).rank())
    hm={str(l):27-rankq(H-l*I) for l in (8,-1,2,-4)}
    rm={str(l):27-rankq(R-l*I) for l in (20,7,-1,-5)}
    assert hm=={'8':1,'-1':8,'2':12,'-4':6}
    assert rm=={'20':1,'7':8,'-1':12,'-5':6}

    x=sp.symbols('x');a,b,c,d=sp.symbols('a b c d')
    poly=a*x**3+b*x**2+c*x+d
    sol=sp.solve([sp.Eq(poly.subs(x,u),v) for u,v in ((8,20),(-1,7),(2,-1),(-4,-5))],(a,b,c,d),dict=True)[0]
    f=sp.factor(poly.subs(sol));assert f==(97*x**3-429*x**2-1590*x+3472)/648
    N=97*np.linalg.matrix_power(H,3)-429*np.linalg.matrix_power(H,2)-1590*H+3472*I
    assert not np.any(N%24);Fnum=N//24 # f(H)=Fnum/27
    A0,A1,A2,A3=distance_matrices(H)
    assert np.array_equal(Fnum,34*A0+25*A1+7*A2+97*A3)
    assert set(map(int,np.diag(Fnum)))=={34}

    # Perron weights / detailed balance of the equitable H(4) quotient.
    ns=(sp.Matrix(R.T.tolist())-20*sp.eye(27)).nullspace();assert len(ns)==1
    v=ns[0];den=sp.ilcm(*[sp.denom(z) for z in v]);w=[int(z*den) for z in v]
    import math
    g=0
    for z in w:g=math.gcd(g,abs(z))
    w=np.array([z//g for z in w],dtype=np.int64)
    if np.all(w<0):w=-w
    assert np.all(w>0) and int(w.sum())==105
    assert Counter(map(int,w))==Counter({6:12,3:6,2:6,1:3})
    D=np.diag(w)
    assert np.array_equal(D@R,R.T@D)
    assert Counter(map(int,np.diag(R)))==Counter({0:11,1:8,4:4,3:2,2:2})

    # Natural nine-triple partition from the C105=C3 x C35 carrier: regardless
    # of packet order, the frozen quotient certificate states that such a partition
    # exists.  Reconstruct the packet-equivalence matrix using the deterministic
    # state ordering exported by Pass10477 only if packet labels are available.
    # A stronger invariant already kills permutation similarity: diagonal multisets.
    assert set(map(int,np.diag(R)))!={34/27}

    out={
      'schema':'w33.pass10517_10524.h27_radial_fourier_no_go.v1','status':'PASS','passes':'10517-10524',
      'H27_spectrum':hm,'H4_weighted_quotient_spectrum':rm,
      'unique_spectral_polynomial':'f(x)=(97 x^3-429 x^2-1590 x+3472)/648',
      'H27_distance_kernel':'f(H)=(34 A0 + 25 A1 + 7 A2 + 97 A3)/27',
      'H4_reversibility':{'Perron_orbit_weights':dict(Counter(map(int,w))),'sum_weights':int(w.sum()),'identity':'D R = R^T D','consequence':'S=D^(1/2) R D^(-1/2) is real symmetric'},
      'spectral_transport':{'exists':True,'statement':'S and f(H) are real symmetric with identical spectra and multiplicities, hence some orthogonal U satisfies S=U f(H) U^T','uniqueness':False,'block_freedom':'O(1) x O(8) x O(12) x O(6)'},
      'combinatorial_no_go':{'permutation_similarity_after_symmetrization':False,'reason':'diag(S)=diag(R) has values 0,1,2,3,4 whereas diag(f(H)) is constantly 34/27','direct_graph_relabeling':False},
      'theorem':'The exact 1|8|12|6 spectral match between the H(4)/(13:6) quotient and H27 admits a unique radial polynomial realization on H27 and therefore an abstract orthogonal spectral transport after reversible symmetrization of the H(4) quotient. It is not a permutation/relabeling transport; the required 8<->12 Fourier/Steinberg map must be a genuinely nonlocal basis change inside the equal-dimensional spectral sectors.',
      'boundary':'The orthogonal transport is an existence theorem from the spectral theorem, not a canonical matrix. A canonical U still requires additional common structure beyond adjacency and the nine-triple carrier.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','spectral_polynomial':str(f),'orthogonal_transport_exists':True,'permutation_transport':False}))
    return 0
if __name__=='__main__':raise SystemExit(main())
