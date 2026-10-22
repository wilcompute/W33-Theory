"""Prime-power symplectic-code theorem tests, exact over defining characteristic."""
import pytest
from analysis.w33_20261022_allq_pascal_CSS_exact_distance import case,release

@pytest.fixture(scope="module")
def packet():
    return release()

def test_all_six_css_dimensions_and_distances(packet):
    assert packet["classical_RH_proved"] is False
    assert [(z["q"],z["CSS"]["n"],z["CSS"]["k"],z["CSS"]["distance"]) for z in packet["cases"]]==[
        (2,15,7,3),(3,40,20,4),(4,85,53,5),
        (5,156,86,6),(8,585,457,9),(9,820,620,10)]

def test_hyperplane_isolation_proof_and_line_logical(packet):
    for row in packet["cases"]:
        q=row["q"]
        assert row["line_check_in_kernel_B"]
        assert row["line_not_in_stabilizer_row_B"]
        assert row["all_rows_weight"]==q**3
        assert row["line_logical_word_weight"]==q+1
        assert row["uncovered_hyperplane_union_bound"]==1
        assert row["isolating_hyperplane_lower_bound"]==q+2
        assert len(row["sample_support_q_isolating_H_indices"])==q

def test_q4_short_support_exhaustive_binary_control(packet):
    q4=next(x for x in packet["cases"] if x["q"]==4)
    assert q4["q4_all_dual_weights_below5_excluded_by_xor"] is True

def test_existing_w33_css_code_and_new_q9_case(packet):
    q3=next(x for x in packet["cases"] if x["q"]==3)
    q9=next(x for x in packet["cases"] if x["q"]==9)
    assert q3["CSS"]=={"n":40,"k":20,"distance":4,"symbol_field":"F_3"}
    assert q9["CSS"]=={"n":820,"k":620,"distance":10,"symbol_field":"F_3"}
