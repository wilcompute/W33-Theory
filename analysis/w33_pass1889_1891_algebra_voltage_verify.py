#!/usr/bin/env python3
"""Independent exact reconstruction for Passes 1889--1891."""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/w33_pass1876_rows45_hex.txt"
COMP = ROOT / "data/w33_pass1837_middle_layer_compression.json"
BRANCH = ROOT / "data/w33_pass1885_exceptional_s6_carrier_intertwiners.json"


def read_rows() -> list[int]:
    out = []
    for line in ROWS.read_text().splitlines():
        limbs = [int(x, 16) for x in line.split()]
        out.append(sum(x << (64 * i) for i, x in enumerate(limbs)))
    assert len(out) == 45
    return out


def permute_duad(d: tuple[int, int], p: tuple[int, ...]) -> tuple[int, int]:
    return tuple(sorted((p[d[0]], p[d[1]])))


def canonical_cycle(c: tuple[int, ...]) -> tuple[int, ...]:
    rots = []
    for z in (c, tuple(reversed(c))):
        rots += [z[i:] + z[:i] for i in range(len(z))]
    return min(rots)


def cycles_of_length(G: nx.Graph, length: int) -> set[tuple[int, ...]]:
    out: set[tuple[int, ...]] = set()
    for start in G:
        def dfs(path: list[int]) -> None:
            v = path[-1]
            if len(path) == length:
                if G.has_edge(v, start):
                    out.add(canonical_cycle(tuple(path)))
                return
            for w in G[v]:
                if w == start or w in path:
                    continue
                dfs(path + [w])
        dfs([start])
    return out


def main() -> dict:
    duads = list(itertools.combinations(range(6), 2))
    synthemes = []
    for pairs in itertools.combinations(duads, 3):
        if sorted(x for d in pairs for x in d) == list(range(6)):
            synthemes.append(tuple(sorted(pairs)))
    synthemes = sorted(set(synthemes))
    assert len(duads) == len(synthemes) == 15

    # Pass 1889: exact rank-nine domain lattice.
    AJ = sp.zeros(15)
    for i, a in enumerate(duads):
        for j, b in enumerate(duads):
            if i != j and len(set(a) & set(b)) == 1:
                AJ[i, j] = 1
    E9n = (AJ - 8 * sp.eye(15)) * (AJ - 2 * sp.eye(15))
    pivots = [0, 1, 2, 3, 5, 6, 7, 9, 10]
    gram = E9n.extract(pivots, pivots)
    snf = sp.matrices.normalforms.smith_normal_form(gram, domain=sp.ZZ)
    invariants = [abs(int(snf[i, i])) for i in range(9)]
    assert invariants == [2, 10, 10, 10, 20, 40, 40, 40, 40]
    assert abs(int(gram.det())) == 102_400_000_000

    # Pass 1890: commutant and C4 eigenspace arithmetic from exact characters.
    branch = json.loads(BRANCH.read_text())
    mult = Counter()
    for sector in ("24", "90"):
        mult.update({k: int(v) for k, v in branch["branching_by_partition"][sector].items()})
    assert mult == Counter({"(4, 1, 1)": 3, "(4, 2)": 2, "(3, 2, 1)": 2, "(3, 1, 1, 1)": 2, "(2, 2, 2)": 1, "(2, 2, 1, 1)": 1})
    s6_commutant_dimension = sum(v * v for v in mult.values())
    assert s6_commutant_dimension == 23

    def c4_mult(sector: str) -> dict[str, int]:
        chars = branch["restricted_characters"][sector]
        d = int(sector)
        t = int(chars["(4, 2)"])
        t2 = int(chars["(2, 2, 1, 1)"])
        a = (d + t2 + 2 * t) // 4
        b = (d + t2 - 2 * t) // 4
        c = (d - t2) // 4
        return {"1": a, "-1": b, "i": c, "-i": c}

    assert c4_mult("24") == {"1": 6, "-1": 6, "i": 6, "-i": 6}
    assert c4_mult("90") == {"1": 22, "-1": 20, "i": 24, "-i": 24}
    assert 28 * 28 + 26 * 26 + 2 * 30 * 30 == 3260

    # Pass 1891: Tutte--Coxeter graph and C4 voltage action.
    D = np.zeros((15, 15), dtype=np.int64)
    for i, s in enumerate(synthemes):
        for j, d in enumerate(duads):
            D[i, j] = int(d in s)
    G = nx.Graph()
    G.add_nodes_from(range(30))
    for i, j in zip(*np.nonzero(D)):
        G.add_edge(15 + int(i), int(j))
    assert G.number_of_nodes() == 30 and G.number_of_edges() == 45
    assert nx.is_connected(G) and nx.diameter(G) == 4

    gen = (1, 4, 3, 2, 5, 0)
    dperm = tuple(duads.index(permute_duad(d, gen)) for d in duads)
    sperm = tuple(synthemes.index(tuple(sorted(permute_duad(d, gen) for d in s))) for s in synthemes)
    vperm = tuple(dperm) + tuple(15 + sperm[i] for i in range(15))
    assert all(G.has_edge(vperm[a], vperm[b]) for a, b in G.edges())

    octagons = cycles_of_length(G, 8)
    assert len(octagons) == 90
    unseen = set(octagons)
    orbit_sizes = []
    while unseen:
        c = min(unseen)
        orbit = set()
        z = c
        for _ in range(4):
            orbit.add(canonical_cycle(tuple(vperm[x] for x in z)))
            z = tuple(vperm[x] for x in z)
        unseen.difference_update(orbit)
        orbit_sizes.append(len(orbit))
    assert Counter(orbit_sizes) == Counter({4: 22, 1: 2})

    # All 180 pair-transfer coordinates are nonincident syntheme--duad pairs.
    rows = read_rows()
    comp = json.loads(COMP.read_text())
    residual = [int(v) for v in comp["residual_vertices"]]
    vertex_to_duad = {int(k): int(v) for k, v in comp["residual_to_duad_index"].items()}
    pos_to_duad = [duads[vertex_to_duad[v]] for v in residual]
    pair_records = []
    pair_to_residual = {}
    type_counts = Counter()
    for e in range(240):
        fpos = [i for i in range(30) if (rows[i] >> e) & 1]
        rpos = [i for i in range(15) if (rows[30 + i] >> e) & 1]
        profile = (len(fpos), len(rpos))
        type_counts[profile] += 1
        if profile == (2, 1):
            fp = tuple(sorted((fpos[0] // 5, fpos[1] // 5)))
            pair_to_residual.setdefault(fp, set()).add(pos_to_duad[rpos[0]])
            pair_records.append((fp, pos_to_duad[rpos[0]]))
    assert type_counts == Counter({(2, 1): 180, (3, 0): 40, (0, 3): 20})
    pair_to_syntheme = {}
    for fp, appearing in pair_to_residual.items():
        missing = tuple(sorted(set(duads) - appearing))
        assert missing in synthemes
        pair_to_syntheme[fp] = missing
    nonincidences = {(pair_to_syntheme[fp], d) for fp, d in pair_records}
    assert len(nonincidences) == 180
    assert all(d not in s for s, d in nonincidences)

    # Exact Hashimoto twisted traces.
    undirected = sorted(tuple(sorted(e)) for e in G.edges())
    states = [(a, b) for a, b in undirected for a, b in ((a, b), (b, a))]
    si = {s: i for i, s in enumerate(states)}
    B = np.zeros((90, 90), dtype=np.int64)
    for i, (a, b) in enumerate(states):
        for c in G[b]:
            if c != a:
                B[si[(b, c)], i] = 1
    sp_state = tuple(si[(vperm[a], vperm[b])] for a, b in states)
    powers = [np.eye(90, dtype=np.int64)]
    for _ in range(16):
        powers.append(B @ powers[-1])
    expected = {
        0: [0, 0, 0, 0, 0, 0, 0, 1440, 0, 1440, 0, 7200, 0, 30240, 0, 145440],
        1: [0, 16, 0, 0, 0, 160, 0, 512, 0, 2176, 0, 7680, 0, 33280, 0, 131072],
        2: [0, 0, 0, 32, 0, 96, 0, 640, 0, 1920, 0, 8192, 0, 32256, 0, 133120],
        3: [0, 16, 0, 0, 0, 160, 0, 512, 0, 2176, 0, 7680, 0, 33280, 0, 131072],
    }
    for k in range(4):
        p = tuple(range(90))
        for _ in range(k):
            p = tuple(sp_state[p[i]] for i in range(90))
        got = [sum(int(powers[n][i, p[i]]) for i in range(90)) for n in range(1, 17)]
        assert got == expected[k]

    out = {
        "status": "PASS",
        "gram_snf": invariants,
        "s6_commutant_dimension": s6_commutant_dimension,
        "c4_multiplicities": {"24": c4_mult("24"), "90": c4_mult("90")},
        "tutte_coxeter_octagon_orbits": dict(Counter(orbit_sizes)),
        "pair_transfer_nonincidences": len(nonincidences),
        "hashimoto_twisted_traces_verified": True,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return out


if __name__ == "__main__":
    main()
