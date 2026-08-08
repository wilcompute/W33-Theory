#!/usr/bin/env python3
"""Pass 4381 -- does the comparator's law survive outside the symplectic quadrangle?

Pass 4374 found detection = 1 - q/((q+1)(q^2+1) - 1) across W(3,q) for q = 2,3,5,7.  Every
one of those is a GQ of order (q, q): same number of points as lines, same number of points
per line as lines per point.  The closed form may be a fact about generalized quadrangles or
a fact about the self-dual-parameter case, and the two are distinguished by looking at a GQ
of order (s, t) with s != t.

Rather than construct Hermitian and orthogonal quadrangles explicitly -- which is real work
and not the question -- derive the detection rate for a general GQ(s, t) from its parameters
and check the derivation against the four cases already measured.  If the general formula
reproduces Pass 4374's numbers when s = t = q, the derivation is sound and the asymmetric
case follows from it.

A GQ of order (s, t) has
    (s+1)(st+1) points, (t+1)(st+1) lines, s+1 points per line, t+1 lines per point.

    py -3 analysis/w33_pass4381_other_quadrangles.py
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rates(s, t):
    """Point-fault, line-fault and mean detection for a GQ of order (s, t)."""
    P = (s + 1) * (s * t + 1)
    L = (t + 1) * (s * t + 1)
    pts_per_line = s + 1
    lines_per_pt = t + 1
    # a corrupted point survives iff it is another point of the held line
    miss_p = Fraction(pts_per_line - 1, P - 1)
    # a corrupted line survives iff it is another line through the held point
    miss_l = Fraction(lines_per_pt - 1, L - 1)
    return P, L, miss_p, miss_l, 1 - (miss_p + miss_l) / 2


def main() -> int:
    print("=" * 78)
    print("Pass 4381 -- the detection law for a general GQ of order (s, t)")
    print("=" * 78)
    print("  points (s+1)(st+1), lines (t+1)(st+1), s+1 points per line,"
          " t+1 lines per point\n")

    print("  FIRST, reproduce Pass 4374's measured cases with s = t = q:")
    print(f"  {'q':>3s} {'points':>7s} {'lines':>7s} {'detection':>11s} {'measured':>11s}")
    measured = {2: 0.8571428571428572, 3: 0.9230769230769231,
                5: 0.967741935483871, 7: 0.9824561403508771}
    ok = True
    for q in (2, 3, 5, 7):
        P, L, mp, ml, det = rates(q, q)
        agree = abs(float(det) - measured[q]) < 1e-12
        ok &= agree
        print(f"  {q:3d} {P:7d} {L:7d} {100 * float(det):10.4f}% "
              f"{100 * measured[q]:10.4f}%  {'match' if agree else 'MISMATCH'}")
    print(f"\n  the general formula reproduces every measured symplectic case: {ok}")
    if not ok:
        print("  derivation is wrong; refusing to extrapolate from it")
        return 1

    print("\n  NOW THE ASYMMETRIC FAMILIES, which the symplectic case cannot distinguish:")
    print(f"  {'family':28s} {'(s,t)':>10s} {'points':>7s} {'lines':>7s} {'detection':>11s}")
    rows = []
    fams = [("symplectic W(3,q), q=3", 3, 3),
            ("Hermitian H(3,q^2), q=3", 3, 9),
            ("Hermitian dual, q=3", 9, 3),
            ("orthogonal Q(5,q), q=3", 3, 9),
            ("symplectic W(3,q), q=9", 9, 9)]
    for name, s, t in fams:
        P, L, mp, ml, det = rates(s, t)
        rows.append({"family": name, "s": s, "t": t, "points": P, "lines": L,
                     "miss_point": float(mp), "miss_line": float(ml),
                     "detection": float(det)})
        print(f"  {name:28s} {f'({s},{t})':>10s} {P:7d} {L:7d} "
              f"{100 * float(det):10.4f}%")

    sym = rows[0]
    herm = rows[1]
    dual = rows[2]
    print(f"""
  THE LAW IS ABOUT GENERALIZED QUADRANGLES, NOT ABOUT SELF-DUALITY.  The derivation uses
  only the four incidence parameters, and it reproduces all four measured symplectic points
  exactly, so the closed form of Pass 4374 is the s = t specialisation of

      detection = 1 - [ s/((s+1)(st+1) - 1) + t/((t+1)(st+1) - 1) ] / 2 .

  THE ASYMMETRIC CASE IS THE INTERESTING ONE.  For the Hermitian quadrangle at q=3, order
  (3,9), a point fault and a line fault are no longer equally detectable: the miss rates are
  {100 * herm['miss_point']:.3f}% and {100 * herm['miss_line']:.3f}% respectively.  The register with FEWER
  neighbours is the better-protected one, because there are fewer wrong values that still
  satisfy incidence.

  That is a design lever the symplectic case hides completely.  In W(3,3) both halves of the
  flag are equally exposed and there is nothing to choose; in an asymmetric quadrangle a
  designer can put the more failure-prone register on the side with the smaller miss rate.
  Whether such a machine can be built is a separate question -- these families have
  different automorphism groups and the instruction set would have to be rebuilt -- and
  nothing here claims it can.

  SCOPE.  This is a derivation from incidence parameters, verified against four explicitly
  constructed cases. The asymmetric rows are NOT measured: no Hermitian or orthogonal
  quadrangle was built here, and if one of those families fails to have the stated
  parameters the corresponding row is wrong.""")

    out = {"general_formula": ("1 - [s/((s+1)(st+1)-1) + t/((t+1)(st+1)-1)]/2"),
           "reproduces_measured_symplectic": bool(ok),
           "rows": rows,
           "asymmetric_gives_unequal_protection": True,
           "asymmetric_rows_are_derived_not_measured": True}
    p = ROOT / "data" / "PART_W33_PASS4381_OTHER_QUADRANGLES.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
