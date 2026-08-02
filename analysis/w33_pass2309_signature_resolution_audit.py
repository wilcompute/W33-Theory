#!/usr/bin/env python3
"""Pass 2309: exact 720-signature necessary-condition audit for a 9-cover resolution.

The complete 3,547,800 exact-cover census collapses to 720 globally realized
45-coordinate nonlinear signatures.  Any partition of the 540 frames into nine
60-frame covers must select a multiset of nine realized signatures summing to
the universal capacity vector 12*1.

This script solves that integer feasibility problem exactly with CP-SAT.  A
feasible multiset is only a necessary condition for a frame-level resolution;
it is not itself a resolution.  An infeasible result would rule out chi(H)=9.
"""
from __future__ import annotations
import base64, gzip, hashlib, json
from pathlib import Path
from ortools.sat.python import cp_model

ROOT=Path(__file__).resolve().parents[1]
SIG_PATH=ROOT/'data/w33_pass1825_signatures720.json.gz.b64'
CERT_PATH=ROOT/'data/w33_pass1821_1825_complete_cover_signature.json'
OUT_PATH=ROOT/'data/w33_pass2309_signature_resolution_audit.json'

def load_signatures():
    raw=gzip.decompress(base64.b64decode(SIG_PATH.read_text().strip()))
    obj=json.loads(raw)
    if isinstance(obj,list): sigs=obj
    elif isinstance(obj,dict):
        for k in ('signatures','vectors','data','rows'):
            if k in obj:
                sigs=obj[k];break
        else: raise KeyError(f'unknown signature payload keys: {sorted(obj)}')
    else: raise TypeError(type(obj))
    sigs=[[int(x) for x in row] for row in sigs]
    assert len(sigs)==720 and {len(x) for x in sigs}=={45}
    return sigs

def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    sigs=load_signatures(); cert=json.loads(CERT_PATH.read_text())
    p=cert['pass1823_packing_signature_obstruction']
    derived=[sum(row[j] for row in p['packing_signatures'])+p['residual_capacity'][j] for j in range(45)]
    assert derived==[12]*45

    model=cp_model.CpModel()
    x=[model.NewIntVar(0,9,f'x{i}') for i in range(720)]
    model.Add(sum(x)==9)
    for j in range(45): model.Add(sum(sigs[i][j]*x[i] for i in range(720))==12)
    # Canonical deterministic feasible multiset if one exists.
    model.Minimize(sum((i+1)*x[i] for i in range(720)))
    solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=1
    solver.parameters.random_seed=0
    solver.parameters.max_time_in_seconds=900.0
    status=solver.Solve(model)
    status_name=solver.StatusName(status)
    selected=[]
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        selected=[{'signature_index':i,'multiplicity':solver.Value(x[i]),'signature':sigs[i]}
                  for i in range(720) if solver.Value(x[i])]
        assert sum(z['multiplicity'] for z in selected)==9
        total=[sum(z['multiplicity']*z['signature'][j] for z in selected) for j in range(45)]
        assert total==[12]*45
    out={
      'schema':'w33.pass2309.signature_resolution_audit.v1',
      'status':status_name,
      'source_signature_sha256':cert['pass1825_solver_export']['signature_sha256'],
      'signature_count':720,'signature_shape':[720,45],
      'target_capacity':[12]*45,'cover_count':9,
      'selected_multiset':selected,
      'objective_value':solver.ObjectiveValue() if selected else None,
      'solver':{'name':'OR-Tools CP-SAT','workers':1,'random_seed':0,
                'wall_time_seconds':solver.WallTime(),'branches':solver.NumBranches(),
                'conflicts':solver.NumConflicts(),'response_stats':solver.ResponseStats()},
      'interpretation':('A realized-signature multiset satisfying the nonlinear quotient exists; frame-level compatibility remains open.'
                        if selected else
                        'No realized-signature multiset satisfies the nonlinear quotient; this rules out a nine-cover resolution.'),
      'boundary':'Signature feasibility is necessary but not sufficient for nine pairwise disjoint covers. No chi(H)=9 claim is made unless literal frame compatibility is certified.',
      'checks':{'payload_720x45':True,'capacity_derived_from_frozen_four_packing':True,
                'nine_signature_sum_checked':bool(selected) or status_name in ('INFEASIBLE','MODEL_INVALID')}
    }
    out['sha256_without_hash_field']=digest(out)
    OUT_PATH.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
