#!/usr/bin/env python3
"""Exact finite control light-cone on the 72-element packet runtime group.

Runtime group:
    G = F3^2 semidirect D8, |G|=72.

Take as one-control-tick primitives the symmetric set
    +/- e_rho translation,
    +/- e_a translation,
    R, R^{-1},
    S.
These are exactly the two qutrit/Hesse translation axes, the probe quarter-turn
and its inverse, and the reflection/sector primitive already used by the packet
ABI.

The undirected Cayley graph is 7-regular.  Exact BFS gives distance shells
    1, 7, 19, 25, 16, 4
and diameter 5, so cumulative causal reach is
    1, 8, 27, 52, 68, 72.
The radius-two count 27 is exact but is NOT a Heisenberg H27 subgroup:
27 does not divide 72 and the radius-two ball is not closed under multiplication.

The adjacency spectrum is integral:
  7^1, 5^3, 4^4, 3^3, 2^12, 1^5, 0^12,
  (-1)^12, (-2)^4, (-3)^12, (-5)^4.
Hence the simple random-walk spectral gap is (7-5)/7 = 2/7.

This is a finite control/locality theorem. It does not identify graph distance
with spacetime distance or derive the physical speed of light.
"""
from __future__ import annotations
import json
from collections import Counter,deque
from fractions import Fraction as F
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_packet72_cayley_causal_cone.json'
I=(1,0,0,1);R=(0,2,1,0);S=(1,0,0,2)

def mm(A,B):
    return tuple(sum(A[2*i+k]*B[2*k+j] for k in range(2))%3
                 for i in range(2) for j in range(2))
def mv(A,v):
    return ((A[0]*v[0]+A[1]*v[1])%3,(A[2]*v[0]+A[3]*v[1])%3)
def mpow(A,n):
    o=I
    for _ in range(n):o=mm(o,A)
    return o
D8=[]
for s in range(2):
    for p in range(4):
        L=mm(mpow(S,s),mpow(R,p))
        if L not in D8:D8.append(L)
T=[(x,y) for x in range(3) for y in range(3)]
G=[(t,L) for t in T for L in D8]

def mul(g,h):
    t,L=g;u,M=h;Lu=mv(L,u)
    return (((t[0]+Lu[0])%3,(t[1]+Lu[1])%3),mm(L,M))

def main(write=True):
    e=((0,0),I)
    gens=[
      ((1,0),I),((2,0),I),((0,1),I),((0,2),I),
      ((0,0),R),((0,0),mpow(R,3)),((0,0),S)]
    assert len(gens)==7
    # symmetric generator set
    assert all(any(mul(g,h)==e and mul(h,g)==e for h in gens) for g in gens)

    dist={e:0};q=deque([e])
    while q:
        g=q.popleft()
        for s in gens:
            h=mul(g,s)
            if h not in dist:
                dist[h]=dist[g]+1;q.append(h)
    assert len(dist)==72
    shell=Counter(dist.values())
    assert shell==Counter({0:1,1:7,2:19,3:25,4:16,5:4})
    cumulative=[];z=0
    for r in range(6):
        z+=shell[r];cumulative.append(z)
    assert cumulative==[1,8,27,52,68,72]

    # Radius-two ball is not a subgroup.
    B2={g for g,d in dist.items() if d<=2}
    assert len(B2)==27
    not_closed=next((a,b,mul(a,b)) for a in B2 for b in B2 if mul(a,b) not in B2)
    assert 72%27!=0

    idx={g:i for i,g in enumerate(G)}
    A=[[0]*72 for _ in range(72)]
    for g in G:
        i=idx[g]
        for s in gens:
            A[i][idx[mul(g,s)]]=1
    assert all(sum(r)==7 for r in A)
    assert all(A[i][j]==A[j][i] for i in range(72) for j in range(72))

    # Exact spectrum by SymPy over integers.
    ev=sp.Matrix(A).eigenvals()
    spectrum={int(k):int(v) for k,v in ev.items()}
    expected={7:1,5:3,4:4,3:3,2:12,1:5,0:12,-1:12,-2:4,-3:12,-5:4}
    assert spectrum==expected
    assert sum(spectrum.values())==72
    gap=F(7-5,7)
    assert gap==F(2,7)

    parent=json.loads((ROOT/'data/w33_punctured_hesse_packet_group.json').read_text())
    assert parent['q3_group']['order']==72

    out={
      'schema':'w33.packet72_cayley_causal_cone.v1',
      'status':'PASS_FINITE_CONTROL_CAUSAL_CONE',
      'headline':'With the seven natural runtime primitives as one-tick local controls, the 72-element packet group has an exact 7-regular Cayley light-cone of diameter5. Distance shells are 1,7,19,25,16,4 and cumulative reach is 1,8,27,52,68,72. The adjacency spectrum is integral and the simple-random-walk gap is 2/7.',
      'group':'F3^2 semidirect D8','order':72,
      'primitive_controls':['+rho','-rho','+a','-a','R','R^-1','S'],
      'cayley_graph':{
        'degree':7,'diameter':5,
        'distance_shells':[shell[i] for i in range(6)],
        'cumulative_balls':cumulative,
        'adjacency_spectrum':{str(k):v for k,v in sorted(spectrum.items(),reverse=True)},
        'random_walk_spectral_gap':'2/7'},
      'radius_two_27':{
        'count':27,'is_subgroup':False,
        'lagrange_obstruction':'27 does not divide 72',
        'closure_counterexample':{
          'left':str(not_closed[0]),'right':str(not_closed[1]),
          'product':str(not_closed[2])}},
      'physics_reading':'The controller has a strict finite propagation bound in word metric: no sequence of n primitive operations can leave the radius-n Cayley ball, and every runtime state is reachable in at most five primitive ticks. This is a control-plane analogue of a causal cone, not a spacetime theorem.',
      'boundary':'Graph/control distance is not physical length and the five-tick diameter does not determine c or a Lieb-Robinson velocity without a Hamiltonian, gate duration, and physical locality map.',
      'parent':'data/w33_punctured_hesse_packet_group.json',
      'checks':{'group72':True,'degree7':True,'diameter5':True,'balls_1_8_27_52_68_72':True,
                'radius2_not_H27_subgroup':True,'integral_spectrum':True,'gap_2_7':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':main(True)
