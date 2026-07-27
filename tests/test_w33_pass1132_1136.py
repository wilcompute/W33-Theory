from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_committed_exact_certificates():
    filenames = [
        "w33_pass1133_true_spectral_functional_calculus.json",
        "w33_pass1134_we6_432_stabilizers.json",
        "w33_pass1135_cubic_kernel_decomposition.json",
        "w33_shifted_adjacency_descendant_audit.json",
        "BT1634_540_audit_results.synthetic.json",
    ]
    for filename in filenames:
        data = json.loads((ROOT / "data" / filename).read_text(encoding="utf-8"))
        assert data["status"] == "PASS"


def test_true_functional_calculus_rebuild():
    mod = load_module("pass1133", ROOT / "analysis" / "w33_pass1133_true_spectral_functional_calculus.py")
    A = mod.adjacency()
    D = A - np.eye(40, dtype=np.int64)
    ranks = {
        name: int(mod.rational_trace(num, den))
        for name, (num, den) in mod.scaled_projectors(D).items()
    }
    assert ranks == {"11": 1, "1": 24, "-5": 15}


def test_stabilizer_and_kernel_theorems():
    stabilizer = json.loads((ROOT / "data" / "w33_pass1134_we6_432_stabilizers.json").read_text())
    assert all(record["stabilizer"]["order"] == 120 for record in stabilizer["records"])
    assert all(record["stabilizer"]["small_group_identification"].startswith("S5") for record in stabilizer["records"])
    assert all(item["conjugate_in_WE6"] for item in stabilizer["pairwise_conjugacy"])

    kernel = json.loads((ROOT / "data" / "w33_pass1135_cubic_kernel_decomposition.json").read_text())
    assert kernel["kernel_dimension"] == 2195
    assert kernel["cubic_module_decomposition"] == [
        {"name": "1", "degree": 1, "multiplicity": 1},
        {"name": "20", "degree": 20, "multiplicity": 1},
        {"name": "24", "degree": 24, "multiplicity": 1},
    ]
    assert kernel["steinberg_obstruction"]["multiplicity_in_kernel"] == 3


def test_occurrence_level_540_classifier():
    mod = load_module("tag540", ROOT / "scripts" / "tag_540_disambiguation.py")
    line_text = "The 540 skew line pairs form cube frames. {540:line-nonedge}"
    point_text = "The 540 noncollinear point pairs have mu=4. {540:point-nonedge}"
    line_match = next(__import__("re").finditer(r"(?<!\d)540(?!\d)", line_text))
    point_match = next(__import__("re").finditer(r"(?<!\d)540(?!\d)", point_text))
    line_result = mod.classify_occurrence(line_text, line_match.start(), line_match.end(), "line.md")
    point_result = mod.classify_occurrence(point_text, point_match.start(), point_match.end(), "point.md")
    assert line_result["category"] == "line-nonedge"
    assert point_result["category"] == "point-nonedge"
