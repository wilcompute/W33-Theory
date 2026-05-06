"""Regression tests for PART CCCLI larger W33 structure sector maps."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLI_LARGER_W33_STRUCTURE_SECTOR_MAPS.py'
def load_module():
    spec=importlib.util.spec_from_file_location('larger_w33_cccli',MODULE_PATH); mod=importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(mod); return mod
def test_all_larger_w33_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=11
def test_w33_invariants():
    mod=load_module(); inv=mod.invariant_checks(); assert inv['directed_edges_equals_2E']; assert inv['hashimoto_outdegree_split']; assert inv['h1_matches_e8_g1']
def test_expected_sector_counts():
    mod=load_module(); maps=mod.derive_all_maps(); assert maps['dirac_role']['sector_count']==2; assert maps['tetra_role']['sector_count']==4; assert maps['quotient_role']['sector_count']==4
def test_feature_registry_covers_channels():
    mod=load_module(); reg=mod.larger_feature_registry(); assert set(reg.keys())==set(mod.CHANNELS)
def test_result_payload_cccli():
    mod=load_module(); r=mod.build_results(); assert 'hashimoto_role' in r['derived_maps']; assert 'Larger W33 structures' in r['theorem']
