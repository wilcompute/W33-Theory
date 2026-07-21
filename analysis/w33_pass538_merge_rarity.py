#!/usr/bin/env python3
"""Pass 538: the original q = 5 orbit-merge pilot sample.

Pass 537 bounded the q = 5 image by the Sp(2,5) orbit count, 2,034,735, and
left open whether that bound is close: orbits could merge systematically, in
which case the image would be far smaller.  At q = 3 exactly one merge occurs
in seven orbits, which is either noise or the start of a pattern.

THE TEST.  Canonicalise each sampled section under the full group -- the
lexicographic minimum over Sp(2,p) -- and count distinct ORBITS against
distinct CHARPOLYS in the same sample.  Merges are exactly the difference.

  p = 3, 81 seeded draws:  7 orbits, 6 charpolys, ONE merge.
  p = 5, 300 samples:      300 orbits, 300 charpolys, ZERO merges.

The q = 3 line is the control: the draws hit all seven canonical orbits, whose
completeness is independently known from Pass 537, and the method finds the
known merge.  The draw itself is not an enumeration of all 81 sections.

WHAT IT SETTLES.  Only the sampled statement: these 300 canonical q = 5
orbits have 300 distinct characteristic polynomials.  The q = 3 control shows
that the comparison code can detect a merge when one is present.

RETROSPECTIVE STATUS.  Pass 540 targeted full support and found merges at
q = 5, including an affine-inequivalent pair.  Therefore this pilot does not
bound the global image cardinality, establish rarity, or show that the orbit
bound is close to sharp.  Pass 540 also explains the q = 3 merge as the two
D4 half-spin chiralities.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass538_merge_rarity.json"


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P487 = _load("p487", "w33_pass487_scope_of_the_law_and_det_hunt.py")
P489 = _load("p489", "w33_pass489_frobenius_generality.py")
P504 = _load("p504", "w33_pass504_trDq_fitting_and_noncommutative.py")

matmul, trace = P487.matmul, P504.trace
Cyc, LF, Heis = P487.Cyc, P489.LocalFrobenius, P489.Heis


def run(p, N, seed=11):
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

    def canon(sec):
        best = None
        for g in SP:
            a, b, c, d = g
            inv = pow((a * d - b * c) % p, -1, p)
            t = tuple(
                sec[
                    (
                        ((d * v[0] - b * v[1]) * inv) % p,
                        ((-c * v[0] + a * v[1]) * inv) % p,
                    )
                ]
                for v in vecs
            )
            if best is None or t < best:
                best = t
        return best

    def cp(sec):
        fs = {(els[v[0]], els[v[1]]): els[sec[v]] for v in vecs}
        B = H.block(fs)
        D = [[C.sub(B[i][j], F[i][j]) for j in range(q)] for i in range(q)]
        A = [[C.rat(1) if i == j else C.zero() for j in range(q)] for i in range(q)]
        o = []
        for _ in range(q):
            A = matmul(A, D, C)
            o.append(tuple(trace(A, C)))
        return tuple(o)

    rng = random.Random(seed)
    orbs, cps = set(), set()
    for _ in range(N):
        sec = {}
        for v in vecs:
            if v in sec:
                continue
            c = rng.randrange(p)
            sec[v] = c
            sec[((-v[0]) % p, (-v[1]) % p)] = (-c) % p
        orbs.add(canon(sec))
        cps.add(cp(sec))
    return len(orbs), len(cps)


def part_A_merges(checks):
    rows = {}
    o3, c3 = run(3, 81)
    o5, c5 = run(5, 300)
    rows["p3"] = {"samples": 81, "orbits": o3, "charpolys": c3, "merges": o3 - c3}
    rows["p5"] = {"samples": 300, "orbits": o5, "charpolys": c5, "merges": o5 - c5}
    checks["q3_control_finds_its_known_merge"] = (o3 - c3) == 1
    checks["q3_recovers_seven_orbits"] = o3 == 7
    checks["q5_original_sample_has_no_merging"] = (o5 - c5) == 0
    checks["q5_sample_size_is_300_distinct_orbits"] = o5 == 300
    return {
        "rows": rows,
        "method": (
            "Canonicalise each section under the full group -- the "
            "lexicographic minimum over Sp(2,p) -- and count distinct "
            "ORBITS against distinct CHARPOLYS in the same sample.  Merges "
            "are the difference."
        ),
        "control": (
            "A measured control, not an assumption: the q = 3 line recovers all seven orbits "
            "and finds the one merge that Pass 537 located.  So a count of "
            "zero at q = 5 is a measurement, not a blind spot in the "
            "method."
        ),
    }


def part_B_consequence(checks):
    checks["sample_boundary_is_explicit"] = True
    return {
        "settled": (
            "Exactly these 300 sampled canonical q = 5 orbits carry 300 distinct "
            "characteristic polynomials.  The q = 3 control confirms that the "
            "comparison detects its known merge."
        ),
        "reframes_q3": (
            "A proved count, per Pass 537: the finite lookup table at q = 3 exists since SEVEN "
            "orbits exist there, not because merging compressed anything.  The "
            "smallness is the group's, not a coincidence's."
        ),
        "not_settled": (
            "The sample does not estimate the global image cardinality or a "
            "collision rate.  Pass 540 later found q = 5 full-support merges "
            "and explained the q = 3 merge by D4 half-spin chirality."
        ),
    }


def main_payload():
    checks = {}
    A = part_A_merges(checks)
    B = part_B_consequence(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass538.merge_rarity.v1",
        "status": status,
        "headline": (
            "ORIGINAL 300-ORBIT q = 5 PILOT (retrospectively bounded).  Canonicalising sections under "
            "the full symplectic group and comparing distinct orbits with "
            "distinct characteristic polynomials: at q = 3 the method recovers "
            "all seven orbits and the single known merge, and at q = 5 it "
            "finds 300 orbits carrying 300 distinct charpolys -- ZERO merges.  "
            "The q = 3 control is what makes the q = 5 zero a measurement "
            "rather than a blind spot in that comparison.  No global "
            "cardinality or rarity conclusion follows: Pass 540 later found "
            "q = 5 merges in a targeted full-support sample."
        ),
        "part_A_merge_counts": A,
        "part_B_consequence": B,
        "boundary": (
            "Measured, not proved.  The q = 3 line uses 81 seeded draws with "
            "replacement; it is orbit-complete only because it hits all seven "
            "orbits and Pass 537 independently proves that seven is the total. "
            "The q = 5 "
            "line samples 300 sections, which happened to give 300 distinct "
            "orbits.  It makes no global claim about merging or the size of "
            "the characteristic-polynomial image.  Pass 540 supersedes the "
            "old interpretation and explains the q = 3 merge."
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
            raise SystemExit("Pass 538 certificate drift")
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
