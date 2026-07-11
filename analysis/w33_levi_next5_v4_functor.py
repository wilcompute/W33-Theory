#!/usr/bin/env python3
"""Explicit W(3,3) -> E6 -> E8 incidence functor with generator-level equivariance."""
from __future__ import annotations
from functools import lru_cache

from collections import Counter, deque
from itertools import combinations, product
import json
import sys
from pathlib import Path

import networkx as nx
import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from w33_levi_next5_v4_common import (
    SEEDS, apply_cols, build_w33, compose_cols, compose_perm, dot2,
    group_closure_cols, homology_action, invariant_linear_span,
    line_perm_from_point_perm, point_outer_perm, point_transvection_perm,
    restrict_action, sha256_json, weight_q,
)


def classical_lines():
    labels = [f"E{i}" for i in range(6)]
    labels += [f"L{i}{j}" for i, j in combinations(range(6), 2)]
    labels += [f"Q{i}" for i in range(6)]

    def intersects(a, b):
        if a == b:
            return False
        ka, kb = a[0], b[0]
        if ka == "E" and kb == "E":
            return False
        if ka == "Q" and kb == "Q":
            return False
        if ka == "E" and kb == "L":
            return int(a[1]) in {int(b[1]), int(b[2])}
        if ka == "L" and kb == "E":
            return intersects(b, a)
        if ka == "E" and kb == "Q":
            return int(a[1]) != int(b[1])
        if ka == "Q" and kb == "E":
            return intersects(b, a)
        if ka == "L" and kb == "L":
            return not ({int(a[1]), int(a[2])} & {int(b[1]), int(b[2])})
        if ka == "L" and kb == "Q":
            return int(b[1]) in {int(a[1]), int(a[2])}
        if ka == "Q" and kb == "L":
            return intersects(b, a)
        raise AssertionError((a, b))

    G = nx.Graph()
    G.add_nodes_from(range(27))
    for i, j in combinations(range(27), 2):
        if intersects(labels[i], labels[j]):
            G.add_edge(i, j)
    assert set(dict(G.degree()).values()) == {10}
    return labels, G


def v3_module():
    geom = build_w33()
    pgens = [point_transvection_perm(geom.points, v) for v in SEEDS]
    outerp = point_outer_perm(geom.points)
    lgens = [line_perm_from_point_perm(geom.lines, p) for p in pgens]
    outerl = line_perm_from_point_perm(geom.lines, outerp)
    _, hom, acts = homology_action(geom.line_adjacency, lgens + [outerl])
    u6 = invariant_linear_span(0x3D7, acts[:-1])
    assert len(u6) == 6
    racts = restrict_action(acts, u6)

    def ambient_h(c):
        out = 0
        for i, rep in enumerate(hom):
            if (c >> i) & 1:
                out ^= rep
        return out

    def ambient6(v):
        c = 0
        for i, b in enumerate(u6):
            if (v >> i) & 1:
                c ^= b
        return ambient_h(c)

    singular = [v for v in range(1, 64) if weight_q(ambient6(v)) == 0]
    assert len(singular) == 27
    sindex = {v: i for i, v in enumerate(singular)}
    line_perms = [tuple(sindex[apply_cols(a, v)] for v in singular) for a in racts]
    G = nx.Graph()
    G.add_nodes_from(range(27))
    for i, j in combinations(range(27), 2):
        if dot2(ambient6(singular[i]), ambient6(singular[j])) == 0:
            G.add_edge(i, j)
    labels, CG = classical_lines()
    mapping = next(nx.algorithms.isomorphism.GraphMatcher(G, CG).isomorphisms_iter())
    names = [None] * 27
    for s, c in mapping.items():
        names[s] = labels[c]
    return geom, pgens + [outerp], lgens + [outerl], racts, line_perms, G, names, singular


def object_sets(G):
    triangles = [tuple(c) for c in combinations(range(27), 3) if all(G.has_edge(i, j) for i, j in combinations(c, 2))]
    sixes = [tuple(c) for c in combinations(range(27), 6) if all(not G.has_edge(i, j) for i, j in combinations(c, 2))]
    assert len(triangles) == 45 and len(sixes) == 72
    return triangles, sixes


def set_action_perm(lineperm, objects):
    idx = {frozenset(x): i for i, x in enumerate(objects)}
    return tuple(idx[frozenset(lineperm[x] for x in obj)] for obj in objects)


def e8_roots():
    roots = []
    for i, j in combinations(range(8), 2):
        for si, sj in product((-2, 2), repeat=2):
            v = [0] * 8
            v[i], v[j] = si, sj
            roots.append(tuple(v))
    for signs in product((-1, 1), repeat=8):
        if sum(1 for x in signs if x < 0) % 2 == 0:
            roots.append(tuple(signs))
    roots = sorted(set(roots))
    assert len(roots) == 240 and all(sum(x*x for x in r) == 8 for r in roots)
    return roots


def ip(a, b):
    value = sum(x*y for x, y in zip(a, b))
    assert value % 4 == 0
    return value // 4


def reflection_perm(roots, alpha):
    idx = {r: i for i, r in enumerate(roots)}
    out = []
    for r in roots:
        k = ip(r, alpha)
        s = tuple(r[i] - k * alpha[i] for i in range(8))
        out.append(idx[s])
    return tuple(out)


def find_e6_simple_roots(roots72):
    nbr = {r: [s for s in roots72 if ip(r, s) == -1] for r in roots72}
    center = roots72[0]
    for a1 in nbr[center]:
        for a0 in nbr[a1]:
            if a0 == center or ip(a0, center) != 0:
                continue
            for a3 in nbr[center]:
                if a3 in {a1, a0} or ip(a3, a1) != 0 or ip(a3, a0) != 0:
                    continue
                for a4 in nbr[a3]:
                    if a4 in {center, a1, a0}:
                        continue
                    if any(ip(a4, x) != 0 for x in (center, a1, a0)):
                        continue
                    for a5 in nbr[center]:
                        if a5 in {a0, a1, a3, a4}:
                            continue
                        if any(ip(a5, x) != 0 for x in (a0, a1, a3, a4)):
                            continue
                        simple = [a0, a1, center, a3, a4, a5]
                        if np.linalg.matrix_rank(np.array(simple, dtype=float)) == 6:
                            return simple
    raise RuntimeError("failed to find E6 simple roots")


def orbit(seed, gens):
    seen = {seed}
    q = deque([seed])
    while q:
        x = q.popleft()
        for g in gens:
            y = g[x]
            if y not in seen:
                seen.add(y)
                q.append(y)
    return sorted(seen)


def conjugate_perm(p, mapping, n):
    inv = [0] * n
    for old, new in mapping.items():
        inv[new] = old
    return tuple(mapping[p[inv[i]]] for i in range(n))


def find_generator_lifts(std27_gens, std240_gens, targets):
    identity = tuple(range(27))
    seen = {identity: 0}
    states = [identity]
    parent = [(-1, -1)]
    q = deque([0])
    target_set = set(targets)
    found = {identity} & target_set
    while q and len(found) < len(target_set):
        sid = q.popleft()
        state = states[sid]
        for gi, gen in enumerate(std27_gens):
            nxt = compose_perm(gen, state)
            if nxt not in seen:
                nid = len(states)
                seen[nxt] = nid
                states.append(nxt)
                parent.append((sid, gi))
                q.append(nid)
                if nxt in target_set:
                    found.add(nxt)
    if len(found) != len(target_set):
        raise RuntimeError(f"only found {len(found)} of {len(target_set)} target generators")

    def word_for(target):
        sid = seen[target]
        word = []
        while parent[sid][0] >= 0:
            sid, gi = parent[sid]
            word.append(gi)
        word.reverse()
        return word

    lifted = []
    words = []
    for target in targets:
        word = word_for(target)
        p = tuple(range(240))
        for gi in word:
            p = compose_perm(std240_gens[gi], p)
        lifted.append(p)
        words.append(word)
    return lifted, words, len(seen)


def incidence_equivariant(rows, col_perm, row_perm):
    idx = {frozenset(row): i for i, row in enumerate(rows)}
    induced = tuple(idx[frozenset(col_perm[x] for x in row)] for row in rows)
    return induced == row_perm


def paired_psp_closure(pgens, line27gens):
    ep = tuple(range(40))
    el = tuple(range(27))
    seen = {el: ep}
    q = deque([(el, ep)])
    while q:
        l, p = q.popleft()
        for gl, gp in zip(line27gens, pgens):
            nl = compose_perm(gl, l)
            np_ = compose_perm(gp, p)
            if nl not in seen:
                seen[nl] = np_
                q.append((nl, np_))
            else:
                assert seen[nl] == np_
    assert len(seen) == 25920
    return seen


@lru_cache(maxsize=1)
def analyze():
    geom, point_gens, line40_gens, _racts, line27_gens, schlafli, names, _singular = v3_module()
    triangles, sixes = object_sets(schlafli)
    tri_gens = [set_action_perm(p, triangles) for p in line27_gens]
    six_gens = [set_action_perm(p, sixes) for p in line27_gens]

    roots = e8_roots()
    a2a = roots[0]
    a2b = next(r for r in roots if ip(a2a, r) == -1)
    e6roots = [r for r in roots if ip(r, a2a) == 0 and ip(r, a2b) == 0]
    assert len(e6roots) == 72
    simple = find_e6_simple_roots(e6roots)
    std240 = [reflection_perm(roots, a) for a in simple]

    root_orbits = []
    unseen = set(range(240))
    while unseen:
        o = orbit(next(iter(unseen)), std240)
        root_orbits.append(o)
        unseen -= set(o)
    orbit_sizes = sorted(len(o) for o in root_orbits)
    assert orbit_sizes == [1]*6 + [27]*6 + [72]
    orbit72 = next(o for o in root_orbits if len(o) == 72)
    orbit27 = next(o for o in root_orbits if len(o) == 27)

    candidate_graphs = []
    for value in (-1, 0, 1):
        G = nx.Graph(); G.add_nodes_from(range(27))
        for i, j in combinations(range(27), 2):
            if ip(roots[orbit27[i]], roots[orbit27[j]]) == value:
                G.add_edge(i, j)
        candidate_graphs.append((value, G))
    value, stdG = next((value, G) for value, G in candidate_graphs if set(dict(G.degree()).values()) == {10})
    mapping = next(nx.algorithms.isomorphism.GraphMatcher(stdG, schlafli).isomorphisms_iter())

    oidx = {x: i for i, x in enumerate(orbit27)}
    std27_raw = [tuple(oidx[p[x]] for x in orbit27) for p in std240]
    std27 = [conjugate_perm(p, mapping, 27) for p in std27_raw]
    e8_gens, words, bfs_states = find_generator_lifts(std27, std240, line27_gens)

    mapped_six_idx = {frozenset(s): i for i, s in enumerate(sixes)}
    e6_to_six = {}
    for ridx in orbit72:
        plus_std = [i for i, widx in enumerate(orbit27) if ip(roots[widx], roots[ridx]) == 1]
        minus_std = [i for i, widx in enumerate(orbit27) if ip(roots[widx], roots[ridx]) == -1]
        assert len(plus_std) == 6 and len(minus_std) == 6
        plus_native = frozenset(mapping[i] for i in plus_std)
        assert plus_native in mapped_six_idx
        e6_to_six[ridx] = mapped_six_idx[plus_native]
    assert len(set(e6_to_six.values())) == 72

    e8root_index72 = {ridx: i for i, ridx in enumerate(orbit72)}
    e8_72_gens = [tuple(e8root_index72[p[x]] for x in orbit72) for p in e8_gens]
    six_to_e8pos = {six: pos for pos, ridx in enumerate(orbit72) for six in [e6_to_six[ridx]]}
    induced_six_gens = []
    for p in e8_gens:
        perm = [0] * 72
        for ridx, six_idx in e6_to_six.items():
            perm[six_idx] = e6_to_six[p[ridx]]
        induced_six_gens.append(tuple(perm))
    assert induced_six_gens == six_gens

    pairs = [(i, j) for i, j in combinations(range(40), 2) if not geom.adjacency[i, j]]
    assert len(pairs) == 540
    pidx = {frozenset(p): i for i, p in enumerate(pairs)}
    pair_gens = [tuple(pidx[frozenset(g[x] for x in pair)] for pair in pairs) for g in point_gens]
    paired = paired_psp_closure(point_gens[:-1], line27_gens[:-1])
    base_pair = frozenset(pairs[0])
    stabilizer48 = [(l, p) for l, p in paired.items() if frozenset(p[x] for x in base_pair) == base_pair]
    assert len(stabilizer48) == 48

    w33_line_rows = list(geom.lines)
    tri_rows = [frozenset(t) for t in triangles]
    root_rows = [frozenset(s) for s in sixes]
    pair_rows = [frozenset(p) for p in pairs]
    equivariance = {
        "W33_point_line": all(incidence_equivariant(w33_line_rows, pg, lg) for pg, lg in zip(point_gens, line40_gens)),
        "line_tritangent": all(incidence_equivariant(tri_rows, lg, tg) for lg, tg in zip(line27_gens, tri_gens)),
        "line_root_six": all(incidence_equivariant(root_rows, lg, rg) for lg, rg in zip(line27_gens, six_gens)),
        "pair_endpoint": all(incidence_equivariant(pair_rows, pg, qg) for pg, qg in zip(point_gens, pair_gens)),
        "root72_in_E8_240": all(all(p[r] in set(orbit72) for r in orbit72) for p in e8_gens),
        "double_six_equals_E6_root_action": induced_six_gens == six_gens,
    }

    inclusion72 = [orbit72[six_to_e8pos[i]] for i in range(72)]
    checks = {
        "e8_roots_240": len(roots) == 240,
        "e6_orthogonal_roots_72": len(e6roots) == 72,
        "e8_W_E6_orbits": orbit_sizes == [1]*6 + [27]*6 + [72],
        "schlafli_27_identified": set(dict(stdG.degree()).values()) == {10},
        "all_native_generators_lift_to_E8": len(e8_gens) == 9,
        "oriented_double_six_root_bijection": len(set(e6_to_six.values())) == 72,
        "all_incidence_squares_commute": all(equivariance.values()),
        "middleware_stabilizer_48": len(stabilizer48) == 48,
        "pair_orbit_540": len(pairs) == 540,
    }

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "objects": {
            "W33_points": 40, "W33_lines": 40, "cubic_lines": 27,
            "tritangent_planes": 45, "E6_roots_oriented_double_sixes": 72,
            "E8_roots": 240, "noncollinear_pairs": 540, "middleware_fiber": 48,
        },
        "E8_decomposition_under_W_E6": {
            "orbit_sizes": orbit_sizes,
            "reading": "72 E6 roots + 6 fixed A2 roots + six minuscule 27-orbits = 240",
            "A2_simple_roots_doubled": [list(a2a), list(a2b)],
            "E6_simple_roots_doubled": [list(x) for x in simple],
        },
        "incidence_equivariance": equivariance,
        "root_map": {
            "pairing_value_for_schlafli_edges": value,
            "E6_root_to_oriented_double_six": {str(k): v for k, v in sorted(e6_to_six.items())},
            "oriented_double_six_to_E8_root_index": inclusion72,
        },
        "generator_lift": {
            "bfs_states_visited": bfs_states,
            "word_lengths": [len(w) for w in words],
            "E8_240_digest": sha256_json(e8_gens),
            "line27_digest": sha256_json(line27_gens),
            "pair540_digest": sha256_json(pair_gens),
        },
        "middleware": {
            "base_pair": sorted(base_pair),
            "stabilizer_order": len(stabilizer48),
            "digest": sha256_json([(l, p) for l, p in stabilizer48]),
        },
        "theorem": (
            "The native PSp(4,3):2 generators define one commuting incidence diagram on 40 points, 40 lines, "
            "27 cubic lines, 45 tritangents, 72 oriented double-sixes/E6 roots, 240 E8 roots, 540 noncollinear pairs, "
            "and the 48-element pair stabilizer. The E8 restriction is 72 + 6 + 6*27, and the root-to-double-six map is pairing-defined."
        ),
    }


def main():
    out = analyze()
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
