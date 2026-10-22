"""Eight exact PG(3,4) hyperovals close the classical dual rank gap."""
import pytest
from analysis.w33_20261022_q4_hyperoval_dual_completion import release,HYPEROVALS

@pytest.fixture(scope="module")
def packet():
    return release()

def test_complete_q4_dual_from_lines_and_hyperovals(packet):
    assert packet["status"]=="PASS_EXACT_HYPEROVAL_COMPLETION"
    assert packet["line_check_rank"]==61
    assert packet["added_hyperoval_words"]==8
    assert packet["line_plus_hyperoval_rank"]==69
    assert packet["full_noncollinearity_dual_dimension"]==69
    assert packet["classical_RH_proved"] is False

def test_each_witness_is_plane_hyperoval_and_independent(packet):
    assert len(HYPEROVALS)==8 and len(set(HYPEROVALS))==8
    for r in packet["independent_hyperovals"]:
        assert r["weight"]==6
        assert r["new_independent_direction"]
        assert sum(r["line_intersection_histogram"].values())==21
        assert r["line_intersection_histogram"]["2"]==15
        assert r["line_intersection_histogram"]["0"]==6

def test_classical_quantum_check_distinction(packet):
    assert packet["line_parity_check_weight"]==5
    assert packet["hyperoval_parity_check_weight"]==6
    assert "not automatically" in packet["hardware_boundary"]
