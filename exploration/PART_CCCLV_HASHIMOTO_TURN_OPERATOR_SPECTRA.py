#!/usr/bin/env python3
"""PART CCCLV -- Hashimoto Triangle/Open Turn Operator Spectra Compiler.

Builds W(3,3), the 480 directed-edge Hashimoto carrier, and the exact
non-backtracking decomposition

    B = T + O,

where T records triangle-closing turns and O records open turns.  It computes
row sums, transition counts, traces of low powers, commutator norm, and exact
rank diagnostics over a modular prime.  This is the first direct operator-level
sector evidence for the triangle/open-turn response split.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
from typing import Dict, List, Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
P_RANK=1000003
Vector=Tuple[int,int,int,int]
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def mul(a,u): return tuple((a*u[i])%MOD for i in range(4))
def add(u,v): return tuple((u[i]+v[i])%MOD for i in range(4))
def omega(x,y): return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%MOD
def canon(v):
    for a in v:
        if a%MOD:
            return mul(1 if a==1 else 2,v)
    raise ValueError('zero')
def points():
    pts=[]; seen=set()
    for v in itertools.product(range(MOD), repeat=4):
        if v==(0,0,0,0): continue
        c=canon(v)
        if c not in seen: seen.add(c); pts.append(c)
    return pts
def build_graph():
    pts=points(); n=len(pts); adj=[set() for _ in range(n)]
    for i,j in itertools.combinations(range(n),2):
        if omega(pts[i],pts[j])==0: adj[i].add(j); adj[j].add(i)
    return pts,adj
def directed_edges(adj): return [(i,j) for i in range(len(adj)) for j in sorted(adj[i])]
def build_turn_matrices(adj):
    de=directed_edges(adj); idx={e:i for i,e in enumerate(de)}; n=len(de)
    T=[set() for _ in range(n)]; O=[set() for _ in range(n)]; B=[set() for _ in range(n)]
    for r,(a,b) in enumerate(de):
        for c in adj[b]:
            if c==a: continue
            col=idx[(b,c)]; B[r].add(col)
            if c in adj[a]: T[r].add(col)
            else: O[r].add(col)
    return de,B,T,O
def row_sums(M): return [len(r) for r in M]
def edge_count(M): return sum(len(r) for r in M)
def trace_product(A,B):
    # trace(A B) for sparse 0/1 row-set matrices
    total=0
    for i,row in enumerate(A):
        for j in row:
            if i in B[j]: total+=1
    return total
def matmul_sparse(A,B):
    n=len(A); C=[set() for _ in range(n)]
    for i,row in enumerate(A):
        out=set()
        for j in row: out.update(B[j])
        C[i]=out
    return C
def trace_power(A,p):
    if p==1: return sum(1 for i,row in enumerate(A) if i in row)
    M=A
    for _ in range(p-1): M=matmul_sparse(M,A)
    return sum(1 for i,row in enumerate(M) if i in row)
def commutator_frobenius_sq(A,B):
    AB=matmul_sparse(A,B); BA=matmul_sparse(B,A); total=0
    for i in range(len(A)):
        total += len(AB[i].symmetric_difference(BA[i]))
    return total
def rank_mod_sparse(M,p=P_RANK):
    # sparse rows -> modular Gaussian elimination on sets/dicts
    rows=[]
    for row in M:
        d={j:1 for j in row}
        if d: rows.append(d)
    pivots={}
    rank=0
    for row in rows:
        while row:
            pivot=min(row)
            coeff=row[pivot]%p
            if coeff==0:
                del row[pivot]; continue
            if pivot not in pivots:
                inv=pow(coeff,p-2,p)
                row={k:(v*inv)%p for k,v in row.items() if (v*inv)%p}
                pivots[pivot]=row; rank+=1; break
            factor=coeff
            prow=pivots[pivot]
            for k,v in prow.items():
                row[k]=(row.get(k,0)-factor*v)%p
                if row[k]==0: del row[k]
    return rank
def transpose_sparse(M):
    n=len(M); T=[set() for _ in range(n)]
    for i,row in enumerate(M):
        for j in row: T[j].add(i)
    return T
def build_results():
    checks=[]; pts,adj=build_graph(); de,B,T,O=build_turn_matrices(adj)
    rsB=row_sums(B); rsT=row_sums(T); rsO=row_sums(O)
    traces={"B1":trace_power(B,1),"B2":trace_power(B,2),"B3":trace_power(B,3),"T1":trace_power(T,1),"T2":trace_power(T,2),"T3":trace_power(T,3),"O1":trace_power(O,1),"O2":trace_power(O,2),"O3":trace_power(O,3),"TO_trace":trace_product(T,O),"OT_trace":trace_product(O,T)}
    ranks={"rank_B_mod_p":rank_mod_sparse(B),"rank_T_mod_p":rank_mod_sparse(T),"rank_O_mod_p":rank_mod_sparse(O),"rank_BT_mod_p":rank_mod_sparse(transpose_sparse(B))}
    comm=commutator_frobenius_sq(T,O)
    checks.append(ok('directed carrier has 480 states',len(de)==480,len(de)))
    checks.append(ok('B row sum is 11',sorted(set(rsB))==[11],sorted(set(rsB))))
    checks.append(ok('T row sum is 2',sorted(set(rsT))==[2],sorted(set(rsT))))
    checks.append(ok('O row sum is 9',sorted(set(rsO))==[9],sorted(set(rsO))))
    checks.append(ok('B edge count is 5280',edge_count(B)==480*11,edge_count(B)))
    checks.append(ok('T edge count is 960',edge_count(T)==480*2,edge_count(T)))
    checks.append(ok('O edge count is 4320',edge_count(O)==480*9,edge_count(O)))
    checks.append(ok('B=T+O disjoint rowwise',all(B[i]==T[i].union(O[i]) and T[i].isdisjoint(O[i]) for i in range(480)),True))
    checks.append(ok('B has no diagonal transitions',traces['B1']==0,traces['B1']))
    checks.append(ok('T/O commutator is nonzero',comm>0,comm))
    checks.append(ok('rank diagnostics are positive',all(v>0 for v in ranks.values()),ranks))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLV","title":"Hashimoto Triangle/Open Turn Operator Spectra Compiler","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"carrier":{"directed_edges":len(de),"B_row_sum":sorted(set(rsB)),"T_row_sum":sorted(set(rsT)),"O_row_sum":sorted(set(rsO)),"B_edges":edge_count(B),"T_edges":edge_count(T),"O_edges":edge_count(O)},"trace_moments":traces,"rank_diagnostics":ranks,"commutator_frobenius_sq":comm,"sector_interpretation":{"T":"triangle-compatible local turns, even/closed kernel evidence","O":"open nonbacktracking turns, transition/transport evidence","B":"full Hashimoto carrier B=T+O"},"architecture_upgrade":"CCCLII computed W33 graph counts. CCCLV builds the actual 480-state Hashimoto operator and its triangle/open-turn decomposition B=T+O, providing direct operator-level evidence for response-sector separation.","theorem":"In the directed-edge carrier of W(3,3), every state has 11 non-backtracking continuations split uniformly as 2 triangle turns and 9 open turns. The sparse matrices T and O are disjoint and sum to the Hashimoto operator B, giving an exact operator decomposition for local closed/even versus open/transition sector tests.","honesty_boundary":"The compiler reports sparse operator moments and modular rank diagnostics, not full real/complex eigenvalue lists. Full numerical spectra can be added if a numerical linear algebra dependency is allowed.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLV_hashimoto_turn_operator_spectra_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
