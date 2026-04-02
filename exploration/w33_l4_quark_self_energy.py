"""Exact l4 quark self-energy sector after the cubic no-go.

This module packages the next higher-tower result after the induced-quark
firewall obstruction.

What is implemented:
  - the full SU(3)xSU(2) screen on the complete 27-slice cubic span, proving
    that no raw cubic linear combination opens a clean quark direction;
  - exact contraction of the repo's l4 tower data into generation-diagonal
    27x27 operators of the form l4(a_0, b_1, h_2, x_2) -> y_2;
  - classification of the 54 firewall-triad contractions into clean and
    nonclean operator families;
  - extraction of the clean triplet-family l4 sector and its exact quark-only
    image under the full screen;
  - primitive integer counterterms supported only on Q, u_c, and d_c.

What is not claimed:
  - cancellation of the induced quark Yukawa residual;
  - a final Standard Model quark mass theorem;
  - the missing 4D refinement/scaling theorem.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration._artifact_paths import resolve_repo_data_path
from w33_finite_spectral_triple import (
    canonical_cubic_tensor_27,
    canonical_generation_basis,
    color_factor_operator_27,
    sector_block_indices_27,
    weak_factor_operator_27,
)
from w33_quark_firewall_obstruction import firewall_triad_records


L4_PATH = resolve_repo_data_path(
    ROOT, Path("V24_output_v13_full") / "l4_patch_quads_full.jsonl"
)
META_PATH = resolve_repo_data_path(
    ROOT,
    Path("extracted_v13")
    / "W33-Theory-master"
    / "artifacts"
    / "e8_root_metadata_table.json",
)
SC_PATH = resolve_repo_data_path(
    ROOT, Path("artifacts") / "e8_structure_constants_w33_discrete.json"
)
FLOAT_TOL = 1e-10
TRIPLET_FAMILIES = ("quark_triplet", "antiquark_triplet")
QUARK_SECTORS = ("Q", "u_c", "d_c")
UD_ONLY_SECTORS = ("u_c", "d_c")
UD_ONLY_COUNTERTERM_TERMS = (
    (-1, ("u_c_2", "Tbar_1", "d_c_3")),
    (-1, ("d_c_3", "Tbar_1", "u_c_2")),
    (1, ("d_c_1", "Tbar_2", "u_c_3")),
    (1, ("u_c_1", "Tbar_3", "d_c_2")),
)
FULL_QUARK_COUNTERTERM_TERMS = (
    (-1, ("u_c_3", "d_c_1", "Tbar_2")),
    (1, ("d_c_2", "u_c_1", "Tbar_3")),
    (1, ("Q_1_1", "Q_2_2", "T_3")),
    (1, ("Q_1_2", "Q_3_1", "T_2")),
)


@dataclass(frozen=True)
class ContractedL4OperatorSummary:
    """Summary data for one contracted l4 operator."""

    family: str
    ordered_slots: tuple[str, str, str]
    repeated_slot: str
    support_count: int
    matrix_rank: int
    residual_norm: float
    clean: bool


@dataclass(frozen=True)
class CountertermEntry:
    """One nonzero counterterm matrix entry."""

    row_slot: str
    col_slot: str
    value: int


@dataclass(frozen=True)
class CountertermTerm:
    """One contracted-l4 term in a primitive counterterm."""

    coefficient: int
    ordered_slots: tuple[str, str, str]


@dataclass(frozen=True)
class L4QuarkSelfEnergyCandidate:
    """Packaged higher-tower quark self-energy result."""

    full27_cubic_slice_screen_rank: int
    full27_cubic_slice_screen_nullity: int
    total_contracted_operator_count: int
    clean_operator_count: int
    nonclean_operator_count: int
    clean_family_counts: tuple[tuple[str, int], ...]
    nonclean_family_counts: tuple[tuple[str, int], ...]
    clean_triplet_operator_count: int
    nonclean_triplet_operator_count: int
    quark_only_subspace_dimension: int
    q_linked_subspace_dimension: int
    ud_only_subspace_dimension: int
    explicit_ud_only_counterterm_terms: tuple[CountertermTerm, ...]
    explicit_ud_only_counterterm_entries: tuple[CountertermEntry, ...]
    explicit_full_quark_counterterm_terms: tuple[CountertermTerm, ...]
    explicit_full_quark_counterterm_entries: tuple[CountertermEntry, ...]


@dataclass(frozen=True)
class _ContractedL4Operator:
    family: str
    ordered_slots: tuple[str, str, str]
    matrix_sympy: sp.Matrix
    residual_norm: float


def _numpy_matrix(matrix: sp.Matrix) -> np.ndarray:
    return np.array(matrix.tolist(), dtype=float)


@lru_cache(maxsize=1)
def _canonical_basis_lookup() -> tuple[
    dict[str, int],
    dict[str, int],
    dict[int, str],
    dict[int, str],
]:
    slot_to_source = {}
    slot_to_local = {}
    local_to_slot = {}
    source_to_slot = {}
    for state in canonical_generation_basis():
        slot_to_source[state.slot] = state.source_i27
        slot_to_local[state.slot] = state.local_index
        local_to_slot[state.local_index] = state.slot
        source_to_slot[state.source_i27] = state.slot
    return slot_to_source, slot_to_local, local_to_slot, source_to_slot


@lru_cache(maxsize=1)
def _sympy_permutation_source_to_local() -> sp.Matrix:
    _, slot_to_local, _, source_to_slot = _canonical_basis_lookup()
    matrix = sp.zeros(27, 27)
    for source_i27, slot in source_to_slot.items():
        matrix[slot_to_local[slot], source_i27] = 1
    return matrix


@lru_cache(maxsize=1)
def _grade_maps() -> dict[str, object]:
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    sc = json.loads(SC_PATH.read_text(encoding="utf-8"))
    cartan_dim = sc["basis"]["cartan_dim"]
    sc_roots = [tuple(root) for root in sc["basis"]["roots"]]

    grade_by_orbit = {}
    i27_by_orbit = {}
    i3_by_orbit = {}
    for row in meta["rows"]:
        root_orbit = tuple(row["root_orbit"])
        grade_by_orbit[root_orbit] = row["grade"]
        i27_by_orbit[root_orbit] = row.get("i27")
        i3_by_orbit[root_orbit] = row.get("i3")

    sc_by_generation_source = {}
    for index, root_orbit in enumerate(sc_roots):
        sc_idx = cartan_dim + index
        if grade_by_orbit.get(root_orbit) == "g1":
            sc_by_generation_source[
                (i3_by_orbit[root_orbit], i27_by_orbit[root_orbit])
            ] = sc_idx
    return {"sc_by_generation_source": sc_by_generation_source}


@lru_cache(maxsize=1)
def _l4_lookup() -> dict[tuple[tuple[int, ...], int], int]:
    lookup = {}
    with L4_PATH.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            lookup[(tuple(sorted(record["in"])), record["out"])] = record["coeff"]
    return lookup


def _parity_to_sorted(args: tuple[int, int, int, int]) -> int:
    pairs = list(enumerate(args))
    sorted_pairs = sorted(pairs, key=lambda item: item[1])
    permutation = [old_index for old_index, _ in sorted_pairs]
    inversions = 0
    for left in range(len(permutation)):
        for right in range(left + 1, len(permutation)):
            if permutation[left] > permutation[right]:
                inversions += 1
    return -1 if inversions % 2 else 1


@lru_cache(maxsize=1)
def _full_weak_generators_27() -> tuple[np.ndarray, ...]:
    return (
        weak_factor_operator_27(0, 1),
        weak_factor_operator_27(0, -1j),
        weak_factor_operator_27(1, 0),
    )


@lru_cache(maxsize=1)
def _full_color_generators_27() -> tuple[np.ndarray, ...]:
    generators = (
        np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex),
        np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex),
        (1.0 / np.sqrt(3.0))
        * np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex),
    )
    return tuple(color_factor_operator_27(matrix) for matrix in generators)


def full_screen_residual_norm_27(matrix: np.ndarray) -> float:
    total = 0.0
    for weak in _full_weak_generators_27():
        for color in _full_color_generators_27():
            residual = (matrix @ weak - weak @ matrix) @ color - color @ (
                matrix @ weak - weak @ matrix
            )
            total += float(np.linalg.norm(residual) ** 2)
    return float(np.sqrt(total))


@lru_cache(maxsize=1)
def full27_cubic_slice_screen_rank_nullity() -> tuple[int, int]:
    tensor = canonical_cubic_tensor_27().astype(float)
    columns = []
    for state in canonical_generation_basis():
        matrix = tensor[:, :, state.local_index]
        residual_vectors = []
        for weak in _full_weak_generators_27():
            for color in _full_color_generators_27():
                residual = (matrix @ weak - weak @ matrix) @ color - color @ (
                    matrix @ weak - weak @ matrix
                )
                residual_vectors.append(residual.reshape(-1))
        columns.append(np.concatenate(residual_vectors))
    screen = np.stack(columns, axis=1)
    gram = screen.T @ screen
    rank = int(np.linalg.matrix_rank(gram, tol=FLOAT_TOL))
    return rank, screen.shape[1] - rank


def _contracted_l4_operator_sympy_by_source(
    a_source: int,
    b_source: int,
    h_source: int,
    *,
    target_generation: int = 2,
) -> sp.Matrix:
    lookup = _l4_lookup()
    sc_by_generation_source = _grade_maps()["sc_by_generation_source"]
    permutation = _sympy_permutation_source_to_local()

    a = sc_by_generation_source[(0, a_source)]
    b = sc_by_generation_source[(1, b_source)]
    h = sc_by_generation_source[(target_generation, h_source)]

    source_matrix = sp.zeros(27, 27)
    for x_source in range(27):
        if x_source == h_source:
            continue
        x = sc_by_generation_source[(target_generation, x_source)]
        args = (a, b, h, x)
        sorted_args = tuple(sorted(args))
        sign = _parity_to_sorted(args)
        for y_source in range(27):
            y = sc_by_generation_source[(target_generation, y_source)]
            coeff = lookup.get((sorted_args, y), 0)
            if coeff:
                source_matrix[y_source, x_source] = sign * coeff
    return permutation * source_matrix * permutation.T


@lru_cache(maxsize=None)
def contracted_l4_operator_27(ordered_slots: tuple[str, str, str]) -> np.ndarray:
    slot_to_source, _, _, _ = _canonical_basis_lookup()
    matrix = _contracted_l4_operator_sympy_by_source(
        slot_to_source[ordered_slots[0]],
        slot_to_source[ordered_slots[1]],
        slot_to_source[ordered_slots[2]],
    )
    return _numpy_matrix(matrix)


@lru_cache(maxsize=1)
def _contracted_l4_records() -> tuple[_ContractedL4Operator, ...]:
    _, _, _, source_to_slot = _canonical_basis_lookup()
    records = []
    for triad in firewall_triad_records():
        for repeated_index, repeated_source in enumerate(triad.e6ids):
            other_sources = [
                source
                for index, source in enumerate(triad.e6ids)
                if index != repeated_index
            ]
            for a_source, b_source in (tuple(other_sources), tuple(reversed(other_sources))):
                ordered_slots = (
                    source_to_slot[a_source],
                    source_to_slot[b_source],
                    source_to_slot[repeated_source],
                )
                matrix_sympy = _contracted_l4_operator_sympy_by_source(
                    a_source,
                    b_source,
                    repeated_source,
                )
                residual_norm = full_screen_residual_norm_27(
                    _numpy_matrix(matrix_sympy)
                )
                records.append(
                    _ContractedL4Operator(
                        family=triad.family,
                        ordered_slots=ordered_slots,
                        matrix_sympy=matrix_sympy,
                        residual_norm=residual_norm,
                    )
                )
    return tuple(records)


@lru_cache(maxsize=1)
def contracted_l4_operator_summaries() -> tuple[ContractedL4OperatorSummary, ...]:
    summaries = []
    for record in _contracted_l4_records():
        matrix = _numpy_matrix(record.matrix_sympy)
        summaries.append(
            ContractedL4OperatorSummary(
                family=record.family,
                ordered_slots=record.ordered_slots,
                repeated_slot=record.ordered_slots[2],
                support_count=int(np.count_nonzero(np.abs(matrix) > FLOAT_TOL)),
                matrix_rank=int(np.linalg.matrix_rank(matrix)),
                residual_norm=record.residual_norm,
                clean=bool(np.isclose(record.residual_norm, 0.0, atol=FLOAT_TOL)),
            )
        )
    return tuple(summaries)


@lru_cache(maxsize=1)
def _clean_triplet_records() -> tuple[_ContractedL4Operator, ...]:
    clean = []
    for record in _contracted_l4_records():
        if (
            record.family in TRIPLET_FAMILIES
            and np.isclose(record.residual_norm, 0.0, atol=FLOAT_TOL)
        ):
            clean.append(record)
    return tuple(clean)


def _subspace_image_rank(allowed_sectors: tuple[str, ...]) -> int:
    blocks = sector_block_indices_27()
    clean_triplet = _clean_triplet_records()

    forbidden_rows = []
    allowed_rows = []
    for row_name, row_indices in blocks.items():
        for col_name, col_indices in blocks.items():
            for row_index in row_indices:
                for col_index in col_indices:
                    values = [
                        record.matrix_sympy[row_index, col_index]
                        for record in clean_triplet
                    ]
                    if row_name in allowed_sectors and col_name in allowed_sectors:
                        allowed_rows.append(values)
                    else:
                        forbidden_rows.append(values)

    forbidden = sp.Matrix(forbidden_rows)
    nullspace = forbidden.nullspace()
    if not nullspace:
        return 0
    allowed = sp.Matrix(allowed_rows)
    image = sp.Matrix.hstack(*[allowed * vector for vector in nullspace])
    return image.rank()


def _counterterm_matrix_sympy(
    terms: tuple[tuple[int, tuple[str, str, str]], ...],
) -> sp.Matrix:
    total = sp.zeros(27, 27)
    for coefficient, ordered_slots in terms:
        total += coefficient * sp.Matrix(
            contracted_l4_operator_27(ordered_slots).astype(int).tolist()
        )
    return total


def _counterterm_entries(
    matrix: sp.Matrix,
) -> tuple[CountertermEntry, ...]:
    _, _, local_to_slot, _ = _canonical_basis_lookup()
    entries = []
    for row_index in range(matrix.rows):
        for col_index in range(matrix.cols):
            value = matrix[row_index, col_index]
            if value != 0:
                entries.append(
                    CountertermEntry(
                        row_slot=local_to_slot[row_index],
                        col_slot=local_to_slot[col_index],
                        value=int(value),
                    )
                )
    return tuple(entries)


@lru_cache(maxsize=1)
def explicit_ud_only_counterterm_27() -> np.ndarray:
    return _numpy_matrix(_counterterm_matrix_sympy(UD_ONLY_COUNTERTERM_TERMS))


@lru_cache(maxsize=1)
def explicit_full_quark_counterterm_27() -> np.ndarray:
    return _numpy_matrix(_counterterm_matrix_sympy(FULL_QUARK_COUNTERTERM_TERMS))


@lru_cache(maxsize=1)
def build_l4_quark_self_energy_candidate() -> L4QuarkSelfEnergyCandidate:
    cubic_rank, cubic_nullity = full27_cubic_slice_screen_rank_nullity()
    summaries = contracted_l4_operator_summaries()
    clean_family_counts = Counter(summary.family for summary in summaries if summary.clean)
    nonclean_family_counts = Counter(
        summary.family for summary in summaries if not summary.clean
    )

    clean_triplet = [
        summary for summary in summaries if summary.clean and summary.family in TRIPLET_FAMILIES
    ]
    nonclean_triplet = [
        summary
        for summary in summaries
        if (not summary.clean) and summary.family in TRIPLET_FAMILIES
    ]

    quark_only_dimension = _subspace_image_rank(QUARK_SECTORS)
    ud_only_dimension = _subspace_image_rank(UD_ONLY_SECTORS)
    q_linked_dimension = quark_only_dimension - ud_only_dimension

    ud_matrix = _counterterm_matrix_sympy(UD_ONLY_COUNTERTERM_TERMS)
    full_quark_matrix = _counterterm_matrix_sympy(FULL_QUARK_COUNTERTERM_TERMS)

    return L4QuarkSelfEnergyCandidate(
        full27_cubic_slice_screen_rank=cubic_rank,
        full27_cubic_slice_screen_nullity=cubic_nullity,
        total_contracted_operator_count=len(summaries),
        clean_operator_count=sum(1 for summary in summaries if summary.clean),
        nonclean_operator_count=sum(1 for summary in summaries if not summary.clean),
        clean_family_counts=tuple(sorted(clean_family_counts.items())),
        nonclean_family_counts=tuple(sorted(nonclean_family_counts.items())),
        clean_triplet_operator_count=len(clean_triplet),
        nonclean_triplet_operator_count=len(nonclean_triplet),
        quark_only_subspace_dimension=quark_only_dimension,
        q_linked_subspace_dimension=q_linked_dimension,
        ud_only_subspace_dimension=ud_only_dimension,
        explicit_ud_only_counterterm_terms=tuple(
            CountertermTerm(coefficient=coeff, ordered_slots=slots)
            for coeff, slots in UD_ONLY_COUNTERTERM_TERMS
        ),
        explicit_ud_only_counterterm_entries=_counterterm_entries(ud_matrix),
        explicit_full_quark_counterterm_terms=tuple(
            CountertermTerm(coefficient=coeff, ordered_slots=slots)
            for coeff, slots in FULL_QUARK_COUNTERTERM_TERMS
        ),
        explicit_full_quark_counterterm_entries=_counterterm_entries(
            full_quark_matrix
        ),
    )
