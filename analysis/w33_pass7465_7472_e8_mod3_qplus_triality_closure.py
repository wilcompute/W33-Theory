#!/usr/bin/env python3
"""Pass7465-7472: close the global E8 triality geometry via E8/3E8.

Each E8 A2 subsystem has a canonical 1D radical modulo 3.  These 1120 radicals
are exactly the singular projective points of Q+(7,3).  Each of the 2240
Eisenstein W33 leaves is exactly the 40-point projective point set of a maximal
totally singular 4-space.  The two leaf parity halves are the two generator
families of Q+(7,3).  Hence the 1120+1120+1120 triad is the classical D4
point/generator/generator triality geometry.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np
import w33_pass7425_7432_e8_2240_leaf_geometry as leaf

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7465_7472_E8_MOD3_QPLUS_TRIALITY_CLOSURE.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def canon3(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple((x*y)%3 for y in v) if x==1 else tuple((2*y)%3 for y in v)
    raise ValueError('zero')
def rank3(M):return leaf.rank_mod(np.asarray(M,dtype=np.int16),3)
def gf2rank(rows):
    piv={}
    for x0 in rows:
        x=int(x0)
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def main():
    R=leaf.roots();I={r:i for i,r in enumerate(R)};A2=leaf.enum_a2(R);ai={S:i for i,S in enumerate(A2)}
    # Canonical radical of the A2 Gram form modulo 3: for simple roots a,b,
    # rad = <a-b>.  Independence from chosen adjacent root pair is checked.
    radicals=[]
    for S in A2:
        vals=set()
        for i,j in itertools.combinations(sorted(S),2):
            if leaf.dot(R[i],R[j])==-4:
                vals.add(canon3(tuple(R[i][k]-R[j][k] for k in range(8))))
        assert len(vals)==1
        radicals.append(next(iter(vals)))
    assert len(set(radicals))==1120
    assert all(sum(x*x for x in v)%3==0 for v in radicals)
    singular=set()
    for v in itertools.product(range(3),repeat=8):
        if any(v) and sum(x*x for x in v)%3==0:singular.add(canon3(v))
    assert len(singular)==1120 and set(radicals)==singular
    # 1120 singular projective points distinguishes plus type in dimension 8 over F3.
    q=3;per_generator_family=(q+1)*(q*q+1)*(q**3+1)
    assert per_generator_family==1120
    # Rebuild all 2240 leaves.
    rg=[tuple(I[leaf.refl(r,s)] for r in R) for s in leaf.SIMPLES]
    c=tuple(range(240))
    for g in rg:c=comp(g,c)
    J=tuple(range(240))
    for _ in range(10):J=comp(c,J)
    ag=[tuple(ai[frozenset(g[x] for x in S)] for S in A2) for g in rg]
    base=frozenset(i for i,S in enumerate(A2) if frozenset(J[x] for x in S)==S);assert len(base)==40
    leaves=[base];li={base:0};dq=deque([base])
    while dq:
        X=dq.popleft()
        for g in ag:
            Y=frozenset(g[x] for x in X)
            if Y not in li:li[Y]=len(leaves);leaves.append(Y);dq.append(Y)
    assert len(leaves)==2240
    # Every leaf radical set spans a rank-4 totally singular vector subspace; its
    # 40 projective points are therefore the complete PG(3,3) point set.
    for L in leaves:
        V=np.asarray([radicals[x] for x in L],dtype=np.int16)%3
        assert rank3(V)==4 and not np.any((V@V.T)%3)
    assert len({frozenset(radicals[x] for x in L) for L in leaves})==2240
    # Leaf overlap parity gives the two classical generator classes.
    masks=[sum(1<<x for x in L) for L in leaves];G=[set() for _ in leaves]
    for i in range(2240):
        for j in range(i+1,2240):
            if (masks[i]&masks[j]).bit_count()==13:G[i].add(j);G[j].add(i)
    parity=[None]*2240;parity[0]=0;dq=deque([0])
    while dq:
        v=dq.popleft()
        for w in G[v]:
            if parity[w] is None:parity[w]=1-parity[v];dq.append(w)
            else:assert parity[w]!=parity[v]
    Lp=[i for i,x in enumerate(parity) if x==0];Lm=[i for i,x in enumerate(parity) if x==1]
    assert len(Lp)==len(Lm)==1120
    same=Counter();opp=Counter()
    for i in range(2240):
        for j in range(i+1,2240):
            z=(masks[i]&masks[j]).bit_count();(same if parity[i]==parity[j] else opp)[z]+=1
    assert set(same)=={0,4,40} and set(opp)=={1,13}
    projdim={0:0,1:1,4:2,13:3,40:4}
    assert all(projdim[z]%2==0 for z in same) and all(projdim[z]%2==1 for z in opp)
    # Build the full 3360 point/+generator/-generator triality graph.
    pp={v:i for i,v in enumerate(Lp)};pm={v:i for i,v in enumerate(Lm)}
    rows=[0]*3360
    for j,v in enumerate(Lp):
        b=1120+j
        for a in leaves[v]:rows[a]|=1<<b;rows[b]|=1<<a
    for j,v in enumerate(Lm):
        b=2240+j
        for a in leaves[v]:rows[a]|=1<<b;rows[b]|=1<<a
    for v in Lp:
        a=1120+pp[v]
        for w in G[v]:
            b=2240+pm[w];rows[a]|=1<<b;rows[b]|=1<<a
    assert {x.bit_count() for x in rows}=={80}
    r2=gf2rank(rows);assert r2==602
    # Exact distance distribution from one point in the full triality graph.
    adj=[]
    for r in rows:
        S=set();x=r
        while x:
            y=x&-x;S.add(y.bit_length()-1);x-=y
        adj.append(S)
    dist=[-1]*3360;dist[0]=0;dq=deque([0])
    while dq:
        v=dq.popleft()
        for w in adj[v]:
            if dist[w]<0:dist[w]=dist[v]+1;dq.append(w)
    assert Counter(dist)==Counter({2:2550,3:729,1:80,0:1})
    triangles=sum(len(adj[u]&adj[v]) for u in range(3360) for v in adj[u])//6
    assert triangles==582400
    # Spectrum follows from the exact centered pair-incidence groupoid of Pass7441:
    # trivial family-color space gives 80,-40,-40; common 300D sector gives
    # 24 and two copies of -12; the 3*819 orthogonal kernels give zero.
    spectrum={'80':1,'24':300,'0':2457,'-12':600,'-40':2}
    assert 80+24*300-12*600-40*2==0
    assert 80**2+300*24**2+600*12**2+2*40**2==3360*80
    assert 80**3+300*24**3-600*12**3-2*40**3==6*triangles
    out={
      'schema':'w33.pass7465_7472.e8_mod3_qplus_triality_closure.v1','status':'PASS','passes':'7465-7472',
      'mod3_quadratic_space':{'model':'E8/3E8 with the reduced E8 bilinear/quadratic form','dimension':8,'type':'plus','singular_projective_points':1120},
      'A2_radical_map':{'formula':'A2=<a,b> -> projective <a-b> mod 3','bijective_onto_Qplus_singular_points':True},
      'leaf_map':{'leaves':2240,'each_leaf_points':40,'span_dimension':4,'totally_singular':True,'object':'maximal totally singular PG(3,3)','generator_families':[1120,1120],'same_family_intersection_vector_dimensions':[4,2,0],'opposite_family_intersection_vector_dimensions':[3,1]},
      'triality_closure':'The three E8 families are exactly the three classical D4 triality types of Q+(7,3): singular points and the two families of maximal totally singular 4-spaces. Classical triality permutes these three types.',
      'pair_2240_identification':'The 2240 point/+generator (or point/-generator) graph is the D4(3) point-generator incidence graph. The earlier DSp(6,3) match was only an intersection-array match and is superseded by this explicit Q+(7,3) coordinatization.',
      'full_3360_graph':{'vertices':3360,'degree':80,'diameter':3,'distance_distribution':[1,80,2550,729],'relation_refinement_from_one_vertex':[1,80,390,2160,729],'triangles':triangles,'spectrum':spectrum,'binary_adjacency_rank':r2,'external_name':'O+(8,3), triality graph in the uniformity/association-scheme literature'},
      'outer_S3':'At the ambient polar-space level this is the standard D4 graph-automorphism S3 permuting points and the two generator classes. The E8 Weyl group embeds in O+(8,3) through E8 mod 3, as in the classical lattice construction.',
      'claim_boundary':'The finite-geometric identification is explicit and objectwise. No Standard Model or physical particle interpretation follows.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','Qplus':'1120 points + 1120+1120 generators','triality_graph':3360,'GF2rank':r2}))
if __name__=='__main__':main()
