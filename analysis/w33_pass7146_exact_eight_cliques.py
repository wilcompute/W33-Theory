#!/usr/bin/env python3
"""Pass7146: exact maximum-clique closure for the eight q=9 Gram-anchor cases.

Requires python-sat.  Each 512-state compatibility graph is converted to a SAT
instance: one Boolean per normalized row, binary clauses for incompatible pairs,
and a cardinality constraint.  Starting from a verified greedy lower bound, we
raise the target until the first UNSAT result.  Every SAT model is checked again
against the finite-field pairing law before it can enter the certificate.
"""
from __future__ import annotations
import hashlib, itertools, json
from pathlib import Path
from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver
import w33_pass7138_7145_c2_normalform_matrix_quotient as q
import w33_pass7130_7137_structural_attack as p

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7146_EXACT_EIGHT_CLIQUES.json'
TYPES=[(1,1,2),(1,1,3),(1,1,4),(1,1,5),(1,2,3),(1,2,4),(1,3,4),(1,3,5)]
STATES=[(1,a,b,c) for a in range(1,9) for b in range(1,9) for c in range(1,9)]


def incompatibilities(rep):
    Gi=p.invmat9(q.canonical_anchor_G(rep)); bad=[]
    for i in range(512):
        for j in range(i+1,512):
            if q.pair_value9(STATES[i],Gi,STATES[j])==0: bad.append((i,j))
    return Gi,bad


def greedy(Gi):
    adj=[set() for _ in range(512)]
    for i in range(512):
        for j in range(i+1,512):
            if q.pair_value9(STATES[i],Gi,STATES[j])!=0:
                adj[i].add(j); adj[j].add(i)
    best=[]
    for s in sorted(range(512),key=lambda v:len(adj[v]),reverse=True):
        C=[s]; cand=set(adj[s])
        while cand:
            v=max(cand,key=lambda x:len(adj[x]&cand))
            C.append(v); cand &= adj[v]
        if len(C)>len(best): best=C
    return best


def verify_clique(sel,Gi):
    assert len(sel)==len(set(sel))
    assert all(q.pair_value9(STATES[i],Gi,STATES[j])!=0 for i,j in itertools.combinations(sel,2))


def solve_atleast(bad,k):
    cnf=CNF()
    for i,j in bad: cnf.append([-(i+1),-(j+1)])
    card=CardEnc.atleast(lits=list(range(1,513)),bound=k,top_id=512,encoding=EncType.totalizer)
    cnf.extend(card.clauses)
    # Freeze a content hash independently of solver output.
    h=hashlib.sha256()
    for cl in cnf.clauses: h.update((' '.join(map(str,cl))+' 0\n').encode())
    with Solver(name='cadical195',bootstrap_with=cnf.clauses) as s:
        sat=s.solve(); model=s.get_model() if sat else None
    sel=sorted(x-1 for x in (model or []) if 1<=x<=512)
    return sat,sel,h.hexdigest(),len(cnf.clauses),card.nv


def main():
    rows={}
    for rep in TYPES:
        Gi,bad=incompatibilities(rep)
        lb=greedy(Gi); verify_clique(lb,Gi)
        trials=[]; best=lb
        k=len(best)+1
        while True:
            sat,sel,sha,nclauses,nvars=solve_atleast(bad,k)
            trials.append({'target':k,'sat':sat,'cnf_sha256':sha,'clauses':nclauses,'variables':nvars})
            if not sat: break
            verify_clique(sel,Gi)
            if len(sel)>len(best): best=sel
            k=len(best)+1
        rows[str(rep)]={
            'maximum_clique':len(best),
            'maximum_state_indices':best,
            'maximum_states':[STATES[i] for i in best],
            'incompatibility_edges':len(bad),
            'trials':trials,
            'upper_certificate':f'UNSAT for clique size >= {len(best)+1}',
        }
        print(rep,rows[str(rep)]['maximum_clique'],flush=True)
    out={
      'schema':'w33.pass7146.exact_eight_cliques.v1','status':'PASS',
      'boundary':'Exact finite SAT closure of the eight normalized q=9 rank-four Gram cases; no statement beyond the proved equivalence of Pass7139 is imported silently.',
      'solver':'python-sat CaDiCaL195 + totalizer cardinality encoding',
      'states':512,'anchor_types':TYPES,'cases':rows,
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v['maximum_clique'] for k,v in rows.items()},sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
