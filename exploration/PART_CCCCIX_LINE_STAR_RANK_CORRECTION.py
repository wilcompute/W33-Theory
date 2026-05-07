#!/usr/bin/env python3
"""PART CCCCIX -- Line-Star Rank Correction and Matter-Sector Interpretation.

Part CCCCVIII correctly identified the K4 line-star triples as the weight-3
X-logical obstruction, but its rank accounting overreached.  If the line-star
rows commute with all triangle Z checks, they lie in ker(H_Z).  Since
rank(H_Z)=120 on n=240 qubits, dim ker(H_Z)=120.  Therefore the span of vertex
X checks plus line-star rows cannot have rank 159.

This correction computes the exact facts:

    rank(H_X vertex checks) = 39
    rank(H_Z triangle checks) = 120
    dim ker(H_Z) = 120
    rank(line-star span) = 120
    rank(H_X + line-star span) = 120
    quotient rank line-star / H_X = 120 - 39 = 81

Thus the K4 line-star packet is not merely a small obstruction; modulo vertex
switching, it spans the entire 81-dimensional X-logical/matter sector.

Consequences:
  - adding all line-stars as stabilizers gives k = 240 - 120 - 120 = 0;
  - promoting all line-stars to pure gauge would erase the W33 matter sector;
  - to raise distance while preserving k=81, the line-star degrees must be
    encoded into a higher-distance local packet (tomotope/chirality/inner code),
    not simply killed.
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
def commute(rowsA,rowsB): return all(((a&b).bit_count()%2)==0 for a in rowsA for b in rowsB)
def css(adj):
    E=edges(adj); T=triangles(adj); eidx={e:i for i,e in enumerate(E)}
    Hx=[bit(eidx[tuple(sorted((v,w)))] for w in adj[v]) for v in range(len(adj))]
    Hz=[bit(eidx[tuple(sorted(e))] for e in itertools.combinations(t,2)) for t in T]
    return E,T,eidx,Hx,Hz
def k4_lines(adj):
    return sorted(tuple(q) for q in itertools.combinations(range(len(adj)),4) if all(j in adj[i] for i,j in itertools.combinations(q,2)))
def line_star_rows(adj,eidx):
    rows=[]; witnesses=[]
    for line in k4_lines(adj):
        for v in line:
            others=[u for u in line if u!=v]
            eds=[tuple(sorted((v,u))) for u in others]
            rows.append(bit(eidx[e] for e in eds))
            witnesses.append({"line":line,"center":v,"edges":eds})
    return rows,witnesses
def build_results():
    pts,adj=build_graph(); E,T,eidx,Hx,Hz=css(adj); L,wit=line_star_rows(adj,eidx)
    rx=len(gf2_basis(Hx)); rz=len(gf2_basis(Hz)); rL=len(gf2_basis(L)); rXL=len(gf2_basis(Hx+L)); k_base=len(E)-rx-rz; k_if_line_stabilizers=len(E)-rXL-rz; quotient_line_mod_vertex=rXL-rx
    checks=[]
    checks.append(ok('W33 counts 40/240/160',len(pts)==40 and len(E)==240 and len(T)==160,{"V":len(pts),"E":len(E),"T":len(T)}))
    checks.append(ok('K4 lines = 40',len(k4_lines(adj))==40,len(k4_lines(adj))))
    checks.append(ok('line-star triples = 160',len(L)==160,len(L)))
    checks.append(ok('line-star rows weight 3',sorted({r.bit_count() for r in L})==[3],sorted({r.bit_count() for r in L})))
    checks.append(ok('line-stars commute with triangle Z checks',commute(L,Hz),True))
    checks.append(ok('rank H_X=39, rank H_Z=120',rx==39 and rz==120,{"rx":rx,"rz":rz}))
    checks.append(ok('rank line-star span = 120',rL==120,rL))
    checks.append(ok('rank H_X plus line-stars = 120',rXL==120,rXL))
    checks.append(ok('line-star quotient over vertex checks = 81',quotient_line_mod_vertex==81,quotient_line_mod_vertex))
    checks.append(ok('adding line-stars as stabilizers gives k=0',k_if_line_stabilizers==0,k_if_line_stabilizers))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCCIX","title":"Line-Star Rank Correction and Matter-Sector Interpretation","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"rank_table":{"rank_X_vertex":rx,"rank_Z_triangle":rz,"base_k":k_base,"rank_line_star_span":rL,"rank_X_plus_line_star":rXL,"line_star_mod_vertex_rank":quotient_line_mod_vertex,"k_if_line_stars_are_stabilizers":k_if_line_stabilizers},"line_star_packet":{"k4_lines":40,"line_star_triples":160,"line_star_weight":3,"sample_witnesses":wit[:8]},"architecture_upgrade":"Corrects the line-star gauge rank accounting: the K4 line-stars span the full X-logical/matter sector modulo vertex checks. They are not disposable stabilizers; they are the local low-distance representation of the 81 protected degrees.","theorem":"The 160 K4 line-star triples span a 120-dimensional subspace equal to ker(H_Z). Modulo the 39 vertex checks, this gives an 81-dimensional quotient, exactly the W33 logical/matter sector. Adding them as stabilizers would collapse k to zero.","honesty_boundary":"This supersedes the rank-effect statement in CCCCVIII. The next fault-tolerance layer must re-encode the line-star/matter degrees into a higher-distance tomotope/chirality or inner-code packet rather than gauge them away.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCCIX_line_star_rank_correction_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
