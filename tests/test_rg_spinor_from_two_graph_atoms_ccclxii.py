"""Regression tests for PART CCCLXII RG spinor from W33 atoms."""
from __future__ import annotations
import importlib.util
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXII_RG_SPINOR_FROM_TWO_GRAPH_ATOMS.py'
def load_module():
    spec=importlib.util.spec_from_file_location('rg_spinor_atoms_ccclxii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_spinor_derivation_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=11
def test_atoms():
    mod=load_module(); assert mod.Phi3==13; assert mod.Phi6==7; assert mod.B==67; assert mod.A==140; assert mod.M2==Fraction(5049,4)
def test_generator_identity():
    mod=load_module(); assert mod.tr(mod.G)==0; assert mod.det(mod.G)==-mod.M2; assert mod.mm(mod.G,mod.G)==mod.ms(mod.M2,mod.I)
def test_derivation_chain():
    mod=load_module(); chain=mod.derivation_chain(); assert chain['B']=='2v-Phi3=67'; assert chain['A']=='(v/2)Phi6=140'; assert chain['M2']=='(B^2+4A)/4=5049/4'
def test_result_payload_ccclxii():
    mod=load_module(); r=mod.build_results(); assert r['operator_identity']=='G^2=(5049/4)I'; assert 'derived from W33' in r['theorem']
