import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10945_choi_fourier_three_channel_weld.py"
CERT = ROOT / "data/w33_pass10945_choi_fourier_three_channel_weld.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run([sys.executable, str(PRODUCER)], cwd=ROOT, check=True,
                   capture_output=True, text=True, timeout=120)


def test_s1_is_three_localized_nine_history_sectors():
    x = load()
    assert x["status"] == "PASS_CHOI_FOURIER_THREE_CHANNEL_TEMPORAL_WELD"
    s = x["S1_factorization"]
    assert s["dimension"] == 27
    assert s["qutrit_matrix_coefficient_dimension"] == 9
    assert s["external_clock_dimension"] == 3
    assert s["localized_phase_basis_verified"] is True
    w = s["matrix_unit_intertwiner"]
    assert w["verified_matrix_units"] == 9
    assert "E_ir=" in w["formula"]


def test_retyping_quotient_is_three_exact_18_channels():
    q = load()["three_phase_quotient"]
    assert q["identity"] == "54 = 18 + 18 + 18"
    assert [r["S1_intersection_dimension"] for r in q["phase_channels"]] == [9, 9, 9]
    assert [r["quotient_channel_dimension"] for r in q["phase_channels"]] == [18, 18, 18]
    assert set(q["pair_quotient_dimensions"].values()) == {36}
    assert q["full_quotient_dimension"] == 54


def test_pure_welds_are_correlated_graph_subspaces():
    w = load()["weld_geometry"]
    assert w["pure_center_dimension"] == 36
    assert w["pure_external_dimension"] == 36
    assert w["pure_center_external_intersection_dimension"] == 18
    assert w["pure_center_external_span_dimension"] == 54
    assert w["inclusion_exclusion"] == "54 = 36 + 36 - 18"
    for name in ("center", "external"):
        row = w["backgrounds"][name]
        assert set(row["single_phase_projection_ranks"].values()) == {18}
        assert set(row["two_phase_projection_ranks"].values()) == {36}
        assert row["any_two_phases_determine_pure_background"] is True
    for name in ("center_plus_external", "center_minus_external"):
        row = w["backgrounds"][name]
        assert row["total_quotient_rank"] == 54
        assert row["any_two_phases_determine_pure_background"] is False
