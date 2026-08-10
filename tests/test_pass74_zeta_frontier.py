"""Pytest suite for Pass 74 -- The Zeta Frontier of W(3,3) (six tracks)."""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass74_zeta_frontier as mod

    mod.main()
    return json.loads(Path("w33_pass74_zeta_frontier.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_A_levi_quadrangle_primes() -> None:
    """Incidence graph girth 8; first primes are oriented quadrangles; pi_G(8)=2*1620."""
    a = _data()["trackA_levi_incidence_zeta"]
    assert a["vertices"] == 80
    assert a["girth"] == 8
    assert a["first_prime_length"] == 8
    assert a["bipartite_ramanujan_modulus_sqrt3"] is True
    assert a["pi_8_oriented_quadrangles"] == 3240
    assert a["ordinary_quadrangles_direct_8cycle_count"] == 1620
    assert a["quadrangle_crosscheck_ok"] is True
    # N_m = 0 for m < girth
    for m in range(1, 8):
        assert a["N_m"][str(m)] == 0


def test_B_explicit_formula_amplitude_is_dim_E6() -> None:
    b = _data()["trackB_explicit_formula"]
    assert b["oscillatory_amplitude"] == 78
    assert b["amplitude_equals_dim_E6"] is True
    assert b["all_match"] is True
    assert abs(b["cos2_gauge_equals_1_over_11"] - 1.0 / 11.0) < 1e-6


def test_C_functional_equation_and_spanning_trees() -> None:
    c = _data()["trackC_functional_equation"]
    assert c["pole_set_invariant_under_involution"] is True
    assert c["all_poles_on_RH_circle"] is True
    assert c["tau_equals_2^81_5^23"] is True
    assert c["spanning_trees_tau"] == (2**81) * (5**23)


def test_D_spence_cospectrality() -> None:
    d = _data()["trackD_spence_cospectrality"]
    assert d["spence_count"] == 28
    assert d["ihara_separates_28"] is False
    assert d["bartholdi_separates_28"] is False
    assert "edge zeta" in d["separator"]


def test_E_irrep_degrees() -> None:
    e = _data()["trackE_artin_ihara_reps"]
    assert e["f_is_irrep_degree"] is True
    assert e["g_is_irrep_degree"] is True


def test_F_weil_point_counts() -> None:
    f = _data()["trackF_weil_vs_ihara"]
    # |W(F_{3^n})| = (3^n+1)(3^{2n}+1)
    for n in range(1, 6):
        assert f["point_counts_F_3n"][str(n)] == (3**n + 1) * (3 ** (2 * n) + 1)
    assert f["point_counts_F_3n"]["1"] == 40
