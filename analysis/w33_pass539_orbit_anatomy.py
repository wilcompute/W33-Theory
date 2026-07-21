#!/usr/bin/env python3
"""Pass 539: the anatomy of the seven q = 3 orbits -- and the merge is exactly
the full-support pair.

Passes 536-538 established that charpoly is an Sp(2,p)-invariant, that q = 3
has seven orbits, that six characteristic polynomials occur, and that merging
is not systematic.  What was never done is look at the seven orbits.

THE ANATOMY.  With |Sp(2,3)| = 24, and writing "support" for the number of the
eight nonzero v with c(v) != 0:

    size  stabiliser  support   charpoly
      1       24        0/8     x^3                 (the flat section)
      8        3        8/8     x^3 - 36x - 81      <- merge
      8        3        8/8     x^3 - 36x - 81      <- merge
      8        3        6/8     x^3 - 27x
      8        3        2/8     x^3 -  9x
     24        1        6/8     x^3 - 27x - 27
     24        1        4/8     x^3 - 18x

Sizes and stabilisers multiply to 24 throughout, as they must.

THE MERGE IS THE FULL-SUPPORT PAIR.  The two orbits that share a
characteristic polynomial are exactly the two whose sections have FULL
SUPPORT -- every c(v) nonzero.  No other pair of orbits shares a polynomial,
and no other orbit has full support.  That is a clean characterisation of
where the coincidence lives, and it was not visible before the orbits were
listed.

WHAT THIS PASS DID NOT DO.  Support does not SEPARATE the two: both are 8/8.
Pass 540 subsequently identifies the finer fixed-frame invariant as
coordinate-product parity, with the frame-corrected scalar of a Moore-Dickson
form giving the intrinsic version, and identifies the two fibers with the D4
half-spin chiralities.

SUPPORT IS NOT A COMPLETE INVARIANT EITHER.  Two orbits have support 6/8 -- one
of size 8 and one of size 24 -- with different polynomials.  So neither support
nor orbit size alone classifies.  The pair (size, support) gives six fibers and
separates every orbit except the two full-support chiralities.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass539_orbit_anatomy.json"


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


def part_A_anatomy(checks):
    p = 3
    R, C = LF(p, 1), Cyc(p, 1)
    H = Heis(R, C)
    q = H.q
    F = H.block(H.full_sec(tuple(R.zero for _ in H.pairs)))
    els = list(R.elems)
    vecs = [(a, b) for a in range(p) for b in range(p) if (a, b) != (0, 0)]
    SP = [
        (a, b, c, d)
        for a in range(p)
        for b in range(p)
        for c in range(p)
        for d in range(p)
        if (a * d - b * c) % p == 1
    ]
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

    def act(g, sec):
        a, b, c, d = g
        inv = pow((a * d - b * c) % p, -1, p)
        return {
            v: sec[
                (((d * v[0] - b * v[1]) * inv) % p, ((-c * v[0] + a * v[1]) * inv) % p)
            ]
            for v in vecs
        }

    def key(sec):
        return tuple(sec[pairs[i][0]] for i in range(len(pairs)))

    def cp(sec):
        fs = {(els[v[0]], els[v[1]]): els[sec[v]] for v in vecs}
        B = H.block(fs)
        D = [[C.sub(B[i][j], F[i][j]) for j in range(q)] for i in range(q)]
        return (
            tuple(-x // 2 for x in trace(matmul(D, D, C), C)),
            tuple(det_exact(D, C)),
        )

    allsec = [tuple(o) for o in itertools.product(range(p), repeat=len(pairs))]
    unseen, rows = set(allsec), []
    while unseen:
        s0 = next(iter(unseen))
        sec = sec_from(s0)
        O = {key(act(g, sec)) for g in SP} & set(allsec)
        stab = sum(1 for g in SP if key(act(g, sec)) == s0)
        supp = sum(1 for v in vecs if sec[v] != 0)
        k = cp(sec)
        rows.append(
            {
                "size": len(O),
                "stabiliser": stab,
                "support": supp,
                "e2": k[0][0],
                "e3": k[1][0],
                "rep": list(s0),
            }
        )
        unseen -= O
    rows.sort(key=lambda r: (r["size"], -r["support"]))
    bycp = {}
    for r in rows:
        bycp.setdefault((r["e2"], r["e3"]), []).append(r)
    merged = [v for v in bycp.values() if len(v) > 1]
    full = [r for r in rows if r["support"] == 8]
    by_size_support = {}
    for r in rows:
        by_size_support.setdefault((r["size"], r["support"]), []).append(r)
    checks["seven_orbits"] = len(rows) == 7
    checks["orbit_times_stabiliser_is_group_order"] = all(
        r["size"] * r["stabiliser"] == 24 for r in rows
    )
    checks["exactly_one_merged_pair"] = len(merged) == 1
    checks["the_merge_is_exactly_the_full_support_pair"] = (
        len(merged) == 1
        and len(full) == 2
        and {tuple(r["rep"]) for r in merged[0]} == {tuple(r["rep"]) for r in full}
    )
    checks["size_support_has_six_fibers_and_only_merges_the_chiral_pair"] = len(
        by_size_support
    ) == 6 and [key for key, value in by_size_support.items() if len(value) > 1] == [
        (8, 8)
    ]
    return {
        "orbits": rows,
        "merged_pair": merged[0] if merged else None,
        "full_support_orbits": full,
        "finding": (
            "The two orbits sharing a characteristic polynomial are "
            "exactly the two whose sections have FULL SUPPORT -- every "
            "c(v) nonzero.  No other pair shares a polynomial and no other "
            "orbit has full support."
        ),
        "what_it_does_not_do": (
            "Support does not SEPARATE the two: both are 8/8, so whatever "
            "distinguishes them as orbits is finer than support and the "
            "characteristic polynomial cannot see it.  Their "
            "representatives differ in a single pair value.  Pass 540 "
            "subsequently names the fixed-frame invariant as coordinate-product "
            "parity and its intrinsic correction as the Moore-Dickson bracket "
            "scalar, equivalently the unordered D4 half-spin split."
        ),
        "support_is_not_complete": (
            "Two orbits have support 6/8 -- one of size 8, one of size 24 "
            "-- with different polynomials.  Neither support nor orbit "
            "size alone classifies.  The pair (size, support) has six fibers "
            "and separates every orbit except the two full-support "
            "chiralities."
        ),
    }


def main_payload():
    checks = {}
    A = part_A_anatomy(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass539.orbit_anatomy.v1",
        "status": status,
        "headline": (
            "THE q = 3 MERGE IS EXACTLY THE FULL-SUPPORT PAIR.  Listing the "
            "seven Sp(2,3)-orbits with their stabilisers and supports -- the "
            "number of nonzero c(v) out of eight -- gives sizes 1, 8, 8, 8, 8, "
            "24, 24 with stabilisers 24, 3, 3, 3, 3, 1, 1 and supports 0, 8, "
            "8, 6, 2, 6, 4.  The two orbits sharing x^3 - 36x - 81 are "
            "precisely the two of FULL support, and no other orbit has full "
            "support.  That locates the coincidence structurally for the first "
            "time.  Pass 540 resolves the remaining separator as "
            "coordinate-product parity / D4 half-spin chirality."
        ),
        "part_A_anatomy": A,
        "boundary": (
            "Exhaustive over the complete 81-section space and the full group "
            "at q = 3, so the anatomy is decisive there.  Nothing is claimed "
            "here for q >= 5; an exhaustive listing was not attempted.  Pass "
            "540 supersedes the formerly open separator and carries it into a "
            "targeted q = 5 full-support search."
        ),
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
            raise SystemExit("Pass 539 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(
        json.dumps(
            {
                "status": pl["status"],
                "checks": sum(pl["checks"].values()),
                "total": len(pl["checks"]),
            }
        )
    )
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
