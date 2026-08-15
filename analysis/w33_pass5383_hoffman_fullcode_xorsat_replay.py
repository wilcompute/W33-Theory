#!/usr/bin/env python3
"""Pass5383: execute the Pass5348 full Hoffman-shortened XOR-SAT model.

Pass5348 constructs an injective 52-bit generator for the full shortened
[312,52,d] code and encodes 'exists a nonzero word of weight <=39' exactly as
XOR gates plus a cardinality constraint. Pass5383 executes that exact model,
independently reconstructs any SAT witness, and freezes the solver result under
the live pass number.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5348_hoffman_fullcode_xorsat import build_code,encode_xor
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5383_HOFFMAN_FULLCODE_XORSAT_REPLAY.json'

def main():
    from pysat.formula import CNF,IDPool
    from pysat.card import CardEnc,EncType
    from pysat.solvers import Solver
    B,coords=build_code();r=len(B);assert (r,len(coords))==(52,312)
    pool=IDPool(start_from=r+1);u=list(range(1,r+1));x=[];cnf=CNF()
    for j in coords:
        out=pool.id(('x',j));x.append(out)
        ins=[u[i] for i,row in enumerate(B) if (row>>j)&1]
        encode_xor(cnf,pool,ins,out)
    cnf.append(u[:])
    cnf.extend(CardEnc.atmost(lits=x,bound=39,vpool=pool,encoding=EncType.seqcounter).clauses)
    solver=None;used=None
    for name in ('cadical195','cadical153','glucose42','g4','m22'):
        try:
            solver=Solver(name=name,bootstrap_with=cnf.clauses);used=name;break
        except Exception:pass
    if solver is None:raise RuntimeError('No PySAT backend available')
    sat=solver.solve();model=solver.get_model() if sat else None;solver.delete()
    rec={'pass':5383,'rank':52,'length':312,'query':'exists nonzero codeword of weight <=39',
         'solver':used,'sat':bool(sat),'cnf_variables':pool.top,'cnf_clauses':len(cnf.clauses)}
    if sat:
        M={v for v in model if v>0};msg=[i for i,v in enumerate(u) if v in M];z=0
        for i in msg:z^=B[i]
        support=[j for j in coords if (z>>j)&1];wt=len(support);assert 0<wt<=39
        rec.update(status='COUNTEREXAMPLE_HOFFMAN_DISTANCE_BELOW40',witness_weight=wt,
                   message_support=msg,coordinate_support=support,
                   conclusion=f'Exact SAT witness gives d <= {wt}; combine with prior d in {{28,32,36,40}} to refine the exact distance.')
    else:
        rec.update(status='THEOREM_HOFFMAN_SHORTENED_CODE_312_52_40',minimum_distance=40,
                   code='[312,52,40]_2',
                   conclusion='UNSAT excludes every nonzero word of weight <=39; Pass5264 cell words attain weight40.')
    rec['boundary']='Exact for the reconstructed 52-dimensional shortened code; public theorem status requires successful clean replay.'
    OUT.write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
if __name__=='__main__':main()
