#!/usr/bin/env python3
"""PART CCCCIII -- W33 CSS Code Distance.

Part CCCCII constructed a CSS code from W33:

    physical qubits: edges, n = 240
    X checks: vertex-edge incidence, rank 39
    Z checks: triangle-boundary incidence, rank 120
    logical dimension: k = 240 - 39 - 120 = 81

This part computes the code distance.

For CSS codes:

    d_X = min wt(x) for x in ker(H_Z) \ row(H_X)
    d_Z = min wt(z) for z in ker(H_X) \ row(H_Z)
    d   = min(d_X, d_Z)

Results:

    d_X = 3
    d_Z = 4
    d   = 3

So the base W33 CSS code is

    [[240,81,3]].

Interpretation:
The code has a large topological/logical sector, but the base distance is low.
For hardware robustness, the W33 code should be treated as the finite logical
architecture/core block and then protected by lifting, concatenation, subsystem
gauge-fixing, or a higher-distance cover.
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
                basis[p]=x
                break
            x ^= basis[p]
    return basis

def reduce_by_basis(x,basis):
    y=x
    while y:
        p=y.bit_length()-1
        if p not in basis:
            return y
        y ^= basis[p]
    return 0

def css_data(adj):
    E=edges(adj); edge_index={e:i for i,e in enumerate(E)}; T=triangles(adj)
    Hx=[]
    for v in range(len(adj)):
        Hx.append(bit(edge_index[tuple(sorted((v,w)))] for w in adj[v]))
    Hz=[]
    for tri in T:
        Hz.append(bit(edge_index[tuple(sorted(e))] for e in itertools.combinations(tri,2)))
    edge_tri_masks=[0]*len(E)
    for ti,tri in enumerate(T):
        for e in itertools.combinations(tri,2):
            edge_tri_masks[edge_index[tuple(sorted(e))]] ^= (1<<ti)
    return E,T,Hx,Hz,edge_tri_masks

def in_kernel_hz(edge_subset,edge_tri_masks):
    m=0
    for i in edge_subset:
        m ^= edge_tri_masks[i]
    return m==0

def simple_cycles_len(adj,E,edge_index,L):
    cycles=set(); n=len(adj)
    def cycle_edges(cyc):
        return tuple(sorted(edge_index[tuple(sorted((cyc[i],cyc[(i+1)%L])))] for i in range(L)))
    for start in range(n):
        def dfs(path,used):
            if len(path)==L:
                if start in adj[path[-1]]:
                    cyc=path[:]
                    if min(cyc)!=start: return
                    if cyc[1]>cyc[-1]: return
                    cycles.add(tuple(cyc))
                return
            last=path[-1]
            for nb in sorted(adj[last]):
                if nb==start or nb in used or nb<start:
                    continue
                dfs(path+[nb], used|{nb})
        dfs([start],{start})
    return cycles

def cycle_bit(cyc,E,edge_index):
    L=len(cyc)
    return bit(edge_index[tuple(sorted((cyc[i],cyc[(i+1)%L])))] for i in range(L))

def compute_dx(E,edge_tri_masks,basis_Hx):
    # No weight 1 or 2 vectors satisfy ker(H_Z).  Then find/count weight-3 witnesses.
    for w in (1,2):
        for comb in itertools.combinations(range(len(E)),w):
            if in_kernel_hz(comb,edge_tri_masks) and reduce_by_basis(bit(comb),basis_Hx)!=0:
                return {"d_X":w,"witness_indices":comb,"witness_edges":[E[i] for i in comb],"weight3_kernel_count":None}
    witnesses=[]; count=0
    for comb in itertools.combinations(range(len(E)),3):
        if in_kernel_hz(comb,edge_tri_masks):
            count+=1
            if reduce_by_basis(bit(comb),basis_Hx)!=0 and not witnesses:
                witnesses.append(comb)
    assert witnesses
    comb=witnesses[0]
    return {"d_X":3,"witness_indices":comb,"witness_edges":[E[i] for i in comb],"weight3_kernel_count":count}

def compute_dz(adj,E,T,basis_Hz):
    edge_index={e:i for i,e in enumerate(E)}
    # Weight < 3 cannot be a nonzero cycle.  Weight 3 cycles are exactly triangles and are in row(H_Z).
    triangle_bits=[bit(edge_index[tuple(sorted(e))] for e in itertools.combinations(t,2)) for t in T]
    all_triangles_in_span=all(reduce_by_basis(tb,basis_Hz)==0 for tb in triangle_bits)
    cycles4=simple_cycles_len(adj,E,edge_index,4)
    nontriv=[]; trivial=0
    for cyc in cycles4:
        cb=cycle_bit(cyc,E,edge_index)
        if reduce_by_basis(cb,basis_Hz)!=0:
            nontriv.append(cyc)
        else:
            trivial+=1
    assert all_triangles_in_span
    assert nontriv
    cyc=nontriv[0]
    witness_edges=[tuple(sorted((cyc[i],cyc[(i+1)%4]))) for i in range(4)]
    return {"d_Z":4,"all_triangles_in_Z_stabilizer_span":all_triangles_in_span,"simple_4_cycles":len(cycles4),"nontrivial_4_cycles":len(nontriv),"trivial_4_cycles":trivial,"witness_vertices":cyc,"witness_edges":witness_edges}

def build_results():
    pts,adj=build_graph(); E,T,Hx,Hz,edge_tri_masks=css_data(adj); basis_Hx=gf2_basis(Hx); basis_Hz=gf2_basis(Hz)
    dx=compute_dx(E,edge_tri_masks,basis_Hx); dz=compute_dz(adj,E,T,basis_Hz); d=min(dx['d_X'],dz['d_Z'])
    checks=[]
    checks.append(ok('W33 counts 40/240/160',len(pts)==40 and len(E)==240 and len(T)==160,{"V":len(pts),"E":len(E),"T":len(T)}))
    checks.append(ok('rank Hx = 39',len(basis_Hx)==39,len(basis_Hx)))
    checks.append(ok('rank Hz = 120',len(basis_Hz)==120,len(basis_Hz)))
    checks.append(ok('d_X = 3',dx['d_X']==3,dx))
    checks.append(ok('d_Z = 4',dz['d_Z']==4,dz))
    checks.append(ok('distance d = 3',d==3,d))
    checks.append(ok('weight-3 X witnesses count = 160',dx['weight3_kernel_count']==160,dx['weight3_kernel_count']))
    checks.append(ok('all triangle 3-cycles are Z stabilizers',dz['all_triangles_in_Z_stabilizer_span'] is True,True))
    checks.append(ok('nontrivial 4-cycle witnesses exist',dz['nontrivial_4_cycles']>0,dz['nontrivial_4_cycles']))
    verified=all(c['passed'] for c in checks)
    return {
        "part":"CCCCIII",
        "title":"W33 CSS Code Distance",
        "verified":verified,
        "checks_total":len(checks),
        "checks_passed":sum(c['passed'] for c in checks),
        "css_parameters":{"n":240,"k":81,"d":d,"d_X":dx['d_X'],"d_Z":dz['d_Z'],"notation":"[[240,81,3]]"},
        "x_distance_certificate":dx,
        "z_distance_certificate":dz,
        "architecture_upgrade":"Completes the base W33 CSS stabilizer-code parameters: [[240,81,3]], with d_X=3 and d_Z=4. This proves the core has a large logical sector but low bare distance.",
        "theorem":"For the W33 edge-qubit CSS code, the minimum nontrivial X logical has weight 3 and the minimum nontrivial Z logical has weight 4. Hence the CSS code distance is d=min(3,4)=3.",
        "honesty_boundary":"Distance 3 is exact for the base code. Fault-tolerant photonic hardware will need lifting, concatenation, subsystem gauge design, or another protection layer to raise distance.",
        "checks":checks
    }

def main():
    r=build_results(); out=ROOT/'PART_CCCCIII_w33_css_distance_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"notation":r['css_parameters']['notation'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
