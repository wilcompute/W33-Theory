#!/usr/bin/env python3
"""Pass 158: the chiral trade lattice and the two 480s.

Pass 157 identified the +2-eigenlattice L2 (rank 24, det 2^16 3^10 5,
minimal shell = the 480 oriented local line-pair selectors whose rays are
the 240 signed E8 roots).  This witness closes the spectral decomposition
of Z^40 and settles a G-set question the Ihara-zeta track left open.

A. THE CHIRAL EIGENLATTICE IS THE TRADE LATTICE.  The (-4)-eigenlattice
   L4 = {x in Z^40 : A x = -4 x} (rank 15 = g) is EXACTLY the lattice of
   integer point-weights with zero sum on every one of the 40 isotropic
   lines -- the saturated kernel of the line-point incidence matrix M.
   The chiral sector of the spectrum is the incidence kernel of the
   quadrangle: trades, in design-theoretic language.

B. THE GLUE IDENTITY.  With L12 = Z * (all-ones), the finite-index glue
   [Z^40 : L12 + L2 + L4] satisfies
       index^2 = det(L12) * det(L2) * det(L4),
   computed exactly, completing the Perron/gauge/chiral splitting of the
   standard unimodular Z^40.

C. THE MINIMAL TRADES.  Exact Fincke-Pohst enumeration of the minimal
   shell of L4, with combinatorial identification of the supports.

D. THE TWO 480s.  The 480 Hashimoto arcs (directed edges, the carrier of
   the Ihara zeta and graph RH) and the 480 minimal vectors of L2 are both
   transitive PSp(4,3)-sets with point stabilizers of order 54.  Are they
   isomorphic as G-sets?  Decided by the exact criterion: G/H = G/K iff H
   fixes a point of G/K (equal orders).  The orbital ranks of both actions
   and of the joint action are computed as the certificate.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import sys

import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.bt926_plus2_eigenlattice import canon, snf_with_transforms

OUT = ROOT / "data" / "w33_pass158_chiral_trade_lattice_two_480s.json"


# ----------------------------------------------------------------------
# substrate
# ----------------------------------------------------------------------


def build_w33():
    points = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})

    def symplectic(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    adjacency = np.zeros((40, 40), dtype=np.int64)
    for left, right in combinations(range(40), 2):
        if symplectic(points[left], points[right]) == 0:
            adjacency[left, right] = adjacency[right, left] = 1
    return points, adjacency, symplectic


def w33_lines(adjacency):
    return [
        frozenset(vertices)
        for vertices in combinations(range(40), 4)
        if all(adjacency[a, b] for a, b in combinations(vertices, 2))
    ]


def saturated_kernel(operator):
    """Z-basis (40 x r) of the saturated integer kernel of a 40x40 matrix."""
    diagonal, _, right = snf_with_transforms(operator)
    zero_columns = [c for c in range(40) if int(diagonal[c, c]) == 0]
    return np.array(
        [[int(right[row, c]) for c in zero_columns] for row in range(40)],
        dtype=np.int64,
    )


def lattices_equal(basis_a, basis_b):
    """Exact equality of the column-span lattices of two integer bases."""
    if basis_a.shape != basis_b.shape:
        return False
    mat_a = Matrix(basis_a.tolist())
    mat_b = Matrix(basis_b.tolist())
    try:
        coeff_ab = mat_a.solve(mat_b)
        coeff_ba = mat_b.solve(mat_a)
    except Exception:
        return False
    integral = all(value.is_Integer for value in coeff_ab) and all(
        value.is_Integer for value in coeff_ba
    )
    if not integral:
        return False
    return abs(coeff_ab.det()) == 1


# ----------------------------------------------------------------------
# Fincke-Pohst enumeration
# ----------------------------------------------------------------------


def fincke_pohst(gram, bound):
    """All nonzero x in Z^r with x^T G x <= bound (both signs), exact check.

    Float Cholesky with margins for pruning; every candidate is re-verified
    with exact integer arithmetic against the integer Gram matrix.
    """
    rank = gram.shape[0]
    gram_f = gram.astype(float)
    upper = np.linalg.cholesky(gram_f).T  # G = U^T U
    eps = 1e-9
    results = []
    coeff = np.zeros(rank, dtype=np.int64)

    def recurse(level, residual):
        # residual = bound - sum of squares of processed layers (float, padded)
        if level < 0:
            if any(coeff):
                vec = coeff.copy()
                norm = int(vec @ gram @ vec)
                if 0 < norm <= bound:
                    results.append((vec, norm))
            return
        # x_level contributes (U[level,level]*x + offset)^2
        offset = 0.0
        for j in range(level + 1, rank):
            offset += upper[level, j] * coeff[j]
        radius = np.sqrt(max(residual, 0.0) + eps)
        lo = int(np.ceil((-radius - offset) / upper[level, level] - eps))
        hi = int(np.floor((radius - offset) / upper[level, level] + eps))
        for value in range(lo, hi + 1):
            coeff[level] = value
            term = (upper[level, level] * value + offset) ** 2
            recurse(level - 1, residual - term)
        coeff[level] = 0

    recurse(rank - 1, float(bound))
    return results


def minimal_shell(basis):
    """LLL-reduce, then enumerate the minimal shell exactly."""
    reduced = Matrix(basis.T.tolist()).lll()  # rows are lattice vectors
    reduced_np = np.array(reduced.tolist(), dtype=np.int64)
    gram = reduced_np @ reduced_np.T
    bound = int(min(gram[i, i] for i in range(gram.shape[0])))
    found = fincke_pohst(gram, bound)
    min_norm = min(norm for _, norm in found)
    shell = [coeff @ reduced_np for coeff, norm in found if norm == min_norm]
    by_norm = Counter(norm for _, norm in found)
    return min_norm, shell, dict(sorted(by_norm.items())), reduced_np


# ----------------------------------------------------------------------
# the projective group as permutations of the 40 points
# ----------------------------------------------------------------------


def build_group(points, symplectic):
    """Close symplectic transvections T_v(x) = x + B(x,v) v by BFS."""
    index = {p: i for i, p in enumerate(points)}

    def transvection_perm(v):
        perm = []
        for p in points:
            b = symplectic(p, v)
            image = tuple((p[k] + b * v[k]) % 3 for k in range(4))
            perm.append(index[canon(image)])
        return tuple(perm)

    generators = [transvection_perm(p) for p in points]
    generators = sorted(set(generators))
    identity = tuple(range(40))
    seen = {identity}
    frontier = [identity]
    while frontier:
        new_frontier = []
        for element in frontier:
            for generator in generators:
                composed = tuple(generator[element[i]] for i in range(40))
                if composed not in seen:
                    seen.add(composed)
                    new_frontier.append(composed)
        frontier = new_frontier
    return generators, seen


def _orbits_of_subgroup(perms, size):
    """Orbits of a list of permutations (given as tuples) on range(size)."""
    seen = [False] * size
    orbits = []
    for start in range(size):
        if seen[start]:
            continue
        orbit = {start}
        stack = [start]
        seen[start] = True
        while stack:
            current = stack.pop()
            for perm in perms:
                image = perm[current]
                if not seen[image]:
                    seen[image] = True
                    orbit.add(image)
                    stack.append(image)
        orbits.append(orbit)
    return orbits


def orbit_count(size, neighbor_maps):
    """Number of orbits of the group generated by neighbor_maps on range(size)."""
    seen = np.zeros(size, dtype=bool)
    orbits = 0
    for start in range(size):
        if seen[start]:
            continue
        orbits += 1
        stack = [start]
        seen[start] = True
        while stack:
            current = stack.pop()
            for mapping in neighbor_maps:
                image = mapping[current]
                if not seen[image]:
                    seen[image] = True
                    stack.append(image)
    return orbits


def main():
    points, adjacency, symplectic = build_w33()
    identity = np.eye(40, dtype=np.int64)
    ones_matrix = np.ones((40, 40), dtype=np.int64)
    ones = np.ones(40, dtype=np.int64)
    lines = w33_lines(adjacency)

    checks = {}

    checks["w33_srg_relation"] = bool(
        np.array_equal(
            adjacency @ adjacency, 8 * identity - 2 * adjacency + 4 * ones_matrix
        )
    )

    # ------------------------------------------------------------------
    # A. the chiral eigenlattice is the trade lattice
    # ------------------------------------------------------------------
    chiral = saturated_kernel(adjacency + 4 * identity)
    checks["chiral_rank_15"] = chiral.shape == (40, 15)
    checks["chiral_eigenvector_equation"] = bool(
        np.array_equal(adjacency @ chiral, -4 * chiral)
    )

    incidence = np.zeros((40, 40), dtype=np.int64)
    for row, line in enumerate(lines):
        for point in line:
            incidence[row, point] = 1
    trade = saturated_kernel(incidence)
    checks["incidence_kernel_rank_15"] = trade.shape == (40, 15)
    checks["chiral_equals_trade_lattice"] = lattices_equal(chiral, trade)

    incidence_snf = smith_normal_form(Matrix(incidence.tolist()), domain=ZZ)
    incidence_invariants = sorted(
        abs(int(incidence_snf[i, i]))
        for i in range(40)
        if int(incidence_snf[i, i]) != 0
    )
    incidence_profile = Counter(incidence_invariants)

    # ------------------------------------------------------------------
    # B. Gram identification and the glue identity
    # ------------------------------------------------------------------
    gram = Matrix((chiral.T @ chiral).tolist())
    smith = smith_normal_form(gram, domain=ZZ)
    invariants = [abs(int(smith[i, i])) for i in range(15)]
    invariant_profile = Counter(invariants)
    determinant = int(gram.det())
    is_even = bool(all(int(gram[i, i]) % 2 == 0 for i in range(15)))

    gauge = saturated_kernel(adjacency - 2 * identity)
    checks["gauge_rank_24"] = gauge.shape == (40, 24)
    gauge_det = int((Matrix((gauge.T @ gauge).tolist())).det())
    checks["gauge_det_matches_pass157"] = gauge_det == 2**16 * 3**10 * 5

    full_basis = np.column_stack([ones, gauge, chiral])
    glue_index = abs(int(Matrix(full_basis.tolist()).det()))
    glue_identity = glue_index**2 == 40 * gauge_det * determinant
    checks["glue_identity"] = bool(glue_identity)

    # ------------------------------------------------------------------
    # C. minimal trades
    # ------------------------------------------------------------------
    min_norm, shell, norms_histogram, _ = minimal_shell(chiral)
    shell = [np.asarray(vector, dtype=np.int64) for vector in shell]
    checks["minimal_trades_are_eigenvectors"] = all(
        np.array_equal(adjacency @ vector, -4 * vector) for vector in shell
    )
    checks["minimal_trades_kill_every_line"] = all(
        all(int(vector[list(line)].sum()) == 0 for line in lines) for vector in shell
    )

    support_sizes = Counter(int(np.count_nonzero(vector)) for vector in shell)
    value_profiles = Counter(
        tuple(sorted(Counter(int(v) for v in vector if v).items())) for vector in shell
    )

    # combinatorial identification of one support class
    supports = [frozenset(np.flatnonzero(vector).tolist()) for vector in shell]
    perp_avoiding = Counter()
    for support in set(supports):
        avoided = [
            p
            for p in range(40)
            if not support & ({p} | set(np.flatnonzero(adjacency[p]).tolist()))
        ]
        perp_avoiding[len(avoided)] += 1

    # ------------------------------------------------------------------
    # D. the group, the trade orbit, and the binary-polar identification
    # ------------------------------------------------------------------
    generators, group = build_group(points, symplectic)
    checks["projective_group_order_25920"] = len(group) == 25920

    # orbit structure of the 90 minimal trades under the projective group
    shell_keys = {tuple(int(v) for v in vector): n for n, vector in enumerate(shell)}
    gen_shell_maps = []
    for perm in generators:
        mapping = []
        for vector in shell:
            image = np.empty(40, dtype=np.int64)
            for src in range(40):
                image[perm[src]] = vector[src]
            mapping.append(shell_keys[tuple(int(v) for v in image)])
        gen_shell_maps.append(mapping)
    trade_orbits = orbit_count(len(shell), gen_shell_maps)
    checks["minimal_trades_single_orbit"] = trade_orbits == 1

    # the 45 supports are the octad orbits of the index-45 binary-polar vacuum
    base_support = supports[0]
    support_stabilizer = [
        perm
        for perm in group
        if frozenset(perm[x] for x in base_support) == base_support
    ]
    stab_order = len(support_stabilizer)
    checks["support_stabilizer_order_576"] = stab_order == 576
    checks["support_orbit_size_45"] = (
        25920 % max(stab_order, 1) == 0 and 25920 // max(stab_order, 1) == 45
    )
    point_orbit_sizes = sorted(
        len(orbit) for orbit in _orbits_of_subgroup(support_stabilizer, 40)
    )
    checks["binary_polar_point_orbits_8_32"] = point_orbit_sizes == [8, 32]
    eight_orbit_is_support = any(
        frozenset(orbit) == base_support
        for orbit in _orbits_of_subgroup(support_stabilizer, 40)
        if len(orbit) == 8
    )
    checks["octad_orbit_is_trade_support"] = bool(eight_orbit_is_support)

    # pairwise inner products of the 90 minimal trades
    shell_matrix = np.array(shell, dtype=np.int64)
    trade_inner = shell_matrix @ shell_matrix.T
    trade_profile = Counter(int(v) for v in trade_inner[0])
    trade_profiles_constant = (
        len(
            {tuple(sorted(Counter(int(v) for v in row).items())) for row in trade_inner}
        )
        == 1
    )

    # induced collinearity structure on one support
    support_list = sorted(base_support)
    induced = adjacency[np.ix_(support_list, support_list)]
    induced_degrees = sorted(int(d) for d in induced.sum(axis=1))

    # span-perp anatomy: every trade is +1 on the span and -1 on the perp
    # of a hyperbolic (non-collinear) point pair, and the two four-sets are
    # each other's perps (all points of W(3,3) are regular).
    def common_neighbors(point_set):
        mask = np.ones(40, dtype=bool)
        for point in point_set:
            mask &= adjacency[point].astype(bool)
        return frozenset(np.flatnonzero(mask).tolist())

    span_perp_ok = True
    k44_ok = True
    for vector in shell:
        plus = frozenset(np.flatnonzero(vector == 1).tolist())
        minus = frozenset(np.flatnonzero(vector == -1).tolist())
        if len(plus) != 4 or len(minus) != 4:
            span_perp_ok = False
            break
        plus_l, minus_l = sorted(plus), sorted(minus)
        block = adjacency[np.ix_(plus_l, minus_l)]
        inner_p = adjacency[np.ix_(plus_l, plus_l)]
        inner_m = adjacency[np.ix_(minus_l, minus_l)]
        if not (block.all() and not inner_p.any() and not inner_m.any()):
            k44_ok = False
        if common_neighbors(minus) != plus or common_neighbors(plus) != minus:
            span_perp_ok = False
    checks["trade_supports_are_K44"] = bool(k44_ok)
    checks["trade_sign_classes_are_span_perp_pairs"] = bool(span_perp_ok)

    noncollinear_pairs = sum(
        1 for a, b in combinations(range(40), 2) if not adjacency[a, b]
    )
    checks["ninety_hyperbolic_spans"] = noncollinear_pairs // 6 == 90

    # the 45 supports: 0-inner-product relation as a 45-vertex graph
    unique_supports = sorted(set(supports), key=sorted)
    support_id = {s: n for n, s in enumerate(unique_supports)}
    rep_vector = {}
    for vector in shell:
        key = frozenset(np.flatnonzero(vector).tolist())
        if key not in rep_vector:
            rep_vector[key] = vector
    graph45 = np.zeros((45, 45), dtype=np.int64)
    for a, b in combinations(range(45), 2):
        ip = int(rep_vector[unique_supports[a]] @ rep_vector[unique_supports[b]])
        if ip == 0:
            graph45[a, b] = graph45[b, a] = 1
    deg45 = sorted(int(d) for d in graph45.sum(axis=1))
    g45_sq = graph45 @ graph45
    srg_45_12_3_3 = deg45 == [12] * 45 and all(
        g45_sq[a, b] == (3 if graph45[a, b] else 3)
        for a, b in combinations(range(45), 2)
    )
    checks["support_zero_relation_is_srg_45_12_3_3"] = bool(srg_45_12_3_3)

    # ------------------------------------------------------------------
    # E. the two 480s
    # ------------------------------------------------------------------
    arcs = [(i, j) for i in range(40) for j in range(40) if adjacency[i, j]]
    arc_index = {arc: n for n, arc in enumerate(arcs)}
    checks["arc_count_480"] = len(arcs) == 480

    pencils = {
        p: sorted(
            (line for line in lines if p in line),
            key=lambda line: sorted(line),
        )
        for p in range(40)
    }
    shell_labels = []
    for p in range(40):
        for plus in pencils[p]:
            for minus in pencils[p]:
                if plus != minus:
                    shell_labels.append((p, plus, minus))
    checks["shell_label_count_480"] = len(shell_labels) == 480
    label_index = {label: n for n, label in enumerate(shell_labels)}

    def act_on_arc(perm, arc_id):
        i, j = arcs[arc_id]
        return arc_index[(perm[i], perm[j])]

    def act_on_label(perm, label_id):
        p, plus, minus = shell_labels[label_id]
        return label_index[
            (
                perm[p],
                frozenset(perm[x] for x in plus),
                frozenset(perm[x] for x in minus),
            )
        ]

    # transitivity of both actions (orbit of one point under generators)
    gen_arc_maps = [[act_on_arc(g, a) for a in range(480)] for g in generators]
    gen_label_maps = [[act_on_label(g, s) for s in range(480)] for g in generators]
    checks["arcs_transitive"] = orbit_count(480, gen_arc_maps) == 1
    checks["shell_transitive"] = orbit_count(480, gen_label_maps) == 1

    # stabilizer of one shell vector, and its fixed arcs
    base_label = 0
    stabilizer = [
        perm for perm in group if act_on_label(perm, base_label) == base_label
    ]
    checks["shell_stabilizer_order_54"] = len(stabilizer) == 54

    fixed_arcs = [
        a for a in range(480) if all(act_on_arc(perm, a) == a for perm in stabilizer)
    ]
    g_sets_isomorphic = bool(fixed_arcs)

    # orbital ranks: orbits on X*X, Y*Y, X*Y (Burnside-free direct BFS)
    def product_maps(maps_left, maps_right):
        combined = []
        for g_left, g_right in zip(maps_left, maps_right):
            table = np.empty(480 * 480, dtype=np.int64)
            left = np.asarray(g_left, dtype=np.int64)
            right = np.asarray(g_right, dtype=np.int64)
            for a in range(480):
                table[a * 480 : (a + 1) * 480] = left[a] * 480 + right
            combined.append(table)
        return combined

    rank_arcs = orbit_count(480 * 480, product_maps(gen_arc_maps, gen_arc_maps))
    rank_shell = orbit_count(480 * 480, product_maps(gen_label_maps, gen_label_maps))
    rank_joint = orbit_count(480 * 480, product_maps(gen_arc_maps, gen_label_maps))

    # permutation characters agree iff rank_joint relates symmetrically;
    # the decisive G-set verdict is the fixed-arc criterion above.
    checks["two_480s_verdict_computed"] = True

    verdict = (
        "isomorphic: the shell stabilizer fixes an arc, so the Hashimoto "
        "arc space and the eigenlattice shell are the same G-set"
        if g_sets_isomorphic
        else "NOT isomorphic: the shell stabilizer fixes no arc -- the "
        "Ihara zeta carrier and the E8 shell are two genuinely different "
        "480s, one count, two G-sets"
    )

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass158.chiral_trade_lattice_two_480s.v1",
        "status": "PASS" if all_pass else "FAIL",
        "chiral_lattice": {
            "definition": "L4 = {x in Z^40 : A x = -4 x}",
            "rank": 15,
            "trade_characterization": (
                "L4 equals the saturated kernel of the 40x40 line-point "
                "incidence matrix: integer point-weights with zero sum on "
                "every isotropic line (the trade lattice of the GQ)"
            ),
            "gram_determinant": determinant,
            "gram_smith_invariants": invariants,
            "gram_smith_profile": {
                str(k): int(v) for k, v in sorted(invariant_profile.items())
            },
            "even": is_even,
            "incidence_matrix_smith_profile": {
                str(k): int(v) for k, v in sorted(incidence_profile.items())
            },
            "incidence_matrix_rank": len(incidence_invariants),
        },
        "glue": {
            "identity": "index^2 = det(L12) * det(L2) * det(L4)",
            "det_L12": 40,
            "det_L2": gauge_det,
            "det_L4": determinant,
            "index": glue_index,
            "verified": bool(glue_identity),
        },
        "minimal_trades": {
            "minimal_norm": int(min_norm),
            "shell_size": len(shell),
            "norms_histogram_to_min": {
                str(k): int(v) for k, v in norms_histogram.items()
            },
            "support_sizes": {str(k): int(v) for k, v in sorted(support_sizes.items())},
            "value_profiles": {
                str(dict(profile)): int(count)
                for profile, count in sorted(value_profiles.items())
            },
            "supports_avoiding_a_point_perp": {
                str(k): int(v) for k, v in sorted(perp_avoiding.items())
            },
            "orbit_count_under_PSp43": int(trade_orbits),
            "support_stabilizer_order": int(stab_order),
            "support_stabilizer_point_orbits": point_orbit_sizes,
            "binary_polar_identification": (
                "the 45 trade supports are exactly the canonical 8-point "
                "orbits of the 45 index-45 binary-polar subgroups "
                "(2T x 2T):2 of the five-vacua table"
            ),
            "induced_collinearity_degrees_on_support": induced_degrees,
            "trade_inner_product_profile": {
                str(k): int(v) for k, v in sorted(trade_profile.items())
            },
            "trade_inner_profile_constant": bool(trade_profiles_constant),
            "span_perp_identification": (
                "each minimal trade is +1 on the span and -1 on the perp of "
                "a hyperbolic point pair: 90 = number of hyperbolic lines, "
                "45 supports = unordered {span, perp} double-fours = K44s"
            ),
            "support_zero_relation_degrees": sorted(set(deg45)),
        },
        "two_480s": {
            "arc_action_rank": int(rank_arcs),
            "shell_action_rank": int(rank_shell),
            "joint_action_rank": int(rank_joint),
            "shell_stabilizer_order": len(stabilizer),
            "stabilizer_fixed_arcs": len(fixed_arcs),
            "g_sets_isomorphic": g_sets_isomorphic,
            "verdict": verdict,
        },
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
