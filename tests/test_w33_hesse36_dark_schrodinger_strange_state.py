from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_hesse36_dark_schrodinger_strange_state.py"
DATA = ROOT / "data/w33_hesse36_dark_schrodinger_strange_state.json"


def load():
    spec = importlib.util.spec_from_file_location("dark_strange", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_replay_matches_frozen_certificate():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_dark_strange_bridge_and_m36_firewall():
    out = json.loads(DATA.read_text())
    assert out["qutrit_convention"]["stacked_projector_rank"] == 2
    assert out["qutrit_convention"]["common_kernel_dimension"] == 1
    assert out["dark_multiplicity_ray"]["unnormalized"] == ["1","-omega","0"]
    assert out["strange_bridge"]["exact_Clifford_word"] == "Z X^2"
    assert out["strange_bridge"]["same_projective_Clifford_orbit"] is True
    assert out["dark8_reading"]["formula"] == "chi_ext + chi_ext^2 + V_omega + V_omega^2"
    assert out["M36_firewall"]["same_resource_as_M36_Q4_RAW"] is False
    assert out["M36_firewall"]["M36_injection_boundary_changed"] is False
    assert all(out["checks"].values())
