from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_affine_holonomy_vm_code_architecture.py"
DATA = ROOT / "data/w33_affine_holonomy_vm_code_architecture.json"


def load():
    spec = importlib.util.spec_from_file_location("affine_holonomy_vm", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_replay():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_vm_code_and_automorphism_contract():
    out = json.loads(DATA.read_text())
    assert out["encoder"]["logical_line_trits"] == 12
    assert out["encoder"]["affine_holonomy_check_trits"] == 9
    assert out["codes"]["full"]["parameters"] == "[45,12,6]_3"
    assert out["codes"]["punctured_core"]["parameters"] == "[21,12,4]_3"
    assert out["codes"]["dual"]["parameters"] == "[45,33,2]_3"
    assert out["codes"]["dual"]["weight2_word_count"] == 72
    assert out["codes"]["dual"]["local_private_triple_difference_subcode_dimension"] == 24
    assert out["codes"]["euclidean_hull_dimension"] == 9
    group = out["automorphism_group"]
    assert group["coordinate_permutation_group"] == "S3^12 : AGL(2,3)"
    assert group["affine_quotient_order"] == 432
    assert group["order"] == 940_369_969_152
    assert all(out["checks"].values())
