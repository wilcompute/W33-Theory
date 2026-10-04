#!/usr/bin/env python3
"""Passes 3276-3277: independent iterative verifier for the 876-state quotient.

Unlike Pass 3216's recursive-signature constructor, this program:
  1. builds every reachable raw hypothesis subset;
  2. records its Moore output, greedy action and outcome transitions;
  3. computes the coarsest stable partition by iterative label refinement;
  4. repeats discovery in opposite traversal order and compares partitions.

State numbers are deliberately traversal-dependent. The certificate is the
partition of raw subsets and the quotient transition graph, not ROM bytes.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3276_BT3277_INDEPENDENT_CURVATURE_QUOTIENT_results.json"
D4 = [(a, b) for a in range(4) for b in range(2)]
DI = {g: i for i, g in enumerate(D4)}
ONE = (0, 0)
FAULTS = [g for g in D4 if g != ONE]
EDGES = list(itertools.combinations(range(10), 2))
TRIANGLES = list(itertools.combinations(range(10), 3))
FROZEN23 = [(5,6,9),(2,5,9),(4,5,8),(2,4,7),(0,3,6),(0,1,8),
 (1,2,4),(1,3,5),(3,4,8),(0,4,9),(2,3,8),(4,8,9),(1,7,8),
 (1,4,6),(0,2,3),(3,7,9),(1,3,9),(2,6,9),(3,5,7),(0,1,7),
 (3,6,8),(0,4,5),(4,6,7)]
SELECTED = [TRIANGLES.index(t) for t in FROZEN23]
REMAINING = [i for i in range(120) if i not in set(SELECTED)]


def mul(g, h):
    a, b = g; c, d = h
    return ((a + (-1 if b else 1) * c) % 4, (b + d) % 2)


def inv(g):
    a, b = g
    return ((-((-1 if b else 1) * a)) % 4, b)


def directed(edge, g, u, v):
    if (u, v) == edge: return g
    if (v, u) == edge: return inv(g)
    return ONE


def syndrome(hyp):
    out = []
    for i, j, k in TRIANGLES:
        product = ONE
        for u, v in ((i,j),(j,k),(k,i)):
            factor = ONE
            for edge, g in hyp:
                factor = mul(directed(edge, g, u, v), factor)
            product = mul(factor, product)
        out.append(DI[product])
    return tuple(out)


def universe():
    rows = [tuple()]
    rows.extend(((e, g),) for e in EDGES for g in FAULTS)
    rows.extend(((e,g),(f,h)) for e,f in itertools.combinations(EDGES,2) for g in FAULTS for h in FAULTS)
    assert len(rows) == 48_826
    return rows


def curvature(rows):
    measured = set()
    for tri in FROZEN23:
        es = [tuple(sorted(x)) for x in itertools.combinations(tri, 2)]
        measured.update(tuple(sorted(x)) for x in itertools.combinations(es, 2))
    assert len(measured) == 69
    def comm(a,b): return mul(mul(mul(a,b),inv(a)),inv(b))
    labels = []
    for row in rows:
        if len(row) != 2:
            labels.append(0); continue
        (e,a),(f,b) = row
        if tuple(sorted((e,f))) not in measured: labels.append(0)
        else: labels.append(2 if comm(a,b) == (2,0) else 1)
    assert Counter(labels) == Counter({0:45_445,1:1_725,2:1_656})
    return labels


def choose(indices, full):
    best = None
    for t in REMAINING:
        parts = defaultdict(list)
        for i in indices: parts[int(full[i,t])].append(i)
        key = (-len(parts), max(map(len, parts.values())), t)
        if best is None or key < best[0]: best = (key, t, parts)
    return best[1], {o: tuple(v) for o,v in best[2].items()}


def raw_machine(initial, full, labels, reverse=False):
    queue = deque(initial)
    seen = set(initial)
    records = {}
    while queue:
        state = queue.pop() if reverse else queue.popleft()
        hist = Counter(labels[i] for i in state)
        output = (hist[0], hist[1], hist[2])
        if len(state) <= 1:
            records[state] = (True, None, output, {})
            continue
        action, children = choose(state, full)
        records[state] = (False, action, output, children)
        for child in sorted(children.values()):
            if child not in seen:
                seen.add(child); queue.append(child)
    return records


def same_partition(left, right):
    lr = defaultdict(set); rl = defaultdict(set)
    for state in left:
        lr[left[state]].add(right[state])
        rl[right[state]].add(left[state])
    return all(len(x) == 1 for x in lr.values()) and all(len(x) == 1 for x in rl.values())


def refine(records):
    states = sorted(records)
    labels = {s: (records[s][0], records[s][1], records[s][2]) for s in states}
    rounds = 0
    while True:
        palette = {key:i for i,key in enumerate(sorted(set(labels.values()), key=repr))}
        old = {s:palette[labels[s]] for s in states}
        signatures = {}
        for s in states:
            terminal, action, output, children = records[s]
            signatures[s] = (terminal, action, output, tuple(sorted((o, old[ch]) for o,ch in children.items())))
        palette2 = {key:i for i,key in enumerate(sorted(set(signatures.values()), key=repr))}
        new = {s:palette2[signatures[s]] for s in states}
        rounds += 1
        if same_partition(old, new):
            return new, signatures, rounds
        labels = signatures


def canonical_certificate(records, classes):
    members = defaultdict(list)
    for state, cid in classes.items(): members[cid].append(state)
    rows = []
    for cid, group in members.items():
        rep = min(group)
        terminal, action, output, children = records[rep]
        expected = (terminal, action, output, tuple(sorted((o, classes[ch]) for o,ch in children.items())))
        for state in group:
            t,a,out,ch = records[state]
            observed = (t,a,out,tuple(sorted((o,classes[c]) for o,c in ch.items())))
            assert observed == expected
        rows.append({
            "member_count": len(group),
            "terminal": terminal,
            "action": action,
            "output": output,
            "transitions": expected[3],
        })
    rows.sort(key=repr)
    text = json.dumps(rows, sort_keys=True, separators=(",",":"))
    return hashlib.sha256(text.encode()).hexdigest(), rows


def groups(classes):
    result = defaultdict(list)
    for state,cid in classes.items(): result[cid].append(state)
    return result.values()


def main():
    rows = universe()
    full = np.array([syndrome(r) for r in rows], dtype=np.uint8)
    grouped = defaultdict(list)
    for i,key in enumerate(map(tuple,full[:,SELECTED])): grouped[key].append(i)
    initial = [tuple(v) for v in grouped.values() if len(v)>1]
    assert len(grouped) == 46_284 and len(initial) == 1_436 and max(map(len,initial)) == 3
    labels = curvature(rows)

    forward = raw_machine(initial, full, labels, reverse=False)
    reverse = raw_machine(initial, full, labels, reverse=True)
    assert set(forward) == set(reverse)
    cf, sf, rounds_f = refine(forward)
    cr, sr, rounds_r = refine(reverse)
    pf = sorted(tuple(sorted(group)) for group in groups(cf))
    pr = sorted(tuple(sorted(group)) for group in groups(cr))
    assert pf == pr
    assert len(set(cf.values())) == 876
    assert len({cf[s] for s in initial}) == 770
    digest, quotient = canonical_certificate(forward, cf)

    payload = {
        "schema": "w33.pass3276_3277.independent_curvature_quotient.v1",
        "status": "EXACT_ITERATIVE_BISIMULATION_CERTIFICATE",
        "hypotheses": 48_826,
        "base_signatures": 46_284,
        "collision_classes": 1_436,
        "raw_reachable_subsets": len(forward),
        "quotient_states": 876,
        "initial_quotient_states": 770,
        "refinement_rounds_forward": rounds_f,
        "refinement_rounds_reverse": rounds_r,
        "traversal_independent_partition": True,
        "quotient_semantic_sha256": digest,
        "algorithmic_independence": "Build raw subset DAG first, then iterate Moore partition refinement to a fixed point. No recursive signatures, canonical ROM IDs, or ROM-byte comparison are used.",
        "boundary": "Exact for the same frozen noiseless greedy sensing policy. It verifies behavioral quotient equivalence, not noisy posterior equivalence, synthesis, placement, or physical sensing performance.",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"raw":len(forward),"quotient":876,"initial":770,"sha256":digest}, sort_keys=True))


if __name__ == "__main__":
    main()
