"""Pytest suite for Pass 73 -- Prime Geodesic Spectrum of W(3,3)."""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _run_and_load(module_name: str, output_file: str) -> dict:
    import importlib

    mod = importlib.import_module(module_name)
    mod.main()
    return json.loads(Path(output_file).read_text(encoding="utf-8"))


def _data() -> dict:
    return _run_and_load(
        "w33_pass73_prime_geodesics", "w33_pass73_prime_geodesics.json"
    )


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_srg_graph() -> None:
    g = _data()["graph"]
    assert (g["n"], g["k"], g["lambda"], g["mu"]) == (40, 12, 2, 4)
    assert g["spectrum"] == {"12": 1, "2": 24, "-4": 15}
    assert g["srg_verified"] is True


def test_hashimoto_dimensions() -> None:
    h = _data()["hashimoto"]
    assert h["arcs"] == 480
    assert h["edges"] == 240
    assert h["genus_rank_EminusV"] == 200
    assert h["bass_spectrum_ok"] is True
    assert h["all_nontrivial_modulus_sqrt11"] is True


def test_length3_prime_count_is_320_not_160() -> None:
    """The correction: pi_G(3) = 2T = 320 (oriented triangles), not the triangle count 160."""
    d = _data()
    assert d["pi_primes"]["3"] == 320
    tc = d["triangle_crosscheck"]
    assert tc["triangles"] == 160
    assert tc["expected_2x"] == 320
    assert tc["ok"] is True
    # forced by N_3 = tr(B^3) = 960 = 3 * pi_G(3)
    assert d["N_m_trace_Bm"]["3"] == 960
    assert 3 * d["pi_primes"]["3"] == d["N_m_trace_Bm"]["3"]


def test_prime_counts_are_positive_integers_and_mobius_consistent() -> None:
    d = _data()
    N = {int(k): v for k, v in d["N_m_trace_Bm"].items()}
    pi = {int(k): v for k, v in d["pi_primes"].items()}

    def mobius(k: int) -> int:
        if k == 1:
            return 1
        res, kk, p = 1, k, 2
        while p * p <= kk:
            if kk % p == 0:
                kk //= p
                if kk % p == 0:
                    return 0
                res = -res
            p += 1
        return -res if kk > 1 else res

    for m in range(3, 13):
        s = sum(mobius(m // d0) * N[d0] for d0 in range(1, m + 1) if m % d0 == 0)
        assert s % m == 0
        assert s // m == pi[m]
        assert pi[m] >= 0


def test_graph_pnt_ratio_converges() -> None:
    ratios = _data()["graph_PNT_ratio"]
    # pi_G(m) * m / 11^m -> 1
    assert abs(ratios["12"] - 1.0) < 0.01
    assert abs(ratios["9"] - 1.0) < 0.01


def test_ramanujan_error_bound_holds() -> None:
    d = _data()["ramanujan_error_bound"]
    assert d["all_hold"] is True
    for row in d["rows"]:
        assert row["residual"] <= row["bound"] + 1e-6


def test_mixing_gap() -> None:
    mx = _data()["mixing"]
    assert mx["perron"] == 11
    assert abs(mx["second_modulus"] - math.sqrt(11)) < 1e-6
