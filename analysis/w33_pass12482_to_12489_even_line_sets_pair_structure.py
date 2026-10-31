"""Passes 12482-12489 (Claude track): minimal even line sets of W(3,q) over every GF(q), and their pair structure.

12482 -- even_line_sets_gf.py builds W(3,q) over GF(p^k) (12467/12474 were prime-q only).  Controls q = 2, 3, 5 reproduce 6, 10, 20;
  q = 4 and 8 give 10 and 18 = 2(q+1) instantly: the KNOWN minimum weight of the binary dual code for q even (grids; Kim-Mellinger-
  Storme 2007, cited by Pepe-Storme-Van de Voorde 2010) -- a control, not a result.
12483 -- q = 3 completely: exactly 216 minimum even line sets (CP-SAT enumeration, one worker), ONE PSp(4,3)-orbit (stabiliser order
  120), every one with intersection graph K_{5,5} minus a perfect matching; none is twin-paired; weights 1..9 infeasible (control).
12484 -- q = 5: the optimum found is twin-paired -- 10 pairs of disjoint lines, each pair's perp {L,L'}^perp (its q+1 = 6 common
  transversals) lying inside the set as 3 other pairs -- and the pair graph is the PETERSEN graph.
12485 -- lemma (proof in the md): in W(q), q odd, a coverage-{0,2} even line set has twin classes of size <= 2, and if every class is a
  pair the pair graph is ((q+1)/2)-regular of girth >= 5 (lines of W(q) are antiregular).  Hence |S| >= 2 + (q+1)^2/2, with equality
  iff the pair graph is a Moore graph: q in {3, 5, 13, 113} only (Hoffman-Singleton).  q = 5 attains it (Petersen); q = 3 does not
  (12483: no twin-paired optimum), though its minimum 10 equals the bound.
12486 -- q = 7 structure of the exact optimum 40 (rerun over GF(7) with the lines saved), when present.
12487 -- q = 9 (GF(9)), when present.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "search_drivers_12466"
OUT = ROOT / "data" / "w33_pass12482_to_12489_even_line_sets_pair_structure.json"


def load(name):
    p = D / name
    return json.loads(p.read_text()) if p.exists() else None


def main():
    checks, res = {}, {}
    gf = {q: load(f"even_line_sets_gf_q{q}.json") for q in (2, 3, 4, 5)}
    gf[8] = load("even_line_sets_gf_q8_sym2.json")
    res["12482_minima"] = {q: r["min_even_line_set"] for q, r in gf.items()}
    checks["12482: GF(q) driver reproduces the prime-q minima 6, 10, 20 at q = 2, 3, 5 (optimal, verified even)"] = all(
        gf[q]["optimal"] and gf[q]["verified_even"] for q in (2, 3, 5)) and [gf[q]["min_even_line_set"] for q in (2, 3, 5)] == [6, 10, 20]
    checks["12482: q = 4, 8 give 2(q+1) = 10, 18 (the known even-q minimum weight; control)"] = (
        gf[4]["optimal"] and gf[8]["optimal"] and gf[4]["min_even_line_set"] == 10 and gf[8]["min_even_line_set"] == 18)
    ps = load("pair_structure.json"); orb = load("orbit_q3.json")
    e3 = ps["q3_enumeration"]
    res["12483"] = dict(count=e3["count"], orbit=orb, control=e3["control_weight_1_to_9"])
    spec = list(e3["spectrum_classes"].values())
    checks["12483: q = 3 has exactly 216 minimum even line sets, one PSp(4,3)-orbit (stabiliser order 120), none below 10"] = (
        e3["status"] == "OPTIMAL" and e3["count"] == 216 and orb["one_orbit"] and orb["stabiliser_order_in_PSp43"] == 120
        and e3["control_weight_1_to_9"] == "INFEASIBLE")
    checks["12483: all 216 have intersection graph K55 minus a matching (spectrum +-4, +-1^4) and none is twin-paired"] = (
        spec == [216] and "-4.0" in list(e3["spectrum_classes"])[0] and e3["twin_classes"] == {"(False, None, None)": 216})
    p5 = ps["q5_plain"]
    res["12484"] = p5
    checks["12484: the q = 5 optimum is twin-paired, every perp lies inside, and the pair graph is the Petersen graph (girth 5)"] = (
        p5["twin_paired"] and p5["perps_inside"] and p5["pair_graph_is_petersen"] and p5["pair_graph_girth"] == 5
        and p5["pair_graph_n"] == p5["moore_bound_pairs"] == 10)
    o5 = load("orbit_q5.json")
    res["12484_orbit"] = o5
    checks["12484: the Petersen set has PSp(4,5)-orbit 4875 and stabiliser order 960 = 8 * |Aut(Petersen)|"] = (
        o5["orbit_size"] == 4875 and o5["stabiliser_order"] == 960 and o5["divides"])
    bound = {q: 2 + (q + 1) ** 2 // 2 for q in (3, 5, 7, 9, 13, 113)}
    res["12485_twin_paired_bound"] = bound
    res["12485_moore_q"] = [2 * k - 1 for k in (2, 3, 7, 57)]
    checks["12485: Moore degrees 2, 3, 7, 57 correspond to q = 3, 5, 13, 113 and the bound 2 + (q+1)^2/2 is 10, 20, 100, 6500"] = (
        res["12485_moore_q"] == [3, 5, 13, 113] and [bound[q] for q in (3, 5, 13, 113)] == [10, 20, 100, 6500])
    for q, key in ((7, "q7_sym2"), (9, "q9_sym2")):
        r = load(f"even_line_sets_gf_q{q}_sym2.json")
        if r:
            res[f"q{q}"] = {k: v for k, v in r.items() if k != "chosen_lines"}
            if key in ps:
                res[f"q{q}_structure"] = ps[key]
    if res.get("q7"):
        checks["12486: the GF(7) rerun reproduces the exact q = 7 minimum 40 of 12474 (optimal, verified even)"] = (
            res["q7"]["optimal"] and res["q7"]["min_even_line_set"] == 40 and res["q7"]["verified_even"])
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
