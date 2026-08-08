#!/usr/bin/env python3
from __future__ import annotations
import hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4214_4221_SMALL_COVER_SU4_QUANTUM_HYSTERESIS_CLOCK_HAWKING_PELL_VACUUM_VELOCITY.json'
LEGACY=ROOT/'analysis/w33_pass4213_4220_small_cover_su4_quantum_hysteresis_clock_hawking_pell_vacuum_velocity.py'
def semantic_hash(c):
    x=dict(c);x.pop('semantic_sha256',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load_engine():
    s=importlib.util.spec_from_file_location('p4213_legacy_engine',LEGACY);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def legacy_view(C):
    L={}
    mapping={4213:4214,4214:4215,4215:4216,4216:4217,4217:4218,4218:4219,4219:4220,4220:4221}
    suffixes=['small_high_girth_cover','su4_holonomic_universality','quantized_hysteresis_memory','compressed_exact_3local_clock','full_19mode_hawking_channel','pell_echo','levi_vacuum_entanglement','high_girth_information_velocity']
    for (old,new),suffix in zip(mapping.items(),suffixes):L[f'pass{old}_{suffix}']=C[f'pass{new}_{suffix}']
    return L
def verify():
    C=json.loads(OUT.read_text());assert semantic_hash(C)==C['semantic_sha256'] and C['all_checks_hold']
    assert set(C['checks'])=={str(i) for i in range(4214,4222)}
    m=load_engine();L=legacy_view(C)
    m.cover_check(L);m.su4_check(L);m.hyst_check(L);m.clock_check(L);m.hawking_check(L);m.pell_check(L);m.vac_check(L);m.velocity_check(L)
    print('PASS_4214_4221',C['semantic_sha256']);return True
if __name__=='__main__':verify()
