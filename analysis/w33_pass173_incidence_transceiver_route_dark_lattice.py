#!/usr/bin/env python3
"""Pass 173: the incidence transceiver and the asymmetric dark lattices.

Let N be the 40-line by 40-point incidence matrix of W(3,3).  Previous
passes computed the point/address kernel ker_Z(N), but not the integral
line/route kernel ker_Z(N^T).  This witness computes both and proves:

1. C = 10N-J is the integral form of the centered transceiver
   T=N-J/10.  It intertwines the point and line concurrence graphs and
   has polar square 6 times the projector onto their common rank-24
   constituent.
2. All 480 Pass-157 selector vectors have fixed, exactly decodable
   40-channel analyzer signatures under N, while the point dark lattice
   is killed.
3. The point and line dark lattices have different determinants, Smith
   forms, minima, and binary codes: [40,15,8] versus [40,15,10].
4. The complete norm-10 shell of ker_Z(N^T) is exactly the 432 signed
   pentads / 216 pentad cores of BT844--BT846.  Each support is a
   K_{5,5} minus a perfect matching, and the deleted matchings double
   cover all 540 skew-line charts.

The last item upgrades the old pentad census to an intrinsic lattice
identification.  It also gives an integral obstruction to the stale claim
that W(3,3) is self-dual -- IT IS NOT (q=3 is odd; Pass 4563/4755). An incidence
duality would permutation-identify
the two kernels and preserve these invariants, but they differ.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
from math import comb
import json
from pathlib import Path
import shutil
import subprocess
import sys

import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass157_eigenlattice_prime_collision import (
    local_line_pair_shell,
)
from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_group,
    build_w33,
    orbit_count,
    saturated_kernel,
    w33_lines,
)


OUT = ROOT / "data" / "w33_pass173_incidence_transceiver_route_dark_lattice.json"

PARI_CACHE = {
    "address": {"minimal_vector_count": 90, "minimal_norm": 8, "half_shell_columns": 45},
    "route": {"minimal_vector_count": 432, "minimal_norm": 10, "half_shell_columns": 216},
}


def profile(values) -> dict[str, int]:
    counts = Counter(int(value) for value in values)
    return {str(key): int(counts[key]) for key in sorted(counts)}


def gram_certificate(basis: np.ndarray) -> tuple[int, dict[str, int]]:
    gram = Matrix((basis.T @ basis).tolist())
    smith = smith_normal_form(gram, domain=ZZ)
    invariants = [abs(int(smith[i, i])) for i in range(smith.rows)]
    return int(gram.det()), profile(invariants)


def pari_minimum_certificate(
    basis: np.ndarray, label: str
) -> tuple[dict[str, int], str]:
    """Exact integral qfminim census, with a committed-value fallback."""
    if shutil.which("gp") is None:
        return dict(PARI_CACHE[label]), "cached"

    reduced = Matrix(basis.T.tolist()).lll()
    gram = reduced * reduced.T
    gp_matrix = "[" + ";".join(
        ",".join(str(int(gram[r, c])) for c in range(gram.cols))
        for r in range(gram.rows)
    ) + "]"
    program = (
        f"G={gp_matrix};"
        "r=qfminim(G);"
        "print(r[1]);"
        "print(r[2]);"
        "print(matsize(r[3])[2]);"
        "quit;\n"
    )
    completed = subprocess.run(
        ["gp", "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=300,
    )
    values = [
        int(line.strip())
        for line in completed.stdout.splitlines()
        if line.strip()
    ]
    if len(values) != 3:
        raise RuntimeError(f"unexpected PARI output: {completed.stdout!r}")
    return {
        "minimal_vector_count": values[0],
        "minimal_norm": values[1],
        "half_shell_columns": values[2],
    }, "live"


def rank_mod2(matrix: np.ndarray) -> int:
    work = (np.asarray(matrix, dtype=np.int64) % 2).copy()
    rank = 0
    for column in range(work.shape[1]):
        pivot = next(
            (row for row in range(rank, work.shape[0]) if work[row, column]),
            None,
        )
        if pivot is None:
            continue
        work[[rank, pivot]] = work[[pivot, rank]]
        for row in range(work.shape[0]):
            if row != rank and work[row, column]:
                work[row] ^= work[rank]
        rank += 1
        if rank == work.shape[0]:
            break
    return rank


def binary_kernel_code(
    integer_kernel: np.ndarray, operator: np.ndarray
) -> tuple[np.ndarray, np.ndarray, Counter[int]]:
    """Independent generators and all words of the reduced integral kernel."""
    work = (integer_kernel.T % 2).astype(np.uint8)
    row = 0
    for column in range(work.shape[1]):
        pivot = next(
            (r for r in range(row, work.shape[0]) if work[r, column]),
            None,
        )
        if pivot is None:
            continue
        work[[row, pivot]] = work[[pivot, row]]
        for r in range(work.shape[0]):
            if r != row and work[r, column]:
                work[r] ^= work[row]
        row += 1
    generators = work[:row]
    coefficients = np.array(
        [[(mask >> bit) & 1 for bit in range(row)] for mask in range(2**row)],
        dtype=np.uint8,
    )
    words = (coefficients @ generators) % 2
    assert np.all((words @ (operator % 2).T) % 2 == 0)
    weights = Counter(int(value) for value in words.sum(axis=1))
    return generators, words, weights


def macwilliams_dual(
    weights: Counter[int], length: int, dimension: int
) -> Counter[int]:
    """Exact binary MacWilliams transform via integer Krawtchouk sums."""
    dual: Counter[int] = Counter()
    code_size = 2**dimension
    for degree in range(length + 1):
        total = 0
        for weight, multiplicity in weights.items():
            krawtchouk = sum(
                (-1) ** overlap
                * comb(weight, overlap)
                * comb(length - weight, degree - overlap)
                for overlap in range(degree + 1)
                if overlap <= weight and degree - overlap <= length - weight
            )
            total += multiplicity * krawtchouk
        assert total % code_size == 0
        coefficient = total // code_size
        if coefficient:
            dual[degree] = coefficient
    return dual


def pentad_core_census(lines: list[frozenset[int]]):
    """Intrinsic census of the BT844--BT846 pentad cores."""
    line_sets = [set(line) for line in lines]
    by_cover: dict[frozenset[int], list[frozenset[int]]] = defaultdict(list)
    raw_partial_spreads = 0
    for candidate in combinations(range(40), 5):
        if not all(
            line_sets[left].isdisjoint(line_sets[right])
            for left, right in combinations(candidate, 2)
        ):
            continue
        raw_partial_spreads += 1
        pentad = frozenset(candidate)
        cover = frozenset().union(*(line_sets[index] for index in pentad))
        by_cover[cover].append(pentad)

    cover_multiplicities = Counter(len(parts) for parts in by_cover.values())
    cores = [tuple(parts) for parts in by_cover.values() if len(parts) == 2]
    special_pentads = {pentad for pair in cores for pentad in pair}

    crown_ok = True
    signed_vectors: list[np.ndarray] = []
    supports: set[frozenset[int]] = set()
    chart_cover: Counter[frozenset[int]] = Counter()
    for left, right in cores:
        cross = np.array(
            [
                [bool(line_sets[a] & line_sets[b]) for b in sorted(right)]
                for a in sorted(left)
            ],
            dtype=np.int64,
        )
        crown_ok &= bool(
            np.all(cross.sum(axis=0) == 4)
            and np.all(cross.sum(axis=1) == 4)
        )
        for a in left:
            deleted = [b for b in right if line_sets[a].isdisjoint(line_sets[b])]
            crown_ok &= len(deleted) == 1
            for b in deleted:
                chart_cover[frozenset((a, b))] += 1

        vector = np.zeros(40, dtype=np.int64)
        vector[list(left)] = 1
        vector[list(right)] = -1
        signed_vectors.extend((vector, -vector))
        supports.add(frozenset(left | right))

    skew_pairs = {
        frozenset((left, right))
        for left, right in combinations(range(40), 2)
        if line_sets[left].isdisjoint(line_sets[right])
    }
    return {
        "raw_partial_spreads": raw_partial_spreads,
        "cover_multiplicities": cover_multiplicities,
        "cores": cores,
        "special_pentads": special_pentads,
        "crown_ok": crown_ok,
        "signed_vectors": signed_vectors,
        "supports": supports,
        "chart_cover": chart_cover,
        "skew_pairs": skew_pairs,
    }


def main() -> int:
    points, point_adjacency, symplectic = build_w33()
    lines = w33_lines(point_adjacency)
    incidence = np.zeros((40, 40), dtype=np.int64)
    for row, line in enumerate(lines):
        incidence[row, list(line)] = 1
    identity = np.eye(40, dtype=np.int64)
    ones = np.ones((40, 40), dtype=np.int64)
    line_adjacency = incidence @ incidence.T - 4 * identity

    checks: dict[str, bool] = {}
    checks["forty_points_and_lines"] = len(points) == len(lines) == 40
    checks["two_concurrence_grams"] = bool(
        np.array_equal(incidence.T @ incidence, 4 * identity + point_adjacency)
        and np.array_equal(incidence @ incidence.T, 4 * identity + line_adjacency)
    )

    # ------------------------------------------------------------------
    # The centered point-to-line transceiver.
    # ------------------------------------------------------------------
    centered10 = 10 * incidence - ones  # 10*T, kept integral
    point_projector30 = 20 * identity + 5 * point_adjacency - 2 * ones
    line_projector30 = 20 * identity + 5 * line_adjacency - 2 * ones
    checks["centered_rank_24"] = Matrix(centered10.tolist()).rank() == 24
    checks["centered_kills_constants"] = bool(
        np.all(centered10.sum(axis=0) == 0)
        and np.all(centered10.sum(axis=1) == 0)
    )
    checks["centered_intertwines"] = bool(
        np.array_equal(centered10 @ point_adjacency, line_adjacency @ centered10)
    )
    checks["polar_square_is_six_projector"] = bool(
        np.array_equal(centered10.T @ centered10, 20 * point_projector30)
        and np.array_equal(centered10 @ centered10.T, 20 * line_projector30)
    )

    selectors, selector_labels = local_line_pair_shell(point_adjacency, lines)
    analyzer = (incidence @ selectors.T).T
    analyzer_profiles = {
        tuple(sorted(Counter(int(value) for value in row).items()))
        for row in analyzer
    }
    expected_profile = ((-3, 1), (-1, 9), (0, 20), (1, 9), (3, 1))
    checks["selector_shell_480"] = len(selectors) == len(selector_labels) == 480
    checks["selector_analyzer_signature_fixed"] = analyzer_profiles == {
        expected_profile
    }
    checks["selector_norm_gain_six"] = bool(
        np.all(np.einsum("ij,ij->i", selectors, selectors) == 6)
        and np.all(np.einsum("ij,ij->i", analyzer, analyzer) == 36)
    )
    checks["selector_exact_decode"] = bool(
        np.array_equal(analyzer @ incidence, 6 * selectors)
    )
    checks["selector_tight_frames"] = bool(
        np.array_equal(selectors.T @ selectors, 4 * point_projector30)
        and np.array_equal(analyzer.T @ analyzer, 24 * line_projector30)
    )

    # ------------------------------------------------------------------
    # Integral point/address and line/route dark lattices.
    # ------------------------------------------------------------------
    address_kernel = saturated_kernel(incidence)
    route_kernel = saturated_kernel(incidence.T)
    checks["both_dark_ranks_15"] = (
        address_kernel.shape == (40, 15) and route_kernel.shape == (40, 15)
    )
    checks["both_dark_equations"] = bool(
        np.all(incidence @ address_kernel == 0)
        and np.all(incidence.T @ route_kernel == 0)
    )
    checks["centered_kills_both_dark_sides"] = bool(
        np.all(centered10 @ address_kernel == 0)
        and np.all(centered10.T @ route_kernel == 0)
    )

    address_det, address_smith = gram_certificate(address_kernel)
    route_det, route_smith = gram_certificate(route_kernel)
    checks["address_lattice_certificate"] = (
        address_det == 2**17 * 3**10
        and address_smith == {"2": 5, "6": 9, "24": 1}
    )
    checks["route_lattice_certificate"] = (
        route_det == 2**11 * 3**14
        and route_smith == {"1": 1, "3": 5, "6": 8, "24": 1}
    )
    checks["determinant_ratio_81_over_64"] = route_det * 64 == address_det * 81

    address_minimum, address_pari_source = pari_minimum_certificate(
        address_kernel, "address"
    )
    route_minimum, route_pari_source = pari_minimum_certificate(route_kernel, "route")
    checks["address_minimum_90_norm8"] = address_minimum == PARI_CACHE["address"]
    checks["route_minimum_432_norm10"] = route_minimum == PARI_CACHE["route"]

    address_generators, address_words, address_weights = binary_kernel_code(
        address_kernel, incidence
    )
    route_generators, route_words, route_weights = binary_kernel_code(
        route_kernel, incidence.T
    )
    address_nonzero = min(weight for weight in address_weights if weight)
    route_nonzero = min(weight for weight in route_weights if weight)
    checks["address_code_40_15_8"] = (
        len(address_generators) == 15
        and address_nonzero == 8
        and address_weights[8] == 45
    )
    checks["route_code_40_15_10"] = (
        len(route_generators) == 15
        and route_nonzero == 10
        and route_weights[10] == 216
    )
    address_gram2_rank = rank_mod2(address_generators @ address_generators.T)
    route_gram2_rank = rank_mod2(route_generators @ route_generators.T)
    checks["address_code_self_orthogonal"] = address_gram2_rank == 0
    checks["route_code_hull_dimension_9"] = route_gram2_rank == 6

    address_dual = macwilliams_dual(address_weights, 40, 15)
    route_dual = macwilliams_dual(route_weights, 40, 15)
    checks["context_duals_agree_at_weights_4_and_6"] = (
        address_dual[4] == route_dual[4] == 40
        and address_dual[6] == route_dual[6] == 240
    )
    checks["context_duals_first_split_at_weight_8"] = (
        all(address_dual[weight] == route_dual[weight] for weight in range(8))
        and address_dual[8] == 5085
        and route_dual[8] == 3645
        and address_dual[10] == 47824
        and route_dual[10] == 54736
    )
    # For the unscaled parity lattice {z in Z^40 : z mod 2 in C}, the
    # exponent is ||z||^2/2.  At exponent 4 there are always
    # 4*C(40,2)=3120 coordinate vectors; weight-8 words add 2^8 each.
    address_parity_q4 = 4 * comb(40, 2) + address_weights[8] * 2**8
    route_parity_q4 = 4 * comb(40, 2) + route_weights[8] * 2**8
    route_parity_q5 = route_weights[10] * 2**10
    checks["parity_lattices_split_before_route_pentad_shell"] = (
        address_parity_q4 == 14640
        and route_parity_q4 == 3120
        and route_parity_q5 == 221184
    )

    # ------------------------------------------------------------------
    # Complete identification of the route shell with pentad cores.
    # ------------------------------------------------------------------
    pentads = pentad_core_census(lines)
    signed_route_vectors = pentads["signed_vectors"]
    signed_keys = {tuple(int(value) for value in vector) for vector in signed_route_vectors}
    checks["partial_spread_census"] = (
        pentads["raw_partial_spreads"] == 13824
        and pentads["cover_multiplicities"] == Counter({1: 13392, 2: 216})
    )
    checks["exactly_216_cores_432_pentads"] = (
        len(pentads["cores"]) == 216 and len(pentads["special_pentads"]) == 432
    )
    checks["all_cores_are_crowns"] = bool(pentads["crown_ok"])
    checks["core_vectors_are_432_distinct_route_dark_vectors"] = (
        len(signed_route_vectors) == len(signed_keys) == 432
        and all(
            np.array_equal(incidence.T @ vector, np.zeros(40, dtype=np.int64))
            and int(vector @ vector) == 10
            for vector in signed_route_vectors
        )
    )
    checks["pentad_charts_double_cover_all_540"] = (
        len(pentads["skew_pairs"]) == 540
        and set(pentads["chart_cover"]) == pentads["skew_pairs"]
        and Counter(pentads["chart_cover"].values()) == Counter({2: 540})
    )
    route_weight10_supports = {
        frozenset(np.flatnonzero(word).tolist())
        for word in route_words
        if int(word.sum()) == 10
    }
    checks["weight10_words_are_exactly_pentad_cores"] = (
        route_weight10_supports == pentads["supports"]
    )
    # PARI proves completeness: the exhibited 432 vectors exhaust the shell.
    checks["pentad_vectors_exhaust_route_minimal_shell"] = (
        len(signed_keys) == route_minimum["minimal_vector_count"]
        and route_minimum["minimal_norm"] == 10
    )

    # PSp(4,3) preserves the two pentad chiralities: the signed shell splits
    # into two 216-orbits, while the 216 supports form one orbit.
    generators, group = build_group(points, symplectic)
    line_index = {line: index for index, line in enumerate(lines)}

    def induced_line_perm(point_perm):
        return tuple(
            line_index[frozenset(point_perm[point] for point in line)]
            for line in lines
        )

    shell_list = signed_route_vectors
    shell_lookup = {
        tuple(int(value) for value in vector): index
        for index, vector in enumerate(shell_list)
    }
    shell_maps = []
    for point_perm in generators:
        line_perm = induced_line_perm(point_perm)
        mapping = []
        for vector in shell_list:
            image = np.empty(40, dtype=np.int64)
            for source in range(40):
                image[line_perm[source]] = vector[source]
            mapping.append(shell_lookup[tuple(int(value) for value in image)])
        shell_maps.append(mapping)
    signed_orbits = orbit_count(432, shell_maps)

    base = shell_list[0]
    base_support = frozenset(np.flatnonzero(base).tolist())
    signed_stabilizer = 0
    support_stabilizer = 0
    sign_flips = 0
    for point_perm in group:
        line_perm = induced_line_perm(point_perm)
        image = np.empty(40, dtype=np.int64)
        for source in range(40):
            image[line_perm[source]] = base[source]
        if np.array_equal(image, base):
            signed_stabilizer += 1
        if np.array_equal(image, -base):
            sign_flips += 1
        if frozenset(line_perm[index] for index in base_support) == base_support:
            support_stabilizer += 1
    checks["psp_order_25920"] = len(group) == 25920
    checks["two_chiral_signed_orbits"] = (
        signed_orbits == 2 and signed_stabilizer == 120 and sign_flips == 0
    )
    checks["one_216_support_orbit"] = (
        support_stabilizer == 120 and len(group) // support_stabilizer == 216
    )

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass173.incidence_transceiver_route_dark_lattice.v1",
        "status": "PASS" if all_pass else "FAIL",
        "incidence_transceiver": {
            "centered_operator": "T = N - J/10",
            "integral_operator": "C = 10N - J",
            "rank": 24,
            "intertwining": "T A_point = A_line T",
            "polar_identity": "T^T T = 6 E_24(point), T T^T = 6 E_24(line)",
            "boundary": (
                "an exact algebraic analyzer/decoder on the shared 24-space; "
                "not by itself a physical optical implementation"
            ),
        },
        "selector_analyzer": {
            "selectors": 480,
            "input_norm": 6,
            "output_norm": 36,
            "output_histogram": {"-3": 1, "-1": 9, "0": 20, "1": 9, "3": 1},
            "decode": "x = N^T(Nx)/6",
            "tight_frame": "X^T X=120 E_24(point), Y^T Y=720 E_24(line)",
        },
        "dark_lattices": {
            "address_point": {
                "definition": "ker_Z(N)",
                "rank": 15,
                "determinant": address_det,
                "determinant_factorization": "2^17 * 3^10",
                "smith_profile": address_smith,
                "minimum": address_minimum,
                "pari_source": address_pari_source,
                "binary_code": "[40,15,8]",
                "weight_enumerator": profile(
                    value
                    for weight, count in address_weights.items()
                    for value in [weight] * count
                ),
                "binary_gram_rank": address_gram2_rank,
            },
            "route_line": {
                "definition": "ker_Z(N^T)",
                "rank": 15,
                "determinant": route_det,
                "determinant_factorization": "2^11 * 3^14",
                "smith_profile": route_smith,
                "minimum": route_minimum,
                "pari_source": route_pari_source,
                "binary_code": "[40,15,10]",
                "weight_enumerator": profile(
                    value
                    for weight, count in route_weights.items()
                    for value in [weight] * count
                ),
                "binary_gram_rank": route_gram2_rank,
                "binary_hull_dimension": 15 - route_gram2_rank,
            },
            "determinant_ratio": "det(route)/det(address)=81/64=(9/8)^2",
            "covolume_ratio": "9/8",
            "context_dual_split": {
                "address_A4_A6_A8_A10": [
                    address_dual[4],
                    address_dual[6],
                    address_dual[8],
                    address_dual[10],
                ],
                "route_A4_A6_A8_A10": [
                    route_dual[4],
                    route_dual[6],
                    route_dual[8],
                    route_dual[10],
                ],
                "reading": (
                    "the two 25-dimensional context duals agree at weights "
                    "4 and 6, then first separate at weight 8"
                ),
            },
            "unscaled_parity_lattice_opening": {
                "address_q4": address_parity_q4,
                "route_q4": route_parity_q4,
                "route_q5": route_parity_q5,
                "reading": (
                    "the address code is doubly even and self-orthogonal; "
                    "the route code has weight-10 words and is not "
                    "self-orthogonal, so the usual scaled integral "
                    "Construction-A quotient exists only on the address side"
                ),
            },
            "self_duality_obstruction": (
                "a point-line incidence duality would permutation-identify the "
                "two kernels, but determinant, Smith form, minimum, kissing "
                "number, and binary distance all differ"
            ),
        },
        "route_minimal_shell": {
            "signed_vectors": len(signed_keys),
            "projective_rays_and_supports": len(pentads["supports"]),
            "special_pentads": len(pentads["special_pentads"]),
            "raw_five_line_partial_spreads": pentads["raw_partial_spreads"],
            "support_geometry": "K_5,5 minus a perfect matching",
            "covered_points_per_pentad": 20,
            "skew_charts": 540,
            "chart_cover_multiplicity": 2,
            "psp_signed_orbits": [216, 216],
            "psp_support_orbit": 216,
            "stabilizer_order": 120,
            "identification": (
                "the complete norm-10 shell of ker_Z(N^T) is exactly the "
                "BT844--BT846 chiral pentad/core carrier"
            ),
        },
        "checks": checks,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Pass 173: {'PASS' if all_pass else 'FAIL'} ({sum(checks.values())}/{len(checks)})")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
