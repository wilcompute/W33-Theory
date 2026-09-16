#!/usr/bin/env python3
"""Verify that the explicit E8->two-qutrit lift core and all four table shards agree."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
core=json.loads((ROOT/'data'/'w33_e8_pauli_cocycle_lift.json').read_text())
assert core['status']=='PASS' and core['entry_count']==80
rows=[]
for k,path in enumerate(core['entry_shards']):
    d=json.loads((ROOT/path).read_text()); assert d['status']=='PASS'
    assert d['range']==[20*k,20*k+19] and len(d['entries'])==20
    rows.extend(d['entries'])
rows=sorted(rows,key=lambda x:x['orbit_index'])
assert [r['orbit_index'] for r in rows]==list(range(80))
assert len({tuple(r['pauli_degree']) for r in rows})==80
assert all(len(r['root_cycle'])==3 and len(r['pauli_monomial_9x9'])==9 for r in rows)
assert all(r['lie_isomorphism_scale']['magnitude']=='1/sqrt(3)' for r in rows)
print(json.dumps({'status':'PASS','entries':80,'degrees':80,'shards':4,'all_core_checks':all(core['checks'].values())},indent=2))
