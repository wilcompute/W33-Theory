#!/usr/bin/env python3
"""Pass 4389 -- H(3,9) built and MEASURED, turning Pass 4381's derived rows into data.

Pass 4374 measured the flag-incidence comparator on the symplectic quadrangles and got
detection = 1 - q/((q+1)(q^2+1) - 1).  Pass 4381 generalised it to any GQ(s,t) from the
incidence parameters alone and observed that asymmetric quadrangles protect their two
registers UNEQUALLY -- a design lever the symplectic case (s = t) cannot show, because
there the two rates coincide by symmetry.

Pass 4381 stated its own scope: those asymmetric rows are DERIVED, never constructed.  This
pass removes that caveat for the smallest interesting case.  The Hermitian variety H(3,9)
is built explicitly over GF(9) -- points, totally isotropic lines, the whole incidence
relation -- its GQ parameters are verified rather than assumed, and the comparator's miss
set is enumerated EXHAUSTIVELY over every (flag, single-register fault) pair.  W(3,3) is
rebuilt alongside it as a control that must reproduce Pass 4367's measured 92.31%.

The prediction under test, stated before the run:

    H(3,9) is a GQ of order (s,t) = (9,3), so
        points  P = (s+1)(st+1) = 10 * 28 = 280
        lines   L = (t+1)(st+1) =  4 * 28 = 112
        point-register miss = s/(P-1) = 9/279 = 3.2258%
        line-register miss  = t/(L-1) = 3/111 = 2.7027%
        detection = 1 - (miss_p + miss_l)/2 = 97.0358%

    py -3 analysis/w33_pass4389_hermitian_quadrangle_measured.py
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# GF(9) = GF(3)[i]/(i^2 + 1).  -1 is a non-square mod 3, so x^2 + 1 is irreducible.
# Element a + b*i is encoded as the integer a + 3*b, a, b in {0,1,2}.
# ---------------------------------------------------------------------------
Q = 9


def _mul(x: int, y: int) -> int:
    a, b = x % 3, x // 3
    c, d = y % 3, y // 3
    # (a + bi)(c + di) = (ac - bd) + (ad + bc)i
    return (a * c - b * d) % 3 + 3 * ((a * d + b * c) % 3)


MUL = [[_mul(x, y) for y in range(Q)] for x in range(Q)]
ADD = [[(x % 3 + y % 3) % 3 + 3 * ((x // 3 + y // 3) % 3) for y in range(Q)]
       for x in range(Q)]
# Frobenius x -> x^3 is the involutory field automorphism of GF(9) over GF(3):
# (a + bi)^3 = a - bi.
CONJ = [x % 3 + 3 * ((-(x // 3)) % 3) for x in range(Q)]
INV = {x: next(y for y in range(1, Q) if MUL[x][y] == 1) for x in range(1, Q)}


def check_field() -> None:
    """The field must be a field before anything built on it means anything."""
    assert all(MUL[x][INV[x]] == 1 for x in range(1, Q))
    assert all(CONJ[CONJ[x]] == x for x in range(Q)), "conjugation is an involution"
    assert sum(1 for x in range(Q) if CONJ[x] == x) == 3, "fixed field is GF(3)"
    # x^3 must be a ring homomorphism.
    for x in range(Q):
        for y in range(Q):
            assert CONJ[MUL[x][y]] == MUL[CONJ[x]][CONJ[y]]
            assert CONJ[ADD[x][y]] == ADD[CONJ[x]][CONJ[y]]


def herm(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    """Sesquilinear form B(x,y) = sum_i x_i * conj(y_i)."""
    s = 0
    for xi, yi in zip(x, y):
        s = ADD[s][MUL[xi][CONJ[yi]]]
    return s


def projective_points(dim: int, q: int) -> list[tuple[int, ...]]:
    """Normalised representatives: leading nonzero coordinate equal to 1."""
    pts = []
    for lead in range(dim):
        for tail in itertools.product(range(q), repeat=dim - lead - 1):
            pts.append((0,) * lead + (1,) + tail)
    return pts


def build_h39() -> tuple[list, list, dict]:
    """Points and totally isotropic lines of the Hermitian surface H(3,9)."""
    pts = [p for p in projective_points(4, Q) if herm(p, p) == 0]
    index = {p: i for i, p in enumerate(pts)}

    def normalise(v: tuple[int, ...]) -> tuple[int, ...]:
        for c in v:
            if c:
                return tuple(MUL[INV[c]][x] for x in v)
        raise ValueError("zero vector")

    lines = set()
    for i, x in enumerate(pts):
        for y in pts[i + 1:]:
            if herm(x, y) != 0 or herm(y, x) != 0:
                continue
            # span(x,y) is totally isotropic; collect its projective points
            span = set()
            for a in range(Q):
                for b in range(Q):
                    if a == 0 and b == 0:
                        continue
                    v = tuple(ADD[MUL[a][xi]][MUL[b][yi]] for xi, yi in zip(x, y))
                    span.add(normalise(v))
            assert all(herm(v, v) == 0 for v in span), "isotropic span"
            lines.add(frozenset(index[v] for v in span))
    return pts, sorted(lines, key=sorted), index


def build_w33() -> tuple[list, list, dict]:
    """Points and totally isotropic lines of W(3,3), the control."""
    F = 3
    pts = projective_points(4, F)
    index = {p: i for i, p in enumerate(pts)}

    def symp(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % F

    def normalise(v):
        for c in v:
            if c:
                inv = pow(c, F - 2, F)
                return tuple((inv * z) % F for z in v)
        raise ValueError

    lines = set()
    for i, x in enumerate(pts):
        for y in pts[i + 1:]:
            if symp(x, y) != 0:
                continue
            span = set()
            for a in range(F):
                for b in range(F):
                    if a == 0 and b == 0:
                        continue
                    span.add(normalise(tuple((a * xi + b * yi) % F
                                             for xi, yi in zip(x, y))))
            lines.add(frozenset(index[v] for v in span))
    return pts, sorted(lines, key=sorted), index


def gq_parameters(pts: list, lines: list) -> tuple[int, int]:
    """(s, t): s+1 points per line, t+1 lines per point.  Verified, not assumed."""
    sizes = {len(L) for L in lines}
    assert len(sizes) == 1, f"lines of unequal size: {sorted(sizes)}"
    per_pt = [sum(1 for L in lines if i in L) for i in range(len(pts))]
    assert len(set(per_pt)) == 1, f"points of unequal degree: {sorted(set(per_pt))}"
    return sizes.pop() - 1, per_pt[0] - 1


def measure(pts: list, lines: list) -> dict:
    """Exhaustive miss enumeration over every (flag, single-register fault).

    A flag is an incident (point, line).  A single-register fault replaces exactly one of
    the two with a different element of the same type.  The comparator sees the fault iff
    the resulting pair is NOT a flag; it misses iff the pair is still incident.
    """
    on_line = [set(L) for L in lines]
    thru_pt: list[set[int]] = [set() for _ in pts]
    for j, L in enumerate(lines):
        for i in L:
            thru_pt[i].add(j)

    flags = [(i, j) for j, L in enumerate(lines) for i in L]
    miss_p = miss_l = trials_p = trials_l = 0
    for i, j in flags:
        # fault the POINT register: any other point
        trials_p += len(pts) - 1
        miss_p += len(on_line[j]) - 1        # still on the same line -> invisible
        # fault the LINE register: any other line
        trials_l += len(lines) - 1
        miss_l += len(thru_pt[i]) - 1        # still through the same point -> invisible

    mp, ml = Fraction(miss_p, trials_p), Fraction(miss_l, trials_l)
    return {"flags": len(flags), "miss_point": mp, "miss_line": ml,
            "detection": 1 - (mp + ml) / 2}


def predicted(s: int, t: int) -> dict:
    P, L = (s + 1) * (s * t + 1), (t + 1) * (s * t + 1)
    mp, ml = Fraction(s, P - 1), Fraction(t, L - 1)
    return {"points": P, "lines": L, "miss_point": mp, "miss_line": ml,
            "detection": 1 - (mp + ml) / 2}


def main() -> int:
    print("=" * 78)
    print("Pass 4389 -- H(3,9) constructed and measured")
    print("=" * 78)
    check_field()
    print("  GF(9) verified: multiplicative inverses, Frobenius is an involutory")
    print("  automorphism, its fixed field has 3 elements.\n")

    rows = []
    for name, builder in (("W(3,3)  [control]", build_w33), ("H(3,9)", build_h39)):
        pts, lines, _ = builder()
        s, t = gq_parameters(pts, lines)
        m, pr = measure(pts, lines), predicted(s, t)
        ok_struct = (len(pts), len(lines)) == (pr["points"], pr["lines"])
        ok_meas = (m["miss_point"], m["miss_line"]) == (pr["miss_point"], pr["miss_line"])
        print(f"  {name}")
        print(f"    order (s,t)            : ({s},{t})   [verified from the incidence, "
              f"not assumed]")
        print(f"    points / lines         : {len(pts)} / {len(lines)}"
              f"   predicted {pr['points']} / {pr['lines']}   "
              f"{'MATCH' if ok_struct else 'MISMATCH'}")
        print(f"    incident flags         : {m['flags']}")
        print(f"    miss, point register   : {float(m['miss_point']) * 100:7.4f}%"
              f"   = {m['miss_point']}")
        print(f"    miss, line register    : {float(m['miss_line']) * 100:7.4f}%"
              f"   = {m['miss_line']}")
        print(f"    detection (measured)   : {float(m['detection']) * 100:7.4f}%")
        print(f"    detection (Pass 4381)  : {float(pr['detection']) * 100:7.4f}%"
              f"   {'MATCH' if ok_meas else 'MISMATCH'}\n")
        assert ok_struct and ok_meas, f"{name}: Pass 4381's law failed against measurement"
        rows.append({"geometry": name.split()[0], "s": s, "t": t,
                     "points": len(pts), "lines": len(lines), "flags": m["flags"],
                     "miss_point": str(m["miss_point"]), "miss_line": str(m["miss_line"]),
                     "detection": str(m["detection"]),
                     "detection_pct": round(float(m["detection"]) * 100, 4),
                     "agrees_with_pass4381": True})

    h = rows[1]
    gap = float(Fraction(h["miss_point"]) / Fraction(h["miss_line"]))
    print(f"""  THE ASYMMETRIC ROW IS NOW MEASURED, NOT DERIVED.

  H(3,9) exists, its order is (9,3), and its two registers are protected at DIFFERENT
  rates: {float(Fraction(h['miss_point'])) * 100:.4f}% of point faults are invisible against {float(Fraction(h['miss_line'])) * 100:.4f}% of line faults --
  a factor of {gap:.3f}.  In W(3,3) the two rates are equal to the last digit because s = t
  forces it, so the symplectic case cannot even pose the question.

  WHAT THIS DOES AND DOES NOT LICENSE.  It licenses the arithmetic: Pass 4381's law is
  now confirmed against a construction rather than only against its own derivation, in a
  case where the two rates differ.  It does NOT yet license the design conclusion that one
  should put the more failure-prone register on the better-protected side, because that
  needs a machine on H(3,9), and H(3,9) is not self-dual -- its automorphism group is
  PGU(4,3), not Sp(4,3), and the four-opcode instruction set of the blueprint was built on
  the symplectic form. Whether any universal instruction set exists there is the open
  question, and it is stated here as open rather than assumed favourable.""")

    out = {"field": "GF(9) = GF(3)[i]/(i^2+1)", "rows": rows,
           "control_reproduced": rows[0]["detection_pct"],
           "pass4381_law_confirmed_against_construction": True,
           "asymmetry_factor_h39": round(gap, 6),
           "open": ("no instruction set is known on H(3,9); PGU(4,3) is not Sp(4,3) and "
                    "the quadrangle is not self-dual, so the design lever is confirmed "
                    "to EXIST but not yet shown to be REACHABLE"),
           "conclusion": ("H(3,9) built explicitly over GF(9); order (9,3) verified from "
                          "the incidence; exhaustive miss enumeration reproduces Pass "
                          "4381's derived rates exactly, and the two registers differ")}
    p = ROOT / "data" / "PART_W33_PASS4389_HERMITIAN_MEASURED.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
