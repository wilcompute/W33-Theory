#!/usr/bin/env python3
"""Coherent continuation-selector semantics and a Steinberg-81 falsifier.

Question: can the protected 81-dimensional W33 sector be used to coherently
control HoloVM continuations while Merkle roots remain classical authenticated
boundary data?

This file separates two statements that are easy to conflate.

(1) YES: an abstract 81-dimensional control register can coherently select among
    up to 81 externally stored continuation roots.  The amplitudes are quantum
    data; the roots and their immutable Merkle closures stay classical.  A
    measurement selects one slot/root and never requires encoding a SHA-256
    digest as an optical amplitude.

(2) NOT YET PROVED: the obvious 81-slot realization indexed by F_3^4 is the
    repository's primitive Steinberg-81 representation.  In fact this naive
    phase-space permutation model has a basis vector |0> fixed by every
    symplectic transvection, hence a nonzero invariant trivial subspace.  It is
    reducible and therefore cannot simply be identified with the primitive
    Steinberg projector certified elsewhere in the repo.

So the correct next representation-theory task is an explicit intertwiner from
an operational continuation-control basis into the existing rank-81 primitive
projector image, not a dimension match.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import isclose, sqrt
import cmath
import json
from pathlib import Path
from typing import Any, Iterable

from w33_finite_control_unbounded_guest_hypervisor import transvection
from w33_merkle_capability_memory import digest
from w33_typed_universal_microvm import GEOMETRY

ROOT = Path(__file__).resolve().parents[1]
Q = 3
SLOTS = tuple(product(range(Q), repeat=4))
INDEX = {v: i for i, v in enumerate(SLOTS)}
ZERO_SLOT = INDEX[(0, 0, 0, 0)]
DIMENSION = len(SLOTS)


def _act(matrix: tuple[tuple[int, ...], ...], v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(matrix[i][j] * v[j] for j in range(4)) % Q for i in range(4))


def slot_permutation(axis: int, lam: int) -> tuple[int, ...]:
    if not 0 <= axis < 40 or lam not in (1, 2):
        raise ValueError("invalid W33 transvection opcode")
    matrix = transvection(tuple(int(x) for x in GEOMETRY.points[axis]), lam)
    perm = tuple(INDEX[_act(matrix, v)] for v in SLOTS)
    if set(perm) != set(range(DIMENSION)):
        raise AssertionError("symplectic transvection failed to permute F3^4")
    return perm


def _norm2(amplitudes: Iterable[complex]) -> float:
    return float(sum((z.real * z.real + z.imag * z.imag) for z in amplitudes))


def _complex_hex(z: complex) -> tuple[str, str]:
    """Canonical bit-exact software encoding of a Python complex amplitude."""
    return (float(z.real).hex(), float(z.imag).hex())


@dataclass(frozen=True)
class ContinuationSelector:
    """81-dimensional coherent control with an external classical root table."""

    roots: tuple[str, ...]
    amplitudes: tuple[complex, ...]

    def __post_init__(self) -> None:
        if len(self.roots) != DIMENSION or len(self.amplitudes) != DIMENSION:
            raise ValueError("selector requires exactly 81 classical slots and amplitudes")
        if len(set(self.roots)) != DIMENSION:
            raise ValueError("continuation roots must be distinct slot identities")
        if any(not isinstance(r, str) or not r.startswith("sha256:") or len(r) != 71 for r in self.roots):
            raise ValueError("every slot must name a canonical continuation digest")
        if not isclose(_norm2(self.amplitudes), 1.0, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError("selector amplitudes must be normalized")

    @property
    def selector_id(self) -> str:
        # This is the exact identity of the *software simulation descriptor*.
        # Relative phase must be committed: equal Born probabilities are not
        # equal coherent states.  float.hex() records Python's exact binary64
        # values; this is not a tomography identity for an unknown device state.
        return digest({
            "schema": "w33.continuation-selector.v2",
            "roots": list(self.roots),
            "amplitudes_binary64_hex": [list(_complex_hex(z)) for z in self.amplitudes],
        })

    @property
    def root_table_id(self) -> str:
        """Classical identity of the external continuation-slot table alone."""
        return digest({"schema": "w33.continuation-root-table.v1", "roots": list(self.roots)})

    def probabilities(self) -> tuple[float, ...]:
        return tuple(abs(z) ** 2 for z in self.amplitudes)

    def root_distribution(self) -> dict[str, float]:
        return {root: p for root, p in zip(self.roots, self.probabilities()) if p > 1e-15}

    def apply_transvection(self, axis: int, lam: int) -> "ContinuationSelector":
        perm = slot_permutation(axis, lam)
        out = [0j] * DIMENSION
        # U|i> = |perm[i]>.
        for i, z in enumerate(self.amplitudes):
            out[perm[i]] += z
        return ContinuationSelector(self.roots, tuple(out))

    def apply_diagonal_phase(self, phase_trits: tuple[int, ...]) -> "ContinuationSelector":
        if len(phase_trits) != DIMENSION or any(x not in (0, 1, 2) for x in phase_trits):
            raise ValueError("one F3 phase trit required per slot")
        omega = cmath.exp(2j * cmath.pi / 3)
        return ContinuationSelector(
            self.roots,
            tuple(z * (omega ** phase_trits[i]) for i, z in enumerate(self.amplitudes)),
        )

    def measure_by_quantile(self, q: float) -> str:
        """Deterministic inverse-CDF measurement harness for replayable tests."""
        if not 0.0 <= q < 1.0:
            raise ValueError("measurement quantile must lie in [0,1)")
        running = 0.0
        for root, p in zip(self.roots, self.probabilities()):
            running += p
            if q < running + 1e-15:
                return root
        return self.roots[-1]


def uniform_selector() -> ContinuationSelector:
    roots = tuple(digest({"schema": "w33.demo-continuation-slot.v1", "slot": i}) for i in range(DIMENSION))
    amp = 1.0 / sqrt(DIMENSION)
    return ContinuationSelector(roots, tuple(complex(amp, 0.0) for _ in range(DIMENSION)))


def steinberg_certificate() -> dict[str, Any]:
    path = ROOT / "data" / "PART_W33_20260901_K33_STEINBERG_PRIMITIVE.json"
    return json.loads(path.read_text(encoding="utf-8"))


def verify() -> dict[str, Any]:
    cert = steinberg_certificate()
    primitive = cert["scaledOperator"]
    exact_rank81 = (
        cert.get("status") == "PASS"
        and primitive.get("isPrimitiveSteinberg81Projector") is True
        and str(primitive.get("actualPermutationSpaceRank")) == "81"
    )

    permutations = [slot_permutation(axis, lam) for axis in range(40) for lam in (1, 2)]
    all_bijections = all(len(set(p)) == DIMENSION for p in permutations)
    zero_fixed_by_all = all(p[ZERO_SLOT] == ZERO_SLOT for p in permutations)
    # The sum of all basis vectors is also fixed by every permutation. Either
    # fixed vector is enough to witness reducibility of this naive model.
    uniform_vector_fixed = all(sorted(p) == list(range(DIMENSION)) for p in permutations)

    selector = uniform_selector()
    moved = selector.apply_transvection(7, 2)
    phase_trits = tuple(sum(v) % 3 for v in SLOTS)
    phased = moved.apply_diagonal_phase(phase_trits)
    measured = phased.measure_by_quantile(0.37)

    # A nonuniform two-slot state makes the root/amplitude split observable.
    roots = selector.roots
    amps = [0j] * DIMENSION
    amps[3] = complex(sqrt(0.25), 0)
    amps[11] = complex(sqrt(0.75), 0)
    sparse = ContinuationSelector(roots, tuple(amps))
    sparse_distribution = sparse.root_distribution()

    # Equal probabilities with a changed relative phase must be distinct
    # coherent simulation states while retaining the same classical root table.
    phased_amps = list(amps)
    phased_amps[11] *= -1
    sparse_phase_flip = ContinuationSelector(roots, tuple(phased_amps))

    checks = {
        "repository_certifies_a_primitive_rank81_steinberg_projector": exact_rank81,
        "phase_space_has_exactly_81_slots": DIMENSION == 3**4 == 81,
        "all_80_W33_transvections_act_as_slot_bijections": len(permutations) == 80 and all_bijections,
        "naive_phase_space_model_has_nonzero_fixed_zero_slot": zero_fixed_by_all,
        "naive_permutation_model_has_fixed_uniform_vector": uniform_vector_fixed,
        "therefore_dimension_match_does_not_identify_steinberg_irrep": exact_rank81 and zero_fixed_by_all,
        "coherent_selector_norm_survives_transvection": isclose(_norm2(moved.amplitudes), 1.0, abs_tol=1e-12),
        "coherent_selector_norm_survives_phase": isclose(_norm2(phased.amplitudes), 1.0, abs_tol=1e-12),
        "measurement_returns_external_classical_continuation_root": measured in selector.roots,
        "sparse_superposition_probabilities_are_exact": (
            len(sparse_distribution) == 2
            and isclose(sparse_distribution[roots[3]], 0.25, abs_tol=1e-12)
            and isclose(sparse_distribution[roots[11]], 0.75, abs_tol=1e-12)
        ),
        "Merkle_roots_are_classical_table_entries_not_amplitudes": all(isinstance(z, complex) for z in sparse.amplitudes) and all(isinstance(r, str) for r in sparse.roots),
        "relative_phase_changes_coherent_selector_identity": sparse.selector_id != sparse_phase_flip.selector_id,
        "relative_phase_does_not_change_classical_root_table_identity": sparse.root_table_id == sparse_phase_flip.root_table_id,
        "relative_phase_flip_preserves_Born_distribution": sparse.probabilities() == sparse_phase_flip.probabilities(),
    }
    return {
        "schema": "w33.continuation-superposition-semantics.v2",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "steinberg_anchor": {
            "source": "data/PART_W33_20260901_K33_STEINBERG_PRIMITIVE.json",
            "primitive_rank": 81,
            "primitive_projector_certified": exact_rank81,
        },
        "naive_81_slot_model": {
            "basis": "F3^4",
            "dimension": DIMENSION,
            "transvection_permutations": len(permutations),
            "fixed_zero_slot": ZERO_SLOT,
            "reducibility_witness": "|0> is fixed by all 80 transvections; the all-ones vector is also invariant",
            "conclusion": "The obvious F3^4 continuation-slot permutation model is not automatically the primitive Steinberg-81 representation.",
        },
        "coherent_control_semantics": {
            "selector_id": sparse.selector_id,
            "root_table_id": sparse.root_table_id,
            "phase_flipped_selector_id": sparse_phase_flip.selector_id,
            "nonzero_slots": [3, 11],
            "probabilities": [0.25, 0.75],
            "measurement_surface": "slot measurement returns one external authenticated continuation root",
            "root_storage": "classical immutable Merkle archive outside the 81-dimensional amplitude register",
            "simulation_identity_boundary": "selector_id commits exact Python binary64 amplitude components; it is a software-state identity, not physical tomography",
        },
        "next_representation_theory_target": (
            "Construct and verify an explicit intertwiner/projector from an operational continuation-control basis into the repository's primitive Steinberg-81 image. "
            "Until that map exists, coherent continuation selection is an abstract 81-dimensional control semantics, not a demonstrated encoding in the protected Steinberg sector."
        ),
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    raise SystemExit(out["status"] != "PASS")
