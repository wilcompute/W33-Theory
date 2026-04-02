"""Executable W(3,3) finite spectral triple candidate.

This module packages a first explicit internal geometry candidate F_W33 from
the exact 27-plet data already present in the repository.

What is implemented:
  - the canonical 27-state basis per generation from root_k2 data;
  - a Higgs-contracted integer mass kernel extracted from the exact cubic
    tensor on the three generation legs;
  - a generation-blind lift to H_matter = 27 x 3;
  - the even/real finite triple data on H_F = H_matter (+) H_matter^c;
  - explicit U(1)_Y, weak-doublet, and color-triplet support operators.

What is not claimed:
  - a proof that this is already the unique Standard Model finite triple;
  - the full Connes order-zero/order-one/orientability theorem for W(3,3);
  - the missing refinement/scaling bridge to a genuine 4D continuum.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Sequence

import numpy as np


REPO_ROOT = Path(__file__).resolve().parent.parent
if __package__ in {None, ""}:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    from exploration._artifact_paths import resolve_repo_data_path
else:
    from ._artifact_paths import resolve_repo_data_path

META_PATH = resolve_repo_data_path(
    REPO_ROOT,
    Path("extracted_v13")
    / "W33-Theory-master"
    / "artifacts"
    / "e8_root_metadata_table.json",
)
SC_PATH = resolve_repo_data_path(
    REPO_ROOT, Path("artifacts") / "e8_structure_constants_w33_discrete.json"
)
L3_PATH = resolve_repo_data_path(
    REPO_ROOT, Path("V24_output_v13_full") / "l3_patch_triples_full.jsonl"
)

PER_GENERATION_DIM = 27
GENERATION_COUNT = 3
MATTER_DIM = PER_GENERATION_DIM * GENERATION_COUNT
TOTAL_DIM = 2 * MATTER_DIM
HIGGS_SOURCE_I27 = (20, 21, 22, 23)
SPINOR_SOURCE_I27 = tuple(range(1, 17))
VECTOR_SOURCE_I27 = tuple(range(17, 27))

_SM_ORDER = {
    "S": 0,
    "Q": 1,
    "u_c": 2,
    "d_c": 3,
    "L": 4,
    "e_c": 5,
    "nu_c": 6,
    "T": 7,
    "H": 8,
    "Tbar": 9,
    "Hbar": 10,
}


@dataclass(frozen=True)
class BasisState:
    """One basis state in the candidate finite internal space."""

    generation: int
    local_index: int
    matter_index: int
    source_i27: int
    slot: str
    sm: str
    sector: str
    su5: str
    su3: str
    su2: str
    hypercharge: Fraction
    color: int | None
    isospin: int | None
    root_k2: tuple[int, ...]


@dataclass(frozen=True)
class FiniteSpectralTripleCandidate:
    """Packaged finite internal geometry candidate."""

    algebra_label: str
    generation_basis: tuple[BasisState, ...]
    matter_basis: tuple[BasisState, ...]
    source_order_per_canonical: tuple[int, ...]
    mass_matrix_27: np.ndarray
    mass_matrix_81: np.ndarray
    dirac_162: np.ndarray
    grading_162: np.ndarray
    real_structure_162: np.ndarray
    hypercharge_27: np.ndarray
    hypercharge_81: np.ndarray
    hypercharge_162: np.ndarray
    weak_doublet_blocks_27: tuple[tuple[int, ...], ...]
    q_color_block_27: tuple[int, ...]
    color_triplet_blocks_27: tuple[tuple[int, ...], ...]
    color_antitriplet_blocks_27: tuple[tuple[int, ...], ...]


def _fraction(num: int, den: int = 1) -> Fraction:
    return Fraction(num, den)


@lru_cache(maxsize=1)
def _meta_rows() -> tuple[dict, ...]:
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    return tuple(meta["rows"])


@lru_cache(maxsize=1)
def _g1_rows_generation_zero() -> tuple[dict, ...]:
    rows = {}
    for row in _meta_rows():
        if row["grade"] == "g1" and row["i3"] == 0:
            rows[row["i27"]] = row
    if len(rows) != PER_GENERATION_DIM:
        raise ValueError(f"Expected 27 g1 rows at i3=0, found {len(rows)}")
    return tuple(rows[i27] for i27 in range(PER_GENERATION_DIM))


def _classify_spinor(root_k2: Sequence[int]) -> dict[str, object]:
    inner = [root_k2[2], root_k2[3], root_k2[4], root_k2[5], root_k2[6]]
    n_neg = sum(1 for value in inner if value < 0)
    neg_positions = [idx for idx, value in enumerate(inner) if value < 0]

    if n_neg == 0:
        return {
            "su5": "1",
            "sm": "nu_c",
            "su3": "1",
            "su2": "1",
            "hypercharge": _fraction(0),
            "color": None,
            "isospin": None,
        }

    if n_neg == 4:
        pos = [idx for idx, value in enumerate(inner) if value > 0][0]
        if pos <= 2:
            return {
                "su5": "5bar",
                "sm": "d_c",
                "su3": "3bar",
                "su2": "1",
                "hypercharge": _fraction(1, 3),
                "color": pos + 1,
                "isospin": None,
            }
        return {
            "su5": "5bar",
            "sm": "L",
            "su3": "1",
            "su2": "2",
            "hypercharge": _fraction(-1, 2),
            "color": None,
            "isospin": pos - 3,
        }

    if n_neg == 2:
        color_neg = [idx for idx in neg_positions if idx <= 2]
        weak_neg = [idx for idx in neg_positions if idx >= 3]

        if len(color_neg) == 2 and len(weak_neg) == 0:
            pos_color = [idx for idx in range(3) if idx not in color_neg][0]
            return {
                "su5": "10",
                "sm": "u_c",
                "su3": "3bar",
                "su2": "1",
                "hypercharge": _fraction(-2, 3),
                "color": pos_color + 1,
                "isospin": None,
            }

        if len(color_neg) == 1 and len(weak_neg) == 1:
            return {
                "su5": "10",
                "sm": "Q",
                "su3": "3",
                "su2": "2",
                "hypercharge": _fraction(1, 6),
                "color": color_neg[0] + 1,
                "isospin": weak_neg[0] - 3,
            }

        if len(color_neg) == 0 and len(weak_neg) == 2:
            return {
                "su5": "10",
                "sm": "e_c",
                "su3": "1",
                "su2": "1",
                "hypercharge": _fraction(1),
                "color": None,
                "isospin": None,
            }

    raise ValueError(f"Unrecognized spinor root_k2 pattern: {tuple(root_k2)}")


def _classify_vector(root_k2: Sequence[int]) -> dict[str, object]:
    inner = [root_k2[2], root_k2[3], root_k2[4], root_k2[5], root_k2[6]]
    nonzero = [(idx, value) for idx, value in enumerate(inner) if value != 0]
    if len(nonzero) != 1:
        raise ValueError(f"Unrecognized vector root_k2 pattern: {tuple(root_k2)}")

    pos, value = nonzero[0]
    is_5bar = value > 0

    if pos <= 2:
        return {
            "su5": "5bar" if is_5bar else "5",
            "sm": "Tbar" if is_5bar else "T",
            "su3": "3bar" if is_5bar else "3",
            "su2": "1",
            "hypercharge": _fraction(1, 3) if is_5bar else _fraction(-1, 3),
            "color": pos + 1,
            "isospin": None,
        }

    return {
        "su5": "5bar" if is_5bar else "5",
        "sm": "Hbar" if is_5bar else "H",
        "su3": "1",
        "su2": "2",
        "hypercharge": _fraction(-1, 2) if is_5bar else _fraction(1, 2),
        "color": None,
        "isospin": pos - 3,
    }


def _classify_source_state(source_i27: int, root_k2: Sequence[int]) -> dict[str, object]:
    if source_i27 == 0:
        return {
            "sector": "singlet",
            "su5": "1",
            "sm": "S",
            "su3": "1",
            "su2": "1",
            "hypercharge": _fraction(0),
            "color": None,
            "isospin": None,
        }

    if source_i27 in SPINOR_SOURCE_I27:
        info = _classify_spinor(root_k2)
        info["sector"] = "spinor"
        return info

    if source_i27 in VECTOR_SOURCE_I27:
        info = _classify_vector(root_k2)
        info["sector"] = "vector"
        return info

    raise ValueError(f"Unexpected source i27 index: {source_i27}")


def _slot_name(sm: str, color: int | None, isospin: int | None) -> str:
    if sm == "Q":
        return f"Q_{color}_{isospin + 1}"
    if sm in {"u_c", "d_c", "T", "Tbar"}:
        return f"{sm}_{color}"
    if sm in {"L", "H", "Hbar"}:
        return f"{sm}_{isospin + 1}"
    return sm


def _canonical_sort_key(info: dict[str, object]) -> tuple[int, int, int, int]:
    color = info["color"] or 0
    isospin = info["isospin"] or 0
    return (
        _SM_ORDER[info["sm"]],
        color,
        isospin,
        int(info["source_i27"]),
    )


@lru_cache(maxsize=1)
def canonical_generation_basis() -> tuple[BasisState, ...]:
    source_states = []
    for row in _g1_rows_generation_zero():
        source_i27 = row["i27"]
        root_k2 = tuple(int(value) for value in row["root_k2"])
        info = _classify_source_state(source_i27, root_k2)
        info["source_i27"] = source_i27
        info["root_k2"] = root_k2
        source_states.append(info)

    source_states.sort(key=_canonical_sort_key)
    basis = []
    for local_index, info in enumerate(source_states):
        basis.append(
            BasisState(
                generation=0,
                local_index=local_index,
                matter_index=local_index,
                source_i27=int(info["source_i27"]),
                slot=_slot_name(
                    str(info["sm"]),
                    info["color"],
                    info["isospin"],
                ),
                sm=str(info["sm"]),
                sector=str(info["sector"]),
                su5=str(info["su5"]),
                su3=str(info["su3"]),
                su2=str(info["su2"]),
                hypercharge=info["hypercharge"],
                color=info["color"],
                isospin=info["isospin"],
                root_k2=tuple(int(value) for value in info["root_k2"]),
            )
        )
    return tuple(basis)


@lru_cache(maxsize=1)
def source_order_per_canonical() -> tuple[int, ...]:
    return tuple(state.source_i27 for state in canonical_generation_basis())


@lru_cache(maxsize=1)
def matter_basis(num_generations: int = GENERATION_COUNT) -> tuple[BasisState, ...]:
    basis = []
    template = canonical_generation_basis()
    for generation in range(num_generations):
        offset = generation * PER_GENERATION_DIM
        for state in template:
            basis.append(
                BasisState(
                    generation=generation,
                    local_index=state.local_index,
                    matter_index=offset + state.local_index,
                    source_i27=state.source_i27,
                    slot=state.slot,
                    sm=state.sm,
                    sector=state.sector,
                    su5=state.su5,
                    su3=state.su3,
                    su2=state.su2,
                    hypercharge=state.hypercharge,
                    color=state.color,
                    isospin=state.isospin,
                    root_k2=state.root_k2,
                )
            )
    return tuple(basis)


@lru_cache(maxsize=1)
def _tensor_source_basis() -> np.ndarray:
    sc_data = json.loads(SC_PATH.read_text(encoding="utf-8"))
    sc_roots = [tuple(root) for root in sc_data["basis"]["roots"]]
    cartan_dim = int(sc_data["basis"]["cartan_dim"])

    grade_by_orbit = {}
    i27_by_orbit = {}
    i3_by_orbit = {}
    for row in _meta_rows():
        root_orbit = tuple(row["root_orbit"])
        grade_by_orbit[root_orbit] = row["grade"]
        i27_by_orbit[root_orbit] = row.get("i27")
        i3_by_orbit[root_orbit] = row.get("i3")

    idx_i27 = {}
    idx_i3 = {}
    for root_index, root in enumerate(sc_roots):
        sc_index = cartan_dim + root_index
        if grade_by_orbit.get(root) == "g1":
            idx_i27[sc_index] = i27_by_orbit.get(root)
            idx_i3[sc_index] = i3_by_orbit.get(root)

    tensor = np.zeros((PER_GENERATION_DIM, PER_GENERATION_DIM, PER_GENERATION_DIM))
    with L3_PATH.open(encoding="utf-8") as handle:
        for line in handle:
            entry = json.loads(line)
            gi = [(idx_i3[idx], idx_i27[idx]) for idx in entry["in"]]
            gi.sort(key=lambda pair: pair[0])
            tensor[gi[0][1], gi[1][1], gi[2][1]] += entry["coeff"]
    return tensor


@lru_cache(maxsize=1)
def canonical_cubic_tensor_27() -> np.ndarray:
    """Return the exact cubic tensor in canonical 27-basis order."""

    perm = source_order_per_canonical()
    return _tensor_source_basis()[np.ix_(perm, perm, perm)]


@lru_cache(maxsize=1)
def higgs_contracted_mass_matrix_27() -> np.ndarray:
    tensor = canonical_cubic_tensor_27()
    mass_source = np.zeros((PER_GENERATION_DIM, PER_GENERATION_DIM))
    for higgs_index in HIGGS_SOURCE_I27:
        slice_matrix = tensor[:, :, higgs_index]
        mass_source += slice_matrix.T @ slice_matrix

    if not np.allclose(mass_source, mass_source.T):
        raise ValueError("Higgs-contracted mass kernel should be symmetric")
    if not np.allclose(mass_source, np.rint(mass_source)):
        raise ValueError("Higgs-contracted mass kernel should be integer-valued")
    return np.rint(mass_source).astype(np.int64)


@lru_cache(maxsize=1)
def matter_mass_matrix_81(num_generations: int = GENERATION_COUNT) -> np.ndarray:
    return np.kron(np.eye(num_generations, dtype=np.int64), higgs_contracted_mass_matrix_27())


@lru_cache(maxsize=1)
def grading_162(num_generations: int = GENERATION_COUNT) -> np.ndarray:
    matter_dim = num_generations * PER_GENERATION_DIM
    plus = np.eye(matter_dim, dtype=np.int64)
    minus = -np.eye(matter_dim, dtype=np.int64)
    return np.block(
        [
            [plus, np.zeros((matter_dim, matter_dim), dtype=np.int64)],
            [np.zeros((matter_dim, matter_dim), dtype=np.int64), minus],
        ]
    )


@lru_cache(maxsize=1)
def real_structure_162(num_generations: int = GENERATION_COUNT) -> np.ndarray:
    matter_dim = num_generations * PER_GENERATION_DIM
    identity = np.eye(matter_dim, dtype=np.int64)
    zeros = np.zeros((matter_dim, matter_dim), dtype=np.int64)
    return np.block([[zeros, identity], [identity, zeros]])


@lru_cache(maxsize=1)
def finite_dirac_162(num_generations: int = GENERATION_COUNT) -> np.ndarray:
    matter_mass = matter_mass_matrix_81(num_generations)
    zeros = np.zeros_like(matter_mass)
    return np.block([[zeros, matter_mass], [matter_mass, zeros]])


@lru_cache(maxsize=1)
def hypercharge_operator_27() -> np.ndarray:
    values = [float(state.hypercharge) for state in canonical_generation_basis()]
    return np.diag(values)


@lru_cache(maxsize=1)
def hypercharge_operator_81(num_generations: int = GENERATION_COUNT) -> np.ndarray:
    return np.kron(np.eye(num_generations), hypercharge_operator_27())


@lru_cache(maxsize=1)
def hypercharge_operator_162(num_generations: int = GENERATION_COUNT) -> np.ndarray:
    hypercharge = hypercharge_operator_81(num_generations)
    zeros = np.zeros_like(hypercharge)
    return np.block([[hypercharge, zeros], [zeros, -hypercharge]])


@lru_cache(maxsize=1)
def sector_block_indices_27() -> dict[str, tuple[int, ...]]:
    blocks: dict[str, list[int]] = {}
    for state in canonical_generation_basis():
        blocks.setdefault(state.sm, []).append(state.local_index)
    return {key: tuple(value) for key, value in blocks.items()}


@lru_cache(maxsize=1)
def weak_doublet_blocks_27() -> tuple[tuple[int, ...], ...]:
    q_blocks = {}
    for state in canonical_generation_basis():
        if state.sm == "Q":
            q_blocks.setdefault(state.color, []).append(state.local_index)

    blocks = [tuple(indices) for _, indices in sorted(q_blocks.items())]
    sector_blocks = sector_block_indices_27()
    for name in ("L", "H", "Hbar"):
        blocks.append(sector_blocks[name])
    return tuple(blocks)


@lru_cache(maxsize=1)
def q_color_block_27() -> tuple[int, ...]:
    return sector_block_indices_27()["Q"]


@lru_cache(maxsize=1)
def color_triplet_blocks_27() -> tuple[tuple[int, ...], ...]:
    sector_blocks = sector_block_indices_27()
    return (sector_blocks["T"],)


@lru_cache(maxsize=1)
def color_antitriplet_blocks_27() -> tuple[tuple[int, ...], ...]:
    sector_blocks = sector_block_indices_27()
    return (
        sector_blocks["u_c"],
        sector_blocks["d_c"],
        sector_blocks["Tbar"],
    )


def quaternion_matrix(alpha: complex, beta: complex) -> np.ndarray:
    """Embed a quaternion into M_2(C)."""

    return np.array(
        [
            [alpha, beta],
            [-np.conjugate(beta), np.conjugate(alpha)],
        ],
        dtype=complex,
    )


def weak_factor_operator_27(alpha: complex, beta: complex) -> np.ndarray:
    """Act by the same quaternionic block on every weak doublet."""

    operator = np.eye(PER_GENERATION_DIM, dtype=complex)
    block = quaternion_matrix(alpha, beta)
    for indices in weak_doublet_blocks_27():
        operator[np.ix_(indices, indices)] = block
    return operator


def color_factor_operator_27(
    color_matrix: np.ndarray,
    *,
    conjugate_antitriplets: bool = True,
) -> np.ndarray:
    """Act on color triplet sectors in the canonical 27-state basis."""

    color_matrix = np.asarray(color_matrix, dtype=complex)
    if color_matrix.shape != (3, 3):
        raise ValueError("color_matrix must be 3x3")

    operator = np.eye(PER_GENERATION_DIM, dtype=complex)
    operator[np.ix_(q_color_block_27(), q_color_block_27())] = np.kron(
        color_matrix,
        np.eye(2, dtype=complex),
    )
    for indices in color_triplet_blocks_27():
        operator[np.ix_(indices, indices)] = color_matrix

    anti_color = np.conjugate(color_matrix) if conjugate_antitriplets else color_matrix
    for indices in color_antitriplet_blocks_27():
        operator[np.ix_(indices, indices)] = anti_color
    return operator


def u1_hypercharge_phase_27(theta: float) -> np.ndarray:
    """Exponentiate the diagonal hypercharge operator."""

    values = np.diag(hypercharge_operator_27())
    return np.diag(np.exp(1j * theta * values))


@lru_cache(maxsize=1)
def build_w33_finite_spectral_triple(
    num_generations: int = GENERATION_COUNT,
) -> FiniteSpectralTripleCandidate:
    return FiniteSpectralTripleCandidate(
        algebra_label=(
            "Candidate F_W33 gauge support: exact U(1)_Y diagonal plus weak-doublet "
            "quaternionic blocks and color-triplet M_3(C) blocks on the canonical 27 basis"
        ),
        generation_basis=canonical_generation_basis(),
        matter_basis=matter_basis(num_generations),
        source_order_per_canonical=source_order_per_canonical(),
        mass_matrix_27=higgs_contracted_mass_matrix_27(),
        mass_matrix_81=matter_mass_matrix_81(num_generations),
        dirac_162=finite_dirac_162(num_generations),
        grading_162=grading_162(num_generations),
        real_structure_162=real_structure_162(num_generations),
        hypercharge_27=hypercharge_operator_27(),
        hypercharge_81=hypercharge_operator_81(num_generations),
        hypercharge_162=hypercharge_operator_162(num_generations),
        weak_doublet_blocks_27=weak_doublet_blocks_27(),
        q_color_block_27=q_color_block_27(),
        color_triplet_blocks_27=color_triplet_blocks_27(),
        color_antitriplet_blocks_27=color_antitriplet_blocks_27(),
    )
