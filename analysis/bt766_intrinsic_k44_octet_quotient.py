#!/usr/bin/env python3
"""BT766 — Intrinsic K4,4 octet quotient theorem.

This verifier builds W(3,3), its centered local K_{3,3} charts, and the
chart-antipodal quotient.  The new result is that the quotient/apartment
incidence decomposes into 405 little C8 components, but those components
collapse 9-to-1 onto exactly 45 induced K_{4,4} octets inside the W33
point graph.

Those 45 octets are not an imposed tomotope/codec layer.  They are an
intrinsic partition of the 540 W33 nonedges into 45 packets of 12
nonedges each, and their intersection graph recovers the known 45-point
quotient SRG layer.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx
import numpy as np

MOD = 3
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT766_INTRINSIC_K44_OCTET_QUOTIENT_results.json"


def inv(a: int) -> int:
    a %= MOD
    if a == 1:
        return 1
    if a == 2:
        return 2
    raise ZeroDivisionError(a)


def norm(v):
    v = tuple(x % MOD for x in v)
    for x in v:
        if x % MOD:
            s = inv(x)
            return tuple((s * y) % MOD for y in v)
    raise ValueError("zero vector")


def add(u, v):
    return tuple((a + b) % MOD for a, b in zip(u, v))


def smul(a, v):
    return tuple((a * x) % MOD for x in v)


def symp(u, v):
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % MOD


def build_w33():
    pts = sorted({norm(v) for v in itertools.product(range(MOD), repeat=4) if any(v)})
    idx = {p: i for i, p in enumerate(pts)}
    lines = set()
    for p, q in itertools.combinations(pts, 2):
        if symp(p, q) == 0:
            L = frozenset(
                norm(add(smul(a, p), smul(b, q)))
                for a in range(MOD)
                for b in range(MOD)
                if a or b
            )
            if len(L) == 4:
                lines.add(L)
    lines = sorted(lines, key=lambda L: sorted(idx[p] for p in L))

    G = nx.Graph()
    G.add_nodes_from(range(len(pts)))
    point_lines = defaultdict(list)
    for li, L in enumerate(lines):
        ids = sorted(idx[p] for p in L)
        for p in ids:
            point_lines[p].append(li)
        for a, b in itertools.combinations(ids, 2):
            G.add_edge(a, b, line=li)
    return pts, lines, idx, G, point_lines


def srg_parameters(G):
    degs = Counter(dict(G.degree()).values())
    lambdas = Counter()
    mus = Counter()
    for i, j in itertools.combinations(G.nodes(), 2):
        cn = len(set(G.neighbors(i)) & set(G.neighbors(j)))
        if G.has_edge(i, j):
            lambdas[cn] += 1
        else:
            mus[cn] += 1
    return degs, lambdas, mus


def canonical_counter(counter):
    return {str(k): int(v) for k, v in sorted(counter.items())}


def spectrum_counter(G):
    vals = np.linalg.eigvalsh(nx.to_numpy_array(G, nodelist=sorted(G.nodes())))
    return canonical_counter(Counter(int(round(x)) for x in vals))


def main():
    pts, lines, idx, G, point_lines = build_w33()
    degs, lambdas, mus = srg_parameters(G)

    nonedges = []
    nonedge_to_id = {}
    for a, b in itertools.combinations(range(40), 2):
        if not G.has_edge(a, b):
            nonedge_to_id[(a, b)] = len(nonedges)
            nonedges.append((a, b))

    charts = []
    chart_nonedges = []
    for p in range(40):
        for l1, l2 in itertools.combinations(point_lines[p], 2):
            A = sorted(idx[x] for x in lines[l1] if idx[x] != p)
            B = sorted(idx[x] for x in lines[l2] if idx[x] != p)
            nes = []
            for a in A:
                for b in B:
                    e = tuple(sorted((a, b)))
                    assert e in nonedge_to_id
                    nes.append(nonedge_to_id[e])
            charts.append((p, l1, l2))
            chart_nonedges.append(tuple(sorted(nes)))

    chart_graph = nx.Graph()
    chart_graph.add_nodes_from(range(len(charts)))
    chart_sets = [set(x) for x in chart_nonedges]
    for i, j in itertools.combinations(range(len(charts)), 2):
        inter = len(chart_sets[i] & chart_sets[j])
        assert inter in (0, 1)
        if inter == 1:
            chart_graph.add_edge(i, j)

    distances = dict(nx.all_pairs_shortest_path_length(chart_graph))
    antipode = {}
    for i, d in distances.items():
        far = [j for j, dd in d.items() if dd == 4]
        assert len(far) == 1
        antipode[i] = far[0]
    assert all(antipode[antipode[i]] == i for i in antipode)

    antipodal_pairs = sorted({tuple(sorted((i, antipode[i]))) for i in antipode})
    pair_id = {p: k for k, p in enumerate(antipodal_pairs)}
    pair_meta = []
    for a, b in antipodal_pairs:
        assert charts[a][0] == charts[b][0]
        pair_meta.append({"center": charts[a][0], "charts": [a, b]})

    quotient = nx.Graph()
    quotient.add_nodes_from(range(len(antipodal_pairs)))
    multiplicity = Counter()
    qedge_links = {}
    for a, b in chart_graph.edges():
        qa = pair_id[tuple(sorted((a, antipode[a])))]
        qb = pair_id[tuple(sorted((b, antipode[b])))]
        if qa == qb:
            continue
        u, v = sorted((qa, qb))
        quotient.add_edge(u, v)
        multiplicity[(u, v)] += 1

    qedge_to_apartments = []
    for qei, (u, v) in enumerate(sorted(multiplicity)):
        links = []
        for a in antipodal_pairs[u]:
            for b in antipodal_pairs[v]:
                inter = chart_sets[a] & chart_sets[b]
                if inter:
                    assert len(inter) == 1
                    links.append((a, b, next(iter(inter))))
        assert len(links) == 2
        P = pair_meta[u]["center"]
        Q = pair_meta[v]["center"]
        assert not G.has_edge(P, Q)
        apartments = []
        for _, _, eid in links:
            r, s = nonedges[eid]
            A = frozenset((P, Q, r, s))
            sub = G.subgraph(A)
            assert sub.number_of_edges() == 4
            assert sorted(dict(sub.degree()).values()) == [2, 2, 2, 2]
            apartments.append(A)
        qedge_to_apartments.append((u, v, apartments))

    incidence = nx.Graph()
    for qei, (_, _, apts) in enumerate(qedge_to_apartments):
        incidence.add_node(("qedge", qei), bipartite=0)
        for A in apts:
            incidence.add_node(("apt", tuple(sorted(A))), bipartite=1)
            incidence.add_edge(("qedge", qei), ("apt", tuple(sorted(A))))

    comp_sizes = Counter()
    comp_is_c8 = True
    component_octets = []
    for comp in nx.connected_components(incidence):
        comp_sizes[len(comp)] += 1
        if len(comp) != 8 or any(incidence.degree(n) != 2 for n in comp):
            comp_is_c8 = False
        apartments = [frozenset(n[1]) for n in comp if n[0] == "apt"]
        octet = frozenset().union(*apartments)
        component_octets.append(octet)

    octet_mult = Counter(component_octets)
    unique_octets = sorted(octet_mult, key=lambda S: sorted(S))

    octet_k44_ok = True
    for S in unique_octets:
        sub = G.subgraph(S)
        if len(S) != 8 or not nx.is_bipartite(sub):
            octet_k44_ok = False
            break
        if sub.number_of_edges() != 16 or sorted(dict(sub.degree()).values()) != [4] * 8:
            octet_k44_ok = False
            break

    point_octet_count = Counter(p for S in unique_octets for p in S)
    edge_octet_count = Counter()
    nonedge_octet_count = Counter()
    for S in unique_octets:
        for a, b in itertools.combinations(sorted(S), 2):
            if G.has_edge(a, b):
                edge_octet_count[(a, b)] += 1
            else:
                nonedge_octet_count[(a, b)] += 1

    octet_graph = nx.Graph()
    octet_graph.add_nodes_from(range(len(unique_octets)))
    intersection_sizes = Counter()
    for i, j in itertools.combinations(range(len(unique_octets)), 2):
        s = len(unique_octets[i] & unique_octets[j])
        intersection_sizes[s] += 1
        if s == 2:
            octet_graph.add_edge(i, j)

    oct_degs, oct_lam, oct_mu = srg_parameters(octet_graph)
    oct_comp = nx.complement(octet_graph)
    comp_degs, comp_lam, comp_mu = srg_parameters(oct_comp)

    checks = {
        "W33_SRG_40_12_2_4": len(pts) == 40 and len(lines) == 40 and G.number_of_edges() == 240
        and degs == Counter({12: 40}) and lambdas == Counter({2: 240}) and mus == Counter({4: 540}),
        "local_chart_count_240": len(charts) == 240 and len(set(chart_nonedges)) == 240,
        "chart_graph_27_regular_diameter_4": chart_graph.number_of_nodes() == 240
        and Counter(dict(chart_graph.degree()).values()) == Counter({27: 240})
        and nx.diameter(chart_graph) == 4,
        "unique_antipode_per_chart": len(antipodal_pairs) == 120,
        "quotient_has_120_vertices_1620_edges_multiplicity_2": quotient.number_of_nodes() == 120
        and quotient.number_of_edges() == 1620 and Counter(multiplicity.values()) == Counter({2: 1620}),
        "qedge_apartment_incidence_405_C8_components": comp_sizes == Counter({8: 405}) and comp_is_c8,
        "components_collapse_9_to_1_onto_45_octets": len(unique_octets) == 45
        and Counter(octet_mult.values()) == Counter({9: 45}),
        "each_octet_induces_K44": octet_k44_ok,
        "octets_cover_points_edges_nonedges_with_9_3_1": Counter(point_octet_count.values()) == Counter({9: 40})
        and Counter(edge_octet_count.values()) == Counter({3: 240})
        and Counter(nonedge_octet_count.values()) == Counter({1: 540}),
        "octet_intersection_graph_SRG_45_32_22_24": octet_graph.number_of_nodes() == 45
        and octet_graph.number_of_edges() == 720
        and oct_degs == Counter({32: 45}) and oct_lam == Counter({22: 720}) and oct_mu == Counter({24: 270}),
        "octet_disjointness_complement_SRG_45_12_3_3": oct_comp.number_of_nodes() == 45
        and oct_comp.number_of_edges() == 270
        and comp_degs == Counter({12: 45}) and comp_lam == Counter({3: 270}) and comp_mu == Counter({3: 720}),
    }

    result = {
        "theorem": "BT766 Intrinsic K4,4 Octet Quotient Theorem",
        "summary": {
            "W33_points": len(pts),
            "W33_lines": len(lines),
            "W33_edges": G.number_of_edges(),
            "W33_nonedges": len(nonedges),
            "centered_local_K33_charts": len(charts),
            "chart_graph_edges": chart_graph.number_of_edges(),
            "chart_graph_diameter": nx.diameter(chart_graph),
            "antipodal_chart_pairs": len(antipodal_pairs),
            "quotient_vertices": quotient.number_of_nodes(),
            "quotient_edges": quotient.number_of_edges(),
            "qedge_apartment_incidence_components": nx.number_connected_components(incidence),
            "unique_K44_octets": len(unique_octets),
            "octet_multiplicity_distribution": canonical_counter(Counter(octet_mult.values())),
        },
        "spectra": {
            "chart_graph": spectrum_counter(chart_graph),
            "antipodal_quotient_graph": spectrum_counter(quotient),
            "octet_intersection_graph": spectrum_counter(octet_graph),
            "octet_disjointness_complement": spectrum_counter(oct_comp),
        },
        "covering_laws": {
            "point_octet_incidence": canonical_counter(Counter(point_octet_count.values())),
            "W33_edge_octet_incidence": canonical_counter(Counter(edge_octet_count.values())),
            "W33_nonedge_octet_incidence": canonical_counter(Counter(nonedge_octet_count.values())),
            "octet_pair_intersection_sizes": canonical_counter(intersection_sizes),
            "component_size_distribution": canonical_counter(comp_sizes),
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": (
            "The 45 K4,4 octets are intrinsic W33 point-subgraphs and recover the 45-point "
            "quotient SRG layer.  This does not assert the missing BT763 root-torsor to Q(4,3) "
            "transport table; it bypasses that table by using chart/apartment incidence already "
            "visible inside W(3,3)."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
