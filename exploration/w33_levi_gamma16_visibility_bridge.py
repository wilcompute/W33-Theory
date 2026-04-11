"""Exact Levi visibility law on the mixed 16-core.

This bridge is the missing weld between the corrected geometric chain and the
older Dirac-side exact packet

    16 = 10 + 6.

The point-line Levi operator does not see that 16 uniformly:

  - the 10-part sits inside the point-side 24 and is fully Levi-visible,
  - the 6-part sits inside the point-side 15 and is Levi-null.

So on the common 16-core, point-line incidence itself is the exact visibility
projector:

    H H^T |16 = 6 P_10 + 0 P_6 = 3 (I + Gamma).

Then the corrected spread result finishes the story: line-spread incidence kills
the line-side 24 exactly, so the full point-line-spread chain annihilates the
entire mixed 16.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_gamma16_chirality_bridge import (
    _basis_from_projector,
    _cluster_indices,
    _matrices,
    _qr_columns,
)
from exploration.w33_twin_v15_levi_null_bridge import _build_lines_and_spreads


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_levi_gamma16_visibility_bridge_summary.json"


def build_summary() -> dict[str, object]:
    a0, a1, a2 = _matrices()
    n = a0.shape[0]
    identity = np.eye(n, dtype=complex)
    all_ones = np.ones((n, n), dtype=complex)

    p1 = all_ones / n
    p24 = (a0 + 4.0 * identity) / 6.0 - all_ones / 15.0
    p15 = identity - p1 - p24

    u24 = _basis_from_projector(p24)
    u15 = _basis_from_projector(p15)

    b24 = u24.T.conj() @ a1 @ u24
    b15 = u15.T.conj() @ a1 @ u15
    _, eigvecs24 = np.linalg.eig(b24)
    _, eigvecs15 = np.linalg.eig(b15)
    clusters24 = _cluster_indices(b24)
    clusters15 = _cluster_indices(b15)

    matter_dominant_indices = [index for indices in clusters24.values() if len(indices) > 1 for index in indices]
    gauge_dominant_indices = [index for indices in clusters15.values() if len(indices) > 1 for index in indices]

    v24_dom = _qr_columns(u24 @ eigvecs24[:, matter_dominant_indices])
    v15_dom = _qr_columns(u15 @ eigvecs15[:, gauge_dominant_indices])

    d_h = a0 + 1j * (a1 - a2) / np.sqrt(3.0)
    eigvals_dh, eigvecs_dh = np.linalg.eigh(d_h)
    v16 = _qr_columns(eigvecs_dh[:, np.isclose(eigvals_dh, -1.0, atol=1e-8)])

    u10, _, _ = np.linalg.svd(v16.T.conj() @ v24_dom, full_matrices=False)
    v10 = _qr_columns(v16 @ u10[:, :10])
    u6, _, _ = np.linalg.svd(v16.T.conj() @ v15_dom, full_matrices=False)
    v6 = _qr_columns(v16 @ u6[:, :6])
    gamma = v10 @ v10.T.conj() - v6 @ v6.T.conj()

    _lines, H_int, B_int = _build_lines_and_spreads(np.asarray(a0.real, dtype=int))
    H = H_int.astype(complex)
    B = B_int.astype(complex)
    a_line = H.T.conj() @ H - 4.0 * np.eye(40, dtype=complex)
    p24_line = (a_line + 4.0 * np.eye(40, dtype=complex)) / 6.0 - np.ones((40, 40), dtype=complex) / 15.0
    p15_line = np.eye(40, dtype=complex) - np.ones((40, 40), dtype=complex) / 40.0 - p24_line

    n_point = H @ H.T.conj()
    n16 = v16.T.conj() @ n_point @ v16
    gamma16 = v16.T.conj() @ gamma @ v16
    p10_16 = v16.T.conj() @ (v10 @ v10.T.conj()) @ v16
    p6_16 = v16.T.conj() @ (v6 @ v6.T.conj()) @ v16

    line_image_16 = H.T.conj() @ v16
    line_image_10 = H.T.conj() @ v10
    line_image_6 = H.T.conj() @ v6
    singular_16 = np.linalg.svd(line_image_16, compute_uv=False)

    cascade_16 = B.T.conj() @ H.T.conj() @ v16

    return {
        "carrier_dictionary": {
            "mixed_core": "16 = 10_visible + 6_null",
            "point_line_visibility": "H H^T |16 = 6 P10",
            "full_cascade": "B^T H^T |16 = 0",
        },
        "exact_operator_laws": {
            "point_line_visibility": "H H^T |16 = 6 P10 = 3 (I + Gamma)",
            "line_side_support": "H^T(16) ⊂ line-24",
            "spread_side_extinction": "B^T H^T(16) = 0",
        },
        "spectral_packet": {
            "HHt_on_16_eigenvalues": [float(np.real_if_close(value)) for value in np.linalg.eigvalsh(n16)],
            "H_from_16_singular_values": [float(value) for value in singular_16],
        },
        "levi_gamma16_visibility_theorem": {
            "the_mixed_core_splits_exactly_as_10_plus_6": bool(v10.shape[1] == 10 and v6.shape[1] == 6),
            "point_line_incidence_sees_exactly_the_10_and_kills_exactly_the_6": bool(
                np.linalg.matrix_rank(line_image_10) == 10
                and np.linalg.norm(line_image_6) < 1e-12
                and np.linalg.matrix_rank(line_image_16) == 10
            ),
            "the_line_image_of_the_16_lands_entirely_in_the_line_side_24": bool(
                np.linalg.norm(p15_line @ line_image_16) < 1e-12
                and np.linalg.norm((p24_line - np.eye(40)) @ line_image_16) < 1e-12
            ),
            "the_levi_visibility_operator_on_the_16_is_exactly_6_times_the_10_projector": bool(
                np.linalg.norm(n16 - 6.0 * p10_16) < 1e-12
            ),
            "equivalently_the_levi_visibility_operator_is_exactly_3_times_I_plus_Gamma_on_the_16": bool(
                np.linalg.norm(n16 - 3.0 * (np.eye(16) + gamma16)) < 1e-12
            ),
            "the_full_point_line_spread_cascade_annihilates_the_entire_mixed_16": bool(
                np.linalg.norm(cascade_16) < 1e-12
            ),
            "the_visibility_spectrum_on_the_16_is_exactly_6_ten_times_and_0_six_times": bool(
                np.array_equal(
                    np.rint(np.linalg.eigvalsh(n16)).astype(int),
                    np.array([0] * 6 + [6] * 10),
                )
            ),
        },
        "interpretation": (
            "The old mixed 16 core and the new Levi/spread geometry are now one exact operator law. "
            "The point-line Levi operator sees only the 10-part of the mixed core and kills the 6-part, "
            "so Gamma on the 16 is literally the normalized Levi visibility operator. Then the line-spread "
            "bridge kills the surviving line-side 24 image, so the full point-line-spread cascade extinguishes "
            "the entire mixed 16. This is the exact weld between the Dirac-side 16=10+6 packet and the corrected "
            "geometric carrier chain."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("=" * 72)
    print("W33 LEVI GAMMA16 VISIBILITY BRIDGE")
    print("=" * 72)
    for key, value in summary["levi_gamma16_visibility_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
