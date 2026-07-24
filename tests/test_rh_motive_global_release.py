from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp

from analysis.w33_all_prime_frobenius_census import build_census
from analysis.w33_fixed_E_debranges_falsifier import E_fixed, hb_gap, perturbed_E
from analysis.w33_motivic_24_15_packet import I, P12, P2, PM4, add, multiply, trace
from analysis.w33_renormalized_boundary_formula import (
    completed_direct_difference,
    completed_finite_part,
)

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATES = (
    "w33_motivic_24_15_packet_certificate.json",
    "w33_all_prime_frobenius_census_certificate.json",
    "w33_renormalized_boundary_formula_certificate.json",
    "w33_fixed_E_debranges_falsifier_certificate.json",
    "w33_preregistered_higher_moment_search_certificate.json",
)


def load(name: str) -> dict:
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def test_all_release_certificates_pass():
    for name in CERTIFICATES:
        payload = load(name)
        assert payload["status"] == "PASS", name
        assert all(payload["checks"].values()), name


def test_exact_1_24_15_projectors():
    assert multiply(P12, P12) == P12
    assert multiply(P2, P2) == P2
    assert multiply(PM4, PM4) == PM4
    assert multiply(P2, PM4) == (0, 0, 0)
    assert add(add(P12, P2), PM4) == I
    assert [int(trace(x)) for x in (P12, P2, PM4)] == [1, 24, 15]


def test_frobenius_census_replay_lock():
    rows, summary = build_census()
    assert len(rows) == 1229
    assert summary["W33_signature"]["matching_primes"] == [11]
    p5 = next(row for row in rows if row["p"] == 5)
    assert (int(p5["E_2_a_p"]), int(p5["E_-4_a_p"])) == (-3, 2)


def test_boundary_finite_part_identity():
    mp.mp.dps = 50
    for delta in (mp.mpf("0.01"), mp.mpf("0.2"), mp.mpf("0.4")):
        assert abs(completed_finite_part(delta) - completed_direct_difference(delta)) < mp.mpf("1e-40")
        assert completed_finite_part(delta) > 0


def test_fixed_E_falsifier_is_sensitive():
    mp.mp.dps = 45
    assert hb_gap(E_fixed, mp.mpc("14", "0.15")) > 0
    defective = perturbed_E(mp.mpf("0.2"), mp.mpf("14"))
    assert hb_gap(defective, mp.mpc("14", "0.15")) < 0


def test_pre_registered_reserved_moments_fail():
    payload = load("w33_preregistered_higher_moment_search_certificate.json")
    signed = payload["signed_exact_interpolation"]
    positive = payload["positive_constrained_search"]
    assert min(signed["weights_s2_s3_s4"]) < 0
    assert float(signed["relative_errors"]["10"]) > 0.2
    assert float(signed["relative_errors"]["12"]) > 1.0
    assert float(positive["relative_errors"]["10"]) > 0.7
    assert float(positive["relative_errors"]["12"]) > 3.0


def test_rank_78_bridge_matches_pass637_count_without_promoting_map():
    motive = load("w33_motivic_24_15_packet_certificate.json")
    assert motive["motivic_candidate"]["rank"] == 78
    assert motive["motivic_candidate"]["degree"] == 78
