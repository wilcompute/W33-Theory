#!/usr/bin/env python3
"""Pass 4577 -- the 12-fold apartment fibers reconstruct O+(8,2) polarity internally.

Pass4558 proved that the 1620 W33 apartments map 12-to-1 onto the 135 nonzero
singular classes of the protected V8=O+(8,2), with each individual fiber carrying
K_{4,4,4} intersection geometry.

This pass studies *between* fibers. For two distinct 12-apartment fibers F_x,F_y,
let n2(x,y) be the number of ordered cross pairs (A,B) in F_x x F_y whose four-line
apartment supports share exactly two W33 lines. Exact exhaustion of all C(135,2)
fiber pairs gives

  B(x,y)=1  <=>  n2(x,y)=12,
  B(x,y)=0  <=>  n2(x,y) in {0,2,6,48}.

Thus the apartment quotient does not merely label the 135 singular points: its own
cross-fiber intersection statistics recover their polar relation. Declaring two
fibers adjacent when n2 != 12 reconstructs SRG(135,70,37,35), the nonzero singular
orthogonality graph of O+(8,2), without supplying external eight-dimensional
coordinates.
"""
from __future__ import annotations

import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np

from w33_pass4495_4502_distance_prism_reconstruction import geometry

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4577_APARTMENT_FIBER_O8PLUS_POLARITY.json'


def q8(mask):
    w=int(mask).bit_count();assert w%4==0;return (w//4)&1


def srg_params(adj):
    n=len(adj);deg={len(x) for x in adj};aa=set();nn=set()
    for i,j in itertools.combinations(range(n),2):
        c=len(adj[i]&adj[j]);(aa if j in adj[i] else nn).add(c)
    assert len(deg)==len(aa)==len(nn)==1
    return [n,next(iter(deg)),next(iter(aa)),next(iter(nn))]


def main()->int:
    pts,pidx,lines,A,apartments,apmasks,H=geometry();assert len(apartments)==1620
    fibers=defaultdict(list)
    for ai,ap in enumerate(apartments):
        b=np.zeros(40,dtype=np.uint8);b[list(ap)]=1;y=(A@b)%2
        ym=sum(int(z)<<i for i,z in enumerate(y));assert ym.bit_count()==16
        fibers[ym].append(ai)
    assert len(fibers)==135 and set(map(len,fibers.values()))=={12}
    keys=sorted(fibers);adj=[set() for _ in keys];n2_by_polar={0:Counter(),1:Counter()}
    for i,j in itertools.combinations(range(135),2):
        x,y=keys[i],keys[j];pol=q8(x^y) # q(x)=q(y)=0, so this is B(x,y)
        n2=sum(1 for a in fibers[x] for b in fibers[y] if (apmasks[a]&apmasks[b]).bit_count()==2)
        n2_by_polar[pol][n2]+=1
        assert (n2==12)==bool(pol)
        if n2!=12:adj[i].add(j);adj[j].add(i)
    assert n2_by_polar[1]==Counter({12:4320})
    assert n2_by_polar[0]==Counter({6:2160,0:1620,2:810,48:135})
    params=srg_params(adj);assert params==[135,70,37,35]
    out={
      'pass':4577,'apartments':1620,'fibers':135,'fiber_size':12,
      'cross_statistic':'n2(x,y)=number of cross-fiber apartment pairs sharing exactly two W33 lines',
      'polar_reconstruction':{'nonorthogonal_B1':'n2=12 exactly','orthogonal_B0':'n2 in {0,2,6,48}',
                              'B1_pair_count':4320,'B0_pair_count':4725},
      'orthogonal_pair_n2_distribution':{'0':1620,'2':810,'6':2160,'48':135},
      'reconstructed_singular_polar_graph_srg':params,
      'theorem':'The 12-fold apartment quotient plus cross-fiber line-intersection counts reconstructs the 135-point O+(8,2) singular polar graph intrinsically.',
      'boundary':'Finite quotient/association geometry. Cross-fiber intersection multiplicities are not physical couplings or transition rates.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
