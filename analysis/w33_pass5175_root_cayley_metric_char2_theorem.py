#!/usr/bin/env python3
"""Pass5175: symbolic root-Cayley word metric in characteristic two.

Pass5143 proves the shell formula in characteristic >3 and Pass5165 proves the
characteristic-three family.  Characteristic two is the last uniform case.

In canonical root coordinates the two-move families are obtained from distinct
root directions.  Four unordered direction pairs commute; (0,1) and (0,2) are
noncommuting in odd characteristic, giving eight two-parameter families.  In
characteristic two the commutator correction for (0,2) is -2st=0, so its two
orders coincide.  Thus the exact distance-two shell has 7(q-1)^2 states.

For a,b!=0 normalize

    u=c/(ab),  v=d/(a^2 b).

Exhausting direction patterns of length <=3 in characteristic two gives exactly

    u=0,  u=1,  or  v in {0,1,u,u^2}.

For u not in {0,1}, the four displayed v-values are distinct (u^2=u only for
u=0,1 in a field of characteristic two).  Hence the number of missing
normalized pairs is (q-2)(q-4), and the distance-four shell is
(q-1)^2(q-2)(q-4).  Subtracting from q^4 gives the distance-three shell.
"""
from __future__ import annotations
import json
from collections import Counter,deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5175_ROOT_CAYLEY_METRIC_CHAR2_THEOREM.json'

class GF2m:
    def __init__(self,m,poly): self.m=m;self.q=1<<m;self.poly=poly;self.mask=self.q-1
    def add(self,a,b): return a^b
    def mul(self,a,b):
        z=0
        while b:
            if b&1:z^=a
            b>>=1;a<<=1
            if a&self.q:a^=self.poly
        return z&self.mask
    def inv(self,a):
        assert a
        z=1
        for _ in range(self.q-2):z=self.mul(z,a)
        return z

def mm(A,B,F):
    C=[0]*16
    for i in range(4):
      for j in range(4):
        z=0
        for k in range(4):z=F.add(z,F.mul(A[4*i+k],B[4*k+j]))
        C[4*i+j]=z
    return tuple(C)

def eye():
    z=[0]*16
    for i in range(4):z[4*i+i]=1
    return tuple(z)

def roots(F):
    I=eye(); X=[]
    for entries in (((0,1),(3,2)),((1,3),),((0,3),(1,2)),((0,2),)):
        Z=[0]*16
        for i,j in entries:Z[4*i+j]=1
        X.append(tuple(Z))
    H=[]
    for Z in X:
        R=[]
        for t in range(F.q):
            M=list(I)
            for k,z in enumerate(Z):
                if z:M[k]=F.add(M[k],F.mul(t,z))
            R.append(tuple(M))
        H.append(R)
    return H

def coords(M,F):
    a=M[1];b=M[7];c=M[6];d=F.add(M[2],F.mul(a,c))
    return a,b,c,d

def shells_formula(q):
    s0=1;s1=4*(q-1);s2=7*(q-1)**2
    s4=(q-1)**2*(q-2)*(q-4)
    s3=q**4-s0-s1-s2-s4
    assert s3==4*(q-1)**2*(2*q-3)
    return {0:s0,1:s1,2:s2,3:s3,4:s4}

def bfs_anchor(m,poly):
    F=GF2m(m,poly);q=F.q;H=roots(F);I=eye();gens=[g for R in H for g in R[1:]]
    dist={I:0};Q=deque([I])
    while Q:
        g=Q.popleft()
        for h in gens:
            z=mm(g,h,F)
            if z not in dist:dist[z]=dist[g]+1;Q.append(z)
    C=Counter(dist.values());got={k:C[k] for k in range(max(C)+1)}
    assert got=={k:v for k,v in shells_formula(q).items() if v}
    # Verify the normalized <=3 locus directly.
    reach={u:set() for u in range(q)}
    for M,r in dist.items():
        a,b,c,d=coords(M,F)
        if a and b and r<=3:
            u=F.mul(c,F.inv(F.mul(a,b)))
            v=F.mul(d,F.inv(F.mul(F.mul(a,a),b)))
            reach[u].add(v)
    for u in range(q):
        if u in (0,1): assert len(reach[u])==q
        else: assert reach[u]=={0,1,u,F.mul(u,u)}
    return {'q':q,'vertices':q**4,'shells':{str(k):v for k,v in got.items()},
            'normalized_three_move_locus_verified':True}

def main():
    A={
      '2':bfs_anchor(1,0b11),
      '4':bfs_anchor(2,0b111),
      '8':bfs_anchor(3,0b1011),
    }
    out={
      'pass':5175,
      'status':'THEOREM_ROOT_CAYLEY_METRIC_CHARACTERISTIC_2',
      'field_range':'q=2^f',
      'two_move_collision':'The two orderings of root directions (0,2) coincide because their correction -2st vanishes; hence shell2=7(q-1)^2.',
      'normalized_three_move_locus':'for a,b!=0: u=0 or u=1, or v in {0,1,u,u^2}',
      'distance_four_count':'(q-1)^2(q-2)(q-4)',
      'shell_formula':{
        'd0':'1','d1':'4(q-1)','d2':'7(q-1)^2',
        'd3':'4(q-1)^2(2q-3)','d4':'(q-1)^2(q-2)(q-4)'
      },
      'anchors':A,
      'synthesis':'Together with Pass5143 and Pass5165, the four-root U(q) Cayley word metric is now symbolically classified over every finite field.',
      'boundary':'Exact finite-field/group theorem; no physical timing or hardware claim.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
