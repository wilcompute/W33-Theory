"""Exact common generation flag inside the reduced Yukawa algebra.

This module packages the strongest exact flag-like structure already present in
the repo-native Yukawa reduction.

What is established:
  - the two universal generation matrices on the active sectors are unipotent
    3x3 operators C_(+-) and C_(-+);
  - their nilpotent parts N = C - I both have rank 2, share the same rank-1
    square N^2, and satisfy N^3 = 0;
  - that common square defines an exact common flag in C^3:
        L = im(N^2) = ker(N_(+-)) = ker(N_(-+)),
        P = ker(N^2),
    with dim L = 1 and dim P = 2;
  - in the native integer chart one may take
        L = span{(1,1,0)},
        P = {(x,y,z) : x = y} = span{(1,1,0), (0,0,1)}.

So the reduced Yukawa generation algebra already carries a common line-plane
flag before any continuum interpretation is added. This is the strongest
repo-native finite hint toward a flag/Grassmannian family variable.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
if __package__ in {None, ""}:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from exploration._artifact_paths import load_json_from_repo_data
else:
    from ._artifact_paths import load_json_from_repo_data

DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_yukawa_generation_flag_bridge_summary.json"

LINE_VECTOR = np.array([1.0, 1.0, 0.0], dtype=float)
PLANE_BASIS = np.array([[1.0, 1.0, 0.0], [0.0, 0.0, 1.0]], dtype=float)
HEAVY_VECTOR = np.array([1.0, -1.0, 0.0], dtype=float)


def _read_json(filename: str) -> dict[str, Any]:
    return load_json_from_repo_data(ROOT, Path("data") / filename)


def _normalized_projector_from_columns(columns: np.ndarray) -> np.ndarray:
    gram = columns.T @ columns
    return columns @ np.linalg.inv(gram) @ columns.T


def _normalized_line_projector(vector: np.ndarray) -> np.ndarray:
    norm = float(vector @ vector)
    return np.outer(vector, vector) / norm


def _integer_rank(matrix: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(matrix.astype(float)))


def _lies_in_plane(vector: np.ndarray) -> bool:
    return int(vector[0]) == int(vector[1])


@lru_cache(maxsize=1)
def build_yukawa_generation_flag_summary() -> dict[str, Any]:
    summary = _read_json("w33_yukawa_unipotent_reduction_bridge_summary.json")
    algebra = summary["universal_generation_algebra"]

    c_plus = np.array(algebra["plus_minus_generation_matrix"], dtype=int)
    c_minus = np.array(algebra["minus_plus_generation_matrix"], dtype=int)
    identity = np.eye(3, dtype=int)
    n_plus = c_plus - identity
    n_minus = c_minus - identity
    n_square = n_plus @ n_plus

    plane_projector = _normalized_projector_from_columns(PLANE_BASIS.T)
    line_projector = _normalized_line_projector(LINE_VECTOR)
    heavy_projector = _normalized_line_projector(HEAVY_VECTOR)

    line_vector_int = LINE_VECTOR.astype(int)
    plane_basis_int = PLANE_BASIS.astype(int)
    heavy_vector_int = HEAVY_VECTOR.astype(int)

    return {
        "status": "ok",
        "generation_matrices": {
            "plus_minus": c_plus.astype(int).tolist(),
            "minus_plus": c_minus.astype(int).tolist(),
            "plus_minus_nilpotent": n_plus.astype(int).tolist(),
            "minus_plus_nilpotent": n_minus.astype(int).tolist(),
            "common_nilpotent_square": n_square.astype(int).tolist(),
        },
        "common_flag": {
            "line_generator": line_vector_int.tolist(),
            "plane_basis": plane_basis_int.tolist(),
            "plane_equation": "x = y",
            "orthogonal_heavy_generator": heavy_vector_int.tolist(),
            "line_projector": line_projector.tolist(),
            "plane_projector": plane_projector.tolist(),
            "heavy_projector": heavy_projector.tolist(),
        },
        "generation_flag_theorem": {
            "both_nilpotent_parts_have_rank_2": _integer_rank(n_plus) == 2
            and _integer_rank(n_minus) == 2,
            "common_nilpotent_square_has_rank_1": _integer_rank(n_square) == 1,
            "common_nilpotent_square_is_shared_exactly": np.array_equal(n_square, n_minus @ n_minus),
            "nilpotent_cubes_vanish": np.array_equal(n_plus @ n_square, np.zeros((3, 3), dtype=int))
            and np.array_equal(n_minus @ n_square, np.zeros((3, 3), dtype=int)),
            "common_line_equals_kernel_of_both_nilpotents": np.array_equal(
                n_plus @ line_vector_int, np.zeros(3, dtype=int)
            )
            and np.array_equal(n_minus @ line_vector_int, np.zeros(3, dtype=int)),
            "common_line_equals_image_of_common_square": np.array_equal(
                n_square[:, 0], line_vector_int
            )
            and np.array_equal(n_square[:, 1], -line_vector_int),
            "common_plane_equals_kernel_of_common_square": np.array_equal(
                n_square @ plane_basis_int[0], np.zeros(3, dtype=int)
            )
            and np.array_equal(n_square @ plane_basis_int[1], np.zeros(3, dtype=int)),
            "both_generation_matrices_preserve_common_line": np.array_equal(
                c_plus @ line_vector_int, line_vector_int
            )
            and np.array_equal(c_minus @ line_vector_int, line_vector_int),
            "both_generation_matrices_preserve_common_plane": _lies_in_plane(
                c_plus @ plane_basis_int[0]
            )
            and _lies_in_plane(c_plus @ plane_basis_int[1])
            and _lies_in_plane(c_minus @ plane_basis_int[0])
            and _lies_in_plane(c_minus @ plane_basis_int[1]),
            "orthogonal_heavy_line_is_complement_of_common_plane": np.allclose(
                np.eye(3) - plane_projector, heavy_projector
            ),
        },
        "bridge_verdict": (
            "The universal reduced Yukawa generation algebra already carries a "
            "common exact flag. The two unipotent generation matrices share the "
            "same rank-1 nilpotent square, the same fixed line span(1,1,0), and "
            "the same invariant plane x=y. So before any continuum guess is "
            "added, the finite internal generation side already organizes itself "
            "as a 1<2<3 flag rather than as unrelated free directions."
        ),
        "source_files": [
            "data/w33_yukawa_unipotent_reduction_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_yukawa_generation_flag_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
