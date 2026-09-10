#!/usr/bin/env python3
"""Exact presentation and normal-subgroup lattice of the Heawood C6 PSp stabilizer.

The companion fingerprint certificate identifies the order-96 stabilizer H as
the mixed index-two kernel inside D8 x S4 with a V4 kernel on the D8 side.
This file turns that fingerprint into an explicit abstract model:

    H = {(d,sigma) in D8 x S4 : chi(d)=sgn(sigma)},
    chi(r^i s^j)=i mod 2.

Because the odd D8 coset contains the reflection t=rs of order two, the fiber
product splits.  Writing

    V = ker chi = <z=r^2, u=s> ~= C2 x C2,

and using the section sigma |-> (t^sgn(sigma), sigma), gives

    H ~= V4 semidirect S4,

where the S4 action factors through sign: even permutations act trivially on
V, while every odd permutation fixes z and sends u -> z u.

The script verifies a four-generator presentation, enumerates every normal
subgroup by normal closures and joins, and freezes the Hasse diagram of the
normal-subgroup lattice.  It also recovers Z(H)=C2 and H'=C2 x A4 of order 24.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, permutations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_heawood_stabilizer96_presentation_lattice.json"

ID4 = (0, 1, 2, 3)


def perm_compose(p, q):
    """p after q."""
    return tuple(p[q[i]] for i in range(4))


def perm_inverse(p):
    out = [0] * 4
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def perm_parity(p):
    inv = 0
    for i, j in combinations(range(4), 2):
        inv ^= int(p[i] > p[j])
    return inv


def perm_order(p):
    x = ID4
    for n in range(1, 25):
        x = perm_compose(p, x)
        if x == ID4:
            return n
    raise AssertionError(p)


def d8_mul(a, b):
    """Multiply r^i s^j * r^k s^l with srs=r^-1."""
    i, j = a
    k, l = b
    return ((i + (-k if j else k)) % 4, (j + l) % 2)


def d8_inv(a):
    i, j = a
    return ((-i) % 4, 0) if j == 0 else (i, 1)


def d8_chi(a):
    return a[0] % 2


def mul(a, b):
    di, dj, p = a
    ei, ej, q = b
    fi, fj = d8_mul((di, dj), (ei, ej))
    return (fi, fj, perm_compose(p, q))


def inv(a):
    i, j, p = a
    di, dj = d8_inv((i, j))
    return (di, dj, perm_inverse(p))


def identity():
    return (0, 0, ID4)


def element_order(x):
    e = identity()
    y = e
    for n in range(1, 97):
        y = mul(x, y)
        if y == e:
            return n
    raise AssertionError(x)


def closure(generators):
    e = identity()
    gens = tuple(dict.fromkeys(generators))
    group = {e}
    q = deque([e])
    while q:
        x = q.popleft()
        for g in gens:
            for y in (mul(g, x), mul(x, g)):
                if y not in group:
                    group.add(y)
                    q.append(y)
    return frozenset(group)


def conjugate(g, x):
    return mul(mul(g, x), inv(g))


def all_group_elements():
    rows = []
    for i in range(4):
        for j in range(2):
            for p in permutations(range(4)):
                p = tuple(p)
                if d8_chi((i, j)) == perm_parity(p):
                    rows.append((i, j, p))
    H = frozenset(rows)
    assert len(H) == 96
    return H


def center(H):
    return frozenset(x for x in H if all(mul(x, y) == mul(y, x) for y in H))


def commutator(a, b):
    return mul(mul(mul(a, b), inv(a)), inv(b))


def derived(H):
    return closure(commutator(a, b) for a in H for b in H)


def normal_closure(H, x):
    return closure(conjugate(g, x) for g in H)


def enumerate_normal_subgroups(H):
    # Every normal subgroup is the join of the normal closures of its elements.
    # Start from the trivial subgroup and close under joins with the finitely many
    # distinct one-element normal closures until no new subgroup appears.
    single = {normal_closure(H, x) for x in H}
    normals = {frozenset({identity()})}
    changed = True
    while changed:
        changed = False
        current = tuple(normals)
        for N in current:
            for C in single:
                J = closure(tuple(N) + tuple(C))
                if J not in normals:
                    normals.add(J)
                    changed = True
    normals.add(H)
    # Exhaustive conjugation firewall.
    for N in normals:
        assert all(conjugate(g, x) in N for g in H for x in N)
    return tuple(normals)


def subgroup_product(A, B):
    return frozenset(mul(a, b) for a in A for b in B)


def projection_s4(N):
    return frozenset(x[2] for x in N)


def projection_d8(N):
    return frozenset((x[0], x[1]) for x in N)


def element_text(x):
    i, j, p = x
    return f"r^{i}s^{j}|{''.join(str(k) for k in p)}"


def set_signature(N):
    return tuple(sorted(element_text(x) for x in N))


def build_result():
    H = all_group_elements()
    e = identity()
    Z = center(H)
    Hp = derived(H)

    s4_all = tuple(tuple(p) for p in permutations(range(4)))
    s4_even = frozenset(p for p in s4_all if perm_parity(p) == 0)
    s4_v4 = frozenset(
        p for p in s4_even
        if perm_order(p) in (1, 2)
    )
    assert len(s4_v4) == 4  # identity + three double transpositions

    V = frozenset((i, j, ID4) for i in (0, 2) for j in (0, 1))
    z = (2, 0, ID4)
    u = (0, 1, ID4)
    t_d8 = (1, 1)  # rs, chi=1 and order two

    def section(p):
        d = t_d8 if perm_parity(p) else (0, 0)
        return (d[0], d[1], p)

    S4 = frozenset(section(p) for p in s4_all)
    A4 = frozenset(section(p) for p in s4_even)
    K4 = frozenset(section(p) for p in s4_v4)

    # Concrete S4 presentation generators a=(01), b=(0123).
    a_perm = (1, 0, 2, 3)
    b_perm = (1, 2, 3, 0)
    a = section(a_perm)
    b = section(b_perm)

    generated = closure((z, u, a, b))
    assert generated == H

    def pow_elem(x, n):
        y = e
        for _ in range(n):
            y = mul(x, y)
        return y

    presentation_relations = {
        "z^2=1": pow_elem(z, 2) == e,
        "u^2=1": pow_elem(u, 2) == e,
        "[z,u]=1": commutator(z, u) == e,
        "a^2=1": pow_elem(a, 2) == e,
        "b^4=1": pow_elem(b, 4) == e,
        "(ab)^3=1": pow_elem(mul(a, b), 3) == e,
        "z_centralizes_a": mul(z, a) == mul(a, z),
        "z_centralizes_b": mul(z, b) == mul(b, z),
        "a_u_a^-1=z*u": conjugate(a, u) == mul(z, u),
        "b_u_b^-1=z*u": conjugate(b, u) == mul(z, u),
        "four_generators_have_order_96": len(generated) == 96,
    }

    split_checks = {
        "V_is_V4": len(V) == 4 and all(element_order(x) <= 2 for x in V),
        "S4_section_has_order_24": len(S4) == 24,
        "section_is_homomorphism": all(section(perm_compose(p, q)) == mul(section(p), section(q)) for p in s4_all for q in s4_all),
        "V_intersection_S4_is_trivial": V & S4 == frozenset({e}),
        "V_times_S4_is_all_H": subgroup_product(V, S4) == H,
        "even_S4_centralizes_V": all(mul(section(p), v) == mul(v, section(p)) for p in s4_even for v in V),
        "odd_S4_fixes_z": all(conjugate(section(p), z) == z for p in s4_all if perm_parity(p)),
        "odd_S4_sends_u_to_zu": all(conjugate(section(p), u) == mul(z, u) for p in s4_all if perm_parity(p)),
    }

    normals = enumerate_normal_subgroups(H)
    normals_sorted = sorted(normals, key=lambda N: (len(N), set_signature(N)))
    nid = {N: f"N{idx:02d}" for idx, N in enumerate(normals_sorted)}

    known = {
        frozenset({e}): "1",
        Z: "Z(H)=C2",
        V: "V4_kernel",
        K4: "S4_normal_V4_section",
        A4: "A4_section",
        Hp: "H_prime=C2_x_A4",
        subgroup_product(V, K4): "V4_kernel_x_V4_section",
        subgroup_product(V, A4): "preimage_A4=V4_x_A4",
        H: "H",
    }

    # A second characteristic order-48 subgroup is Z times the split S4 section.
    ZS4 = subgroup_product(Z, S4)
    if len(ZS4) == 48:
        known[ZS4] = "Z_x_S4_section"

    normal_rows = []
    for N in normals_sorted:
        orders = Counter(element_order(x) for x in N)
        normal_rows.append(
            {
                "id": nid[N],
                "name": known.get(N),
                "order": len(N),
                "contains_center": Z <= N,
                "contains_derived": Hp <= N,
                "contains_V4_kernel": V <= N,
                "intersection_V4_kernel_order": len(N & V),
                "intersection_S4_section_order": len(N & S4),
                "S4_projection_order": len(projection_s4(N)),
                "D8_projection_order": len(projection_d8(N)),
                "element_order_histogram": {str(k): v for k, v in sorted(orders.items())},
            }
        )

    hasse = []
    for A in normals_sorted:
        for B in normals_sorted:
            if A == B or not A < B:
                continue
            if not any(A < C < B for C in normals_sorted):
                hasse.append({"lower": nid[A], "upper": nid[B]})

    order_hist = Counter(len(N) for N in normals_sorted)
    index2 = [N for N in normals_sorted if len(N) == 48]

    # Derived subgroup predicted from the semidirect action: [V,S4]=<z>,
    # S4'=A4, and the two factors commute.
    ZA4 = subgroup_product(Z, A4)

    checks = {
        "H_order_96": len(H) == 96,
        "fiber_product_condition_holds": all(d8_chi((x[0], x[1])) == perm_parity(x[2]) for x in H),
        "all_presentation_relations_hold": all(presentation_relations.values()),
        "all_split_semidirect_checks_hold": all(split_checks.values()),
        "center_is_C2_generated_by_z": Z == frozenset({e, z}),
        "derived_is_Z_times_A4": Hp == ZA4 and len(Hp) == 24,
        "abelianization_is_C2_squared": len(H) // len(Hp) == 4,
        "normal_lattice_contains_trivial_and_full": frozenset({e}) in normals and H in normals,
        "all_enumerated_subgroups_are_normal": all(all(conjugate(g, x) in N for g in H for x in N) for N in normals),
        "exactly_three_index2_normal_subgroups": len(index2) == 3,
        "known_preimage_A4_is_normal": subgroup_product(V, A4) in normals,
        "Z_times_S4_section_is_normal": ZS4 in normals,
    }

    return {
        "schema": "w33.heawood-stabilizer96-presentation-lattice.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The order-96 PSp Heawood-C6 stabilizer is the split fiber product "
            "D8 x_{C2} S4 ~= V4 semidirect S4, with the S4 action factoring "
            "through sign. Even permutations centralize V4; odd permutations "
            "fix z and send u to z*u. The complete normal-subgroup lattice is "
            "enumerated exactly."
        ),
        "fiber_product": {
            "definition": "H={(r^i s^j,sigma) in D8 x S4 : i mod 2 = sgn(sigma)}",
            "D8_character": "chi(r^i s^j)=i mod 2",
            "kernel": "V4=<z=r^2,u=s>",
            "odd_section_element": "t=rs, t^2=1",
            "split_section": "sigma |-> (t^sgn(sigma),sigma)",
            "semidirect_form": "V4 semidirect S4; action factors through sgn:S4->C2",
            "action": "even: u->u,z->z; odd: u->z*u,z->z",
        },
        "presentation": {
            "generators": ["z", "u", "a=(01)", "b=(0123)"],
            "relations_text": [
                "z^2=u^2=a^2=b^4=(ab)^3=1",
                "[z,u]=[z,a]=[z,b]=1",
                "a u a^-1 = z u",
                "b u b^-1 = z u",
            ],
            "relation_checks": presentation_relations,
        },
        "structure": {
            "order": len(H),
            "center_order": len(Z),
            "derived_order": len(Hp),
            "derived_structure": "C2 x A4",
            "abelianization_order": len(H) // len(Hp),
            "abelianization_structure": "C2 x C2",
            "V4_kernel_order": len(V),
            "S4_complement_order": len(S4),
            "A4_section_order": len(A4),
            "S4_normal_V4_section_order": len(K4),
        },
        "normal_subgroup_lattice": {
            "normal_subgroup_count": len(normals_sorted),
            "order_histogram": {str(k): v for k, v in sorted(order_hist.items())},
            "nodes": normal_rows,
            "hasse_edges": hasse,
            "index2_nodes": [nid[N] for N in index2],
        },
        "tomotope_firewall": (
            "This presentation has center C2 and derived subgroup C2 x A4 of "
            "order 24. It therefore remains structurally distinct from the "
            "repo-certified tomotope group with trivial center and derived order 48."
        ),
        "claim_boundary": [
            "The abstract identification uses the prior certificate that the stabilizer is the V4-kernel mixed index-two subgroup of D8 x S4.",
            "The normal-subgroup lattice is exact for this abstract group model; no identification of individual normal subgroups with physical controller subsystems is asserted here.",
        ],
        "checks": checks,
    }


def main():
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "order": result["structure"]["order"],
        "center": result["structure"]["center_order"],
        "derived": result["structure"]["derived_order"],
        "normal_subgroups": result["normal_subgroup_lattice"]["normal_subgroup_count"],
        "normal_order_histogram": result["normal_subgroup_lattice"]["order_histogram"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
