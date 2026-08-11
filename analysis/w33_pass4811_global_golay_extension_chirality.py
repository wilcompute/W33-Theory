#!/usr/bin/env python3
"""Pass 4811 — globalize the 54 local ternary-Golay extension directions.

Each of the 27 GQ(4,2) K5 fibers carries G10=[10,6,4]_3. Pass4806 found two
projective one-coordinate extension directions giving G11=[11,6,5]_3.

First, exhaust all S5 permutations of the five local points and compute their
induced monomial action on G10. The two projective extension directions transform
by parity: A5 fixes each direction and every odd permutation swaps them.

Second, transport that parity through the actual automorphism action of the
27-line intersection graph. The resulting 54-object cover has two PSp(4,3)
orbits of 27, each projecting bijectively to the fibers, while the full
order-51840 group is transitive and exchanges the two sheets.

Consequently either PSp sheet gives a monomially equivariant direct sum of 27
perfect ternary Golay G11 blocks, [297,162,5]_3. Adjoining both directions gives
27 extended ternary Golay G12 blocks, a self-dual [324,162,6]_3 direct sum,
which is invariant under the full outer action.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import networkx as nx
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4811_GLOBAL_GOLAY_EXTENSION_CHIRALITY.json'

def rank_mod(A,p=3):
    A=np.array(A,dtype=int)%p;r=0;piv=[]
    for c in range(A.shape[1]):
        s=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if s is None:continue
        A[[r,s]]=A[[s,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        piv.append(c);r+=1
    return r,piv,A

def nullspace(A,p=3):
    r,piv,R=rank_mod(A,p);free=[c for c in range(R.shape[1]) if c not in piv];B=[]
    for f in free:
        x=np.zeros(R.shape[1],dtype=int);x[f]=1
        for i,c in enumerate(piv):x[c]=(-R[i,f])%p
        B.append(x)
    return np.array(B,dtype=int)

def local_extension_directions():
    tris=list(itertools.combinations(range(5),3));M=np.zeros((5,10),dtype=int)
    for j,t in enumerate(tris):M[list(t),j]=1
    G=nullspace(M);assert G.shape==(6,10)
    msgs=np.array(list(itertools.product(range(3),repeat=6)),dtype=int);C=(msgs@G)%3;base=np.count_nonzero(C,axis=1)
    good=[]
    for a in itertools.product(range(3),repeat=6):
        if not any(a):continue
        aa=np.array(a,dtype=int);w=base+((msgs@aa)%3!=0)
        if min(w[1:])>=5:good.append(tuple(map(int,aa)))
    assert len(good)==4
    dirs=[]
    for a in good:
        b=tuple((2*x)%3 for x in a);rep=min(a,b)
        if rep not in dirs:dirs.append(rep)
    assert len(dirs)==2
    # Coordinate permutation induced by each S5 permutation, followed by solving
    # for the induced 6x6 message map R with R G = G P.
    def parity(p):return sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))&1
    def solve_coeff(v):
        # brute-force 3^6 is tiny and avoids basis-convention assumptions.
        for a in itertools.product(range(3),repeat=6):
            if np.array_equal((np.array(a)@G)%3,v%3):return np.array(a,dtype=int)
        raise AssertionError
    preserved=swapped=0
    for p in itertools.permutations(range(5)):
        idx={t:i for i,t in enumerate(tris)}
        cp=[idx[tuple(sorted(p[x] for x in t))] for t in tris]
        GP=G[:,cp]
        R=np.vstack([solve_coeff(GP[i]) for i in range(6)])%3
        image=[]
        # extension functional a transforms contragrediently: find b with R b = a.
        for a in dirs:
            aa=np.array(a,dtype=int);b=None
            for z in itertools.product(range(3),repeat=6):
                zz=np.array(z,dtype=int)
                if np.array_equal((R@zz)%3,aa):b=tuple(map(int,zz));break
            assert b is not None
            rep=min(b,tuple((2*x)%3 for x in b));image.append(dirs.index(rep))
        if parity(p)==0:
            assert image==[0,1];preserved+=1
        else:
            assert image==[1,0];swapped+=1
    assert preserved==swapped==60
    return dirs

def Qm(v):
    x1,x2,x3,x4,x5,x6=v
    return (x1*x2+x3*x4+x5+x5*x6+x6)&1

def bits(x):return tuple((x>>i)&1 for i in range(6))

def geom():
    qp=[x for x in range(1,64) if Qm(bits(x))==0]
    pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    lines=[tuple(i for i,P in enumerate(pts) if p in P) for p in qp]
    inc={p:tuple(i for i,L in enumerate(lines) if p in L) for p in range(45)}
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if len(set(lines[i])&set(lines[j]))==1:G.add_edge(i,j)
    return lines,inc,G

def groups(G):
    GM=nx.algorithms.isomorphism.GraphMatcher(G,G);gens=[];H=PermutationGroup(Permutation(list(range(27))))
    for m in GM.isomorphisms_iter():
        p=Permutation([m[i] for i in range(27)])
        if not H.contains(p):
            gens.append(p);H=PermutationGroup(gens)
            if H.order()==51840:break
    assert H.order()==51840;D=H.derived_subgroup();assert D.order()==25920
    return D,H

def local_parity(lines,inc,g,ell):
    # Identify each GQ point by its incident triple of line vertices.
    triple_to_point={frozenset(v):p for p,v in inc.items()}
    src=list(lines[ell]);dst=list(lines[int(g(ell))]);pos={p:i for i,p in enumerate(dst)}
    perm=[]
    for p in src:
        image=triple_to_point[frozenset(int(g(x)) for x in inc[p])]
        perm.append(pos[image])
    return sum(perm[i]>perm[j] for i in range(5) for j in range(i+1,5))&1

def cover_orbit(group,lines,inc,seed):
    seen={seed};q=[seed]
    while q:
        ell,d=q.pop()
        for g in group.generators:
            y=(int(g(ell)),d^local_parity(lines,inc,g,ell))
            if y not in seen:seen.add(y);q.append(y)
    return seen

def main():
    dirs=local_extension_directions();lines,inc,G=geom();PSp,Full=groups(G)
    o0=cover_orbit(PSp,lines,inc,(0,0));o1=cover_orbit(PSp,lines,inc,(0,1));of=cover_orbit(Full,lines,inc,(0,0))
    assert len(o0)==len(o1)==27 and o0.isdisjoint(o1) and len(of)==54 and of==o0|o1
    assert {ell for ell,d in o0}==set(range(27)) and {ell for ell,d in o1}==set(range(27))
    out={'pass':4811,'local_projective_extension_directions':2,'local_S5_action':'A5 fixes both directions; every odd permutation swaps them',
      'local_even_permutations_checked':60,'local_odd_permutations_checked':60,
      'global_cover_size':54,'PSp_order':25920,'PSp_orbit_sizes':[27,27],'PSp_direction_stabilizer_order':960,
      'full_order':51840,'full_orbit_sizes':[54],'full_direction_stabilizer_order':960,
      'one_sheet_code':'direct_sum_27 G11 = [297,162,5]_3, monomially PSp-equivariant',
      'both_sheets_code':'direct_sum_27 G12 = [324,162,6]_3, self-dual and full-outer equivariant',
      'theorem':'The 54 local Golay extension directions form a canonical two-sheet cover of the 27 GQ(4,2) fibers. PSp(4,3) preserves the two 27-sheets separately; the outer extension exchanges them and is transitive on all 54.',
      'boundary':'The two 27-sheets are not identified with E6 27 and conjugate-27 representations from cardinality alone. Any such identification requires an explicit representation intertwiner.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
