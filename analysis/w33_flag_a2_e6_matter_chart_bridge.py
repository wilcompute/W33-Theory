"""MCCXLV: flag-anchored A2/E6/matter chart bridge.

The spectral bridge commit proves that the 240 W33 local corners carry the
E8-style split

    240 = 6 + 72 + 81 + 81.

This verifier constructs the split instead of only counting it.  A point-line
flag (p0, L0) selects:

* six same-point corners at p0, the A2-root packet;
* seventy-two adjacent-point corners, grouped as twenty-four triples;
* two 81-corner nonadjacent sectors, each grouped as twenty-seven triples.

Each 81-sector is a full coordinate chart for the rational lambda=-2
eigenspace of the k=3 corner graph.  The natural A2-triplet quotient is also
tested: it preserves rank 24 in the golden tight-frame space, so the E8 rank-8
bridge is not the naive triplet-sum quotient.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import w33_e8_spectral_bridge as spectral  # noqa: E402


def _counter(values: list[int] | np.ndarray) -> dict[str, int]:
    return {str(int(key)): int(value) for key, value in sorted(Counter(values).items())}


def rank_mod_prime(matrix: np.ndarray, prime: int = 7) -> int:
    """Row rank over GF(prime), used as an exact rational-rank certificate."""

    rows = [[int(entry) % prime for entry in row] for row in matrix]
    if not rows:
        return 0

    row_count = len(rows)
    col_count = len(rows[0])
    rank = 0

    for col in range(col_count):
        pivot = None
        for row in range(rank, row_count):
            if rows[row][col]:
                pivot = row
                break
        if pivot is None:
            continue

        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][col], -1, prime)
        pivot_row = rows[rank]
        for idx in range(col, col_count):
            pivot_row[idx] = (pivot_row[idx] * inverse) % prime

        for row in range(rank + 1, row_count):
            factor = rows[row][col]
            if not factor:
                continue
            current = rows[row]
            for idx in range(col, col_count):
                current[idx] = (current[idx] - factor * pivot_row[idx]) % prime

        rank += 1
        if rank == col_count:
            return rank

    return rank


def base_corners(point: int) -> list[int]:
    return [idx for idx, (corner_point, _) in enumerate(spectral.local_vertices) if corner_point == point]


def flag_triplet_decomposition(point: int, line: int) -> dict[str, Any]:
    if line not in spectral.point_lines[point]:
        raise ValueError(f"line {line} is not incident with point {point}")

    base = base_corners(point)
    a2_singletons = [[idx] for idx in base]
    e6_triplets: list[list[int]] = []
    plus_triplets: list[list[int]] = []
    minus_triplets: list[list[int]] = []
    line_adjacent_triplets: list[list[int]] = []
    zero_adjacent_triplets: list[list[int]] = []

    for other_point in range(40):
        if other_point == point:
            continue

        corners = [
            idx
            for idx, (corner_point, _) in enumerate(spectral.local_vertices)
            if corner_point == other_point
        ]

        if spectral.adj[point][other_point]:
            connecting_line = spectral.edge_to_line[tuple(sorted((point, other_point)))]
            through = [idx for idx in corners if connecting_line in spectral.local_vertices[idx][1]]
            away = [idx for idx in corners if connecting_line not in spectral.local_vertices[idx][1]]
            line_adjacent_triplets.append(through)
            zero_adjacent_triplets.append(away)
            e6_triplets.extend([through, away])
            continue

        plus: list[int] = []
        minus: list[int] = []
        for idx in corners:
            signature = [int(spectral.G[idx, base_idx]) for base_idx in base]
            if sum(signature) != 1:
                raise AssertionError((point, line, idx, signature))
            slot = base[signature.index(1)]
            base_pair = spectral.local_vertices[slot][1]
            if line in base_pair:
                plus.append(idx)
            else:
                minus.append(idx)

        plus_triplets.append(plus)
        minus_triplets.append(minus)

    triplets = e6_triplets + plus_triplets + minus_triplets
    covered = {idx for group in a2_singletons + triplets for idx in group}

    return {
        "point": point,
        "line": line,
        "a2_singletons": a2_singletons,
        "e6_triplets": e6_triplets,
        "line_adjacent_triplets": line_adjacent_triplets,
        "zero_adjacent_triplets": zero_adjacent_triplets,
        "plus_triplets": plus_triplets,
        "minus_triplets": minus_triplets,
        "triplets": triplets,
        "covered": covered,
    }


def sector_indices(decomposition: dict[str, Any], key: str) -> list[int]:
    return [idx for group in decomposition[key] for idx in group]


def selection_matrix(indices: list[int], width: int = 240) -> np.ndarray:
    matrix = np.zeros((len(indices), width), dtype=int)
    for row, idx in enumerate(indices):
        matrix[row, idx] = 1
    return matrix


def hamming_h43_spectrum() -> dict[str, int]:
    # H(d,q) eigenvalues are (q-1)d - q*i with multiplicity C(d,i)(q-1)^i.
    return {"-4": 16, "-1": 32, "2": 24, "5": 8, "8": 1}


def rounded_spectrum(matrix: np.ndarray) -> dict[str, int]:
    values = np.linalg.eigvalsh(matrix)
    return {f"{key:.6g}": int(value) for key, value in sorted(Counter(round(float(x), 6) for x in values).items())}


def affine_nonneighbor_count(point: int) -> int:
    """Normalize nonneighbors by omega(point, q)=1; this gives 3^3 vectors."""

    base_vector = spectral.points[point]
    normalized: set[tuple[int, int, int, int]] = set()
    for other_point, vector in enumerate(spectral.points):
        if other_point == point or spectral.adj[point][other_point]:
            continue
        pairing = spectral.omega(base_vector, vector)
        inverse = 1 if pairing == 1 else 2
        normalized.add(tuple((inverse * entry) % 3 for entry in vector))
    return len(normalized)


def all_flag_summary() -> dict[str, Any]:
    minus2_mask = np.abs(spectral.eigs + 2) < 1e-8
    minus2_vectors = spectral.vecs[:, minus2_mask]
    golden = 3 + 3 * np.sqrt(5)
    golden_mask = np.abs(spectral.eigs - golden) < 1e-8
    golden_vectors = spectral.vecs[:, golden_mask]

    flags_checked = 0
    bad_flags: list[tuple[Any, ...]] = []
    minus2_chart_ranks: list[int] = []
    e6_golden_ranks: list[int] = []
    induced_degrees: list[int] = []
    affine_base_counts: list[int] = []

    for point in range(40):
        affine_base_counts.append(affine_nonneighbor_count(point))
        for line in spectral.point_lines[point]:
            packet = flag_triplet_decomposition(point, line)
            flags_checked += 1

            plus = sector_indices(packet, "plus_triplets")
            minus = sector_indices(packet, "minus_triplets")
            e6 = sector_indices(packet, "e6_triplets")
            covered = packet["covered"]

            expected_counts = (
                len(packet["a2_singletons"]),
                len(packet["e6_triplets"]),
                len(packet["plus_triplets"]),
                len(packet["minus_triplets"]),
                len(covered),
            )
            if expected_counts != (6, 24, 27, 27, 240):
                bad_flags.append(("counts", point, line, expected_counts))

            if any(len(group) != 3 for group in packet["triplets"]):
                bad_flags.append(("triplet_size", point, line))

            for sector in (plus, minus):
                rank = int(np.linalg.matrix_rank(minus2_vectors[sector, :], tol=1e-9))
                minus2_chart_ranks.append(rank)
                if rank != 81:
                    bad_flags.append(("minus2_chart_rank", point, line, rank))

                induced = spectral.A3[np.ix_(sector, sector)].astype(int)
                degrees = induced.sum(axis=1)
                induced_degrees.extend(int(value) for value in degrees)
                if not np.all(degrees == 8):
                    bad_flags.append(("induced_degree", point, line, _counter(degrees)))

            e6_rank = int(np.linalg.matrix_rank(golden_vectors[e6, :], tol=1e-9))
            e6_golden_ranks.append(e6_rank)
            if e6_rank != 24:
                bad_flags.append(("e6_golden_rank", point, line, e6_rank))

    return {
        "flags_checked": flags_checked,
        "bad_flags": bad_flags,
        "minus2_chart_rank_profile": _counter(minus2_chart_ranks),
        "e6_golden_rank_profile": _counter(e6_golden_ranks),
        "induced_degree_profile": _counter(induced_degrees),
        "affine_nonneighbor_count_profile": _counter(affine_base_counts),
    }


def representative_checks(point: int, line: int) -> dict[str, Any]:
    packet = flag_triplet_decomposition(point, line)
    plus = sector_indices(packet, "plus_triplets")
    minus = sector_indices(packet, "minus_triplets")
    e6 = sector_indices(packet, "e6_triplets")

    minus2_matrix = spectral.A3.astype(int) + 2 * np.eye(240, dtype=int)
    rank_minus2_equations = rank_mod_prime(minus2_matrix, 7)
    plus_constraint_rank = rank_mod_prime(np.vstack([minus2_matrix, selection_matrix(plus)]), 7)
    minus_constraint_rank = rank_mod_prime(np.vstack([minus2_matrix, selection_matrix(minus)]), 7)

    golden = 3 + 3 * np.sqrt(5)
    golden_vectors = spectral.vecs[:, np.abs(spectral.eigs - golden) < 1e-8]
    minus2_vectors = spectral.vecs[:, np.abs(spectral.eigs + 2) < 1e-8]

    triplet_sums_24 = np.array([golden_vectors[group, :].sum(axis=0) for group in packet["triplets"]])
    triplet_sums_minus2 = np.array([minus2_vectors[group, :].sum(axis=0) for group in packet["triplets"]])

    plus_induced = spectral.A3[np.ix_(plus, plus)].astype(int)
    minus_induced = spectral.A3[np.ix_(minus, minus)].astype(int)
    plus_edges = int(plus_induced.sum() // 2)
    minus_edges = int(minus_induced.sum() // 2)

    return {
        "point": point,
        "line": line,
        "point_vector": list(spectral.points[point]),
        "lines_through_point": list(spectral.point_lines[point]),
        "counts": {
            "a2_root_singletons": len(packet["a2_singletons"]),
            "e6_triplets": len(packet["e6_triplets"]),
            "line_adjacent_triplets": len(packet["line_adjacent_triplets"]),
            "zero_adjacent_triplets": len(packet["zero_adjacent_triplets"]),
            "plus_matter_triplets": len(packet["plus_triplets"]),
            "minus_matter_triplets": len(packet["minus_triplets"]),
            "all_triplets": len(packet["triplets"]),
            "covered_corners": len(packet["covered"]),
            "plus_matter_corners": len(plus),
            "minus_matter_corners": len(minus),
            "e6_corners": len(e6),
        },
        "exact_mod7_chart_certificate": {
            "rank_A3_plus_2I": rank_minus2_equations,
            "minus2_nullity": 240 - rank_minus2_equations,
            "rank_with_plus_sector_zero_constraints": plus_constraint_rank,
            "rank_with_minus_sector_zero_constraints": minus_constraint_rank,
            "reading": (
                "Over GF(7), A3+2I has rank 159. Adding zero-coordinate "
                "constraints on either 81-sector gives rank 240, so an exact "
                "lambda=-2 eigenvector is determined by its coordinates on either sector."
            ),
        },
        "triplet_quotient_rank_test": {
            "golden_24d_triplet_sum_rank": int(np.linalg.matrix_rank(triplet_sums_24, tol=1e-9)),
            "minus2_triplet_sum_rank": int(np.linalg.matrix_rank(triplet_sums_minus2, tol=1e-9)),
            "reading": "The natural A2-triplet-sum quotient preserves rank 24, so it is not the missing rank-8 E8 projection.",
        },
        "ternary_hypercube_budget": {
            "vertices_per_matter_sector": len(plus),
            "affine_nonneighbor_base": affine_nonneighbor_count(point),
            "fiber_size": len(plus) // affine_nonneighbor_count(point),
            "hamming_H_4_3_degree": 8,
            "hamming_H_4_3_edges": 324,
            "plus_induced_degree_profile": _counter(plus_induced.sum(axis=1)),
            "minus_induced_degree_profile": _counter(minus_induced.sum(axis=1)),
            "plus_induced_edges": plus_edges,
            "minus_induced_edges": minus_edges,
            "hamming_H_4_3_spectrum": hamming_h43_spectrum(),
            "plus_induced_spectrum": rounded_spectrum(plus_induced),
            "minus_induced_spectrum": rounded_spectrum(minus_induced),
            "same_budget_as_hamming_H_4_3": plus_edges == minus_edges == 324,
            "not_plain_hamming_graph": rounded_spectrum(plus_induced) != hamming_h43_spectrum()
            and rounded_spectrum(minus_induced) != hamming_h43_spectrum(),
        },
    }


def flag_a2_e6_matter_chart_packet() -> dict[str, Any]:
    point = spectral.points.index((1, 0, 0, 0))
    line = spectral.point_lines[point][0]
    representative = representative_checks(point, line)
    flags = all_flag_summary()

    checks = {
        "all_160_flags_checked": flags["flags_checked"] == 160,
        "all_flags_have_6_24_27_27_triplet_split": not flags["bad_flags"],
        "all_points_have_27_affine_nonneighbors": flags["affine_nonneighbor_count_profile"] == {"27": 40},
        "minus2_eigenspace_nullity_is_81": representative["exact_mod7_chart_certificate"]["minus2_nullity"] == 81,
        "plus_81_sector_is_exact_minus2_coordinate_chart": representative["exact_mod7_chart_certificate"][
            "rank_with_plus_sector_zero_constraints"
        ]
        == 240,
        "minus_81_sector_is_exact_minus2_coordinate_chart": representative["exact_mod7_chart_certificate"][
            "rank_with_minus_sector_zero_constraints"
        ]
        == 240,
        "all_81_sectors_have_numeric_minus2_rank_81": flags["minus2_chart_rank_profile"] == {"81": 320},
        "all_e6_sectors_carry_numeric_golden_rank_24": flags["e6_golden_rank_profile"] == {"24": 160},
        "matter_sector_A3_induced_degree_is_8": flags["induced_degree_profile"] == {"8": 25920},
        "matter_sector_has_hamming_vertex_edge_budget": representative["ternary_hypercube_budget"][
            "same_budget_as_hamming_H_4_3"
        ],
        "matter_sector_is_twisted_not_plain_hamming": representative["ternary_hypercube_budget"][
            "not_plain_hamming_graph"
        ],
        "naive_triplet_sum_does_not_collapse_24d_to_8d": representative["triplet_quotient_rank_test"][
            "golden_24d_triplet_sum_rank"
        ]
        == 24,
    }

    return {
        "part": "MCCXLV",
        "theorem": "Flag A2/E6 matter chart bridge",
        "input_bridge": "w33_e8_spectral_bridge.py MCCXXIX-MCCXLIV",
        "representative_flag": representative,
        "all_flag_summary": flags,
        "reading": (
            "A W33 point-line flag refines the E8-style 240=6+72+81+81 split "
            "into explicit packets: six same-point A2-root corners, twenty-four "
            "E6-root triples over adjacent points, and two 27x3 matter sectors "
            "over the affine nonneighbor cloud. Each 81 sector is a full exact "
            "coordinate chart for the lambda=-2 eigenspace; it has the same "
            "vertex/edge budget as the ternary hypercube H(4,3), but a different "
            "spectrum, so the sector is a twisted ternary hypercube rather than "
            "the plain Hamming network."
        ),
        "boundary": (
            "This proves the ternary matter-chart layer and rules out the naive "
            "A2-triplet-sum projection as the E8 rank-8 bridge. The remaining "
            "target is an additional triality quotient/identification."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = flag_a2_e6_matter_chart_packet()
    out_path = ROOT / "PART_MCCXLV_FLAG_A2_E6_MATTER_CHART_BRIDGE_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCXLV: Flag A2/E6 Matter Chart Bridge ===")
    print("flags checked:", packet["all_flag_summary"]["flags_checked"])
    print("representative counts:", packet["representative_flag"]["counts"])
    print("minus2 chart certificate:", packet["representative_flag"]["exact_mod7_chart_certificate"])
    print("verified:", packet["n_verified"], "/", len(packet["checks"]))


if __name__ == "__main__":
    main()
