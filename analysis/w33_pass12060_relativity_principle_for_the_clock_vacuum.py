"""Pass 12060: a relativity principle for the clock vacuum (Claude track; continues 12059).

A clock vacuum at an event p (12055-12057 condense one event; 12052 its three clock real forms) has symmetry H_p, the
unique index-3 subgroup of the point stabiliser (12059). An observer is a Kramers reversal J (36 up to sign, 11831); a
symmetry g fixes the observer when g J g^-1 = +-J (Lorentz or parity coset). Exact results (Sp(4,3) is transitive on
points and on ordered collinear and non-collinear pairs, so one base event and all partners cover every case):
  1. Relativity. H_p is transitive on the 36 observers: a one-clock vacuum chooses a time but no rest frame.
  2. Two collinear clocks (p, q in one context, i.e. jointly measurable events): common symmetry H_p n H_q has order 12
     (orders 1:1, 2:7, 3:2, 6:2, i.e. +-1 x S_3). It fixes exactly THREE observers, and they are exactly the J with
     Jp = q: the frames in which the two events are each other's time reverse. (9 observers have the line pq in their
     sky; J pairs its four events, and the three pairings give the three frames' classes.)
  3. Two non-collinear clocks: common symmetry has order 16 (orders 1:1, 2:3, 4:12, i.e. 2 x Q8 -- pure spin, no
     translations); its observer orbits are 4,4,4,8,8,8, so no observer is fixed.
Reading. A single clock is Lorentz-democratic (a relativity principle); a rest frame appears only with a second,
compatible clock, and then it is the mirror frame of the pair. Two incompatible clocks leave only rotations.
Scope: finite-group statements with the corpus's stabiliser-defined names; 'rest frame' = observer fixed by the
vacuum symmetry. With three or more clocks the common symmetry drops to +-1 or order 4, which fixes observers
vacuously; no claim is made there.
"""

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass12059_observers_see_space_not_time as M  # noqa: E402

OUT = ROOT / "data" / "w33_pass12060_relativity_principle_for_the_clock_vacuum.json"


def main():
    checks, res = {}, {}
    pts = sorted({M.norm(v) for v in M.VEC if v.any()})
    G = M.build_group(pts)
    _, Js = M.kramers()
    GV = np.einsum("gij,vj->gvi", G, M.VEC) % 3
    vidx = lambda v: int(np.dot(np.asarray(v) % 3, [27, 9, 3, 1]))  # noqa: E731
    Jkey = {}
    for i, J in enumerate(Js):
        Jkey[M.key(J)] = i
        Jkey[M.key(2 * J)] = i
    Om_inv = (2 * M.Om) % 3  # Om^2 = -1

    def clock_group(p):
        pv = np.array(p)
        fix_line = np.array([M.norm(x) == p for x in GV[:, vidx(pv)]])
        perp = [v for v in M.VEC if M.om(pv, v) == 0]
        a = next(v for v in perp if v.any() and M.norm(v) != p)
        b = next(v for v in perp if v.any() and M.om(a, v))
        quo = {}
        for i, j, k in itertools.product(range(3), repeat=3):
            quo[M.key((i * a + j * b + k * pv) % 3)] = (i, j)
        Hm = np.zeros(len(G), bool)
        for g in np.nonzero(fix_line)[0]:
            Mm = np.array([quo[M.key(GV[g, vidx(x)])] for x in (a, b)]).T % 3
            Hm[g] = M.order(Mm) in (1, 2, 4)
        return Hm, fix_line

    def perm_on_observers(mask):
        return np.array([[Jkey[M.key((G[g] @ J @ Om_inv @ G[g].T @ M.Om) % 3)] for J in Js] for g in np.nonzero(mask)[0]])

    def orbit_sizes(perm):
        seen, out = set(), []
        for j in range(36):
            if j not in seen:
                o = set(perm[:, j].tolist())
                seen |= o
                out.append(len(o))
        return sorted(out)

    def orders(mask):
        return dict(sorted(Counter(M.order(G[g]) for g in np.nonzero(mask)[0]).items()))

    allmask = np.ones(len(G), bool)
    checks["control: Sp(4,3) is transitive on the 36 observers"] = orbit_sizes(perm_on_observers(allmask)) == [36]
    p = pts[0]
    pv = np.array(p)
    Hp, Sp_ = clock_group(p)
    res["H_p_order"] = int(Hp.sum())
    res["H_p_observer_orbits"] = orbit_sizes(perm_on_observers(Hp))
    checks["relativity: H_p (432) is transitive on the 36 observers (no rest frame from one clock)"] = (
        res["H_p_order"] == 432 and res["H_p_observer_orbits"] == [36])
    col, far = Counter(), Counter()
    mirror_ok = True
    for q in pts[1:]:
        qv = np.array(q)
        Hq, _ = clock_group(q)
        both = Hp & Hq
        perm = perm_on_observers(both)
        fixed = sorted(j for j in range(36) if set(perm[:, j].tolist()) == {j})
        if M.om(pv, qv) == 0:
            mirror = sorted(j for j in range(36) if M.norm(Js[j] @ pv) == q)
            mirror_ok &= fixed == mirror and len(fixed) == 3
            col[(int(both.sum()), str(orders(both)), str(orbit_sizes(perm)))] += 1
        else:
            far[(int(both.sum()), str(orders(both)), str(orbit_sizes(perm)), len(fixed))] += 1
    res["collinear_pairs"] = {str(k): v for k, v in col.items()}
    res["noncollinear_pairs"] = {str(k): v for k, v in far.items()}
    checks["two collinear clocks: common symmetry +-1 x S3 (12; orders 1:1, 2:7, 3:2, 6:2), all 12 partners"] = (
        list(col) and all(k[0] == 12 and k[1] == str({1: 1, 2: 7, 3: 2, 6: 2}) for k in col) and sum(col.values()) == 12)
    checks["two collinear clocks fix exactly 3 observers = the J with Jp = q (mirror frames)"] = bool(mirror_ok)
    checks["two non-collinear clocks: common symmetry 2 x Q8 (16; orders 1:1, 2:3, 4:12), orbits 4,4,4,8,8,8, none fixed"] = (
        list(far) == [(16, str({1: 1, 2: 3, 4: 12}), str([4, 4, 4, 8, 8, 8]), 0)] and sum(far.values()) == 27)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
