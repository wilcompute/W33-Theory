import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1606_1610_five_continuations.py"
FROZEN = ROOT / "data" / "w33_pass1606_1610_five_continuations.json"


def load_module():
    spec = importlib.util.spec_from_file_location("p1606", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_frozen_certificate():
    module = load_module()
    actual = module.certificate()
    expected = json.loads(FROZEN.read_text())
    assert json.loads(json.dumps(actual)) == expected
    assert actual["status"] == "PASS"
    assert all(actual["checks"].values())
    assert actual["certificate_sha256"] == "b7e0a7d9c1333c8daf624a8527d44bee0375bc2321cd34eb41ebcb61264d29d0"
