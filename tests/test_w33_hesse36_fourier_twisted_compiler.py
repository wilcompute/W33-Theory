from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_hesse36_fourier_twisted_compiler.py"
DATA = ROOT / "data/w33_hesse36_fourier_twisted_compiler.json"


def load():
    spec = importlib.util.spec_from_file_location("hesse36_fourier_compiler", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_replay_matches_frozen_certificate():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_exact_fourier_twisted_compiler_contract():
    out = json.loads(DATA.read_text())
    assert out["status"] == "PASS_EXACT_36D_FOURIER_TWISTED_SL23_COMPILER"
    assert out["group"]["G"] == "SL(2,3)"
    assert out["group"]["ordinary_orbits"] == [4, 4, 4, 24]
    assert out["group"]["safe_orbits"] == [4, 4, 4, 8, 8, 8]
    assert out["group"]["common_safe8_stabilizer_order"] == 3
    compiler = out["compiler"]
    assert compiler["rank"] == 36
    assert compiler["nonzero_entry_count"] == 84
    assert compiler["column_support_profile"] == {"1": 12, "3": 24}
    assert compiler["column_squared_norm_profile"] == {"1": 12, "3": 24}
    assert len(compiler["target_column_to_source_rows_and_omega_exponents"]) == 36
    assert compiler["exact_intertwining_checks"] == 24
    assert compiler["exact_group_law_checks"] == 20736
    rep = out["representation_character"]
    assert rep["untwisted_order3_trace_before"] == 9
    assert rep["twisted_order3_trace_after"] == 3
    assert rep["ordinary_order3_trace"] == 3
    assert rep["twisted_target_equals_ordinary_source"] is True
    assert all(out["checks"].values())
