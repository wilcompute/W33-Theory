"""Pytest suite for Pass 87 -- Construction A lattice theta series of C_2(W)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass87_theta_lattice as mod

    mod.main()
    return json.loads(Path("w33_pass87_theta_lattice.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_even_rank40_weight20() -> None:
    d = _data()
    assert d["lattice_rank"] == 40
    assert d["even_lattice"] is True
    assert d["modular_form_weight"] == 20


def test_theta_low_coefficients() -> None:
    theta = {int(k): v for k, v in _data()["theta_q_expansion"].items()}
    assert theta[0] == 1
    assert theta[4] == 80  # +-2 e_i, = 2n
    assert theta[8] == 14640
    # no small-norm vectors of norm 1,2,3
    assert all(theta.get(k, 0) == 0 for k in (1, 2, 3))


def test_norm8_encodes_45_tritangent_planes() -> None:
    b = _data()["norm8_breakdown"]
    assert b["from_weight8_codewords"] == 45 * 2**8  # 11520
    assert b["total"] == 14640
    assert b["matches_theta"] is True
