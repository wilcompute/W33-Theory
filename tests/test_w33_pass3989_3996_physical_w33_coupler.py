import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass3989_3996_physical_w33_coupler.py"
FROZEN = ROOT / "data" / "PART_3990_PHYSICAL_W33_COUPLER.json"


def load_module():
    spec = importlib.util.spec_from_file_location("pass3990_coupler", SOURCE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_sparse_coupler_matches_frozen():
    module = load_module()
    assert module.build() == json.loads(FROZEN.read_text(encoding="utf-8"))


def test_exact_transfer_and_robustness_coefficients():
    data = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert data["graph"] == {"vertices":40,"degree":12,"edges":240,"adjacency_spectrum":{"12":1,"2":24,"-4":15}}
    assert data["exact_interaction_area"] == "kappa*z=pi/2 modulo 2*pi"
    error = data["uniform_fractional_coupling_error"]
    assert error["weighted_first_moment"] == 0
    assert error["weighted_second_moment"] == 3
