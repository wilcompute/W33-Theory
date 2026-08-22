#!/usr/bin/env python3
"""Pass7386: exact SAT decision of the C2-invariant q=9 target-52 branch.

This is deliberately NOT a WLOG reduction. It decides only partial ovoids invariant
under the exact involution stabilizing the frozen 51-set.
"""
from __future__ import annotations
import hashlib,itertools,json
from pathlib import Path
from pysat.card import CardEnc,EncType
from pysat.formula import CNF,IDPool
from pysat.solvers import Cadical195
from w33_pass7107_q9_target_52 import build,check_field,ADD,MUL,INV

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7386_Q9_INVOLUTION_TARGET52_SAT.json'
A=[[6,0,0,0],[6,3,1,2],[1,0,4,2],[1,0,7,8]]
def sf(xs):
    z=0
    for x in xs:z=ADD[z][x]
    return z
def mv(x):return tuple(sf(MUL[A[i][j]][x[j]] for j in range(4)) for i in range(4))
def canon(v):
    z=INV[next(x for x in v if x)];return tuple(MUL[z][x] for x in v)
def digest(cnf):
    h=hashlib.sha256()
    for C in cnf.clauses:h.update((' '.join(map(str,C))+' 0\n').encode())
    return h.hexdigest()

def solve_case(orbs,valid,adj,fixed_count,pair_count):
    nodes=[k for k in valid];pos={k:i+1 for i,k in enumerate(nodes)};cnf=CNF();conf=0
    for a,b in itertools.combinations(nodes,2):
        if any(y in adj[x] for x in orbs[a] for y in orbs[b]):
            cnf.append([-pos[a],-pos[b]]);conf+=1
    F=[pos[k] for k in nodes if len(orbs[k])==1];P=[pos[k] for k in nodes if len(orbs[k])==2]
    pool=IDPool(start_from=len(nodes)+1)
    ce=CardEnc.equals(F,bound=fixed_count,vpool=pool,encoding=EncType.totalizer);cnf.extend(ce.clauses)
    ce=CardEnc.equals(P,bound=pair_count,vpool=pool,encoding=EncType.totalizer);cnf.extend(ce.clauses)
    sha=digest(cnf)
    with Cadical195(bootstrap_with=cnf.clauses) as s:
        sat=s.solve();model=s.get_model() if sat else None
    selected=[]
    if sat:
        M=set(x for x in model if x>0)
        selected=[k for k in nodes if pos[k] in M]
        assert sum(len(orbs[k]) for k in selected)==fixed_count+2*pair_count==52
        pts=[x for k in selected for x in orbs[k]]
        assert all(y not in adj[x] for x,y in itertools.combinations(pts,2))
    return {'fixed_count':fixed_count,'pair_orbits':pair_count,'variables_primary':len(nodes),'conflict_clauses':conf,'cnf_variables':cnf.nv,'cnf_clauses':len(cnf.clauses),'cnf_sha256':sha,'satisfiable':sat,'selected_orbits':selected}

def main():
    check_field();P,adj,B=build();pi={p:i for i,p in enumerate(P)};perm=tuple(pi[canon(mv(p))] for p in P)
    assert all(perm[perm[i]]==i for i in range(820))
    seen=set();orbs=[]
    for i in range(820):
        if i in seen:continue
        O=tuple(sorted({i,perm[i]}));seen.update(O);orbs.append(O)
    assert sorted(map(len,orbs)).count(1)==20
    bad={k for k,O in enumerate(orbs) if len(O)==2 and O[1] in adj[O[0]]};assert len(bad)==40
    valid=[k for k in range(420) if k not in bad];assert len(valid)==380
    cases=[solve_case(orbs,valid,adj,0,26),solve_case(orbs,valid,adj,2,25)]
    assert all(not x['satisfiable'] for x in cases)
    out={'schema':'w33.pass7386.q9_involution_target52_sat.v1','status':'PASS','orbit_variables':380,'fixed_orbits':20,'admissible_pair_orbits':360,'forbidden_internal_pair_orbits':40,'cases':cases,'theorem':'There is no 52-point partial ovoid invariant under the exact projective C2 stabilizer of the frozen 51-set. The only parity-allowed branches, 0 fixed + 26 pairs and 2 fixed + 25 pairs, are both SAT-UNSAT with frozen CNF hashes.','boundary':'This is an exact closure of the C2-invariant branch only. An asymmetric 52-set remains possible; alpha(W(3,9)) is not claimed to be 51.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','cases':[(x['fixed_count'],x['satisfiable']) for x in cases]}))
if __name__=='__main__':main()
