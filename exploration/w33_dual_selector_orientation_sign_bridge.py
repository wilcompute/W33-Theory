"""Dual selector / orientation / sign bridge for the Z3-graded E8 Jacobi frontier.

This module sharpens the exact boundary left by
`w33_selector_decimal_toroidal_jacobi_bridge.py`.

What is already exact:
  - the local 3-branch qutrit selector is S3 of order 6;
  - the normalized local selector average is exactly +1/6;
  - the sign projector on the 3-point permutation representation is exactly zero;
  - the certified Z3-graded E8 Jacobi artifact closes at the exact rational scales
      scale_sl3 = +1/6,
      scale_g2g2 = -1/6.

The live question is therefore sharper than before:
  - can the negative coefficient -1/6 be explained by a *simple* dual/orientation
    sign flip on the g2 sector?

This script tests the most naive version of that idea directly.  It compares the
canonical bracket against a variant in which only the overall g0-action sign on g2
is flipped, while every other structural piece is kept fixed.

Result:
  - both brackets still tune the dual scale to -1/6 when scale_sl3 is fixed at +1/6;
  - but the sign-flipped variant destroys mixed Jacobi badly on (g0,g1,g2) and
    (g1,g2,g2), even though (g1,g1,g2) stays small.

So the negative coefficient is not a literal local sign projector and not a simple
contragredient/orientation sign flip.  Whatever explains -1/6 is deeper than that.
"""

from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any, Sequence

import numpy as np


if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

from tools.toe_e8_z3graded_bracket_jacobi import (  # noqa: E402
    E6Projector,
    E8Z3,
    E8Z3Bracket,
    _comm,
    _elt_norm,
    _jacobi,
    _load_signed_cubic_triads,
    _random_element,
)


DATA_DIR = ROOT / "data"
ARTIFACT_PATH = ROOT / "artifacts" / "toe_e8_z3graded_jacobi.json"
BASIS_PATH = ROOT / "artifacts" / "e6_27rep_basis_export" / "E6_basis_78.npy"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_dual_selector_orientation_sign_bridge_summary.json"
FLOAT_TOL = 1e-12
CLOSE_TOL = 1e-10
FAIL_THRESHOLD = 10.0
TUNE_SEED = 0
PATTERN_SEED = 11
TUNE_SAMPLES = 32
PATTERN_TRIALS = 8
SCALE0 = 2
SCALE1 = 2
SCALE2 = 2
EXPECTED_PLUS_ONE_SIXTH = Fraction(1, 6)
EXPECTED_MINUS_ONE_SIXTH = Fraction(-1, 6)
FIXED_SCALE_SL3 = float(EXPECTED_PLUS_ONE_SIXTH)
FIXED_SCALE_G2G2 = float(EXPECTED_MINUS_ONE_SIXTH)


def _permutation_matrix(action: Sequence[int]) -> np.ndarray:
    size = len(action)
    matrix = np.zeros((size, size), dtype=float)
    for column, image in enumerate(action):
        matrix[image, column] = 1.0
    return matrix


def _compose(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple(left[index] for index in right)


def _closure(generators: Sequence[Sequence[int]]) -> list[tuple[int, ...]]:
    generators = [tuple(generator) for generator in generators]
    identity = tuple(range(len(generators[0])))
    seen = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            candidate = _compose(generator, current)
            if candidate not in seen:
                seen.add(candidate)
                frontier.append(candidate)
    return sorted(seen)


def _permutation_parity(action: Sequence[int]) -> int:
    inversions = 0
    for index, value_i in enumerate(action):
        for value_j in action[index + 1 :]:
            if value_i > value_j:
                inversions += 1
    return -1 if inversions % 2 else 1


def _matrix_rank(matrix: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(matrix, tol=1e-10))


def _matrix_fraction_strings(matrix: np.ndarray, *, max_denominator: int = 6) -> list[list[str]]:
    out: list[list[str]] = []
    for row in matrix:
        out_row: list[str] = []
        for value in row:
            frac = Fraction(str(float(value))).limit_denominator(max_denominator)
            if frac.numerator == 0:
                out_row.append("0")
            elif frac.denominator == 1:
                out_row.append(str(frac.numerator))
            else:
                out_row.append(f"{frac.numerator}/{frac.denominator}")
        out.append(out_row)
    return out


@lru_cache(maxsize=1)
def _load_basis_and_projector() -> tuple[np.ndarray, tuple[tuple[int, int, int, int], ...], E6Projector]:
    e6_basis = np.load(BASIS_PATH).astype(np.complex128)
    triads = tuple(_load_signed_cubic_triads())
    projector = E6Projector(e6_basis)
    return e6_basis, triads, projector


def _load_jacobi_artifact(path: Path = ARTIFACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class SignFlippedDualActionBracket(E8Z3Bracket):
    """Variant with only the overall g0-action sign on g2 flipped."""

    def bracket(self, a: E8Z3, b: E8Z3) -> E8Z3:
        e6 = _comm(a.e6, b.e6)
        sl3 = _comm(a.sl3, b.sl3)

        g1 = a.e6 @ b.g1 - b.e6 @ a.g1 + b.g1 @ a.sl3.T - a.g1 @ b.sl3.T

        # This is the sole modification relative to the canonical bracket:
        # the overall sign of the g0 action on g2 is flipped.
        g2 = a.e6.T @ b.g2 - b.e6.T @ a.g2 + b.g2 @ a.sl3 - a.g2 @ b.sl3

        g2 = g2 + self.bracket_g1_g1(a.g1, b.g1)
        g1 = g1 + self.bracket_g2_g2(a.g2, b.g2)

        if np.any(a.g1) or np.any(b.g2):
            a0 = a.g1 @ b.g2.T
            b0 = a.g1.T @ b.g2
            e6 = e6 + self.scale_e6 * self._proj_e6.project(a0)
            sl3 = sl3 + self.scale_sl3 * (b0 - (np.trace(b0) / 3.0) * np.eye(3, dtype=np.complex128))
        if np.any(b.g1) or np.any(a.g2):
            a0 = b.g1 @ a.g2.T
            b0 = b.g1.T @ a.g2
            e6 = e6 - self.scale_e6 * self._proj_e6.project(a0)
            sl3 = sl3 - self.scale_sl3 * (b0 - (np.trace(b0) / 3.0) * np.eye(3, dtype=np.complex128))

        return E8Z3(e6=e6, sl3=sl3, g1=g1, g2=g2)


def _build_bracket(
    bracket_cls: type[E8Z3Bracket],
    *,
    scale_sl3: float,
    scale_g2g2: float,
) -> E8Z3Bracket:
    _, triads, projector = _load_basis_and_projector()
    return bracket_cls(
        e6_projector=projector,
        cubic_triads=triads,
        scale_g1g1=1.0,
        scale_g2g2=scale_g2g2,
        scale_e6=1.0,
        scale_sl3=scale_sl3,
    )


def _tune_g2g2_scale(
    bracket_cls: type[E8Z3Bracket],
    *,
    samples: int = TUNE_SAMPLES,
    seed: int = TUNE_SEED,
) -> float:
    e6_basis, _, projector = _load_basis_and_projector()
    rng = np.random.default_rng(seed)

    br0 = bracket_cls(
        e6_projector=projector,
        cubic_triads=_load_basis_and_projector()[1],
        scale_g1g1=1.0,
        scale_g2g2=0.0,
        scale_e6=1.0,
        scale_sl3=FIXED_SCALE_SL3,
    )
    br1 = bracket_cls(
        e6_projector=projector,
        cubic_triads=_load_basis_and_projector()[1],
        scale_g1g1=1.0,
        scale_g2g2=1.0,
        scale_e6=1.0,
        scale_sl3=FIXED_SCALE_SL3,
    )

    numerator = 0.0
    denominator = 0.0
    for _ in range(samples):
        x = _random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=SCALE1,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        y = _random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=SCALE1,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        u = _random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=0,
            scale2=SCALE2,
            include_g0=False,
            include_g1=False,
        )
        j0 = _jacobi(br0, x, y, u).g1.reshape(-1)
        j1 = _jacobi(br1, x, y, u).g1.reshape(-1)
        delta = j1 - j0
        numerator += float(np.vdot(delta, j0).real)
        denominator += float(np.vdot(delta, delta).real)

    if denominator == 0.0:
        return 0.0
    return float(-numerator / denominator)


def _random_grade_element(rng: np.random.Generator, grade: int) -> E8Z3:
    e6_basis, _, _ = _load_basis_and_projector()
    if grade == 0:
        return _random_element(
            rng,
            e6_basis,
            scale0=SCALE0,
            scale1=0,
            scale2=0,
            include_g1=False,
            include_g2=False,
        )
    if grade == 1:
        return _random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=SCALE1,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
    if grade == 2:
        return _random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=0,
            scale2=SCALE2,
            include_g0=False,
            include_g1=False,
        )
    raise ValueError(f"Unsupported grading {grade}")


def _pattern_max_residual(
    bracket_cls: type[E8Z3Bracket],
    pattern: Sequence[int],
    *,
    trials: int = PATTERN_TRIALS,
    seed: int,
) -> float:
    bracket = _build_bracket(
        bracket_cls,
        scale_sl3=FIXED_SCALE_SL3,
        scale_g2g2=FIXED_SCALE_G2G2,
    )
    rng = np.random.default_rng(seed)
    max_residual = 0.0
    for _ in range(trials):
        x, y, z = (_random_grade_element(rng, grade) for grade in pattern)
        max_residual = max(max_residual, _elt_norm(_jacobi(bracket, x, y, z)))
    return float(max_residual)


@lru_cache(maxsize=1)
def build_dual_selector_orientation_sign_summary() -> dict[str, Any]:
    jacobi_artifact = _load_jacobi_artifact()

    translation = (1, 2, 0)
    reflection = (0, 2, 1)
    local_group = _closure([translation, reflection])
    permutation_matrices = [_permutation_matrix(element) for element in local_group]
    parities = [_permutation_parity(element) for element in local_group]
    trivial_projector = sum(permutation_matrices) / len(local_group)
    sign_projector = sum(
        parity * matrix for parity, matrix in zip(parities, permutation_matrices, strict=True)
    ) / len(local_group)

    canonical_tuned_scale = _tune_g2g2_scale(E8Z3Bracket)
    flipped_tuned_scale = _tune_g2g2_scale(SignFlippedDualActionBracket)

    patterns = {
        "g0_g1_g2": (0, 1, 2),
        "g1_g1_g2": (1, 1, 2),
        "g1_g2_g2": (1, 2, 2),
    }
    canonical_pattern_packet: dict[str, dict[str, Any]] = {}
    flipped_pattern_packet: dict[str, dict[str, Any]] = {}
    for index, (name, pattern) in enumerate(patterns.items()):
        canonical_residual = _pattern_max_residual(E8Z3Bracket, pattern, seed=PATTERN_SEED + index)
        flipped_residual = _pattern_max_residual(
            SignFlippedDualActionBracket,
            pattern,
            seed=PATTERN_SEED + index,
        )
        canonical_pattern_packet[name] = {
            "grading_pattern": list(pattern),
            "max_residual": canonical_residual,
        }
        flipped_pattern_packet[name] = {
            "grading_pattern": list(pattern),
            "max_residual": flipped_residual,
        }

    canonical_pattern_max = max(packet["max_residual"] for packet in canonical_pattern_packet.values())
    flipped_pattern_max = max(packet["max_residual"] for packet in flipped_pattern_packet.values())

    return {
        "status": "ok",
        "local_selector_packet": {
            "selector_order": len(local_group),
            "average_weight": "1/6",
            "trivial_projector": {
                "matrix": trivial_projector.tolist(),
                "rational_matrix": _matrix_fraction_strings(trivial_projector),
                "rank": _matrix_rank(trivial_projector),
            },
            "sign_projector": {
                "matrix": sign_projector.tolist(),
                "rational_matrix": _matrix_fraction_strings(sign_projector),
                "rank": _matrix_rank(sign_projector),
            },
            "theorem": {
                "plus_one_sixth_is_exact_local_selector_average": np.allclose(
                    trivial_projector,
                    np.ones((3, 3), dtype=float) / 3.0,
                    atol=FLOAT_TOL,
                ),
                "sign_projector_vanishes_on_the_local_permutation_rep": np.allclose(
                    sign_projector,
                    0.0,
                    atol=FLOAT_TOL,
                ),
            },
        },
        "dual_scale_packet": {
            "fixed_scale_sl3": FIXED_SCALE_SL3,
            "expected_scale_g2g2": FIXED_SCALE_G2G2,
            "canonical_tuned_scale_g2g2": canonical_tuned_scale,
            "sign_flipped_tuned_scale_g2g2": flipped_tuned_scale,
            "artifact_scale_g2g2": float(jacobi_artifact["scales"]["scale_g2g2"]),
            "absolute_errors": {
                "canonical_to_expected": abs(canonical_tuned_scale - FIXED_SCALE_G2G2),
                "sign_flipped_to_expected": abs(flipped_tuned_scale - FIXED_SCALE_G2G2),
            },
            "theorem": {
                "canonical_tunes_to_exact_minus_one_sixth": abs(canonical_tuned_scale - FIXED_SCALE_G2G2) < FLOAT_TOL,
                "sign_flipped_variant_also_tunes_to_exact_minus_one_sixth": abs(flipped_tuned_scale - FIXED_SCALE_G2G2) < FLOAT_TOL,
                "artifact_and_tuned_scale_agree": abs(float(jacobi_artifact["scales"]["scale_g2g2"]) - FIXED_SCALE_G2G2) < FLOAT_TOL,
            },
        },
        "mixed_jacobi_pattern_packet": {
            "fixed_exact_rational_scales": {
                "scale_sl3": FIXED_SCALE_SL3,
                "scale_g2g2": FIXED_SCALE_G2G2,
            },
            "canonical": {
                "patterns": canonical_pattern_packet,
                "max_residual": canonical_pattern_max,
            },
            "sign_flipped": {
                "patterns": flipped_pattern_packet,
                "max_residual": flipped_pattern_max,
            },
            "theorem": {
                "canonical_closes_all_mixed_patterns_at_exact_rational_scales": canonical_pattern_max < CLOSE_TOL,
                "sign_flipped_breaks_g0_g1_g2_badly": flipped_pattern_packet["g0_g1_g2"]["max_residual"] > FAIL_THRESHOLD,
                "sign_flipped_breaks_g1_g2_g2_badly": flipped_pattern_packet["g1_g2_g2"]["max_residual"] > FAIL_THRESHOLD,
                "sign_flipped_leaves_g1_g1_g2_small": flipped_pattern_packet["g1_g1_g2"]["max_residual"] < CLOSE_TOL,
            },
        },
        "frontier_packet": {
            "exact_read": (
                "The positive coefficient +1/6 is explained exactly by the normalized local S3 selector average, "
                "and the local sign projector still vanishes exactly on the 3-point permutation representation."
            ),
            "unresolved_read": (
                "The negative coefficient -1/6 is therefore not a literal local sign projection, and this bridge now shows "
                "it is not recovered by a naive overall sign flip of the g0 action on g2 either. The remaining problem is deeper dual/oriented structure."
            ),
        },
        "bridge_theorem": {
            "plus_one_sixth_is_exact_local_selector_average": np.allclose(
                trivial_projector,
                np.ones((3, 3), dtype=float) / 3.0,
                atol=FLOAT_TOL,
            ),
            "local_sign_projector_vanishes_exactly": np.allclose(sign_projector, 0.0, atol=FLOAT_TOL),
            "canonical_and_sign_flipped_variants_both_tune_to_minus_one_sixth": (
                abs(canonical_tuned_scale - FIXED_SCALE_G2G2) < FLOAT_TOL
                and abs(flipped_tuned_scale - FIXED_SCALE_G2G2) < FLOAT_TOL
            ),
            "canonical_bracket_closes_mixed_jacobi_at_exact_rational_scales": canonical_pattern_max < CLOSE_TOL,
            "naive_sign_flipped_dual_action_breaks_mixed_jacobi": (
                flipped_pattern_packet["g0_g1_g2"]["max_residual"] > FAIL_THRESHOLD
                and flipped_pattern_packet["g1_g2_g2"]["max_residual"] > FAIL_THRESHOLD
            ),
            "minus_one_sixth_is_not_a_simple_local_sign_or_dual_flip": (
                np.allclose(sign_projector, 0.0, atol=FLOAT_TOL)
                and abs(flipped_tuned_scale - FIXED_SCALE_G2G2) < FLOAT_TOL
                and flipped_pattern_packet["g0_g1_g2"]["max_residual"] > FAIL_THRESHOLD
                and flipped_pattern_packet["g1_g2_g2"]["max_residual"] > FAIL_THRESHOLD
            ),
        },
        "bridge_verdict": (
            "The next wall is now cleaner. The negative Jacobi coefficient -1/6 is not a literal local sign projector, because the exact local sign projector vanishes. "
            "And it is not explained by the most naive global dual/orientation fix either, because flipping only the overall g0 action on g2 leaves the tuned scale at -1/6 but breaks mixed Jacobi badly on (g0,g1,g2) and (g1,g2,g2). "
            "So the minus sign is real, exact, and deeper than a simple local sign or simple contragredient sign flip."
        ),
        "source_files": [
            "exploration/w33_selector_decimal_toroidal_jacobi_bridge.py",
            "tools/toe_e8_z3graded_bracket_jacobi.py",
            "artifacts/toe_e8_z3graded_jacobi.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_dual_selector_orientation_sign_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
