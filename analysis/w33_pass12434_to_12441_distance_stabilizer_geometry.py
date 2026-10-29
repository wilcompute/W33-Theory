"""Passes 12434-12441: the distance of the binary adjacency code of W(3,q), stabilizer-state geometry, and the colour obstruction
(Claude track).

CROSS-TRACK OWNERSHIP: q = 5 d = 10 was certified first by cdde9b06b (14:25) -- the MILP here is an independent confirmation;
q = 7 10 <= d <= 14 is 055804fc2; the dual polar C3(3) construction/shells is 30997a710.  See the md table.

12434 -- binary adjacency code (A^2 = 0 mod 2) of W(3,q), q odd.  For x = 1_S in ker_2(A) and s_L = |S cap L|:
  (Lemma) each point y: sum over lines L through y of s_L = (q+1)[y in S] + #(neighbours of y in S) = 0 mod 2 (q + 1 even);
  (Even case: every s_L even) |S| >= 2q + 2: take p in S, a line L through p with a second point p' in S; each of the q other lines through
    p and through p' carries another point of S; no triangles in a GQ makes all 2q + 2 points distinct.  Matches the minimum stabilizer
    weight 2q + 2 (12426: 8, 12, 16).
  (Odd case) exact MILP minimum of ker_2(A) (x_0 = 1 by transitivity): q = 3 -> 6 (control), q = 5 -> 10 (optimal), q = 7 -> see
    certificate.  With the weight-2q logicals of 12421 this PROVES d = 2q at q = 3, 5 (computer-assisted); general q open.
  Useful identity: for any line L, |S| = s_L + sum_{x in L} m_x with m_x = #(S-points off L collinear with x) (each point off L sees
  exactly one point of L) and m_x = s_L - [x in S] mod 2.
12435-12436 -- stabilizer-state geometry (qutrits): Lagrangians of F_3^{2n} = stabilizer frames (40 at n = 2 = the lines of W(3,3); 1120 at
  n = 3); dual polar distance d = n - dim(L cap L').  Every nonzero overlap of stabilizer states equals 3^-d (0 violations over all 360^2
  pairs at n = 2 and 27 x 30240 at n = 3); sphere sizes 1, 12, 27 and 1, 39, 351, 729 = q^{r(r+1)/2} [n r]_q; at the maximal distance n
  every overlap is 3^-n (antipodal frames are mutually unbiased).  [E] stabilizer overlaps and MUBs are known; [I] the reading: distance
  = -log_q fidelity, a metric made of information whose antipodes are the position/momentum (state/update) pairs; the light cone grows
  with n (diameter n), unlike the fixed W(3,q) graph (diameter 2, 12428).
12437 -- location of the colour charge-lattice obstruction (see certificate).
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12434_to_12441_distance_stabilizer_geometry.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    m35 = json.loads((A / "search_drivers_12434" / "milp_dist_3_5.json").read_text())
    res["12434"] = dict(q3_q5=m35)
    checks["12434: exact MILP minimum of ker_2(A): q = 3 -> 6 (control), q = 5 -> 10 = 2q, both optimal"] = (
        m35["3"]["optimal"] and m35["3"]["min_weight"] == 6 and m35["5"]["optimal"] and m35["5"]["min_weight"] == 10)
    p7 = A / "search_drivers_12434" / "milp_dist_7.json"
    if p7.exists():
        m7 = json.loads(p7.read_text()); res["12434"]["q7"] = m7
        checks["12434: q = 7 MILP recorded honestly -- time limit, not solved (d = 14 at q = 7 remains search evidence, 12426)"] = (
            m7["7"]["optimal"] is False)
    sg = json.loads((A / "search_drivers_12435" / "stabgeom.json").read_text())
    res["12435"] = sg
    checks["12435: Lagrangians 40 / 1120; spheres = q^{r(r+1)/2}[n r]_q; every nonzero overlap = 3^-d; antipodes never orthogonal"] = (
        sg["2"]["lagrangians"] == 40 and sg["3"]["lagrangians"] == 1120 and sg["2"]["spheres"] == sg["2"]["spheres_formula"]
        and sg["3"]["spheres"] == sg["3"]["spheres_formula"] and sg["2"]["overlaps_violating_3^-d"] == 0 and sg["3"]["overlaps_violating_3^-d"] == 0
        and "2|zero" not in sg["2"]["overlap_table"] and "3|zero" not in sg["3"]["overlap_table"])
    pf = json.loads((A / "search_drivers_12438" / "polar_family.json").read_text())
    res["12438"] = pf
    from math import comb
    checks["12438: across W(2n-1,q) for (n,q) = (2,2),(3,2),(4,2),(2,3),(3,3),(2,5),(2,7): (A+I)^2 = J mod p; rank_p(A+I) = Smith "
           "1 + C(2n+p-2, 2n-1) (5, 7, 9, 11, 22, 36, 85); the ceiling is attained; random regular graphs reach ~v/2"] = all(
        r["AplusI_sq_J_modp"] and r["rankp_AplusI"] == r["smith"] == 1 + comb(2 * r["n"] + r["q"] - 2, 2 * r["n"] - 1)
        and r["half_cut_max_found"] == r["rankp_AplusI"] and r["control_half_cut"] >= r["v"] // 2 - 1 and (r["q"] == 2 or r["A2_zero_mod2"])
        for r in pf.values()) and len(pf) == 7
    checks["12438: qubit ceilings are 2n + 1 (doily 5, three qubits 7, four qubits 9)"] = (
        pf["2,2"]["rankp_AplusI"] == 5 and pf["3,2"]["rankp_AplusI"] == 7 and pf["4,2"]["rankp_AplusI"] == 9)
    import math
    checks["12439: qubit Schmidt-rank width <= 2n + 1 = log2(v + 1) + 1 (logarithmic -> efficiently simulable MBQC, Van den Nest et al. 2007)"] = all(
        pf[k]["rankp_AplusI"] == math.log2(pf[k]["v"] + 1) + 1 for k in ("2,2", "3,2", "4,2"))
    sq = json.loads((A / "search_drivers_12435" / "stabgeom_q2.json").read_text())
    res["12435_qubits"] = sq
    checks["12435: qubit stabilizer geometry -- 15 / 135 frames, spheres = formula, nonzero overlaps 2^-d, antipodes unbiased"] = (
        sq["2"]["lagrangians"] == 15 and sq["3"]["lagrangians"] == 135 and sq["2"]["spheres"] == sq["2"]["spheres_formula"]
        and sq["3"]["spheres"] == sq["3"]["spheres_formula"] and sq["2"]["overlaps_violating_3^-d"] == 0 and sq["3"]["overlaps_violating_3^-d"] == 0
        and "3|zero" not in sq["3"]["overlap_table"])
    cb = A / "search_drivers_12437" / "colour_block.json"
    if cb.exists():
        c = json.loads(cb.read_text()); res["12437"] = c["table"]
        checks["12437: CORRECTION of 12432 -- with loose values and no anomaly condition the full colour set is FEASIBLE for 17 of 23; "
               "only 6 are colour-blocked (the 12432 'all colour-blocked' was a base-mode statement)"] = (
            len(c["per_model"]) == 23 and sum(v["Q+U+D"] for v in c["per_model"].values()) == 17
            and all(v["Q"] and v["Q+U"] and v["Q+D"] for v in c["per_model"].values()))
        lp = A / "search_drivers_12373" / "vet_loose2.json"
        if lp.exists():
            vl = json.loads(lp.read_text()); res["12437_relaxed_full"] = dict(candidates=len(vl), with_solution=sum(1 for x in vl.values() if x))
            checks["12437: relaxed FULL search: exactly one candidate (SM_2541_c22) admits a three-generation hypercharge"] = (
                len(vl) == 23 and [k for k, x in vl.items() if x] == ["Z6II_06_SM_20260917_2541_c22"])
            sv = json.loads((A / "search_drivers_12373" / "sm2541_vet.json").read_text()); res["12437_SM2541"] = sv
            checks["12437: SM_2541_c22 -- k_Y = 17/3, Tr Y = 0, Y orthogonal to roots and to the anomalous U(1), large-R safe; 90/92 fractional "
                   "fermions liftable, one (1,2,0) pair forbidden at all orders"] = (
                sv["kY"] == "17/3" and sv["t_dot_T_anom"] == "0" and sv["liftable_all_orders"] == 90 and sv["fractional_fermions"] == 92)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
