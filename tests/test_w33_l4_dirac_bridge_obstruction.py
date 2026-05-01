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


OBSTRUCTION = _load_module(
    Path(__file__).resolve().parents[1]
    / "exploration"
    / "w33_l4_dirac_bridge_obstruction.py",
    "w33_l4_dirac_bridge_obstruction",
)


def test_l4_bridge_family_collapses_to_six_effective_modes() -> None:
    certificate = OBSTRUCTION.build_l4_dirac_bridge_obstruction_certificate()
    assert certificate.zero_shared_left_modes == ("ud_23", "ud_13")
    assert certificate.exact_mode_relations == (
        "up_right:q23_ud23 = -up_right:ud_23",
        "up_right:q13_ud13 = up_right:ud_13",
        "down_right:q23_ud23 = down_right:ud_23",
        "down_right:q13_ud13 = -down_right:ud_13",
    )
    assert certificate.effective_mode_names == (
        "shared_left:q23_ud23",
        "shared_left:q13_ud13",
        "up_right:ud_23",
        "up_right:ud_13",
        "down_right:ud_23",
        "down_right:ud_13",
    )


def test_l4_bridge_augmented_rank_proves_no_exact_cancellation() -> None:
    certificate = OBSTRUCTION.build_l4_dirac_bridge_obstruction_certificate()
    assert certificate.response_shape == (24576, 12)
    assert certificate.response_rank == 6
    assert certificate.augmented_rank == 7
    assert certificate.original_total_residual_norm == pytest.approx(2.0344259359556167)
    assert certificate.minimal_total_residual_norm == pytest.approx(1.6919467709619866)
    assert certificate.improvement_factor == pytest.approx(1.2024172219075824)
    assert certificate.normal_equation_max_residual < 1e-12


def test_remaining_l4_residual_is_concentrated_on_nonabelian_triplet_pairs() -> None:
    certificate = OBSTRUCTION.build_l4_dirac_bridge_obstruction_certificate()

    assert tuple(
        (entry.weak_name, entry.color_name)
        for entry in certificate.top_up_residual_pairs
    ) == (
        ("sigma_y", "lambda_6"),
        ("sigma_y", "lambda_5"),
        ("sigma_z", "lambda_6"),
    )
    assert tuple(
        (entry.weak_name, entry.color_name)
        for entry in certificate.top_down_residual_pairs
    ) == (
        ("sigma_z", "lambda_7"),
        ("sigma_z", "lambda_5"),
        ("sigma_y", "lambda_7"),
    )
    assert tuple(
        entry.norm for entry in certificate.top_up_residual_pairs
    ) == pytest.approx((0.38078740070998396, 0.3359263576989749, 0.31676833627000817))
    assert tuple(
        entry.norm for entry in certificate.top_down_residual_pairs
    ) == pytest.approx((0.4438087805288604, 0.3905165492339543, 0.3625477976698757))
