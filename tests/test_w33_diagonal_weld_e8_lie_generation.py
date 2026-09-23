from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_diagonal_weld_e8_lie_generation.py"
DATA = ROOT / "data/w33_diagonal_weld_e8_lie_generation.json"


def load():
    spec = importlib.util.spec_from_file_location("diagonal_weld_e8_generation", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_replay():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_diagonal_phase_is_the_full_generation_switch():
    out = json.loads(DATA.read_text())
    grid = out["dimension_grid_mod_103"]
    diagonal = {"plus", "minus"}
    for left, row in grid.items():
        for right, dimension in row.items():
            assert dimension == (248 if left in diagonal or right in diagonal else 24)
    theorem = out["theorem"]
    assert theorem["all_nondiagonal_pairs_same_subspace"] is True
    assert theorem["matched_diagonal_orientation_required"] is False
    assert theorem["one_diagonal_correlation_is_sufficient"] is True
    assert all(out["checks"].values())
