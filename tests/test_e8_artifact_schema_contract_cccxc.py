"""Regression tests for PART CCCXC E8 artifact schema contract."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCXC_E8_ARTIFACT_SCHEMA_CONTRACT.py'
def load_module():
    spec=importlib.util.spec_from_file_location('e8_schema_contract_cccxc',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_schema_contract_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_artifact_paths_declared():
    mod=load_module(); assert len(mod.ARTIFACTS)==4; assert 'structure_constants' in mod.ARTIFACTS; assert 'root_metadata' in mod.ARTIFACTS
def test_readiness_keys():
    mod=load_module(); r=mod.build_results(); assert set(r['readiness'])=={'g1g2_to_g0_ready','g1g1_to_g2_firewall_ready'}
def test_validations_shape():
    mod=load_module(); v=mod.validations(); assert len(v)==4; assert all('valid' in x for x in v.values())
