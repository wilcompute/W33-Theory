from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "w33_zero_sheet_spectral_cycle_response.py"


def load_module():
    spec = importlib.util.spec_from_file_location("w33_zero_sheet_spectral_cycle_response", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_zero_sheet_spectral_cycle_response_payload() -> None:
    module = load_module()
    payload = module.build_payload()
    summary = payload["summary"]

    assert summary["all_identities_hold"] is True
    assert summary["zero_sheet_cycle_lengths"] == [4, 4, 6]
    assert summary["zero_sheet_cycle_rank"] == 2
    assert summary["spectral_wall"] == 6.0
    assert summary["interior_cycle_deformation"] == 4.0
    assert summary["wall_probe_deformations"] == [5.0, 5.5, 5.9]

    terminal_rows = payload["terminal_wall_approach_rows"]
    assert [row["deformation"] for row in terminal_rows] == [4.0, 5.0, 5.5, 5.9]
    assert all(row["deformation"] < summary["spectral_wall"] for row in terminal_rows)
    assert terminal_rows[-1]["hessian"] > terminal_rows[0]["hessian"] > 0.0
    assert terminal_rows[-1]["stiffness"] < terminal_rows[0]["stiffness"]

    interior_inverse = payload["infinite_inverse_profiles"]["1.0"]["4.0"]["rows"]
    wall_inverse = payload["infinite_inverse_profiles"]["1.0"]["5.9"]["rows"]
    assert interior_inverse[2]["interval_width"] < interior_inverse[1]["interval_width"] < interior_inverse[0]["interval_width"]
    assert wall_inverse[2]["interval_width"] < wall_inverse[1]["interval_width"] < wall_inverse[0]["interval_width"]

    interior_stiffness = payload["infinite_stiffness_profiles"]["1.0"]["4.0"]["rows"]
    wall_stiffness = payload["infinite_stiffness_profiles"]["1.0"]["5.9"]["rows"]
    assert interior_stiffness[2]["stiffness_interval_width"] < interior_stiffness[1]["stiffness_interval_width"] < interior_stiffness[0]["stiffness_interval_width"]
    assert wall_stiffness[2]["stiffness_interval_width"] < wall_stiffness[1]["stiffness_interval_width"] < wall_stiffness[0]["stiffness_interval_width"]