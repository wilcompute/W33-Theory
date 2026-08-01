import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "analysis" / "w33_pass1831_1835_five_executions.py"
spec = importlib.util.spec_from_file_location("p1831_1835", PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_pass1831_1835_frozen_exact():
    result = module.verify(run_workers=False)
    assert result["status"] == "PASS"
    assert result["passed"] == result["total"]
