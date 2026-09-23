from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_e8_full_graded_hybrid_atlas.py"
DATA = ROOT / "data/w33_e8_full_graded_hybrid_atlas.json"


def load():
    spec = importlib.util.spec_from_file_location("full_graded_hybrid", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_replay():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_root_ordered_graded_atlas_contract():
    out = json.loads(DATA.read_text())
    assert out["grading"]["dimensions"] == {"g0":86,"g1":81,"g2":81,"total":248}
    assert out["atlas"]["block_ranks"] == [86,81,81]
    assert out["atlas"]["rank"] == 248
    assert out["grading"]["FI_center_trace"] == "5"
    rows = out["matter_root_row_order"]
    assert len(rows["K_address_order"]) == 81
    assert len(rows["grade1_root_rows"]) == 81
    assert len(rows["grade2_root_rows"]) == 81
    assert all(
        [str(-Fraction(value)) for value in grade1] == grade2
        for grade1, grade2 in zip(rows["grade1_root_rows"], rows["grade2_root_rows"])
    )
    assert all(out["checks"].values())
