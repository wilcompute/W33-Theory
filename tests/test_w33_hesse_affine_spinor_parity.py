from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_hesse_affine_spinor_parity.py"
DATA = ROOT / "data/w33_hesse_affine_spinor_parity.json"


def load():
    spec = importlib.util.spec_from_file_location("w33_hesse_affine_spinor_parity", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_replay():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_affine_character():
    out = json.loads(DATA.read_text())
    g = out["groups"]
    c = out["character"]
    p = out["compiler_reading"]

    assert (g["AGL_order"], g["ASL_order"]) == (432, 216)
    assert c["homomorphism_pairs_checked"] == 432 * 432
    assert (c["trivial_class_elements"], c["nontrivial_class_elements"]) == (216, 216)
    assert c["kernel"] == "ASL(2,3)=F3^2:SL(2,3)"
    assert c["translation_subgroup_in_kernel"] is True
    assert c["orthogonal_image_fibre_size"] == 18

    assert p["unitary_projective_group"] == "ASL(2,3)"
    assert p["extended_affine_group"] == "AGL(2,3)"
    assert p["anti_linear_character"] == 2
    assert p["anti_linear_generator_order"] == 2
    assert all(out["checks"].values())
