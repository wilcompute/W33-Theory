#!/usr/bin/env python3
"""Pass5161: close q=5 leader 22 by a local degree-type DP plus cubic intersections.

Pass5158 raises the strict q=5 counterexample barrier to leader >=22.  For an
m=22 selected Levi graph, deleting any edge leaves m=21, whose adjacent-pair
count is at most 33 by Pass5148.  Averaging gives W<=36; W=36 would force every
edge endpoint-degree sum >=5, but the degree equations are then inconsistent,
so W<=35.

The cubic parity minorant already closes W<=33.  For W=34,35 this producer uses
a tiny exact integer DP over local degree-neighbor types.  Its objective is the
number P4 of selected four-edge Levi paths, counted by center.  Every such path
injects two (1,2,3) chamber triples, worth q=5 apartments each by Pass5140.
The DP is a relaxation: it enforces only vertex counts, deletion endpoint-degree
constraints, and symmetric stub counts.  Therefore its minima are rigorous lower
bounds for every actual simple girth-eight selected Levi graph.
"""
from __future__ import annotations
import json, math
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import optimize

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5161_Q5_CUBIC_LEADER23_LOCALTYPE_DP.json'


def local_patterns(d,minsum):
    out=[]
    for a in range(d+1):
      for b in range(d-a+1):
        c=d-a-b
        if a and d+1<minsum:continue
        if b and d+2<minsum:continue
        if c and d+3<minsum:continue
        f=[0]*a+[1]*b+[2]*c
        cost=sum(f[i]*f[j] for i in range(len(f)) for j in range(i+1,len(f)))
        out.append(((a,b,c),cost))
    return out


def class_dp(d,n,minsum):
    dp={(0,0,0):0}
    for _ in range(n):
        nd={}
        for st,cost in dp.items():
          for p,pc in local_patterns(d,minsum):
            ns=(st[0]+p[0],st[1]+p[1],st[2]+p[2]);nc=cost+pc
            if nc<nd.get(ns,10**9):nd[ns]=nc
        dp=nd
    return dp


def p4_relaxed(n1,n2,n3,minsum):
    D={1:class_dp(1,n1,minsum),2:class_dp(2,n2,minsum),3:class_dp(3,n3,minsum)}
    best=None;arg=None
    for s1,c1 in D[1].items():
      for s2,c2 in D[2].items():
        if s1[1]!=s2[0]:continue
        for s3,c3 in D[3].items():
          if s1[2]!=s3[0] or s2[2]!=s3[1]:continue
          if s1[0]%2 or s2[1]%2 or s3[2]%2:continue
          c=c1+c2+c3
          if best is None or c<best:best,arg=c,(s1,s2,s3)
    assert best is not None
    return best,arg


def profiles(m,W):
    out=[]
    for n3 in range(m+1):
        n2=W-3*n3
        n1=2*m-W-n2
        if min(n1,n2)>=0 and n1+2*n2+3*n3==2*m:out.append((n1,n2,n3))
    return out


def centered_wedge_floor(m,e):
    a,r=divmod(2*e,m)
    return (m-r)*math.comb(a,2)+r*math.comb(a+1,2)


def ceil_frac(x):return (x.numerator+x.denominator-1)//x.denominator


def main():
    m=22
    # W=36 would imply deletion decrement >=3 on every edge, hence endpoint
    # degree sum >=5 and therefore n1=0.  The two degree equations then give
    # n2=8 and 3*n3=28, impossible.
    assert (28%3)!=0
    cap=35
    pair={}
    for W in range(30,cap+1):
        ov,dist,feas,lb=optimize(m,W)
        pair[str(W)]={'distance_counts':list(dist),'pair_weight_lower_bound':lb}
    assert [pair[str(W)]['pair_weight_lower_bound'] for W in range(30,36)]==[872,568,264,-40,-344,-648]

    branches={'N1<=30':{'integer_weight_lower_bound':872}}
    # Cubic-only sectors.
    for W in (31,32,33):
        n112=centered_wedge_floor(m,W)-3*(W//3)
        mass=25*n112
        b=Fraction(pair[str(W)]['pair_weight_lower_bound'],1)+Fraction(6,7)*mass
        branches[f'N1={W}']={'N112_lower':n112,'triple_mass_lower':mass,
          'P4_lower_used':0,'integer_weight_lower_bound':ceil_frac(b)}
    assert [branches[f'N1={W}']['integer_weight_lower_bound'] for W in (31,32,33)]==[1168,950,668]

    dp_cert={}
    for W in (34,35):
        ps=profiles(m,W);rows=[]
        minsum=W-31 # W - previous_cap(33) + 2
        for p in ps:
            val,st=p4_relaxed(*p,minsum)
            rows.append({'degree_counts':{'n1':p[0],'n2':p[1],'n3':p[2]},
                         'endpoint_degree_sum_min':minsum,
                         'P4_relaxed_lower':val,
                         'balanced_stub_totals':{'deg1':list(st[0]),'deg2':list(st[1]),'deg3':list(st[2])}})
        p4=min(r['P4_relaxed_lower'] for r in rows)
        n112=centered_wedge_floor(m,W)-3*(W//3)
        n123=2*p4
        mass=25*n112+5*n123
        b=Fraction(pair[str(W)]['pair_weight_lower_bound'],1)+Fraction(6,7)*mass
        branches[f'N1={W}']={'N112_lower':n112,'P4_lower':p4,'N123_lower':n123,
          'triple_mass_lower':mass,'integer_weight_lower_bound':ceil_frac(b)}
        dp_cert[str(W)]={'profiles':rows,'uniform_P4_lower':p4}
    assert dp_cert['34']['uniform_P4_lower']==56
    assert dp_cert['35']['uniform_P4_lower']==68
    assert branches['N1=34']['integer_weight_lower_bound']==972
    assert branches['N1=35']['integer_weight_lower_bound']==900

    out={'pass':5161,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_23',
      'q':5,'leader_size_closed':22,'target_distance':625,
      'adjacent_pair_cap':35,'pair_relaxations':pair,'local_type_dp':dp_cert,'branches':branches,
      'path_injection':'A selected four-edge Levi path gives two distinct (1,2,3) chamber triples. Girth eight gives uniqueness, so N123>=2 P4.',
      'conclusion':'Every leader-22 sector has apartment weight at least 668; the sharp high-adjacency sectors are much stronger (972 and 900). Thus every q5 apartment-code word of weight <625 has minimum chamber leader at least 23.',
      'boundary':'This closes leader 22 only. The q5/all-q distance theorem remains open for leaders >=23 and the weight-625 equality shell remains unclassified.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
