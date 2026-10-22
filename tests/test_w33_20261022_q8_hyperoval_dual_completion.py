"""120 seeded q8 plane hyperovals span all 120 missing dual-check dimensions."""
import pytest
from analysis.w33_20261022_q8_hyperoval_dual_completion import release

@pytest.fixture(scope="module")
def packet():
    return release()

def test_all_q8_hidden_dual_checks_generated(packet):
    assert packet["status"]=="PASS_EXACT_Q8_HYPEROVAL_COMPLETION"
    assert packet["classical_dual_dim"]==521
    assert packet["line_check_rank"]==401
    assert packet["independent_hyperovals"]==120
    assert packet["completed_dual_rank"]==521
    assert packet["classical_RH_proved"] is False

def test_each_orbit_witness_has_ten_distinct_points_and_frozen_hash(packet):
    assert len(packet["witness_coordinate_supports"])==120
    assert all(len(row)==len(set(row))==10 for row in packet["witness_coordinate_supports"])
    assert packet["ordered_witness_sha256"]=="a5a43a18acc15681c9976d1666f35a5687e7caf0293ec961c868966a0e946113"
    assert packet["shear_steps"]==128

def test_classical_and_CSS_roles_are_not_conflated(packet):
    assert packet["line_check_weight"]==9
    assert packet["hyperoval_check_weight"]==10
    assert packet["noncollinearity_rank"]==64
    assert "do not confuse" in packet["physical_boundary"]
