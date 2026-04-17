import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
if str(EXPLORATION) not in sys.path:
    sys.path.insert(0, str(EXPLORATION))

MODULE_PATH = EXPLORATION / "w33_bundle_spectral_seed.py"

spec = importlib.util.spec_from_file_location("w33_bundle_spectral_seed", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_assert_all():
    mod.assert_all()


def test_bundle_dimension():
    summary = mod.build_summary()
    assert summary["spectral_seed"]["bundle_dimension"] == 270


def test_fixed_sector():
    summary = mod.build_summary()
    assert summary["fixed_sector"] == {"scalar": 1, "shell": 0, "color": 1, "total": 2}


def test_metric_and_real_structure():
    summary = mod.build_summary()
    assert summary["transport"]["all_local_transports_preserve_metric"]
    assert summary["transport"]["all_reverse_edges_are_metric_adjoints"]
    assert summary["spectral_seed"]["J_commutes_with_D"]
    assert summary["spectral_seed"]["J_commutes_with_gamma"]
