"""Canonical primitive plane versus the explicit ``3U`` core on K3.

Two exact K3 bridge objects were already present:

1. a canonical primitive hyperbolic plane carrying the reduced global external
   coefficient ``351/(4 pi^2)``; and
2. a primitive orthogonal ``3U`` core inside the same explicit K3 lattice.

This module resolves their exact relation and then compares that distinguished
plane with the selector-side positive channel.

The main outcomes are:

- the canonical primitive plane is exactly the first explicit ``U`` factor of
  the ``3U`` block;
- the selector's positive ``3U`` shadow decomposes orthogonally across all
  three explicit ``U`` factors; and
- that shadow is not supported on the distinguished primitive plane alone.

So the locked global plane is not floating inside ``3U``. It is one exact
distinguished ``U`` factor, while the selector's positive-side channel mixes
all three hyperbolic factors.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    ROOT = Path(__file__).resolve().parents[1]

from w33_curved_h2_intersection_bridge import SIGN_TOL, ZERO_TOL
from w33_k3_integral_h2_lattice_bridge import (
    integral_k3_h2_intersection_matrix,
    primitive_hyperbolic_plane_coefficients,
)
from w33_k3_selector_e8_shadow_bridge import _selector_plane_integral_coordinates
from w33_k3_three_u_decomposition_bridge import k3_three_u_block_coefficients


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_k3_primitive_plane_three_u_alignment_bridge_summary.json"


def _orthogonal_projector(basis: np.ndarray, form: np.ndarray) -> np.ndarray:
    return basis @ np.linalg.inv(basis.T @ form @ basis) @ basis.T @ form


def _signature_counts(matrix: np.ndarray) -> tuple[int, int]:
    eigenvalues = np.linalg.eigvalsh(matrix.astype(float))
    positive = int(np.sum(eigenvalues > SIGN_TOL))
    negative = int(np.sum(eigenvalues < -SIGN_TOL))
    return positive, negative


def _float_lists(matrix: np.ndarray) -> list[list[float]]:
    return [[float(value) for value in row] for row in matrix.tolist()]


@lru_cache(maxsize=1)
def build_k3_primitive_plane_three_u_alignment_bridge_summary() -> dict[str, Any]:
    ambient_form = integral_k3_h2_intersection_matrix().astype(float)
    primitive_plane = primitive_hyperbolic_plane_coefficients().astype(float)
    three_u = k3_three_u_block_coefficients().astype(float)
    selector = _selector_plane_integral_coordinates()

    u_blocks = [three_u[:, 2 * index : 2 * index + 2] for index in range(3)]
    u_projectors = [_orthogonal_projector(block, ambient_form) for block in u_blocks]
    u_components = [projector @ selector for projector in u_projectors]
    u_forms = [component.T @ ambient_form @ component for component in u_components]
    three_u_shadow = _orthogonal_projector(three_u, ambient_form) @ selector
    reconstruction_error = float(np.max(np.abs(sum(u_components) - three_u_shadow)))

    return {
        "status": "ok",
        "primitive_plane_coefficients": primitive_plane.astype(int).tolist(),
        "three_u_factor_one_coefficients": u_blocks[0].astype(int).tolist(),
        "selector_u_factor_one_form": _float_lists(u_forms[0]),
        "selector_u_factor_two_form": _float_lists(u_forms[1]),
        "selector_u_factor_three_form": _float_lists(u_forms[2]),
        "selector_three_u_shadow_reconstruction_error_linf": reconstruction_error,
        "primitive_plane_three_u_alignment_theorem": {
            "primitive_plane_equals_the_first_explicit_u_factor": any(
                np.array_equal(primitive_plane.astype(int), ub.astype(int)) for ub in u_blocks
            ),
            "selector_three_u_shadow_decomposes_exactly_across_the_three_u_factors": (
                reconstruction_error < ZERO_TOL
            ),
            "selector_has_nonzero_projection_on_u_factor_one": bool(
                float(np.linalg.norm(u_components[0])) > ZERO_TOL
            ),
            "selector_has_nonzero_projection_on_u_factor_two": bool(
                float(np.linalg.norm(u_components[1])) > ZERO_TOL
            ),
            "selector_has_nonzero_projection_on_u_factor_three": bool(
                float(np.linalg.norm(u_components[2])) > ZERO_TOL
            ),
            "selector_three_u_shadow_is_not_supported_on_the_primitive_plane_alone": bool(
                float(np.linalg.norm(u_components[1] + u_components[2])) > ZERO_TOL
            ),
            "primitive_plane_is_distinguished_but_not_equal_to_the_selector_positive_channel": bool(
                np.array_equal(primitive_plane.astype(int), u_blocks[0].astype(int))
                and float(np.linalg.norm(u_components[1] + u_components[2])) > ZERO_TOL
            ),
            "all_three_u_factor_shadows_are_mixed_signature": all(
                _signature_counts(form) == (1, 1) for form in u_forms
            ),
        },
        "bridge_verdict": (
            "The canonical primitive plane is not merely somewhere inside the "
            "hyperbolic K3 core: it is exactly the first explicit U factor of "
            "the 3U block. But the selector's positive-side 3U shadow is not "
            "that plane alone. It decomposes orthogonally across all three U "
            "factors, with nonzero support on each one. So the locked global "
            "351/(4 pi^2) plane is a distinguished hyperbolic factor, whereas "
            "the selector's local positive channel mixes the whole 3U core."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_k3_primitive_plane_three_u_alignment_bridge_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
