#!/usr/bin/env python3
"""BT769 — Center-quad / intrinsic octet identification theorem.

This executes the first BT768 next step.  The old center-quad quotient layer
was built from 90 K4 components: each component has an outer 4-set of pairwise
noncollinear W33 points and a center 4-set of common collinear neighbors.  The
outer<->center map is a fixed-point-free involution, hence 90/2 = 45 quotient
objects.

BT766 found 45 intrinsic K_{4,4} octets from the antipodal local-K_{3,3}
chart quotient.  This verifier proves the two 45-sets are the same: each BT766
octet is exactly outer union center for one involution pair of old K4 components.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx

from bt766_intrinsic_k44_octet_quotient import build_w33

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT769_CENTER_QUAD_OCTET_IDENTIFICATION_results.json"


def compute_bt766_octets(G, lines, idx, point_lines):
    nonedges = []
    nonedge_to_id = {}
    for a, b in itertools.combinations(range(40), 2):
        if not G.has_edge(a, b):
            nonedge_to_id[(a, b)] = len(nonedges)
            nonedges.append((a, b))

    charts = []
    chart_sets = []
    for p in range(40):
        for l1, l2 in itertools.combinations(point_lines[p], 2):
            A = sorted(idx[x] for x in lines[l1] if idx[x] != p)
            B = sorted(idx[x] for x in lines[l2] if idx[x] != p)
            nes = [nonedge_to_id[tuple(sorted((a, b)))] for a in A for b in B]
            charts.append((p, l1, l2))
            chart_sets.append(set(nes))

    chart_graph = nx.Graph()
    chart_graph.add_nodes_from(range(len(charts)))
    for i, j in itertools.combinations(range(len(charts)), 2):
        if len(chart_sets[i] & chart_sets[j]) == 1:
            chart_graph.add_edge(i, j)

    dist = dict(nx.all_pairs_shortest_path_length(chart_graph))
    antipode = {}
    for i, d in dist.items():
        far = [j for j, dd in d.items() if dd == 4]
        assert len(far) == 1
        antipode[i] = far[0]

    pairs = sorted({tuple(sorted((i, antipode[i]))) for i in antipode})
    pair_id = {p: k for k, p in enumerate(pairs)}
    centers = []
    for a, b in pairs:
        assert charts[a][0] == charts[b][0]
        centers.append(charts[a][0])

    qedges = set()
    for a, b in chart_graph.edges():
        u = pair_id[tuple(sorted((a, antipode[a])))]
        v = pair_id[tuple(sorted((b, antipode[b])))]
        if u != v:
            qedges.add(tuple(sorted((u, v))))

    incidence = nx.Graph()
    for qei, (u, v) in enumerate(sorted(qedges)):
        links = []
        for a in pairs[u]:
            for b in pairs[v]:
                inter = chart_sets[a] & chart_sets[b]
                if inter:
                    links.append((a, b, next(iter(inter))))
        assert len(links) == 2
        P, Q = centers[u], centers[v]
        for _, _, eid in links:
            r, s = nonedges[eid]
            apt = tuple(sorted((P, Q, r, s)))
            incidence.add_edge(("q", qei), ("a", apt))

    octets = []
    for comp in nx.connected_components(incidence):
        apartments = [set(n[1]) for n in comp if n[0] == "a"]
        octets.append(frozenset().union(*apartments))
    return sorted(set(octets), key=lambda S: sorted(S))


def find_center_quad_components(G):
    col = {p: set(G.neighbors(p)) for p in G.nodes()}
    components = []
    for S in itertools.combinations(range(40), 4):
        if all(not G.has_edge(a, b) for a, b in itertools.combinations(S, 2)):
            common = set(range(40))
            for p in S:
                common &= col[p]
            if len(common) == 4:
                components.append({"outer": tuple(S), "center": tuple(sorted(common))})
    return components


def main():
    pts, lines, idx, G, point_lines = build_w33()
    bt766_octets = compute_bt766_octets(G, lines, idx, point_lines)
    components = find_center_quad_components(G)

    outer_to_center = {c["outer"]: c["center"] for c in components}
    center_to_outer = {c["center"]: c["outer"] for c in components}

    involution_ok = True
    fixed = []
    involution_pairs = set()
    component_octets = []
    for c in components:
        outer = c["outer"]
        center = c["center"]
        if center not in outer_to_center or outer_to_center.get(center) != outer:
            involution_ok = False
        if outer == center:
            fixed.append(outer)
        pair = tuple(sorted((outer, center)))
        involution_pairs.add(pair)
        component_octets.append(frozenset(set(outer) | set(center)))

    unique_component_octets = sorted(set(component_octets), key=lambda S: sorted(S))
    octet_set = set(bt766_octets)
    component_octet_set = set(unique_component_octets)

    # The 45 quotient graph: adjacent if octets meet in two points.
    quotient_graph = nx.Graph()
    quotient_graph.add_nodes_from(range(len(unique_component_octets)))
    for i, j in itertools.combinations(range(len(unique_component_octets)), 2):
        if len(unique_component_octets[i] & unique_component_octets[j]) == 2:
            quotient_graph.add_edge(i, j)
    comp_graph = nx.complement(quotient_graph)

    def srg_params(H):
        degs = Counter(dict(H.degree()).values())
        lambdas = Counter()
        mus = Counter()
        for i, j in itertools.combinations(H.nodes(), 2):
            cn = len(set(H.neighbors(i)) & set(H.neighbors(j)))
            if H.has_edge(i, j):
                lambdas[cn] += 1
            else:
                mus[cn] += 1
        return degs, lambdas, mus

    q_degs, q_lam, q_mu = srg_params(quotient_graph)
    c_degs, c_lam, c_mu = srg_params(comp_graph)

    checks = {
        "old_center_quad_component_count_90": len(components) == 90,
        "unique_outer_and_center_quads_90_each": len(outer_to_center) == 90 and len(center_to_outer) == 90,
        "outer_center_is_fixed_point_free_involution": involution_ok and len(fixed) == 0,
        "old_quotient_pairs_45": len(involution_pairs) == 45,
        "component_octets_45": len(unique_component_octets) == 45,
        "BT766_octets_45": len(bt766_octets) == 45,
        "BT766_octets_equal_center_quad_unions": octet_set == component_octet_set,
        "each_octet_has_two_K4_halves": Counter(component_octets) and Counter(component_octets) == Counter({S: 2 for S in unique_component_octets}),
        "intersection_graph_SRG_45_32_22_24": quotient_graph.number_of_edges() == 720
        and q_degs == Counter({32: 45}) and q_lam == Counter({22: 720}) and q_mu == Counter({24: 270}),
        "disjointness_complement_SRG_45_12_3_3": comp_graph.number_of_edges() == 270
        and c_degs == Counter({12: 45}) and c_lam == Counter({3: 270}) and c_mu == Counter({3: 720}),
    }

    sample = []
    for i, pair in enumerate(sorted(involution_pairs)[:5]):
        outer, center = pair
        sample.append({
            "quotient_id": i,
            "outer_quad": list(outer),
            "center_quad": list(center),
            "octet": sorted(set(outer) | set(center)),
        })

    result = {
        "theorem": "BT769 Center-Quad / Intrinsic K4,4 Octet Identification Theorem",
        "summary": {
            "old_center_quad_components": len(components),
            "old_outer_center_involution_pairs": len(involution_pairs),
            "BT766_intrinsic_octets": len(bt766_octets),
            "identified_45_sets": octet_set == component_octet_set,
            "quotient_intersection_edges": quotient_graph.number_of_edges(),
            "quotient_disjointness_edges": comp_graph.number_of_edges(),
        },
        "sample_identifications": sample,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "This proves the set-level identification of the old center-quad 90/2 quotient with the BT766 intrinsic K4,4 octets. It does not yet identify external labels from older CSV/phase data; the matching is intrinsic W33 combinatorics."
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
