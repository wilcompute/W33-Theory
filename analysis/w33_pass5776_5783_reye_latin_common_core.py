#!/usr/bin/env python3
"""Passes 5776--5783: exact q=5 Reye/Latin common-core reconstruction.

This script consumes only the frozen Pass5667--5674 certificate and proves:

* the heavy-support incidence and Reye incidence have the same centered
  12-point Gram operator;
* one quarter of that operator is a rank-9 rational orthogonal projector;
* its kernel gives an intrinsic 3 x 4 imprimitivity system;
* the Reye zero shell is a TD(3,4), explicitly isotopic to the Klein V4
  (XOR) Latin square;
* among all 216 balanced 2+2+2 six-subsets, the line-count spectrum is
  0^12, 2^192, 4^12; the zero class is exactly the frozen heavy shell and
  the four-line class is exactly the 12 intercalate supports;
* the rank-3 permutation modules therefore decompose by dimensions as
  12_P = 1 + 9 + 2_P, 12_H = 1 + 9 + 2_H, 16_L = 1 + 9 + 6_L;
* the carrier outer involution fixes the common 9-dimensional constituent
  and swaps the two 2-dimensional spokes, whereas the point-side sign
  tensor twist is disjoint from all three untwisted carrier modules.

No external package is required.  All arithmetic is integral/rational.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "PART_W33_PASS5667_5674_Q5_REYE_EQUIVARIANT_ORIENTATION.json"
OUTPUT = ROOT / "data" / "PART_W33_PASS5776_5783_REYE_LATIN_COMMON_CORE.json"


def transpose(a: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*a)]


def matmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def eye(n: int) -> list[list[int]]:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def ones(n: int, m: int | None = None) -> list[list[int]]:
    if m is None:
        m = n
    return [[1 for _ in range(m)] for _ in range(n)]


def mat_sub(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def mat_add(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def mat_scale(c: int, a: list[list[int]]) -> list[list[int]]:
    return [[c * x for x in row] for row in a]


def rank_q(a: list[list[int]]) -> int:
    m = [[Fraction(x) for x in row] for row in a]
    nr = len(m)
    nc = len(m[0]) if nr else 0
    r = 0
    for c in range(nc):
        pivot = next((i for i in range(r, nr) if m[i][c] != 0), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        q = m[r][c]
        m[r] = [x / q for x in m[r]]
        for i in range(nr):
            if i != r and m[i][c] != 0:
                q = m[i][c]
                m[i] = [x - q * y for x, y in zip(m[i], m[r])]
        r += 1
        if r == nr:
            break
    return r


def row_sums(a: list[list[int]]) -> list[int]:
    return [sum(row) for row in a]


def col_sums(a: list[list[int]]) -> list[int]:
    return row_sums(transpose(a))


def components_from_adjacency(a: list[list[int]]) -> list[list[int]]:
    n = len(a)
    unseen = set(range(n))
    out: list[list[int]] = []
    while unseen:
        root = min(unseen)
        stack = [root]
        unseen.remove(root)
        comp = []
        while stack:
            u = stack.pop()
            comp.append(u)
            for v, x in enumerate(a[u]):
                if x and v in unseen:
                    unseen.remove(v)
                    stack.append(v)
        out.append(sorted(comp))
    return sorted(out)


def incidence(n_points: int, blocks: Iterable[Iterable[int]]) -> list[list[int]]:
    blocks = [list(b) for b in blocks]
    m = [[0] * len(blocks) for _ in range(n_points)]
    for j, block in enumerate(blocks):
        for i in block:
            m[i][j] = 1
    return m


def intercalates(latin: list[list[int]]) -> list[tuple[int, int, int, int]]:
    out = []
    for r1, r2 in itertools.combinations(range(4), 2):
        for c1, c2 in itertools.combinations(range(4), 2):
            a, b = latin[r1][c1], latin[r1][c2]
            if a != b and a == latin[r2][c2] and b == latin[r2][c1]:
                out.append((r1, r2, c1, c2))
    return out


def first_xor_isotopy(latin: list[list[int]]) -> dict[str, list[int]]:
    target = [[i ^ j for j in range(4)] for i in range(4)]
    for pr in itertools.permutations(range(4)):
        for pc in itertools.permutations(range(4)):
            for ps in itertools.permutations(range(4)):
                if all(ps[latin[pr[i]][pc[j]]] == target[i][j]
                       for i in range(4) for j in range(4)):
                    return {
                        "row_permutation_zero_based": list(pr),
                        "column_permutation_zero_based": list(pc),
                        "symbol_relabel_old_to_new_zero_based": list(ps),
                    }
    raise AssertionError("TD(3,4) table is not isotopic to the Klein XOR square")


def main() -> None:
    src = json.loads(SOURCE.read_text())

    moving_positions = src["pass_5667_action_gate"]["moving_cover_positions_one_based"]
    pos_to_moving = {p: i for i, p in enumerate(moving_positions)}

    heavy_cover = src["pass_5673_5674_heavy_dual"]["heavy_blocks_in_cover_positions"]
    heavy = [sorted(pos_to_moving[p] for p in block) for block in heavy_cover]
    reye_one_based = src["pass_5669_reye_zero_shell"]["zero_triples_on_moving_twelve"]
    reye = [[x - 1 for x in block] for block in reye_one_based]

    h = incidence(12, heavy)
    r = incidence(12, reye)
    hh = matmul(h, transpose(h))
    rr = matmul(r, transpose(r))
    j12 = ones(12)
    k_heavy = mat_sub(hh, mat_scale(3, j12))
    k_reye = mat_sub(rr, j12)
    assert k_heavy == k_reye
    k = k_heavy

    # K = 4 P_9 exactly.
    assert matmul(k, k) == mat_scale(4, k)
    assert rank_q(k) == 9
    assert sum(k[i][i] for i in range(12)) == 36
    assert set(k[i][i] for i in range(12)) == {3}
    assert set(k[i][j] for i in range(12) for j in range(12) if i != j) == {-1, 0}

    # A = 3I-K is exactly 3K4.
    a = mat_sub(mat_scale(3, eye(12)), k)
    assert all(a[i][i] == 0 for i in range(12))
    assert set(x for row in a for x in row) <= {0, 1}
    assert set(row_sums(a)) == {3}
    comps = components_from_adjacency(a)
    assert [len(c) for c in comps] == [4, 4, 4]
    for c in comps:
        assert all(a[i][j] == (0 if i == j else 1) for i in c for j in c)

    # Every Reye line is one-from-each-block, and every cross pair occurs once:
    # hence the zero shell is a TD(3,4), i.e. a Latin square of order four.
    comp_sets = [set(c) for c in comps]
    for line in reye:
        assert [len(set(line) & c) for c in comp_sets] == [1, 1, 1]
    cross_pair_counts = {}
    for x, y in itertools.combinations(range(3), 2):
        counts = {}
        for line in reye:
            s = set(line)
            i = next(iter(s & comp_sets[x]))
            j = next(iter(s & comp_sets[y]))
            counts[(i, j)] = counts.get((i, j), 0) + 1
        cross_pair_counts[f"{x}-{y}"] = sorted(counts.values())
        assert len(counts) == 16 and set(counts.values()) == {1}

    c0, c1, c2 = comps
    i0 = {x: i for i, x in enumerate(c0)}
    i1 = {x: i for i, x in enumerate(c1)}
    i2 = {x: i for i, x in enumerate(c2)}
    latin = [[None] * 4 for _ in range(4)]
    for line in reye:
        s = set(line)
        x = next(iter(s & comp_sets[0]))
        y = next(iter(s & comp_sets[1]))
        z = next(iter(s & comp_sets[2]))
        latin[i0[x]][i1[y]] = i2[z]
    assert all(sorted(row) == [0, 1, 2, 3] for row in latin)
    assert all(sorted(latin[i][j] for i in range(4)) == [0, 1, 2, 3] for j in range(4))
    xor_isotopy = first_xor_isotopy(latin)
    inters = intercalates(latin)
    assert len(inters) == 12

    # Intercalate point supports.
    inter_supports = set()
    for r1, r2, c1_, c2_ in inters:
        syms = {latin[r1][c1_], latin[r1][c2_]}
        support = frozenset([c0[r1], c0[r2], c1[c1_], c1[c2_]] + [c2[s] for s in syms])
        inter_supports.add(support)
    assert len(inter_supports) == 12

    # Enumerate every balanced 2+2+2 six-set and count contained Reye lines.
    balanced = []
    reye_sets = [set(x) for x in reye]
    for q0 in itertools.combinations(c0, 2):
        for q1 in itertools.combinations(c1, 2):
            for q2 in itertools.combinations(c2, 2):
                support = frozenset(q0 + q1 + q2)
                nlines = sum(1 for line in reye_sets if line <= support)
                balanced.append((support, nlines))
    spectrum = {}
    for _, nlines in balanced:
        spectrum[nlines] = spectrum.get(nlines, 0) + 1
    assert spectrum == {0: 12, 2: 192, 4: 12}

    heavy_sets = {frozenset(x) for x in heavy}
    zero_balanced = {s for s, n in balanced if n == 0}
    four_balanced = {s for s, n in balanced if n == 4}
    all_points = set(range(12))
    assert heavy_sets == zero_balanced
    assert four_balanced == inter_supports
    assert {frozenset(all_points - set(s)) for s in heavy_sets} == inter_supports

    # The common projector has an explicit three-block form.
    block_order = [x for comp in comps for x in comp]
    kb = [[k[i][j] for j in block_order] for i in block_order]
    expected_block = []
    for bi in range(3):
        for ii in range(4):
            row = []
            for bj in range(3):
                for jj in range(4):
                    row.append(3 if bi == bj and ii == jj else (-1 if bi == bj else 0))
            expected_block.append(row)
    assert kb == expected_block

    # Rank-3 character facts are producer-certified in Pass5667--5674.
    fw = src["sign_twist_module_firewall"]
    assert fw["point_heavy_character_inner_product"] == 2
    assert fw["point_line_character_inner_product"] == 2
    assert fw["heavy_line_character_inner_product"] == 2
    assert fw["sign_twisted_point_heavy_inner_product"] == 0
    assert fw["sign_twisted_point_line_inner_product"] == 0

    # Derive <eps*pi_P,pi_P> from the exact odd fixed-count distribution.
    group_order = src["pass_5667_action_gate"]["group_order"]
    point_rank = 3
    odd_sq = sum(fixed * fixed * count for fixed, count in fw["odd_element_point_fixed_count_distribution"])
    signed_point_self = Fraction(point_rank * group_order - 2 * odd_sq, group_order)
    assert signed_point_self == 0

    # Full incidence ranks: trivial + common 9.  Centering removes the trivial line.
    assert rank_q(h) == 10
    assert rank_q(r) == 10
    assert row_sums(h) == [6] * 12 and col_sums(h) == [6] * 12
    assert row_sums(r) == [4] * 12 and col_sums(r) == [3] * 16

    comps_one = [[x + 1 for x in c] for c in comps]
    comps_cover = [[moving_positions[x] for x in c] for c in comps]

    # A convenient exact object-level coordinate chart.  Under the first XOR
    # isotopy the first two component orderings stay fixed; the third is relabelled.
    pr = xor_isotopy["row_permutation_zero_based"]
    pc = xor_isotopy["column_permutation_zero_based"]
    ps = xor_isotopy["symbol_relabel_old_to_new_zero_based"]
    row_cover = [moving_positions[c0[i]] for i in pr]
    col_cover = [moving_positions[c1[i]] for i in pc]
    symbol_cover_old = [moving_positions[c2[i]] for i in range(4)]
    symbol_cover_new = [None] * 4
    for old, new in enumerate(ps):
        symbol_cover_new[new] = symbol_cover_old[old]

    results = {
        "schema": "w33.pass5776_5783.reye_latin_common_core.v1",
        "status": "PASS",
        "source_certificate": str(SOURCE.relative_to(ROOT)),
        "pass_5776_dual_incidence_gram": {
            "heavy_shape": [12, 12],
            "reye_shape": [12, 16],
            "heavy_row_col_sums": [6, 6],
            "reye_row_col_sums": [4, 3],
            "identity": "H H^T - 3 J_12 = R R^T - J_12 = K_9",
            "K9_rank": rank_q(k),
            "K9_trace": sum(k[i][i] for i in range(12)),
            "K9_quadratic_identity": "K_9^2 = 4 K_9",
            "common_projector": "P_9 = K_9 / 4",
        },
        "pass_5777_intrinsic_three_by_four": {
            "moving12_components_one_based": comps_one,
            "cover13_positions_components_one_based": comps_cover,
            "adjacency_identity": "A_3K4 = 3 I_12 - K_9",
            "component_sizes": [4, 4, 4],
            "projector_block_form": "P_9 ~ I_3 tensor (I_4 - J_4/4)",
        },
        "pass_5778_reye_td34_klein_latin": {
            "every_line_profile_across_components": [1, 1, 1],
            "cross_pair_multiplicity": 1,
            "latin_table_zero_based_before_isotopy": latin,
            "xor_isotopy": xor_isotopy,
            "normalized_table": [[i ^ j for j in range(4)] for i in range(4)],
            "intercalate_count": len(inters),
            "explicit_cover_coordinate_chart": {
                "row_index_to_cover_position": row_cover,
                "column_index_to_cover_position": col_cover,
                "xor_symbol_index_to_cover_position": symbol_cover_new,
                "law": "symbol = row XOR column",
            },
        },
        "pass_5779_balanced_six_set_census": {
            "balanced_2_2_2_count": len(balanced),
            "contained_reye_line_count_spectrum": [[k_, spectrum[k_]] for k_ in sorted(spectrum)],
            "heavy_is_exact_zero_line_class": True,
            "intercalate_support_is_exact_four_line_class": True,
            "heavy_complements_are_intercalate_supports": True,
        },
        "pass_5780_common_module": {
            "point_module_dimensions": [1, 9, 2],
            "heavy_module_dimensions": [1, 9, 2],
            "line_module_dimensions": [1, 9, 6],
            "centered_heavy_incidence_rank": 9,
            "centered_reye_incidence_rank": 9,
            "common_irrep_dimension": 9,
            "point_kernel_dimensions": [1, 2],
        },
        "pass_5781_outer_vs_sign": {
            "outer_involution_order": src["pass_5673_5674_heavy_dual"]["outer_involution_order"],
            "outer_maps_point_to_heavy_stabilizer_class": src["pass_5673_5674_heavy_dual"]["outer_involution_maps_point_to_heavy_stabilizer_class"],
            "deduction": "the involutive carrier outer automorphism fixes the unique common 9-space and swaps the distinct 2-dimensional point/heavy spokes",
            "sign_twisted_point_self_inner_product": int(signed_point_self),
            "sign_twisted_point_heavy_inner_product": fw["sign_twisted_point_heavy_inner_product"],
            "sign_twisted_point_line_inner_product": fw["sign_twisted_point_line_inner_product"],
            "sign_deduction": "epsilon tensor pi_P is disjoint from all three untwisted P/H/L carrier modules",
        },
        "pass_5782_576_group_disambiguation": {
            "cover_cell_permutation_image": "2^4:(S3 x S3), order 576, centre 1 (Pass5417 producer)",
            "projective_symplectic_hoffman_stabilizer": "2_+^(1+4):(S3 x C3), order 576, centre C2 (Pass5300)",
            "boundary": "These are distinct 576-groups.  The present Reye/Latin theorem concerns the centreless cover-cell permutation image, not the projective symplectic Hoffman stabilizer H.",
        },
        "prior_art_boundary": {
            "reye": "The classical Reye configuration is 12_4 16_3.",
            "tomotope": "Monson--Pellicer--Williams (Ars Math. Contemp. 5 (2012), 355--370, DOI 10.26493/1855-3974.189.e64) identify the tomotope medial layer graph with the Reye Levi graph and give automorphism-group order 576.",
            "new_repo_bridge": "The q=5 multidesign zero shell and heavy shell produce the same exact rank-9 projector, reconstruct a specific Klein-V4 TD(3,4), and identify the heavy shell as the complementary intercalate class.",
        },
        "boundary": "Exact finite incidence/permutation-module theorem.  No continuum, particle, gauge-force, mass/coupling, or physical-unification claim follows.",
    }

    OUTPUT.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print("PASS5776-5783: PASS")
    print("K9 rank=9; Reye TD(3,4)=Klein V4; balanced six-set spectrum 0^12 2^192 4^12")


if __name__ == "__main__":
    main()
