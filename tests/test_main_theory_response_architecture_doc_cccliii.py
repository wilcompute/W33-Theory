"""Regression tests for PART CCCLIII main theory response architecture doc compiler."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLIII_MAIN_THEORY_RESPONSE_ARCHITECTURE_DOC.py'
def load_module():
    spec=importlib.util.spec_from_file_location('main_doc_cccliii',MODULE_PATH); mod=importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(mod); return mod
def test_doc_compiler_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=7
def test_section_contains_core_elements():
    mod=load_module(); text=mod.section_text(); assert 'G^2 = (5049/4) I' in text; assert 'anchor-free response identity' in text; assert 'operator_core' in text; assert '2 + 9 = 11' in text
def test_result_payload_doc_layer():
    mod=load_module(); r=mod.build_results(); assert r['doc_path']=='docs/FINITE_W33_RESPONSE_ARCHITECTURE.md'; assert 'index-ready' in r['architecture_upgrade']
