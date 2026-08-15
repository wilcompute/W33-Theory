#!/usr/bin/env python3
"""Pass5381: exact q=3 radius-nine false-vote-4 frontier.

Pass5263 proves eventual radius eight.  At weight nine a false candidate still
has at most four votes, one from each incident chart.  This pass completely
classifies the maximal false-vote sector V=4 by fixing the false center z=0
(apartment transitivity).

In a chart where z is local position 0, the only z-voting masks avoiding z are
  weight 2: {1,2}, {3,4}
  weight 3: {1,4,5}, {2,3,5}.
Thus every weight-nine set giving z four votes is exactly one of:
  (A) 3+2+2+2 errors in the four z-charts: 4*2^4=64 sets;
  (B) one of the 2^4=16 radius-eight poison echoes plus one error outside the
      20 z-neighbors: 16*1599=25584 sets.
No other local occupancy can give four votes at total weight nine.

The script enumerates all 25648 sets and runs the actual deterministic decoder
(max vote -> max singleton provenance -> min tie degree) until clear, cycle, or
12 sweeps.  Because the automorphism group is transitive on apartments, this is
an exact global classification of the V=4 false-center sector.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5381_Q3_RADIUS9_FALSE_VOTE4_CENSUS.json'
PAIRS=list(itertools.combinations(range(4),2))
LEAD=[0,8,16,1,32,2,4,0]

def syn(m):
    return (((m>>0&1)^(m>>1&1)^(m>>3&1)))|((((m>>0&1)^(m>>2&1)^(m>>4&1)))<<1)|((((m>>1&1)^(m>>2&1)^(m>>5&1)))<<2)

def build():
    G=build_W(3);charts=[[loc[p] for p in PAIRS] for _,loc in G['charts']]
    ach=[[] for _ in G['apartments']]
    for ci,C in enumerate(charts):
        for p,a in enumerate(C):ach[a].append((ci,p))
    adj=[set() for _ in G['apartments']]
    for C in charts:
        for a in C:adj[a].update(x for x in C if x!=a)
    assert len(charts)==1080 and {len(x) for x in ach}=={4} and {len(x) for x in adj}=={20}
    return G,charts,ach,adj

def sweep(errs,charts,ach,adj):
    touched={}
    for a in errs:
        for ci,p in ach[a]:touched[ci]=touched.get(ci,0)^(1<<p)
    vote={};sing={}
    for ci,m in touched.items():
        lm=LEAD[syn(m)]
        if not lm:continue
        p=(lm&-lm).bit_length()-1;a=charts[ci][p]
        vote[a]=vote.get(a,0)+1
        if m.bit_count()==1 and ((m>>p)&1):sing[a]=sing.get(a,0)+1
    if not vote:return tuple()
    mv=max(vote.values());M=[a for a,v in vote.items() if v==mv]
    ms=max(sing.get(a,0) for a in M);F=[a for a in M if sing.get(a,0)==ms]
    deg={a:sum(b in adj[a] for b in F if b!=a) for a in F};md=min(deg.values())
    return tuple(sorted(a for a in F if deg[a]==md))

def decode(E,charts,ach,adj,limit=12):
    E=set(E);seen=set();trace=[len(E)]
    for step in range(limit+1):
        if not E:return {'status':'clear','sweeps':step,'trace':trace}
        key=tuple(sorted(E))
        if key in seen:return {'status':'cycle','sweeps':step,'trace':trace,'state':list(key)}
        seen.add(key);corr=sweep(E,charts,ach,adj)
        if not corr:return {'status':'stuck','sweeps':step,'trace':trace,'state':list(key)}
        E.symmetric_difference_update(corr);trace.append(len(E))
    return {'status':'limit','sweeps':limit,'trace':trace,'state':sorted(E)}

def main():
    G,charts,ach,adj=build();z=0;inc=ach[z];assert len(inc)==4 and {p for _,p in inc}=={0}
    others=[charts[ci][1:] for ci,_ in inc]
    N20=set().union(*map(set,others));assert len(N20)==20
    outside=[a for a in range(1620) if a!=z and a not in N20];assert len(outside)==1599
    two=[(1,2),(3,4)];three=[(1,4,5),(2,3,5)]
    cases=[];kind=[]
    # A: exactly one 3-mask and three 2-masks.
    for heavy in range(4):
        for choices in itertools.product(range(2),repeat=4):
            E=set()
            for q in range(4):
                pat=three[choices[q]] if q==heavy else two[choices[q]]
                E.update(others[q][p-1] for p in pat)
            assert len(E)==9;cases.append(frozenset(E));kind.append('local_3+2+2+2')
    assert len(set(cases))==64
    # B: poison echo plus one true outsider.
    base=[]
    for choices in itertools.product(range(2),repeat=4):
        E=set()
        for q in range(4):E.update(others[q][p-1] for p in two[choices[q]])
        assert len(E)==8;base.append(frozenset(E))
    assert len(set(base))==16
    for B in base:
        for u in outside:
            cases.append(B|{u});kind.append('echo_plus_outsider')
    assert len(cases)==64+16*1599==25648 and len(set(cases))==len(cases)

    status=Counter();traces=Counter();maxsw=0;witness=None
    bykind={k:Counter() for k in set(kind)}
    for K,E in zip(kind,cases):
        # z must indeed receive four local votes in the initial state.
        touched=[]
        for ci,_ in inc:
            m=0
            for p,a in enumerate(charts[ci]):
                if a in E:m|=1<<p
            touched.append(m)
        assert sum((LEAD[syn(m)]&1)!=0 for m in touched)==4
        R=decode(E,charts,ach,adj);status[R['status']]+=1;bykind[K][R['status']]+=1
        traces[tuple(R['trace'])]+=1;maxsw=max(maxsw,R['sweeps'])
        if R['status']!='clear' and witness is None:witness={'initial':sorted(E),'kind':K,'result':R}
    out={'pass':5381,'status':'COMPUTATION_Q3_RADIUS9_FALSE_VOTE4_COMPLETE_CENSUS',
      'fixed_false_center':z,'local_3+2+2+2_cases':64,'echo_plus_outsider_cases':16*1599,
      'total_cases':len(cases),'decoder_status_counts':dict(status),
      'status_by_kind':{k:dict(v) for k,v in bykind.items()},'max_sweeps':maxsw,
      'trace_histogram':{'/'.join(map(str,k)):v for k,v in traces.items()},
      'first_nonclear_witness':witness,
      'globality':'Apartment transitivity maps any false center to z=0, so the census is global for the V=4 sector.',
      'boundary':'This pass classifies only false candidates with maximal vote V=4 at weight9. V=1,2,3 sectors must also be closed before claiming guaranteed eventual radius9.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
