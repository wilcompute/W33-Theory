import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "w33_pathspace_internal_algebra.py"

spec = importlib.util.spec_from_file_location("w33_pathspace_internal_algebra", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_assert_all():
    mod.assert_all()


def test_candidate_blocks():
    s = mod.summary()
    assert s["candidate_algebra_blocks"] == ["C", "H", "M3(C)"]


def test_heisenberg_generates_full_m3():
    s = mod.summary()
    assert s["heisenberg_relations"]["basis_rank"] == 9


def test_hashimoto_shell_gap_is_q():
    s = mod.summary()
    assert abs(s["shell"]["real_gap_sq"] - 3.0) < 1e-10
    assert abs(s["shell"]["imag_gap_sq"] - 3.0) < 1e-10
