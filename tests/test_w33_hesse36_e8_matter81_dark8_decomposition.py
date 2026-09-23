from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_hesse36_e8_matter81_dark8_decomposition.py"
DATA = ROOT / "data/w33_hesse36_e8_matter81_dark8_decomposition.json"


def load():
    spec = importlib.util.spec_from_file_location("dark8", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_replay_matches_frozen_certificate():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_dark8_irreducible_decomposition():
    out = json.loads(DATA.read_text())
    assert out["incidence"]["rank"] == 73
    assert out["incidence"]["dark_dimension"] == 8
    assert out["incidence"]["left_K_invariant"] is True
    assert out["dark_character"]["trace_histogram"] == {
        "-4": 4,
        "-1": 50,
        "2": 24,
        "5": 2,
        "8": 1,
    }
    dec = out["irreducible_decomposition"]
    assert dec["formula"] == "chi_ext + chi_ext^2 + V_omega + V_omega^2"
    assert dec["one_dimensional"] == [
        {"label": [0, 0, 1], "multiplicity": 1},
        {"label": [0, 0, 2], "multiplicity": 1},
    ]
    assert dec["three_dimensional"] == [
        {"central_character_exponent": 1, "external_character_exponent": 0, "multiplicity": 1},
        {"central_character_exponent": 2, "external_character_exponent": 0, "multiplicity": 1},
    ]
    assert dec["conjugation_closed"] is True
    assert all(out["checks"].values())
