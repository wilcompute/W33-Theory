#!/usr/bin/env python3
"""Auxiliary exact certificate for Pass5430 V=3 direction counting.

For every local false-center V=3 core of weight 6..10, and every coordinate
outside the false center's 20 chart-neighbors, one outsider can add new spoiled
chart directions to at most two local core errors.  Combined with the exact core
deficit counts, this rules out all local weights >=7 at total weight10.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5430_Q3_V3_DIRECTION_CAP.json'
PAIRS=list(itertools.combinations(range(4),2));LEAD=[0,8,16,1,32,2,4,0]

def syn(m):
    return (((m>>0&1)^(m>>1&1)^(m>>3&1)))|((((m>>0&1)^(m>>2&1)^(m>>4&1)))<<1)|((((m>>1&1)^(m>>2&1)^(m>>5&1)))<<2)

def main():
    G=build_W(3);charts=[[loc[p] for p in PAIRS] for _,loc in G['charts']]
    ach=[[] for _ in G['apartments']];adj=[set() for _ in G['apartments']]
    for ci,C in enumerate(charts):
        for p,a in enumerate(C):ach[a].append((ci,p))
        for a in C:adj[a].update(x for x in C if x!=a)
    z=0;inc=ach[z];assert {p for _,p in inc}=={0};others=[charts[ci][1:] for ci,_ in inc]
    N20=set().union(*map(set,others));outside=set(range(1620))-{z}-N20
    ndir=[]
    for a in range(1620):
        d={}
        for bit,(ci,p) in enumerate(ach[a]):
            for u in charts[ci]:
                if u!=a:d[u]=bit
        ndir.append(d)
    def mask_to(a,S):
        m=0
        for u in S:
            b=ndir[a].get(u)
            if b is not None:m|=1<<b
        return m
    def vote0(mask5):
        m=sum(((mask5>>(p-1))&1)<<p for p in range(1,6));return (LEAD[syn(m)]&1)!=0
    local=defaultdict(list)
    for ms in itertools.product(range(32),repeat=4):
        w=sum(x.bit_count() for x in ms)
        if w>10 or sum(vote0(x) for x in ms)!=3:continue
        E=set()
        for q,x in enumerate(ms):
            for j,a in enumerate(others[q]):
                if (x>>j)&1:E.add(a)
        local[w].append(frozenset(E))
    assert [len(local[w]) for w in (6,7,8,9,10)]==[32,256,832,1536,1856]
    cap_by_weight={};deficits={}
    for w in (6,7,8,9,10):
        cap=0;dh=Counter()
        for core in local[w]:
            L=set(core);base={a:mask_to(a,L-{a}) for a in L}
            dh[sum(max(0,2-base[a].bit_count()) for a in L)]+=1
            cand=set().union(*(adj[a]&outside for a in L))
            for u in cand:
                c=0
                for a in L:
                    b=ndir[a].get(u)
                    if b is not None and not ((base[a]>>b)&1):c+=1
                cap=max(cap,c)
        cap_by_weight[w]=cap;deficits[w]=dict(sorted(dh.items()))
    assert cap_by_weight=={6:2,7:2,8:2,9:2,10:2}
    assert min(deficits[7])>2*3 and min(deficits[8])>2*2 and min(deficits[9])>2 and min(deficits[10])>0
    out={'pass':5430,'status':'THEOREM_Q3_V3_OUTSIDER_NEW_DIRECTION_CAP_TWO',
      'local_counts':{str(w):len(local[w]) for w in (6,7,8,9,10)},
      'new_direction_cap_by_local_weight':{str(k):v for k,v in cap_by_weight.items()},
      'direction_deficit_histograms':{str(w):{str(k):v for k,v in deficits[w].items()} for w in deficits},
      'consequence':'At total weight10, local V3 weights7..10 cannot reach spoiled>=2; only local weight6 plus four outsiders needs completion enumeration.',
      'boundary':'Auxiliary finite q3 certificate used by Pass5430; no all-q decoder claim.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
