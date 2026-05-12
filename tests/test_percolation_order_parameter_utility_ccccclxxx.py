import importlib.util
from pathlib import Path


def load_module():
    path = Path(__file__).resolve().parents[1] / "scripts" / "PART_CCCCCLXXX_percolation_order_parameters.py"
    spec = importlib.util.spec_from_file_location("percolation_order_parameters", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_utility_zero_visibility():
    m = load_module()
    ledger = m.visibility_ledger([0.0] * 81)
    assert ledger.rank == 0
    assert ledger.trace == 0
    assert ledger.trace2 == 0
    assert ledger.d_eff == 0
    assert ledger.split_count == 0
    assert ledger.outcome_class == "zero"


def test_utility_full_isotropic_visibility():
    m = load_module()
    ledger = m.visibility_ledger([2.0] * 81)
    assert ledger.rank == 81
    assert ledger.trace == 162.0
    assert ledger.trace2 == 324.0
    assert ledger.d_eff == 81.0
    assert ledger.split_count == 1
    assert ledger.outcome_class == "full_isotropic"


def test_utility_full_split_visibility():
    m = load_module()
    ledger = m.visibility_ledger([3.0] * 40 + [1.0] * 41)
    assert ledger.rank == 81
    assert ledger.d_eff < 81
    assert ledger.split_count == 2
    assert ledger.outcome_class == "full_split"


def test_utility_rank_defective_visibility():
    m = load_module()
    ledger = m.visibility_ledger([1.0] * 27 + [0.0] * 54)
    assert ledger.rank == 27
    assert ledger.split_count == 1
    assert ledger.outcome_class == "rank_defective"


def test_split_tolerance_groups_close_values():
    m = load_module()
    vals = [1.0, 1.0 + 1e-10, 2.0]
    assert m.split_count(vals, eps=1e-9) == 2
    assert m.split_count(vals, eps=1e-12) == 3
