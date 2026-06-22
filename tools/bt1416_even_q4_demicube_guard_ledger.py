#!/usr/bin/env python3
"""BT1416: even-Q4 demicube guard ledger."""
from itertools import combinations, product
from collections import Counter
from pathlib import Path
import json
import networkx as nx

EVEN_TICKS = [0, 6, 3, 5, 9, 15, 10, 12]
BT1412_EVEN_TICKS = EVEN_TICKS

def int_to_word(n):
    return tuple((n >> i) & 1 for i in range(4))

def word_to_int(word):
    return sum(bit << i for i, bit in enumerate(word))

def ham(a, b):
    return sum(x != y for x, y in zip(a, b))

def q4():
    g = nx.Graph()
    words = list(product([0, 1], repeat=4))
    g.add_nodes_from(words)
    for a, b in combinations(words, 2):
        if ham(a, b) == 1:
            g.add_edge(a, b)
    return g

def q4_square_faces():
    faces = []
    for free in combinations(range(4), 2):
        fixed_coords = [c for c in range(4) if c not in free]
        for fixed_vals in product([0, 1], repeat=2):
            fixed = dict(zip(fixed_coords, fixed_vals))
            verts = []
            for free_vals in product([0, 1], repeat=2):
                word = [0, 0, 0, 0]
                for c, val in fixed.items():
                    word[c] = val
                for c, val in zip(free, free_vals):
                    word[c] = val
                verts.append(tuple(word))
            faces.append({"free": free, "fixed": fixed, "vertices": verts})
    return faces

def even_layer_graph(evens):
    g = nx.Graph()
    g.add_nodes_from(evens)
    for a, b in combinations(evens, 2):
        if ham(a, b) == 2:
            g.add_edge(a, b)
    return g

def gf2_rank(rows):
    mat = [r[:] for r in rows]
    if not mat:
        return 0
    m, cols = len(mat), len(mat[0])
    rank = col = 0
    while rank < m and col < cols:
        pivot = next((r for r in range(rank, m) if mat[r][col] & 1), None)
        if pivot is None:
            col += 1
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        for r in range(m):
            if r != rank and (mat[r][col] & 1):
                mat[r] = [x ^ y for x, y in zip(mat[r], mat[rank])]
        rank += 1
        col += 1
    return rank

def main():
    Q4 = q4()
    evens = [int_to_word(t) for t in EVEN_TICKS]
    G = even_layer_graph(evens)
    comp = nx.complement(G)
    comp.remove_edges_from(nx.selfloop_edges(comp))
    axes = sorted(tuple(sorted(c)) for c in nx.connected_components(comp) if len(c) == 2)

    idx = {word: i for i, word in enumerate(evens)}
    guard_rows, face_rows = [], []
    for face_id, face in enumerate(q4_square_faces()):
        e = [v for v in face["vertices"] if sum(v) % 2 == 0]
        o = [v for v in face["vertices"] if sum(v) % 2 == 1]
        assert len(e) == len(o) == 2 and ham(e[0], e[1]) == 2
        row = [0] * 8
        row[idx[e[0]]] = row[idx[e[1]]] = 1
        guard_rows.append(row)
        face_rows.append({
            "face_id": face_id,
            "free_coords": list(face["free"]),
            "fixed": {str(k): v for k, v in face["fixed"].items()},
            "even_diagonal": sorted([word_to_int(e[0]), word_to_int(e[1])]),
            "odd_diagonal": sorted([word_to_int(o[0]), word_to_int(o[1])]),
        })

    guard_edges = {tuple(r["even_diagonal"]) for r in face_rows}
    even_edges = {tuple(sorted((word_to_int(a), word_to_int(b)))) for a, b in G.edges()}

    singleton_rows = []
    for _cycle in range(27):
        for state in range(8):
            row = [0] * 8
            row[state] = 1
            singleton_rows.append(row)
    full_rows = singleton_rows + guard_rows

    axis_of = {}
    for axis, pair in enumerate(axes):
        for word in pair:
            axis_of[word] = axis
    axis_hist = Counter(tuple(sorted((axis_of[a], axis_of[b]))) for a, b in G.edges())

    checks = {
        "q4_has_16_vertices": Q4.number_of_nodes() == 16,
        "q4_has_32_edges": Q4.number_of_edges() == 32,
        "q4_has_24_square_faces": len(q4_square_faces()) == 24,
        "even_ticks_are_even": all(sum(x) % 2 == 0 for x in evens),
        "even_layer_has_8_vertices": G.number_of_nodes() == 8,
        "even_layer_has_24_edges": G.number_of_edges() == 24,
        "even_layer_is_6_regular": sorted(dict(G.degree()).values()) == [6] * 8,
        "even_layer_is_K2222": nx.is_isomorphic(G, nx.complete_multipartite_graph(2, 2, 2, 2)),
        "complement_is_4_antipodal_edges": len(axes) == 4 and comp.number_of_edges() == 4,
        "q4_faces_biject_to_even_edges": guard_edges == even_edges and len(guard_edges) == 24,
        "guard_rank_F2_is_7": gf2_rank(guard_rows) == 7,
        "full_ledger_has_240_rows": len(full_rows) == 240,
        "full_ledger_rank_F2_is_8": gf2_rank(full_rows) == 8,
        "full_ledger_state_degree_is_33": sorted(sum(row[i] for row in full_rows) for i in range(8)) == [33] * 8,
        "six_axis_pairs_each_have_4_edges": sorted(axis_hist.values()) == [4] * 6,
    }

    result = {
        "bt": 1416,
        "name": "Even-Q4 Demicube Guard Ledger Theorem",
        "theorem": "BT1412's eight even Q4 words form K_{2,2,2,2}; its 24 distance-2 edges are exactly the even diagonals of the 24 Q4 square plaquettes, so BT1415's 24 guard rows are the Q4 plaquette incidence ledger.",
        "counts": {
            "q4_vertices": Q4.number_of_nodes(),
            "q4_edges": Q4.number_of_edges(),
            "q4_square_faces": len(q4_square_faces()),
            "even_states": len(evens),
            "even_layer_edges": G.number_of_edges(),
            "antipodal_axes": len(axes),
            "axis_pairs": len(axis_hist),
            "guard_rows": len(guard_rows),
            "guard_rank_F2": gf2_rank(guard_rows),
            "steinberg_singleton_rows": len(singleton_rows),
            "full_css_frontend_rows": len(full_rows),
            "full_ledger_rank_F2": gf2_rank(full_rows),
            "state_degree_in_full_ledger": 33,
        },
        "identities": {
            "q4_faces": "C(4,2)*2^2 = 24",
            "even_demicube_edges": "8*6/2 = 24",
            "axis_pair_factorization": "C(4,2)*4 = 24",
            "css_frontend_rows": "27*8 + 24 = 240",
            "per_even_state_degree": "27 + 6 = 33",
        },
        "even_ticks": EVEN_TICKS,
        "even_words": ["".join(map(str, x)) for x in evens],
        "antipodal_axis_pairs": [["".join(map(str, a)), "".join(map(str, b))] for a, b in axes],
        "axis_pair_histogram": {str(k): v for k, v in sorted(axis_hist.items())},
        "face_to_even_diagonal_sample": face_rows[:8],
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "Binary Q4 guard-front-end only: this does not construct the F3 Steinberg module, prove a new CSS stabilizer code, or calibrate a chip. Guard rows alone have F2-rank 7; the 216 singleton Steinberg rows complete rank 8.",
    }
    assert result["all_checks_pass"], checks
    Path("data").mkdir(exist_ok=True)
    Path("data/PART_BT1416_EVEN_Q4_DEMICUBE_GUARD_LEDGER_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"all_checks_pass": True, "counts": result["counts"]}, indent=2))

if __name__ == "__main__":
    main()
