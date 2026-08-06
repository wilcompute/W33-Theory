from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_pass4073_4080_engineering_outside_box.py"
DATA = ROOT / "data/PART_4073_4080_ENGINEERING_OUTSIDE_BOX.json"


def _module():
    spec = importlib.util.spec_from_file_location("pass4073_4080", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_frozen_certificate_and_exact_verifier(capsys):
    module = _module()
    module.main()
    out = capsys.readouterr().out
    assert "PASS_4073_4080" in out
    assert "0304eef2ec49efabf5721ed47a35e48064530f459f2964ae49e455ef1d3c5a31" in out


def test_eight_promoted_fronts_and_boundaries():
    data = json.loads(DATA.read_text())
    for number in range(4073, 4081):
        assert any(key.startswith(f"pass{number}_") for key in data)
    assert data["pass4073_physical_four_router_block_encoding"]["exact_matrix_residual"] == 0
    assert data["pass4075_minimal_nonabelian_multiplicity_extension"]["minimum_exact_factor_extension"]["dimension"] == 57
    assert data["pass4078_bonkers_Maxwell_Calladine_mechanics"]["self_stress_dimension"] == 81
    assert "No fabricated hardware" in data["boundaries"][1]
