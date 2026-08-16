from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass5586_binary_psl2_permutation_span_rank.py"


def load_module():
    spec = importlib.util.spec_from_file_location("pass5586", SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_symbolic_image_algebra_formula():
    mod = load_module()
    for q in (3, 5, 7, 9, 11, 13, 25, 27, 49, 81):
        row = mod.symbolic_row(q)
        assert row["image_algebra_dimension"] == (q + 1) ** 2 // 2
        assert row["jacobson_radical_dimension"] == 2 * q - 1


def test_prime_field_replay_matches_theorem():
    mod = load_module()
    pass5580 = mod.load_pass5580()
    for q in (3, 5, 7, 11, 13):
        measured = pass5580.analyse(q)["binary_rank_measured"]
        assert measured == mod.symbolic_row(q)["target_binary_rank"]
