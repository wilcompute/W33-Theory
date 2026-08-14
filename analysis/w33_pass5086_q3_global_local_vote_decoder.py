#!/usr/bin/env python3
"""Pass5086: global q=3 decoder built from the Pass5078 eight-entry local ROM.

Each apartment belongs to four opposite-pair charts.  Two distinct apartments
share at most one chart.  Each affected K4 chart emits the minimum local coset
leader; apartments accumulate votes and the sweep flips every coordinate of
maximum positive vote.  The script exhausts all weight-1 and weight-2 errors.
"""
from __future__ import annotations
from collections import Counter
import itertools,json,math
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5086_Q3_GLOBAL_DECODER.json'
PAIRS=list(itertools.combinations(range(4),2));POS={e:i for i,e in enumerate(PAIRS)}
SYNPAIRS=list(itertools.combinations(range(1,4),2))
def syndrome(mask):
    s=0
    for b,(i,j) in enumerate(SYNPAIRS):
        v=((mask>>POS[(0,i)])&1)^((mask>>POS[(0,j)])&1)^((mask>>POS[(i,j)])&1);s|=v<<b
    return s
def leader_table():
    best={}
    for m in range(64):
        s=syndrome(m)
        if s not in best or (m.bit_count(),m)<(best[s].bit_count(),best[s]):best[s]=m
    assert len(best)==8
    return best

def main():
    G=build_W(3);n=len(G['apartments']);assert n==1620;best=leader_table()
    chart_coords=[[loc[p] for p in PAIRS] for _,loc in G['charts']];assert len(chart_coords)==1080
    apt_charts=[[] for _ in range(n)]
    pair_seen=set()
    for ci,coords in enumerate(chart_coords):
        for a in coords:apt_charts[a].append(ci)
        for a,b in itertools.combinations(sorted(coords),2):
            assert (a,b) not in pair_seen;pair_seen.add((a,b))
    assert set(map(len,apt_charts))=={4} and len(pair_seen)==16200
    def decode(err):
        E=set(err);votes=Counter();affected={ci for a in E for ci in apt_charts[a]}
        for ci in affected:
            coords=chart_coords[ci];mask=sum(1<<k for k,a in enumerate(coords) if a in E);lead=best[syndrome(mask)]
            for k,a in enumerate(coords):
                if (lead>>k)&1:votes[a]+=1
        if not votes:return set(),0
        mv=max(votes.values());return {a for a,v in votes.items() if v==mv},mv
    assert all(decode((a,))[0]=={a} for a in range(n))
    bad=0;profiles=Counter()
    for a in range(n):
        ca=set(apt_charts[a])
        for b in range(a+1,n):
            corr,mv=decode((a,b));bad += corr!={a,b};profiles[(len(ca&set(apt_charts[b])),mv)]+=1
    assert bad==0 and sum(profiles.values())==math.comb(n,2)
    out={'pass':5086,'status':'THEOREM_EXHAUSTIVE_RADIUS2','code':[1620,81,81],
         'charts':1080,'charts_per_apartment':4,'apartment_pairs_sharing_a_chart':len(pair_seen),'max_shared_charts_per_pair':1,
         'local_rom_entries':8,'single_errors_tested':n,'double_errors_tested':math.comb(n,2),'double_failures':bad,
         'double_profile_sharedcharts_maxvote':{f'{k[0]},{k[1]}':v for k,v in sorted(profiles.items())},
         'guaranteed_global_error_weight':2,
         'decoder':'minimum local K4 coset leaders -> vote -> flip all maximum-vote coordinates',
         'boundary':'Finite hard-decision apartment-bit decoder only. This is far below unique radius 40 and is not an optical/noise threshold.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
