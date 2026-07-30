#!/usr/bin/env python3
"""Pass 1353: finite-geometric derivation of the 120-selector orbit.

The smallest length-four orbit consists of Hamiltonian cycles on the four
points of a totally isotropic projective line of W(3,3). Each line has three
unoriented cyclic orders, equivalently three choices of opposite-point perfect
matching, so the orbit is 40 x 3 = 120.
"""
from __future__ import annotations
from itertools import combinations
from pathlib import Path
import json, hashlib, sys

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; OUT=DATA/'w33_pass1353_selector_geometry.json'
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass1330_1334_modular_triality_cycle_atlas as old

def canon_cycle(c):
    c=list(c); rots=[tuple(c[i:]+c[:i]) for i in range(len(c))]
    r=list(reversed(c)); rots += [tuple(r[i:]+r[:i]) for i in range(len(r))]
    return min(rots)

def span_line(x,y):
    pts=set()
    for a in range(3):
        for b in range(3):
            if a or b: pts.add(old.canon(tuple((a*x[i]+b*y[i])%3 for i in range(4))))
    assert len(pts)==4
    return tuple(sorted(pts))

def main(write=True):
    points,gens=old.point_model(); point_index={p:i for i,p in enumerate(points)}
    lines=set()
    for i,x in enumerate(points):
        for j in range(i+1,len(points)):
            y=points[j]
            if old.symp(x,y)==0:
                line=span_line(x,y)
                assert all(old.symp(a,b)==0 for a,b in combinations(line,2))
                lines.add(line)
    lines=sorted(lines); assert len(lines)==40
    cycles=[]
    for line in lines:
        a,b,c,d=[point_index[p] for p in line]
        candidates={canon_cycle((a,b,c,d)),canon_cycle((a,b,d,c)),canon_cycle((a,c,b,d))}
        assert len(candidates)==3
        cycles.extend(sorted(candidates))
    assert len(cycles)==120 and len(set(cycles))==120
    G=old.group(gens); assert len(G)==51840
    line0=lines[0]; line0_idx={p:i for i,p in enumerate(line0)}; line0_set={point_index[p] for p in line0}
    line_stab=[]; induced=set()
    for g in G:
        if {g[i] for i in line0_set}==line0_set:
            line_stab.append(g)
            induced.add(tuple(line0_idx[points[g[point_index[p]]]] for p in line0))
    assert len(line_stab)==1296 and len(induced)==24
    kernel_order=len(line_stab)//len(induced); assert kernel_order==54
    cyc0=cycles[0]; cyc0canon=canon_cycle(cyc0); cycle_stab=[]; induced_cycle=set()
    for g in line_stab:
        if canon_cycle(tuple(g[i] for i in cyc0))==cyc0canon:
            cycle_stab.append(g)
            induced_cycle.add(tuple(line0_idx[points[g[point_index[p]]]] for p in line0))
    assert len(cycle_stab)==432 and len(induced_cycle)==8
    orbit={canon_cycle(tuple(g[i] for i in cyc0)) for g in G}
    assert len(orbit)==120 and orbit==set(cycles)
    result={'schema':'w33.pass1353.selector_geometry.v1','status':'PASS','group':'W(E6)=U4(2).2','group_order':51840,
      'polar_space':'W(3,3)','point_count':40,'isotropic_line_count':40,'points_per_line':4,
      'selector_object':'totally isotropic line plus an unoriented cyclic order; equivalently a perfect matching of opposite points',
      'cyclic_orders_per_line':3,'selector_count':120,'line_stabilizer_order':1296,'line_induced_group':'S4',
      'line_induced_group_order':24,'line_pointwise_kernel_order':54,'cycle_induced_stabilizer':'D8',
      'cycle_induced_stabilizer_order':8,'cycle_stabilizer_order':432,'cycle_orbit_size':120,
      'factorizations':{'120':'40 isotropic lines x 3 perfect matchings','432':'54 pointwise-line kernel x 8 dihedral stabilizer','1296':'54 pointwise-line kernel x 24 full S4 action','51840':'40 x 1296 = 120 x 432'},
      'representative_line_point_indices':sorted(line0_set),'representative_cycle':list(cyc0),
      'checks':{'all_lines_isotropic':True,'three_cycles_per_line':True,'group_transitive_on_cycles':True,'induced_line_action_is_S4':True,'cycle_stabilizer_is_D8_preimage':True}}
    raw=json.dumps(result,sort_keys=True,separators=(',',':')).encode(); result['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    if write: OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    return result
if __name__=='__main__':
    r=main(); print(json.dumps({'status':r['status'],'selector_count':r['selector_count'],'cycle_stabilizer_order':r['cycle_stabilizer_order'],'factorization':r['factorizations']['120']},indent=2))
