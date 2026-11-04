"""Operational audits of Witting 440-root codebook information, Holevo cap,
all40 native tetrad measurements, and a seeded nonoptimal Haar basis search."""
import importlib.util,sys,math
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/"analysis") not in sys.path:sys.path.insert(0,str(ROOT/"analysis"))
def run(name,filename):
    s=importlib.util.spec_from_file_location(name,ROOT/"analysis"/filename)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    return m.main()
@pytest.fixture(scope="module")
def capacity():
    return run("holevo_probe","toe_20261104_two_e8_witting_holevo_capacity_scan.py")
@pytest.fixture(scope="module")
def basis():
    return run("basis_probe","toe_20261104_two_e8_witting_basis_information_search.py")

def test_holevo_bound_is_ensemble_specific_and_much_below_2_bits(capacity):
    assert capacity["uniform_prior_root_labels"]==440
    assert capacity["coarse_Hilbert_dimension_Holevo_ceiling_bits"]==2
    assert 0.05<capacity["baseline_epsilon_point_one_Holevo_upper_bound_bits"]<.07
    assert capacity["baseline_epsilon_point_one_Witting_information_bits"]<capacity["baseline_epsilon_point_one_Holevo_upper_bound_bits"]

def test_uniform_antipodal_average_and_positivity_scan(capacity):
    assert len(capacity["epsilon_scan"])==6
    for r in capacity["epsilon_scan"]:
        if r["all_440_PSD"]:
            assert r["average_state_is_exact_maximally_mixed"]
            assert r["holevo_bound_bits_per_ququart"]>r["fixed_Witting_POVM_information_bits_per_detected_photon"]>0

def test_encoding_epsilon_02_fourfold_information_increase(capacity):
    assert capacity["epsilon_point_two_Witting_information_bits"]>4*capacity["baseline_epsilon_point_one_Witting_information_bits"]
    assert capacity["epsilon_point_two_Fano_necessary_detected_photons"]==170
    assert abs(capacity["baseline_Witting_information_fraction_of_Holevo"]-.1967106665172878)<1e-10

def test_every_witting_tetrad_equal_information_under_uniform_440root_prior(basis):
    for row in basis["epsilon_scan"]:
        infos=row["all_40_native_Witting_tetrad_information_bits"]
        assert len(infos)==40
        assert max(infos)-min(infos)<1e-10
        assert abs(row["uniform_Witting40_POVM_information_bits"]-sum(infos)/40)<1e-10
    assert basis["uniform_random_Witting_tetrad_with_basis_label_equals_full_POVM_information"]

def test_seeded_haar_basis_comparison_is_reproducible_and_not_optimality_claim(basis):
    assert len(basis["epsilon_scan"])==2
    for row in basis["epsilon_scan"]:
        assert not row["global_optimum_claimed"]
        assert row["sampled_Haar_basis_count"]==320
        assert row["seeded_Haar_best_information_bits"]>row["uniform_Witting40_POVM_information_bits"]
        assert row["seeded_Haar_best_information_bits"]<2
        assert len(row["best_sampled_Haar_unitary_rows_real"])==4
        assert len(row["best_native_tetrad_ray_labels"])==4

def test_two_information_producers_agree_at_both_epsilons(capacity,basis):
    for b in basis["epsilon_scan"]:
        a=next(x for x in capacity["epsilon_scan"] if x["epsilon"]==b["epsilon"])
        assert abs(a["fixed_Witting_POVM_information_bits_per_detected_photon"]-b["uniform_Witting40_POVM_information_bits"])<1e-10
