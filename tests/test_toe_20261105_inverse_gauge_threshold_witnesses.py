"""Counterexample searches and exact 2x2 inverse BSM gauge threshold fits."""
from __future__ import annotations
import sys,json
from pathlib import Path
from fractions import Fraction as F
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261105_inverse_gauge_threshold_witnesses as p
@pytest.fixture(scope="module")
def r():
    return p.main()

def test_beta_coefficients_exact(r):
    assert p.SPECIES["VL_quark_doublet_3_2_1_6"]==(F(2,15),F(2),F(4,3))
    assert p.SPECIES["Majorana_SU2_adjoint_1_3_0"]==(F(0),F(4,3),F(0))
    assert p.SM==(F(41,10),-F(19,6),-F(7))

def test_only_two_one_species_witnesses_among_nine_declared(r):
    assert r["enumerated_declared_representation_count"]==9
    assert r["solutions_count_by_added_species"][1]==2
    assert {x["new_multiplets"][0] for x in r["valid_single_species_witnesses"]}=={
       "VL_quark_doublet_3_2_1_6","Majorana_SU2_adjoint_1_3_0"}

def test_required_masses_solve_three_couplings(r):
    for x in r["valid_single_species_witnesses"]:
        assert x["inverse_coupling_residual"]<2e-12
        assert 1e6<x["new_common_mass_GeV"]<1e7
        assert 1e14<x["triple_crossing_mass_GeV"]<3e15
        assert x["new_common_mass_GeV"]<x["triple_crossing_mass_GeV"]

def test_uncertainty_corners_preserve_both_solutions(r):
    assert len(r["single_species_corner_uncertainty_envelopes"])==2
    for x in r["single_species_corner_uncertainty_envelopes"]:
        assert x["specified_electroweak_input_uncertainty_corners"]==8
        assert x["new_mass_GeV_min"]>1e6
        assert x["GUT_scale_GeV_min"]>2e14

def test_not_physical_gut_proof(r):
    for row in r["valid_single_species_witnesses"]:
        assert not row["is_two_loop_or_proton_safe"]
    assert "Proton decay" in r["epistemic_boundary"]

def test_recomputed_data_roundtrip(r):
    x=json.loads((ROOT/"data/toe_20261105_inverse_gauge_threshold_witnesses.json").read_text())
    assert x==json.loads(json.dumps(r))
