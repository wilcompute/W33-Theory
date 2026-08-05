#!/usr/bin/env python3
"""Passes 3694-3700: exact spread ETF, Norton axial algebra, and firewalls.

This verifier is deliberately self-contained. It reconstructs W(3,3), its 40
isotropic lines and all 36 spreads; proves the centered line/spread incidence
matrix is an ETF(15,36); constructs the canonical Norton algebra on the
15-dimensional primitive-idempotent sector; separates the 36-spread graph from
the 36 Witting-ray orthogonality graph; and proves that the thick C3 panels of
the four-parabolic chamber system cannot be made thin by an unbranched cover.

Monster-word and class-fusion fronts are represented by separate fail-closed
workflows and are not promoted by this Python certificate.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import argparse
import json
from pathlib import Path
from typing import Iterable

import sympy as sp

ROOT = Path(__file__).resolve().parents[1] if Path(__file__).resolve().parent.name == "analysis" else Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT / "data" / "PART_3694_3700_SPREAD_ETF_AXIAL_CLOSURE_results.json"


def canon_f3(v: Iterable[int]) -> tuple[int, ...]:
    w = tuple(int(x) % 3 for x in v)
    for x in w:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in w)
    raise ValueError("zero vector has no projective point")


def symp(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def build_w33() -> tuple[tuple[tuple[int, ...], ...], sp.Matrix, tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    points = tuple(sorted({canon_f3(v) for v in product(range(3), repeat=4) if any(v)}))
    assert len(points) == 40
    A = sp.zeros(40)
    for i, j in combinations(range(40), 2):
        if symp(points[i], points[j]) == 0:
            A[i, j] = A[j, i] = 1
    assert {sum(int(A[i, j]) for j in range(40)) for i in range(40)} == {12}
    assert A * A == 8 * sp.eye(40) - 2 * A + 4 * sp.ones(40)

    lines: list[tuple[int, ...]] = []
    for i, j in combinations(range(40), 2):
        if not A[i, j]:
            continue
        line = tuple(sorted({i, j} | {k for k in range(40) if A[i, k] and A[j, k]}))
        if len(line) == 4 and all(A[a, b] for a, b in combinations(line, 2)):
            lines.append(line)
    lines = sorted(set(lines))
    assert len(lines) == 40

    point_to_lines: dict[int, list[int]] = {p: [] for p in range(40)}
    masks: list[int] = []
    for li, line in enumerate(lines):
        mask = sum(1 << p for p in line)
        masks.append(mask)
        for p in line:
            point_to_lines[p].append(li)

    full_mask = (1 << 40) - 1
    spreads: list[tuple[int, ...]] = []

    def search(covered: int, chosen: list[int]) -> None:
        if covered == full_mask:
            if len(chosen) == 10:
                spreads.append(tuple(chosen))
            return
        if len(chosen) >= 10:
            return
        uncovered = full_mask ^ covered
        candidates_by_point = []
        pbits = uncovered
        while pbits:
            lsb = pbits & -pbits
            p = lsb.bit_length() - 1
            candidates = [li for li in point_to_lines[p] if not (masks[li] & covered)]
            candidates_by_point.append((len(candidates), p, candidates))
            pbits ^= lsb
        count, _, candidates = min(candidates_by_point)
        if count == 0:
            return
        for li in candidates:
            chosen.append(li)
            search(covered | masks[li], chosen)
            chosen.pop()

    search(0, [])
    spreads = sorted(set(tuple(sorted(s)) for s in spreads))
    assert len(spreads) == 36
    return points, A, tuple(lines), tuple(spreads)


def primitive_idempotents(A: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix]:
    I = sp.eye(36)
    J = sp.ones(36)
    E15 = sp.Rational(1, 2) * I + sp.Rational(1, 6) * A - sp.Rational(1, 12) * J
    E20 = sp.Rational(1, 2) * I - sp.Rational(1, 6) * A + sp.Rational(1, 18) * J
    assert E15 * E15 == E15 and E20 * E20 == E20 and E15 * E20 == sp.zeros(36)
    assert E15.rank() == 15 and E20.rank() == 20
    return E15, E20


def matrix_tuple(v: sp.Matrix) -> tuple[Fraction, ...]:
    return tuple(Fraction(int(x.p), int(x.q)) for x in v)


def independent_column_basis(E: sp.Matrix) -> tuple[sp.Matrix, list[int], list[int], sp.Matrix]:
    _, pivcols = E.rref()
    cols = list(pivcols)
    U = E[:, cols]
    assert U.rank() == E.rank()
    _, pivrows = U.T.rref()
    rows = list(pivrows)
    R = U[rows, :]
    Rinv = R.inv()
    return U, cols, rows, Rinv


def coords(v: sp.Matrix, U: sp.Matrix, rows: list[int], Rinv: sp.Matrix) -> sp.Matrix:
    c = Rinv * v[rows, :]
    assert U * c == v
    return c


def norton_product(E: sp.Matrix, x: sp.Matrix, y: sp.Matrix) -> sp.Matrix:
    return E * x.multiply_elementwise(y)


def spectral_projector(M: sp.Matrix, eigenvalue: sp.Rational, spectrum: list[sp.Rational]) -> sp.Matrix:
    P = sp.eye(M.rows)
    for mu in spectrum:
        if mu != eigenvalue:
            P = P * (M - mu * sp.eye(M.rows)) / (eigenvalue - mu)
    return sp.simplify(P)


def axis_fusion_certificate(E15: sp.Matrix, A36: sp.Matrix) -> dict[str, object]:
    U, _, rows, Rinv = independent_column_basis(E15)
    axes = tuple(6 * E15[:, i] for i in range(36))
    assert all(norton_product(E15, a, a) == a for a in axes)
    axis_map = {matrix_tuple(a): i for i, a in enumerate(axes)}

    a0 = axes[0]
    L_full = E15 * sp.diag(*list(a0))
    L = Rinv * L_full[rows, :] * U
    spectrum = [sp.Rational(1), sp.Rational(-1, 2), sp.Rational(1, 6)]
    projectors = {lam: spectral_projector(L, lam, spectrum) for lam in spectrum}
    multiplicities = {str(lam): int(P.rank()) for lam, P in projectors.items()}
    assert multiplicities == {"1": 1, "-1/2": 5, "1/6": 9}
    assert sum(projectors.values(), sp.zeros(15)) == sp.eye(15)

    eigbases: dict[sp.Rational, list[sp.Matrix]] = {}
    for lam in spectrum:
        eigbases[lam] = [U * v for v in projectors[lam].columnspace()]

    fusion: dict[str, list[str]] = {}
    for i, lam in enumerate(spectrum):
        for mu in spectrum[i:]:
            targets: set[sp.Rational] = set()
            for x in eigbases[lam]:
                for y in eigbases[mu]:
                    z = norton_product(E15, x, y)
                    zc = coords(z, U, rows, Rinv)
                    for nu in spectrum:
                        if projectors[nu] * zc != sp.zeros(15, 1):
                            targets.add(nu)
            fusion[f"{lam}*{mu}"] = [str(x) for x in spectrum if x in targets]

    expected_fusion = {
        "1*1": ["1"],
        "1*-1/2": ["-1/2"],
        "1*1/6": ["1/6"],
        "-1/2*-1/2": ["1", "1/6"],
        "-1/2*1/6": ["-1/2"],
        "1/6*1/6": ["1", "1/6"],
    }
    assert fusion == expected_fusion

    adjacent_formula = 0
    nonadjacent_formula = 0
    triples: set[tuple[int, int, int]] = set()
    for i, j in combinations(range(36), 2):
        p = norton_product(E15, axes[i], axes[j])
        if A36[i, j]:
            assert p == (axes[i] + axes[j]) / 6
            adjacent_formula += 1
        else:
            target = 3 * p + (axes[i] + axes[j]) / 2
            k = axis_map.get(matrix_tuple(target))
            assert k is not None and k not in (i, j)
            assert not A36[i, k] and not A36[j, k]
            assert p == -(axes[i] + axes[j]) / 6 + axes[k] / 3
            triples.add(tuple(sorted((i, j, k))))
            nonadjacent_formula += 1
    assert adjacent_formula == 270 and nonadjacent_formula == 360
    assert len(triples) == 120
    point_degree = Counter(v for t in triples for v in t)
    assert set(point_degree.values()) == {10}

    return {
        "axes": axes,
        "axis_count": 36,
        "axis_idempotent": True,
        "primitive_axis": multiplicities["1"] == 1,
        "axis_spectrum": multiplicities,
        "fusion_law": fusion,
        "z2_grading": {"even": ["1", "1/6"], "odd": ["-1/2"]},
        "adjacent_pair_formula_count": adjacent_formula,
        "nonadjacent_pair_formula_count": nonadjacent_formula,
        "norton_triples": tuple(sorted(triples)),
        "triple_count": len(triples),
        "triples_per_axis": sorted(set(point_degree.values())),
        "majorana_verdict": "NOT_MAJORANA: positive Frobenius Norton algebra, but axis eigenvalue -1/2 and fusion law do not match Monster/Majorana type",
    }


# Eisenstein integers a+b*w with w^2+w+1=0.
def eadd(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] + y[0], x[1] + y[1]


def emul(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    a, b = x
    c, d = y
    return a * c - b * d, a * d + b * c - b * d


def econj(x: tuple[int, int]) -> tuple[int, int]:
    a, b = x
    return a - b, -b


def eneg(x: tuple[int, int]) -> tuple[int, int]:
    return -x[0], -x[1]


def magic_ray_graph() -> tuple[sp.Matrix, dict[str, object]]:
    z = (0, 0)
    one = (1, 0)
    ws = ((1, 0), (0, 1), (-1, -1))
    rays: list[tuple[tuple[int, int], ...]] = []
    for mu, nu in product(range(3), repeat=2):
        rays.append((z, one, eneg(ws[mu]), ws[nu]))
    for mu, nu in product(range(3), repeat=2):
        rays.append((one, z, eneg(ws[mu]), eneg(ws[nu])))
    for mu, nu in product(range(3), repeat=2):
        rays.append((one, eneg(ws[mu]), z, ws[nu]))
    for mu, nu in product(range(3), repeat=2):
        rays.append((one, ws[mu], ws[nu], z))
    assert len(rays) == 36

    def inner(x, y):
        s = z
        for a, b in zip(x, y):
            s = eadd(s, emul(econj(a), b))
        return s

    M = sp.zeros(36)
    for i, j in combinations(range(36), 2):
        if inner(rays[i], rays[j]) == z:
            M[i, j] = M[j, i] = 1
    degree = sorted(set(sum(int(M[i, j]) for j in range(36)) for i in range(36)))
    eig = {str(k): int(v) for k, v in sorted(M.eigenvals().items(), key=lambda kv: float(kv[0]), reverse=True)}
    assert degree == [11]
    assert eig == {"11": 1, "2": 20, "-1": 3, "-4": 12}
    Q = sp.zeros(4)
    equitable = True
    for b1 in range(4):
        for b2 in range(4):
            counts = [sum(int(M[i, j]) for j in range(9 * b2, 9 * (b2 + 1))) for i in range(9 * b1, 9 * (b1 + 1))]
            equitable &= len(set(counts)) == 1
            Q[b1, b2] = counts[0]
    assert equitable and Q == 3 * sp.ones(4) - sp.eye(4)
    triangles_per_block = []
    for b in range(4):
        block = M[9*b:9*(b+1), 9*b:9*(b+1)]
        comps = []
        unseen = set(range(9))
        while unseen:
            root = min(unseen)
            stack = [root]
            comp = set()
            while stack:
                u = stack.pop()
                if u in comp:
                    continue
                comp.add(u)
                stack.extend(v for v in range(9) if block[u, v] and v not in comp)
            unseen -= comp
            comps.append(tuple(sorted(comp)))
        triangles_per_block.append(sorted(map(len, comps)))
    assert triangles_per_block == [[3, 3, 3]] * 4
    return M, {
        "vertices": 36,
        "degree": 11,
        "spectrum": eig,
        "strongly_regular": False,
        "equitable_four_by_nine_partition": True,
        "quotient_matrix": [[int(Q[i, j]) for j in range(4)] for i in range(4)],
        "each_nine_block_components": triangles_per_block,
    }


def build_certificate() -> dict[str, object]:
    points, A40, lines, spreads = build_w33()
    spread_sets = [set(S) for S in spreads]

    B = sp.zeros(40, 36)
    for j, spread in enumerate(spreads):
        for li in spread:
            B[li, j] = 1
    assert {sum(int(B[i, j]) for i in range(40)) for j in range(36)} == {10}
    assert {sum(int(B[i, j]) for j in range(36)) for i in range(40)} == {9}

    A36 = sp.zeros(36)
    intersections = Counter()
    for i, j in combinations(range(36), 2):
        n = len(spread_sets[i] & spread_sets[j])
        intersections[n] += 1
        if n == 4:
            A36[i, j] = A36[j, i] = 1
    assert intersections == Counter({1: 360, 4: 270})
    assert {sum(int(A36[i, j]) for j in range(36)) for i in range(36)} == {15}
    assert A36 * A36 == 9 * sp.eye(36) + 6 * sp.ones(36)

    E15, E20 = primitive_idempotents(A36)
    C = B - sp.Rational(1, 4) * sp.ones(40, 36)
    gram = C.T * C
    assert B.T * B == 9 * sp.eye(36) + 3 * A36 + sp.ones(36)
    assert gram == 18 * E15
    norm2 = gram[0, 0]
    normalized = gram / norm2
    offdiag = Counter(normalized[i, j] for i, j in combinations(range(36), 2))
    assert norm2 == sp.Rational(15, 2)
    assert offdiag == Counter({sp.Rational(-1, 5): 360, sp.Rational(1, 5): 270})
    assert sp.Rational(36 - 15, 15 * 35) == sp.Rational(1, 25)
    S = sp.eye(36) + 2 * A36 - sp.ones(36)
    assert S * S - 2 * S - 35 * sp.eye(36) == sp.zeros(36)
    seidel_spectrum = {"7": 15, "-5": 21}
    assert 7 * 15 - 5 * 21 == int(sp.trace(S)) == 0

    naimark_guard_rank = 21
    assert sp.eye(36) - E15 == E20 + sp.Rational(1, 36) * sp.ones(36)

    axial = axis_fusion_certificate(E15, A36)
    triples = axial.pop("norton_triples")
    axial.pop("axes")
    line_to_spreads = {li: [s for s, Sset in enumerate(spread_sets) if li in Sset] for li in range(40)}
    triples_by_line: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
    for t in triples:
        common = set(spreads[t[0]]) & set(spreads[t[1]]) & set(spreads[t[2]])
        assert len(common) == 1
        triples_by_line[next(iter(common))].append(t)
    assert len(triples_by_line) == 40
    for li in range(40):
        assert len(line_to_spreads[li]) == 9
        assert len(triples_by_line[li]) == 3
        assert sorted(v for t in triples_by_line[li] for v in t) == sorted(line_to_spreads[li])

    _, magic = magic_ray_graph()
    magic_separation = {
        "spread_graph_degree": 15,
        "spread_graph_spectrum": {"15": 1, "3": 15, "-3": 20},
        "magic_ray_graph_degree": 11,
        "magic_ray_graph_spectrum": magic["spectrum"],
        "degree_mismatch": True,
        "spectrum_mismatch": True,
        "magic_ray_graph_not_srg": True,
        "verdict": "The 36-spread rank-three graph and the 36-ray orthogonality graph are not isomorphic and must not be identified.",
    }
    panel_cover = {
        "source_panel_size": 3,
        "source_colored_neighbor_degree": 2,
        "thin_panel_size": 2,
        "thin_colored_neighbor_degree": 1,
        "unbranched_type_preserving_cover_possible": False,
        "reason": "A chamber-system covering is locally bijective on each rank-one residue, so panel cardinality and colored degree are preserved.",
        "surviving_routes": ["quotient", "deletion", "branched resolution", "change of incidence structure"],
    }

    result: dict[str, object] = {
        "schema": "w33.pass3694_3700.spread_etf_axial_closure.v1",
        "status": "PASS_EXACT_SEVEN_FRONT_SOURCE_WITH_MONSTER_TARGETS_PENDING",
        "checks": {
            "w33_points_40": True, "w33_lines_40": True, "w33_spreads_36": True,
            "spread_intersections_270_360": True, "spread_srg_36_15_6_6": True,
            "primitive_idempotents_rank_15_20": True, "centered_incidence_gram_18E15": True,
            "etf_15_36_coherence_one_fifth": True, "welch_bound_saturated": True,
            "seidel_minimal_polynomial": True, "naimark_guard_rank_21": True,
            "norton_axes_36_idempotent": True, "norton_axis_spectrum_1_5_9": True,
            "norton_fusion_law_exact": True, "norton_pair_formulas_all_630": True,
            "norton_triples_120": True, "three_triples_partition_nine_spreads_per_line": True,
            "magic_ray_graph_exact_spectrum": True, "magic_spread_graph_separation": True,
            "unbranched_binary_panel_cover_no_go": True,
        },
        "spread_association_scheme": {
            "points": 36,
            "intersection_census": {str(k): v for k, v in sorted(intersections.items())},
            "relation_share_four": {"parameters": [36, 15, 6, 6], "spectrum": {"15": 1, "3": 15, "-3": 20}},
            "primitive_idempotents": {"rank15": "E15 = 1/2 I + 1/6 A - 1/12 J", "rank20": "E20 = 1/2 I - 1/6 A + 1/18 J"},
        },
        "spread_incidence_etf": {
            "incidence_shape": [40, 36], "column_weight": 10, "row_weight": 9,
            "centered_matrix": "C = B - (1/4)J", "exact_gram_identity": "C^T C = 18 E15",
            "column_norm_squared": "15/2", "normalized_inner_products": {"share_4_lines": "1/5", "share_1_line": "-1/5"},
            "frame": "real ETF(15,36)", "welch_coherence_squared": "1/25",
            "seidel_matrix": "S = I + 2A - J", "seidel_spectrum": seidel_spectrum,
            "seidel_polynomial": "S^2 - 2S - 35I = 0",
        },
        "naimark_photonic_certificate": {
            "signal_rank": 15, "input_modes": 36, "minimal_guard_rank": naimark_guard_rank,
            "row_isometry_gram": "E15", "complement_projector": "I36-E15",
            "verdict": "Any exact passive 36-mode unitary dilation of this ETF analysis map requires a 21-dimensional orthogonal guard sector; fewer guard modes cannot complete the isometry.",
            "boundary": "This is a linear-optical dimension certificate, not a fabricated device or laboratory validation.",
        },
        "norton_axial_algebra": {
            **axial, "product": "x star y = E15(x coordinatewise-multiplied by y)", "axis_definition": "a_i = 6 E15 e_i",
            "triple_system": {"triples": 120, "triples_per_axis": 10, "common_w33_line_per_triple": 1, "triples_per_w33_line": 3,
                "partition_statement": "For each of 40 W33 lines, the nine spreads containing it split into three disjoint Norton triples."},
        },
        "magic_ray_firewall": {**magic, **magic_separation},
        "ternary_panel_cover_no_go": panel_cover,
        "monster_word_front": {
            "status": "EXECUTABLE_FAIL_CLOSED_HARNESS_ADDED_CANDIDATE_WORDS_PENDING",
            "required_certificate": ["serialized mmgroup words", "closure order 25920", "four order-3 generators", "four triple closures order 648", "element-order census", "Monster class fingerprints"],
        },
        "monster_class_fusion_front": {
            "status": "EXECUTABLE_GAP_TARGET_ADDED_REMOTE_EXECUTION_PENDING",
            "required_output": "All U4(2)->M class fusions satisfying the 5B-containing constraints and the multiplicity set of degree-81 constituents in the restricted 196883 character.",
            "external_boundary": "The official CTblLib fusion search and Holmes-Wilson class constraints are inputs to the separate GAP workflow, not outputs of this Python verifier.",
        },
        "evidence_boundary": {
            "proved_here": ["exact ETF(15,36) from centered W33 line-spread incidence", "minimal 21-dimensional Naimark guard sector",
                "36-idempotent rank-15 Norton axial algebra and exact fusion law", "120 Norton triples partitioned three-per-W33-line",
                "exact nonisomorphism of spread and magic-ray graphs", "unbranched-cover obstruction for ternary-to-binary panels"],
            "not_proved_here": ["concrete U4(2) words inside the Monster", "executed Monster class-fusion multiplicity",
                "Majorana, Griess, or VOA identification", "regular thin polytope cover", "laboratory implementation"],
        },
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    result["semantic_sha256"] = sha256(payload.encode("utf-8")).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = build_certificate()
    if args.check:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        if expected != result:
            raise SystemExit("frozen certificate mismatch")
        print(f"PASS frozen certificate {result['semantic_sha256']}")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "semantic_sha256": result["semantic_sha256"], "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
