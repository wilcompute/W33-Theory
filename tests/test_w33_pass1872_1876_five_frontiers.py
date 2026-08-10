from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1872_1876_five_frontiers.py"
DUAL = ROOT / "data" / "w33_pass1876_exact_dual_weight_enumerator.json"


def load_module():
    spec = importlib.util.spec_from_file_location("pass1872_1876", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_five_frontiers(tmp_path):
    module = load_module()
    report = module.main(tmp_path / "aggregate.json")
    assert report["status"] == "PASS"
    assert report["n_verified"] == report["n_checks"] == 19
    assert report["pass1872"]["balanced_gram_determinant"] == 2560
    assert report["pass1873"]["primitive_unoriented_cycles"]["8"] == 90
    assert report["pass1874"]["projector_numerator_rank"] == 9
    assert report["pass1875"]["normality_correction"]
    assert report["pass1875"]["directed_automorphism_group"] == "C4"
    assert report["pass1876"]["A12"] == 891_792_940
    assert report["pass1876"]["weight6_equal_syndrome_pairs"] == 1_724_138_884_380
    assert report["sha256_without_hash_field"] == "ac0e784eda0af4bf0caa13ef4b4eee027d65a23cb033490cfe2b67ec5b78480d"


def test_exact_dual_certificate():
    dual = json.loads(DUAL.read_text(encoding="utf-8"))
    assert dual["status"] == "PASS"
    assert dual["n_verified"] == dual["n_checks"] == 8
    assert dual["enumerated_word_total"] == 1 << 45
    assert dual["A12"] == 891_792_940
    assert dual["fixed_coordinate_A12"] == 44_589_647
    assert dual["sha256_without_hash_field"] == "73f2f0e41eb49c8dac6028ea4fe026c3f84a1a7ddcc263960d96f76de29fd958"
