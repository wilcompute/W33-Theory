"""Round12 independent reproducibility audit for five requested tracks."""
from __future__ import annotations
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
@pytest.fixture(scope="module")
def central():
    from w33_20261019_round12_central_spectrum import run
    return run()
@pytest.fixture(scope="module")
def m2():
    from w33_20261019_round12_M2_representations import run
    return run()
@pytest.fixture(scope="module")
def peirce():
    from w33_20261019_round12_peirce_27_map import run
    return run()
@pytest.fixture(scope="module")
def fullmap():
    from w33_20261019_round12_full_octonion_intertwiner import run
    return run()
@pytest.fixture(scope="module")
def exact7():
    from w33_20261019_round12_exact_rational_heptad_counterexample import run
    return run()
def test_all_eight_rational_primitive_central_idempotents(central):
    assert central["all_checks_pass"]
    assert central["rational_split_generating_central_element_found"]
    assert sorted(central["central_idempotents_regular_ranks"])==[1]*5+[4]*3
def test_explicit_three_rational_2_by_2_matrix_representations(m2):
    assert m2["all_checks_pass"]
    assert m2["rational_2x2_blocks_found"]==3
    assert all(len(x["matrices_17_of_2x2"])==17 for x in m2["rank_four_factors"])
def test_invertible_nonmonomial_peirce_map(peirce):
    assert peirce["all_checks_pass"]
    assert peirce["complex_determinant"]=="-4096"
    assert peirce["cross_octet_nonzero_monomials"]==64
def test_entire_firstTits_to_CayleyDickson_cubic_exact(fullmap):
    assert fullmap["all_checks_pass"]
    assert fullmap["determinant"]=="-4096"
    assert fullmap["checks"]["all_64_octonion_trilinear_coefficients_equal_exact"]
def test_rational_certified_global_boundary_counterexample_T1(exact7):
    assert exact7["all_checks_pass"]
    assert exact7["strict_partition_gap_lower_float"]>.009
    assert exact7["numerical_energy_gap_estimate"]<-.0007
def test_40_active_direction_SLSQP_feasible_comparison():
    from w33_20261019_round12_global_phase_multistart import run
    d=run()
    assert d["all_checks_pass"]
    assert len(d["cases"])==6
    witness=next(x for x in d["cases"] if x["T"]==1. and x["offset_above_local"]==0.)
    assert witness["best_feasible"]["E_gap"]<-.0007
def test_optical_heldout_rejection_and_signal():
    from w33_20261019_round12_optical_falsification import run
    d=run()
    assert d["all_checks_pass"]
    assert d["held_out_null"]["false_positive_count"]==0
    assert d["held_out_signal"]["detected_count"]==100
    assert d["total_source_photons_per_trial"]==810000
def test_compact_gauge_ghost_free_quadratic_but_not_protected_chiral():
    from w33_20261019_round12_compactE7_chiral_mass import run
    d=run()
    assert d["all_checks_pass"]
    assert d["total_bosonic_modes"]==384
    assert d["checks"]["symmetric_nondegenerate_mass_tensor_on_56_tensor_2"]
