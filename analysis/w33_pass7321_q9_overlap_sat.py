#!/usr/bin/env python3
"""Pass7321: exact SAT extension of the q=9 local target-48 basin beyond overlap 34."""
from __future__ import annotations
import itertools,json
from pathlib import Path
from pysat.card import CardEnc,EncType
from pysat.formula import CNF,IDPool
from pysat.solvers import Cadical195
import w33_pass7163_7170_e8_hexagonal_lift as b
import w33_pass7180_q9_local_edit_radius as q

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7321_Q9_OVERLAP_SAT.json'

def main():
    Gc,rr=q.residual47();Gi=b.invmat9(Gc);comp=lambda i,j:b.pairv(b.STATES[i],Gi,b.STATES[j])!=0
    core=[x for x in rr if b.rankstate(b.STATES[x])==2];assert len(core)==42
    corepos=set(core);n=512;base=CNF()
    for i,j in itertools.combinations(range(n),2):
        if not comp(i,j):base.append([-(i+1),-(j+1)])
    pool=IDPool(start_from=n+1)
    atleast48=CardEnc.atleast(lits=[i+1 for i in range(n)],bound=48,vpool=pool,encoding=EncType.totalizer)
    base.extend(atleast48.clauses)
    results=[];first_sat=None
    for overlap in (33,32,31,30):
        cnf=CNF(from_clauses=base.clauses);enc=CardEnc.atleast(lits=[i+1 for i in core],bound=overlap,vpool=pool,encoding=EncType.totalizer);cnf.extend(enc.clauses)
        with Cadical195(bootstrap_with=cnf.clauses) as S:
            sat=S.solve();model=S.get_model() if sat else None
        witness=[]
        if sat:
            witness=sorted(i for i in range(n) if model[i]>0)[:48]
            # get_model indexing is variable order for first n in CaDiCaL; re-evaluate robustly by sign set.
            pos={abs(x) for x in model if x>0};witness=sorted(i for i in range(n) if i+1 in pos)
            assert len(witness)>=48
            # Any model may select >48; extract a 48-subset and verify clique.
            witness=witness[:48];assert all(comp(i,j) for i,j in itertools.combinations(witness,2))
            assert len(set(witness)&corepos)>=overlap
            first_sat={'overlap_threshold':overlap,'state_indices':witness,'core_overlap':len(set(witness)&corepos)}
        results.append({'minimum_core_overlap':overlap,'maximum_core_deletions':42-overlap,'target48_exists':bool(sat),'witness':first_sat if sat else None})
        if sat:break
    excluded=max((r['maximum_core_deletions'] for r in results if not r['target48_exists']),default=8)
    out={'schema':'w33.pass7321.q9_overlap_sat.v1','status':'PASS','anchor_type':'(1,3,5)','target':48,'known_core_size':42,
      'prior_exact_exclusion_through_deletions':8,'queries':results,'new_exclusion_through_deletions':excluded,
      'first_sat':first_sat,
      'theorem_or_breakthrough':('No target-48 residual clique exists with core overlap at least %d, extending the exact local basin through %d core deletions.'%(42-excluded,excluded) if first_sat is None else 'A validated target-48 residual clique was found; by the exact four-anchor reduction this is a candidate 52-point partial ovoid and must be reconstructed in ambient W(3,9) immediately.'),
      'boundary':'UNSAT statements are local to canonical anchor type (1,3,5). Unless a SAT witness is reconstructed in ambient points, no global alpha(W(3,9)) claim is made.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','excluded_through':excluded,'sat':first_sat is not None}))
if __name__=='__main__':main()
