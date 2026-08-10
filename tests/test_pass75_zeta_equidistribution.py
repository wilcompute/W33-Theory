"""Pytest suite for Pass 75 -- four even-better zeta ideas."""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass75_zeta_equidistribution as mod

    mod.main()
    return json.loads(Path("w33_pass75_zeta_equidistribution.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_T1_polygon_pairing() -> None:
    t1 = _data()["track1_polygon_pairing"]
    assert t1["collinearity_girth"] == 3
    assert t1["incidence_girth"] == 8
    assert t1["gonality_from_incidence_girth"] == 4
    assert t1["polygon_primes"]["triangle_length3"]["pi_G"] == 320
    assert t1["polygon_primes"]["quadrangle_length8"]["pi_G"] == 3240


def test_T2_equidistribution() -> None:
    t2 = _data()["track2_equidistribution"]
    # non-monic minimal polynomial => not a root of unity => irrational multiple of pi
    assert t2["unit_phase_minpoly_121u4_198u2_121"][0] == 121
    assert t2["unit_phase_is_algebraic_integer"] is False
    assert t2["theta_is_irrational_multiple_of_pi"] is True
    assert t2["alpha_returns_to_1_within_200"] == []
    assert t2["discrepancy_bounded_by_1"] is True
    assert t2["discrepancy_max_abs_R_over_40"] <= 1.0


def test_T3_edge_zeta_separation() -> None:
    t3 = _data()["track3_edge_zeta_separation"]
    assert t3["both_SRG_16_6_2_2"] is True
    assert t3["cospectral"] is True
    # identical Ihara N_m -> zeta cannot hear them
    assert t3["ihara_zeta_identical"] is True
    assert t3["ihara_N_m_rook"] == t3["ihara_N_m_shrikhande"]
    # local neighbourhood 2K3 vs C6 -> non-isomorphic, edge zeta separates
    assert t3["neighbourhood_spectrum_rook_2K3"] == {"-1": 4, "2": 2}
    assert t3["neighbourhood_spectrum_shrikhande_C6"] == {
        "-2": 1,
        "-1": 2,
        "1": 2,
        "2": 1,
    }
    assert t3["local_structure_differs"] is True


def test_T4_dim_E6_amplitude() -> None:
    t4 = _data()["track4_dim_E6_amplitude"]
    assert t4["f_plus_g"] == 39
    assert t4["f_plus_g_equals_v_minus_1"] is True
    assert t4["amplitude_2(f+g)"] == 78
    assert t4["closed_form_2q(q^2+q+1)"] == 78
    assert t4["equals_dim_E6"] is True
    assert t4["f_g_are_PSp43_irrep_degrees"] is True
