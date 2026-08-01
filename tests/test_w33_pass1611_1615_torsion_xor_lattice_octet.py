import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1611_1615_torsion_xor_lattice_octet.py"
FROZEN = ROOT / "data" / "w33_pass1611_1615_torsion_xor_lattice_octet.json"


def load():
    spec = importlib.util.spec_from_file_location("p1611", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_frozen_certificate_and_xor():
    module = load()
    fresh = module.certificate(write_xor=False)
    frozen = json.loads(FROZEN.read_text())
    assert json.loads(json.dumps(fresh)) == frozen
    assert frozen["status"] == "PASS" and all(frozen["checks"].values())
    assert frozen["pass1611"]["composition_factors"] == [1, 8, 1, 6, 14]
    assert frozen["pass1614"]["saturated_bridge_determinant"] == 2
    assert frozen["pass1615"]["two_fiber_rank"] == 45
