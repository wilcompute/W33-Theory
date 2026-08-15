from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'analysis/w33_pass5404_5409_allq_unsigned_apartment_spectrum.py'
FROZEN=ROOT/'data/PART_W33_PASS5404_5409_ALLQ_UNSIGNED_APARTMENT_SPECTRUM.json'
BT546=ROOT/'data/PART_BT546_W33_LEVI_CYCLE_PHASE_FRAME_UNIFICATION_results.json'
BT549=ROOT/'data/PART_BT549_W33_LEVI_CYCLE_CUT_TIGHT_FRAME_DUALITY_results.json'


def load_module():
    spec=importlib.util.spec_from_file_location('pass5404_unsigned',SCRIPT);assert spec and spec.loader
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def test_frozen_certificate_matches_executable():
    m=load_module(); assert m.build_certificate()==json.loads(FROZEN.read_text(encoding='utf-8'))


def test_unsigned_full_rank_signed_cycle_rank_and_cut_gap():
    m=load_module()
    for q in m.ANCHORS:
        r=m.row(q);N=(q+1)**2*(q*q+1)
        assert r['unsigned_rank']==N
        assert r['signed_rank']==q**4
        assert r['rank_gap_cut_space']==2*(q+1)*(q*q+1)-1
        assert sum(r['multiplicities'])==N


def test_q3_recovers_bt546_and_bt549():
    new=json.loads(FROZEN.read_text(encoding='utf-8'))['anchors']['3']
    b546=json.loads(BT546.read_text(encoding='utf-8'))
    b549=json.loads(BT549.read_text(encoding='utf-8'))
    assert new['flags']==160
    assert new['multiplicities']==[1,24,30,24,81]
    assert new['eigenvalues']==['648','36*(4+sqrt(6))','72','36*(4-sqrt(6))','40']
    old_spec=b546['unsigned_X_side']['spectrum']
    assert old_spec['648']==1
    assert old_spec['144+36sqrt6']==24
    assert old_spec['72']==30
    assert old_spec['144-36sqrt6']==24
    assert old_spec['40']==81
    assert new['signed_rank']==b549['objects']['cycle_projector_rank']==81
    assert new['rank_gap_cut_space']==b549['objects']['cut_projector_rank']==79
