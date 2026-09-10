#!/usr/bin/env python3
"""Close the 270 Heawood/spread bridge under the full PGSp(4,3) action.

The companion PSp certificate proves equivariance for eight symplectic
transvections. The only missing coset is represented by the multiplier-two
similitude already used in w33_pass125_two_we6_embeddings.py:

    D = diag(2,2,1,1),
    omega(Dx,Dy) = 2 omega(x,y)  over F3.

Because projective symplectic similitudes preserve isotropic incidence, D acts
on W(3,3), its 40 lines, 540 skew-line Q3 charts, intrinsic execution slots,
270 C6 components, and 36 spreads. This certificate checks directly that D
preserves the slot graph and commutes with the C6 -> four-intersection spread
pair bijection. Together with the audited PSp generators this proves
PGSp(4,3)-equivariance.

The full group order 51840 and the PSp order 25920 are prior certified repo
results. Since the 270-cycle action is transitive already under PSp, the full
stabilizer has order 51840/270 = 192, agreeing exactly with Pass 1996's
independent D8 x S4 stabilizer computation.
"""

from __future__ import annotations

from collections import deque
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_marcelis_multichart_atlas import w33, chart_web  # noqa: E402
from w33_heawood_spread_pair_270_bridge import (  # noqa: E402
    connected_components,
    enumerate_spreads,
)
from w33_heawood_spread_pair_psp_equivariance import (  # noqa: E402
    GENERATOR_VECTORS,
    component_to_spread_pair,
    induced_chart_perm,
    induced_line_perm,
    induced_spread_perm,
    intrinsic_slot_graph,
    map_slot_node,
    symplectic_form,
    transvection_point_perm,
)

OUT = ROOT / "data" / "w33_heawood_spread_pair_pgsp_equivariance.json"
PSP43_ORDER = 25920
PGSP43_ORDER = 51840
MULTIPLIER_TWO = (
    (2, 0, 0, 0),
    (0, 2, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
)


def canon_f3(v):
    row = tuple(int(x) % 3 for x in v)
    for x in row:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in row)
    raise ValueError("zero vector")


def apply_matrix(v, matrix):
    return tuple(
        sum(matrix[r][c] * v[c] for c in range(4)) % 3
        for r in range(4)
    )


def matrix_point_perm(points, matrix):
    index = {p: i for i, p in enumerate(points)}
    out = [index[canon_f3(apply_matrix(p, matrix))] for p in points]
    assert sorted(out) == list(range(len(points)))
    return tuple(out)


def component_perm_for_point_perm(
    point_perm, lines, charts, slot_adj, components, component_index
):
    lperm = induced_line_perm(lines, point_perm)
    cperm = induced_chart_perm(charts, lperm)
    mapped_nodes = {node: map_slot_node(node, cperm) for node in slot_adj}
    assert set(mapped_nodes.values()) == set(slot_adj)
    comp_perm = []
    for comp in components:
        image = frozenset(mapped_nodes[node] for node in comp)
        assert image in component_index
        comp_perm.append(component_index[image])
    comp_perm = tuple(comp_perm)
    assert sorted(comp_perm) == list(range(len(components)))
    return lperm, cperm, mapped_nodes, comp_perm


def orbit(seed, generators):
    seen = {seed}
    q = deque([seed])
    while q:
        x = q.popleft()
        for g in generators:
            y = g[x]
            if y not in seen:
                seen.add(y)
                q.append(y)
    return seen


def build_result():
    points, lines = w33()
    charts, web, _ = chart_web(lines)
    spreads = enumerate_spreads(lines)
    slot_adj, _ = intrinsic_slot_graph(charts, web, lines)
    components = connected_components(slot_adj)
    assert len(components) == 270 and {len(C) for C in components} == {6}
    component_index = {frozenset(C): i for i, C in enumerate(components)}
    cycle_to_pair, _by_symdiff, spread_hist = component_to_spread_pair(
        components, charts, spreads
    )

    # Reconstruct the PSp component generators only to certify transitivity in
    # the exact same representation used for the outer audit.
    inner_component_perms = []
    for v in GENERATOR_VECTORS:
        pperm = transvection_point_perm(points, v)
        _lp, _cp, _nodes, comp_perm = component_perm_for_point_perm(
            pperm, lines, charts, slot_adj, components, component_index
        )
        inner_component_perms.append(comp_perm)

    # Verify the similitude identity on the actual F3 vectors BEFORE
    # projective canonicalization. Canonicalizing Dx and Dy independently can
    # multiply the symplectic form by unrelated projective scalars and is not a
    # valid test of a matrix-level similitude identity.
    multiplier_checks = [
        symplectic_form(
            apply_matrix(x, MULTIPLIER_TWO),
            apply_matrix(y, MULTIPLIER_TWO),
        )
        == (2 * symplectic_form(x, y)) % 3
        for x in points
        for y in points
    ]

    Dperm = matrix_point_perm(points, MULTIPLIER_TWO)
    lperm, cperm, mapped_nodes, outer_comp_perm = component_perm_for_point_perm(
        Dperm, lines, charts, slot_adj, components, component_index
    )
    sperm = induced_spread_perm(spreads, lperm)

    chart_web_ok = all(
        {cperm[x] for x in web[ci]} == set(web[cperm[ci]])
        for ci in range(len(charts))
    )
    slot_graph_ok = all(
        mapped_nodes[v] in slot_adj[mapped_nodes[u]]
        for u, nbrs in slot_adj.items()
        for v in nbrs
    )

    outer_equivariant = True
    for cid in range(len(components)):
        cid2 = outer_comp_perm[cid]
        si, sj = cycle_to_pair[cid]
        expected = tuple(sorted((sperm[si], sperm[sj])))
        if cycle_to_pair[cid2] != expected:
            outer_equivariant = False
            break

    psp_orbit = orbit(0, inner_component_perms)
    pgsp_orbit = orbit(0, inner_component_perms + [outer_comp_perm])
    outer_fixed = sum(i == j for i, j in enumerate(outer_comp_perm))
    outer_order_two_on_points = all(Dperm[Dperm[i]] == i for i in range(40))
    outer_order_two_on_cycles = all(
        outer_comp_perm[outer_comp_perm[i]] == i for i in range(270)
    )

    full_stabilizer = PGSP43_ORDER // len(pgsp_orbit)
    psp_stabilizer = PSP43_ORDER // len(psp_orbit)

    checks = {
        "multiplier_two_identity_holds_on_all_F3_point_representative_pairs": all(multiplier_checks),
        "outer_matrix_is_projective_involution_on_points": outer_order_two_on_points,
        "outer_preserves_chart_web": chart_web_ok,
        "outer_preserves_intrinsic_slot_graph": slot_graph_ok,
        "outer_permutes_all_270_C6_components": sorted(outer_comp_perm) == list(range(270)),
        "outer_is_involution_on_C6_set": outer_order_two_on_cycles,
        "outer_commutes_with_C6_spread_pair_bijection": outer_equivariant,
        "PSp_generators_are_transitive_on_270_C6": len(psp_orbit) == 270,
        "PGSp_generators_are_transitive_on_270_C6": len(pgsp_orbit) == 270,
        "PSp_stabilizer_is_96": psp_stabilizer == 96,
        "full_PGSp_stabilizer_is_192": full_stabilizer == 192,
        "full_stabilizer_doubles_PSp_stabilizer": full_stabilizer == 2 * psp_stabilizer,
        "spread_pair_census_remains_270_at_intersection4": spread_hist[4] == 270,
    }

    return {
        "schema": "w33.heawood-spread-pair-pgsp-equivariance.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The 270 C6 execution cycles -> 270 four-intersection spread-pair "
            "bijection is equivariant under the full PGSp(4,3) action. The "
            "single multiplier-two outer similitude preserves the intrinsic "
            "slot graph and commutes with the bijection, closing the only coset "
            "left open by the PSp certificate."
        ),
        "outer_generator": {
            "matrix_mod3": [list(row) for row in MULTIPLIER_TWO],
            "similitude_multiplier": 2,
            "projective_order": 2,
            "fixed_C6_components": outer_fixed,
            "moves_C6_components": 270 - outer_fixed,
            "commutes_with_bijection": outer_equivariant,
        },
        "orbit_stabilizer": {
            "PSp_order_prior_certified": PSP43_ORDER,
            "PSp_C6_orbit": len(psp_orbit),
            "PSp_C6_stabilizer": psp_stabilizer,
            "PGSp_order_prior_certified": PGSP43_ORDER,
            "PGSp_C6_orbit": len(pgsp_orbit),
            "PGSp_C6_stabilizer": full_stabilizer,
            "prior_Pass1996_full_stabilizer_structure": "D8 x S4",
        },
        "equivariance_generators": {
            "inner": "eight explicit symplectic transvections",
            "outer": "diag(2,2,1,1), multiplier 2",
            "conclusion": (
                "These generate the certified full PGSp(4,3) point action; "
                "the C6-spread dictionary commutes with every generator."
            ),
        },
        "claim_boundary": [
            "The group orders 25920 and 51840 are imported from prior exact repo certificates.",
            "The D8 x S4 structure of the 192-element full stabilizer is the independent Pass 1996 result; this script matches its orbit-stabilizer order and proves the explicit G-set map is full-G equivariant.",
            "The 96-element PSp stabilizer is not the tomotope automorphism group; the companion stabilizer fingerprint supplies the derived-subgroup obstruction.",
        ],
        "checks": checks,
    }


def main():
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "outer_fixed_C6": result["outer_generator"]["fixed_C6_components"],
        "outer_equivariant": result["outer_generator"]["commutes_with_bijection"],
        "PSp_stabilizer": result["orbit_stabilizer"]["PSp_C6_stabilizer"],
        "PGSp_stabilizer": result["orbit_stabilizer"]["PGSp_C6_stabilizer"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
