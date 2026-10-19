"""Regression for five independent W33 Round6 research fronts."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
def test_E8_matter_branch_lift_and_mu_origin():
    from w33_20261019_round6_matter_lift_branch import run
    d=run()
    assert d["all_checks_pass"]
    assert d["dimension_1_27_54"]==[3,27,54]
    assert d["max_energy_origin_shift_residual"]<1e-10
def test_all_heptads_clifford_transitive_and_translation_quotient():
    from w33_20261019_round6_heptad_symmetry import out
    assert out["all_checks_pass"]
    assert out["orbit_heptads"]==2880
    assert out["number_translation_cosets"]==27
    assert sorted(c["size"] for c in out["five_spectral_families"])==[81,162,486,486,972]
def test_18_mode_CZ_F3_optical_mesh_and_loss():
    from w33_20261019_round6_optics_component_budget import run
    d=run()
    assert d["all_checks_pass"]
    assert d["component_budget"]["full_W_tunable_SU2_couplers_upper_bound"]==36
    assert d["full_G_9mode_reconstruction_error"]<1e-12
def test_normalized_E8_chevalley_full_root_system():
    import json
    from w33_20261019_round6_chevalley_realform import run
    run()
    d=json.loads((ROOT/"data/w33_20261019_round6_chevalley_realform.json").read_text())
    assert d["all_checks_pass"]
    assert d["rank_of_generated_root_vectors_and_h"]==248
    assert d["positive_roots_generated"]==d["negative_roots_generated"]==120
    assert d["cartan_determinant"]==1
def test_absolute_scale_nonidentifiability():
    import json
    from w33_20261019_round6_scale_nogo import run
    run()
    d=json.loads((ROOT/"data/w33_20261019_round6_scale_nogo.json").read_text())
    assert d["all_checks_pass"]
    assert max(row["unitary_time_scaling_residual"] for row in d["rescaling_factors"])<1e-10


def test_exact_integer_characteristic_polynomials_for_27_orbits():
    from w33_20261019_round6_heptad_exact_charpoly import run
    d=run()
    assert d["all_checks_pass"]
    assert d["checks"]["all_27_translation_cosets_exactly_classified"]
    assert len(d["exact_27_translation_orbit_polynomial_multiplicities"])==5
    assert sorted(x["orbit_count"] for x in d["exact_27_translation_orbit_polynomial_multiplicities"])==[1,2,6,6,12]
