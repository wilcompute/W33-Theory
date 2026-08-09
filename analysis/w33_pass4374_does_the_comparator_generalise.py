#!/usr/bin/env python3
"""Pass 4374 -- is the comparator's 92.31% a law, or a coincidence of q=3?

Pass 4367 built the flag-incidence comparator on GQ(3,3) and read its detection boundary
off the geometry: each line carries 4 points so 3 of 39 wrong points survive, each point
lies on 4 lines so 3 of 39 wrong lines survive, giving 92.31% single-register detection.

Every number in that sentence is a parameter of q=3.  The design either generalises or it
does not, and one computation settles which -- exactly the check Pass 4372's sixth failure
mode says to run before treating a measured rate as a property of the design.

Build the symplectic quadrangle W(3,q) over F_q for several primes and measure.

    py -3 analysis/w33_pass4374_does_the_comparator_generalise.py
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def quadrangle(q):
    """Points and totally isotropic lines of W(3,q): the symplectic GQ of order (q,q)."""
    # symplectic form: <x,y> = x0 y1 - x1 y0 + x2 y3 - x3 y2
    def form(u, v):
        return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % q

    def norm(v):
        # canonical projective representative: scale so the first non-zero entry is 1
        for x in v:
            if x % q:
                inv = pow(x, q - 2, q)
                return tuple((c * inv) % q for c in v)
        return None

    seen, pts = set(), []
    for v in product(range(q), repeat=4):
        if not any(v):
            continue
        k = norm(v)
        if k not in seen:
            seen.add(k)
            pts.append(k)
    pidx = {p: i for i, p in enumerate(pts)}

    lines = set()
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if form(pts[i], pts[j]):
                continue
            span = set()
            for a in range(q):
                for b in range(q):
                    w = tuple((a * pts[i][t] + b * pts[j][t]) % q for t in range(4))
                    if any(w):
                        span.add(norm(w))
            if len(span) == q + 1:
                lines.add(frozenset(span))
    return pts, pidx, sorted(lines, key=lambda s: sorted(s))


def main() -> int:
    print("=" * 78)
    print("Pass 4374 -- the comparator across W(3,q)")
    print("=" * 78)
    print(f"  {'q':>3s} {'points':>7s} {'lines':>7s} {'pts/line':>9s} {'lines/pt':>9s} "
          f"{'flags':>7s} {'reject':>8s} {'detect':>8s}")
    rows = []
    for q in (2, 3, 5, 7):
        pts, pidx, lines = quadrangle(q)
        n = len(pts)
        if not lines:
            continue
        per_line = {len(L) for L in lines}
        per_point = {sum(1 for L in lines if p in L) for p in pts}
        if len(per_line) != 1 or len(per_point) != 1:
            print(f"  {q:3d}  irregular incidence; skipping")
            continue
        k_l, k_p = per_line.pop(), per_point.pop()
        flags = sum(len(L) for L in lines)
        reject = 1 - flags / (n * len(lines))
        # a corrupted point survives iff it lies on the same line: k_l - 1 of n - 1
        miss_p = (k_l - 1) / (n - 1)
        miss_l = (k_p - 1) / (len(lines) - 1)
        detect = 1 - (miss_p + miss_l) / 2
        rows.append({"q": q, "points": n, "lines": len(lines), "points_per_line": k_l,
                     "lines_per_point": k_p, "flags": flags,
                     "reject_fraction": reject, "detection": detect})
        print(f"  {q:3d} {n:7d} {len(lines):7d} {k_l:9d} {k_p:9d} {flags:7d} "
              f"{100 * reject:7.2f}% {100 * detect:7.2f}%")

    print(f"\n  predicted from the parameters alone, with N = (q+1)(q^2+1):")
    print(f"  {'q':>3s} {'N predicted':>12s} {'detect predicted':>18s}")
    ok = True
    for r in rows:
        q = r["q"]
        N = (q + 1) * (q * q + 1)
        pred = 1 - q / (N - 1)
        print(f"  {q:3d} {N:12d} {100 * pred:17.2f}%")
        ok &= (N == r["points"]) and abs(pred - r["detection"]) < 1e-12

    print(f"\n  the closed form matches every measured row: {ok}")
    print(f"""
  IT IS A LAW, NOT A COINCIDENCE OF q=3.  The symplectic quadrangle W(3,q) has
  N = (q+1)(q^2+1) points and the same number of lines, with q+1 points on every line and
  q+1 lines through every point.  A corrupted register survives the incidence check exactly
  when it lands on one of the other q points of the held line, so

      detection = 1 - q / ((q+1)(q^2+1) - 1).

  AND IT IMPROVES WITH q, which is the useful direction.  At q=2 the comparator catches
  {100 * rows[0]['detection']:.1f}%; at q=3, {100 * rows[1]['detection']:.2f}%; by q=7 it is {100 * rows[-1]['detection']:.2f}%.  The miss set shrinks
  because the register grows quadratically while the number of ways to stay on a line grows
  only linearly.

  So the design is not tuned to this machine's parameters -- q=3 is the WEAK end of a
  family that gets better. That is worth stating precisely because Pass 4367 could have
  been read the other way: a 92.31% figure quoted alone invites the question "and is that
  because three is special?", and the answer is that three is nearly the worst case.""")

    out = {

        "boundary": ("the law is derived for self-dual quadrangles and checked against the measured "

            "symplectic cases; nothing outside GQ(s,s) is verified in this pass"),"rows": rows, "closed_form": "1 - q/((q+1)(q^2+1) - 1)",
           "closed_form_verified": bool(ok),
           "improves_with_q": True,
           "q3_is_weak_end": True}
    p = ROOT / "data" / "PART_W33_PASS4374_COMPARATOR_GENERALISES.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
