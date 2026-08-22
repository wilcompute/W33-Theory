"""Pass 7237 -- what the 90 J-stable D4s are, in W(3,3) terms.

THE QUESTION. Pass 7229 showed the other lane's "90 D4s selected by W(3,3)" are exactly the
J-stable D4 subsystems of E8. That explains the selection but not the object: 90 is not 40
(points) and not 40 (lines), so what does a J-stable D4 correspond to inside the quadrangle?

WHAT IT CANNOT BE, established already. A LINE of W(3,3) pulls back to A2^4 -- 24 roots of
RANK 8. A D4 also has 24 roots but RANK 4. Same count, different objects, so lines are not
D4s and the coincidence 24 = 24 is exactly the sort this repo keeps having to disarm.

THE TEST. Each of the 90 J-stable D4s is 24 roots. The 40 J-stable A2s are 6 roots each. Ask
directly which A2s sit inside each D4 and what configuration they form in W(3,3): a point
set? a line? a perp? Then count how many D4s each A2 lies in, and check the incidence numbers
close.

ALSO HERE: how many distinct W(3,3) copies does E8 carry? Springer says the zeta_3-regular
class has centraliser G32 of order 155520, so there are 696729600/155520 = 4480
fixed-point-free order-3 elements. J and J^2 stabilise the same A2s, bounding the copies by
2240. This samples to see whether distinct J really do give distinct 40-sets.

    py -3 analysis/w33_pass7237_what_are_the_ninety.py
"""

from __future__ import annotations

import itertools
import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np  # noqa: E402
from w33_pass7217_ovoid_pullback_to_e8 import (  # noqa: E402
    CARTAN, roots_in_root_basis, simple_reflection, order_of,
)
from w33_pass7229_a2_census_of_e8 import all_a2_subsystems  # noqa: E402


def main() -> int:
    print("=" * 78)
    print("Pass 7237 -- what the 90 J-stable D4s are in W(3,3) terms")
    print("=" * 78)

    R = roots_in_root_basis()
    Rarr = np.array(R, dtype=np.int64)
    G = CARTAN
    I8 = np.eye(8, dtype=np.int64)
    gens = [simple_reflection(i) for i in range(8)]
    cox = I8.copy()
    for g in gens:
        cox = cox @ g
    J = np.linalg.matrix_power(cox, 10)

    def stable(fam, M):
        return {tuple(int(x) for x in (M @ np.array(v, dtype=np.int64)))
                for v in fam} == set(fam)

    A2s = all_a2_subsystems(Rarr, G)
    st = [f for f in A2s if stable(f, J)]
    print(f"\n  J-stable A2s (= points of W(3,3)): {len(st)}")

    # collinearity via A2 orthogonality
    def orth(f1, f2):
        return all(int(np.array(a) @ G @ np.array(b)) == 0 for a in f1 for b in f2)

    coll = [[False] * 40 for _ in range(40)]
    for i, j in itertools.combinations(range(40), 2):
        if orth(st[i], st[j]):
            coll[i][j] = coll[j][i] = True

    # build D4s, keep J-stable ones
    rootset = {tuple(int(x) for x in v) for v in Rarr}
    lines_v, seen = [], set()
    for v in Rarr:
        t = tuple(int(x) for x in v)
        if t in seen:
            continue
        seen.add(t)
        seen.add(tuple(-x for x in t))
        lines_v.append(np.array(t, dtype=np.int64))
    orthL = [[i != j and int(lines_v[i] @ G @ lines_v[j]) == 0 for j in range(120)]
             for i in range(120)]
    D4s = set()
    for a in range(120):
        Na = [x for x in range(a + 1, 120) if orthL[a][x]]
        for bi, b in enumerate(Na):
            Nb = [x for x in Na[bi + 1:] if orthL[b][x]]
            for ci, c in enumerate(Nb):
                for d in [x for x in Nb[ci + 1:] if orthL[c][x]]:
                    vs = [lines_v[a], lines_v[b], lines_v[c], lines_v[d]]
                    hit = False
                    for sg in itertools.product((1, -1), repeat=3):
                        s = vs[0].copy()
                        for k, g2 in enumerate(sg):
                            s = s + g2 * vs[k + 1]
                        if np.all(s % 2 == 0) and tuple(int(x) for x in (s // 2)) in rootset:
                            hit = True
                            break
                    if not hit:
                        continue
                    Gm = np.array([[int(u @ G @ w) for w in vs] for u in vs], dtype=float)
                    Gi = np.linalg.inv(Gm)
                    sub = []
                    for v in Rarr:
                        co = Gi @ np.array([int(v @ G @ u) for u in vs], dtype=float)
                        if np.allclose(sum(co[k] * vs[k] for k in range(4)),
                                       v.astype(float), atol=1e-7):
                            sub.append(tuple(int(x) for x in v))
                    if len(sub) == 24:
                        D4s.add(frozenset(sub))
    jd4 = [F for F in D4s if stable(F, J)]
    print(f"  D4s: {len(D4s)}, J-stable: {len(jd4)}")

    # which A2s sit inside each J-stable D4?
    prof = Counter()
    incid = Counter()
    configs = Counter()
    for F in jd4:
        inside = [i for i in range(40) if set(st[i]) <= F]
        prof[len(inside)] += 1
        for i in inside:
            incid[i] += 1
        if len(inside) >= 2:
            npairs = len(list(itertools.combinations(inside, 2)))
            ncoll = sum(1 for a, b in itertools.combinations(inside, 2) if coll[a][b])
            configs[(len(inside), ncoll, npairs)] += 1
    print(f"\n  J-stable A2s contained in each J-stable D4: {dict(sorted(prof.items()))}")
    print(f"  configuration (n_points, collinear pairs, total pairs): "
          f"{dict(sorted(configs.items()))}")
    if incid:
        c = Counter(incid.values())
        print(f"  D4s through each point: {dict(sorted(c.items()))}")
        tot = sum(incid.values())
        print(f"  incidence check: sum over D4s of |A2 inside| = {tot}"
              f"   = 90 * {tot / 90:.2f} = 40 * {tot / 40:.2f}")

    # how many distinct W(3,3) copies?
    rng = random.Random(7237)
    sets_seen = set()
    Js = 0
    for _ in range(6000):
        M = I8.copy()
        for _ in range(rng.randrange(2, 16)):
            M = M @ gens[rng.randrange(8)]
        o = order_of(M, 40)
        if o is None or o % 3:
            continue
        Jc = np.linalg.matrix_power(M, o // 3)
        if order_of(Jc, 4) != 3 or int(np.trace(Jc)) != -4:
            continue
        Js += 1
        sets_seen.add(frozenset(frozenset(f) for f in A2s if stable(f, Jc)))
        if Js >= 30:
            break
    print(f"\n  sampled {Js} fixed-point-free order-3 elements -> "
          f"{len(sets_seen)} distinct 40-point sets")
    print(f"    Springer: 696729600/155520 = 4480 such elements, so at most 2240 copies")
    print(f"    sample gives {len(sets_seen)}/{Js} distinct, consistent with each pair "
          f"{{J, J^2}} sharing a set")

    out = {"boundary": ("identifies what the 90 J-stable D4s contain in W(3,3) terms; the "
                        "count of distinct copies is a SAMPLE, not an enumeration"),
           "j_stable_a2": len(st), "d4_total": len(D4s), "d4_j_stable": len(jd4),
           "a2_per_d4": {str(k): v for k, v in sorted(prof.items())},
           "configurations": {str(k): v for k, v in sorted(configs.items())},
           "class_size_springer": 4480, "max_distinct_copies": 2240,
           "sampled_elements": Js, "distinct_sets_in_sample": len(sets_seen)}
    fp = ROOT / "data" / "PART_W33_PASS7237_WHAT_ARE_THE_NINETY.json"
    fp.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
