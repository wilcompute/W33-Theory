#!/usr/bin/env python3
"""Passes 7233--7240: correct the boundary of Pass7216's 'general GF(p^k)' claim.

Pass7216 introduced a useful finite-field table constructor.  Its polynomial
selection is mathematically sufficient in extension degrees 2 and 3, because a
quadratic or cubic over a field is reducible iff it has a root.  For k>=4 the
same rootlessness test is not an irreducibility criterion: a polynomial may
factor into higher-degree factors while having no linear factor.

This audit implements the standard finite-field irreducibility criterion:
for monic f of degree k over F_p,

  x^(p^k) = x (mod f)

and for every prime divisor r of k,

  gcd(f, x^(p^(k/r)) - x) = 1.

It then checks the exact extension degrees used by the recent q=4,9,25,27 lanes
and supplies explicit counterexamples to the unrestricted 'general k' wording.
No numerical result from the degree-2/3 lanes is withdrawn.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS7233_7240_FIELD_IRREDUCIBILITY_AUDIT.json"


def trim(a, p):
    a = [int(x) % p for x in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def divmod_poly(a, b, p):
    a = trim(a, p)
    b = trim(b, p)
    if b == [0]:
        raise ZeroDivisionError
    q = [0] * max(1, len(a) - len(b) + 1)
    inv = pow(int(b[-1]), -1, p)
    while a != [0] and len(a) >= len(b):
        c = a[-1] * inv % p
        d = len(a) - len(b)
        q[d] = c
        for i, bi in enumerate(b):
            a[d + i] = (a[d + i] - c * bi) % p
        a = trim(a, p)
    return trim(q, p), trim(a, p)


def gcd_poly(a, b, p):
    a, b = trim(a, p), trim(b, p)
    while b != [0]:
        _, r = divmod_poly(a, b, p)
        a, b = b, r
    if a == [0]:
        return a
    inv = pow(int(a[-1]), -1, p)
    return trim([(inv * x) % p for x in a], p)


def mulmod(a, b, f, p):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] = (c[i + j] + x * y) % p
    return divmod_poly(c, f, p)[1]


def powmod_poly(a, n, f, p):
    out = [1]
    base = trim(a, p)
    while n:
        if n & 1:
            out = mulmod(out, base, f, p)
        base = mulmod(base, base, f, p)
        n //= 2
    return out


def sub_poly(a, b, p):
    n = max(len(a), len(b))
    return trim([
        ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
        for i in range(n)
    ], p)


def prime_divisors(n):
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def modulus_from_rhs(rhs, p):
    """Pass7216 convention x^k = sum rhs[i] x^i -> monic modulus."""
    k = len(rhs)
    return [(-int(rhs[i])) % p for i in range(k)] + [1]


def is_irreducible_rhs(rhs, p):
    k = len(rhs)
    f = modulus_from_rhs(rhs, p)
    x = [0, 1]
    if sub_poly(powmod_poly(x, p ** k, f, p), x, p) != [0]:
        return False
    for r in prime_divisors(k):
        h = sub_poly(powmod_poly(x, p ** (k // r), f, p), x, p)
        if len(gcd_poly(f, h, p)) > 1:
            return False
    return True


def legacy_selector(p, k):
    """Exact rootlessness logic used by Pass7216."""
    for cand in itertools.product(range(p), repeat=k):
        poly = list(cand)
        if k == 2:
            ok = all((r * r - sum(poly[i] * (r ** i) for i in range(k))) % p != 0 for r in range(p))
        elif k == 3:
            ok = all((r ** 3 - sum(poly[i] * (r ** i) for i in range(k))) % p != 0 for r in range(p))
        else:
            ok = all(
                (pow(r, k, p) - sum(poly[i] * pow(r, i, p) for i in range(k))) % p != 0
                for r in range(p)
            )
        if ok:
            return poly
    raise RuntimeError("legacy selector found no candidate")


def rigorous_selector(p, k):
    for cand in itertools.product(range(p), repeat=k):
        # Nonzero constant term is necessary for irreducibility for k>1 and
        # removes obvious x factors early.
        if cand[0] == 0:
            continue
        rhs = list(cand)
        if is_irreducible_rhs(rhs, p):
            return rhs
    raise RuntimeError(f"no irreducible polynomial found over F_{p} of degree {k}")


def main() -> int:
    safe_lanes = []
    for q, p, k in ((4, 2, 2), (9, 3, 2), (25, 5, 2), (27, 3, 3)):
        legacy = legacy_selector(p, k)
        assert is_irreducible_rhs(legacy, p)
        safe_lanes.append({
            "q": q,
            "p": p,
            "k": k,
            "legacy_rhs": legacy,
            "rigorously_irreducible": True,
        })

    # Logical counterexample to 'rootless => irreducible' for degree >= 4:
    # over F2, x^4+x^2+1 = (x^2+x+1)^2 has no roots in F2.
    rootless_reducible_rhs = [1, 0, 1, 0]  # x^4 = 1+x^2 -> x^4+x^2+1
    assert all(
        (pow(r, 4, 2) - sum(rootless_reducible_rhs[i] * pow(r, i, 2) for i in range(4))) % 2 != 0
        for r in range(2)
    )
    assert not is_irreducible_rhs(rootless_reducible_rhs, 2)

    # Stronger implementation-level counterexamples: the exact legacy selector
    # itself chooses reducible moduli for k=5 and k=8 over F2.
    bad = []
    for k in (5, 8):
        legacy = legacy_selector(2, k)
        assert not is_irreducible_rhs(legacy, 2)
        robust = rigorous_selector(2, k)
        assert is_irreducible_rhs(robust, 2)
        bad.append({
            "p": 2,
            "k": k,
            "legacy_rhs": legacy,
            "legacy_is_irreducible": False,
            "rigorous_rhs": robust,
            "rigorous_is_irreducible": True,
        })

    out = {
        "schema": "w33.pass7233_7240.field_irreducibility_audit.v1",
        "status": "PASS",
        "passes": "7233-7240",
        "finding": (
            "Pass7216's rootlessness selector is a valid irreducibility test in degrees 2 and 3, "
            "but not for unrestricted extension degree k>=4."
        ),
        "safe_recent_lanes": safe_lanes,
        "counterexample_rootless_but_reducible": {
            "field": "F2",
            "polynomial": "x^4+x^2+1=(x^2+x+1)^2",
            "pass7216_rootlessness_test": True,
            "rigorous_irreducibility": False,
        },
        "legacy_selector_failures": bad,
        "replacement": (
            "Use Frobenius/Rabin irreducibility: x^(p^k)=x mod f and gcd(f,x^(p^(k/r))-x)=1 "
            "for every prime divisor r of k."
        ),
        "claim_boundary": (
            "The q=4, q=9, q=25 and q=27 finite-field constructions use extension degrees 2 or 3 and survive this audit. "
            "The phrase 'general GF(p^k)' in Pass7216 is withdrawn until its caller is switched to the rigorous selector."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "safe_q": [4, 9, 25, 27], "bad_k": [5, 8]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
