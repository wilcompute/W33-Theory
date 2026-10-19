"""Pass 12073: the two-clock vacuum organises one generation into three triality-related families, each a singlet plus a
Q8-torsor, with family-diagonal mass couplings (Claude track; 12064, 12066, 12067).

For two non-collinear clocks p, q (common symmetry K = C2 x Q8), 27 = 1+1+1 + 8_v+8_s+8_c (12064). Exact results:
  1. Families. Each singlet f_i (a weight of the second clock's monomial) has inner product -2/3 with every weight of
     exactly one octet; F_i = {f_i} u 8_i gives 27 = F_0 + F_1 + F_2 (9 each), permuted cyclically by the triality ticks
     (12066).
  2. Q8-torsors. K acts on each octet through K/<-1> = Q8 (element orders 1:1, 2:1, 4:6), REGULARLY: each octet is a
     Q8-torsor (stabiliser of a weight = +-1).
  3. Yukawa monomials by family: 45 = 12 family-diagonal (4 per family, each f_i x y with x, y in 8_i) + 33 with one
     weight from each family. The diagonal ones pair each octet perfectly (4 pairs covering 8), and the pairing is the
     orbit partition of the central involution of Q8. The 33 cross monomials are the invariant singlet monomial
     f_0 f_1 f_2 (orbit 1) and 4 orbits of 8 of type 8_0 8_1 8_2.
Reading. A vacuum value along the second clock's monomial (the singlets f_i) gives each family a mass term pairing its
octet by the Q8 centre: the mass matrix is family-diagonal, with one parameter <f_i> per family; K allows the three to
differ, triality (re-choosing the clock) relates them. No hierarchy is predicted here.
Scope: Weyl-level weights and monomials; the identification of octets with physical families is a reading.
"""

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12066_time_turns_triality import model, orbits  # noqa: E402

OUT = ROOT / "data" / "w33_pass12073_three_families_of_one_plus_a_q8_torsor.json"


def main():
    checks, res = {}, {}
    M = model()
    G, p, far, L27, trip = M["G"], M["p"], M["far"], M["L27"], M["trip"]
    q = far[0]
    K = M["H"](p) & M["H"](q)
    acts = [M["act27"](g) for g in G[K]]
    orb = orbits(acts, 27)
    eights = [sorted(o) for o in orb if len(o) == 8]
    f = sorted(k for o in orb if len(o) == 1 for k in o)
    fam = {}
    for fi in f:
        cands = [e for e in eights if all(int(round(3 * L27[fi] @ L27[x])) == -2 for x in e)]
        fam[fi] = cands[0] if len(cands) == 1 else None
    checks["each singlet is at -2/3 from exactly one octet: three families F_i = 1 + 8"] = (
        None not in fam.values() and len({tuple(v) for v in fam.values()}) == 3)
    famof = {}
    for i, fi in enumerate(f):
        famof[fi] = i
        for x in fam[fi]:
            famof[x] = i

    def order(pm):
        x, n = list(pm), 1
        while x != list(range(8)):
            x = [pm[i] for i in x]
            n += 1
        return n
    q8 = True
    for fi, e in fam.items():
        perms = {tuple(e.index(a[k]) for k in e) for a in acts}
        q8 &= len(perms) == 8 and Counter(order(pm) for pm in perms) == Counter({1: 1, 2: 1, 4: 6})
        q8 &= all(len({a[e[0]] for a in acts}) == 8 for _ in [0])
    checks["K acts on each octet through Q8 (orders 1:1, 2:1, 4:6), regularly (a Q8-torsor)"] = bool(q8)
    types = Counter(tuple(sorted(famof[k] for k in t)) for t in trip)
    res["family_types"] = {str(k): v for k, v in types.items()}
    checks["45 = 12 family-diagonal (4 per family) + 33 one-from-each-family"] = types == Counter({(0, 0, 0): 4, (1, 1, 1): 4, (2, 2, 2): 4, (0, 1, 2): 33})
    pair_ok = True
    for fi, e in fam.items():
        diag = [t for t in trip if {famof[k] for k in t} == {famof[fi]}]
        pair_ok &= all(fi in t for t in diag)
        pairs = {tuple(sorted(set(t) - {fi})) for t in diag}
        centre = None
        for a in acts:
            pm = tuple(e.index(a[k]) for k in e)
            if order(pm) == 2:
                centre = a
        cpairs = {tuple(sorted((x, centre[x]))) for x in e}
        pair_ok &= len(pairs) == 4 and len(set(sum(map(list, pairs), []))) == 8 and pairs == cpairs
    checks["the diagonal monomials f_i x y pair each octet perfectly, by the orbits of the Q8 centre"] = bool(pair_ok)
    seen, tor = set(), []
    for t in trip:
        if t not in seen:
            o = {tuple(sorted(a[k] for k in t)) for a in acts}
            seen |= o
            tor.append(o)
    cross = sorted(len(o) for o in tor if len({famof[k] for k in next(iter(o))}) == 3)
    checks["cross monomials: f_0 f_1 f_2 invariant (orbit 1) + 4 orbits of 8 of type 8_0 8_1 8_2"] = (
        cross == [1, 8, 8, 8, 8] and any(o == {tuple(f)} for o in tor))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
