#!/usr/bin/env python3
"""No-go: the 216 sentinel circuits are not an internal qutrit-Clifford torsor.

The preceding sentinel-shell theorem produces 216 five-circuits with
stabilizer S5 in PSp(4,3).  Since the project also contains the projective
single-qutrit Clifford group of order 216, it is tempting to identify the
circuit set with a regular Clifford orbit.  This script tests the strongest
internal version of that idea.

It constructs representatives of both order-216 subgroup classes of
PSp(4,3) in the native W33 coordinates:

  H_point = derived subgroup of a point stabilizer (order 216),
  H_pair  = stabilizer of a perfect matching on a W33 line (order 216).

Their normalizers have orders 648 and 216, hence conjugacy-class lengths 40
and 120, matching the two order-216 classes in the published subgroup lattice.
Neither is transitive on the 216 five-circuits.

It also reconstructs the central C3 of the order-648 point stabilizer.  The
known projective qutrit Clifford is the quotient point_stabilizer/C3.  Each
nontrivial central element acts on the 216 circuits as 72 disjoint 3-cycles,
so the C3 does not act trivially and the quotient action cannot descend to the
circuit orbit.

Boundary: the script proves an internal-action no-go.  It does not rule out an
external, non-PSp-equivariant bijection or a different representation of the
Clifford group on a 216-element set.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260829_216_CLIFFORD_TORSOR_NOGO.json"


def norm(v):
    i = next(k for k, x in enumerate(v) if x % 3)
    z = pow(v[i] % 3, -1, 3)
    return tuple((z * x) % 3 for x in v)


def form(u, v):
    return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % 3


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(q)))


def invperm(p):
    q = [0] * len(p)
    for i, j in enumerate(p):
        q[j] = i
    return tuple(q)


def porder(p):
    seen = set(); out = 1
    for i in range(len(p)):
        if i in seen:
            continue
        j = i; n = 0
        while j not in seen:
            seen.add(j); n += 1; j = p[j]
        out = math.lcm(out, n)
    return out


def geometry():
    pts = sorted({norm(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    idx = {v: i for i, v in enumerate(pts)}
    lines = set()
    for a, b in itertools.combinations(range(40), 2):
        if form(pts[a], pts[b]):
            continue
        S = set()
        for s, t in itertools.product(range(3), repeat=2):
            if s == t == 0:
                continue
            S.add(idx[norm(tuple((s * pts[a][k] + t * pts[b][k]) % 3 for k in range(4)))])
        if len(S) == 4:
            lines.add(tuple(sorted(S)))
    lines = sorted(lines)
    assert len(pts) == len(lines) == 40
    N = [[0] * 40 for _ in range(40)]
    for li, L in enumerate(lines):
        for p in L:
            N[li][p] = 1
    return pts, idx, lines, N


def supports_from_N(N):
    cols = [tuple(N[l][p] for l in range(40)) for p in range(40)]
    sig = defaultdict(list)
    for S in itertools.combinations(range(40), 4):
        z = tuple(sum(cols[p][l] for p in S) for l in range(40))
        sig[z].append(S)
    pairs = sorted(
        tuple(sorted((tuple(v[0]), tuple(v[1]))))
        for v in sig.values() if len(v) == 2
    )
    assert len(pairs) == 45
    supports = [frozenset(set(a) | set(b)) for a, b in pairs]
    masks = [sum(1 << i for i in S) for S in supports]
    return supports, masks


def closure_paired(g40s, g45s):
    e40 = tuple(range(40)); e45 = tuple(range(45))
    G = {(e40, e45)}; Q = deque([(e40, e45)])
    while Q:
        a40, a45 = Q.popleft()
        for g40, g45 in zip(g40s, g45s):
            h = (compose(g40, a40), compose(g45, a45))
            if h not in G:
                G.add(h); Q.append(h)
    return sorted(G)


def closure(gens, n, limit=None):
    e = tuple(range(n)); H = {e}; Q = deque([e])
    while Q:
        a = Q.popleft()
        for g in gens:
            h = compose(g, a)
            if h not in H:
                H.add(h); Q.append(h)
                if limit is not None and len(H) > limit:
                    raise AssertionError("subgroup exceeded expected order")
    return H


def deterministic_generators(H, n):
    gens = []; K = {tuple(range(n))}
    for g in sorted(H):
        if g in K:
            continue
        gens.append(g)
        K = closure(gens, n, len(H))
        if len(K) == len(H):
            break
    assert K == set(H)
    return gens


def comm(a, b):
    return compose(invperm(a), compose(invperm(b), compose(a, b)))


def derived_subgroup(H, n):
    gensH = deterministic_generators(H, n)
    gens = [comm(a, b) for a in gensH for b in gensH]
    gens = [g for g in gens if g != tuple(range(n))]
    while True:
        K = closure(gens, n, len(H))
        extra = []
        for k in gens:
            for s in gensH:
                c = compose(invperm(s), compose(k, s))
                if c not in K:
                    extra.append(c)
        if not extra:
            return K
        gens.extend(extra)


def normalizer_size(G, H, n):
    H = set(H)
    gens = deterministic_generators(H, n)
    count = 0
    for g in G:
        gi = invperm(g)
        if all(compose(gi, compose(h, g)) in H for h in gens):
            count += 1
    return count


def cycle_shape(p):
    seen = set(); C = Counter()
    for i in range(len(p)):
        if i in seen:
            continue
        j = i; n = 0
        while j not in seen:
            seen.add(j); n += 1; j = p[j]
        C[n] += 1
    return dict(sorted(C.items()))


def main():
    pts, idx, lines, N = geometry()
    supports, masks = supports_from_N(N)

    circuits = []
    for C in itertools.combinations(range(45), 5):
        w = 0
        for i in C:
            w ^= masks[i]
        if w == 0:
            circuits.append(C)
    assert len(circuits) == 216
    circuit_index = {C: i for i, C in enumerate(circuits)}

    # Native transvections and one deterministic generating four-tuple.
    gens40 = []
    for v in pts:
        for alpha in (1, 2):
            p = []
            for x in pts:
                z = alpha * form(x, v) % 3
                y = norm(tuple((x[k] + z * v[k]) % 3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    si = {S: i for i, S in enumerate(supports)}
    gens45 = []
    for p in gens40:
        gens45.append(tuple(si[frozenset(p[x] for x in S)] for S in supports))
    chosen = (18, 62, 77, 10)
    Gpaired = closure_paired([gens40[i] for i in chosen], [gens45[i] for i in chosen])
    assert len(Gpaired) == 25920
    G45 = [p45 for _, p45 in Gpaired]

    def act_circuit(i, g):
        return circuit_index[tuple(sorted(g[x] for x in circuits[i]))]

    def orbit(H, seed):
        return {act_circuit(seed, g) for g in H}

    def orbit_partition(H):
        rem = set(range(216)); sizes = []
        while rem:
            s = min(rem); O = orbit(H, s)
            sizes.append(len(O)); rem -= O
        return sorted(sizes, reverse=True)

    # Class 10 in Connor-Leemans: 3^(1+2):Q8, length 40.  It is the derived
    # subgroup of the order-648 point stabilizer.
    point_stab_pairs = [(p40, p45) for p40, p45 in Gpaired if p40[0] == 0]
    assert len(point_stab_pairs) == 648
    point_stab = {p45 for _, p45 in point_stab_pairs}
    H_point = derived_subgroup(point_stab, 45)
    assert len(H_point) == 216
    assert normalizer_size(G45, H_point, 45) == 648
    assert orbit_partition(H_point) == [108, 36, 36, 36]

    # Class 11 in Connor-Leemans: the second order-216 class, length 120.
    # In native W33 coordinates it is obtained by stabilizing a perfect
    # matching of the four points on a line inside that line's order-648
    # stabilizer.
    L = tuple(lines[0]); Lset = set(L)
    line_stab_pairs = [
        (p40, p45) for p40, p45 in Gpaired
        if {p40[x] for x in Lset} == Lset
    ]
    assert len(line_stab_pairs) == 648
    matching = {frozenset((L[0], L[1])), frozenset((L[2], L[3]))}
    H_pair = set()
    for p40, p45 in line_stab_pairs:
        image = {frozenset(p40[x] for x in e) for e in matching}
        if image == matching:
            H_pair.add(p45)
    assert len(H_pair) == 216
    assert normalizer_size(G45, H_pair, 45) == 216
    assert orbit_partition(H_pair) == [108, 36, 27, 27, 18]

    # The center of the 648 point stabilizer is C3.  The projective one-qutrit
    # Clifford is the quotient by this center, but the center is not in the
    # kernel of the circuit action.
    pgens = deterministic_generators(point_stab, 45)
    center = [
        z for z in point_stab
        if all(compose(z, g) == compose(g, z) for g in pgens)
    ]
    assert len(center) == 3
    assert Counter(porder(z) for z in center) == Counter({1: 1, 3: 2})
    e45 = tuple(range(45))
    central_shapes = []
    for z in center:
        if z == e45:
            continue
        pc = tuple(act_circuit(i, z) for i in range(216))
        assert cycle_shape(pc) == {3: 72}
        central_shapes.append(cycle_shape(pc))

    out = {
        "schema": "w33.20260829.216-clifford-torsor-nogo.v1",
        "status": "PASS",
        "circuitOrbit": {
            "size": 216,
            "stabilizer": "S5",
            "ambientGroup": "PSp(4,3)",
            "ambientOrder": 25920,
        },
        "order216Subgroups": [
            {
                "construction": "derived subgroup of a point stabilizer",
                "order": 216,
                "normalizerOrder": 648,
                "conjugacyClassLength": 40,
                "publishedClass": "3^(1+2):Q8",
                "circuitOrbitSizes": [108, 36, 36, 36],
                "transitive": False,
            },
            {
                "construction": "perfect-matching stabilizer inside a W33-line stabilizer",
                "order": 216,
                "normalizerOrder": 216,
                "conjugacyClassLength": 120,
                "publishedClass": "second order-216 class (Connor-Leemans class 11)",
                "circuitOrbitSizes": [108, 36, 27, 27, 18],
                "transitive": False,
            },
        ],
        "exhaustion": "Connor-Leemans subgroup lattice lists exactly these two conjugacy classes of order 216; therefore no order-216 subgroup of PSp(4,3) is transitive on the 216 circuits.",
        "qutritCliffordQuotient": {
            "pointStabilizerOrder": 648,
            "center": "C3",
            "quotientOrder": 216,
            "knownQuotient": "projective one-qutrit Clifford / Hessian ASL(2,3)",
            "nontrivialCenterCycleShapeOnCircuits": {"3": 72},
            "fixedCircuitsPerNontrivialCenterElement": 0,
            "descendsToCircuitAction": False,
        },
        "theorem": "The 216 five-circuit set is not a regular orbit for any internal order-216 subgroup of PSp(4,3), and the point-stabilizer Clifford quotient does not act on it because its central C3 is not in the action kernel.",
        "boundary": "This rules out the natural internal/torsor identification only. It does not forbid an external non-equivariant bijection or another representation of the qutrit Clifford group.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "Hpoint": [108, 36, 36, 36],
        "Hpair": [108, 36, 27, 27, 18],
        "center": "72x3-cycles",
        "regular216": False,
    }))


if __name__ == "__main__":
    main()
