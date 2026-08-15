#!/usr/bin/env python3
"""Pass5349: exact XOR-SAT search for a q=11 weight-20 dual shell on the 120-edge equality wall.

Pass5304 proved that any q11 dual20 has at least 120 selected carrier-pair edges.
Equality holds exactly when every W-point is covered 0 or 2 times. This model
searches that extremal case directly: 7381 carrier variables, exact weight20,
one fixed carrier by transitivity, even point parity, and at-most-two selected
carriers through every W-point. SAT returns a genuine weight20 dual witness;
UNSAT proves that no dual20 can saturate the 120-edge wall (but does not exclude
higher-overlap dual20 supports).
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from analysis.w33_pass5304_q11_dual20_density_wall import carriers
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5349_Q11_DUAL20_DOUBLECOVER_XORSAT.json'

def xor_gate(cnf,a,b,c):
    cnf.extend([[a,b,-c],[-a,-b,-c],[a,-b,c],[-a,b,c]])

def parity_zero(cnf,pool,lits,key):
    if not lits:return
    if len(lits)==1:cnf.append([-lits[0]]);return
    cur=lits[0]
    for k,b in enumerate(lits[1:]):
        t=pool.id(('px',key,k));xor_gate(cnf,cur,b,t);cur=t
    cnf.append([-cur])

def components(adj):
    rem=set(adj);out=[]
    while rem:
        s=next(iter(rem));C={s};Q=[s];rem.remove(s)
        while Q:
            u=Q.pop()
            for v in adj[u]:
                if v in rem:rem.remove(v);C.add(v);Q.append(v)
        out.append(sorted(C))
    return sorted(out,key=lambda C:(len(C),C))

def cycle_lengths(vertices,adj):
    rem=set(vertices);ans=[]
    while rem:
        s=next(iter(rem));prev=None;u=s;L=[]
        while True:
            L.append(u);rem.discard(u)
            nxt=[v for v in adj[u] if v in set(vertices) and v!=prev]
            if not nxt:break
            v=nxt[0]
            if v==s:break
            prev,u=u,v
        ans.append(len(L))
    return sorted(ans)

def main():
    from pysat.formula import CNF,IDPool
    from pysat.card import CardEnc,EncType
    from pysat.solvers import Solver
    P,C=carriers(11);n=len(C);assert len(P)==1464 and n==7381
    inc=[[] for _ in P]
    for j,B in enumerate(C):
        for p in B:inc[p].append(j)
    assert {len(v) for v in inc}=={121}
    y=list(range(1,n+1));pool=IDPool(start_from=n+1);cnf=CNF()
    cnf.append([y[0]]) # carrier transitivity symmetry break
    cnf.extend(CardEnc.equals(lits=y,bound=20,vpool=pool,encoding=EncType.seqcounter).clauses)
    for p,L in enumerate(inc):
        lits=[y[j] for j in L]
        parity_zero(cnf,pool,lits,p)
        cnf.extend(CardEnc.atmost(lits=lits,bound=2,vpool=pool,encoding=EncType.seqcounter).clauses)
    solver=None;used=None
    for name in ['cadical195','cadical153','g4','m22']:
        try:solver=Solver(name=name,bootstrap_with=cnf.clauses);used=name;break
        except Exception:pass
    if solver is None:raise RuntimeError('no PySAT backend available')
    sat=solver.solve();model=solver.get_model() if sat else None;solver.delete()
    rec={'pass':5349,'solver':used,'q':11,'P_components':n,'query':'weight20 dual support with all W-point multiplicities in {0,2}','sat':bool(sat)}
    if not sat:
        rec.update(status='THEOREM_Q11_NO_DUAL20_ON_120_EDGE_EQUALITY_WALL',
                   conclusion='Any q11 dual20, if one exists, must have >120 adjacent carrier pairs and at least one W-point of multiplicity >=4.',
                   boundary='This does not exclude weight20 dual words above the equality wall and does not prove d=121.')
    else:
        M=set(v for v in model if v>0);S=[j for j,v in enumerate(y) if v in M];assert len(S)==20 and 0 in S
        degp=[sum(p in C[j] for j in S) for p in range(len(P))]
        assert set(degp)<={0,2} and sum(degp)==480
        A={j:set() for j in S};N={j:set() for j in S}
        e=0
        for a,b in itertools.combinations(S,2):
            t=len(set(C[a])&set(C[b]));assert t in (0,2)
            if t==2:A[a].add(b);A[b].add(a);e+=1
            else:N[a].add(b);N[b].add(a)
        assert e==120 and {len(A[j]) for j in S}=={12}
        comps=components(N);ctype=[len(x) for x in comps]
        skeleton=None
        if ctype==[10,10]:
            internal={j:{v for v in A[j] if v in set(next(Cc for Cc in comps if j in Cc))} for j in S}
            if {len(internal[j]) for j in S}=={2}:
                skeleton={'complement_components':[list(x) for x in comps],
                          'internal_2factor_cycle_types':[cycle_lengths(x,internal) for x in comps],
                          'type':'K10,10 plus a 2-factor on each half'}
        rec.update(status='THEOREM_Q11_DUAL20_EQUALITY_WITNESS',selected_carriers=S,
                   active_W_points=sum(d==2 for d in degp),selected_pair_edges=e,
                   selected_graph_degree=12,zero_intersection_complement_component_sizes=ctype,
                   skeleton=skeleton,
                   conclusion='A genuine q11 weight20 footprint-dual word exists and saturates the exact 120-edge overlap lower bound.',
                   boundary='The witness alone does not yet prove primal d=121; a pair-orbital moment certificate is the next step.')
    rec['certificate']='Exact CNF: 7381 carrier bits, weight exactly20, one transitivity-fixed carrier, even point parities, and point multiplicity <=2.'
    OUT.write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
if __name__=='__main__':main()
