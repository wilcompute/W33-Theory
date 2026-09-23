from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_extended_clifford_pass408_intertwiner.py"
DATA = ROOT / "data/w33_extended_clifford_pass408_intertwiner.json"


def load_module():
    spec = importlib.util.spec_from_file_location("w33_ext_cliff_pass408", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_extended_clifford_pass408_intertwiner_replays_frozen_certificate():
    module = load_module()
    got = module.main(write=False)
    frozen = json.loads(DATA.read_text())
    assert got == frozen
    assert got["group_structure"]["full_group"] == "H27 : GL(2,3)"
    assert got["group_structure"]["full_order"] == 1296
    assert got["group_structure"]["unitary_order"] == 648
    assert got["group_structure"]["projective_full_order"] == 432
    assert got["group_structure"]["projective_unitary_order"] == 216
    assert got["group_structure"]["full_center_order"] == 1
    assert got["group_structure"]["unitary_center_order"] == 3
    assert got["group_structure"]["full_derived_order"] == 648
    assert got["group_structure"]["unitary_derived_order"] == 216
    assert got["pass408_weld"]["permutation_sets_equal"] is True
    assert got["pass408_weld"]["q3_no_extras"] is True
    assert got["parity_weld"]["kappa_inverts_Pauli_center"] is True
    assert all(got["checks"].values())
