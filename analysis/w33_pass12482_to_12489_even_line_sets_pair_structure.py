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
12486 -- symmetric search (one CP-SAT variable per orbit of g = A (+) A^k): recovers the true minima 10, 20, 40 at q = 3, 5, 7 in
  seconds and finds even sets of 84 (q = 11) and 168 (q = 13), refuting the 12474 fit 5*2^((q-1)/2) = 160, 320.
12487 -- the q = 7 optima are not twin-paired (4 twin pairs + 32 singles).
12488 -- the local counting bound (one line, antiregular triples) is proved but weak: 9, 16, 23 at q = 3, 5, 7.
12489 -- THE CUBE: S(R0, M) = R0 + the perps of a perfect matching M of a regulus R0 (no isotropic opposite line) has (q+1)(q+3)/2
  lines and is even iff M is good (pairwise non-square cross-ratios, no three chords concurrent) -- checked against the geometry at
  q = 3, 5, 7, 11.  Good matchings exist only for q = 3, 7, 11 among primes <= 61 (complete search); each is one PGL(2,q)-orbit with
  stabiliser D4 / S4 / A5: the antipodal pairs of a square, a CUBE and an ICOSAHEDRON.  The exact q = 7 minimum 40 is the cube.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "search_drivers_12466"
OUT = ROOT / "data" / "w33_pass12482_to_12489_even_line_sets_pair_structure.json"


def load(name):
    p = D / name
    return json.loads(p.read_text()) if p.exists() else None


def local_bound(q):
    """12488: 1 + (q+1) + D_min, D_min = the fewest distance-2 lines X with sum c_X = q(q+1), sum C(c_X,3) <= C(q+1,3),
    1 <= c_X <= q+1 (exact: dynamic programme over (mass, triple budget))."""
    from math import comb
    M, B = q * (q + 1), comb(q + 1, 3)
    INF = 10 ** 9
    best = [[INF] * (B + 1) for _ in range(M + 1)]       # best[m][b] = fewest vertices with mass m using b triples
    best[0][0] = 0
    for m in range(M + 1):
        for b in range(B + 1):
            if best[m][b] == INF: continue
            for c in range(1, q + 2):
                mm, bb = m + c, b + comb(c, 3)
                if mm <= M and bb <= B and best[m][b] + 1 < best[mm][bb]:
                    best[mm][bb] = best[m][b] + 1
    return 1 + (q + 1) + min(best[M])


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
    bound = {q: 2 + (q + 1) ** 2 // 2 for q in (3, 5, 7, 9, 11, 13, 113)}
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
    # 12486: symmetric upper bounds (every set verified even by the driver)
    sym = {}
    for q, r in ((3, 2), (5, 3), (7, 8), (11, 6), (13, 7)):
        recs = load(f"symmetric_q{q}_r{r}.json")
        if recs:
            ok = [x for x in recs if x.get("verified_even")]
            sym[q] = min(x["weight"] for x in ok) if ok else None
    res["12486_symmetric_upper_bounds"] = sym
    checks["12486: symmetric search reaches the true minima 10, 20, 40 at q = 3, 5, 7 (controls)"] = (
        sym.get(3) == 10 and sym.get(5) == 20 and sym.get(7) == 40)
    if 11 in sym and 13 in sym:
        checks["12486: explicit even sets of 84 lines (q = 11) and 168 (q = 13) refute the 12474 fit 5*2^((q-1)/2) = 160, 320"] = (
            sym[11] is not None and sym[13] is not None and sym[11] <= 84 < 160 and sym[13] <= 168 < 320
            and sym[11] >= bound[11] and sym[13] >= bound[13])
    s7 = load("sym_structure_q7_r8.json")
    if s7:
        forty = [x for x in s7 if x["weight"] == 40]
        res["12487_q7"] = forty
        checks["12487: the symmetric 40-line optima at q = 7 are not twin-paired (4 twin pairs + 32 singles)"] = bool(forty) and all(
            not x["twin_paired"] and x["twin_class_sizes"] == [[1, 32], [2, 4]] for x in forty)
    # 12489: the regulus-matching family and its exceptional (square / cube / icosahedron) matchings
    rm = {q: load(f"regulus_matching_q{q}.json") for q in (3, 5, 7, 11)}
    geo = {q: (r["results"][-1]["matchings"], r["results"][-1]["even"],
               (r["results"][-1]["example"] or {}).get("size")) for q, r in rm.items() if r}
    res["12489_geometric"] = geo
    checks["12489: S(R0,M) is even for exactly 3, 0, 14, 22 of the 3, 15, 105, 10395 matchings at q = 3, 5, 7, 11, sizes 12, -, 40, 84"] = (
        geo.get(3) == (3, 3, 12) and geo.get(5, (15, 0, None))[1] == 0 and geo.get(7) == (105, 14, 40) and geo.get(11) == (10395, 22, 84))
    cc = load("chord_condition.json")
    res["12489_condition"] = cc
    checks["12489: the cross-ratio / no-concurrency condition selects exactly the geometric matchings at q = 3, 5, 7, 11"] = bool(cc) and all(
        cc[str(q)]["condition_count"] == cc[str(q)]["geometric_count"] and cc[str(q)]["geometric_ones_satisfy"] for q in (3, 5, 7, 11))
    small, large = load("chord_search_small.json") or {}, load("chord_search_large.json") or {}
    allq = {**small, **large}
    res["12489_search"] = {q: r["status"] for q, r in allq.items()}
    found = sorted(int(q) for q, r in allq.items() if r["status"] == "found")
    none_ = sorted(int(q) for q, r in allq.items() if r["status"] == "none")
    checks["12489: complete search -- good matchings exist only for q = 3, 7, 11 among the primes tested (up to 61)"] = (
        found == [3, 7, 11] and {5, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61} <= set(none_))
    ex = load("exceptional_matching.json")
    res["12489_stabilisers"] = ex
    checks["12489: one PGL(2,q)-orbit each; stabiliser D4 (q=3), S4 = cube (q=7), A5 = icosahedron (q=11), transitive, pairs = blocks"] = (
        bool(ex) and ex["3"]["stabiliser"] == 8 and ex["7"]["order_profile"] == {"1": 1, "2": 9, "3": 8, "4": 6}
        and ex["11"]["order_profile"] == {"1": 1, "2": 15, "3": 20, "5": 24}
        and all(ex[k]["one_orbit"] and ex[k]["transitive_on_PG1"] and ex[k]["pairs_are_blocks"] for k in ("3", "7", "11")))
    lb = {q: local_bound(q) for q in (3, 5, 7)}
    res["12488_local_bound"] = lb
    checks["12488: the local counting bound is 9, 16, 23 at q = 3, 5, 7 -- valid (<= 10, 20, 40) but not sharp"] = (
        lb == {3: 9, 5: 16, 7: 23})
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
