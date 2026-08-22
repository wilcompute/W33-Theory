"""Pass 7202 -- independently verifying the other lane's E8/D4 counts, and correcting myself.

MY OWN FRAMING WAS WRONG FIRST. I proposed testing whether 10 is MAXIMAL for a "ten-D4
spread". It is not a maximum, it is forced: D4 has 24 roots, E8 has 240, and 240/24 = 10
exactly. A partition of the E8 roots into D4 root systems has ten parts by arithmetic, and
there is nothing to optimise. Recording that because it was my idea and it was empty.

WHAT IS ACTUALLY CHECKABLE, and worth checking under the cross-lane protocol in CLAUDE.md.
The other lane reports, from its own enumeration:

    122,850  orthogonal four-frames of root lines
      9,450  of those satisfying the D4 half-sum criterion
      3,150  D4 root subsystems in E8   (= 9,450 / 3)
    221,184  = |W(E8)| / 3150 = |N_{W(E8)}(D4)|

This rebuilds E8 from scratch and recomputes all four, by a route that does not reuse their
code. Roots are carried in DOUBLED coordinates so everything stays integral: the 112 vectors
(+-2,+-2,0^6) and the 128 vectors (+-1)^8 with an even number of minus signs, all of norm 8.

A count that agrees is a genuine cross-lane confirmation. A count that disagrees is worth
more, and would be reported as such rather than smoothed over.

    py -3 analysis/w33_pass7202_e8_d4_independent_check.py
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CLAIMED = {"four_frames": 122850, "d4_frames": 9450, "d4_subsystems": 3150,
           "normaliser": 221184}
W_E8 = 696729600


def e8_roots():
    R = []
    for i, j in itertools.combinations(range(8), 2):
        for si in (2, -2):
            for sj in (2, -2):
                v = [0] * 8
                v[i], v[j] = si, sj
                R.append(tuple(v))
    for signs in itertools.product((1, -1), repeat=8):
        if signs.count(-1) % 2 == 0:
            R.append(tuple(signs))
    return R


def main() -> int:
    print("=" * 78)
    print("Pass 7202 -- independent recount of the E8 / D4 numbers")
    print("=" * 78)

    R = e8_roots()
    print(f"\n  E8 roots built: {len(R)}   (expect 240)")
    assert len(R) == 240
    norms = {sum(x * x for x in r) for r in R}
    print(f"  norms (doubled coords): {norms}   (expect {{8}})")
    assert norms == {8}

    # root LINES: identify r with -r
    lines = []
    seen = set()
    for r in R:
        if r in seen:
            continue
        neg = tuple(-x for x in r)
        seen.add(r)
        seen.add(neg)
        lines.append(r)
    L = len(lines)
    print(f"  root lines: {L}   (expect 120)")
    assert L == 120

    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))

    orth = [set() for _ in range(L)]
    for i in range(L):
        for j in range(i + 1, L):
            if dot(lines[i], lines[j]) == 0:
                orth[i].add(j)
                orth[j].add(i)
    deg = len(orth[0])
    print(f"  orthogonality graph on lines: degree {deg}", flush=True)

    # 4-cliques = orthogonal four-frames
    frames = []
    for a in range(L):
        Na = {x for x in orth[a] if x > a}
        for b in sorted(Na):
            Nb = Na & orth[b]
            for c in sorted(x for x in Nb if x > b):
                for d in sorted(x for x in (Nb & orth[c]) if x > c):
                    frames.append((a, b, c, d))
    print(f"  orthogonal four-frames: {len(frames)}   "
          f"claimed {CLAIMED['four_frames']}   "
          f"{'AGREES' if len(frames) == CLAIMED['four_frames'] else 'DISAGREES'}",
          flush=True)

    # D4 half-sum criterion: (a+b+c+d)/2 is a root, for some choice of signs
    rootset = set(R)

    def is_d4_frame(f):
        vs = [lines[i] for i in f]
        for signs in itertools.product((1, -1), repeat=3):
            s = list(vs[0])
            for k, sg in enumerate(signs):
                s = [s[t] + sg * vs[k + 1][t] for t in range(8)]
            if all(x % 2 == 0 for x in s):
                h = tuple(x // 2 for x in s)
                if h in rootset:
                    return True
        return False

    d4f = [f for f in frames if is_d4_frame(f)]
    print(f"  frames meeting the D4 half-sum criterion: {len(d4f)}   "
          f"claimed {CLAIMED['d4_frames']}   "
          f"{'AGREES' if len(d4f) == CLAIMED['d4_frames'] else 'DISAGREES'}", flush=True)

    # group frames into D4 subsystems: the D4 spanned by a frame is the set of
    # roots lying in its rational span
    subs = {}
    for f in d4f:
        basis = [lines[i] for i in f]
        key = frozenset(
            r for r in R
            if all(dot(r, b) * dot(b, b) == dot(r, b) * dot(b, b) for b in basis)
            and _in_span(r, basis))
        subs.setdefault(key, []).append(f)
    ns = len(subs)
    per = sorted({len(v) for v in subs.values()})
    sizes = sorted({len(k) for k in subs})
    print(f"  distinct D4 subsystems: {ns}   claimed {CLAIMED['d4_subsystems']}   "
          f"{'AGREES' if ns == CLAIMED['d4_subsystems'] else 'DISAGREES'}")
    print(f"    frames per subsystem: {per}   (claimed 3)")
    print(f"    roots per subsystem : {sizes}   (D4 has 24)")

    norm = W_E8 // ns if ns else 0
    print(f"  |N_W(E8)(D4)| = |W(E8)|/{ns} = {norm}   claimed {CLAIMED['normaliser']}   "
          f"{'AGREES' if norm == CLAIMED['normaliser'] else 'DISAGREES'}")

    print(f"""
  ON THE "TEN-D4 SPREAD". Ten is FORCED, not maximal: 240 E8 roots / 24 roots per D4 = 10
  exactly, so any partition of the roots into D4 systems has ten parts. My proposal to search
  for a larger one was empty and is withdrawn.""")

    res = {"four_frames": len(frames), "d4_frames": len(d4f), "d4_subsystems": ns,
           "normaliser": norm}
    agree = {k: res[k] == CLAIMED[k] for k in CLAIMED}
    out = {
        "boundary": ("independent recount of four E8/D4 numbers reported by the other lane, "
                     "from a fresh construction. Agreement is confirmation; disagreement "
                     "would be reported as such. Says nothing about their scheme or Krein "
                     "results, which are not recomputed here"),
        "claimed": CLAIMED, "recomputed": res, "agreement": agree,
        "all_agree": all(agree.values()),
        "my_withdrawn_idea": ("that 10 might not be maximal for a ten-D4 spread; 10 is forced "
                              "by 240/24 and there is nothing to optimise"),
    }
    fp = ROOT / "data" / "PART_W33_PASS7202_E8_D4_RECOUNT.json"
    fp.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\n  all four agree: {all(agree.values())}")
    print(f"wrote {fp.relative_to(ROOT).as_posix()}")
    return 0


def _in_span(r, basis):
    """Is r in the rational span of the four orthogonal basis vectors?"""
    acc = [0] * 8
    for b in basis:
        num = sum(x * y for x, y in zip(r, b))
        den = sum(x * x for x in b)
        for t in range(8):
            acc[t] += num * b[t] / den
    return all(abs(acc[t] - r[t]) < 1e-9 for t in range(8))


if __name__ == "__main__":
    raise SystemExit(main())
