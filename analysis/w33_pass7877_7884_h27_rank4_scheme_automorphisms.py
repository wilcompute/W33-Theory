#!/usr/bin/env python3
"""Pass7877-7884: full automorphism group of the 27-point rank-4 H27/Schlaefli scheme.

Pass7701 identifies the three nontrivial relations as Z(H27)\{1} (9 K3),
Schlaefli degree 16, and the horizontal H27 Cayley relation degree 8.  Pass7186
already found Aut(horizontal H27 graph)=H27:GL(2,3), order 1296.  Here we ask the
stronger simultaneous question: which permutations preserve all three relation
colors?  Exhaustive colored-graph automorphism enumeration gives exactly 1296,
and an explicit H27 left-regular x GL(2,3) construction supplies 1296 such maps.
Thus the entire association scheme has the same automorphism group.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7877_7884_H27_RANK4_SCHEME_AUTOMORPHISMS.json'
F=[(x,y) for x in range(3) for y in range(3)]
V=[(u,z) for u in F for z in range(3)]
vi={x:i for i,x in enumerate(V)}

def add(u,v):return ((u[0]+v[0])%3,(u[1]+v[1])%3)
def neg(u):return ((-u[0])%3,(-u[1])%3)
def det(u,v):return (u[0]*v[1]-u[1]*v[0])%3
def mul(x,y):
    u,z=x;v,w=y;return (add(u,v),(z+w-det(u,v))%3)
def inv(x):u,z=x;return (neg(u),(-z)%3)
def detM(M):return (M[0][0]*M[1][1]-M[0][1]*M[1][0])%3
def Mv(M,u):return ((M[0][0]*u[0]+M[0][1]*u[1])%3,(M[1][0]*u[0]+M[1][1]*u[1])%3)

def relation(x,y):
    if x==y:return 0
    d=mul(inv(x),y)
    if d[0]==(0,0):return 1
    if d[1]==0:return 3
    return 2

def main():
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):G.add_edge(i,j,c=relation(V[i],V[j]))
    prof=Counter()
    for i in range(27):prof[tuple(sorted(Counter(G[i][j]['c'] for j in G[i]).items()))]+=1
    assert prof==Counter({((1,2),(2,16),(3,8)):27})

    em=nx.algorithms.isomorphism.categorical_edge_match('c',None)
    GM=nx.algorithms.isomorphism.GraphMatcher(G,G,edge_match=em)
    total=0;fix0=0
    for m in GM.isomorphisms_iter():
        total+=1;fix0+=int(m[0]==0)
    assert (total,fix0)==(1296,48)

    GL=[]
    for z in itertools.product(range(3),repeat=4):
        M=((z[0],z[1]),(z[2],z[3]))
        if detM(M)!=0:GL.append(M)
    assert len(GL)==48
    explicit=set()
    for h in V:
      for M in GL:
        d=detM(M)
        p=[]
        for x in V:
            u,z=x;phi=(Mv(M,u),(d*z)%3);p.append(vi[mul(h,phi)])
        p=tuple(p);assert len(set(p))==27
        for i,j in itertools.combinations(range(27),2):assert relation(V[i],V[j])==relation(V[p[i]],V[p[j]])
        explicit.add(p)
    assert len(explicit)==1296

    # Point stabilizer acts as GL2(3) and its projective action on the four
    # one-dimensional directions of F3^2 is S4=PGL2(3).
    dirs=[]
    def canon(u):
        if u==(0,0):raise ValueError
        return u if next(x for x in u if x)!=2 else ((2*u[0])%3,(2*u[1])%3)
    dirs=sorted({canon(u) for u in F if u!=(0,0)});assert len(dirs)==4
    dperms=set()
    for M in GL:dperms.add(tuple(dirs.index(canon(Mv(M,u))) for u in dirs))
    assert len(dperms)==24

    out={
      'schema':'w33.pass7877_7884.h27_rank4_scheme_automorphisms.v1','status':'PASS','passes':'7877-7884',
      'relation_degrees':{'Z_nonidentity':2,'Schlaefli':16,'H27_horizontal':8},
      'colored_scheme_automorphism_order':total,'point_stabilizer_order':fix0,
      'explicit_group':'H27 : GL(2,3)','translation_order':27,'linear_order':48,
      'four_direction_quotient':'GL(2,3)/{+-I}=PGL(2,3)=S4, order 24',
      'theorem':'The full simultaneous automorphism group of the 9K3/Schlaefli/H27 rank-4 scheme is exactly H27:GL(2,3), order 1296. No additional Schlaefli symmetry survives once the central-triangle and horizontal-Cayley colors are retained.',
      'prior_art_boundary':'Pass7186 already computed order 1296 for the horizontal H27 graph alone; Pass7701 identified the rank-4 Cayley scheme. This pass proves the simultaneous colored-scheme automorphism group and gives the explicit semidirect realization.',
      'claim_boundary':'Exact finite permutation-group theorem; no physical controller interpretation is forced.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','Aut':1296,'stabilizer':48,'structure':'H27:GL2(3)'}))
if __name__=='__main__':main()
