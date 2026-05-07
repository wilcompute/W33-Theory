#!/usr/bin/env python3
"""PART CCCCII -- W33 CSS Topological Code Architecture.

The CCCC/CCCCI signed-switching bridge has an immediate quantum-computing
interpretation:

    qubits live on W33 edges (n = 240),
    X/star checks live on vertices (rank = 39),
    Z/face checks live on triangles (rank = 120).

Because every triangle boundary meets each vertex in 0 or 2 incident edges,

    H_X H_Z^T = 0  over GF(2),

so this is a valid CSS stabilizer code.  Its encoded logical dimension is

    k = n - rank(H_X) - rank(H_Z) = 240 - 39 - 120 = 81.

This upgrades the photonic topological quantum computer architecture:

    signed edge phases      -> physical edge qubits / phase bits,
    vertex switching        -> X-gauge/star equivalence,
    triangle flatness       -> Z-face stabilizers,
    residual 2^81 sectors   -> logical/topological matter memory.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
Vector=Tuple[int,int,int,int]

def ok(name, cond, value=None):
    return {"name":name,"passed":bool(cond),"value":value}

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
        if c not in seen:
            seen.add(c); pts.append(c)
    return pts

def build_graph():
    pts=points(); adj=[set() for _ in pts]
    for i,j in itertools.combinations(range(len(pts)),2):
        if omega(pts[i],pts[j])==0:
            adj[i].add(j); adj[j].add(i)
    return pts,adj

def edges(adj): return [(i,j) for i in range(len(adj)) for j in sorted(adj[i]) if i<j]
def triangles(adj): return [(i,j,k) for i,j,k in itertools.combinations(range(len(adj)),3) if j in adj[i] and k in adj[i] and k in adj[j]]

def gf2_rank_rows(rows,ncols):
    basis={}
    for row in rows:
        x=row
        while x:
            p=x.bit_length()-1
            if p not in basis:
                basis[p]=x
                break
            x ^= basis[p]
    return len(basis)

def bit_from_indices(indices):
    x=0
    for i in indices: x ^= (1<<i)
    return x

def css_matrices(adj):
    E=edges(adj); edge_index={e:i for i,e in enumerate(E)}; T=triangles(adj)
    # X checks: vertex-edge incidence rows, one row per vertex.
    Hx=[]
    for v in range(len(adj)):
        Hx.append(bit_from_indices(edge_index[tuple(sorted((v,w)))] for w in adj[v]))
    # Z checks: triangle boundary rows, one row per triangle.
    Hz=[]
    for tri in T:
        Hz.append(bit_from_indices(edge_index[tuple(sorted(e))] for e in itertools.combinations(tri,2)))
    return E,T,Hx,Hz

def commute(Hx,Hz):
    for x in Hx:
        for z in Hz:
            if (x & z).bit_count() % 2:
                return False
    return True

def row_weight_set(rows): return sorted({r.bit_count() for r in rows})

def build_results():
    pts,adj=build_graph(); E,T,Hx,Hz=css_matrices(adj); n=len(E); rx=gf2_rank_rows(Hx,n); rz=gf2_rank_rows(Hz,n); k=n-rx-rz
    checks=[]
    checks.append(ok('W33 counts 40/240/160',len(pts)==40 and len(E)==240 and len(T)==160,{"V":len(pts),"E":len(E),"T":len(T)}))
    checks.append(ok('CSS commutation Hx Hz^T = 0',commute(Hx,Hz),True))
    checks.append(ok('rank Hx = 39',rx==39,rx))
    checks.append(ok('rank Hz = 120',rz==120,rz))
    checks.append(ok('logical k = 81',k==81,k))
    checks.append(ok('physical qubits n = 240',n==240,n))
    checks.append(ok('X check weights are vertex degree 12',row_weight_set(Hx)==[12],row_weight_set(Hx)))
    checks.append(ok('Z check weights are triangle boundaries 3',row_weight_set(Hz)==[3],row_weight_set(Hz)))
    checks.append(ok('encoded sector count 2^81',k==81,"2^81"))
    verified=all(c['passed'] for c in checks)
    return {
        "part":"CCCCII",
        "title":"W33 CSS Topological Code Architecture",
        "verified":verified,
        "checks_total":len(checks),
        "checks_passed":sum(c['passed'] for c in checks),
        "css_parameters":{
            "n_physical_edge_qubits":n,
            "rank_X_vertex_checks":rx,
            "rank_Z_triangle_checks":rz,
            "k_logical_qubits":k,
            "distance":"not_computed",
            "notation":"[[240,81,d]] with d pending"
        },
        "check_weights":{
            "X_vertex_check_weights":row_weight_set(Hx),
            "Z_triangle_check_weights":row_weight_set(Hz)
        },
        "architecture_map":{
            "edge_signs":"physical edge phase/qubit variables",
            "vertex_switching":"X/star gauge checks, rank 39",
            "triangle_flatness":"Z/face stabilizer checks, rank 120",
            "logical_sector":"2^81 residual topological sectors = H1 matter module"
        },
        "architecture_upgrade":"Turns the signed-switching quotient into a concrete CSS stabilizer-code architecture for the photonic topological quantum computer: edge qubits, vertex X checks, triangle Z checks, and 81 encoded logical/topological degrees of freedom.",
        "theorem":"The W33 edge-qubit CSS code with vertex incidence X checks and triangle-boundary Z checks is valid because H_X H_Z^T=0 over GF(2). Its stabilizer ranks are 39 and 120, hence it encodes k=240-39-120=81 logical qubits/sectors.",
        "honesty_boundary":"The code dimension is exact. The code distance and a physical photonic measurement schedule are not computed here and remain next-step hardware/compiler tasks.",
        "checks":checks
    }

def main():
    r=build_results(); out=ROOT/'PART_CCCCII_w33_css_topological_code_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"k":r['css_parameters']['k_logical_qubits'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
