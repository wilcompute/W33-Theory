from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    previous = sys.modules.get(name)
    had_previous = name in sys.modules
    try:
        sys.modules[name] = module
        spec.loader.exec_module(module)
    except BaseException:
        if had_previous:
            sys.modules[name] = previous
        else:
            sys.modules.pop(name, None)
        raise
    return module


BRIDGE = _load_module(
    Path(__file__).resolve().parents[1]
    / "exploration"
    / "w33_l4_quark_dirac_bridge.py",
    "w33_l4_quark_dirac_bridge",
)
SELF_ENERGY = _load_module(
    Path(__file__).resolve().parents[1] / "exploration" / "w33_l4_quark_self_energy.py",
    "w33_l4_quark_self_energy_for_bridge_tests",
)


def test_bridge_basis_is_exact_and_clean() -> None:
    basis = BRIDGE.l4_dirac_bridge_basis()
    assert tuple(element.name for element in basis) == (
        "ud_23",
        "ud_13",
        "q23_ud23",
        "q13_ud13",
    )
    assert basis[0].entries == (
        BRIDGE.CountertermEntry("u_c_2", "u_c_2", 2),
        BRIDGE.CountertermEntry("u_c_3", "u_c_3", -2),
        BRIDGE.CountertermEntry("d_c_2", "d_c_2", -2),
        BRIDGE.CountertermEntry("d_c_3", "d_c_3", 2),
    )
    assert basis[2].entries == (
        BRIDGE.CountertermEntry("Q_2_1", "Q_2_1", 2),
        BRIDGE.CountertermEntry("Q_2_2", "Q_2_2", 2),
        BRIDGE.CountertermEntry("Q_3_1", "Q_3_1", -2),
        BRIDGE.CountertermEntry("Q_3_2", "Q_3_2", -2),
        BRIDGE.CountertermEntry("u_c_2", "u_c_2", -2),
        BRIDGE.CountertermEntry("u_c_3", "u_c_3", 2),
        BRIDGE.CountertermEntry("d_c_2", "d_c_2", -2),
        BRIDGE.CountertermEntry("d_c_3", "d_c_3", 2),
    )
    for element in basis:
        matrix = BRIDGE.basis_matrix_27(element.name)
        assert SELF_ENERGY.full_screen_residual_norm_27(matrix) == 0.0


def test_l4_dirac_bridge_reduces_full_screen_residual() -> None:
    candidate = BRIDGE.build_l4_quark_dirac_bridge_candidate()
    assert candidate.shared_left_coeffs == pytest.approx(
        (0.0, 0.0, -0.10870090768720922, 0.17372388038021844)
    )
    assert candidate.up_block.right_coeffs == pytest.approx(
        (
            -0.020824661275933836,
            -0.043653079554613915,
            0.02082466127593378,
            -0.043653079554613956,
        )
    )
    assert candidate.down_block.right_coeffs == pytest.approx(
        (
            -0.07169916081994468,
            -0.043217744317060144,
            -0.07169916081994468,
            0.04321774431706016,
        )
    )
    assert candidate.original_total_residual_norm == pytest.approx(2.0344259359556167)
    assert candidate.bridged_total_residual_norm == pytest.approx(1.6919467709619866)
    assert candidate.residual_improvement_factor == pytest.approx(1.2024172219075824)
    assert candidate.residual_reduction_fraction == pytest.approx(0.16834191844529336)


def test_l4_dirac_bridge_lifts_quark_block_ranks() -> None:
    candidate = BRIDGE.build_l4_quark_dirac_bridge_candidate()
    assert candidate.support_preserved is True

    assert candidate.up_block.original_rank == 2
    assert candidate.up_block.bridged_rank == 3
    assert candidate.up_block.support_count == 15
    assert candidate.up_block.original_residual_norm == pytest.approx(
        1.1135528725660053
    )
    assert candidate.up_block.bridged_residual_norm == pytest.approx(1.0931431037711359)

    assert candidate.down_block.original_rank == 2
    assert candidate.down_block.bridged_rank == 3
    assert candidate.down_block.support_count == 17
    assert candidate.down_block.original_residual_norm == pytest.approx(
        1.7026123718829504
    )
    assert candidate.down_block.bridged_residual_norm == pytest.approx(
        1.2914031246850464
    )
