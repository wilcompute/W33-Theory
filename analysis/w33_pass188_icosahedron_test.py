#!/usr/bin/env python3
"""Pass 188: are the 36 dodecads icosahedra?

Pass 186 found the pentad shell's valency-5 orbitals decompose into 36
twelve-vertex components with stabilizer order 720.  A 5-regular graph on
12 vertices with this symmetry has one famous candidate: the icosahedron
(spectrum {5, sqrt5 x3, -1 x5, -sqrt5 x3}).  And 36 with stabilizer 720
inside W(E6)-order symmetry is the count of DOUBLE-SIXES of the Schlafli
configuration.  This witness decides both:

1. THE COMBINATORIAL TEST.  Every twelve-vertex component is checked
   directly to be K6,6 minus a perfect matching, hence not an
   icosahedron.  The spectrum follows exactly from that isomorphism.

2. THE SYMMETRY.  The image of the 720-element component stabilizer in
   Sym(12) -- for an icosahedron, at most Aut = A5 x C2 of order 120.

3. THE DOUBLE-SIX GLUING.  The two invariant K6 families are proved to
   be exactly the two sixes in each crown component.  Its stabilizer acts
   as the full S6 on either side, producing the internal double-six
   geometry rather than relying on a count or a floating spectrum.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_group,
    build_w33,
    w33_lines,
)
from analysis.w33_pass160_trade_tower_gq42 import (
    generic_saturated_kernel,
    staged_minimal_shell,
)
from analysis.w33_pass161_gq42_ihara_inheritance import small_generating_set

OUT = ROOT / "data" / "w33_pass188_icosahedron_test.json"


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    incidence = np.zeros((40, 40), dtype=np.int64)
    for row, line in enumerate(lines):
        for p in line:
            incidence[row, p] = 1
    route = generic_saturated_kernel(incidence.T)
    _, shell = staged_minimal_shell(route, bounds=(4, 6, 8, 10))
    shell = [np.asarray(v, dtype=np.int64) for v in shell]
    checks["shell_432"] = len(shell) == 432

    generators, group = build_group(points, symplectic)
    checks["group_order"] = len(group) == 25920
    two_gens = small_generating_set(group)
    line_index = {line: n for n, line in enumerate(lines)}

    def line_perm(perm):
        return [
            line_index[frozenset(perm[x] for x in lines[n])] for n in range(40)
        ]

    shell_keys = {tuple(int(x) for x in v): n for n, v in enumerate(shell)}
    gen_maps = []
    for g in two_gens:
        lp = line_perm(g)
        table = []
        for v in shell:
            image = np.empty(40, dtype=np.int64)
            for src in range(40):
                image[lp[src]] = v[src]
            table.append(shell_keys[tuple(int(x) for x in image)])
        gen_maps.append(table)

    tables = []
    for mapping in gen_maps:
        arr = np.asarray(mapping, dtype=np.int64)
        tables.append((arr[:, None] * 432 + arr[None, :]).reshape(-1))
    labels = np.full(432 * 432, -1, dtype=np.int64)
    orbital_count = 0
    for start in range(432 * 432):
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
    label_grid = labels.reshape(432, 432)
    orbital_matrices = [
        (label_grid == orbital).astype(np.int64)
        for orbital in range(orbital_count)
    ]

    def active_valency(matrix):
        rows = np.flatnonzero(matrix.sum(axis=1) > 0)
        return int(matrix[int(rows[0])].sum()) if len(rows) else 0

    def nontrivial_components(matrix):
        seen = np.zeros(432, dtype=bool)
        components = []
        for start in range(432):
            if seen[start] or int(matrix[start].sum()) == 0:
                seen[start] = True
                continue
            component = {start}
            stack = [start]
            seen[start] = True
            while stack:
                current = stack.pop()
                for nxt in np.flatnonzero(matrix[current]):
                    nxt = int(nxt)
                    if not seen[nxt]:
                        seen[nxt] = True
                        component.add(nxt)
                        stack.append(nxt)
            components.append(frozenset(component))
        return sorted(components, key=lambda component: sorted(component))

    def bipartition(matrix, component):
        colors = {next(iter(component)): 0}
        stack = list(colors)
        while stack:
            current = stack.pop()
            for nxt in np.flatnonzero(matrix[current]):
                nxt = int(nxt)
                if nxt not in component:
                    continue
                wanted = 1 - colors[current]
                if nxt in colors and colors[nxt] != wanted:
                    return None
                if nxt not in colors:
                    colors[nxt] = wanted
                    stack.append(nxt)
        if len(colors) != len(component):
            return None
        return (
            frozenset(vertex for vertex, color in colors.items() if color == 0),
            frozenset(vertex for vertex, color in colors.items() if color == 1),
        )

    directed_five = [
        orbital
        for orbital, matrix in enumerate(orbital_matrices)
        if active_valency(matrix) == 5 and not np.array_equal(matrix, matrix.T)
    ]
    symmetric_five = [
        orbital
        for orbital, matrix in enumerate(orbital_matrices)
        if active_valency(matrix) == 5 and np.array_equal(matrix, matrix.T)
    ]
    checks["valency5_orbitals_split_2_directed_2_symmetric"] = (
        len(directed_five) == 2 and len(symmetric_five) == 2
    )
    crown_matrix = orbital_matrices[directed_five[0]] + orbital_matrices[
        directed_five[1]
    ]
    checks["directed_orbitals_are_transposes"] = np.array_equal(
        orbital_matrices[directed_five[0]].T,
        orbital_matrices[directed_five[1]],
    )
    crown_components = nontrivial_components(crown_matrix)
    crown_parts = {}
    crown_exact = len(crown_components) == 36
    for component in crown_components:
        induced = crown_matrix[np.ix_(sorted(component), sorted(component))]
        parts = bipartition(crown_matrix, component)
        if not (
            len(component) == 12
            and parts is not None
            and tuple(sorted(map(len, parts))) == (6, 6)
            and np.array_equal(induced, induced.T)
            and bool((np.diag(induced) == 0).all())
            and set(int(value) for value in induced.reshape(-1)) <= {0, 1}
            and bool((induced.sum(axis=1) == 5).all())
        ):
            crown_exact = False
        crown_parts[component] = parts
    checks["all_36_components_are_exact_crown_graphs"] = crown_exact

    six_families = []
    six_exact = True
    for orbital in symmetric_five:
        components = nontrivial_components(orbital_matrices[orbital])
        if len(components) != 36 or any(len(component) != 6 for component in components):
            six_exact = False
        for component in components:
            ordered = sorted(component)
            induced = orbital_matrices[orbital][np.ix_(ordered, ordered)]
            if not np.array_equal(
                induced, np.ones((6, 6), dtype=np.int64) - np.eye(6, dtype=np.int64)
            ):
                six_exact = False
        six_families.append(set(components))
    checks["two_exact_36_component_K6_families"] = six_exact

    used_sixes = [set(), set()]
    gluing_exact = True
    for component, parts in crown_parts.items():
        if parts is None:
            gluing_exact = False
            continue
        memberships = [
            (part in six_families[0], part in six_families[1]) for part in parts
        ]
        if sorted(memberships) != [(False, True), (True, False)]:
            gluing_exact = False
            continue
        for part in parts:
            family = 0 if part in six_families[0] else 1
            used_sixes[family].add(part)
    checks["crown_bipartitions_glue_the_two_six_families_bijectively"] = (
        gluing_exact
        and used_sixes[0] == six_families[0]
        and used_sixes[1] == six_families[1]
    )

    # The component stabilizer is faithful on the crown and is the full S6
    # on either intrinsic six.
    comp = sorted(crown_components[0])
    side = sorted(crown_parts[crown_components[0]][0])
    vec_to_pos = {
        tuple(int(x) for x in shell[i]): position for position, i in enumerate(comp)
    }
    side_positions = [comp.index(vertex) for vertex in side]
    side_index = {position: i for i, position in enumerate(side_positions)}
    stabilizer_images = set()
    side_images = set()
    sides_preserved = True
    stab_order = 0
    for perm in group:
        lp = line_perm(perm)
        image_perm = []
        ok = True
        for i in comp:
            img = np.empty(40, dtype=np.int64)
            for src in range(40):
                img[lp[src]] = shell[i][src]
            key = tuple(int(x) for x in img)
            if key not in vec_to_pos:
                ok = False
                break
            image_perm.append(vec_to_pos[key])
        if not ok:
            continue
        stab_order += 1
        image_perm = tuple(image_perm)
        stabilizer_images.add(image_perm)
        if {image_perm[position] for position in side_positions} != set(side_positions):
            sides_preserved = False
        else:
            side_images.add(
                tuple(side_index[image_perm[position]] for position in side_positions)
            )
    checks["component_stabilizer_is_faithful_720"] = (
        stab_order == len(stabilizer_images) == 720
    )
    checks["component_stabilizer_is_full_S6_on_each_six"] = (
        sides_preserved and len(side_images) == 720
    )
    checks["orbit_stabilizer_gives_36_components"] = 25920 // stab_order == 36

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass188.double_six_crown.v2",
        "status": "PASS" if all_pass else "FAIL",
        "orbital_families": {
            "directed_crown_pair": directed_five,
            "symmetric_six_pair": symmetric_five,
            "crown_components": len(crown_components),
            "sixes_per_family": [len(family) for family in six_families],
        },
        "verdict": {
            "is_icosahedron": False,
            "exact_graph": "K6,6 minus a perfect matching (the 6-crown)",
            "exact_characteristic_polynomial": "(x-5)(x+5)(x-1)^5(x+1)^5",
            "reading": (
                "each dodecad is assembled bijectively from one K6 in each "
                "of the two shell orbits; crossing adjacency is exactly the "
                "6-crown.  This is an internal PSp-equivariant double-six "
                "model, not an identification inferred from a spectrum"
            ),
        },
        "symmetry": {
            "component_stabilizer_order": stab_order,
            "image_in_sym12_order": len(stabilizer_images),
            "image_on_one_six_order": len(side_images),
            "group": "S6 on either intrinsic six",
        },
        "double_six_count": {
            "components": len(crown_components),
            "first_sixes": len(six_families[0]),
            "second_sixes": len(six_families[1]),
            "gluing": "one six from each family per crown, bijectively",
        },
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
