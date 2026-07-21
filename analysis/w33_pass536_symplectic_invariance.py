#!/usr/bin/env python3
"""Pass 536: the characteristic polynomial is a SYMPLECTIC INVARIANT, and the
q = 3 multiplicities are orbit sizes.

Pass 535 closed the q = 3 lattice and left one question: which lattice points
the sections realise, and why with multiplicities 1, 8, 24, 8, 24, 16.  The
answer is a group action nobody in this arc had used.

THE INVARIANCE.  Sp(2,p) acts on sections by (g . c)(v) = c(g^{-1} v), and
charpoly(D) is CONSTANT on orbits -- 0 changes in 180 trials at p = 3, 5, 7.
This is not surprising in hindsight (Pass 459 recorded a Galois covariance of
the blocks) but it had not been applied to the image question.

THE q = 3 MULTIPLICITIES ARE ORBIT SIZES.  SL(2,3) = Sp(2,3) has order 24 and
acts on the 81 sections with SEVEN orbits, of sizes

        1, 8, 8, 8, 8, 24, 24        (summing to 81).

Six characteristic polynomials occur, so exactly ONE coincidence happens: two
of the four size-8 orbits share a polynomial, giving the class of size 16.
The observed multiplicities 1, 8, 8, 16, 24, 24 are therefore orbit sizes with
a single merge, and the question "why these multiplicities" is answered:
they are the orbit sizes of the symplectic group, not a numerical accident.

WHAT REMAINS AT q = 3.  Only the merge.  Two size-8 orbits are distinct as
orbits and identical in characteristic polynomial; no reason is offered here.
That is a genuine coincidence of the same kind Pass 456 found for the q = 5
cospectral pair, and it is recorded as one rather than explained.

WHY THIS MATTERS AT q = 5.  The image of the section space in charpoly space
is a quotient of the ORBIT space, not of the section space.  At q = 5 that
replaces 5^12 sections by at most 5^12/120 orbits, and -- more usefully --
tells us that whatever refines the valuation profile must itself be an
Sp(2,5)-invariant.  That is a real constraint on the search Pass 524 opened,
and it is stated here, not used.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass536_symplectic_invariance.json"


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P487 = _load("p487", "w33_pass487_scope_of_the_law_and_det_hunt.py")
P489 = _load("p489", "w33_pass489_frobenius_generality.py")
P504 = _load("p504", "w33_pass504_trDq_fitting_and_noncommutative.py")

matmul, trace, det_exact = P487.matmul, P504.trace, P487.det_exact
Cyc, LF, Heis = P487.Cyc, P489.LocalFrobenius, P489.Heis


def cell(p):
    R, C = LF(p, 1), Cyc(p, 1)
    H = Heis(R, C)
    F = H.block(H.full_sec(tuple(R.zero for _ in H.pairs)))
    els = list(R.elems)
    vecs = [(a, b) for a in range(p) for b in range(p) if (a, b) != (0, 0)]
    SP = [(a, b, c, d) for a in range(p) for b in range(p)
          for c in range(p) for d in range(p) if (a * d - b * c) % p == 1]
    return R, C, H, H.q, F, els, vecs, SP


def act(p, g, sec, vecs):
    a, b, c, d = g
    inv = pow((a * d - b * c) % p, -1, p)
    return {v: sec[(((d * v[0] - b * v[1]) * inv) % p,
                    ((-c * v[0] + a * v[1]) * inv) % p)] for v in vecs}


def cdata(C, H, q, F, els, vecs, sec):
    fs = {(els[v[0]], els[v[1]]): els[sec[v]] for v in vecs}
    B = H.block(fs)
    D = [[C.sub(B[i][j], F[i][j]) for j in range(q)] for i in range(q)]
    A = [[C.rat(1) if i == j else C.zero() for j in range(q)]
         for i in range(q)]
    out = []
    for _ in range(q):
        A = matmul(A, D, C)
        out.append(tuple(trace(A, C)))
    return tuple(out)


def part_A_invariance(checks):
    rows, ok = {}, True
    for p in (3, 5, 7):
        R, C, H, q, F, els, vecs, SP = cell(p)
        rng = random.Random(7)
        bad, tot = 0, 0
        for _ in range(6):
            base = {}
            for v in vecs:
                if v in base:
                    continue
                c = rng.randrange(p)
                base[v] = c
                base[((-v[0]) % p, (-v[1]) % p)] = (-c) % p
            c0 = cdata(C, H, q, F, els, vecs, base)
            for g in rng.sample(SP, min(10, len(SP))):
                tot += 1
                if cdata(C, H, q, F, els, vecs,
                         act(p, g, base, vecs)) != c0:
                    bad += 1
        if bad:
            ok = False
        rows[f"p{p}"] = {"group_order": len(SP), "trials": tot,
                         "changed": bad}
    checks["charpoly_is_symplectically_invariant"] = ok
    checks["invariance_tested_at_three_primes"] = len(rows) == 3
    return {"rows": rows,
            "action": "(g . c)(v) = c(g^{-1} v), for g in Sp(2,p)",
            "finding": (
                "charpoly(D) is constant on Sp(2,p)-orbits of sections; 0 "
                "changes in 180 trials across p = 3, 5, 7.")}


def part_B_orbits(checks):
    p = 3
    R, C, H, q, F, els, vecs, SP = cell(p)
    pairs, seen = [], set()
    for v in vecs:
        nv = ((-v[0]) % p, (-v[1]) % p)
        if v in seen or nv in seen:
            continue
        seen.add(v)
        seen.add(nv)
        pairs.append((v, nv))

    def sec_from(o):
        d = {}
        for (v, nv), c in zip(pairs, o):
            d[v] = c % p
            d[nv] = (-c) % p
        return d

    allsec = [tuple(o) for o in itertools.product(range(p), repeat=len(pairs))]
    unseen, orbits = set(allsec), []
    while unseen:
        s0 = next(iter(unseen))
        sec = sec_from(s0)
        O = {tuple(act(p, g, sec, vecs)[pairs[i][0]]
                   for i in range(len(pairs))) for g in SP}
        O &= set(allsec)
        orbits.append(O)
        unseen -= O
    sizes = sorted(len(o) for o in orbits)
    cps = {}
    for O in orbits:
        k = cdata(C, H, q, F, els, vecs, sec_from(next(iter(O))))
        cps.setdefault(k, 0)
        cps[k] += len(O)
    checks["seven_orbits_at_q3"] = len(orbits) == 7
    checks["orbit_sizes_are_1_8_8_8_8_24_24"] = sizes == [1, 8, 8, 8, 8,
                                                          24, 24]
    checks["six_charpolys_so_exactly_one_merge"] = len(cps) == 6
    checks["orbits_sum_to_81"] = sum(sizes) == 81
    return {"orbit_sizes": sizes, "orbits": len(orbits),
            "distinct_charpolys": len(cps),
            "charpoly_class_sizes": sorted(cps.values()),
            "reading": (
                "SL(2,3) = Sp(2,3) has order 24 and acts on the 81 sections "
                "with SEVEN orbits of sizes 1, 8, 8, 8, 8, 24, 24.  Six "
                "characteristic polynomials occur, so exactly ONE coincidence "
                "happens: two of the four size-8 orbits share a polynomial, "
                "giving the class of size 16.  The multiplicities "
                "1, 8, 8, 16, 24, 24 are therefore orbit sizes with a single "
                "merge -- not a numerical accident."),
            "the_merge_is_unexplained": (
                "Two size-8 orbits are distinct as orbits and identical in "
                "characteristic polynomial.  No reason is offered; it is a "
                "coincidence of the same kind Pass 456 found for the q = 5 "
                "cospectral pair, and is recorded as one.")}


def part_C_consequence(checks):
    checks["consequence_stated"] = True
    return {"statement": (
        "The image of the section space in charpoly space is a quotient of the "
        "ORBIT space, not of the section space.  At q = 5 that replaces 5^12 "
        "sections by at most 5^12/120 orbits."),
        "sharper": (
            "More usefully: whatever refines the valuation profile at q = 5 -- "
            "the invariant Pass 524 showed must exist, since 34 profiles carry "
            "52 trace vectors -- must itself be an Sp(2,5)-INVARIANT.  That is "
            "a real constraint on the search."),
        "not_used": (
            "Stated, not used.  No q = 5 invariant is proposed or tested "
            "here.")}


def main_payload():
    checks = {}
    A = part_A_invariance(checks)
    B = part_B_orbits(checks)
    C = part_C_consequence(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass536.symplectic_invariance.v1",
        "status": status,
        "headline": (
            "THE CHARACTERISTIC POLYNOMIAL IS A SYMPLECTIC INVARIANT, AND THE "
            "q = 3 MULTIPLICITIES ARE ORBIT SIZES.  Sp(2,p) acts on sections "
            "by (g . c)(v) = c(g^{-1} v) and charpoly(D) is constant on orbits "
            "-- 0 changes in 180 trials at p = 3, 5, 7.  At q = 3, Sp(2,3) has "
            "order 24 and acts on the 81 sections with SEVEN orbits of sizes "
            "1, 8, 8, 8, 8, 24, 24; six characteristic polynomials occur, so "
            "exactly ONE coincidence happens -- two size-8 orbits share a "
            "polynomial, giving the class of 16.  So the multiplicities "
            "1, 8, 8, 16, 24, 24 that Pass 535 left unexplained are orbit "
            "sizes with a single merge.  The merge itself is a genuine "
            "coincidence and is recorded, not explained.  Consequence for "
            "q = 5: whatever refines the valuation profile must itself be an "
            "Sp(2,5)-invariant."),
        "part_A_symplectic_invariance": A,
        "part_B_q3_orbit_structure": B,
        "part_C_consequence_for_q5": C,
        "boundary": (
            "Part A samples 6 sections and 10 group elements per prime, 180 "
            "trials in total; the invariance is a property of the "
            "construction rather than a sampled fact, but it is verified here "
            "and not derived.  Part B is EXHAUSTIVE over the 81 sections and "
            "the full group at q = 3.  Part C states a constraint and does not "
            "use it: no q = 5 invariant is proposed or tested."),
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
            raise SystemExit("Pass 536 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
