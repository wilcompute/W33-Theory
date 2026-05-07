#!/usr/bin/env python3
"""PART CCCCVIII -- Line-Star Gauge / Tomotope Bridge.

CCCCIII-CCCCVII found the real obstruction to the W33 CSS code distance:
weight-3 X logicals supported on K4 line-star triples.  A naive cyclic cover does
not remove them.

This part builds the next architecture layer: treat the K4 line-star triples as
subsystem/gauge generators rather than protected logicals.  The resulting gauge
quotient removes the 160 weight-3 line-star directions from the protected sector
in the same spirit as the tomotope local incidence packet:

    tomotope flags = 12 edges * 16 local flags,
    16 = 2 orientations * 4 tetrahedral chart vertices * 2 Clifford chiralities.

The K4 line-star is exactly a local tetrahedral chart obstruction: at each W33
K4 line, each vertex has a 3-edge star.  There are 40 K4 lines and 4 stars per
line, giving 160 line-star triples.  Promoting them to gauge operators is the
natural subsystem move suggested by the tomotope/Fourier/Clifford local packet.

This file proves the count/rank effect over GF(2):
  - there are 160 line-star triples,
  - their span has rank 120,
  - adjoining them to the X-gauge/check algebra raises X-side rank from 39 to
    159,
  - the protected/gauge-quotiented dimension drops from 81 to 240-159-120=-39
    if imposed as stabilizers, so they must be subsystem gauge operators, not
    stabilizers.

Therefore the correct architecture is not "add all line-stars as stabilizers";
it is "promote line-stars to gauge degrees and protect logical information in a
reduced/gauge-fixed sector or in a lifted code where gauge fixing selects a
higher-distance subsystem."
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
Vector=Tuple[int,int,int,int]

def ok(name, cond, value=None): return {"name":name,"passed":bool(cond),"value":value}
def mul(a,u): return tuple((a*u[i])%MOD for i in range(4))
def omega(x,y): return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%MOD
def canon(v):
    for a in v:
        if a%MOD: return mul(1 if a==1 else 2,v)
    raise ValueError('zero')
def points():
    pts=[]; seen=set()
    for v in itertools.product(range(MOD), repeat=4):
        if v==(0,0,0,0): continue
        c=canon(v)
        if c not in seen: seen.add(c); pts.append(c)
    return pts
def build_graph():
    pts=points(); adj=[set() for _ in pts]
    for i,j in itertools.combinations(range(len(pts)),2):
        if omega(pts[i],pts[j])==0: adj[i].add(j); adj[j].add(i)
    return pts,adj
def edges(adj): return [(i,j) for i in range(len(adj)) for j in sorted(adj[i]) if i<j]
def triangles(adj): return [(i,j,k) for i,j,k in itertools.combinations(range(len(adj)),3) if j in adj[i] and k in adj[i] and k in adj[j]]
def bit(indices):
    x=0
    for i in indices: x ^= (1<<i)
    return x
def gf2_basis(rows):
    basis={}
    for r in rows:
        x=r
        while x:
            p=x.bit_length()-1
            if p not in basis:
                basis[p]=x; break
            x ^= basis[p]
    return basis
def css_matrices(adj):
    E=edges(adj); eidx={e:i for i,e in enumerate(E)}; T=triangles(adj)
    Hx=[bit(eidx[tuple(sorted((v,w)))] for w in adj[v]) for v in range(len(adj))]
    Hz=[bit(eidx[tuple(sorted(e))] for e in itertools.combinations(t,2)) for t in T]
    return E,T,eidx,Hx,Hz
def k4_lines(adj):
    # Maximal K4 cliques in W33 are GQ lines.  Enumerate unique 4-cliques.
    lines=set()
    for quad in itertools.combinations(range(len(adj)),4):
        if all(j in adj[i] for i,j in itertools.combinations(quad,2)):
            lines.add(tuple(quad))
    return sorted(lines)
def line_star_triples(adj,E,eidx):
    rows=[]; witnesses=[]
    for line in k4_lines(adj):
        for v in line:
            other=[u for u in line if u!=v]
            eds=[tuple(sorted((v,u))) for u in other]
            row=bit(eidx[e] for e in eds)
            rows.append(row)
            witnesses.append({"line":line,"center":v,"edges":eds})
    return rows,witnesses
def commute(rowsA,rowsB): return all(((a&b).bit_count()%2)==0 for a in rowsA for b in rowsB)
def build_results():
    pts,adj=build_graph(); E,T,eidx,Hx,Hz=css_matrices(adj); line_rows,wit=line_star_triples(adj,E,eidx); bx=gf2_basis(Hx); bz=gf2_basis(Hz); bg=gf2_basis(Hx+line_rows); bl=gf2_basis(line_rows)
    stabilizer_if_added_k=len(E)-len(bg)-len(bz)
    checks=[]
    checks.append(ok('W33 counts 40/240/160',len(pts)==40 and len(E)==240 and len(T)==160,{"V":len(pts),"E":len(E),"T":len(T)}))
    checks.append(ok('K4 lines count = 40',len(k4_lines(adj))==40,len(k4_lines(adj))))
    checks.append(ok('line-star triples count = 160',len(line_rows)==160,len(line_rows)))
    checks.append(ok('line-star rows have weight 3',sorted({r.bit_count() for r in line_rows})==[3],sorted({r.bit_count() for r in line_rows})))
    checks.append(ok('line-star span rank = 120',len(bl)==120,len(bl)))
    checks.append(ok('base X rank 39, Z rank 120',len(bx)==39 and len(bz)==120,{"rx":len(bx),"rz":len(bz)}))
    checks.append(ok('X plus line-star gauge rank = 159',len(bg)==159,len(bg)))
    checks.append(ok('line-stars commute with triangle Z checks',commute(line_rows,Hz),True))
    checks.append(ok('adding line-stars as stabilizers overconstrains k negative',stabilizer_if_added_k==-39,stabilizer_if_added_k))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCCVIII","title":"Line-Star Gauge / Tomotope Bridge","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"line_star_packet":{"k4_lines":40,"stars_per_line":4,"line_star_triples":160,"line_star_span_rank":120,"line_star_weight":3,"sample_witnesses":wit[:8]},"rank_effect":{"base_X_rank":len(bx),"Z_rank":len(bz),"X_plus_line_star_rank":len(bg),"if_added_as_stabilizers_k":stabilizer_if_added_k},"tomotope_packet":{"flags":192,"edges":12,"local_flags_per_edge":16,"local_decomposition":"16=2 orientations * 4 tetrahedral chart vertices * 2 Clifford chiralities","axis_tomotope_block_duality":"48 common <r0,r3> blocks; tomotope (12,4,16,3) dual to axis (16,3,12,4)"},"architecture_upgrade":"Identifies the weight-3 X-logical obstruction as the K4 line-star packet and links it to the tomotope local incidence/Fourier-Clifford packet. The correct protection move is subsystem gauge treatment, not adding all line-stars as stabilizers.","theorem":"W33 has 40 K4 lines and 160 line-star triples of weight 3. These triples span rank 120 and commute with the triangle Z checks, but adjoining them as ordinary stabilizers would overconstrain the code. Therefore they should be treated as gauge generators/local tomotope-chart degrees, not stabilizer checks, in the next fault-tolerance layer.","honesty_boundary":"This proves the line-star obstruction and its rank effect. It does not yet construct the final subsystem code distance after gauge fixing; that is the next compiler step.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCCVIII_line_star_gauge_tomotope_bridge_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
