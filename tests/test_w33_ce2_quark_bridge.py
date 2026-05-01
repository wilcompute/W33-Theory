from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
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


MODULE = _load_module(
    Path(__file__).resolve().parents[1] / "exploration" / "w33_ce2_quark_bridge.py",
    "w33_ce2_quark_bridge",
)


def test_ce2_generates_full_quark_source_matrix_algebra() -> None:
    certificate = MODULE.build_ce2_quark_bridge_certificate()

    assert certificate.q_source_ids == (7, 8, 11, 12, 13, 14)
    assert certificate.u_source_ids == (10, 6, 4)
    assert certificate.d_source_ids == (9, 5, 3)

    assert certificate.generated_source_unit_count == 144
    assert certificate.uv_only_source_unit_count == 90
    assert certificate.uvw_only_source_unit_count == 0
    assert certificate.uv_and_uvw_source_unit_count == 54
    assert certificate.source_matrix_algebra_is_full is True

    record_by_pair = {
        (record.source_row, record.source_col): record
        for record in certificate.generated_units
    }
    assert record_by_pair[(7, 7)].row_slot == "Q_1_1"
    assert record_by_pair[(7, 7)].col_slot == "Q_1_1"
    assert record_by_pair[(10, 10)].row_slot == "u_c_1"
    assert record_by_pair[(9, 9)].row_slot == "d_c_1"
    assert record_by_pair[(14, 3)].row_slot == "Q_3_2"
    assert record_by_pair[(14, 3)].col_slot == "d_c_3"


def test_ce2_right_identities_are_generated_exactly() -> None:
    up_identity = MODULE.ce2_right_identity_up_27()
    down_identity = MODULE.ce2_right_identity_down_27()

    up_block = up_identity[np.ix_((7, 8, 9), (7, 8, 9))]
    down_block = down_identity[np.ix_((10, 11, 12), (10, 11, 12))]

    assert np.array_equal(up_block, np.eye(3))
    assert np.array_equal(down_block, np.eye(3))


def test_ce2_bridge_closes_current_residual_only_trivially() -> None:
    certificate = MODULE.build_ce2_quark_bridge_certificate()

    assert certificate.projected_mode_count == 54
    assert certificate.left_mode_count == 36
    assert certificate.up_right_mode_count == 9
    assert certificate.down_right_mode_count == 9
    assert certificate.response_rank == 28
    assert certificate.augmented_rank == 28
    assert certificate.original_total_residual_norm == pytest.approx(2.0344259359556167)
    assert certificate.trivial_closure_total_residual_norm < 1e-12
    assert certificate.trivial_closure_up_residual_norm < 1e-12
    assert certificate.trivial_closure_down_residual_norm < 1e-12

    assert (
        np.count_nonzero(
            np.abs(MODULE.ce2_trivial_closed_up_quark_yukawa_8x8()) > 1e-12
        )
        == 0
    )
    assert (
        np.count_nonzero(
            np.abs(MODULE.ce2_trivial_closed_down_quark_yukawa_8x8()) > 1e-12
        )
        == 0
    )


def test_full_quark_family_has_only_zero_clean_point() -> None:
    certificate = MODULE.build_ce2_quark_bridge_certificate()

    assert certificate.arbitrary_quark_screen_rank == 36
    assert certificate.arbitrary_quark_screen_nullity == 0
    assert certificate.zero_is_unique_clean_point is True


def test_l4_response_is_contained_in_ce2_bridge_span() -> None:
    certificate = MODULE.build_ce2_quark_bridge_certificate()

    assert certificate.l4_response_contained_in_ce2 is True
    assert certificate.max_l4_containment_error < 1e-12
