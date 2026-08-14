#!/usr/bin/env python3
"""Pass5239: exact q=3 weight-eight false-center echo family.

Pass5215 proves a global radius-seven theorem for the provenance-refined decoder
(max vote -> max singleton evidence -> min tie degree).  At weight eight the
true-only first-correction property fails in a completely structured way.

Every apartment z belongs to four charts.  In each incident local K4 syndrome
chart there are exactly two 2-error masks on the other five coordinates whose
unique local leader is z.  Choosing one poison pair independently in all four
charts gives 2^4=16 weight-eight errors.  Exhaustively over all 1620 centers:

  1620*16 = 25920 distinct error sets.

For every one, the provenance stage selects the false center z alone.  However
the full deterministic decoder self-heals in exactly three sweeps:

  E (wt8) -> E union {z} (wt9) -> {z} (wt1) -> empty.

Thus monotone/true-only guaranteed radius is exactly seven, but this family does
not disprove eventual radius eight.  It identifies the first complete
nonmonotone obstruction family that any radius-eight proof must handle.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict,Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5239_Q3_RADIUS8_FALSE_CENTER_ECHO.json'
LEAD=[0,8,16,1,32,2,4,0]

def syn(m):
    return (((m>>0&1)^(m>>1&1)^(m>>3&1)) |
            (((m>>0&1)^(m>>2&1)^(m>>4&1))<<1) |
            (((m>>1&1)^(m>>2&1)^(m>>5&1))<<2))

def main():
    G=build_W(3);pairs=list(itertools.combinations(range(4),2));charts=[[loc[p] for p in pairs] for _,loc in G['charts']]
    n=len(G['apartments']);ach=[[] for _ in range(n)];adj=[set() for _ in range(n)]
    for ci,C in enumerate(charts):
        for p,a in enumerate(C):ach[a].append((ci,p))
        for a,b in itertools.combinations(C,2):adj[a].add(b);adj[b].add(a)
    assert n==1620 and len(charts)==1080 and {len(x) for x in ach}=={4}
    def leader(mask):
        lm=LEAD[syn(mask)];return None if not lm else (lm&-lm).bit_length()-1
    def provenance(E):
        masks={}
        for a in E:
            for ci,p in ach[a]:masks[ci]=masks.get(ci,0)^(1<<p)
        votes=Counter();sing=Counter()
        for ci,m in masks.items():
            p=leader(m)
            if p is None:continue
            a=charts[ci][p];votes[a]+=1
            if m.bit_count()==1 and ((m>>p)&1):sing[a]+=1
        if not votes:return []
        mv=max(votes.values());ms=max(sing[a] for a in votes if votes[a]==mv)
        return sorted(a for a in votes if votes[a]==mv and sing[a]==ms)
    def correction(E):
        F=provenance(E)
        if not F:return []
        deg={x:sum(y in adj[x] for y in F if y!=x) for x in F};d=min(deg.values())
        return sorted(x for x in F if deg[x]==d)
    def decode(E):
        E=set(E);hist=[]
        for _ in range(10):
            if not E:return True,hist
            C=correction(sorted(E));hist.append((len(E),tuple(C)))
            if not C:return False,hist
            E.symmetric_difference_update(C)
        return False,hist
    seen=set();example=None;profiles=Counter()
    for z in range(n):
        opts=[]
        for ci,pz in ach[z]:
            O=[]
            for i,j in itertools.combinations([p for p in range(6) if p!=pz],2):
                if leader((1<<i)|(1<<j))==pz:O.append((charts[ci][i],charts[ci][j]))
            assert len(O)==2;opts.append(O)
        for bits in itertools.product((0,1),repeat=4):
            E=tuple(sorted(x for k,b in enumerate(bits) for x in opts[k][b]))
            assert len(E)==8 and provenance(E)==[z]
            ok,h=decode(E);assert ok and [x[0] for x in h]==[8,9,1]
            seen.add(E);profiles[tuple(x[0] for x in h)]+=1
            if example is None:example={'false_center':z,'errors':list(E),'sweep_weights':[x[0] for x in h],'corrections':[list(x[1]) for x in h]}
    assert len(seen)==25920 and profiles==Counter({(8,9,1):25920})
    out={'pass':5239,'status':'THEOREM_Q3_WEIGHT8_FALSE_CENTER_ECHO_FAMILY_SELF_HEALS',
      'centers':1620,'poison_pairs_per_incident_chart':2,'incident_charts_per_center':4,
      'configurations_per_center':16,'distinct_weight8_configurations':25920,
      'provenance_failure':'For every configuration the max-vote/max-singleton stage returns the false center alone.',
      'full_decoder':'Every configuration clears in exactly three sweeps with residual weights 8 -> 9 -> 1 -> 0.',
      'example':example,
      'consequence':'The true-only/monotone first-correction guarantee is sharp at radius7. Radius8 eventual decoding is not disproved because this complete obstruction family self-heals.',
      'boundary':'No orbit-complete classification of every connected/disconnected weight8 error is claimed; global eventual radius8 remains open.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
