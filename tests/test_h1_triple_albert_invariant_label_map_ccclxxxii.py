"""Regression tests for PART CCCLXXXII H1 Triple-Albert invariant label map."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXXII_H1_TRIPLE_ALBERT_INVARIANT_LABEL_MAP.py'
def load_module():
    spec=importlib.util.spec_from_file_location('h1_label_map_ccclxxxii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_label_map_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=8
def test_counts():
    mod=load_module(); r=mod.build_results(); assert r['sector_counts']=={'diagonal_fiber':9,'octonion_offdiagonal':72}; assert r['generation_counts']=={1:27,2:27,3:27}
def test_bijections():
    mod=load_module(); rows=mod.label_map(); assert sorted(r['label_index'] for r in rows)==list(range(81)); assert sorted(r['original_h1_index'] for r in rows)==list(range(81))
def test_signature_order():
    mod=load_module(); rows=mod.label_map(); sigs=[tuple(r['signature']) for r in rows]; assert sigs==sorted(sigs)
def test_payload_ccclxxxii():
    mod=load_module(); r=mod.build_results(); assert 'cycle-signature' in r['architecture_upgrade']; assert 'not yet proved invariant' in r['honesty_boundary']
