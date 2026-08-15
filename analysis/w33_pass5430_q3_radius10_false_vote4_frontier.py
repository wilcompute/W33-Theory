#!/usr/bin/env python3
"""Pass5430: exact rooted V=4 reduction for the q=3 weight-ten decoder frontier.

Pass5381 closes eventual radius nine.  Fix a false candidate z.  Its four
incident charts are pairwise disjoint outside z.  The only noncenter local masks
that vote for z are two weight-2 poison masks and two weight-3 poison masks.
Therefore a weight-ten error in the V=4 false-center sector has exactly one of:

  (2,2,2,2) locally + 2 outsiders,
  (3,2,2,2) locally + 1 outsider,
  (3,3,2,2) locally + 0 outsiders.

There are 1599 apartments outside the 20 local z-neighbors, hence the complete
raw rooted census is

  16*C(1599,2) + 64*1599 + 96 = 20,544,048.

A further necessary provenance condition is exact: every outsider must share at
least one chart with another true error. Otherwise it has four singleton incident
charts, obtains vote 4 with positive singleton provenance, and eliminates the
false center at the max-singleton stage.  This gives the correct finite target for
a radius-ten closure/falsifier search.  The pass does NOT claim radius ten.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5430_Q3_RADIUS10_FALSE_VOTE4_FRONTIER.json'
PAIRS=list(itertools.combinations(range(4),2));LEAD=[0,8,16,1,32,2,4,0]

def syn(m):
    return (((m>>0&1)^(m>>1&1)^(m>>3&1)))|((((m>>0&1)^(m>>2&1)^(m>>4&1)))<<1)|((((m>>1&1)^(m>>2&1)^(m>>5&1)))<<2)

def vote0(mask5):
    m=sum(((mask5>>(p-1))&1)<<p for p in range(1,6))
    return (LEAD[syn(m)]&1)!=0

def main():
    G=build_W(3);charts=[[loc[p] for p in PAIRS] for _,loc in G['charts']]
    ach=[[] for _ in G['apartments']]
    for ci,C in enumerate(charts):
        for p,a in enumerate(C):ach[a].append((ci,p))
    z=0;inc=ach[z];assert len(inc)==4 and {p for _,p in inc}=={0}
    others=[charts[ci][1:] for ci,_ in inc]
    N20=set().union(*map(set,others));assert len(N20)==20
    outside=[a for a in range(1620) if a!=z and a not in N20];assert len(outside)==1599

    voting=[]
    for mask in range(32):
        if vote0(mask):voting.append((mask,mask.bit_count()))
    bywt={w:[m for m,ww in voting if ww==w] for w in range(6)}
    assert len(bywt[2])==2 and len(bywt[3])==2 and sum(map(len,bywt.values()))==4

    local8=2**4
    local9=4*2**4
    local10=math.comb(4,2)*2**4
    raw_8_2=local8*math.comb(1599,2)
    raw_9_1=local9*1599
    raw_10_0=local10
    total=raw_8_2+raw_9_1+raw_10_0
    assert (raw_8_2,raw_9_1,raw_10_0,total)==(20441616,102336,96,20544048)

    out={
      'pass':5430,'status':'THEOREM_Q3_RADIUS10_V4_ROOTED_FRONTIER_REDUCTION_NOT_RADIUS_CLOSURE',
      'prior':'Pass5381 proves global eventual radius9; radius10 was open.',
      'false_center_incident_charts':4,
      'noncenter_z_voting_masks':{'weight2':2,'weight3':2,'total':4},
      'outside_coordinates':1599,
      'weight10_V4_shapes':{
        '2+2+2+2 plus two outsiders':raw_8_2,
        '3+2+2+2 plus one outsider':raw_9_1,
        '3+3+2+2 plus no outsiders':raw_10_0},
      'complete_raw_rooted_V4_count':total,
      'necessary_outsider_prune':'Every outsider in a surviving false-center configuration must share a chart with another true error; an isolated outsider has four singleton votes for itself and defeats the false center at max-singleton provenance.',
      'next_exact_target':'Apply the no-isolated-outsider prune, then run the actual deterministic decoder on the remaining rooted V4 candidates; V=1,2,3 require their own weight10 stopping/MILP completion checks.',
      'boundary':'This is an exact finite reduction of the hardest V=4 sector. It does not claim global eventual radius10 and does not rule out V=1,2,3 counterexamples.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
