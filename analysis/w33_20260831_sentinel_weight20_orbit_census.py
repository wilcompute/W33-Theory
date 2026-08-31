#!/usr/bin/env python3
"""Exact PSp(4,3) orbit census of the 17,376 weight-20 sentinel words.

The [40,15,8]_2 Hermitian/sentinel code has 17,376 words of weight 20.  The
432 W33 two-ovoids are known to lie in this shell.  This audit classifies the
*entire* shell under the native PSp(4,3) action, recording orbit sizes,
stabilizer orders/order spectra, W33-line intersection profiles, sentinel
minimum-support intersection profiles, and complement behaviour.

This is deliberately a full shell census rather than a search seeded at the
known hemisystem: every one of the 2^15 codewords is generated first and only
then filtered by weight.
"""
from __future__ import annotations

import json
from collections import Counter, deque
from pathlib import Path

import w33_20260829_pg34_polarity_sentinel as pg
import w33_20260829_216_clifford_torsor_nogo as base

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_SENTINEL_WEIGHT20_ORBIT_CENSUS.json'
ALL=(1<<40)-1


def mask(bits):
    return sum((x&1)<<i for i,x in enumerate(bits))


def perm_mask(w,p):
    z=0
    while w:
        l=w & -w
        i=l.bit_length()-1
        z |= 1<<p[i]
        w ^= l
    return z


def profile(w, masks):
    return tuple(sorted(Counter((w&m).bit_count() for m in masks).items()))


def main():
    N,A=pg.geometry(); B,_=pg.trade_incidence(N)
    support_masks=[sum((B[i][j]&1)<<i for i in range(40)) for j in range(45)]
    basis=pg.gf2_basis(support_masks); assert len(basis)==15

    shell=set(); enum=Counter()
    for c in range(1<<15):
        w=0
        for i,b in enumerate(basis):
            if (c>>i)&1: w^=b
        enum[w.bit_count()]+=1
        if w.bit_count()==20: shell.add(w)
    assert len(shell)==17376 and enum[20]==17376

    pts,idx,lines,_=base.geometry()
    line_masks=[sum(1<<x for x in L) for L in lines]
    gens=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*base.form(x,v)%3
                y=base.norm(tuple((x[k]+z*v[k])%3 for k in range(4)))
                p.append(idx[y])
            gens.append(tuple(p))
    chosen=(18,62,77,10); gg=[gens[i] for i in chosen]
    G=base.closure(gg,40); assert len(G)==25920
    assert all(perm_mask(w,g) in shell for w in list(shell)[:100] for g in gg)

    rem=set(shell); orbits=[]
    while rem:
        seed=min(rem); O={seed}; q=deque([seed])
        while q:
            w=q.popleft()
            for g in gg:
                u=perm_mask(w,g)
                assert u in shell
                if u not in O: O.add(u); q.append(u)
        rem-=O; orbits.append(O)
    orbits.sort(key=lambda O:(-len(O),min(O)))
    assert sum(map(len,orbits))==17376

    rows=[]; hemi=[]
    for oi,O in enumerate(orbits):
        r=min(O)
        lp=profile(r,line_masks)
        sp=profile(r,support_masks)
        stab=[g for g in G if perm_mask(r,g)==r]
        assert len(stab)*len(O)==25920
        oh=dict(sorted(Counter(base.porder(g) for g in stab).items()))
        comp=ALL^r
        comp_orbit=next(j for j,Q in enumerate(orbits) if comp in Q)
        is_hemi=(lp==((2,40),))
        if is_hemi: hemi.append(oi)
        rows.append({
          'orbitIndex':oi,'size':len(O),'stabilizerOrder':len(stab),
          'stabilizerElementOrderHistogram':oh,
          'representative':sorted(i for i in range(40) if (r>>i)&1),
          'lineIntersectionProfile':{str(k):v for k,v in lp},
          'sentinelSupportIntersectionProfile':{str(k):v for k,v in sp},
          'complementOrbitIndex':comp_orbit,'complementClosed':comp in O,
          'isTwoOvoid':is_hemi,
        })

    assert len(hemi)==1
    h=rows[hemi[0]]
    assert h['size']==432 and h['lineIntersectionProfile']=={'2':40}
    orbit_sizes=Counter(r['size'] for r in rows)
    stabilizers=Counter(r['stabilizerOrder'] for r in rows)

    out={
      'schema':'w33.20260831.sentinel-weight20-orbit-census.v1','status':'PASS',
      'code':{'parameters':'[40,15,8]_2','weight20Words':17376},
      'ambientGroup':{'name':'PSp(4,3)','order':25920,'orbitCount':len(rows)},
      'orbitSizeHistogram':dict(sorted(orbit_sizes.items())),
      'stabilizerOrderHistogram':dict(sorted(stabilizers.items())),
      'twoOvoidOrbitIndex':hemi[0],
      'twoOvoidOrbit':h,
      'orbits':rows,
      'theorem':'The complete 17,376-word weight-20 sentinel shell splits into the PSp(4,3) orbits recorded here. Exactly one orbit has constant W33 line intersection 2; it has size 432 and is precisely the oriented two-ovoid/hemisystem orbit.',
      'boundary':'Exact binary-code and finite-group census. Orbit/stabilizer coincidences with unrelated project counts are not identifications without an equivariant map.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','orbits':len(rows),'sizes':[r['size'] for r in rows],
      'stabilizers':[r['stabilizerOrder'] for r in rows],'twoOvoidOrbit':hemi[0]},sort_keys=True))

if __name__=='__main__': main()
