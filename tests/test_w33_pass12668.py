"""Pass 12668: stabiliser states fibre 6-to-1 over the 180 minimal integral BPS charges; Lean module present."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_stabiliser_fibration():
    d = load("w33_stabiliser_states_minimal_charges.json")
    assert d["n_states"] == 1080 and d["n_images"] == 180 and d["n_minimal_integral_charges"] == 180
    assert d["image_equals_minimal_set"] and d["fibre_sizes"] == {"6": 180}
    assert d["fibre_span_dims"] == {"2": 180}
    assert d["fibres_equal_quaternionic_line"] == 180 and d["fibres_with_qubit_stabiliser_overlaps"] == 180


def test_lean_module_states_the_three_inequalities():
    p = os.path.join(ROOT, "formal", "W33", "Pass12667AttractorMajorisation.lean")
    s = open(p, encoding="utf-8").read()
    for name in ("max_ge_geomean", "sum_ge_three_geomean", "attractor_majorisation"):
        assert f"theorem {name}" in s
    assert "sorry" not in s
