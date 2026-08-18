#!/usr/bin/env python3
"""Pass7154: solve one of the eight residual q=9 48-clique decisions.

Environment CASE_INDEX selects one of the eight anchor types. The output is a replayable
SAT/UNSAT record with a CNF content hash. SAT models are rechecked against the exact
GF(9) pairing law. The aggregate workflow runs all eight cases in parallel.
"""
from __future__ import annotations
import hashlib, itertools, json, os
from pathlib import Path
from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver
import w33_pass7130_7137_structural_attack as p
import w33_pass7138_7145_c2_normalform_matrix_quotient as q

TYPES=[(1,1,2),(1,1,3),(1,1,4),(1,1,5),(1,2,3),(1,2,4),(1,3,4),(1,3,5)]
STATES=[(1,a,b,c) for a in range(1,9) for b in range(1,9) for c in range(1,9)]
idx=int(os.environ['CASE_INDEX']); rep=TYPES[idx]
out=Path(os.environ.get('CASE_OUTPUT',f'evidence/pass7154/case_{idx}.json'))
out.parent.mkdir(parents=True,exist_ok=True)
Gi=p.invmat9(q.canonical_anchor_G(rep)); bad=[]
for i in range(512):
    for j in range(i+1,512):
        if q.pair_value9(STATES[i],Gi,STATES[j])==0: bad.append((i,j))
cnf=CNF()
for i,j in bad: cnf.append([-(i+1),-(j+1)])
card=CardEnc.atleast(lits=list(range(1,513)),bound=48,top_id=512,encoding=EncType.totalizer)
cnf.extend(card.clauses)
h=hashlib.sha256()
for cl in cnf.clauses: h.update((' '.join(map(str,cl))+' 0\n').encode())
with Solver(name='cadical195',bootstrap_with=cnf.clauses) as s:
    sat=s.solve(); model=s.get_model() if sat else None; stats=s.accum_stats()
sel=sorted(x-1 for x in (model or []) if 1<=x<=512)
if sat:
    assert len(sel)>=48
    assert all(q.pair_value9(STATES[i],Gi,STATES[j])!=0 for i,j in itertools.combinations(sel,2))
row={
 'schema':'w33.pass7154.parallel48.case.v1','case_index':idx,'anchor_type':list(rep),
 'target':48,'sat':bool(sat),'incompatibility_edges':len(bad),'cnf_sha256':h.hexdigest(),
 'clauses':len(cnf.clauses),'variables':card.nv,'solver':'CaDiCaL195 via python-sat','solver_stats':stats,
 'selected_state_indices':sel if sat else [],'selected_states':[STATES[i] for i in sel] if sat else [],
}
out.write_text(json.dumps(row,indent=2,sort_keys=True)+'\n')
print(json.dumps(row,sort_keys=True))
