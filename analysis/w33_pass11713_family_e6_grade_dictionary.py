"""Pass 11713: three families on the two-qutrit levels -- the family SU(3), its E6 centraliser, and the grade of each
family multiplet.

Setting (Passes 11706-11708).  In the operator-type Standard Model of the two-qutrit E8 the nine levels split
9 = 5 + 1 + 3: five Georgi-Glashow levels F5, one vacuum level s, and three remaining "family" levels F3.  (Pass 11731
of the Codex track uses the same family SU(3) on levels 3,4,5 for its bundle obstruction and Pass 11732 for the
3875 Yukawa channel; they are cited, not re-derived.)

FOUND (worked configuration of Pass 11707, every choice of vacuum level among the four free levels):
  * the operator SU(3)_F rotating the three family levels has E8 centraliser exactly E6 (72 roots), containing the
    SM roots and the Georgi-Glashow SU(5): E8 > E6 x SU(3)_F is SU(9) > SU(6) x SU(3)_F with 6 = F5 + s;
  * the 81 roots of (27,3) split into three families of 27 (one per family level), and each family is spread over all
    three grades of e8 = sl9 + Lambda^3 + Lambda^3*:
        27 = 15 (three-fermion: two levels from F5 + s, one family level)
           + 6bar (operator: family level <- F5 + s) + 6bar (three-hole),
    i.e. under SU(5): 10 + 5 in the three-fermion grade, 5bar + 1 in each of the other two grades;
  * the E8 bracket between different families lands in the third: [27_f, 27_g] lies in (27bar, 3bar) with family weight
    -e_h (f, g, h distinct); same-family brackets vanish (the epsilon_fgh structure; the symmetric family channel needs
    the 3875, Pass 11732).
Branching of the W(3,3) T^6/Z3 vacuum spectrum (Pass 11714) under SU(5) x SU(3)_F: each untwisted 84 gives
(10,3) + (10,1) + (10bar,1) + (5,3) + (5,3bar) + (1,3bar) + (1,1)-type states, so its net tens are one family triplet
(10,3); three planes give 9 = 3 x 3 net tens, balanced by 27 twisted 5bar against 3 x 6 untwisted 5s.
Scope: group theory on the explicit E8; which levels are families in an actual vacuum is the subject of Pass 11715.
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11701_11702_clock_symmetry_breaking as B  # noqa: E402
import w33_pass11706_11709_vacuum_clock_hypercharge as H  # noqa: E402

OUT = ROOT / "data" / "w33_pass11713_family_e6_grade_dictionary.json"
XY, RV, KIND = B.XY, B.RV, H.KIND


def mask(f, k):
    return B.kept(B.lifts(B.Z9 ** np.array([f(x, y) % 9 for x, y in XY]))[k])


def configuration():
    m = mask(lambda x, y: 3 * x * y * y, 1) & mask(lambda x, y: x ** 3 + 3 * x * y + 3 * x * x * y, 1)
    comps = H.su5_completions(m)
    roots, Y = [(r, y) for r, y in comps.items() if all(KIND[H.RKEY[q]] == "A" for q in r)][0]
    F5 = sorted({t for q in roots for t in B.T.ROOTS[H.RKEY[q]][1]})
    return m, Y, F5


def family_dictionary(m, Y, F5, s):
    rest = [t for t in range(9) if t not in F5]
    F3 = [t for t in rest if t != s]
    fam_roots = [j for j in range(240) if KIND[j] == "A" and set(B.T.ROOTS[j][1]) <= set(F3)]
    cent = np.array([all(abs(RV[j] @ RV[f]) < 1e-9 for f in fam_roots) for j in range(240)])
    sm_idx = np.nonzero(m)[0]
    fund = {tuple(np.round(np.eye(3)[a] - 1 / 3, 6)): a for a in range(3)}
    by_fam = defaultdict(list)
    for j in range(240):
        v = RV[j][F3]
        w = tuple(np.round(v - v.mean(), 6))
        if w in fund:
            by_fam[fund[w]].append(j)
    grade = {"A": "operator", "L": "three-fermion", "Ld": "three-hole"}
    content = {}
    for a, js in by_fam.items():
        c = Counter()
        for j in js:
            nG = sum(1 for t in B.T.ROOTS[j][1] if t in F5)
            c[f"{grade[KIND[j]]}|GUT levels {nG}|Y {Fraction(float(RV[j] @ Y)).limit_denominator(6)}"] += 1
        content[str(XY[F3[a]])] = dict(sorted(c.items()))
    grade_split = {str(XY[F3[a]]): dict(Counter(grade[KIND[j]] for j in js)) for a, js in by_fam.items()}
    brackets = Counter()
    for f, g in itertools.product(range(3), repeat=2):
        for b in by_fam[f]:
            for c in by_fam[g]:
                k = H.RKEY.get(tuple(np.round(RV[b] + RV[c], 6)))
                if k is not None:
                    v = RV[k][F3]
                    brackets[(f, g, tuple(np.round(v - v.mean(), 3)))] += 1
    eps_structure = all((f != g) for (f, g, _) in brackets) and all(
        w == tuple(np.round(-(np.eye(3)[3 - f - g] - 1 / 3), 3)) for (f, g, w) in brackets)
    return dict(vacuum_level=str(XY[s]), family_levels=[str(XY[t]) for t in F3], centraliser=list(B.typ(cent)),
                sm_in_centraliser=bool(all(cent[j] for j in sm_idx)), roots_per_family={str(XY[F3[a]]): len(v) for a, v in by_fam.items()},
                grade_split=grade_split, content=content, bracket_counts={str(k): v for k, v in brackets.items()},
                epsilon_family_structure=bool(eps_structure))


def z3_branching():
    """Branch 3 x Lambda^3(9) + 27 x 9bar under SU(5) x SU(3)_F with 9 = 5 (G) + 1 (s) + 3 (F)."""
    G, S, F = range(5), [5], [6, 7, 8]
    cls = Counter()
    for T in itertools.combinations(range(9), 3):
        nG = sum(t in G for t in T)
        ns = sum(t in S for t in T)
        nF = sum(t in F for t in T)
        cls[(nG, ns, nF)] += 1
    names = {(3, 0, 0): "(10bar,1)", (2, 1, 0): "(10,1)", (2, 0, 1): "(10,3)", (1, 1, 1): "(5,3)", (1, 0, 2): "(5,3bar)",
             (0, 1, 2): "(1,3bar)", (0, 0, 3): "(1,1)"}
    per84 = {names[k]: v for k, v in cls.items()}
    net_tens_per_plane = (per84["(10,3)"] + per84["(10,1)"] - per84["(10bar,1)"]) // 10
    fives = (per84["(5,3)"] + per84["(5,3bar)"]) // 5
    return dict(per_84_states=per84, net_tens_per_plane=net_tens_per_plane, net_tens_family_triplet="(10,3)",
                planes=3, net_tens_total=3 * net_tens_per_plane, untwisted_fives=3 * fives, twisted_5bar=27,
                net_5bar=27 - 3 * fives)


def main():
    m, Y, F5 = configuration()
    rest = [t for t in range(9) if t not in F5]
    res = dict(pass_id=11713, gut_levels=[str(XY[t]) for t in F5],
               families=[family_dictionary(m, Y, F5, s) for s in rest if s != 0], z3_vacuum_branching=z3_branching())
    print(json.dumps(res, indent=1)[:3500])
    json.dump(res, open(OUT, "w"), indent=1)


if __name__ == "__main__":
    main()
