#!/usr/bin/env python3
"""Exact residual test for the order-576 Latin-square coincidence.

The 576 labelled 4x4 Latin squares split under the standard paratopy group
S4^3 : S3 into main classes 144+432.  The 144-class representative is the
C2^2 (Klein four) group table, so its paratopy stabilizer itself has order 576.
This script computes that stabilizer as permutations of the twelve coordinate
symbols and compares its exact invariants with the W33 minimum-vector
stabilizer H of order 576.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260828_LATIN144_STABILIZER_NOGO.json'
P4=list(itertools.permutations(range(4)))
P3=list(itertools.permutations(range(3)))

def table(kind):
    if kind=='C4': return tuple(tuple((r+c)%4 for c in range(4)) for r in range(4))
    return tuple(tuple(r^c for c in range(4)) for r in range(4))
def triples(L): return frozenset((r,c,L[r][c]) for r in range(4) for c in range(4))
def act_set(T,ap,ps):
    out=[]
    for t in T:
        u=[0]*3
        for i in range(3):u[ap[i]]=ps[i][t[i]]
        out.append(tuple(u))
    return frozenset(out)
def act12(ap,ps):
    p=[0]*12
    for i in range(3):
        for v in range(4):p[4*i+v]=4*ap[i]+ps[i][v]
    return tuple(p)
def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def inverse(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def order(p):
    seen=set();z=1
    for i in range(len(p)):
        if i in seen:continue
        j=i;n=0
        while j not in seen:seen.add(j);n+=1;j=p[j]
        z=math.lcm(z,n)
    return z
def stab_and_orbit(L):
    T=triples(L);stab=[];orbit=set()
    for ap in P3:
      for a in P4:
       for b in P4:
        for c in P4:
          ps=(a,b,c);U=act_set(T,ap,ps);orbit.add(U)
          if U==T:stab.append(act12(ap,ps))
    return stab,len(orbit)
def derived_size(G):
    ident=tuple(range(len(G[0])));inv={g:inverse(g) for g in G};C={ident}
    for g in G:
      for h in G:C.add(compose(compose(compose(inv[g],inv[h]),g),h))
    H={ident};q=deque([ident]);gens=list(C)
    while q:
      x=q.popleft()
      for g in gens:
        y=compose(g,x)
        if y not in H:H.add(y);q.append(y)
    return len(H)
def invariants(G):
    cen=sum(all(compose(g,h)==compose(h,g) for h in G) for g in G)
    return {'order':len(G),'centerOrder':cen,'derivedOrder':derived_size(G),
            'elementOrderCensus':dict(sorted(Counter(order(g) for g in G).items()))}
def main():
    c4,o4=stab_and_orbit(table('C4'));v4,ov=stab_and_orbit(table('V4'))
    assert (len(c4),o4)==(192,432) and (len(v4),ov)==(576,144)
    latin=invariants(v4)
    assert latin=={'order':576,'centerOrder':1,'derivedOrder':144,
      'elementOrderCensus':{1:1,2:75,3:80,4:180,6:240}}
    w33={'order':576,'centerOrder':2,'derivedOrder':96,
         'elementOrderCensus':{1:1,2:43,3:80,4:84,6:272,12:96}}
    assert latin!=w33 and 12 not in latin['elementOrderCensus'] and 12 in w33['elementOrderCensus']
    out={'schema':'w33.20260828.latin144-stabilizer-nogo.v1','status':'PASS',
      'paratopyGroup':{'structure':'S4^3 : S3','order':82944},
      'mainClasses':{'C2xC2_table':144,'C4_table':432},
      'latin144PointStabilizer':{**latin,'structure':'2^4 : (S3 x S3)'},
      'w33MinimumVectorStabilizer':{**w33,'structure':'2^{1+4}_+ : (S3 x C3)'},
      'noGo':['center orders differ: 1 vs 2','derived orders differ: 144 vs 96',
              'the W33 stabilizer has 96 elements of order 12; the Latin stabilizer has none'],
      'theorem':'The meaningful residual 576 coincidence is between two stabilizer groups: the paratopy stabilizer of a Klein-four Latin square in the 144-square main class and the W33 minimum-vector stabilizer. They are non-isomorphic by exact permutation-group invariants, so the residual canonical group bridge is ruled out.',
      'boundary':'This rules out identification through the standard 4x4 Latin-square paratopy action. It does not forbid an unrelated nonstandard action on a 144-element set.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','main_classes':[144,432],'latin576':latin,'w33_576':w33}))
if __name__=='__main__':main()
