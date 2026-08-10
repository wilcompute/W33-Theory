import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1806_1810_torsion_xor_lattice_octet.py"
FROZEN = ROOT / "data" / "w33_pass1806_1810_torsion_xor_lattice_octet.json"


def load():
    spec = importlib.util.spec_from_file_location("p1806", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_frozen_reconciliation_certificate():
    module = load()
    fresh = module.certificate(write_xor=False)
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert json.loads(json.dumps(fresh)) == frozen
    assert frozen["status"] == "PASS" and all(frozen["checks"].values())
    assert frozen["pass1806"]["alternative_composition_series"] == [1, 8, 1, 6, 14]
    assert frozen["pass1807"]["cross_color_redundancy_dimension"] == 30
    assert frozen["pass1808"]["single_cover_signature"] == 8
    assert frozen["pass1809"]["missing_vector_weight"] == 128
    assert frozen["pass1810"]["row_intersection_partition_closed"] is False
