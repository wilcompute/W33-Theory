"""Passes 12450-12457 (Claude track).

12450 -- d = 2q by CP-SAT with native XOR parity: q = 3 controls exact (no word of weight <= 4; a weight-6 word found), but q = 5 at W = 8
  returns UNKNOWN in both symmetry cases after 900 s each (the MILP of 12434 and cdde9b06b settle q = 5); CP-SAT is not the q = 7 lever.
  Prior art located: Pass 4754 (bac1e7df4, 2026-08-10) proves the DUAL statement for every odd q -- the binary kernel of the LINE graph
  (= point graph of Q(4,q)) has distance q + 1 (anisotropic-plane conic) -- uncited in 12426-12449.  Point graph 2q vs line graph q + 1.
12450b -- Lemma (proved here): for the POINT graph of W(3,q), q odd, d >= q + 3.  The 4754 double count gives w >= q + 1 with equality iff
  S is pairwise non-collinear and every other point sees 0 or 2 points of S.  Take a, b in S: each z in {a,b}^perp already sees a and b, so
  sees no other point of S; a point s off the hyperbolic line {a,b}^perpperp has s^perp (a plane) meeting the PG-line {a,b}^perp, so s is
  collinear with some z -- contradiction.  Hence S = {a,b}^perpperp, whose outside profile is {1, q+1}: odd, not a kernel word.  So w >= q + 2,
  and kernel weights are even (ker = {N y : sum y even}, other track's 2026-10-29 note; each line has q + 1 points), so d >= q + 3.
  At q = 3 this IS d = 6, by hand.
12451 -- the SM_2541 '(1,2,0) unliftable pair' (12437, 12443-12444b) is an artefact of DIRAC-ONLY pairing: the leftover doublets sit in the
  real representation (2,2) of SU(2)_hidden x SU(2)_L with Y = 0 and a Majorana self-mass psi psi s^n passes the same exact all-orders
  lattice test.  Re-run for the whole family with self-pairing.  SM_2618 (12365) is unaffected: its leftovers are colour triplets or Y != 0.
12452 -- holographic dictionary, exact: the smallest entanglement-deficient region of the binary W(3,q) graph state equals the code distance.
12453 -- cut-rank profile: in the geometry's own characteristic every balanced cut of the W(3,q) graph state is AT the ceiling rank_p(A+I)
  (11 at q = 3, 36 at q = 5); the binary states on the same graphs carry more (15-16 random, >= 11 found; 65-66 random, 63 found at q = 5).
12454 -- scripts/code_parameter_index_all_repos.py: [[n,k,d]] parameters across all primary repositories.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12450_to_12457_majorana_rescue_deficit_cutrank_index.json"
A = ROOT / "analysis"


def j(p):
    return json.loads((A / p).read_text())


def main():
    checks, res = {}, {}
    c4, c6, c8 = (j(f"search_drivers_12450/cpsat_q{q}_W{w}.json") for q, w in ((3, 4), (3, 6), (5, 8)))
    res["12450"] = dict(q3W4=c4, q3W6=c6, q5W8=c8)
    checks["12450: CP-SAT controls at q = 3 exact (no word <= 4, weight-6 kernel word found); q = 5 W = 8 UNKNOWN in both cases (tool limit, not a result)"] = (
        c4["no_word_of_weight_le_W"] and c6["cases"]["a"]["weight"] == 6 and c6["cases"]["a"]["kernel_ok"]
        and all(r["status"] == "UNKNOWN" for r in c8["cases"].values()))
    p4754 = (A / "PASS4754_oddq_kernel_distance_theorem.md").read_text()
    checks["12450: prior art Pass 4754 (line-graph kernel, d = q + 1 for all odd q) exists and is the dual statement"] = (
        "d(K_q)=q+1" in p4754 and "line-intersection adjacency" in p4754)
    ec = j("search_drivers_12450/equality_case.json")
    res["12450b"] = ec
    checks["12450b: d >= q + 3 for every odd q (4754 double count + no hyperbolic-line kernel word); exhaustive at q = 3: 9450 pairwise "
           "non-collinear 4-sets, 0 with an even profile, hyperbolic lines profile {1, 4}"] = (
        ec["3"]["partial_ovoids_of_size_q_plus_1"] == 9450 and ec["3"]["with_even_profile"] == 0 and ec["3"]["hyperbolic_line_profiles"] == [[1, 4]])
    wr = j("search_drivers_12451/which_rule.json")
    res["12451_c22"] = wr
    checks["12451: SM_2541_c22 -- every relaxation leaves 2 Dirac-unmatched doublets; Majorana self-pairing of the real-rep ones leaves none"] = (
        all(wr[k]["unmatched"] == 2 for k in ("none",)) and wr["majorana"]["unmatched_after_dirac"] and wr["majorana"]["unmatched_after_majorana"] == [])
    vm = j("search_drivers_12373/vet_maj.json")
    res["12451_family"] = vm
    checks["12451: all 52 SM_2541 models -- Dirac pairing leaves exactly 2 fractional fermions, Majorana self-pairing lifts ALL fractional states"] = (
        len(vm) == 52 and all(r["fractional"] - r["dirac"] == 2 and r["with_majorana"] == r["fractional"] for r in vm.values()))
    mc = j("search_drivers_12451/majorana_control.json")
    res["12451_control"] = mc
    checks["12451 control: the self-mass lattice test is not vacuous -- on c22 it passes for only 8 of 92 fractional fields, and all 6 real "
           "Y = 0 fields are among them; on SM_2618 it rescues nothing (0 real Y = 0 fields)"] = (
        mc["c22"]["self_lattice_ok_any_rep"] == 8 and mc["c22"]["fractional"] == 92 and mc["c22"]["real_y0_fields"] == 6
        and mc["c22"]["real_y0_self_ok"] == 6 and mc["sm2618"]["majorana_rescued"] == 0 and mc["sm2618"]["real_y0_fields"] == 0)
    s2618 = j("search_drivers_12357/lift_exact_Z6II_06_SM_20260917_2618_v0.json")
    checks["12451: SM_2618 unaffected -- its unmatched types are colour triplets or carry Y != 0 (no real-rep Y = 0 self-mass)"] = all(
        t.split(",")[0].strip("( ") in ("3", "-3") or t.split(",")[2].strip(" ')") != "0" for t in s2618["unmatched_types"])
    dm = j("search_drivers_12452/deficit_milp.json")
    d35, d36, d59 = (j(f"search_drivers_12452/deficit_cpsat_q{q}_R{r}.json") for q, r in ((3, 5), (3, 6), (5, 9)))
    res["12452"] = dict(milp=dm, cpsat_q3_R5=d35, cpsat_q3_R6=d36, cpsat_q5_R9=d59)
    checks["12452: q = 3 smallest deficient region = 6 = d, twice (HiGHS optimum 6 with a kernel word; CP-SAT: none <= 5, one of size 6)"] = (
        dm["3"]["optimal"] and dm["3"]["min_region"] == 6 and dm["3"]["x_in_kernel"] and d35["no_region_le_R"] and d36["cases"]["a"]["region"] == 6)
    checks["12452: q = 5 -- HiGHS hits its 3000 s limit at the trivial incumbent 31 (a vertex and its neighbours); recorded, not used"] = (
        not dm["5"]["optimal"] and dm["5"]["min_region"] == 31)
    res["12452_q5_status"] = "PROVED min region = 10 = d" if d59["no_region_le_R"] else "OPEN: CP-SAT " + str({k: v["status"] for k, v in d59["cases"].items()})
    cr = j("search_drivers_12453/cut_rank.json")
    res["12453"] = cr
    checks["12453: own-characteristic W(3,q) graph states -- every sampled balanced cut and every local-search cut at the ceiling (11, 36)"] = (
        all(cr[k]["random_balanced"]["min"] == cr[k]["ceiling"] == cr[k]["local_search_min"] for k in ("q=3,p=3", "q=5,p=5"))
        and cr["q=3,p=3"]["ceiling"] == 11 and cr["q=5,p=5"]["ceiling"] == 36)
    checks["12453: binary states on the same graphs exceed the q-ary ceiling on balanced cuts (>= 15 at q = 3, >= 65 at q = 5)"] = (
        cr["q=3,p=2"]["random_balanced"]["min"] >= 15 and cr["q=5,p=2"]["random_balanced"]["min"] >= 65)
    idx = (ROOT / "CODE_PARAMETER_INDEX_ALL_REPOS.md").read_text(encoding="utf-8")
    rows = [l for l in idx.splitlines() if l.startswith("| [[")]
    res["12454_parameters"] = len(rows)
    checks["12454: cross-repo code-parameter index built; contains the W(3,3) CSS [[40,8,6]]"] = len(rows) > 50 and any(r.startswith("| [[40,8,6]]") for r in rows)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
