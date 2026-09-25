import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10952_clock_complete_positivity_firewall.py"
CERT = ROOT / "data/w33_pass10952_clock_complete_positivity_firewall.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run(
        [sys.executable, str(PRODUCER)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert load()["status"] == "PASS_CLOCK_COMPLETE_POSITIVITY_FIREWALL"
def test_single_tick_is_positive_tp_but_not_cp():
    c = load()["complete_positivity_firewall"]
    assert c["single_tick_positive"] is True
    assert c["single_tick_trace_preserving"] is True
    assert c["single_tick_completely_positive"] is False
    assert c["single_tick_choi_inertia_pos_neg_zero"] == [6, 3, 0]
    assert c["single_tick_choi_eigenvalues"] == [-1.0] * 3 + [1.0] * 6
    expected = [-1 / 3] * 3 + [1 / 3] * 6
    assert all(
        abs(a - b) < 1e-11
        for a, b in zip(c["reference_Bell_output_eigenvalues"], expected)
    )


def test_all_eight_powers_have_exact_cp_parity():
    rows = load()["complete_positivity_firewall"]["all_eight_powers"]
    assert [r["power"] for r in rows] == list(range(8))
    for row in rows:
        if row["power"] % 2 == 0:
            assert row["completely_positive"] is True
            assert row["choi_inertia_pos_neg_zero"] == [1, 0, 8]
        else:
            assert row["completely_positive"] is False
            assert row["choi_inertia_pos_neg_zero"] == [6, 3, 0]
def test_even_subgroup_is_physical_c4():
    e = load()["even_tick_physical_subgroup"]
    assert e["two_tick_unitary"] is True
    assert e["two_tick_channel_projective_order"] == 4
    assert e["four_tick_phase_space_matrix"] == "-I2"
    assert e["four_tick_is_scalar"] is False
    assert abs(e["four_tick_scalarity_abs_trace_over_3"] - 1 / 3) < 1e-8
    assert e["eight_tick_scalar_identity_error"] < 1e-8


def test_representation_firewall():
    r = load()["representation_firewall"]
    assert "scalar -1" in r["spin_representation"]
    assert "non-scalar parity Clifford" in r["qutrit_Clifford_representation"]
    assert "central-character statement" in r["consequence"]


def test_doubled_conjugate_sector_restores_unitary_z8():
    d = load()["doubled_conjugate_sector_escape"]
    assert d["carrier_dimension"] == 6
    assert d["unitarity_error"] < 1e-8
    assert d["projective_order"] == 8
    assert d["square_block_error"] < 1e-8
def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(
        encoding="utf-8"
    )
    assert docs.count('id="pass10952-clock-complete-positivity"') == 1
    assert tail.count(
        "PASS10952_CLOCK_COMPLETE_POSITIVITY_FIREWALL_INSERT}%"
    ) == 1
