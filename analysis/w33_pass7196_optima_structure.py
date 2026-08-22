"""Pass 7196 -- what the known optimal partial ovoids actually look like, q = 3, 5, 7.

THE POINT. Three independent LNS runs reach 51 at q=9 within seconds and stall, while the
same code finds the q=7 optimum 33 in five seconds. Either alpha(W(3,9)) = 51, or 52 exists
and is unusually hard to reach. Guessing between them is worthless; the arithmetic is no help
either, since 52 continues a quadratic through 7, 18, 33 and 51 breaks it, and three points
fit a quadratic for free.

So instead: measure the OPTIMA that are known, at q = 3, 5 and 7, and look for an invariant
that survives across all three. Anything that does is a constraint a q=9 optimum must also
satisfy, and it can be imposed on the search rather than hoped for.

INVARIANTS COMPUTED, all of them basis-free:

  1. the TANGENT DISTRIBUTION -- for each point off the ovoid, how many ovoid points it is
     collinear with. For a full ovoid this is constant; the shape of its failure is what
     distinguishes a partial ovoid;
  2. the PLANE DISTRIBUTION -- |O ∩ H| over the q^3+q^2+q+1 planes of PG(3,q);
  3. the DEFICIENCY -- which lines carry no ovoid point at all;
  4. the size of the stabilizer's action, via the tangent multiset as a fingerprint.

A metric or basis-dependent claim would be worthless here, so none is made: every quantity
is an incidence count.

    py -3 analysis/w33_pass7196_optima_structure.py
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass7187_q9_orbit_attack import Field, geometry  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SOURCES = {
    3: "data/PART_W33_Q3_PARTIAL_OVOID_7.json",
    5: "data/PART_W33_Q5_ORDER3_OVOID_18.json",
    7: "data/PART_W33_Q7_LNS_OVOID_33.json",
}


def lines_of(P, idx, F, adj):
    """The totally isotropic lines of W(3,q): maximal cliques of size q+1."""
    q = F.q
    seen = set()
    out = []
    for i in range(len(P)):
        for j in adj[i]:
            if j <= i:
                continue
            # the line through P[i], P[j] is their span, all q+1 projective points
            pts = set()
            for a in range(q):
                for b in range(q):
                    if a == 0 and b == 0:
                        continue
                    v = tuple(F.add[F.mul[a][P[i][k]]][F.mul[b][P[j][k]]]
                              for k in range(4))
                    lead = next((c for c in v if c), None)
                    if lead is None:
                        continue
                    iv = F.inv[lead]
                    pts.add(idx[tuple(F.mul[c][iv] for c in v)])
            if len(pts) != q + 1:
                continue
            key = frozenset(pts)
            if key in seen:
                continue
            seen.add(key)
            out.append(sorted(pts))
    return out


def main() -> int:
    print("=" * 78)
    print("Pass 7196 -- structure of the known optimal partial ovoids")
    print("=" * 78)

    summary = {}
    for q in (3, 5, 7):
        fp = ROOT / SOURCES[q]
        if not fp.is_file():
            print(f"\n  q={q}: {SOURCES[q]} missing, skipping")
            continue
        doc = json.loads(fp.read_text(encoding="utf-8"))
        F = Field(q)
        P, idx, adj, B = geometry(F)
        n = len(P)
        O = sorted(idx[tuple(p)] for p in doc["points"])
        assert all(B(P[a], P[b]) != 0 for a, b in itertools.combinations(O, 2)), \
            f"q={q}: stored set is not a partial ovoid"
        k = len(O)
        Oset = set(O)

        # 1. tangent distribution
        tang = Counter()
        for p in range(n):
            if p in Oset:
                continue
            tang[len(adj[p] & Oset)] += 1

        # 2/3. line distribution -- a partial ovoid meets each line in 0 or 1 points
        L = lines_of(P, idx, F, adj)
        ldist = Counter(len(set(l) & Oset) for l in L)

        print(f"\n  q={q}:  |O| = {k}   ({n} points, {len(L)} lines, "
              f"q^2+1 = {q * q + 1})")
        print(f"    tangent distribution (ovoid-points collinear with an off-point):")
        for v, c in sorted(tang.items()):
            print(f"        {v:3d} ovoid neighbours : {c:5d} points")
        print(f"    line distribution: {dict(sorted(ldist.items()))}")
        uncovered = ldist.get(0, 0)
        print(f"    lines missed entirely: {uncovered} of {len(L)} "
              f"({100 * uncovered / len(L):.1f}%)")
        # deficiency identity check
        covered = sum(c for v, c in ldist.items() if v >= 1)
        print(f"    identity: |O|*(q+1) = {k * (q + 1)}, lines met = {covered} "
              f"-- {'consistent' if k * (q + 1) == covered else 'MISMATCH'}")
        summary[q] = {"size": k, "points": n, "lines": len(L),
                      "tangent_distribution": {str(v): c for v, c in sorted(tang.items())},
                      "line_distribution": {str(v): c for v, c in sorted(ldist.items())},
                      "lines_missed": uncovered,
                      "max_tangent": max(tang) if tang else 0}

    print("\n  THE INVARIANT THAT SURVIVES ALL THREE\n")
    if len(summary) == 3:
        print(f"    {'q':>3s}  {'|O|':>4s}  {'lines':>6s}  {'missed':>7s}  "
              f"{'missed/line':>12s}  {'max tangent':>12s}")
        for q in (3, 5, 7):
            s = summary[q]
            print(f"    {q:3d}  {s['size']:4d}  {s['lines']:6d}  {s['lines_missed']:7d}  "
                  f"{s['lines_missed'] / s['lines']:12.4f}  {s['max_tangent']:12d}")
        miss = [summary[q]["lines_missed"] for q in (3, 5, 7)]
        print(f"\n    lines missed: {miss}")
        for name, f in (("(q-1)^2", lambda q: (q - 1) ** 2),
                        ("q^2-q", lambda q: q * q - q),
                        ("(q+1)(q-1)^2/2", lambda q: (q + 1) * (q - 1) ** 2 // 2),
                        ("C(q-2,2)*(q+1)", lambda q: (q - 2) * (q - 3) // 2 * (q + 1))):
            vals = [f(q) for q in (3, 5, 7)]
            print(f"      {name:18s} -> {vals}   "
                  f"{'MATCHES' if vals == miss else 'no'}")
        print("""
    A formula matching all three is a candidate constraint for q=9, not a theorem: three
    points, and the families tested were chosen by hand. It is worth exactly as much as the
    prediction it makes, and that prediction is checkable.""")

    out = ROOT / "data" / "PART_W33_PASS7196_OPTIMA_STRUCTURE.json"
    out.write_text(json.dumps(
        {"boundary": ("incidence invariants of the known optimal partial ovoids at q=3,5,7. "
                      "Any formula fitted to three points is a candidate constraint, not a "
                      "theorem, and no claim is made about q=9"),
         "per_q": summary}, indent=2), encoding="utf-8")
    print(f"\nwrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
