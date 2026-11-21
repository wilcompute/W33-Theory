#!/usr/bin/env python3
"""Odd/even characteristic geometry behind the natural H(q) -> W(5,q) projection.
Finite mathematical certificate, not a physical quantum-computing implementation.
Standalone standard-library script: python analysis/toe_20261121_orthogonal_projection_reflection.py
"""
from __future__ import annotations
from collections import Counter
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/toe_20261121_orthogonal_projection_reflection.json"


def canonical(v, p):
    j = next(i for i, a in enumerate(v) if a % p)
    t = pow(int(v[j]), -1, p)
    return tuple((int(a) * t) % p for a in v)


def quadratic(v, p):
    return (-v[0] * v[0] - sum(v[i] * v[i + 3] for i in (1, 2, 3))) % p


def polar(x, y, p):
    z = tuple((a + b) % p for a, b in zip(x, y))
    return (quadratic(z, p) - quadratic(x, p) - quadratic(y, p)) % p


def point_sets(p):
    pg = sorted({canonical(v, p) for v in product(range(p), repeat=7) if any(v)})
    quad = [v for v in pg if quadratic(v, p) == 0]
    assert len(pg) == (p**7 - 1) // (p - 1)
    assert len(quad) == (p**6 - 1) // (p - 1)
    return pg, quad


def projection(x, c, p):
    j = next(i for i, a in enumerate(c) if a)
    t = x[j] * pow(c[j], -1, p) % p
    return canonical(tuple((a - t * b) % p for a, b in zip(x, c)), p)


def reflection(x, c, p):
    assert p % 2 and quadratic(c, p)
    t = polar(x, c, p) * pow(quadratic(c, p), -1, p) % p
    return canonical(tuple((a - t * b) % p for a, b in zip(x, c)), p)


def theoretical_counts(p):
    assert p % 2
    n = (p**6 - 1) // (p - 1)
    plus = (p**2 + 1) * (p**2 + p + 1)
    minus = (p**3 + 1) * (p + 1)
    assert plus - minus == 2 * p**2
    assert (n - plus) // 2 == (p**5 - p**2) // 2
    assert (n - minus) // 2 == (p**5 + p**2) // 2
    return {"null_points": n,
            "plus": {"tangent": plus, "double": (n - plus) // 2,
                     "image": (n + plus) // 2},
            "minus": {"tangent": minus, "double": (n - minus) // 2,
                      "image": (n + minus) // 2}}


def verify_odd_center(c, quad, p):
    q_c = quadratic(c, p)
    assert q_c
    sections = sum(polar(x, c, p) == 0 for x in quad)
    seen = set()
    orbit = Counter()
    image_fibers = Counter()
    nonorthogonal_collisions = 0
    for x in quad:
        y = reflection(x, c, p)
        assert quadratic(y, p) == 0
        assert reflection(y, c, p) == x
        assert projection(x, c, p) == projection(y, c, p)
        image_fibers[projection(x, c, p)] += 1
        if x not in seen:
            seen.add(x)
            seen.add(y)
            orbit[1 if y == x else 2] += 1
            if y != x:
                assert polar(x, y, p) != 0
                nonorthogonal_collisions += 1
    assert len(seen) == len(quad)
    assert orbit[1] == sections
    assert orbit[2] * 2 + orbit[1] == len(quad)
    assert Counter(image_fibers.values()) == orbit
    typ = "plus" if sections == theoretical_counts(p)["plus"]["tangent"] else "minus"
    assert sections == theoretical_counts(p)[typ]["tangent"]
    assert orbit[2] == theoretical_counts(p)[typ]["double"]
    return {"form_type": typ, "section_points": sections,
            "singleton_fibers": orbit[1], "doubleton_fibers": orbit[2],
            "distinct_images": len(image_fibers),
            "paired_points_nonorthogonal": nonorthogonal_collisions}


def audit_odd(p, exhaustive=False):
    pg, quad = point_sets(p)
    center_counts = Counter()
    reps = {}
    for c in pg:
        value = quadratic(c, p)
        if not value:
            continue
        sign = "square" if pow(value, (p - 1) // 2, p) == 1 else "nonsquare"
        center_counts[sign] += 1
        reps.setdefault(sign, c)
    assert sum(center_counts.values()) == p**6
    checked = {label: verify_odd_center(c, quad, p) for label, c in reps.items()}
    assert {r["form_type"] for r in checked.values()} == {"plus", "minus"}
    if exhaustive:
        assert p == 3
        sections = Counter()
        for c in pg:
            if quadratic(c, p):
                sections[sum(polar(x, c, p) == 0 for x in quad)] += 1
        assert sections == {112: 351, 130: 378}
    return {"field": p, "anisotropic_centers": dict(center_counts),
            "isotropic_centers": len(quad), "theory": theoretical_counts(p),
            "representative_reflection_checks": checked,
            "exhaustive_all_center_tangent_check": bool(exhaustive)}


def audit_even_two():
    p = 2
    pg, quad = point_sets(p)
    nucleus = (1, 0, 0, 0, 0, 0, 0)
    assert quadratic(nucleus, p) == 1
    assert all(polar(nucleus, v, p) == 0 for v in pg)
    assert all(polar(v, v, p) == 0 for v in pg)
    images = {projection(v, nucleus, p) for v in quad}
    assert len(images) == len(quad) == 63
    # In characteristic two, x_0^2 = u.v has one solution for any quotient
    # direction, and the induced polar form is alternating and nondegenerate.
    return {"field": 2, "null_points": len(quad), "projected_points": len(images),
            "nucleus_in_polar_radical": True, "induced_alternating_form": True,
            "bijective_nucleus_projection": True}


def audit_even_four():
    """Independent nucleus lift for GF(4), using alpha^2=alpha+1."""
    def mul(a, b):
        a0, a1 = a & 1, (a >> 1) & 1
        b0, b1 = b & 1, (b >> 1) & 1
        return ((a0 & b0) ^ (a1 & b1)) | (((a0 & b1) ^ (a1 & b0) ^ (a1 & b1)) << 1)

    def dot(u, v):
        z = 0
        for a, b in zip(u, v):
            z ^= mul(a, b)
        return z

    def norm(v):
        return mul(v[0], v[0]) ^ dot(v[1:4], v[4:7])

    def cn(v):
        z = next(a for a in v if a)
        inv = mul(z, z)  # all nonzero GF(4) elements have order three
        return tuple(mul(a, inv) for a in v)

    quotient = sorted({cn(v) for v in product(range(4), repeat=6) if any(v)})
    assert len(quotient) == (4**6 - 1) // 3 == 1365
    lifted = set()
    for u in quotient:
        b = dot(u[:3], u[3:])
        a = mul(b, b)  # unique square root b^(2), since b^(4)=b
        x = (a,) + u
        assert norm(x) == 0
        lifted.add(cn(x))
    assert len(lifted) == len(quotient)
    e = [tuple(int(j == i) for j in range(6)) for i in range(6)]
    def symp(u, v):
        return dot(u[:3], v[3:]) ^ dot(v[:3], u[3:])
    assert all(symp(u, u) == 0 for u in quotient)
    assert all(any(symp(u, basis) for basis in e) for u in quotient)
    return {"field": 4, "null_points": len(lifted),
            "projected_points": len(quotient),
            "unique_frobenius_square_root": True,
            "symplectic_form_alternating_nondegenerate": True,
            "bijective_nucleus_projection": True}


def run(write=True):
    data = {"schema": "toe.20261121.odd_even_orthogonal_projection.v1",
            "status": "PASS",
            "even_q2": audit_even_two(),
            "even_q4": audit_even_four(),
            "odd_q3": audit_odd(3, exhaustive=True),
            "odd_q5": audit_odd(5, exhaustive=False),
            "general_odd_q": "Every anisotropic-center fiber is an orthogonal-reflection orbit; branch Q+ or Q-; double fibers (q^5 -/+ q^2)/2.",
            "general_even_q": "Polar-form nucleus and bijective projection using unique Frobenius square root.",
            "boundary": "Ambient orthogonal projection only; no incidence-preserving hexagon to Pauli intertwiner and no physical TOE."}
    if write:
        OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "q2": data["even_q2"],
                      "q3": data["odd_q3"]["representative_reflection_checks"],
                      "q5": data["odd_q5"]["representative_reflection_checks"]}, sort_keys=True))
    return data


if __name__ == "__main__":
    run()
