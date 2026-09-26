#!/usr/bin/env python3
"""Pass 10977: q=5 Niemeier/600-cell six-carrier lift firewall.

Pass 10970 puts the six A4 components of N(A4^6) on the existing
P1(F5)/Singer six-object carrier. Pass 599 puts that same six-object A5 carrier
on the six fivefold axes of an actual 600-cell vertex figure.

Both constructions also contain a natural 120-object shell. This packet tests
whether that shared cardinality lifts equivariantly. It does not.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "analysis") not in sys.path:
    sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass599_600cell_singer_axis_transport as P599

OUT = ROOT / "data" / "w33_pass10977_q5_niemeier_600cell_lift_firewall.json"
P10970 = ROOT / "data" / "w33_pass10970_projective_clock_code_lattice_tower.json"
P599_CERT = ROOT / "data" / "w33_pass599_600cell_singer_axis_transport.json"
def comp(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inv(p):
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def parity(p):
    return sum(
        p[i] > p[j]
        for i in range(len(p))
        for j in range(i + 1, len(p))
    ) % 2


def cyc5(cycle):
    p = list(range(5))
    for a, b in zip(cycle, cycle[1:] + cycle[:1]):
        p[a] = b
    return tuple(p)


def closure5(gens):
    ident = tuple(range(5))
    group = {ident}
    front = [ident]
    while front:
        a = front.pop()
        for b in gens:
            c = comp(a, b)
            if c not in group:
                group.add(c)
                front.append(c)
    return frozenset(group)
def build_s5_packet():
    s5 = tuple(itertools.permutations(range(5)))
    a5 = tuple(g for g in s5 if parity(g) == 0)
    subgroups = set()
    for tail in itertools.permutations((1, 2, 3, 4)):
        subgroups.add(closure5((cyc5((0,) + tail),)))
    sylow5 = tuple(sorted(subgroups, key=lambda h: sorted(h)))
    assert len(sylow5) == 6
    sid = {h: i for i, h in enumerate(sylow5)}

    def conjugate(g, h):
        gi = inv(g)
        return frozenset(comp(comp(g, x), gi) for x in h)

    def act(g, x):
        s, i, j = x
        return (sid[conjugate(g, sylow5[s])], g[i], g[j])

    singer = frozenset(
        tuple(sid[conjugate(g, h)] for h in sylow5)
        for g in a5
    )
    assert singer == P599.singer_A5()
    return s5, a5, sylow5, act, singer
def orbit(group, action, x):
    return {action(g, x) for g in group}


def permutation_order(p):
    ident = tuple(range(len(p)))
    x = ident
    for n in range(1, 121):
        x = comp(x, p)
        if x == ident:
            return n
    raise AssertionError("order bound")


def root_packet():
    s5, a5, sylow5, action, singer = build_s5_packet()
    roots = tuple(
        (s, i, j)
        for s in range(6)
        for i in range(5)
        for j in range(5)
        if i != j
    )
    assert len(roots) == 120

    base = roots[0]
    s5_orbit = orbit(s5, action, base)
    s5_stab = [g for g in s5 if action(g, base) == base]
    assert len(s5_orbit) == 120 and len(s5_stab) == 1

    unseen = set(roots)
    a5_orbits = []
    while unseen:
        x = min(unseen)
        o = orbit(a5, action, x)
        a5_orbits.append(o)
        unseen -= o
    assert sorted(map(len, a5_orbits)) == [60, 60]
    def antipode(x):
        s, i, j = x
        return (s, j, i)

    assert all(
        all(antipode(x) in o for x in o)
        for o in a5_orbits
    )
    proots = tuple(sorted({min(x, antipode(x)) for x in roots}))

    def act_projective(g, x):
        return min(action(g, x), antipode(action(g, x)))

    unseen = set(proots)
    projective_a5_orbits = []
    while unseen:
        x = min(unseen)
        o = {act_projective(g, x) for g in a5}
        projective_a5_orbits.append(o)
        unseen -= o
    assert sorted(map(len, projective_a5_orbits)) == [30, 30]

    pbase = proots[0]
    assert len({act_projective(g, pbase) for g in s5}) == 60
    projective_s5_stab = sum(
        act_projective(g, pbase) == pbase for g in s5
    )
    assert projective_s5_stab == 2

    s5_order_hist = Counter(permutation_order(g) for g in s5)
    fibres = Counter(s for s, _, _ in roots)
    assert fibres == Counter({i: 20 for i in range(6)})

    return {
        "root_model": "six A4 components, roots e_i-e_j labelled (Singer fibre,i,j)",
        "root_count": len(roots),
        "fibres": 6,
        "roots_per_A4": 20,
        "diagonal_S5_action": {
            "order": len(s5),
            "orbit_size": len(s5_orbit),
            "stabilizer_order": len(s5_stab),
            "regular": True,
            "element_order_histogram": {
                str(k): int(v) for k, v in sorted(s5_order_hist.items())
            },
        },
        "A5_restriction": {
            "order": len(a5),
            "root_orbit_sizes": sorted(map(len, a5_orbits)),
            "each_root_orbit_regular": True,
            "antipode_preserves_each_60_orbit": True,
        },
        "projective_roots": {
            "count": len(proots),
            "A5_orbit_sizes": sorted(map(len, projective_a5_orbits)),
            "A5_stabilizer_order": 2,
            "S5_orbit_size": 60,
            "S5_stabilizer_order": projective_s5_stab,
        },
        "six_fibre_A5_action_order": len(singer),
    }
def fadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def fneg(x):
    return (-x[0], -x[1])


def fsub(x, y):
    return fadd(x, fneg(y))


def fmul(x, y):
    return P599.qmul(x, y)


def qmul4(u, v):
    a, b, c, d = u
    e, f, g, h = v
    return (
        fsub(fsub(fsub(fmul(a, e), fmul(b, f)), fmul(c, g)), fmul(d, h)),
        fadd(fadd(fsub(fmul(a, f), fmul(d, g)), fmul(b, e)), fmul(c, h)),
        fadd(fadd(fsub(fmul(a, g), fmul(b, h)), fmul(c, e)), fmul(d, f)),
        fadd(fadd(fsub(fmul(a, h), fmul(c, f)), fmul(b, g)), fmul(d, e)),
    )


def half(v):
    assert all(a % 2 == 0 and b % 2 == 0 for a, b in v)
    return tuple((a // 2, b // 2) for a, b in v)


def vmul(u, v):
    return half(qmul4(u, v))
def vorder(u, identity):
    x = identity
    for n in range(1, 121):
        x = vmul(x, u)
        if x == identity:
            return n
    raise AssertionError("binary order bound")


def neg4(u):
    return tuple(fneg(x) for x in u)


def canon_pm(u):
    return min(u, neg4(u))


def closure_perm(gens, n):
    ident = tuple(range(n))
    group = {ident}
    front = [ident]
    while front:
        a = front.pop()
        for b in gens:
            c = comp(a, b)
            if c not in group:
                group.add(c)
                front.append(c)
    return group
def derived_order(perms):
    perms = tuple(perms)
    commutators = set()
    for a in perms:
        ai = inv(a)
        for b in perms:
            bi = inv(b)
            commutators.add(comp(comp(comp(a, b), ai), bi))
    return len(closure_perm(tuple(commutators), len(perms[0])))


def cell600_packet():
    vertices = P599.vertices600()
    vset = set(vertices)
    zero = (0, 0)
    identity = ((2, 0), zero, zero, zero)
    assert identity in vset
    assert len(vertices) == 120

    for u in vertices:
        for v in vertices:
            assert vmul(u, v) in vset

    order_hist = Counter(vorder(v, identity) for v in vertices)
    center = [
        u for u in vertices
        if all(vmul(u, v) == vmul(v, u) for v in vertices)
    ]
    assert len(center) == 2
    assert sorted(vorder(u, identity) for u in center) == [1, 2]
    assert order_hist[2] == 1
    pvertices = tuple(sorted({canon_pm(v) for v in vertices}))
    assert len(pvertices) == 60
    pid = {v: i for i, v in enumerate(pvertices)}
    actions = set()
    for g in vertices:
        actions.add(tuple(
            pid[canon_pm(vmul(g, v))]
            for v in pvertices
        ))
    assert len(actions) == 60
    porder_hist = Counter(permutation_order(p) for p in actions)
    assert porder_hist == Counter({1: 1, 2: 15, 3: 20, 5: 24})
    assert derived_order(actions) == 60
    assert len({p[0] for p in actions}) == 60
    assert sum(p[0] == 0 for p in actions) == 1

    return {
        "coordinate_source": "Pass 599 exact Z[phi] 600-cell coordinates",
        "vertices": len(vertices),
        "closed_under_scaled_quaternion_multiplication": True,
        "binary_group": {
            "order": len(vertices),
            "center_order": len(center),
            "involutions": order_hist[2],
            "element_order_histogram": {
                str(k): int(v) for k, v in sorted(order_hist.items())
            },
            "identification": "binary icosahedral group 2.A5",
        },
        "antipodal_quotient": {
            "vertices": len(pvertices),
            "left_action_order": len(actions),
            "regular": True,
            "element_order_histogram": {
                str(k): int(v) for k, v in sorted(porder_hist.items())
            },
            "derived_subgroup_order": derived_order(actions),
            "identification": "A5",
        },
    }


def payload():
    q5 = json.loads(P10970.read_text(encoding="utf-8"))
    p599 = json.loads(P599_CERT.read_text(encoding="utf-8"))
    assert q5["q5"]["identification"] == "Niemeier lattice N(A4^6)"
    assert q5["q5"]["base_root_count"] == 120
    assert q5["q5"]["repo_P1F5_weld"]["six_sylow5_subgroups"] is True
    assert p599["checks"]["axis_action_conjugate_to_Singer"] is True

    roots = root_packet()
    cell = cell600_packet()
    root_hist = roots["diagonal_S5_action"]["element_order_histogram"]
    cell_hist = cell["binary_group"]["element_order_histogram"]
    checks = {
        "q5_parent_is_N_A4_6": q5["q5"]["identification"] == "Niemeier lattice N(A4^6)",
        "q5_parent_has_120_roots": q5["q5"]["base_root_count"] == 120,
        "same_six_Singer_carrier":
            q5["q5"]["repo_P1F5_weld"]["objects"]
            == "six Sylow-5 subgroups of S5",
        "pass599_six_axis_transport":
            p599["checks"]["axis_action_conjugate_to_Singer"] is True,
        "root_packet_6x20": roots["root_count"] == 120 and roots["roots_per_A4"] == 20,
        "root_S5_regular": roots["diagonal_S5_action"]["regular"] is True,
        "root_A5_is_60_plus_60":
            roots["A5_restriction"]["root_orbit_sizes"] == [60, 60],
        "projective_root_A5_is_30_plus_30":
            roots["projective_roots"]["A5_orbit_sizes"] == [30, 30],
        "600_vertices_form_order120_group":
            cell["binary_group"]["order"] == 120,
        "600_binary_group_unique_involution":
            cell["binary_group"]["involutions"] == 1,
        "600_projective_A5_regular":
            cell["antipodal_quotient"]["regular"] is True,
        "600_projective_A5_one_orbit60":
            cell["antipodal_quotient"]["vertices"] == 60,
        "full_120_groups_not_isomorphic": root_hist != cell_hist,
    }
    assert all(checks.values())
    return {
        "schema": "w33.pass10977.q5-niemeier-600cell-lift-firewall.v1",
        "status": "PASS",
        "headline": (
            "The q=5 Niemeier A4^6 shell and the 600-cell share the exact six-object "
            "Singer/icosahedral carrier, but their tempting common 120 count does not "
            "lift equivariantly. The A4^6 roots carry a regular diagonal S5 action; "
            "the exact 600-cell vertices carry the binary icosahedral group 2.A5. "
            "After antipodal quotient the root packet is 30+30 under A5, while the "
            "600-cell quotient is one regular 60-orbit."
        ),
        "coarse_six_object_bridge": {
            "q5_clock_objects": "six P1(F5) coordinates / six Sylow-5 subgroups of S5",
            "niemeier_objects": "six A4 components",
            "600cell_objects": "six fivefold axes in a vertex-figure icosahedron",
            "group": "A5 on six objects; extended to S5=PGL2(5) on the q=5 code carrier",
            "status": "EXACT",
        },
        "niemeier_root_packet": roots,
        "cell600_packet": cell,
        "lift_firewall": {
            "same_cardinality_120": True,
            "root_cover_group": "S5 in the diagonal regular model",
            "cell600_cover_group": "2.A5 under scaled unit-icosian multiplication",
            "root_cover_involutions": int(root_hist["2"]),
            "cell600_cover_involutions": int(cell_hist["2"]),
            "full_120_equivariant_identification": False,
            "projective_root_A5_orbits": [30, 30],
            "projective_600cell_A5_orbits": [60],
            "projective_60_equivariant_identification": False,
            "reason": (
                "orbit/stabilizer data already disagree after quotient: projective "
                "A4^6 roots have two A5 orbits of size 30 with stabilizer C2, while "
                "projective 600-cell vertices are a regular A5-set of size 60"
            ),
        },
        "what_survives": (
            "The meaningful q=5 weld is the six-coordinate P1(F5) carrier, not a "
            "120-point identification. The shared 120 is a secondary shell count "
            "with inequivalent extension data above the same coarse sixfold geometry."
        ),
        "prior_art_boundary": (
            "A4 has 20 roots, N(A4^6) has 120 roots, the 600-cell has 120 vertices, "
            "and its unit-icosian realization is classical. The repository increment "
            "is the explicit Singer-labelled root action, exact orbit census, and "
            "the computational no-go showing the six-object bridge cannot be lifted "
            "to either the 120 shells or their 60-point antipodal quotients."
        ),
        "boundary": (
            "This is a finite root-system/group-action firewall. It does not deny "
            "other correspondences between N(A4^6), H4/600-cell geometry, or modular "
            "constructions; it rules out this natural objectwise lift respecting the "
            "certified Singer A5/S5 actions. No physical identification follows from "
            "the common cardinalities."
        ),
        "checks": checks,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    p = payload()
    text = json.dumps(p, indent=2, sort_keys=True) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text(encoding="utf-8") != text:
            raise SystemExit("certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text, encoding="utf-8")
    print(json.dumps({
        "status": p["status"],
        "root_A5_orbits": p["niemeier_root_packet"]["A5_restriction"]["root_orbit_sizes"],
        "projective_root_A5": p["niemeier_root_packet"]["projective_roots"]["A5_orbit_sizes"],
        "projective_600_A5": [p["cell600_packet"]["antipodal_quotient"]["vertices"]],
        "root_involutions": p["lift_firewall"]["root_cover_involutions"],
        "cell_involutions": p["lift_firewall"]["cell600_cover_involutions"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
