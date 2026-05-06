"""Regression tests for PART CCCLXVI two-graph architecture doc update."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXVI_TWO_GRAPH_ARCHITECTURE_DOC_UPDATE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('twograph_doc_ccclxvi',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_doc_update_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_expected_phrases():
    mod=load_module(); phrases=mod.expected_phrases(); assert 'M M^T = 320 I + 16 J + 4 A' in phrases; assert 'nullity(K) = 4440' in phrases
def test_doc_path():
    mod=load_module(); r=mod.build_results(); assert r['doc_path']=='docs/TWO_GRAPH_RESPONSE_ARCHITECTURE_ADDENDUM.md'
