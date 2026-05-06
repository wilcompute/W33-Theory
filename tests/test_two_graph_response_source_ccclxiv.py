"""Regression tests for PART CCCLXIV two-graph response source."""
from __future__ import annotations
import importlib.util
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXIV_TWO_GRAPH_PRIMITIVE_RESPONSE_OPERATOR.py'
def load_module():
    spec=importlib.util.spec_from_file_location('twograph_source_ccclxiv',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_atoms():
    mod=load_module(); d=mod.primitive_derivation(); assert d['k']==12; assert d['q']==3; assert d['B']==67; assert d['offdiag']==140
def test_square_identity():
    mod=load_module(); d=mod.primitive_derivation(); assert d['M2']==Fraction(5049,4); assert d['G2']==mod.scale2(d['M2'],d['I'])
def test_payload():
    mod=load_module(); r=mod.build_results(); assert r['generator']['M2']=='5049/4'
