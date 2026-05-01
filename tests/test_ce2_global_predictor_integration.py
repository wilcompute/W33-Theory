from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from tools.build_linfty_firewall_extension import (
    LInftyE8Extension,
    _load_bad9,
    _load_bracket_tool,
)
from tools.exhaustive_homotopy_check_rationalized_l3 import basis_elem_g1, basis_elem_g2

ROOT = Path(__file__).resolve().parents[1]
E6_BASIS_PATH = ROOT / "artifacts" / "e6_27rep_basis_export" / "E6_basis_78.npy"

pytestmark = pytest.mark.skipif(
    not E6_BASIS_PATH.exists(),
    reason=(
        "artifacts/e6_27rep_basis_export/E6_basis_78.npy is an optional E6 basis export; "
        "run tools/build_e6_27rep_minuscule.py --export-basis to materialize this integration suite"
    ),
)


def max_abs(e) -> float:
    return float(
        max(
            0.0 if e.e6.size == 0 else np.max(np.abs(e.e6)),
            0.0 if e.sl3.size == 0 else np.max(np.abs(e.sl3)),
            0.0 if e.g1.size == 0 else np.max(np.abs(e.g1)),
            0.0 if e.g2.size == 0 else np.max(np.abs(e.g2)),
        )
    )


def _build_linfty():
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()
    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)
    return toe, linfty


def _assert_predictor_cancels_triples(triples) -> None:
    for triple in triples:
        toe, linfty = _build_linfty()
        x = basis_elem_g1(toe, triple[0])
        y = basis_elem_g2(toe, triple[1])
        z = basis_elem_g2(toe, triple[2])

        baseline = linfty.homotopy_jacobi(x, y, z)
        assert max_abs(baseline) > 1e-10, triple

        linfty.enable_ce2_global_predictor()
        repaired = linfty.homotopy_jacobi(x, y, z)
        assert max_abs(repaired) < 1e-10, triple


def test_global_ce2_predictor_cancels_known_mixed_basis_triple() -> None:
    """Integration check: the CE2 global predictor cancels a recorded g1,g1,g2 obstruction.

    This threads the metaplectic/Weil CE2 phase law through the L∞ firewall:
    `homotopy_jacobi` should reduce to ~0 on this triple without attaching a
    per-triple CE2 artifact or running an LSQ solve.
    """
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    # Known failing mixed triple (regression key used elsewhere in the suite).
    x = basis_elem_g1(toe, (0, 0))
    y = basis_elem_g1(toe, (17, 1))
    z = basis_elem_g2(toe, (3, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_dual_diagonal_fiber_triple() -> None:
    """Integration check for the first closed-form g1,g2,g2 W-family."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (4, 1))
    y = basis_elem_g2(toe, (4, 1))
    z = basis_elem_g2(toe, (25, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_artifact_loader_does_not_smear_dual_w_family() -> None:
    """Artifact aggregation must not block the dual predictor on unseen c-legs."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)
    linfty.attach_l4_from_symbolic_constants(
        "artifacts/l4_symbolic_constants.json", load_ce2_artifact=True
    )
    linfty.enable_ce2_global_predictor()

    x = basis_elem_g1(toe, (0, 0))
    y = basis_elem_g2(toe, (0, 0))
    z = basis_elem_g2(toe, (21, 2))

    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_dual_same_e6id_fiber_triple() -> None:
    """Integration check for the second closed-form g1,g2,g2 family."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (4, 1))
    y = basis_elem_g2(toe, (4, 2))
    z = basis_elem_g2(toe, (25, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_dual_missing_focus_u_triple() -> None:
    """Integration check for the focus-section U-family."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (0, 0))
    y = basis_elem_g2(toe, (1, 0))
    z = basis_elem_g2(toe, (15, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_second_focus_section_u_orbit() -> None:
    """A second orbit checks the section rule is not a one-off fit."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (0, 2))
    y = basis_elem_g2(toe, (9, 2))
    z = basis_elem_g2(toe, (4, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_origin_line_w_family() -> None:
    """Integration check for the first off-fiber W-only frontier family."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (0, 0))
    y = basis_elem_g2(toe, (1, 0))
    z = basis_elem_g2(toe, (16, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_origin_line_w_family_second_lambda() -> None:
    """A second affine-line placement checks the lookup table orientation."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (0, 1))
    y = basis_elem_g2(toe, (2, 1))
    z = basis_elem_g2(toe, (15, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_origin_line_w_family_mirror_z_order() -> None:
    """Mirror z-order should be covered by the same origin-line law."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (0, 0))
    y = basis_elem_g2(toe, (4, 0))
    z = basis_elem_g2(toe, (13, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_origin_line_v_family() -> None:
    """Color-swapped dual of the origin-line W-family."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (0, 0))
    y = basis_elem_g2(toe, (1, 1))
    z = basis_elem_g2(toe, (16, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_origin_line_v_family_mirror_z_order() -> None:
    """Mirror z-order should be covered for the dual V family too."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (0, 0))
    y = basis_elem_g2(toe, (4, 1))
    z = basis_elem_g2(toe, (13, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_origin_line_v_family_second_line() -> None:
    """A second line direction checks the dual V table."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (0, 0))
    y = basis_elem_g2(toe, (2, 2))
    z = basis_elem_g2(toe, (15, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_origin_same_fiber_uv_family_mirror_z_order() -> (
    None
):
    """The 1/108 overlap family should also cover the mirrored z-order."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (0, 0))
    y = basis_elem_g2(toe, (4, 1))
    z = basis_elem_g2(toe, (9, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_origin_same_fiber_uv_family_x_axis() -> None:
    """The explicit V-sign table should cover the x-axis line too."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (0, 0))
    y = basis_elem_g2(toe, (11, 1))
    z = basis_elem_g2(toe, (14, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_translated_2v_line_w_family() -> None:
    """Translated branch with `a` at the 2v,z=2 point."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 0))
    y = basis_elem_g2(toe, (0, 0))
    z = basis_elem_g2(toe, (20, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_translated_2v_line_v_family() -> None:
    """Translated V dual on the same branch."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 0))
    y = basis_elem_g2(toe, (0, 1))
    z = basis_elem_g2(toe, (20, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_translated_2v_overlap_uv_family() -> None:
    """Translated half-strength overlap branch."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 0))
    y = basis_elem_g2(toe, (0, 1))
    z = basis_elem_g2(toe, (22, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_vertical_z2_line_w_family() -> None:
    """Gauge-fixed same-z vertical branch with pure W support."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 1))
    y = basis_elem_g2(toe, (2, 1))
    z = basis_elem_g2(toe, (22, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_vertical_z2_line_v_family() -> None:
    """Color-swapped vertical same-z dual."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 2))
    y = basis_elem_g2(toe, (2, 0))
    z = basis_elem_g2(toe, (22, 2))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_vertical_z2_overlap_uv_family() -> None:
    """Half-strength vertical overlap with U on the z=1 fiber point."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 1))
    y = basis_elem_g2(toe, (2, 0))
    z = basis_elem_g2(toe, (20, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchored_nonvertical_z2_line_w_family() -> None:
    """Nonvertical z=2 affine-line W-family through the a=(0,2,2) anchor."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 0))
    y = basis_elem_g2(toe, (3, 0))
    z = basis_elem_g2(toe, (13, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchored_nonvertical_z2_line_v_family() -> None:
    """Color-swapped dual on the same nonvertical z=2 affine line."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 0))
    y = basis_elem_g2(toe, (3, 1))
    z = basis_elem_g2(toe, (13, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchored_nonvertical_z2_overlap_uv_family() -> (
    None
):
    """Half-strength overlap on the active nonvertical z=2 branch."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 0))
    y = basis_elem_g2(toe, (3, 1))
    z = basis_elem_g2(toe, (6, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchored_z1_to_z0_line_w_family() -> None:
    """Anchored branch with the first g2 leg in z=1 and the second in z=0."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 0))
    y = basis_elem_g2(toe, (4, 0))
    z = basis_elem_g2(toe, (19, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchored_z1_to_z0_line_v_family() -> None:
    """Color-swapped dual on the anchored z=1 -> z=0 branch."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 0))
    y = basis_elem_g2(toe, (4, 1))
    z = basis_elem_g2(toe, (19, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchored_z1_to_z0_overlap_uv_family() -> None:
    """Half-strength overlap on the anchored z=1 -> z=0 branch."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 0))
    y = basis_elem_g2(toe, (4, 1))
    z = basis_elem_g2(toe, (9, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchored_nonvertical_z2_complement_uv_family() -> (
    None
):
    """Complementary overlap on the u1=1 half of the anchored z=2 pencil."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 0))
    y = basis_elem_g2(toe, (7, 1))
    z = basis_elem_g2(toe, (19, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchored_nonvertical_z2_complement_uv_family_negative_v_sign() -> (
    None
):
    """A second direction checks the complementary V-sign table."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (1, 0))
    y = basis_elem_g2(toe, (11, 1))
    z = basis_elem_g2(toe, (17, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_01_origin_line_w_family() -> None:
    """Origin-line branch for the new a=(0,1,2) anchor."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (2, 0))
    y = basis_elem_g2(toe, (0, 0))
    z = basis_elem_g2(toe, (23, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_01_origin_overlap_uv_family() -> None:
    """Half-strength origin overlap for the new a=(0,1,2) anchor."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (2, 0))
    y = basis_elem_g2(toe, (0, 1))
    z = basis_elem_g2(toe, (21, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_01_samefiber_z2_line_w_family() -> None:
    """Same-fiber z=2 branch for the new a=(0,1,2) anchor."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (2, 1))
    y = basis_elem_g2(toe, (1, 1))
    z = basis_elem_g2(toe, (21, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_01_samefiber_z2_overlap_uv_family() -> (
    None
):
    """Half-strength same-fiber overlap for the new a=(0,1,2) anchor."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (2, 0))
    y = basis_elem_g2(toe, (1, 2))
    z = basis_elem_g2(toe, (23, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_01_affine_z2_line_w_family() -> None:
    """Representative nonvertical z=2 affine-line branch for a=(0,1,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (2, 0))
    y = basis_elem_g2(toe, (5, 0))
    z = basis_elem_g2(toe, (18, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_01_affine_z2_overlap_uv_family() -> None:
    """Representative nonvertical z=2 overlap for a=(0,1,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (2, 0))
    y = basis_elem_g2(toe, (3, 1))
    z = basis_elem_g2(toe, (6, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_01_affine_z1_overlap_uv_family() -> None:
    """Representative z=1 affine overlap for a=(0,1,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (2, 0))
    y = basis_elem_g2(toe, (6, 1))
    z = basis_elem_g2(toe, (3, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_01_affine_z1_complement_uv_family() -> (
    None
):
    """Complementary z=1 overlap on the u1=1 half of the a=(0,1,2) pencil."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (2, 0))
    y = basis_elem_g2(toe, (8, 1))
    z = basis_elem_g2(toe, (18, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_01_affine_z1_complement_uv_family_second_direction() -> (
    None
):
    """A second direction checks the complementary z=1 U-sign character."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (2, 0))
    y = basis_elem_g2(toe, (12, 1))
    z = basis_elem_g2(toe, (19, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_origin_overlap_uv_family() -> None:
    """Origin overlap branch for the anchored a=(2,0,2) orbit."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (0, 1))
    z = basis_elem_g2(toe, (21, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_samefiber_z2_line_w_family() -> None:
    """Same-fiber z=2 line branch for the anchored a=(2,0,2) orbit."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (11, 0))
    z = basis_elem_g2(toe, (21, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_samefiber_z2_overlap_uv_family() -> (
    None
):
    """Half-strength same-fiber overlap for the anchored a=(2,0,2) orbit."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (11, 1))
    z = basis_elem_g2(toe, (17, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_zero2_z2_line_w_family() -> None:
    """Affine z=2 branch through b=(0,2,2) for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (1, 0))
    z = basis_elem_g2(toe, (8, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_zero2_z2_overlap_uv_family() -> None:
    """Half-strength overlap on the b=(0,2,2) affine branch for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (1, 1))
    z = basis_elem_g2(toe, (15, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_zero1_z2_line_w_family() -> None:
    """Affine z=2 branch through b=(0,1,2) for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (2, 0))
    z = basis_elem_g2(toe, (7, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_zero1_z2_overlap_uv_family() -> None:
    """Half-strength overlap on the b=(0,1,2) affine branch for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (2, 1))
    z = basis_elem_g2(toe, (20, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_two2_z1_line_w_family() -> None:
    """z=1 affine branch through b=(2,2,1) for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (4, 0))
    z = basis_elem_g2(toe, (5, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_two2_z1_overlap_uv_family() -> None:
    """Half-strength overlap on the b=(2,2,1) branch for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (4, 1))
    z = basis_elem_g2(toe, (9, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_two1_z2_complement_uv_family() -> None:
    """Complementary z=2 overlap through b=(2,1,2) for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (5, 1))
    z = basis_elem_g2(toe, (24, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_one2_z2_complement_uv_family() -> None:
    """Complementary z=2 overlap through b=(1,2,2) for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (7, 1))
    z = basis_elem_g2(toe, (12, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_one1_z1_complement_uv_family() -> None:
    """Complementary z=1 overlap through b=(1,1,1) for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (8, 1))
    z = basis_elem_g2(toe, (18, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_two2_z2_line_w_family() -> None:
    """z=2 line branch through b=(2,2,2) for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (9, 0))
    z = basis_elem_g2(toe, (24, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_one2_z1_line_w_family() -> None:
    """z=1 line branch through b=(1,2,1) for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (12, 0))
    z = basis_elem_g2(toe, (20, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_one2_z1_overlap_uv_family() -> None:
    """Half-strength overlap on the b=(1,2,1) branch for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (12, 1))
    z = basis_elem_g2(toe, (7, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_zero2_z1_line_w_family() -> None:
    """z=1 line branch through b=(0,2,1) for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (15, 0))
    z = basis_elem_g2(toe, (18, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_20_zero2_z1_overlap_uv_family() -> None:
    """Half-strength overlap on the b=(0,2,1) branch for a=(2,0,2)."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (3, 0))
    y = basis_elem_g2(toe, (15, 1))
    z = basis_elem_g2(toe, (1, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_22_line_families() -> None:
    """Table-driven line families on the anchored a=(2,2,1) orbit."""
    triples = [
        ((4, 0), (0, 0), (18, 1)),
        ((4, 0), (1, 1), (12, 0)),
        ((4, 0), (2, 0), (11, 1)),
        ((4, 0), (3, 1), (10, 0)),
        ((4, 0), (6, 0), (24, 1)),
        ((4, 0), (7, 1), (23, 0)),
        ((4, 0), (8, 0), (22, 1)),
        ((4, 0), (16, 1), (17, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_22_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(2,2,1) orbit."""
    triples = [
        ((4, 0), (0, 1), (22, 0)),
        ((4, 0), (0, 2), (22, 0)),
        ((4, 0), (1, 1), (23, 0)),
        ((4, 0), (2, 1), (16, 0)),
        ((4, 0), (3, 1), (6, 0)),
        ((4, 0), (7, 1), (12, 0)),
        ((4, 0), (7, 2), (12, 0)),
        ((4, 0), (8, 1), (18, 0)),
        ((4, 0), (10, 1), (24, 0)),
        ((4, 0), (11, 1), (17, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_21_line_families() -> None:
    """Table-driven line families on the anchored a=(2,1,2) orbit."""
    triples = [
        ((5, 0), (1, 0), (14, 1)),
        ((5, 0), (2, 1), (13, 0)),
        ((5, 0), (3, 0), (25, 1)),
        ((5, 0), (6, 1), (9, 0)),
        ((5, 0), (7, 0), (21, 1)),
        ((5, 0), (8, 1), (20, 0)),
        ((5, 0), (15, 0), (17, 1)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_21_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(2,1,2) orbit."""
    triples = [
        ((5, 0), (0, 1), (21, 0)),
        ((5, 0), (0, 2), (21, 0)),
        ((5, 0), (1, 1), (15, 0)),
        ((5, 0), (2, 1), (20, 0)),
        ((5, 0), (3, 1), (6, 0)),
        ((5, 0), (7, 1), (19, 0)),
        ((5, 0), (7, 2), (19, 0)),
        ((5, 0), (8, 1), (13, 0)),
        ((5, 0), (9, 1), (25, 0)),
        ((5, 0), (14, 1), (17, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_201_line_families() -> None:
    """Table-driven line families on the anchored a=(2,0,1) orbit."""
    triples = [
        ((6, 0), (0, 0), (17, 1)),
        ((6, 0), (0, 1), (17, 0)),
        ((6, 0), (1, 0), (8, 1)),
        ((6, 0), (1, 1), (8, 0)),
        ((6, 0), (2, 0), (7, 1)),
        ((6, 0), (2, 1), (7, 0)),
        ((6, 0), (4, 0), (5, 1)),
        ((6, 0), (4, 1), (5, 0)),
        ((6, 0), (10, 0), (25, 1)),
        ((6, 0), (10, 1), (25, 0)),
        ((6, 0), (13, 0), (23, 1)),
        ((6, 0), (13, 1), (23, 0)),
        ((6, 0), (14, 0), (22, 1)),
        ((6, 0), (14, 1), (22, 0)),
        ((6, 0), (16, 0), (19, 1)),
        ((6, 0), (16, 1), (19, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_201_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(2,0,1) orbit."""
    triples = [
        ((6, 0), (0, 1), (22, 0)),
        ((6, 0), (0, 2), (22, 0)),
        ((6, 0), (1, 1), (23, 0)),
        ((6, 0), (1, 2), (23, 0)),
        ((6, 0), (2, 1), (16, 0)),
        ((6, 0), (2, 2), (16, 0)),
        ((6, 0), (4, 1), (25, 0)),
        ((6, 0), (4, 2), (25, 0)),
        ((6, 0), (5, 1), (10, 0)),
        ((6, 0), (5, 2), (10, 0)),
        ((6, 0), (7, 1), (19, 0)),
        ((6, 0), (7, 2), (19, 0)),
        ((6, 0), (8, 1), (13, 0)),
        ((6, 0), (8, 2), (13, 0)),
        ((6, 0), (14, 1), (17, 0)),
        ((6, 0), (14, 2), (17, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_122_line_families() -> None:
    """Line families on the anchored a=(1,2,2) orbit."""
    triples = [
        ((7, 0), (0, 0), (24, 1)),
        ((7, 0), (0, 1), (24, 0)),
        ((7, 0), (1, 0), (25, 1)),
        ((7, 0), (1, 1), (25, 0)),
        ((7, 0), (3, 0), (16, 1)),
        ((7, 0), (3, 1), (16, 0)),
        ((7, 0), (4, 0), (15, 1)),
        ((7, 0), (4, 1), (15, 0)),
        ((7, 0), (5, 0), (22, 1)),
        ((7, 0), (5, 1), (22, 0)),
        ((7, 0), (6, 0), (20, 1)),
        ((7, 0), (6, 1), (20, 0)),
        ((7, 0), (8, 0), (11, 1)),
        ((7, 0), (8, 1), (11, 0)),
        ((7, 0), (13, 0), (17, 1)),
        ((7, 0), (13, 1), (17, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_122_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(1,2,2) orbit."""
    triples = [
        ((7, 0), (0, 1), (22, 0)),
        ((7, 0), (0, 2), (22, 0)),
        ((7, 0), (1, 1), (15, 0)),
        ((7, 0), (1, 2), (15, 0)),
        ((7, 0), (3, 1), (6, 0)),
        ((7, 0), (3, 2), (6, 0)),
        ((7, 0), (4, 1), (25, 0)),
        ((7, 0), (4, 2), (25, 0)),
        ((7, 0), (5, 1), (24, 0)),
        ((7, 0), (5, 2), (24, 0)),
        ((7, 0), (8, 1), (13, 0)),
        ((7, 0), (8, 2), (13, 0)),
        ((7, 0), (11, 1), (17, 0)),
        ((7, 0), (11, 2), (17, 0)),
        ((7, 0), (16, 1), (20, 0)),
        ((7, 0), (16, 2), (20, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_111_line_families() -> None:
    """Line families on the anchored a=(1,1,1) orbit."""
    triples = [
        ((8, 0), (0, 0), (25, 1)),
        ((8, 0), (0, 1), (25, 0)),
        ((8, 0), (2, 0), (24, 1)),
        ((8, 0), (2, 1), (24, 0)),
        ((8, 0), (3, 0), (23, 1)),
        ((8, 0), (3, 1), (23, 0)),
        ((8, 0), (4, 0), (21, 1)),
        ((8, 0), (4, 1), (21, 0)),
        ((8, 0), (5, 0), (16, 1)),
        ((8, 0), (5, 1), (16, 0)),
        ((8, 0), (6, 0), (15, 1)),
        ((8, 0), (6, 1), (15, 0)),
        ((8, 0), (7, 0), (14, 1)),
        ((8, 0), (7, 1), (14, 0)),
        ((8, 0), (12, 0), (17, 1)),
        ((8, 0), (12, 1), (17, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_111_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(1,1,1) orbit."""
    triples = [
        ((8, 0), (0, 1), (21, 0)),
        ((8, 0), (0, 2), (21, 0)),
        ((8, 0), (2, 1), (16, 0)),
        ((8, 0), (2, 2), (16, 0)),
        ((8, 0), (3, 1), (6, 0)),
        ((8, 0), (3, 2), (6, 0)),
        ((8, 0), (4, 1), (25, 0)),
        ((8, 0), (4, 2), (25, 0)),
        ((8, 0), (5, 1), (24, 0)),
        ((8, 0), (5, 2), (24, 0)),
        ((8, 0), (7, 1), (12, 0)),
        ((8, 0), (7, 2), (12, 0)),
        ((8, 0), (14, 1), (17, 0)),
        ((8, 0), (14, 2), (17, 0)),
        ((8, 0), (15, 1), (23, 0)),
        ((8, 0), (15, 2), (23, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_222_line_families() -> None:
    """Line families on the anchored a=(2,2,2) orbit."""
    triples = [
        ((9, 0), (1, 0), (12, 1)),
        ((9, 0), (1, 1), (12, 0)),
        ((9, 0), (2, 0), (11, 1)),
        ((9, 0), (2, 1), (11, 0)),
        ((9, 0), (3, 0), (10, 1)),
        ((9, 0), (3, 1), (10, 0)),
        ((9, 0), (5, 0), (26, 1)),
        ((9, 0), (5, 1), (26, 0)),
        ((9, 0), (13, 0), (21, 1)),
        ((9, 0), (13, 1), (21, 0)),
        ((9, 0), (14, 0), (20, 1)),
        ((9, 0), (14, 1), (20, 0)),
        ((9, 0), (15, 0), (19, 1)),
        ((9, 0), (15, 1), (19, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_222_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(2,2,2) orbit."""
    triples = [
        ((9, 0), (0, 1), (21, 0)),
        ((9, 0), (0, 2), (21, 0)),
        ((9, 0), (1, 1), (15, 0)),
        ((9, 0), (1, 2), (15, 0)),
        ((9, 0), (2, 1), (20, 0)),
        ((9, 0), (2, 2), (20, 0)),
        ((9, 0), (3, 1), (26, 0)),
        ((9, 0), (3, 2), (26, 0)),
        ((9, 0), (5, 1), (10, 0)),
        ((9, 0), (5, 2), (10, 0)),
        ((9, 0), (11, 1), (14, 0)),
        ((9, 0), (11, 2), (14, 0)),
        ((9, 0), (12, 1), (19, 0)),
        ((9, 0), (12, 2), (19, 0)),
        ((9, 0), (13, 1), (18, 0)),
        ((9, 0), (13, 2), (18, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_211_line_families() -> None:
    """Line families on the anchored a=(2,1,1) orbit."""
    triples = [
        ((10, 0), (0, 0), (19, 1)),
        ((10, 0), (0, 1), (19, 0)),
        ((10, 0), (1, 0), (14, 1)),
        ((10, 0), (1, 1), (14, 0)),
        ((10, 0), (2, 0), (13, 1)),
        ((10, 0), (2, 1), (13, 0)),
        ((10, 0), (4, 0), (26, 1)),
        ((10, 0), (4, 1), (26, 0)),
        ((10, 0), (6, 0), (9, 1)),
        ((10, 0), (6, 1), (9, 0)),
        ((10, 0), (11, 0), (23, 1)),
        ((10, 0), (11, 1), (23, 0)),
        ((10, 0), (12, 0), (22, 1)),
        ((10, 0), (12, 1), (22, 0)),
        ((10, 0), (16, 0), (18, 1)),
        ((10, 0), (16, 1), (18, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_211_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(2,1,1) orbit."""
    triples = [
        ((10, 0), (0, 1), (22, 0)),
        ((10, 0), (0, 2), (22, 0)),
        ((10, 0), (1, 1), (23, 0)),
        ((10, 0), (1, 2), (23, 0)),
        ((10, 0), (2, 1), (16, 0)),
        ((10, 0), (2, 2), (16, 0)),
        ((10, 0), (4, 1), (9, 0)),
        ((10, 0), (4, 2), (9, 0)),
        ((10, 0), (6, 1), (26, 0)),
        ((10, 0), (6, 2), (26, 0)),
        ((10, 0), (11, 1), (14, 0)),
        ((10, 0), (11, 2), (14, 0)),
        ((10, 0), (12, 1), (19, 0)),
        ((10, 0), (12, 2), (19, 0)),
        ((10, 0), (13, 1), (18, 0)),
        ((10, 0), (13, 2), (18, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_102_line_families() -> None:
    """Line families on the anchored a=(1,0,2) orbit."""
    triples = [
        ((11, 0), (1, 0), (24, 1)),
        ((11, 0), (1, 0), (24, 2)),
        ((11, 0), (1, 1), (24, 0)),
        ((11, 0), (1, 2), (24, 0)),
        ((11, 0), (3, 0), (22, 1)),
        ((11, 0), (3, 0), (22, 2)),
        ((11, 0), (3, 1), (22, 0)),
        ((11, 0), (3, 2), (22, 0)),
        ((11, 0), (4, 0), (20, 1)),
        ((11, 0), (4, 0), (20, 2)),
        ((11, 0), (4, 1), (20, 0)),
        ((11, 0), (4, 2), (20, 0)),
        ((11, 0), (7, 0), (18, 1)),
        ((11, 0), (7, 0), (18, 2)),
        ((11, 0), (7, 1), (18, 0)),
        ((11, 0), (7, 2), (18, 0)),
        ((11, 0), (9, 0), (16, 1)),
        ((11, 0), (9, 0), (16, 2)),
        ((11, 0), (9, 1), (16, 0)),
        ((11, 0), (9, 2), (16, 0)),
        ((11, 0), (10, 0), (15, 1)),
        ((11, 0), (10, 0), (15, 2)),
        ((11, 0), (10, 1), (15, 0)),
        ((11, 0), (10, 2), (15, 0)),
        ((11, 0), (12, 0), (13, 1)),
        ((11, 0), (12, 0), (13, 2)),
        ((11, 0), (12, 1), (13, 0)),
        ((11, 0), (12, 2), (13, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_102_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(1,0,2) orbit."""
    triples = [
        ((11, 0), (0, 1), (22, 0)),
        ((11, 0), (0, 2), (22, 0)),
        ((11, 0), (1, 1), (15, 0)),
        ((11, 0), (1, 2), (15, 0)),
        ((11, 0), (3, 1), (26, 0)),
        ((11, 0), (3, 2), (26, 0)),
        ((11, 0), (4, 1), (9, 0)),
        ((11, 0), (4, 2), (9, 0)),
        ((11, 0), (7, 1), (12, 0)),
        ((11, 0), (7, 2), (12, 0)),
        ((11, 0), (10, 1), (24, 0)),
        ((11, 0), (10, 2), (24, 0)),
        ((11, 0), (13, 1), (18, 0)),
        ((11, 0), (13, 2), (18, 0)),
        ((11, 0), (16, 1), (20, 0)),
        ((11, 0), (16, 2), (20, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_121_line_families() -> None:
    """Line families on the anchored a=(1,2,1) orbit."""
    triples = [
        ((12, 0), (0, 0), (24, 1)),
        ((12, 0), (0, 0), (24, 2)),
        ((12, 0), (0, 1), (24, 0)),
        ((12, 0), (0, 2), (24, 0)),
        ((12, 0), (2, 0), (26, 1)),
        ((12, 0), (2, 0), (26, 2)),
        ((12, 0), (2, 1), (26, 0)),
        ((12, 0), (2, 2), (26, 0)),
        ((12, 0), (3, 0), (16, 1)),
        ((12, 0), (3, 0), (16, 2)),
        ((12, 0), (3, 1), (16, 0)),
        ((12, 0), (3, 2), (16, 0)),
        ((12, 0), (4, 0), (15, 1)),
        ((12, 0), (4, 0), (15, 2)),
        ((12, 0), (4, 1), (15, 0)),
        ((12, 0), (4, 2), (15, 0)),
        ((12, 0), (8, 0), (11, 1)),
        ((12, 0), (8, 0), (11, 2)),
        ((12, 0), (8, 1), (11, 0)),
        ((12, 0), (8, 2), (11, 0)),
        ((12, 0), (9, 0), (23, 1)),
        ((12, 0), (9, 0), (23, 2)),
        ((12, 0), (9, 1), (23, 0)),
        ((12, 0), (9, 2), (23, 0)),
        ((12, 0), (10, 0), (21, 1)),
        ((12, 0), (10, 0), (21, 2)),
        ((12, 0), (10, 1), (21, 0)),
        ((12, 0), (10, 2), (21, 0)),
        ((12, 0), (14, 0), (18, 1)),
        ((12, 0), (14, 0), (18, 2)),
        ((12, 0), (14, 1), (18, 0)),
        ((12, 0), (14, 2), (18, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_121_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(1,2,1) orbit."""
    triples = [
        ((12, 0), (0, 1), (21, 0)),
        ((12, 0), (0, 2), (21, 0)),
        ((12, 0), (2, 1), (16, 0)),
        ((12, 0), (2, 2), (16, 0)),
        ((12, 0), (3, 1), (26, 0)),
        ((12, 0), (3, 2), (26, 0)),
        ((12, 0), (4, 1), (9, 0)),
        ((12, 0), (4, 2), (9, 0)),
        ((12, 0), (8, 1), (18, 0)),
        ((12, 0), (8, 2), (18, 0)),
        ((12, 0), (10, 1), (24, 0)),
        ((12, 0), (10, 2), (24, 0)),
        ((12, 0), (11, 1), (14, 0)),
        ((12, 0), (11, 2), (14, 0)),
        ((12, 0), (15, 1), (23, 0)),
        ((12, 0), (15, 2), (23, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_112_line_families() -> None:
    """Line families on the anchored a=(1,1,2) orbit."""
    triples = [
        ((13, 0), (1, 0), (26, 1)),
        ((13, 0), (1, 0), (26, 2)),
        ((13, 0), (1, 1), (26, 0)),
        ((13, 0), (1, 2), (26, 0)),
        ((13, 0), (5, 0), (16, 1)),
        ((13, 0), (5, 0), (16, 2)),
        ((13, 0), (5, 1), (16, 0)),
        ((13, 0), (5, 2), (16, 0)),
        ((13, 0), (6, 0), (15, 1)),
        ((13, 0), (6, 0), (15, 2)),
        ((13, 0), (6, 1), (15, 0)),
        ((13, 0), (6, 2), (15, 0)),
        ((13, 0), (7, 0), (14, 1)),
        ((13, 0), (7, 0), (14, 2)),
        ((13, 0), (7, 1), (14, 0)),
        ((13, 0), (7, 2), (14, 0)),
        ((13, 0), (9, 0), (22, 1)),
        ((13, 0), (9, 0), (22, 2)),
        ((13, 0), (9, 1), (22, 0)),
        ((13, 0), (9, 2), (22, 0)),
        ((13, 0), (10, 0), (20, 1)),
        ((13, 0), (10, 0), (20, 2)),
        ((13, 0), (10, 1), (20, 0)),
        ((13, 0), (10, 2), (20, 0)),
        ((13, 0), (11, 0), (19, 1)),
        ((13, 0), (11, 0), (19, 2)),
        ((13, 0), (11, 1), (19, 0)),
        ((13, 0), (11, 2), (19, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_112_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(1,1,2) orbit."""
    triples = [
        ((13, 0), (0, 1), (22, 0)),
        ((13, 0), (0, 2), (22, 0)),
        ((13, 0), (1, 1), (15, 0)),
        ((13, 0), (1, 2), (15, 0)),
        ((13, 0), (5, 1), (10, 0)),
        ((13, 0), (5, 2), (10, 0)),
        ((13, 0), (6, 1), (26, 0)),
        ((13, 0), (6, 2), (26, 0)),
        ((13, 0), (7, 1), (19, 0)),
        ((13, 0), (7, 2), (19, 0)),
        ((13, 0), (9, 1), (25, 0)),
        ((13, 0), (9, 2), (25, 0)),
        ((13, 0), (11, 1), (14, 0)),
        ((13, 0), (11, 2), (14, 0)),
        ((13, 0), (16, 1), (20, 0)),
        ((13, 0), (16, 2), (20, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_110_line_families() -> None:
    """Line families on the anchored a=(1,1,0) orbit."""
    triples = [
        ((18, 0), (1, 0), (26, 1)),
        ((18, 0), (1, 0), (26, 2)),
        ((18, 0), (1, 1), (26, 0)),
        ((18, 0), (1, 2), (26, 0)),
        ((18, 0), (2, 0), (24, 1)),
        ((18, 0), (2, 0), (24, 2)),
        ((18, 0), (2, 1), (24, 0)),
        ((18, 0), (2, 2), (24, 0)),
        ((18, 0), (3, 0), (23, 1)),
        ((18, 0), (3, 0), (23, 2)),
        ((18, 0), (3, 1), (23, 0)),
        ((18, 0), (3, 2), (23, 0)),
        ((18, 0), (4, 0), (21, 1)),
        ((18, 0), (4, 0), (21, 2)),
        ((18, 0), (4, 1), (21, 0)),
        ((18, 0), (4, 2), (21, 0)),
        ((18, 0), (9, 0), (22, 1)),
        ((18, 0), (9, 0), (22, 2)),
        ((18, 0), (9, 1), (22, 0)),
        ((18, 0), (9, 2), (22, 0)),
        ((18, 0), (10, 0), (20, 1)),
        ((18, 0), (10, 0), (20, 2)),
        ((18, 0), (10, 1), (20, 0)),
        ((18, 0), (10, 2), (20, 0)),
        ((18, 0), (11, 0), (19, 1)),
        ((18, 0), (11, 0), (19, 2)),
        ((18, 0), (11, 1), (19, 0)),
        ((18, 0), (11, 2), (19, 0)),
        ((18, 0), (12, 0), (17, 1)),
        ((18, 0), (12, 0), (17, 2)),
        ((18, 0), (12, 1), (17, 0)),
        ((18, 0), (12, 2), (17, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_110_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(1,1,0) orbit."""
    triples = [
        ((18, 0), (1, 1), (23, 0)),
        ((18, 0), (1, 2), (23, 0)),
        ((18, 0), (2, 1), (20, 0)),
        ((18, 0), (2, 2), (20, 0)),
        ((18, 0), (3, 1), (26, 0)),
        ((18, 0), (3, 2), (26, 0)),
        ((18, 0), (4, 1), (9, 0)),
        ((18, 0), (4, 2), (9, 0)),
        ((18, 0), (10, 1), (24, 0)),
        ((18, 0), (10, 2), (24, 0)),
        ((18, 0), (11, 1), (17, 0)),
        ((18, 0), (11, 2), (17, 0)),
        ((18, 0), (12, 1), (19, 0)),
        ((18, 0), (12, 2), (19, 0)),
        ((18, 0), (21, 1), (22, 0)),
        ((18, 0), (21, 2), (22, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_120_line_families() -> None:
    """Line families on the anchored a=(1,2,0) orbit."""
    triples = [
        ((19, 0), (1, 0), (25, 1)),
        ((19, 0), (1, 0), (25, 2)),
        ((19, 0), (1, 1), (25, 0)),
        ((19, 0), (1, 2), (25, 0)),
        ((19, 0), (2, 0), (26, 1)),
        ((19, 0), (2, 0), (26, 2)),
        ((19, 0), (2, 1), (26, 0)),
        ((19, 0), (2, 2), (26, 0)),
        ((19, 0), (5, 0), (22, 1)),
        ((19, 0), (5, 0), (22, 2)),
        ((19, 0), (5, 1), (22, 0)),
        ((19, 0), (5, 2), (22, 0)),
        ((19, 0), (6, 0), (20, 1)),
        ((19, 0), (6, 0), (20, 2)),
        ((19, 0), (6, 1), (20, 0)),
        ((19, 0), (6, 2), (20, 0)),
        ((19, 0), (9, 0), (23, 1)),
        ((19, 0), (9, 0), (23, 2)),
        ((19, 0), (9, 1), (23, 0)),
        ((19, 0), (9, 2), (23, 0)),
        ((19, 0), (10, 0), (21, 1)),
        ((19, 0), (10, 0), (21, 2)),
        ((19, 0), (10, 1), (21, 0)),
        ((19, 0), (10, 2), (21, 0)),
        ((19, 0), (13, 0), (17, 1)),
        ((19, 0), (13, 0), (17, 2)),
        ((19, 0), (13, 1), (17, 0)),
        ((19, 0), (13, 2), (17, 0)),
        ((19, 0), (14, 0), (18, 1)),
        ((19, 0), (14, 0), (18, 2)),
        ((19, 0), (14, 1), (18, 0)),
        ((19, 0), (14, 2), (18, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_120_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(1,2,0) orbit."""
    triples = [
        ((19, 0), (1, 1), (23, 0)),
        ((19, 0), (1, 2), (23, 0)),
        ((19, 0), (2, 1), (20, 0)),
        ((19, 0), (2, 2), (20, 0)),
        ((19, 0), (5, 1), (10, 0)),
        ((19, 0), (5, 2), (10, 0)),
        ((19, 0), (6, 1), (26, 0)),
        ((19, 0), (6, 2), (26, 0)),
        ((19, 0), (9, 1), (25, 0)),
        ((19, 0), (9, 2), (25, 0)),
        ((19, 0), (13, 1), (18, 0)),
        ((19, 0), (13, 2), (18, 0)),
        ((19, 0), (14, 1), (17, 0)),
        ((19, 0), (14, 2), (17, 0)),
        ((19, 0), (21, 1), (22, 0)),
        ((19, 0), (21, 2), (22, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_101_line_families() -> None:
    """Line families on the anchored a=(1,0,1) orbit."""
    triples = [
        ((14, 0), (0, 0), (26, 1)),
        ((14, 0), (0, 0), (26, 2)),
        ((14, 0), (0, 1), (26, 0)),
        ((14, 0), (0, 2), (26, 0)),
        ((14, 0), (2, 0), (25, 1)),
        ((14, 0), (2, 0), (25, 2)),
        ((14, 0), (2, 1), (25, 0)),
        ((14, 0), (2, 2), (25, 0)),
        ((14, 0), (5, 0), (23, 1)),
        ((14, 0), (5, 0), (23, 2)),
        ((14, 0), (5, 1), (23, 0)),
        ((14, 0), (5, 2), (23, 0)),
        ((14, 0), (6, 0), (21, 1)),
        ((14, 0), (6, 0), (21, 2)),
        ((14, 0), (6, 1), (21, 0)),
        ((14, 0), (6, 2), (21, 0)),
        ((14, 0), (8, 0), (19, 1)),
        ((14, 0), (8, 0), (19, 2)),
        ((14, 0), (8, 1), (19, 0)),
        ((14, 0), (8, 2), (19, 0)),
        ((14, 0), (9, 0), (16, 1)),
        ((14, 0), (9, 0), (16, 2)),
        ((14, 0), (9, 1), (16, 0)),
        ((14, 0), (9, 2), (16, 0)),
        ((14, 0), (10, 0), (15, 1)),
        ((14, 0), (10, 0), (15, 2)),
        ((14, 0), (10, 1), (15, 0)),
        ((14, 0), (10, 2), (15, 0)),
        ((14, 0), (12, 0), (13, 1)),
        ((14, 0), (12, 0), (13, 2)),
        ((14, 0), (12, 1), (13, 0)),
        ((14, 0), (12, 2), (13, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_101_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(1,0,1) orbit."""
    triples = [
        ((14, 0), (0, 1), (21, 0)),
        ((14, 0), (0, 2), (21, 0)),
        ((14, 0), (2, 1), (16, 0)),
        ((14, 0), (2, 2), (16, 0)),
        ((14, 0), (5, 1), (10, 0)),
        ((14, 0), (5, 2), (10, 0)),
        ((14, 0), (6, 1), (26, 0)),
        ((14, 0), (6, 2), (26, 0)),
        ((14, 0), (8, 1), (13, 0)),
        ((14, 0), (8, 2), (13, 0)),
        ((14, 0), (9, 1), (25, 0)),
        ((14, 0), (9, 2), (25, 0)),
        ((14, 0), (12, 1), (19, 0)),
        ((14, 0), (12, 2), (19, 0)),
        ((14, 0), (15, 1), (23, 0)),
        ((14, 0), (15, 2), (23, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_021_line_families() -> None:
    """Line families on the anchored a=(0,2,1) orbit."""
    triples = [
        ((15, 0), (0, 0), (20, 1)),
        ((15, 0), (0, 0), (20, 2)),
        ((15, 0), (0, 1), (20, 0)),
        ((15, 0), (0, 2), (20, 0)),
        ((15, 0), (3, 0), (13, 1)),
        ((15, 0), (3, 0), (13, 2)),
        ((15, 0), (3, 1), (13, 0)),
        ((15, 0), (3, 2), (13, 0)),
        ((15, 0), (5, 0), (11, 1)),
        ((15, 0), (5, 0), (11, 2)),
        ((15, 0), (5, 1), (11, 0)),
        ((15, 0), (5, 2), (11, 0)),
        ((15, 0), (7, 0), (9, 1)),
        ((15, 0), (7, 0), (9, 2)),
        ((15, 0), (7, 1), (9, 0)),
        ((15, 0), (7, 2), (9, 0)),
        ((15, 0), (8, 0), (26, 1)),
        ((15, 0), (8, 0), (26, 2)),
        ((15, 0), (8, 1), (26, 0)),
        ((15, 0), (8, 2), (26, 0)),
        ((15, 0), (12, 0), (25, 1)),
        ((15, 0), (12, 0), (25, 2)),
        ((15, 0), (12, 1), (25, 0)),
        ((15, 0), (12, 2), (25, 0)),
        ((15, 0), (14, 0), (24, 1)),
        ((15, 0), (14, 0), (24, 2)),
        ((15, 0), (14, 1), (24, 0)),
        ((15, 0), (14, 2), (24, 0)),
        ((15, 0), (16, 0), (21, 1)),
        ((15, 0), (16, 0), (21, 2)),
        ((15, 0), (16, 1), (21, 0)),
        ((15, 0), (16, 2), (21, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_021_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(0,2,1) orbit."""
    triples = [
        ((15, 0), (0, 1), (21, 0)),
        ((15, 0), (0, 2), (21, 0)),
        ((15, 0), (3, 1), (26, 0)),
        ((15, 0), (3, 2), (26, 0)),
        ((15, 0), (5, 1), (24, 0)),
        ((15, 0), (5, 2), (24, 0)),
        ((15, 0), (7, 1), (12, 0)),
        ((15, 0), (7, 2), (12, 0)),
        ((15, 0), (8, 1), (13, 0)),
        ((15, 0), (8, 2), (13, 0)),
        ((15, 0), (9, 1), (25, 0)),
        ((15, 0), (9, 2), (25, 0)),
        ((15, 0), (11, 1), (14, 0)),
        ((15, 0), (11, 2), (14, 0)),
        ((15, 0), (16, 1), (20, 0)),
        ((15, 0), (16, 2), (20, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_011_line_families() -> None:
    """Line families on the anchored a=(0,1,1) orbit."""
    triples = [
        ((16, 0), (0, 0), (23, 1)),
        ((16, 0), (0, 0), (23, 2)),
        ((16, 0), (0, 1), (23, 0)),
        ((16, 0), (0, 2), (23, 0)),
        ((16, 0), (4, 0), (14, 1)),
        ((16, 0), (4, 0), (14, 2)),
        ((16, 0), (4, 1), (14, 0)),
        ((16, 0), (4, 2), (14, 0)),
        ((16, 0), (6, 0), (12, 1)),
        ((16, 0), (6, 0), (12, 2)),
        ((16, 0), (6, 1), (12, 0)),
        ((16, 0), (6, 2), (12, 0)),
        ((16, 0), (7, 0), (26, 1)),
        ((16, 0), (7, 0), (26, 2)),
        ((16, 0), (7, 1), (26, 0)),
        ((16, 0), (7, 2), (26, 0)),
        ((16, 0), (8, 0), (10, 1)),
        ((16, 0), (8, 0), (10, 2)),
        ((16, 0), (8, 1), (10, 0)),
        ((16, 0), (8, 2), (10, 0)),
        ((16, 0), (11, 0), (25, 1)),
        ((16, 0), (11, 0), (25, 2)),
        ((16, 0), (11, 1), (25, 0)),
        ((16, 0), (11, 2), (25, 0)),
        ((16, 0), (13, 0), (24, 1)),
        ((16, 0), (13, 0), (24, 2)),
        ((16, 0), (13, 1), (24, 0)),
        ((16, 0), (13, 2), (24, 0)),
        ((16, 0), (15, 0), (22, 1)),
        ((16, 0), (15, 0), (22, 2)),
        ((16, 0), (15, 1), (22, 0)),
        ((16, 0), (15, 2), (22, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_011_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(0,1,1) orbit."""
    triples = [
        ((16, 0), (0, 1), (22, 0)),
        ((16, 0), (0, 2), (22, 0)),
        ((16, 0), (4, 1), (25, 0)),
        ((16, 0), (4, 2), (25, 0)),
        ((16, 0), (6, 1), (26, 0)),
        ((16, 0), (6, 2), (26, 0)),
        ((16, 0), (7, 1), (12, 0)),
        ((16, 0), (7, 2), (12, 0)),
        ((16, 0), (8, 1), (13, 0)),
        ((16, 0), (8, 2), (13, 0)),
        ((16, 0), (10, 1), (24, 0)),
        ((16, 0), (10, 2), (24, 0)),
        ((16, 0), (11, 1), (14, 0)),
        ((16, 0), (11, 2), (14, 0)),
        ((16, 0), (15, 1), (23, 0)),
        ((16, 0), (15, 2), (23, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_001_line_families() -> None:
    """Line families on the anchored a=(0,0,1) orbit."""
    triples = [
        ((21, 0), (2, 0), (15, 1)),
        ((21, 0), (2, 0), (15, 2)),
        ((21, 0), (2, 1), (15, 0)),
        ((21, 0), (2, 2), (15, 0)),
        ((21, 0), (3, 0), (14, 1)),
        ((21, 0), (3, 0), (14, 2)),
        ((21, 0), (3, 1), (14, 0)),
        ((21, 0), (3, 2), (14, 0)),
        ((21, 0), (5, 0), (12, 1)),
        ((21, 0), (5, 0), (12, 2)),
        ((21, 0), (5, 1), (12, 0)),
        ((21, 0), (5, 2), (12, 0)),
        ((21, 0), (8, 0), (9, 1)),
        ((21, 0), (8, 0), (9, 2)),
        ((21, 0), (8, 1), (9, 0)),
        ((21, 0), (8, 2), (9, 0)),
        ((21, 0), (17, 0), (26, 1)),
        ((21, 0), (17, 0), (26, 2)),
        ((21, 0), (17, 1), (26, 0)),
        ((21, 0), (17, 2), (26, 0)),
        ((21, 0), (18, 0), (25, 1)),
        ((21, 0), (18, 0), (25, 2)),
        ((21, 0), (18, 1), (25, 0)),
        ((21, 0), (18, 2), (25, 0)),
        ((21, 0), (19, 0), (24, 1)),
        ((21, 0), (19, 0), (24, 2)),
        ((21, 0), (19, 1), (24, 0)),
        ((21, 0), (19, 2), (24, 0)),
        ((21, 0), (20, 0), (23, 1)),
        ((21, 0), (20, 0), (23, 2)),
        ((21, 0), (20, 1), (23, 0)),
        ((21, 0), (20, 2), (23, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_001_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(0,0,1) orbit."""
    triples = [
        ((21, 0), (2, 1), (20, 0)),
        ((21, 0), (2, 2), (20, 0)),
        ((21, 0), (3, 1), (26, 0)),
        ((21, 0), (3, 2), (26, 0)),
        ((21, 0), (5, 1), (24, 0)),
        ((21, 0), (5, 2), (24, 0)),
        ((21, 0), (8, 1), (18, 0)),
        ((21, 0), (8, 2), (18, 0)),
        ((21, 0), (9, 1), (25, 0)),
        ((21, 0), (9, 2), (25, 0)),
        ((21, 0), (12, 1), (19, 0)),
        ((21, 0), (12, 2), (19, 0)),
        ((21, 0), (14, 1), (17, 0)),
        ((21, 0), (14, 2), (17, 0)),
        ((21, 0), (15, 1), (23, 0)),
        ((21, 0), (15, 2), (23, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_010_line_families() -> None:
    """The az=0 line frontier closes by a constant-target W/V law."""
    triples = [
        ((20, 0), (1, 0), (21, 1)),
        ((20, 0), (1, 0), (21, 2)),
        ((20, 0), (1, 1), (21, 0)),
        ((20, 0), (1, 2), (21, 0)),
        ((20, 0), (3, 0), (19, 1)),
        ((20, 0), (3, 0), (19, 2)),
        ((20, 0), (3, 1), (19, 0)),
        ((20, 0), (3, 2), (19, 0)),
        ((20, 0), (5, 0), (18, 1)),
        ((20, 0), (5, 0), (18, 2)),
        ((20, 0), (5, 1), (18, 0)),
        ((20, 0), (5, 2), (18, 0)),
        ((20, 0), (9, 0), (17, 1)),
        ((20, 0), (9, 0), (17, 2)),
        ((20, 0), (9, 1), (17, 0)),
        ((20, 0), (9, 2), (17, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_010_line_families_on_other_g1_colors() -> (
    None
):
    """The az=0 line branch lifts across the nonzero g1 colors as well."""
    triples = [
        ((20, 1), (1, 1), (21, 0)),
        ((20, 1), (1, 0), (21, 1)),
        ((20, 2), (1, 2), (21, 0)),
        ((20, 2), (1, 0), (21, 2)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_leaves_anchor_010_overlap_representatives_zero() -> None:
    """The az=0 overlap slice is symbolic-only here and must stay inactive."""
    triples = [
        ((20, 0), (0, 1), (21, 0)),
        ((20, 0), (1, 1), (23, 0)),
        ((20, 0), (3, 1), (6, 0)),
        ((20, 0), (5, 1), (10, 0)),
        ((20, 0), (14, 1), (17, 0)),
    ]
    for triple in triples:
        toe, linfty = _build_linfty()
        x = basis_elem_g1(toe, triple[0])
        y = basis_elem_g2(toe, triple[1])
        z = basis_elem_g2(toe, triple[2])

        baseline = linfty.homotopy_jacobi(x, y, z)
        assert max_abs(baseline) < 1e-10, triple

        linfty.enable_ce2_global_predictor()
        repaired = linfty.homotopy_jacobi(x, y, z)
        assert max_abs(repaired) < 1e-10, triple


def test_global_ce2_predictor_cancels_anchor_010_target16_line_families() -> None:
    """The second az=0 line branch lands on the fixed target i=16 orbit."""
    triples = [
        ((20, 0), (7, 0), (26, 1)),
        ((20, 0), (7, 0), (26, 2)),
        ((20, 0), (7, 1), (26, 0)),
        ((20, 0), (7, 2), (26, 0)),
        ((20, 0), (11, 0), (25, 1)),
        ((20, 0), (11, 0), (25, 2)),
        ((20, 0), (11, 1), (25, 0)),
        ((20, 0), (11, 2), (25, 0)),
        ((20, 0), (13, 0), (24, 1)),
        ((20, 0), (13, 0), (24, 2)),
        ((20, 0), (13, 1), (24, 0)),
        ((20, 0), (13, 2), (24, 0)),
        ((20, 0), (15, 0), (22, 1)),
        ((20, 0), (15, 0), (22, 2)),
        ((20, 0), (15, 1), (22, 0)),
        ((20, 0), (15, 2), (22, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_010_overlap_families() -> None:
    """The remaining az=0 overlap witnesses close in sparse 1/108 U/V pairs."""
    triples = [
        ((20, 0), (7, 1), (19, 0)),
        ((20, 0), (7, 2), (19, 0)),
        ((20, 0), (9, 1), (25, 0)),
        ((20, 0), (9, 2), (25, 0)),
        ((20, 0), (11, 1), (17, 0)),
        ((20, 0), (11, 2), (17, 0)),
        ((20, 0), (13, 1), (18, 0)),
        ((20, 0), (13, 2), (18, 0)),
        ((20, 0), (21, 1), (22, 0)),
        ((20, 0), (21, 2), (22, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_a01_b00_reflection_u_families() -> None:
    """The next z=1,2 frontier against b_i=0 is a reflected 1/6 U-family."""
    triples = [
        ((16, 0), (0, 0), (24, 1)),
        ((16, 0), (0, 0), (24, 2)),
        ((16, 0), (0, 0), (25, 1)),
        ((16, 0), (0, 0), (25, 2)),
        ((16, 0), (0, 0), (26, 1)),
        ((16, 0), (0, 0), (26, 2)),
        ((2, 0), (0, 0), (17, 1)),
        ((2, 0), (0, 0), (17, 2)),
        ((2, 0), (0, 0), (18, 1)),
        ((2, 0), (0, 0), (18, 2)),
        ((2, 0), (0, 0), (19, 1)),
        ((2, 0), (0, 0), (19, 2)),
        ((16, 1), (0, 1), (24, 0)),
        ((16, 1), (0, 1), (24, 2)),
        ((16, 2), (0, 2), (24, 0)),
        ((16, 2), (0, 2), (24, 1)),
        ((2, 1), (0, 1), (17, 0)),
        ((2, 1), (0, 1), (17, 2)),
        ((2, 2), (0, 2), (17, 0)),
        ((2, 2), (0, 2), (17, 1)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_a01_b0_reflection_uv12_families() -> None:
    """Color-swapped reflected companion on b_i=0 closes at coefficient 1/12."""
    triples = [
        ((16, 0), (0, 1), (24, 0)),
        ((16, 0), (0, 1), (25, 0)),
        ((16, 0), (0, 1), (26, 0)),
        ((16, 0), (0, 2), (24, 0)),
        ((16, 0), (0, 2), (25, 0)),
        ((16, 0), (0, 2), (26, 0)),
        ((2, 0), (0, 1), (17, 0)),
        ((2, 0), (0, 1), (18, 0)),
        ((2, 0), (0, 1), (19, 0)),
        ((2, 0), (0, 2), (17, 0)),
        ((2, 0), (0, 2), (18, 0)),
        ((2, 0), (0, 2), (19, 0)),
        ((16, 1), (0, 0), (24, 1)),
        ((16, 1), (0, 2), (24, 1)),
        ((2, 1), (0, 0), (17, 1)),
        ((2, 1), (0, 2), (17, 1)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_a01_source1_line_u_families() -> None:
    """The unresolved source-id-1 sheet on a=(0,1,2) closes with a 1/6 U law."""
    triples = [
        ((2, 0), (1, 0), (8, 1)),
        ((2, 0), (1, 0), (8, 2)),
        ((2, 0), (1, 0), (12, 1)),
        ((2, 0), (1, 0), (12, 2)),
        ((2, 0), (1, 0), (14, 1)),
        ((2, 0), (1, 0), (14, 2)),
        ((2, 1), (1, 1), (8, 0)),
        ((2, 1), (1, 1), (8, 2)),
        ((2, 1), (1, 1), (12, 0)),
        ((2, 1), (1, 1), (12, 2)),
        ((2, 2), (1, 2), (8, 0)),
        ((2, 2), (1, 2), (14, 1)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_a01_source1_line_uv12_families() -> None:
    """Off-color companions on the source-id-1 sheet add the 1/12 e6 compensator."""
    triples = [
        ((2, 0), (1, 1), (8, 0)),
        ((2, 0), (1, 1), (12, 0)),
        ((2, 0), (1, 2), (14, 0)),
        ((2, 1), (1, 0), (8, 1)),
        ((2, 1), (1, 0), (12, 1)),
        ((2, 1), (1, 2), (14, 1)),
        ((2, 2), (1, 0), (8, 2)),
        ((2, 2), (1, 1), (12, 2)),
        ((2, 2), (1, 1), (14, 2)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_a01_source1_z0_line_u_families() -> None:
    """The a=(0,1,0) source-id-1 sheet closes with the same 1/6 transport law."""
    triples = [
        ((20, 0), (1, 0), (24, 1)),
        ((20, 0), (1, 0), (24, 2)),
        ((20, 0), (1, 0), (25, 1)),
        ((20, 0), (1, 0), (25, 2)),
        ((20, 1), (1, 1), (24, 0)),
        ((20, 1), (1, 1), (24, 2)),
        ((20, 2), (1, 2), (25, 0)),
        ((20, 2), (1, 2), (26, 1)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_a01_source1_z0_line_uv12_families() -> None:
    """Off-color companions on the a=(0,1,0) source-id-1 sheet add the 1/12 e6 term."""
    triples = [
        ((20, 0), (1, 1), (24, 0)),
        ((20, 0), (1, 1), (25, 0)),
        ((20, 0), (1, 2), (26, 0)),
        ((20, 1), (1, 0), (24, 1)),
        ((20, 1), (1, 2), (25, 1)),
        ((20, 2), (1, 0), (24, 2)),
        ((20, 2), (1, 1), (25, 2)),
        ((20, 2), (1, 1), (26, 2)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_leaves_translated_2v_overlap_false_positive_zero() -> (
    None
):
    """The legacy translated-2v overlap rule must stay inactive on a=(0,1,2)."""
    triples = [
        ((2, 0), (0, 1), (22, 0)),
        ((2, 1), (0, 0), (22, 1)),
    ]
    for triple in triples:
        toe, linfty = _build_linfty()
        x = basis_elem_g1(toe, triple[0])
        y = basis_elem_g2(toe, triple[1])
        z = basis_elem_g2(toe, triple[2])

        baseline = linfty.homotopy_jacobi(x, y, z)
        assert max_abs(baseline) < 1e-10, triple

        linfty.enable_ce2_global_predictor()
        repaired = linfty.homotopy_jacobi(x, y, z)
        assert max_abs(repaired) < 1e-10, triple


def test_global_ce2_predictor_cancels_a01_sameid_source_color_uv12_families() -> None:
    """Same-id source branch rotates color with one U and one sl3 term."""
    triples = [
        ((20, 0), (0, 0), (20, 1)),
        ((20, 0), (0, 0), (20, 2)),
        ((16, 0), (1, 0), (16, 1)),
        ((16, 0), (1, 0), (16, 2)),
        ((16, 1), (1, 1), (16, 0)),
        ((16, 2), (1, 2), (16, 1)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_a01_sameid_source_diag_uv18_families() -> None:
    """Same-id diagonal branch needs a weaker U plus diagonal e6+sl3 compensation."""
    triples = [
        ((20, 0), (0, 1), (20, 0)),
        ((20, 0), (0, 2), (20, 0)),
        ((16, 0), (1, 1), (16, 0)),
        ((16, 0), (1, 2), (16, 0)),
        ((16, 1), (1, 0), (16, 1)),
        ((16, 2), (1, 0), (16, 2)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_100_line_families() -> None:
    """Line families on the anchored a=(1,0,0) orbit."""
    triples = [
        ((17, 0), (1, 0), (24, 1)),
        ((17, 0), (1, 0), (24, 2)),
        ((17, 0), (1, 1), (24, 0)),
        ((17, 0), (1, 2), (24, 0)),
        ((17, 0), (2, 0), (25, 1)),
        ((17, 0), (2, 0), (25, 2)),
        ((17, 0), (2, 1), (25, 0)),
        ((17, 0), (2, 2), (25, 0)),
        ((17, 0), (3, 0), (22, 1)),
        ((17, 0), (3, 0), (22, 2)),
        ((17, 0), (3, 1), (22, 0)),
        ((17, 0), (3, 2), (22, 0)),
        ((17, 0), (4, 0), (20, 1)),
        ((17, 0), (4, 0), (20, 2)),
        ((17, 0), (4, 1), (20, 0)),
        ((17, 0), (4, 2), (20, 0)),
        ((17, 0), (5, 0), (23, 1)),
        ((17, 0), (5, 0), (23, 2)),
        ((17, 0), (5, 1), (23, 0)),
        ((17, 0), (5, 2), (23, 0)),
        ((17, 0), (6, 0), (21, 1)),
        ((17, 0), (6, 0), (21, 2)),
        ((17, 0), (6, 1), (21, 0)),
        ((17, 0), (6, 2), (21, 0)),
        ((17, 0), (7, 0), (18, 1)),
        ((17, 0), (7, 0), (18, 2)),
        ((17, 0), (7, 1), (18, 0)),
        ((17, 0), (7, 2), (18, 0)),
        ((17, 0), (8, 0), (19, 1)),
        ((17, 0), (8, 0), (19, 2)),
        ((17, 0), (8, 1), (19, 0)),
        ((17, 0), (8, 2), (19, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_100_overlap_families() -> None:
    """Half-strength overlap families on the anchored a=(1,0,0) orbit."""
    triples = [
        ((17, 0), (1, 1), (23, 0)),
        ((17, 0), (1, 2), (23, 0)),
        ((17, 0), (2, 1), (20, 0)),
        ((17, 0), (2, 2), (20, 0)),
        ((17, 0), (3, 1), (6, 0)),
        ((17, 0), (3, 2), (6, 0)),
        ((17, 0), (4, 1), (25, 0)),
        ((17, 0), (4, 2), (25, 0)),
        ((17, 0), (5, 1), (24, 0)),
        ((17, 0), (5, 2), (24, 0)),
        ((17, 0), (7, 1), (19, 0)),
        ((17, 0), (7, 2), (19, 0)),
        ((17, 0), (8, 1), (18, 0)),
        ((17, 0), (8, 2), (18, 0)),
        ((17, 0), (21, 1), (22, 0)),
        ((17, 0), (21, 2), (22, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_samefiber_partner_v_families() -> None:
    """Generic same-fiber partner branch repeats across multiple anchors."""
    triples = [
        ((6, 0), (3, 0), (6, 1)),
        ((6, 0), (3, 1), (6, 0)),
        ((9, 0), (4, 0), (9, 1)),
        ((9, 0), (4, 1), (9, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_anchor_201_samefiber_v_families() -> None:
    """Same-fiber sl3/e6 families on the anchored a=(2,0,1) orbit."""
    triples = [
        ((6, 0), (3, 0), (6, 1)),
        ((6, 0), (3, 0), (6, 2)),
        ((6, 0), (3, 1), (6, 0)),
        ((6, 0), (3, 2), (6, 0)),
    ]
    _assert_predictor_cancels_triples(triples)


def test_global_ce2_predictor_cancels_origin_same_fiber_uv_family() -> None:
    """Half-strength U/V overlap on a same-fiber origin line."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (0, 0))
    y = basis_elem_g2(toe, (1, 1))
    z = basis_elem_g2(toe, (15, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_origin_same_fiber_uv_family_diagonal() -> None:
    """A diagonal same-fiber case checks the sign tables beyond the axis lines."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (0, 0))
    y = basis_elem_g2(toe, (9, 1))
    z = basis_elem_g2(toe, (4, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_002_line_w_family_first_branch() -> None:
    """Promote the first exact a=(0,0,2) W-only frontier witness."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (22, 0))
    y = basis_elem_g2(toe, (1, 0))
    z = basis_elem_g2(toe, (16, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_002_line_v_family_first_branch() -> None:
    """Color-swapped companion of the first a=(0,0,2) line branch."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (22, 0))
    y = basis_elem_g2(toe, (1, 1))
    z = basis_elem_g2(toe, (16, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_002_overlap_uv_family_first_branch() -> (
    None
):
    """Half-strength overlap branch on the first promoted a=(0,0,2) witness."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (22, 0))
    y = basis_elem_g2(toe, (1, 1))
    z = basis_elem_g2(toe, (23, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_002_overlap_uv_family_color_flip() -> None:
    """Color-flipped overlap branch on the first promoted a=(0,0,2) witness."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (22, 0))
    y = basis_elem_g2(toe, (1, 2))
    z = basis_elem_g2(toe, (23, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_002_line_w_family_second_branch() -> None:
    """Second exact a=(0,0,2) W-only witness from the frontier sample."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (22, 0))
    y = basis_elem_g2(toe, (4, 0))
    z = basis_elem_g2(toe, (13, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_global_ce2_predictor_cancels_anchor_002_triple() -> None:
    """Regression test for the missing a=(0,0,2) anchor coverage."""
    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    # Use the E6 id for (0,0,2) anchor (g1 index 22).
    # This triple previously had a nonzero Jacobi residual until the anchor CE2 entry
    # was added to the sparse artifact.
    x = basis_elem_g1(toe, (22, 0))
    y = basis_elem_g1(toe, (0, 1))
    z = basis_elem_g2(toe, (0, 0))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    linfty.enable_ce2_global_predictor()
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10
