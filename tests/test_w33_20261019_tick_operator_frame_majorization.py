"""Regression for the exact 120-projector operator-frame certificate."""
import importlib.util
from pathlib import Path

def test_tick_projector_gram_and_majorization():
    root = Path(__file__).resolve().parents[1]
    path = root / "analysis" / "w33_20261019_tick_operator_frame_majorization.py"
    spec = importlib.util.spec_from_file_location("tick_operator_frame", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    certificate = module.certify()
    assert certificate["all_checks_pass"]
    assert certificate["pair_types"] == {
        "same_point_different_outcome":120,
        "collinear_distinct_point":2160,
        "noncollinear_distinct_point":4860,
    }
