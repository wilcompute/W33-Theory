"""Passes 12363-12368: radius-by-radius tachyon analysis and the closure of the three-doublet non-SUSY Z6-II lineages (Claude track).

Prior art (cited): non-SUSY SO(16) x SO(16) orbifold Standard-Model-like models exist in the literature (Blaszczyk, Groot Nibbelink,
Loukas, Ramos-Sanchez, arXiv:1407.6362); a vanishing one-loop cosmological constant is impossible on non-SUSY toroidal orbifolds
(Groot Nibbelink et al., arXiv:1710.09237); in-corpus: 12322 (torsion window), 12351-12362 (SM_2913 lineage, sub-orbifold geometries).

12363 -- small radius.  A winding-w string of the theta^2 sub-orbifold is the element (g, l + w e5); feeding the engine constructing
  elements shifted by w e5 gives the states that are light as R5 -> 0.  Controls: with W5 = 0 winding changes nothing (twisted sectors
  identical; 24 untwisted neutral states relabelled by the engine); with W5 on, w = 2 equals w = 0 (W5^2 = 22).  Odd winding (w = -1,
  +-3, 5; w = +1 trips an engine assertion): 42 level-matched tachyons, m_R^2 = -1/6, identical for every odd w.  So SM_2913_v6 is
  tachyonic for R5 < sqrt(2/3) sqrt(alpha') (alpha' m^2/4 = -1/6 + R5^2/4) AND for R5 > sqrt(3/8) (12359): NO tachyon-free R5.
12364 -- hypercharge searches (exact MILP; Y orthogonal to every non-abelian root and to the anomalous U(1); per-field Y from a finite
  set; net chiral content = three SM generations, all else vector-like or hidden-chiral with Y = 0).  Control SM_2913_v6: solutions,
  including its parent's k_Y = 5/3.  SM_574 (v0, v5, v6; small-R safe, a hidden SU(5) family 10 + 5bar): NO solution, also with the
  anomaly condition dropped, hidden values widened and every non-(3,2) value loosened to (1/6)Z in [-1, 1]; mechanism: the coloured
  conditions plus Y-neutral hidden SU(5) states are already infeasible.  SM_1105_v12 (large-R safe): net two SU(2)_L doublets that are
  triplets of a hidden SU(3)' -- chiral exotics for every hypercharge.
12365 -- SM_2618 (small-R safe, three generations with k_Y = 5/3): 12 of its 52 fractional-charge fermions ((3,1,-+1/6), (1,1,+-1/2))
  cannot be paired at ANY order -- exact lattice test with no degree bound, no positivity and every translation sector allowed (the most
  permissive rule; further rules only forbid more).  Control SM_2913_v6: 52/52 at all orders.
12366 -- all-radius census of the 99 tachyon-free parents (twisted-sector channels; Wilson lines on/off): e3e4 clean at large and small
  radius in 99/99; e5e6: (large-R tachyonic, small-R tachyonic) = (no, no) 18, (no, yes) 29, (yes, no) 34, (yes, yes) 18.  The 18
  all-radius-clean parents (SM_1474 x 6, SM_2678 x 12) carry no three net (3,2) doublets (SM_1474: 0; SM_2678: no SU(3)).
12367 -- three-doublet parents: 0 of 17 clean at all radii vs 18 of 82 others (hypergeometric chance C(81,17)/C(99,17) = 0.023: suggestive only).
  Every parent has both W3 and W5 (built in by the route), so no Wilson-line contrast is available in this sample.
12368 -- closure on this sample: every three-doublet lineage of the 99 tachyon-free non-SUSY Z6-II parents fails --
  SM_2913 (no tachyon-free radius), SM_2503 (no tachyon-free radius), SM_2618 (massless fractional charges at all orders),
  SM_574 (no three-generation hypercharge), SM_1105 (Y-independent chiral exotics).  Not covered: untwisted-sector winding channels
  (the engine cannot take a translated untwisted element; 12352's necessary condition stands), non-SUSY vertex rule (moot after
  closure), models outside the 99.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12363_to_12368_all_radius_closure_z6ii.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    w = json.loads((A / "search_drivers_12363" / "summary.json").read_text())
    res["12363"] = w
    checks["12363: controls (W5=0 winding-blind; w=2 = w=0); every odd winding gives the same 42 tachyons; 12 at large R5"] = (
        w["control_noW5_w1_equals_w0_up_to_relabel"] and w["control_W5_w2_equals_w0_up_to_relabel"] and w["odd_winding_identical"]
        and all(w["T"][k] == 42 for k in ("sub2_wm1A", "sub2_wm3A", "sub2_w3A", "sub2_w5A")) and w["T"]["sub2_w0"] == 0
        and w["T"]["sub2_noW5_w0"] == 12)
    y = json.loads((A / "search_drivers_12364" / "summary.json").read_text())
    res["12364"] = y
    s574 = [k for k in y if "574" in k]
    checks["12364: control finds k_Y=5/3 for SM_2913; SM_574 infeasible in every variant; SM_1105 has net 2 hidden-SU(3) doublets"] = (
        "5/3" in y["Z6II_23_SM_20260917_2913_v6"]["kY"] and y["Z6II_23_SM_20260917_2913_v6_noanom_loose"]["solutions"] > 0
        and len(s574) >= 7 and all(y[k]["solutions"] == 0 for k in s574) and abs(y["SM_1105_v12_net_(1,2,3bar,1)"]) == 2)
    D = A / "search_drivers_12357"
    l26 = json.loads((D / "lift_exact_Z6II_06_SM_20260917_2618_v0.json").read_text())
    l29 = json.loads((D / "lift_exact_Z6II_23_SM_20260917_2913_v6.json").read_text())
    res["12365"] = {k: v for k, v in l26.items() if k != "pairs"}
    res["12365_control"] = {k: v for k, v in l29.items() if k != "pairs"}
    checks["12365: SM_2618 lifts 40/52 at all orders (12 forbidden); control SM_2913 52/52"] = (
        l26["liftable_all_orders_upper"] == 40 and l26["fractional"] == 52 and l29["liftable_all_orders_upper"] == 52)
    cb = json.loads((A / "search_drivers_12363" / "combine.json").read_text())
    res["12366"] = dict(table=cb["table"], all_radius_clean=cb["all_radius_clean"])
    rows = cb["rows"]
    checks["12366: e3e4 clean 99/99 at both ends; e5e6 split 18/29/34/18; 18 all-radius-clean parents (SM_1474, SM_2678)"] = (
        len(rows) == 99 and all(r["large_e3e4"] == 0 and r["small_e3a"] == 0 and r["small_e3b"] == 0 for r in rows.values())
        and cb["table"] == {"(False, False)": 18, "(True, True)": 18, "(True, False)": 34, "(False, True)": 29}
        and all(("1474" in m) or ("2678" in m) for m in cb["all_radius_clean"]))
    st = json.loads((A / "search_drivers_12363" / "w5stats.json").read_text())
    three = {m: r for m, r in st["rows"].items() if r["three_doublets"]}
    res["12367"] = st["table"]
    checks["12367: 0 of 17 three-doublet parents clean at all radii; every parent has W3 and W5"] = (
        len(three) == 17 and not any(r["large_e5e6"] == 0 and r["small_e5"] == 0 for r in three.values())
        and all(r["W5"] and r["W3"] for r in st["rows"].values()))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
