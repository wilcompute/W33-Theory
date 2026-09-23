from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_e8_matter81_hybrid_cubic_dark_basis.py"
DATA = ROOT / "data/w33_e8_matter81_hybrid_cubic_dark_basis.json"


def load():
    spec = importlib.util.spec_from_file_location("hybrid81", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_replay_matches_frozen_certificate():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_hybrid_basis_closes_root_coordinate_span_without_claiming_operator_intertwiner():
    out = json.loads(DATA.read_text())
    assert out["cubic_sector"]["rank"] == 73
    assert out["cubic_sector"]["selected_pivot_count"] == 73
    assert len(out["cubic_sector"]["selected_pivot_indices_zero_based"]) == 73
    assert out["dark_sector"]["dimension"] == 8
    assert out["dark_sector"]["Hermitian_Gram_diagonal"] == [81,81,54,54,54,54,54,54]
    assert out["dark_sector"]["orthogonal_to_all_270_cubic_columns"] is True
    assert out["dark_sector"]["magic_ray_is_Clifford_equivalent_to_Strange"] is True
    assert out["hybrid_basis"]["dimension"] == 81
    assert out["hybrid_basis"]["rank"] == 81
    assert out["hybrid_basis"]["matrix_digest"].startswith("sha256:")
    assert out["checks"]["operator_intertwiner_not_claimed"] is True
    assert all(out["checks"].values())
