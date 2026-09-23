from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_hesse_nullcone_spinor_norm.py"
DATA = ROOT / "data/w33_hesse_nullcone_spinor_norm.json"


def load():
    spec = importlib.util.spec_from_file_location("w33_hesse_spinor_norm", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_replay():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_determinant_spinor_character_weld():
    out = json.loads(DATA.read_text())
    s = out["spinor_norm"]
    c = out["character_weld"]
    k = out["antilinear_reflection"]

    assert s["SO_order"] == 24
    assert s["trivial_class_count"] == 12
    assert s["nontrivial_class_count"] == 12
    assert s["every_SO_element_has_two_reflection_decomposition"] is True
    assert s["all_decompositions_consistent"] is True

    assert c["GL2_elements_checked"] == 48
    assert c["rho_image_elements_checked"] == 24
    assert c["kernel_spinor_norm_order"] == 12
    assert c["kernel_equals_SL2_image_mod_center"] is True

    assert k["det_kappa_mod3"] == 2
    assert k["det_rho_kappa_mod3"] == 1
    assert k["spinor_norm_rho_kappa"] == 2
    assert k["null_ray_permutation"] == [0, 1, 3, 2]
    assert k["explicit_reflection_factorization"]["spinor_product"] == 2

    assert all(out["checks"].values())
