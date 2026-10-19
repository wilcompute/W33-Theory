"""Pass 12067: which Yukawa monomials survive one and two clocks (Claude track; continues 12064, 12066).

The 45 tritangents of the 27 of E6(p) are the monomials of the E6 cubic invariant (the 27^3 Yukawa couplings). Exact
orbit structure under the vacuum symmetries (Weyl level, 12052 root model):
  * one clock (H_p, 432):              45 = 9 + 36; the 9 are exactly the clock's own far-point monomials (12064).
  * two non-collinear clocks (C2xQ8): ONE invariant monomial -- the second clock's; 45 = 1 + 8 + 4+4+4 + 8+8+8.
    With the triality ticks (Stab(p) n Stab(q), 48): 45 = 1 + 8 + 12 + 24.
  * two collinear clocks (+-1 x S3):  THREE invariant monomials, outside the 9; they are pairwise disjoint and are
    exactly the three 3-orbits of matter (27 = 3+3+3 + 6+6+6). The other 42 monomials fall in orbits 3^10 + 6^2.
Reading. An incompatible clock pair leaves a single invariant Yukawa coupling (a rank-one texture, the shape the
corpus's Weber law gives at leading order, 11872/11938); a compatible pair leaves three disjoint invariant couplings (a
diagonal three-family texture). Scope: invariance under the finite vacuum symmetry only; magnitudes, the continuous
E6 breaking and the generation assignment are not derived.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12066_time_turns_triality import model, orbits  # noqa: E402

OUT = ROOT / "data" / "w33_pass12067_yukawa_monomials_of_one_and_two_clocks.json"


def main():
    checks, res = {}, {}
    M = model()
    G, p, nb, far, trip = M["G"], M["p"], M["nb"], M["far"], M["trip"]
    cover = {M["mono"](x) for x in far}
    checks["45 monomials; the 27 far points give 9 of them"] = len(trip) == 45 and len(cover) == 9 and cover <= set(trip)

    def torb(mask):
        els = [M["act27"](g) for g in G[mask]]
        seen, out = set(), []
        for t in trip:
            if t not in seen:
                o = {tuple(sorted(a[k] for k in t)) for a in els}
                seen |= o
                out.append(o)
        return out
    q, qc = far[0], nb[0]
    one = torb(M["H"](p))
    res["one_clock"] = sorted(len(o) for o in one)
    checks["one clock: 45 = 9 + 36, the 9 = the clock's far-point monomials"] = sorted(map(len, one)) == [9, 36] and any(o == cover for o in one)
    farp = torb(M["H"](p) & M["H"](q))
    res["far_pair"] = sorted(len(o) for o in farp)
    checks["two non-collinear clocks: one invariant monomial = the second clock's; 1+8+4+4+4+8+8+8"] = (
        sorted(map(len, farp)) == [1, 4, 4, 4, 8, 8, 8, 8] and {M["mono"](q)} in farp)
    tri = torb(M["S"](p) & M["S"](q))
    res["far_pair_with_triality"] = sorted(len(o) for o in tri)
    checks["with the triality ticks: 1 + 8 + 12 + 24"] = sorted(map(len, tri)) == [1, 8, 12, 24]
    mask = M["H"](p) & M["H"](qc)
    colp = torb(mask)
    res["collinear_pair"] = sorted(len(o) for o in colp)
    fixed = [next(iter(o)) for o in colp if len(o) == 1]
    m27 = orbits([M["act27"](g) for g in G[mask]], 27)
    threes = {tuple(sorted(o)) for o in m27 if len(o) == 3}
    checks["two collinear clocks: three invariant monomials, disjoint, outside the 9, = the three 3-orbits of matter"] = bool(
        len(fixed) == 3 and len(set(sum(map(list, fixed), []))) == 9 and not (set(fixed) & cover) and set(fixed) == threes
        and sorted(map(len, m27)) == [3, 3, 3, 6, 6, 6])
    checks["collinear pair: remaining 42 monomials in orbits 3^10 + 6^2"] = sorted(map(len, colp)) == [1, 1, 1] + [3] * 10 + [6, 6]
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
