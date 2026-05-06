"""Regression tests for PART CCCLXXVIII open-turn doc update."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXVIII_OPEN_TURN_DOC_CORRECTION_AUDIT.py'
def load_module():
    spec=importlib.util.spec_from_file_location('open_turn_doc_update_ccclxxviii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_doc_update_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_phrase_list_nonempty():
    mod=load_module(); assert len(mod.expected_phrases())>=5
def test_doc_path():
    mod=load_module(); r=mod.build_results(); assert r['doc_path'].endswith('OPEN_TURN_COMPLEMENT_DUALITY_CORRECTION.md')
