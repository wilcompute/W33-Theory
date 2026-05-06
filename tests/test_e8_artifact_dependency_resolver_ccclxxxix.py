"""Regression tests for PART CCCLXXXIX E8 artifact dependency resolver."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXXIX_E8_ARTIFACT_DEPENDENCY_RESOLVER.py'
def load_module():
    spec=importlib.util.spec_from_file_location('e8_dep_resolver_ccclxxxix',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_dependency_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_next_state_valid():
    mod=load_module(); r=mod.build_results(); assert r['next_state'] in ('READY_FOR_BRACKET_VERIFICATION','MISSING_ARTIFACTS_REGENERATE_OR_RESTORE')
def test_artifacts_and_tools_recorded():
    mod=load_module(); r=mod.build_results(); assert len(r['required_artifacts'])==2; assert len(r['analyzer_tools'])==4
def test_regeneration_targets():
    mod=load_module(); assert len(mod.regeneration_targets())>=5
