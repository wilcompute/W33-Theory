from fractions import Fraction
from pathlib import Path

from scripts.w33_e6_sm_burden_of_proof_bridge import build_bridge


ROOT = Path(__file__).resolve().parents[1]


def test_summary_core_counts():
    payload = build_bridge()
    s = payload["summary"]

    assert s["gauge_algebra_dimension"] == 12
    assert s["harmonic_dimension"] == 81
    assert s["generation_count"] == 3
    assert s["e6_fundamental_dimension"] == 27
    assert s["so10_plus_u1_branch_sum"] == 27


def test_exact_anomaly_zeroes():
    payload = build_bridge()
    a = payload["anomalies_per_generation"]

    for key in ["su3_sq_u1", "su2_sq_u1", "u1_cubed", "grav_sq_u1"]:
        val = Fraction(a[key]["num"], a[key]["den"])
        assert val == 0


def test_all_bridge_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True


def test_public_index_exposes_burden_bridge():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Toroidal Markov / E6" in text
    assert "512x^3 - 168x - 7" in text
    assert "27 = 16 + 10 + 1" in text
    assert "81 = 3&times;27" in text
