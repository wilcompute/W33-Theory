#!/usr/bin/env python3
"""Pass 4604 -- no nonzero unary PSp(4,3)-equivariant map V8 <-> U6 exists at all.

Pass4576 ruled out Boolean polynomial maps through degree two and queued degree
three. The stronger orbit argument removes degree entirely.

Protected V8 has G-orbits {0}, 135 nonzero singular, 120 anisotropic. Natural
U6=O^-(6,2) has G-orbits {0}, 27 nonzero singular, 36 anisotropic.
An equivariant map sends a transitive orbit either to zero or onto a transitive
orbit with constant fiber size. Thus the 120 orbit cannot map to 27 or 36.
The only arithmetically possible V8->U6 nonzero case is 135->27, fiber size 5.
This would be a G-invariant block system of size five on the 135 singular orbit.

We reconstruct the actual PSp action from W33 transvections and the 135 protected
apartment-fiber images. A singular-point stabilizer has order 192 and suborbit
sizes 1,1,1,12,12,12,32,32,32. Any block containing the base point is a union of
stabilizer suborbits; no such union has size five. Hence 135->27 is impossible.
The reverse U6->V8 direction is immediate because source nonzero orbit sizes
27/36 are smaller than target nonzero orbit sizes 120/135.

Therefore every unary equivariant SET MAP in either direction is zero, so in
particular every unary Boolean polynomial map of every degree is zero. Pass4583's
exterior-square bridge is not contradicted: it takes two independent V8 inputs.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict,deque
from pathlib import Path
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4511_4514_dual_even_prism_ihara import build_groups,perm_mask
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4604_NO_UNARY_EQUIVARIANT_MAP_ANY_DEGREE.json'

def main():
    pts,pidx,lines,A,apartments,apmasks,H=geometry();selected,G,outer,PG=build_groups(pts,pidx,lines);assert len(G)==25920
    fib=defaultdict(list)
    for ai,ap in enumerate(apartments):
        b=np.zeros(40,dtype=np.uint8);b[list(ap)]=1;y=(A@b)%2
        m=sum(int(z)<<i for i,z in enumerate(y));fib[m].append(ai)
    keys=sorted(fib);assert len(keys)==135 and set(map(len,fib.values()))=={12}
    base=keys[0];stab=[g for g in G if perm_mask(base,g)==base];assert len(stab)==192
    unseen=set(keys);subs=[]
    while unseen:
        x=next(iter(unseen));o={perm_mask(x,g) for g in stab};subs.append(o);unseen-=o
    sizes=sorted(map(len,subs));assert sizes==[1,1,1,12,12,12,32,32,32]
    # A block containing base must be a union of H-orbits. No subset of subdegrees sums to 5.
    poss={0}
    for s in sizes:
        poss|={x+s for x in list(poss)}
    assert 5 not in poss
    out={'pass':4604,'group':'PSp(4,3)','group_order':25920,'protected_V8_orbits':[1,135,120],'cubic_U6_orbits':[1,27,36],'singular135_stabilizer_order':192,'singular135_stabilizer_suborbits':sizes,'block_size5_possible':False,'theorem':'Every unary PSp(4,3)-equivariant set map V8->U6 and U6->V8 is zero; hence there is no nonzero unary Boolean polynomial map at any degree.','proof_summary':['120 cannot map transitively to 27 or36 because fiber sizes are nonintegral','135->36 is nonintegral; 135->27 would require a block of size5','actual 135-point stabilizer suborbits admit no block-size5 union','27/36 cannot map nontrivially onto the larger 120/135 V8 orbits'],'compatibility':'Pass4583 v,w -> v wedge w -> U6 survives because it is a two-input map through a larger module, not a unary map.','boundary':'Finite G-set obstruction. It says nothing about symmetry-breaking maps or maps with auxiliary state/input.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
