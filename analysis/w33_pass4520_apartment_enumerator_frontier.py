#!/usr/bin/env python3
"""Pass 4520 -- exact enumerator frontier after the 10,789,604-orbit reduction.

The complete numerical [1620,39,162] weight enumerator remains OPEN.  This pass
extends the exact coefficient-support census to m=6 and m=7 and computes the
PGSp(4,3) subset-orbit schedule by support size.  The result is intended as a
resumable exact-work packet, not as a substitute for the missing full table.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path

from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4511_4514_dual_even_prism_ihara import build_groups

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4520_APARTMENT_ENUMERATOR_FRONTIER.json'


def cycle_lengths(p):
    seen=[False]*len(p);out=[]
    for i in range(len(p)):
        if not seen[i]:
            j=i;n=0
            while not seen[j]:seen[j]=True;n+=1;j=p[j]
            out.append(n)
    return tuple(sorted(out))


def fixed_subset_poly(cycles,n=40):
    a=[0]*(n+1);a[0]=1
    for d in cycles:
        for k in range(n-d,-1,-1):
            if a[k]:a[k+d]+=a[k]
    return a


def support_census(row_masks,m):
    c=Counter()
    for S in itertools.combinations(range(40),m):
        x=0
        for i in S:x^=row_masks[i]
        c[x.bit_count()]+=1
    return dict(sorted(c.items()))


def main()->int:
    pts,pidx,lines,A,apartments,apmasks,H=geometry()
    rows=[]
    for i in range(40):
        x=0
        for j,b in enumerate(H[i]):
            if b:x|=1<<j
        rows.append(x)
    c6=support_census(rows,6);c7=support_census(rows,7)
    assert sum(c6.values())==3838380 and min(c6)==486 and c6[486]==1440
    assert sum(c7.values())==18643560 and min(c7)==486 and c7[486]==240

    selected,psp,outer,pgsp=build_groups(pts,pidx,lines)
    ct=Counter(cycle_lengths(p) for p in pgsp);assert len(ct)==25 and sum(ct.values())==51840
    fixed=[0]*41
    for typ,n in ct.items():
        a=fixed_subset_poly(typ)
        for m,v in enumerate(a):fixed[m]+=n*v
    subset_orbits=[x//51840 for x in fixed]
    assert sum(subset_orbits)==21578952
    support_le20=subset_orbits[:21]
    assert support_le20==[1,1,2,5,16,48,165,571,1961,6252,18226,47911,113314,240735,460273,793280,1234880,1739041,2218732,2566830,2694464]
    codeword_orbits_total=10789604
    m20_complement_orbits=codeword_orbits_total-sum(subset_orbits[:20])
    assert m20_complement_orbits==1347360

    out={
      'pass':4520,
      'status':'OPEN_FULL_ENUMERATOR',
      'code':{'length':1620,'dimension':39,'codewords':2**39,'minimum_distance':162},
      'exact_support_6':{str(k):v for k,v in c6.items()},
      'exact_support_7':{str(k):v for k,v in c7.items()},
      'support_orbits_under_PGSp_m0_to20':support_le20,
      'support20_orbits_after_complement':m20_complement_orbits,
      'total_codeword_orbits_mod_PGSp_and_complement':codeword_orbits_total,
      'new_low_support_fact':'weight 486 first appears at support 6 (1440 subsets) and also at support 7 (240 subsets)',
      'remaining_exact_task':'accumulate weight on every symmetry/complement orbit through support 20 and sum orbit sizes by weight',
      'boundary':'The complete numerical weight enumerator and Fisher-zero table are NOT claimed closed.'}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__': raise SystemExit(main())
