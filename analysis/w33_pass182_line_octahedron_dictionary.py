#!/usr/bin/env python3
"""Pass 182: the line-octahedron dictionary after selecting the true orbital.

Pass 169 proved the 40 second-shell octahedra biject with the 40 lines of
W(3,3) via stabilizers -- a group-theoretic identification.  This witness
starts from that group-defined four-valent orbital and then proves that its
line label and axis labels are intrinsic incidence profiles.  It does not
claim that inner products and support intersections recover the orbital:

1. THE PROFILE RULE.  Each triangle consists of 3 GQ(4,2)-trade supports
   = 18 binary-polar octads (8-point sets of W(3,3)).  For each of the
   40 lines, the multiset {|octad cap line|} over the triangle's 18
   octads is computed.  The rule: the matched line is the unique line
   with the distinguished profile -- verified to give a well-defined
   bijection (each triangle selects exactly one line; all 40 lines
   selected).

2. THE AXIS = PAIR-PARTITION THEOREM.  An octahedron has 3 axes; a 4-point
   line has exactly 3 partitions into two pairs.  For the matched pair,
   the interaction profile between each support (axis) and each pair
   partition is computed for all 40 octahedra.  The resulting 120 labels
   are checked equivariantly under both stored generators.

3. THE S3 ALIGNMENT.  Recorded count alignments with the S3 completion
   admission controller (3 completions per ordered path; 12960 = 3*4320)
   -- structural observation with honest scope, no identification claim.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_w33,
    w33_lines,
)
from analysis.w33_pass160_trade_tower_gq42 import (
    generic_saturated_kernel,
    staged_minimal_shell,
)
from analysis.w33_pass161_gq42_ihara_inheritance import support_graph
from analysis.w33_pass168_second_shell_scheme import gq42_lines

OUT = ROOT / "data" / "w33_pass182_line_octahedron_dictionary.json"


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    octads, graph = support_graph(adjacency)  # 45 octads (8-point sets)
    lines45 = gq42_lines(graph)
    incidence45 = np.zeros((27, 45), dtype=np.int64)
    for row, line in enumerate(lines45):
        for p in line:
            incidence45[row, p] = 1
    trade = generic_saturated_kernel(incidence45)
    min_norm, shell = staged_minimal_shell(trade)
    shell = [np.asarray(v, dtype=np.int64) for v in shell]
    checks["shell_240"] = len(shell) == 240 and min_norm == 6

    shell_matrix = np.array(shell, dtype=np.int64)
    gram = shell_matrix @ shell_matrix.T

    # rebuild the 4-valent orbital as in Pass 169 via its intrinsic
    # signature: orthogonal pairs whose supports are disjoint AND which
    # lie in the same octahedron -- recovered here from components of the
    # full orthogonality relation restricted to the 4-valent orbital.
    # The orbital itself needs the group in general, but Pass 169 proved
    # the components are size-6 with spectrum {4,0^3,-2^2}; here we
    # reconstruct them intrinsically below via the profile rule instead.

    # supports of the 240 trades (6-subsets of the 45 octads)
    sup_of = [frozenset(np.flatnonzero(v).tolist()) for v in shell]
    sup120 = sorted(set(sup_of), key=sorted)
    checks["supports_120"] = len(sup120) == 120

    # intrinsic candidate relation on the 120 supports: for supports S, T
    # with representative trades orthogonal and disjoint supports, count
    # pair profiles -- but Pass 169 showed signatures do not separate; so
    # the intrinsic route goes through the LINE profiles directly:

    # for each support (6 octads), and each line (4 points), the meeting
    # profile of the support's octads with the line
    def support_line_profile(support, line):
        return tuple(sorted(len(octads[o] & line) for o in support))

    # the fine profile of a TRIPLE of supports is the sorted 18-tuple
    def triple_line_profile(triple, line):
        values = []
        for s in triple:
            for o in s:
                values.append(len(octads[o] & line))
        return tuple(sorted(values))

    # reconstruct the 40 triangles intrinsically: two supports belong to
    # the same octahedron iff their representative trades are orthogonal
    # with disjoint supports AND the pair extends to a third support
    # orthogonal-disjoint to both; Pass 169's 4-valent relation gave each
    # support exactly two partners.  Candidate partner relation:
    rep = {}
    for n, v in enumerate(shell):
        rep.setdefault(sup_of[n], v)
    partner_candidates = {s: set() for s in sup120}
    for a, b in combinations(range(120), 2):
        sa, sb = sup120[a], sup120[b]
        if sa & sb:
            continue
        if int(rep[sa] @ rep[sb]) == 0:
            partner_candidates[sa].add(sb)
            partner_candidates[sb].add(sa)
    degree_profile = Counter(len(v) for v in partner_candidates.values())

    # the disjoint-orthogonal relation is coarser than the octahedron
    # relation; refine by mutual triples: a triangle is a triple of
    # supports pairwise disjoint-orthogonal whose union meets every
    # W33 point at most twice? -- instead use the exact line-profile
    # split: compute, for one support, the profile against all lines
    sample_profiles = Counter()
    for s in sup120[:6]:
        for line in lines:
            sample_profiles[support_line_profile(s, line)] += 1

    # the dictionary via the coarse relation's triangles: find all
    # 3-cliques in the disjoint-orthogonal relation restricted to pairs
    # that share a common disjoint-orthogonal neighbour... enumerate
    # 3-cliques directly:
    sup_index = {s: n for n, s in enumerate(sup120)}
    adj120 = np.zeros((120, 120), dtype=np.int64)
    for s, partners in partner_candidates.items():
        for t in partners:
            adj120[sup_index[s], sup_index[t]] = 1
    coarse_triangles = 0
    for a in range(120):
        for b in range(a + 1, 120):
            if not adj120[a, b]:
                continue
            for c in range(b + 1, 120):
                if adj120[a, c] and adj120[b, c]:
                    coarse_triangles += 1
    # NEGATIVE CERTIFICATE: every orthogonal pair is support-disjoint, so
    # the coarse invariant relation is 56-regular with a flood of
    # triangles: the octahedron partnering cannot be recovered from
    # inner-product/support data -- Pass 168's blindness, quantified
    checks["coarse_relation_56_regular"] = degree_profile == Counter({56: 120})
    checks["coarse_triangle_flood"] = coarse_triangles == 27040

    # the TRUE triangles need the group: rebuild the 4-valent orbital
    from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
        build_group,
        orbit_count,
    )
    from analysis.w33_pass161_gq42_ihara_inheritance import (
        small_generating_set,
    )

    generators, group = build_group(points, symplectic)
    checks["group_order"] = len(group) == 25920
    two_gens = small_generating_set(group)
    octad_index = {s: n for n, s in enumerate(octads)}
    shell_keys = {tuple(int(x) for x in v): n for n, v in enumerate(shell)}

    def shell_map(perm):
        mapping45 = [
            octad_index[frozenset(perm[x] for x in octads[s])] for s in range(45)
        ]
        table = []
        for v in shell:
            image = np.empty(45, dtype=np.int64)
            for src in range(45):
                image[mapping45[src]] = v[src]
            table.append(shell_keys[tuple(int(x) for x in image)])
        return table

    gen_maps = [shell_map(g) for g in two_gens]
    tables = []
    for mapping in gen_maps:
        arr = np.asarray(mapping, dtype=np.int64)
        tables.append((arr[:, None] * 240 + arr[None, :]).reshape(-1))
    labels = np.full(240 * 240, -1, dtype=np.int64)
    orbital_count = 0
    for start in range(240 * 240):
        if labels[start] >= 0:
            continue
        labels[start] = orbital_count
        stack = [start]
        while stack:
            current = stack.pop()
            for table in tables:
                image = int(table[current])
                if labels[image] < 0:
                    labels[image] = orbital_count
                    stack.append(image)
        orbital_count += 1
    label_grid = labels.reshape(240, 240)
    four_matrix = None
    for o in range(orbital_count):
        matrix = (label_grid == o).astype(np.int64)
        valency = int(matrix[0].sum())
        row_index = int(np.flatnonzero(matrix.sum(axis=1) > 0)[0])
        col = int(np.flatnonzero(matrix[row_index])[0])
        if valency == 4 and int(gram[row_index, col]) == 0:
            four_matrix = matrix
    checks["four_valent_orbital_found"] = four_matrix is not None

    # true triangles on the 120 supports
    adj_true = [set() for _ in range(120)]
    for i in range(240):
        for j in np.flatnonzero(four_matrix[i]):
            a = sup_index[sup_of[i]]
            b = sup_index[sup_of[int(j)]]
            if a != b:
                adj_true[a].add(b)
                adj_true[b].add(a)
    seen = [False] * 120
    triangles = []
    for start in range(120):
        if seen[start]:
            continue
        component = {start}
        stack = [start]
        seen[start] = True
        while stack:
            current = stack.pop()
            for nxt in adj_true[current]:
                if not seen[nxt]:
                    seen[nxt] = True
                    component.add(nxt)
                    stack.append(nxt)
        triangles.append(tuple(sorted(component)))
    checks["forty_true_triangles"] = len(triangles) == 40 and all(
        len(t) == 3 for t in triangles
    )

    # profile rule: for each triangle, find lines with the extremal
    # (most balanced) profile
    matched = {}
    profile_of_match = Counter()
    unique_ok = True
    for tri in triangles:
        triple = [sup120[i] for i in tri]
        best_lines = []
        for ln, line in enumerate(lines):
            profile = triple_line_profile(triple, line)
            profile_of_match[profile] += 0  # touch
            best_lines.append((profile, ln))

        # Exact numerator of 18 times the variance.  Avoid a floating
        # comparison in what is an entirely integral certificate.
        def uniformity(profile):
            return len(profile) * sum(x * x for x in profile) - sum(profile) ** 2

        scored = sorted((uniformity(p), p, ln) for p, ln in best_lines)
        top = [entry for entry in scored if entry[0] == scored[0][0]]
        if len(top) == 1:
            matched[tri] = top[0][2]
            profile_of_match[top[0][1]] += 1
        else:
            unique_ok = False

    checks["profile_rule_unique_per_triangle"] = bool(unique_ok) and len(
        matched
    ) == len(triangles)
    image_lines = set(matched.values())
    checks["dictionary_hits_all_40_lines"] = (
        len(image_lines) == 40 if len(triangles) == 40 else False
    )

    # Axis = pair-partition theorem on every matched pair.  Canonicalize a
    # partition as an unordered pair of unordered point-pairs.
    def canonical_partition(pair1, pair2):
        return tuple(sorted((tuple(sorted(pair1)), tuple(sorted(pair2)))))

    def line_partitions(line):
        line = sorted(line)
        return [
            canonical_partition((line[0], line[1]), (line[2], line[3])),
            canonical_partition((line[0], line[2]), (line[1], line[3])),
            canonical_partition((line[0], line[3]), (line[1], line[2])),
        ]

    axis_tables = {}
    axis_label = {}
    all_tables_permutation = True
    if matched and len(triangles) == 40:
        for tri in triangles:
            partitions = line_partitions(lines[matched[tri]])
            table = []
            for i in tri:
                support = sup120[i]
                row = []
                for p1, p2 in partitions:
                    pair1, pair2 = set(p1), set(p2)
                    count = sum(
                        1
                        for o in support
                        if len(octads[o] & pair1) == 2
                        or len(octads[o] & pair2) == 2
                    )
                    row.append(count)
                table.append(row)
                hits = [j for j, value in enumerate(row) if value == 6]
                if len(hits) == 1 and all(
                    value == (6 if j == hits[0] else 0)
                    for j, value in enumerate(row)
                ):
                    axis_label[i] = partitions[hits[0]]
                else:
                    all_tables_permutation = False
            if sorted(table) != [[0, 0, 6], [0, 6, 0], [6, 0, 0]]:
                all_tables_permutation = False
            axis_tables[tri] = table

    checks["all_40_axis_tables_are_6_times_permutations"] = (
        all_tables_permutation and len(axis_tables) == 40 and len(axis_label) == 120
    )

    # The profile dictionary and every axis label commute with both group
    # generators: 80 triangle cases and 240 axis cases in total.
    line_index = {frozenset(line): i for i, line in enumerate(lines)}
    representative_shell_index = {
        support: next(i for i, value in enumerate(sup_of) if value == support)
        for support in sup120
    }
    support_maps = []
    for shell_mapping in gen_maps:
        support_maps.append(
            [
                sup_index[sup_of[shell_mapping[representative_shell_index[support]]]]
                for support in sup120
            ]
        )

    dictionary_cases = 0
    axis_cases = 0
    dictionary_equivariant = True
    axes_equivariant = True
    for generator, support_map in zip(two_gens, support_maps):
        for tri in triangles:
            image_tri = tuple(sorted(support_map[i] for i in tri))
            expected_line = line_index[
                frozenset(generator[x] for x in lines[matched[tri]])
            ]
            dictionary_cases += 1
            if image_tri not in matched or matched[image_tri] != expected_line:
                dictionary_equivariant = False
        for support in range(120):
            image_support = support_map[support]
            image_partition = canonical_partition(
                (generator[x] for x in axis_label[support][0]),
                (generator[x] for x in axis_label[support][1]),
            )
            axis_cases += 1
            if axis_label[image_support] != image_partition:
                axes_equivariant = False

    checks["profile_dictionary_equivariant_80_cases"] = (
        dictionary_equivariant and dictionary_cases == 80
    )
    checks["axis_partition_equivariant_240_cases"] = (
        axes_equivariant and axis_cases == 240
    )

    axis_partition = axis_tables.get(triangles[0]) if triangles else None

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass182.line_octahedron_dictionary.v2",
        "status": "PASS" if all_pass else "FAIL",
        "blindness_certificate": {
            "disjoint_orthogonal_degree_profile": {
                str(k): int(v) for k, v in sorted(degree_profile.items())
            },
            "coarse_triangle_count": int(coarse_triangles),
            "reading": (
                "every orthogonal trade pair is support-disjoint, so the "
                "coarse invariant relation is 56-regular with 27040 "
                "triangles: the 40 true octahedra are invisible to all "
                "inner-product/support-intersection invariants -- the "
                "quantified form of Pass 168's blindness theorem"
            ),
        },
        "true_triangles": len(triangles),
        "profile_rule": {
            "statement": (
                "for each octahedron-triangle (18 octads), the matched "
                "line is the unique line whose 18 meeting numbers "
                "|octad cap line| are most uniform"
            ),
            "matched_profiles": {
                str(k): int(v) for k, v in profile_of_match.items() if v > 0
            },
            "bijective": bool(checks.get("dictionary_hits_all_40_lines", False)),
        },
        "axis_pair_partition_certificate": {
            "sample": axis_partition,
            "tables_checked": len(axis_tables),
            "axis_labels_checked": len(axis_label),
            "dictionary_generator_cases": dictionary_cases,
            "axis_generator_cases": axis_cases,
            "scope": (
                "the true four-valent orbital is group-selected; once supplied, "
                "the line and pair-partition labels are intrinsic incidence "
                "profiles and equivariant under both stored generators"
            ),
        },
        "s3_alignment": {
            "axes_per_octahedron": 3,
            "completions_per_ordered_path": 3,
            "octahedron_carrier": "40 lines x 3 axes x 2 = 240 trades",
            "controller_carrier": "4320 ordered paths x 3 completions = 12960",
            "honest_scope": (
                "count-level alignment only; no identification of the "
                "4320-path carrier with any octahedron object is claimed"
            ),
        },
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
