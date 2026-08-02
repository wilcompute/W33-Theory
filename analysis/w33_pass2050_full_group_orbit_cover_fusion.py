#!/usr/bin/env python3
"""Fail-closed replay of the Pass-2050 full-group fusion output.

The expensive run constructed the literal 51,840-element PGSp(4,3) point action,
conjugated every one of the 33 positive H=S4xD8 subgroup representatives, and
then conjugated the first deterministic 60-frame witness from each H-class.
This script validates the complete frozen fusion table and refuses to turn the
first-witness sample into a classification of all schedules.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/w33_pass2050_full_group_orbit_cover_fusion.json'
EXPECTED='ee62a332676deabb198367161800e467bb8a09e3694ca1c448d9fe45d20c0663'

def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    d=json.loads(PATH.read_text())
    assert d['sha256_without_hash_field']==EXPECTED==digest(d)
    assert all(d['checks'].values())
    types=d['full_group_fusion']['types']
    assert len(types)==14
    members=sorted(x for row in types for x in row['members'])
    assert members==list(range(33))
    for row in types:
        assert row['normalizer_order']*row['G_class_size']==51840
        assert row['H_classes']==len(row['members'])
    schedules=d['canonical_first_witnesses']['schedule_orbit_members']
    assert sorted(x for row in schedules for x in row)==list(range(33))
    assert len(schedules)==12
    assert d['canonical_first_witnesses']['distinct_frame_sets']==32
    out={'status':d['status'],'certificate':EXPECTED,'positive_H_classes':33,
         'full_group_subgroup_types':14,'first_witness_schedule_orbits':12,
         'boundary':d['boundary']}
    print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=='__main__':main()
