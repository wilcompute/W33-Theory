"""Pass 11703: the chirality vacuum and the SM-shaped clock select the same W(3,3) line -- every SM-shaped breaking by
commuting third-level clocks from Z(x)I is a trinification breaking on the line <Z1, Z2>.

Setting.  L = <Z1, Z2> is a Lagrangian line; its four points q = Z1^a Z2^b each own an SU(3)_q (Pass 11687), and the
centraliser of the line is the sum of the four (A2^4).  Its stabiliser states |x0 y0> with (x0, y0) != 0 are 8 of the 320
vacua of Pass 11698 (kernel point p = {q : a x0 + b y0 = 0}).  Every diagonal clock fixes every |x0 y0> up to phase.

FOUND (all 59049 third-level diagonal clock elements paired with Z(x)I, the E6 x SU(3) lift):
  * 1944 pairs leave an SM-shaped joint centraliser su(3) + su(2) + u(1)^5;
  * in EVERY one, the colour su(3) equals one of the four SU(3)_q of L (none outside), and the su(2) lies inside the
    SU(3)_q' of a DIFFERENT point q' of the same line;
  * the 9 realised ordered pairs (colour point, weak point) each occur 216 times (the 3 pairs with the weak point Z1,
    the first clock's own point, never occur).
Reading: SM-shaped breaking by commuting clocks is trinification breaking SU(3)_C x SU(3)_L -> SU(3)_C x SU(2)_L on a
W(3,3) line, and the clocks fix that line's stabiliser vacua.  For each (colour q, weak q') there are exactly 4 vacua
(2 kernels p outside {q, q'} x 2 conjugate characters) in which BOTH the colour point and the weak point carry the
selected C x T-odd sign Im<D> = +-sqrt3/2.  Scope: compatibility of two selections on one line; no dynamics is derived
that forces this alignment, and the 5 u(1)s (hypercharge) are not resolved.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11697_11698_chirality_vacuum as V  # noqa: E402
import w33_pass11701_11702_clock_symmetry_breaking as B  # noqa: E402

OUT = ROOT / "data" / "w33_pass11703_vacuum_and_clock_share_a_line.json"
POINTS = [(0, 1), (1, 0), (1, 1), (1, 2)]          # q = Z1^a Z2^b, labelled (a, b)


def comps(mask):
    idx = np.nonzero(mask)[0]
    R = B.RV[idx]
    G = R @ R.T
    n = len(R)
    comp = -np.ones(n, int)
    c = 0
    for s0 in range(n):
        if comp[s0] < 0:
            st = [s0]
            comp[s0] = c
            while st:
                a = st.pop()
                for b in np.nonzero((np.abs(G[a]) > 1e-9) & (comp < 0))[0]:
                    comp[b] = c
                    st.append(b)
            c += 1
    return [frozenset(idx[comp == k]) for k in range(c)]


def lift_mask(f, k):
    return B.kept(B.lifts(B.Z9 ** np.array([f(x, y) % 9 for x, y in B.XY]))[k])


def main():
    su3 = {}
    for a, b in POINTS:
        for k in range(3):
            m = lift_mask(lambda x, y, a=a, b=b: 3 * (a * x + b * y), k)
            if B.typ(m) == ("A2", "E6"):
                su3[(a, b)] = [c for c in comps(m) if len(c) == 6][0]
    line_centraliser = lift_mask(lambda x, y: 3 * x, 0) & lift_mask(lambda x, y: 3 * y, 0)
    union_ok = set().union(*su3.values()) == set(np.nonzero(line_centraliser)[0])
    g1 = lift_mask(lambda x, y: 3 * x, 0)
    pairs, outside, simplest = Counter(), 0, {}
    for w, g, lam in B.third_level():
        m = g1 & B.kept(lam)
        if m.sum() != 8 or B.typ(m) != ("A1", "A2"):
            continue
        cs = comps(m)
        col = [c for c in cs if len(c) == 6][0]
        su2 = [c for c in cs if len(c) == 2][0]
        cq = [q for q, s in su3.items() if col == s]
        wq = [q for q, s in su3.items() if su2 <= s]
        if not cq or not wq:
            outside += 1
            continue
        key = f"colour {cq[0]} weak {wq[0]}"
        pairs[key] += 1
        if key not in simplest or w < simplest[key][0]:
            simplest[key] = (w, B.show(g))
    # vacua of Pass 11698 on this line and their chirality-carrying points
    ops = {q: V.weyl((0, q[0], 0, q[1])) for q in POINTS}
    vac = []
    for x0 in range(3):
        for y0 in range(3):
            if (x0, y0) == (0, 0):
                continue
            psi = np.zeros(9, complex)
            psi[3 * x0 + y0] = 1
            im = {q: float(np.vdot(psi, ops[q] @ psi).imag) for q in POINTS}
            vac.append(dict(state=f"|{x0}{y0}>", kernel=[q for q in POINTS if abs(im[q]) < 1e-9],
                            signs={str(q): int(np.sign(round(im[q], 9))) for q in POINTS}))
    aligned = {}
    for key in pairs:
        cq = tuple(int(t) for t in key.split("colour (")[1].split(")")[0].split(", "))
        wq = tuple(int(t) for t in key.split("weak (")[1].split(")")[0].split(", "))
        aligned[key] = sum(1 for v in vac if v["signs"][str(cq)] != 0 and v["signs"][str(wq)] != 0)
    res = dict(pass_id=11703, su3_of_line_points_union_is_line_centraliser=union_ok,
               sm_shaped_pairs_with_Z_x_I=sum(pairs.values()) + outside, colour_or_weak_outside_line=outside,
               ordered_colour_weak_pairs={k: dict(count=v, simplest_second_clock=simplest[k][1]) for k, v in sorted(pairs.items())},
               line_vacua=vac, vacua_with_colour_and_weak_points_chiral=aligned)
    print(json.dumps(res, indent=1))
    json.dump(res, open(OUT, "w"), indent=1)


if __name__ == "__main__":
    main()
