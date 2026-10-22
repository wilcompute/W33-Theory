"""Five scoped Oct 22 RH research tracks: exact all-prime-family and numerical audits."""
import pytest
from analysis.w33_20261022_levi_prime_family import (
    certificate as prime_certificate,local_packet,count_fp,count_fp2
)
from analysis.w33_20261022_ccm_compact_weil_trace import (
    certificate as analytic_certificate,prime_powers,kernel as ccm_kernel
)

@pytest.fixture(scope="module")
def arithmetic():
    return prime_certificate()

@pytest.fixture(scope="module")
def analytic():
    return analytic_certificate()

def test_infinite_prime_family_and_frobenius_samples(arithmetic):
    assert arithmetic["status"]=="PASS_EXACT_LOCAL"
    assert arithmetic["classical_RH_proved"] is False
    assert [p["local_cohomology_rank"] for p in arithmetic["samples"]]==[156,1596,50876]
    assert [(p["C_points_Fp"],p["C_points_Fp2"]) for p in arithmetic["samples"]]==[
        (4,10),(8,50),(24,530)]

def test_local_galois_congruence_and_fixed_rank_obstruction(arithmetic):
    assert local_packet(7,False)["quadratic_exponent"]==350
    with pytest.raises(AssertionError):local_packet(11,False)
    assert "ONE fixed-rank global motive" in arithmetic["global_obstruction"]
    assert "noncanonically" in arithmetic["local_Galois"]

def test_true_finite_prime_CCM_operator(analytic):
    data=analytic["finite_prime_CCM"]
    assert data["prime_powers"]==[2,3,4,5,7,8,9,11,13]
    assert data["dimension"]==9 and data["cutoff"]==13
    assert data["smallest_eigenvector_parity"]>0.999999
    assert abs(data["predicted_first_ordinate"]-data["actual_first_ordinate"])<0.0002
    # Differentiate genuine source kernel formula against diagonal n=0.
    assert ccm_kernel(__import__("math").log(13),0,0,0)==2

def test_two_smooth_compact_completed_Weil_functions(analytic):
    data=analytic["smooth_compact_Weil"]
    assert data["smooth_C_infinity"]
    assert data["exact_prime_tail_zero"]
    assert data["eigenvalues"][0]>1e-7
    assert data["eigenvalues"][1]>0.02
    assert "von_Mangoldt" in data["contribution_parts"]["0,0"]

def test_rank_two_relative_trace_not_automatically_Xi(analytic):
    data=analytic["W33_relative_trace"]
    assert data["exact_dark_modes"]==37
    assert abs(data["relative_trace2"]-data["relative_trace2_theory"])<1e-7
    assert abs(data["relative_trace3"]-data["relative_trace3_theory"])<1e-5
    assert len(data["determinant_ratios"])==2
    assert all(abs(r["full"]-r["Schur"])<1e-8 for r in data["determinant_ratios"])
    assert analytic["classical_RH_proved"] is False
