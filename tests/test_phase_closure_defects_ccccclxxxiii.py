import importlib.util
from pathlib import Path


def load_module():
    path = Path(__file__).resolve().parents[1] / "scripts" / "PART_CCCCCLXXXIII_phase_closure_defects.py"
    spec = importlib.util.spec_from_file_location("phase_closure_defects", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_coherent_cycle_closes_all_defects():
    m = load_module()
    cycle = [
        m.Atom(3, 1, 5, 11),
        m.Atom(9, 2, 5, 11),
        m.Atom(0, 4, 0, 12),
        m.Atom(0, 4, 0, 12),
    ]
    ledger = m.closure_ledger(cycle)
    assert ledger.d12 == 0
    assert ledger.d10 == 0
    assert ledger.d7 == (0, 0, 0)
    assert ledger.dcl == ()
    assert ledger.coherent


def test_defective_cycle_detects_open_phase_and_blades():
    m = load_module()
    cycle = [m.Atom(3, 1, 5, 11), m.Atom(4, 2, 5, 12)]
    ledger = m.closure_ledger(cycle)
    assert ledger.d12 == 7
    assert ledger.d10 == 0
    assert ledger.d7 != (0, 0, 0)
    assert ledger.dcl == (11, 12)
    assert not ledger.coherent


def test_closure_score_mixed_cycles():
    m = load_module()
    coherent = [m.Atom(3, 1, 5, 11), m.Atom(9, 2, 5, 11), m.Atom(0, 4, 0, 12), m.Atom(0, 4, 0, 12)]
    defective = [m.Atom(3, 1, 5, 11), m.Atom(4, 2, 5, 12)]
    assert m.closure_score([coherent, defective]) == 0.5


def test_unoccupied_atoms_are_ignored():
    m = load_module()
    cycle = [m.Atom(3, 1, 5, 11), m.Atom(9, 2, 5, 11), m.Atom(1, 3, 1, 99, occupied=False)]
    ledger = m.closure_ledger(cycle)
    assert ledger.d12 == 0
    assert ledger.d10 == 0
    assert ledger.dcl == ()
