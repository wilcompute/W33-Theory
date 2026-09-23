from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_extended_clifford1296_point_stabilizer.py"
DATA = ROOT / "data/w33_extended_clifford1296_point_stabilizer.json"


def load():
    spec = importlib.util.spec_from_file_location("w33_extended_clifford1296", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_replay():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_extended_clifford_structure():
    out = json.loads(DATA.read_text())
    p = out["point_stabilizers"]
    q = out["quotients"]
    z = out["phase_center_semantics"]
    s = out["spinor_parity_lift"]

    assert (p["even_order"], p["full_order"]) == (648, 1296)
    assert p["even_structure"] == "3_+^{1+2}:SL(2,3)"
    assert p["full_structure"] == "3_+^{1+2}:GL(2,3)"
    assert p["heisenberg_order"] == 27
    assert p["GL23_complement_order"] == 48
    assert p["full_center_order"] == 1

    assert q["even_mod_C3"] == "ASL(2,3)"
    assert q["full_mod_C3"] == "AGL(2,3)"
    assert (q["even_mod_C3_order"], q["full_mod_C3_order"]) == (216, 432)
    assert q["quotient_action_equals_explicit_AGL9"] is True

    assert z["C3_central_in_even_648"] is True
    assert z["C3_normal_in_full_1296"] is True
    assert z["C3_central_in_full_1296"] is False
    assert z["det_minus_one_action"] == "z -> z^2"

    assert (s["trivial_class_size"], s["nontrivial_class_size"]) == (648, 648)
    assert all(out["checks"].values())
