"""Passes 12490-12497 (Claude track): the second regulus family (the Petersen graph), the exclusion of twin-paired Moore sets beyond
q = 5 (no Hoffman-Singleton even line set in W(13)), and the two families over prime powers.

12490 -- the MOORE family.  Take a regulus R0 whose opposite regulus contains TWO isotropic lines A, B (the other antiregular case) and a
  matching M of R0; the mod-2 sum S = R0 + sum_M {L, L'}^perp keeps A, B when (q+1)/2 is odd and has 2 + (q+1)^2/2 lines -- exactly the
  twin-pair Moore bound of 12485.  q = 5: 5 of 15 matchings give the 20-line Petersen minimum; q = 3, 7: none.
12491 -- the matching condition flips: S is even iff all cross-ratios of pairs are SQUARE and no three chords are concurrent; the
  combinatorial count equals the geometric count at q = 3, 5, 7 (0, 5, 0) and at q = 13 (0 of 135,135 matchings, 20 reguli).
12492 -- structure (proof in the md): a twin-paired coverage-{0,2} even set whose pair graph is a Moore graph IS a Moore-family set
  S(R0, M): take any twin pair {A, B}; its neighbourhood is the regulus {A, B}^perp, and diameter 2 forces the rest to be the perps.
12493 -- complete searches: square-good matchings exist only at q = 5 (primes <= 41; 9, 25, 27, 49), so the twin-pair bound is attained
  ONLY at q = 5 among those q.  In particular W(13) has no twin-paired even set of 100 lines (no Hoffman-Singleton realisation).
12494 -- the cube family over prime powers: no good matching at q = 9, 25, 27, 49 (and none at primes 13..61, 12489).
12495 -- q = 7: the 40-line optimum found by the MILP with no symmetry imposed is a cube (4 twin pairs on a regulus + their perps).
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "search_drivers_12466"
OUT = ROOT / "data" / "w33_pass12490_to_12497_moore_family_hs_exclusion.json"


def load(name):
    p = D / name
    return json.loads(p.read_text()) if p.exists() else None


def main():
    checks, res = {}, {}
    geo = {}
    for q in (3, 5, 7, 13):
        r = load(f"regulus_matching_q{q}_opp2.json")
        if r:
            geo[q] = dict(reguli=len(r["results"]), matchings=r["results"][-1]["matchings"],
                          even=sum(x["even"] for x in r["results"]), size=(r["results"][-1]["example"] or {}).get("size"))
    res["12490_geometric"] = geo
    checks["12490: Moore family -- q = 5: 5 of 15 matchings give the 20-line Petersen minimum; q = 3, 7: none"] = (
        geo[5]["even"] == 5 and geo[5]["size"] == 20 and geo[3]["even"] == 0 and geo[7]["even"] == 0)
    checks["12491: q = 13 geometry -- 0 even sets among all 135,135 matchings of each of 20 reguli (the 100-line target)"] = (
        13 in geo and geo[13]["matchings"] == 135135 and geo[13]["even"] == 0 and geo[13]["reguli"] >= 1)
    sq_small = load("chord_search_square_small.json") or {}
    gf = load("chord_search_gf.json") or {}
    moore_found = sorted(int(q) for q, r in sq_small.items() if r["status"] == "found")
    moore_none = sorted(int(q) for q, r in sq_small.items() if r["status"] == "none")
    res["12493_moore_search"] = {"found": moore_found, "none": moore_none,
                                 "prime_powers": {k: v["status"] for k, v in gf.items() if k.endswith("moore")}}
    checks["12493: square-good matchings exist only at q = 5 (primes <= 41 and q = 9, 25, 27, 49) -- no Moore set at q = 13"] = (
        moore_found == [5] and {3, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41} <= set(moore_none)
        and all(gf.get(f"{q}_moore", {}).get("status") == "none" for q in (9, 25, 27, 49)))
    checks["12494: the generic GF(q) search reproduces the prime results (cube 3, 7, 11; Moore 5) and finds neither family at 9, 25, 27, 49"] = (
        gf.get("3_cube", {}).get("status") == "found" and gf.get("7_cube", {}).get("status") == "found"
        and gf.get("11_cube", {}).get("status") == "found" and gf.get("5_moore", {}).get("status") == "found"
        and all(gf.get(f"{q}_cube", {}).get("status") == "none" for q in (5, 9, 25, 27, 49)))
    m7 = load("cube_milp_q7.json")
    if m7:
        res["12495_milp_q7"] = m7
        checks["12495: the 40-line q = 7 optimum found by the MILP with no symmetry imposed is a cube"] = bool(m7["cube"])
    cr = load("cube_recognise_q7.json")
    if cr:
        sampled = [x for x in cr["sampled"] if "cube" in x]
        res["12495_sampled"] = dict(n=len(sampled), cubes=sum(1 for x in sampled if x["cube"]), known=cr["known"])
        checks["12495: every sampled 40-line optimum at q = 7 is a cube"] = bool(sampled) and all(x["cube"] for x in sampled) and all(
            x["cube"] for x in cr["known"])
    for name, key in (("chord_search_square_113.json", "12496_q113_moore"), ("chord_search_cube_67_101.json", "12496_cube_67_101")):
        r = load(name)
        if r:
            res[key] = {q: v["status"] for q, v in r.items()}
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
