"""Regress exact all-q CSS and golden Hamada line-rank gap."""
import pytest
from analysis.w33_20261022_hamada_golden_hidden_checks import release,symbolic_case

@pytest.fixture(scope="module")
def result():
    return release()

def test_independent_rref_projective_lines_and_rank(result):
    samples={r["q"]:r for r in result["direct_finite_field_rank_samples"]}
    assert {q:v["direct_line_check_rank_Fp"] for q,v in samples.items()}=={
        2:11,3:30,4:61,5:121,8:401}
    assert {q:v["lines"] for q,v in samples.items()}=={
        2:35,3:130,4:357,5:806,8:4745}

def test_exact_missing_dual_parity_dimensions(result):
    assert {(x["p"],x["t"]):x["independent_checks_missing_from_lines"]
            for x in result["exact_transfer_predictions"]}=={
                (2,1):0,(2,2):8,(2,3):120,(2,4):1312,
                (3,1):0,(3,2):130,(5,1):0,(5,2):3400}
    assert symbolic_case(3,2)["CSS"]==[820,620,10]
    assert symbolic_case(2,3)["CSS"]==[585,457,9]

def test_golden_ratio_is_intrinsic_hamada_transfer(result):
    assert result["characteristic_two_eigenvalues"]==["5+sqrt5","5-sqrt5"]
    assert result["binary_strict_gap_theorem"].startswith("For all t>=2")
    assert result["classical_RH_proved"] is False
    assert "CANNOT" in result["caveat"]
