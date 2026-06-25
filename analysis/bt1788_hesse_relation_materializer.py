#!/usr/bin/env python3
"""BT1788: Hesse relation materializer and counts-only falsifier.

BT1784/BT1787 left the exact frontier: 9 variables, 12 values, 18 ternary
constraints, 9980 accepted local triples, but no accepted tuple lists.  This builds
that Hesse CSP schema, uses NetworkX to expose the K_{3,3,3} primal graph, then
creates deterministic same-count synthetic tuple materializations to prove that
counts+unary support cannot certify uniqueness.

Synthetic tables are not claimed to be the true BT1781 tables; they are a falsifier
and a scaffold for the real tuple materializer.
"""
from __future__ import annotations

import hashlib, json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1788_hesse_relation_materializer.json"
DOMAIN = tuple(range(12))
COUNTS = [528,562,578,528,612,580,528,528,480,528,612,564,562,528,578,562,562,560]
VARS = [f"R{i}" for i in range(3)] + [f"C{i}" for i in range(3)] + [f"D{i}" for i in range(3)]


def constraints():
    # Hesse nonconcurrency: omit the 9 affine incidences s=(j-i) mod 3.
    return [(f"R{i}", f"C{j}", f"D{s}") for i in range(3) for j in range(3) for s in range(3) if s != (j-i) % 3]


def score(seed, ti, t):
    return hashlib.sha256(f"BT1788|{seed}|{ti}|{t}".encode()).hexdigest()


def relation(seed, ti, count):
    rel = {(0,0,0)}  # incumbent
    # Unary support without creating coordinate-axis free solutions.
    for x in DOMAIN:
        if x == 0: continue
        a = 1 + ((seed + 3*ti + 2*x) % 11)
        b = 1 + ((2*seed + 5*ti + 3*x) % 11)
        c = 1 + ((3*seed + 7*ti + 5*x) % 11)
        rel.update({(x,a,b), (a,x,c), (b,c,x)})
    triples = list(product(DOMAIN, repeat=3))
    triples.sort(key=lambda t: score(seed, ti, t))
    for t in triples:
        if len(rel) >= count: break
        rel.add(t)
    assert len(rel) == count and (0,0,0) in rel
    assert all({t[p] for t in rel} == set(DOMAIN) for p in range(3))
    return rel


def pair_consistency(cons, rels):
    pair_refs = defaultdict(list)
    for ci, tri in enumerate(cons):
        for a,b in combinations(range(3), 2):
            pair = tuple(sorted((tri[a], tri[b])))
            pair_refs[pair].append((ci, (a,b) if pair == (tri[a],tri[b]) else (b,a)))
    rels = [set(r) for r in rels]
    passes, changed = 0, True
    while changed:
        changed, passes = False, passes + 1
        for refs in pair_refs.values():
            inter = None
            for ci,(a,b) in refs:
                proj = {(t[a],t[b]) for t in rels[ci]}
                inter = proj if inter is None else inter & proj
            for ci,(a,b) in refs:
                before = len(rels[ci])
                rels[ci] = {t for t in rels[ci] if (t[a],t[b]) in inter}
                changed |= len(rels[ci]) != before
        if passes > 20: raise RuntimeError("pair consistency did not stabilize")
    sizes = {}
    for pair, refs in pair_refs.items():
        inter = None
        for ci,(a,b) in refs:
            proj = {(t[a],t[b]) for t in rels[ci]}
            inter = proj if inter is None else inter & proj
        sizes["-".join(pair)] = len(inter)
    return rels, {
        "passes": passes,
        "tuple_count_after": sum(map(len, rels)),
        "empty_tables": [i for i,r in enumerate(rels) if not r],
        "pair_frontier_count": len(pair_refs),
        "pair_projection_size_min": min(sizes.values()),
        "pair_projection_size_max": max(sizes.values()),
        "pair_projection_size_histogram": dict(sorted(Counter(sizes.values()).items())),
    }


def supports(rels):
    out = []
    for rel in rels:
        sup = defaultdict(set)
        for t in rel:
            for mask in range(1,8):
                sup[mask].add(tuple(t[p] for p in range(3) if mask & (1<<p)))
        out.append(sup)
    return out


def count_solutions(cons, rels, cap=1000):
    sup, incident = supports(rels), defaultdict(list)
    for ci, tri in enumerate(cons):
        for v in tri: incident[v].append(ci)
    values = [0] + [x for x in DOMAIN if x]
    assign, examples, branch_hist = {}, [], Counter()
    count = visits = 0
    def ok(ci):
        tri, mask, key = cons[ci], 0, []
        for p,v in enumerate(tri):
            if v in assign:
                mask |= 1<<p; key.append(assign[v])
        return mask == 0 or tuple(key) in sup[ci][mask]
    def dfs():
        nonlocal count, visits
        if count >= cap: return
        if len(assign) == len(VARS):
            count += 1
            if len(examples) < 3: examples.append(dict(sorted(assign.items())))
            return
        best_v = best_vals = None
        for v in VARS:
            if v in assign: continue
            vals = []
            for x in values:
                assign[v] = x
                if all(ok(ci) for ci in incident[v]): vals.append(x)
                del assign[v]
            if best_vals is None or len(vals) < len(best_vals):
                best_v, best_vals = v, vals
                if len(vals) <= 1: break
        branch_hist[len(best_vals)] += 1
        for x in best_vals:
            assign[best_v] = x; visits += 1
            dfs()
            del assign[best_v]
            if count >= cap: return
    dfs()
    return {"solutions_counted": count, "hit_cap": count >= cap, "nodes_visited": visits,
            "branch_histogram": dict(sorted(branch_hist.items())), "first_examples": examples}


def run(seed, cons):
    rels = [relation(seed, i, c) for i,c in enumerate(COUNTS)]
    rels2, pc = pair_consistency(cons, rels)
    return {"seed": seed, "pair_consistency": pc, "dfs": count_solutions(cons, rels2),
            "after_counts": [len(r) for r in rels2]}


def main():
    cons = constraints()
    G, B = nx.Graph(), nx.Graph()
    G.add_nodes_from(VARS)
    B.add_nodes_from(VARS, kind="variable")
    for ci, tri in enumerate(cons):
        B.add_node(f"T{ci:02d}", kind="constraint")
        for a,b in combinations(tri,2): G.add_edge(a,b)
        for v in tri: B.add_edge(v, f"T{ci:02d}")
    tw, _ = nx.approximation.treewidth_min_fill_in(G)
    runs = [run(seed, cons) for seed in range(8)]
    sol = [r["dfs"]["solutions_counted"] for r in runs]
    after = [r["pair_consistency"]["tuple_count_after"] for r in runs]
    payload = {
        "bt": "BT1788",
        "title": "Hesse relation materializer and counts-only falsifier",
        "status": "synthetic scaffold; not the real BT1781 tuple data",
        "schema": {"variables": VARS, "domain_size": 12, "constraints": [list(t) for t in cons],
                   "constraint_count": len(cons), "counts": COUNTS, "raw_entries": 18*12**3,
                   "accepted_entries": sum(COUNTS), "nonconcurrency_rule": "s != (j-i) mod 3"},
        "networkx_graph_stats": {"primal_nodes": G.number_of_nodes(), "primal_edges": G.number_of_edges(),
            "primal_degree_sequence": sorted(dict(G.degree()).values()),
            "is_complete_tripartite_K333": G.number_of_edges()==27 and set(dict(G.degree()).values())=={6},
            "approx_treewidth_min_fill": tw, "incidence_nodes": B.number_of_nodes(),
            "incidence_edges": B.number_of_edges(), "incidence_connected": nx.is_connected(B),
            "pair_frontier_count": len({tuple(sorted(p)) for t in cons for p in combinations(t,2)})},
        "same_counts_synthetic_runs": runs,
        "falsifier_summary": {"same_counts": COUNTS, "all_runs_keep_incumbent": all(x>=1 for x in sol),
            "solution_count_min": min(sol), "solution_count_max": max(sol),
            "solution_count_histogram": dict(sorted(Counter(sol).items())),
            "pair_consistency_tuple_count_min": min(after), "pair_consistency_tuple_count_max": max(after),
            "conclusion": "Counts+unary support do not determine the global solve; commit the 18 tuple lists or 27 pair-frontier projections."}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(json.dumps(payload["falsifier_summary"], indent=2, sort_keys=True))


if __name__ == "__main__": main()
