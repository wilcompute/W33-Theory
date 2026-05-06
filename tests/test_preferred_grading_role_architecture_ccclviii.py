"""Regression tests for PART CCCLVIII preferred grading-role architecture."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLVIII_PREFERRED_GRADING_ROLE_ARCHITECTURE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('preferred_grading_ccclviii',MODULE_PATH); mod=importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(mod); return mod
def test_all_preferred_architecture_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=7
def test_preferred_blocks():
    mod=load_module(); b=mod.blocks(mod.PREFERRED); assert b['0']==['mass','heat_trace','zeta']; assert b['1']==['gap','spinor_trace','resolvent_trace']
def test_fallbacks_are_refinements():
    mod=load_module(); assert len(set(mod.MINIMAL.values()))>len(set(mod.PREFERRED.values())); assert len(set(mod.TRANSFORM.values()))>len(set(mod.MINIMAL.values()))
def test_evidence_table_sources():
    mod=load_module(); parts={e['part'] for e in mod.evidence_table()}; assert 'CCCLVI' in parts; assert 'CCCLVII' in parts
def test_result_payload_ccclviii():
    mod=load_module(); r=mod.build_results(); assert r['architecture_policy']['preferred']=='operator_core/grading_role'; assert 'preferred finite W33 response-sector architecture' in r['promoted_theorem']
