"""Passes 5492-5495 -- the Reye/tomotope layer inside W(3,q) is a uniform family, the
40 = 16+12+12 is a partition, and the 48 that looked like F4's roots is q=3 only.

  5492  Pass 5490 found the tomotope's medial layer inside W(3,3) twice.  The last three
        claims in this thread died when run at another q, so this one is run at q = 5 and 7
        before anything is said about it.

  5493  It survives, as a uniform tactical configuration with point degree q+1 and line
        degree q(q-1)/2.  The Reye configuration 12_4 16_3 is its q = 3 member.

  5494  16 + 12 + 12 = 40 exactly, and (q+1)^2 + 2*(q^3-q)/2 = q^3+q^2+q+1 in general, so
        the W(F4) orbits PARTITION the point set rather than merely decomposing part of it.

  5495  And the 48 flags that coincide with W(F4)'s 48 roots are a q=3 coincidence: at q=5
        the flag count is 360.

    py -3 analysis/w33_pass5492_5495_the_tomotope_is_the_q3_member_of_a_family.py
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def analyse(q):
    def nrm(v):
        for a in v:
            if a % q:
                z = pow(a, q - 2, q)
                return tuple((z * x) % q for x in v)
        return None

    pts = sorted({nrm(v) for v in itertools.product(range(q), repeat=4) if any(v)})

    def B(u, v):
        return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % q

    def Qf(v):
        return (v[0] * v[1] + v[2] * v[3]) % q

    S = [p for p in pts if Qf(p) == 0]
    sq = {(x * x) % q for x in range(1, q)}
    P = [p for p in pts if Qf(p) in sq]
    M = [p for p in pts if Qf(p) != 0 and Qf(p) not in sq]
    out = []
    for nm, T in (("square", P), ("nonsquare", M)):
        dp = sorted({sum(1 for s in S if B(t, s) == 0) for t in T})
        dl = sorted({sum(1 for t in T if B(t, s) == 0) for s in S})
        out.append({"class": nm, "points": len(T), "point_degree": dp,
                    "line_degree": dl,
                    "flags": len(T) * dp[0] if len(dp) == 1 else None})
    return {"q": q, "total_points": len(pts), "lines": len(S),
            "q_plus_1_sq": (q + 1) ** 2, "classes": out,
            "partition_ok": len(S) + len(P) + len(M) == len(pts)}


def main() -> int:
    print("=" * 78)
    print("Passes 5492-5495 -- a family, not an accident")
    print("=" * 78)

    print("\n  PASS 5492 -- run it at another q, first, this time\n")
    rows = [analyse(q) for q in (3, 5, 7)]
    print(f"    {'q':>3s} {'points':>7s} {'lines':>6s} {'pts/class':>10s} "
          f"{'pt deg':>7s} {'line deg':>9s} {'flags':>7s}")
    for r in rows:
        c = r["classes"][0]
        print(f"    {r['q']:3d} {r['total_points']:7d} {r['lines']:6d} "
              f"{c['points']:10d} {str(c['point_degree']):>7s} "
              f"{str(c['line_degree']):>9s} {c['flags']:7d}")

    print("""
    IT SURVIVES. Both classes at every q give a tactical configuration -- one point degree,
    one line degree, no exceptions -- where the last three readings in this thread each
    collapsed at exactly this test. The 16-as-Q4 reading died here, the rook and Shrikhande
    candidates died on isomorphism, and (q+1)^2 killed the hypercube vertex count.""")

    print("\n  PASS 5493 -- the closed forms\n")
    print(f"    {'q':>3s} {'lines = (q+1)^2':>16s} {'points = (q^3-q)/2':>19s} "
          f"{'pt deg = q+1':>13s} {'line deg = q(q-1)/2':>20s}")
    ok = True
    for r in rows:
        q = r["q"]
        c = r["classes"][0]
        pred = [(q + 1) ** 2, (q ** 3 - q) // 2, q + 1, q * (q - 1) // 2]
        got = [r["lines"], c["points"], c["point_degree"][0], c["line_degree"][0]]
        ok &= pred == got
        print(f"    {q:3d} {r['lines']:16d} {c['points']:19d} "
              f"{c['point_degree'][0]:13d} {c['line_degree'][0]:20d}")
    print(f"\n    closed forms hold at every q tested : {ok}")
    print("""
    SO THE TOMOTOPE IS THE q = 3 MEMBER OF A FAMILY. At q=3 the parameters are 12_4 16_3,
    which is the Reye configuration and, by BT1363, the tomotope's edge-triangle medial
    layer. At q=5 they are 60_6 36_10 and at q=7 168_8 64_21 -- same construction, different
    numbers, and no polytope attached to those that this lane knows of.

    THAT IS A STRONGER STATEMENT THAN THE q=3 ONE. A structure that appears only at q=3 is a
    coincidence of the smallest case; a structure that appears at every odd q with the
    tomotope sitting at q=3 makes the tomotope an instance rather than an omen.""")

    print("\n  PASS 5494 -- it is a partition\n")
    for r in rows:
        q = r["q"]
        c = r["classes"]
        print(f"    q={q}: {r['lines']} + {c[0]['points']} + {c[1]['points']} = "
              f"{r['lines'] + c[0]['points'] + c[1]['points']} = {r['total_points']}"
              f"   {r['partition_ok']}")
    print("""
    (q+1)^2 + (q^3-q) = q^3 + q^2 + q + 1, which is |PG(3,q)|. So the W(F4) orbits do not
    merely decompose part of the point set -- they exhaust it. Every point of W(3,q) is
    either on the quadric or carries a square or non-square value, and those are the three
    orbits.""")

    print("\n  PASS 5495 -- the 48 that is not F4's roots\n")
    for r in rows:
        print(f"    q={r['q']}: flags = {r['classes'][0]['flags']}")
    print("""
    W(F4) HAS 48 ROOTS AND THE q=3 CONFIGURATION HAS 48 FLAGS, and that is a coincidence of
    q=3: at q=5 the flag count is 360 and at q=7 it is 1344, while W(F4) still has 48 roots.
    The flag count is q(q^2-1)(q+1)/2, which is not a root system count.

    RECORDED BECAUSE IT WAS ON THE LIST AND WOULD OTHERWISE HAVE BEEN TEMPTING. Three
    separate 48s -- roots, flags, edge-face blocks -- and the family separates them in one
    line. scripts/check_order_coincidence.py exists for exactly this shape.""")

    out = {
        "boundary": ("The closed forms are verified at q = 3, 5, 7 only; 'family' means "
                     "those three cases share one parametrisation, not that it is proved "
                     "for all odd q. The identification of the q=3 member with the "
                     "tomotope's medial layer is BT1363's and Pass 5490's isomorphism "
                     "test; no polytope is claimed for q > 3"),
        "pass_5492": {"rows": rows,
                      "note": "run at another q BEFORE claiming, unlike the last three"},
        "pass_5493": {"lines": "(q+1)^2", "points_per_class": "(q^3-q)/2",
                      "point_degree": "q+1", "line_degree": "q(q-1)/2",
                      "closed_forms_hold": ok,
                      "q3_member": "12_4 16_3 = Reye = tomotope medial layer",
                      "q5_member": "60_6 36_10", "q7_member": "168_8 64_21"},
        "pass_5494": {"partition": "(q+1)^2 + (q^3-q) = q^3+q^2+q+1 = |PG(3,q)|",
                      "verified": all(r["partition_ok"] for r in rows)},
        "pass_5495": {"flags_by_q": {r["q"]: r["classes"][0]["flags"] for r in rows},
                      "wf4_roots": 48,
                      "verdict": ("the 48/48 match is q=3 only; the flag count is "
                                  "q(q^2-1)(q+1)/2 and is not a root count")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5492_5495_TOMOTOPE_IS_A_FAMILY_MEMBER.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
