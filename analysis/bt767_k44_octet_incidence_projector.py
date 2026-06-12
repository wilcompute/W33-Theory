#!/usr/bin/env python3
"""BT767 — K4,4 octet incidence projector theorem.

BT766 found the 45 intrinsic K_{4,4} octets.  This verifier studies the
40-by-45 point/octet incidence matrix M and proves it is a spectral
projector/filter:

    M M^T = 8 I + J + 2 A_W33,

so the octet layer kills the 15-dimensional (-4)-eigenspace of W33 and
keeps exactly the 1+24 positive sector.  Dually,

    M^T M = 8 I + 2 A_oct,

where A_oct is the 45-octet intersection graph SRG(45,32,22,24).
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np

from bt766_intrinsic_k44_octet_quotient import build_w33

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT767_K44_OCTET_INCIDENCE_PROJECTOR_results.json"


def cdict(counter):
    return {str(k): int(v) for k, v in sorted(counter.items())}


def matrix_spectrum_counter(M):
    vals = np.linalg.eigvalsh(M)
    return cdict(Counter(int(round(x)) for x in vals))


def get_octets():
    pts, lines, idx, G, point_lines = build_w33()
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
            nes = []
            for a in A:
                for b in B:
                    nes.append(nonedge_to_id[tuple(sorted((a, b)))])
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
        apts = [set(n[1]) for n in comp if n[0] == "a"]
        octets.append(frozenset().union(*apts))
    unique_octets = sorted(set(octets), key=lambda S: sorted(S))
    return G, unique_octets


def srg_params(G):
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


def main():
    G, octets = get_octets()
    A = nx.to_numpy_array(G, nodelist=range(40), dtype=int)
    I40 = np.eye(40, dtype=int)
    J40 = np.ones((40, 40), dtype=int)

    M = np.zeros((40, len(octets)), dtype=int)
    for j, S in enumerate(octets):
        for p in S:
            M[p, j] = 1

    MMt = M @ M.T
    expected_MMt = 8 * I40 + J40 + 2 * A

    oct_graph = nx.Graph()
    oct_graph.add_nodes_from(range(len(octets)))
    for i, j in itertools.combinations(range(len(octets)), 2):
        if len(octets[i] & octets[j]) == 2:
            oct_graph.add_edge(i, j)
    Ao = nx.to_numpy_array(oct_graph, nodelist=range(45), dtype=int)
    MtM = M.T @ M
    expected_MtM = 8 * np.eye(45, dtype=int) + 2 * Ao

    edge_weights = Counter()
    nonedge_weights = Counter()
    for a, b in itertools.combinations(range(40), 2):
        val = int(MMt[a, b])
        if G.has_edge(a, b):
            edge_weights[val] += 1
        else:
            nonedge_weights[val] += 1

    oct_degs, oct_lam, oct_mu = srg_params(oct_graph)
    oct_comp = nx.complement(oct_graph)
    comp_degs, comp_lam, comp_mu = srg_params(oct_comp)

    checks = {
        "incidence_shape_40_by_45": list(M.shape) == [40, 45],
        "row_sum_9_col_sum_8": Counter(M.sum(axis=1)) == Counter({9: 40}) and Counter(M.sum(axis=0)) == Counter({8: 45}),
        "MMt_formula_8I_plus_J_plus_2A": np.array_equal(MMt, expected_MMt),
        "MtM_formula_8I_plus_2A_octet": np.array_equal(MtM, expected_MtM),
        "rank_25_equals_1_plus_24": int(np.linalg.matrix_rank(M)) == 25,
        "MMt_spectrum_72_12_0": matrix_spectrum_counter(MMt) == {"0": 15, "12": 24, "72": 1},
        "MtM_spectrum_72_12_0": matrix_spectrum_counter(MtM) == {"0": 20, "12": 24, "72": 1},
        "adjacent_pairs_share_3_octets": edge_weights == Counter({3: 240}),
        "nonadjacent_pairs_share_1_octet": nonedge_weights == Counter({1: 540}),
        "octet_graph_SRG_45_32_22_24": oct_graph.number_of_edges() == 720
        and oct_degs == Counter({32: 45}) and oct_lam == Counter({22: 720}) and oct_mu == Counter({24: 270}),
        "octet_complement_SRG_45_12_3_3": oct_comp.number_of_edges() == 270
        and comp_degs == Counter({12: 45}) and comp_lam == Counter({3: 270}) and comp_mu == Counter({3: 720}),
    }

    result = {
        "theorem": "BT767 K4,4 Octet Incidence Projector Theorem",
        "incidence_matrix": {
            "shape": [int(x) for x in M.shape],
            "row_sum_distribution": cdict(Counter(int(x) for x in M.sum(axis=1))),
            "column_sum_distribution": cdict(Counter(int(x) for x in M.sum(axis=0))),
            "rank": int(np.linalg.matrix_rank(M)),
        },
        "formulas": {
            "MMt": "8I_40 + J_40 + 2A_W33",
            "MtM": "8I_45 + 2A_octet",
            "interpretation": "The octet incidence layer preserves the 1+24 W33 spectral sector and kills the 15-dimensional (-4)-sector."
        },
        "spectra": {
            "MMt": matrix_spectrum_counter(MMt),
            "MtM": matrix_spectrum_counter(MtM),
            "A_octet_intersection": matrix_spectrum_counter(Ao),
            "A_octet_disjointness_complement": matrix_spectrum_counter(nx.to_numpy_array(oct_comp, nodelist=range(45), dtype=int)),
        },
        "pair_weights": {
            "W33_adjacent_pair_shared_octets": cdict(edge_weights),
            "W33_nonadjacent_pair_shared_octets": cdict(nonedge_weights),
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "This is an incidence/projector theorem for the 45 intrinsic octets from BT766. It is not a claim that the octet incidence is the Levi H1/E4 sector; it is the complementary 1+24 filter."
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
