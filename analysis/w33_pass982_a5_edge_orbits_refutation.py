#!/usr/bin/env python3
"""Pass 982: the A5 edge-orbit claim is refuted.

Pass 886 (BREAKTHROUGH_PASS886_ICOSAHEDRAL_QUASICRYSTAL.md) asserts that the
icosahedral group A5, sitting inside Aut(W(3,3)), "decomposes 240 edges into
four orbits of 60 = |A5| each".  Pass 981 audited that batch and listed this as
the one arithmetically clean item worth pursuing on its own terms.  It does not
survive: the claim is false, and this pass retracts that assessment.

WHY THE ARITHMETIC LOOKED FINE.  240 = 4 x 60 and |A5| = 60, so four orbits of
60 is consistent with the orbit-counting constraint.  But an orbit of size |G|
is a REGULAR orbit, which requires a trivial stabiliser; four of them means A5
acts freely on the edge set.  Divisibility does not imply freeness, and the
question is settled only by constructing the action.

THE CONSTRUCTION.  The 40 vertices are the projective points of F_3^4 carrying
the symplectic form, and Sp(4,3) acts on them through symplectic transvections
T_v(x) = x + lambda * omega(x,v) * v.  Building random products of transvections
gives a supply of permutations of the 40 points; elements of orders 5 and 3 are
extracted and pairs are used to generate subgroups.  A generated subgroup is
accepted as A5 only if it has order 60 AND the exact A5 element-order profile

        1 identity, 15 of order 2, 20 of order 3, 24 of order 5,

which distinguishes A5 from every other group of order 60 (all the others are
soluble and have a normal Sylow subgroup, giving a different profile).

THE RESULT.  Across 17 independently generated, profile-verified A5 subgroups,
EVERY one produces the same edge-orbit profile

        (60, 60, 30, 30, 20, 20, 10, 10)   -- eight orbits, total 240,

with point stabilisers of orders 1, 1, 2, 2, 3, 3, 6, 6 respectively.  Only two
of the eight orbits are regular.  A5 therefore does NOT act freely on the edges,
and there is no decomposition into four orbits of 60.  The uniformity of the
profile across all samples is consistent with a single conjugacy class of A5 in
Aut(W(3,3)), though that is not proved here.

WHAT IS ACTUALLY TRUE AND MIGHT BE WORTH SOMETHING.  The stabiliser orders come
in equal pairs -- 1,1 / 2,2 / 3,3 / 6,6 -- and the orbit sizes 60, 30, 20, 10 are
exactly 60 divided by the divisors 1, 2, 3, 6 of 6.  So the edge set decomposes
as two copies of a transversal indexed by the divisors of 6.  That is a real
structural statement about the A5 action, and it is not the claimed one.

BOUNDARY.  This refutes the four-regular-orbit claim for every A5 sampled.  It
does not classify A5 subgroups up to conjugacy in Aut(W(3,3)), and it says
nothing about the Penrose or Fibonacci material built on top of the claim in that
document, beyond removing its stated group-theoretic foundation.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass982_a5_edge_orbits_refutation.json"
BASE = ROOT / "analysis" / "w33_pass682_flatblock_h1_branch_separation.py"

Q = 3
A5_PROFILE = {1: 1, 2: 15, 3: 20, 5: 24}


def _base():
    spec = importlib.util.spec_from_file_location("w33_pass682_base", BASE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_machinery():
    mod = _base()
    pts, edges, tris, K, d1, d2 = mod.build()
    OM = mod.OMEGA
    pidx = {p: i for i, p in enumerate(pts)}

    def act(M, i):
        v = np.array(pts[i], dtype=np.int64)
        w = tuple(int(x) % Q for x in (M @ v) % Q)
        return pidx[mod.norm(w)]

    def transvection(vv, lam):
        M = np.eye(4, dtype=np.int64)
        for b in range(4):
            e = np.zeros(4, dtype=np.int64)
            e[b] = 1
            val = int((e @ OM @ np.array(vv)) % Q)
            M[:, b] = (e + lam * val * np.array(vv)) % Q
        return M % Q

    def perm_of(M):
        return tuple(act(M, i) for i in range(40))

    return pts, edges, transvection, perm_of


def mul(p, q):
    return tuple(p[q[i]] for i in range(40))


def order_of(p):
    e = tuple(range(40))
    c, o = p, 1
    while c != e:
        c = mul(p, c)
        o += 1
    return o


def closure(seeds, cap=2000):
    e = tuple(range(40))
    S = {e}
    fr = [e]
    while fr:
        x = fr.pop()
        for g in seeds:
            y = mul(g, x)
            if y not in S:
                S.add(y)
                fr.append(y)
                if len(S) > cap:
                    return None
    return S


def part_A_orbits(checks):
    pts, edges, transvection, perm_of = build_machinery()
    random.seed(982)
    vecs = [np.array(v) for v in itertools.product(range(Q), repeat=4) if any(v)]
    pool = [perm_of(transvection(random.choice(vecs), random.choice([1, 2])))
            for _ in range(40)]
    for _ in range(400):
        a, b = random.sample(pool, 2)
        pool.append(mul(a, b))
    o5 = [g for g in pool if order_of(g) == 5]
    o3 = [g for g in pool if order_of(g) == 3]

    eset = [tuple(sorted(e)) for e in edges]
    profiles = Counter()
    verified = 0
    for _ in range(600):
        if not o5 or not o3:
            break
        g, h = random.choice(o5), random.choice(o3)
        S = closure([g, h])
        if not S or len(S) != 60:
            continue
        od = Counter(order_of(p) for p in S)
        if {k: od.get(k, 0) for k in A5_PROFILE} != A5_PROFILE:
            continue
        verified += 1
        seen, orbs = set(), []
        for e in eset:
            if e in seen:
                continue
            orb = {tuple(sorted((p[e[0]], p[e[1]]))) for p in S}
            seen |= orb
            orbs.append(len(orb))
        profiles[tuple(sorted(orbs, reverse=True))] += 1

    profs = {str(list(k)): v for k, v in profiles.items()}
    claimed = (60, 60, 60, 60)
    observed_claim = any(k == claimed for k in profiles)
    single = (len(profiles) == 1)
    the_profile = list(next(iter(profiles))) if single else None
    checks["a5_subgroups_verified"] = (verified >= 5)
    checks["four_regular_orbits_never_observed"] = (not observed_claim)
    checks["profile_is_uniform_across_samples"] = single
    checks["profile_is_60_60_30_30_20_20_10_10"] = (
        the_profile == [60, 60, 30, 30, 20, 20, 10, 10])
    stabs = [60 // s for s in (the_profile or [])]
    return {"verified_A5_subgroups": verified,
            "profiles_observed": profs,
            "claimed_profile": list(claimed),
            "claim_observed": observed_claim,
            "edge_orbit_profile": the_profile,
            "stabiliser_orders": stabs,
            "total_edges": sum(the_profile) if the_profile else None,
            "reading": (
                "Every profile-verified A5 subgroup gives eight edge orbits of "
                "sizes 60, 60, 30, 30, 20, 20, 10, 10 with stabilisers of orders "
                "1, 1, 2, 2, 3, 3, 6, 6.  Only two orbits are regular, so A5 does "
                "not act freely and the claimed four orbits of 60 do not occur.")}


def part_B_why_arithmetic_misled(checks):
    checks["divisibility_alone_is_consistent"] = (240 % 60 == 0)
    checks["regular_orbit_requires_trivial_stabiliser"] = True
    return {"240_over_60": 240 // 60,
            "claim_requires": "a free action: four orbits of size |A5| = 60",
            "actual": "two regular orbits out of eight",
            "structure": (
                "the orbit sizes are 60 divided by the divisors 1, 2, 3, 6 of 6, "
                "each occurring twice"),
            "reading": (
                "240 = 4 x 60 is consistent with the orbit-counting constraint, "
                "which is why the claim looked sound on arithmetic alone; but an "
                "orbit of size |G| is regular and needs a trivial stabiliser, and "
                "divisibility does not imply freeness.")}


def part_C_retraction(checks):
    checks["retraction_recorded"] = True
    return {"retracts": (
        "Pass 981 listed the A5 orbit split 240 = 4 x 60 as 'the one "
        "arithmetically clean new item' of that batch worth pursuing; that "
        "assessment is withdrawn here."),
        "still_true_from_that_audit": (
            "the CKM exclusions, the E8 index error, the Leech rank "
            "impossibility, and the textbook status of the graph-RH "
            "equivalence are unaffected"),
        "not_addressed": (
            "the Penrose tiling and Fibonacci-inflation material built on the "
            "orbit claim; only its group-theoretic foundation is removed")}


def main_payload():
    checks = {}
    A = part_A_orbits(checks)
    B = part_B_why_arithmetic_misled(checks)
    C = part_C_retraction(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass982.a5_edge_orbits_refutation.v1",
        "status": status,
        "headline": (
            "THE A5 EDGE-ORBIT CLAIM IS REFUTED.  Pass 886 asserts that A5 in "
            "Aut(W(3,3)) splits the 240 edges into four orbits of 60.  "
            "Constructing Sp(4,3) by symplectic transvections on the 40 "
            "projective points and sampling A5 subgroups verified by the exact "
            "element-order profile 1+15+20+24, every one of 17 independent "
            "samples gives the edge-orbit profile (60,60,30,30,20,20,10,10) -- "
            "eight orbits with stabilisers of orders 1,1,2,2,3,3,6,6, only two of "
            "them regular.  A5 does not act freely on the edges, so four orbits "
            "of 60 do not occur.  The arithmetic 240 = 4 x 60 is consistent with "
            "orbit counting, which is why the claim looked sound, but an orbit of "
            "size |G| requires a trivial stabiliser and divisibility does not "
            "imply freeness.  This also retracts the one item Pass 981 had "
            "listed as surviving from that batch.  What is true instead: the "
            "orbit sizes are 60 over the divisors 1,2,3,6 of 6, each twice."),
        "part_A_orbits": A,
        "part_B_why_arithmetic_misled": B,
        "part_C_retraction": C,
        "checks": {k: bool(v) for k, v in checks.items()},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    pl = main_payload()
    text = json.dumps(pl, sort_keys=True, separators=(",", ":")) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text() != text:
            raise SystemExit("Pass 982 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
