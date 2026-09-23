from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_hesse_nullcone_adjoint_intertwiner.py"
DATA = ROOT / "data/w33_hesse_nullcone_adjoint_intertwiner.json"


def load():
    spec = importlib.util.spec_from_file_location("w33_hesse_nullcone_adjoint", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_replay():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_explicit_adjoint_weld():
    out = json.loads(DATA.read_text())
    s = out["sl2_model"]
    a = out["adjoint_lift"]
    n = out["null_cone"]
    r = out["antilinear_reflection"]

    assert s["basis_change_P"] == [[1, 1, 0], [1, 0, 2], [2, 0, 0]]
    assert s["identity"] == "P^T Q_hull P = 2 B_sl2"
    assert n["dictionary_matches_parent_without_relabeling"] is True

    assert a["GL2_order"] == 48
    assert a["SL2_order"] == 24
    assert a["rho_image_order"] == 24
    assert a["rho_kernel"] == ["+I2", "-I2"]
    assert a["rho_image"] == "SO(Q_hull)"
    assert a["SL2_image_order"] == 12
    assert a["all_48_direction_actions_match_rho_null_ray_actions"] is True

    assert r["phase_space_determinant_mod3"] == 2
    assert r["rho_determinant_mod3"] == 1
    assert r["null_ray_permutation"] == [0, 1, 3, 2]
    assert r["permutation_parity"] == "odd"

    assert all(out["checks"].values())
