"""Passes 12426-12433: the W(3,q) binary code family's distance, the code-entanglement dictionary, light cones, the commutation form as a
magnetic flux, and a Witten-shift search over 65 new SUSY parents (Claude track).

12426 -- randomised information-set search (Lee-Brickell) on the CSS family A^2 = 0 mod 2: q = 3 control reproduces the exhaustive d = 6
  (cross-track 923c4eb20) and minimum stabiliser 8; q = 5: lightest logical found 10, stabiliser 12; q = 7: 14 and 16.  Evidence (not
  proof) for d = 2q, minimum stabiliser weight 2q + 2.
12427 -- code-entanglement dictionary (binary W(3,3) graph state): a region R is deficient (S(R) < |R|) iff some nonzero x in R has
  A x in R.  Exhaustively over x of weight <= 6: weights 1..5 force regions of >= 13 points, weight 6 gives 6-point regions (the hexads,
  cut-rank 5); x of weight >= 7 gives regions >= 7.  So every region of <= 5 points is maximally entangled and the smallest deficient
  regions have exactly d = 6 points: the code distance IS the entanglement-deficit threshold.  (Ternary: x of weight <= 4 force >= 13;
  weights 5..12 not exhausted.)
12428 -- the collinearity graph of W(3,q) has diameter 2 (q = 3, 5, 7): any update reaches everything in two steps; no extended light
  cone on the fixed graph (consistent with in-corpus toe54).
12429 -- the qutrit clock/shift (ZX = w XZ) are magnetic translations with flux 1/3; Hofstadter bands at flux 1/3 have Chern numbers
  -(1, -2, 1) in this grid orientation (sum 0), satisfying the TKNN Diophantine equation (Hall conductance t_r e^2/h, t_1 = 1, t_2 = -1);
  two qutrits = flux 1/3 in two planes: second Chern numbers C_a C_b (lowest band pair: 1).  [E] for the 2D numbers; [I] the reading:
  the W(3,3) commutation form supplies the topological unit e^2/h; the Hodge (Z0) side is still missing from the finite geometry.
12430-12432 -- see the certificate (Witten-shift search over new parents, filters, hypercharge).
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12426_to_12433_distance_dictionary_flux_newparents.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    md = json.loads((A / "search_drivers_12426" / "mindist.json").read_text())
    res["12426"] = md
    checks["12426: control q = 3 gives d = 6, stabiliser 8; q = 5, 7 lightest logicals found 2q (10, 14), stabilisers 2q + 2"] = (
        md["3"]["min_logical_found"] == 6 and md["3"]["min_stabiliser_found"] == 8 and md["5"]["min_logical_found"] == 10
        and md["5"]["min_stabiliser_found"] == 12 and md["7"]["min_logical_found"] == 14 and md["7"]["min_stabiliser_found"] == 16
        and md["5"]["k"] == 24 and md["7"]["k"] == 48)
    dc = json.loads((A / "search_drivers_12427" / "dictionary.json").read_text())
    res["12427"] = dc
    checks["12427: binary -- all regions of <= 5 points maximally entangled; smallest deficient regions have 6 points (hexads, cut-rank 5)"] = (
        all(dc["F2"][str(w)]["min_region"] >= 13 for w in range(1, 6)) and dc["F2"]["6"]["min_region"] == 6
        and dc["F2"]["6"]["example_region_cut_rank"] == 5)
    fx = json.loads((A / "search_drivers_12429" / "flux.json").read_text())
    res["12428_12429"] = fx
    checks["12428: diameter 2 for q = 3, 5, 7"] = fx["12428_diameter"] == {"3": 2, "5": 2, "7": 2}
    checks["12429: flux-1/3 Hofstadter Chern numbers +-(1, -2, 1), sum 0, TKNN Diophantine satisfied"] = (
        sorted(fx["12429"]["band_chern"]) == [-1, -1, 2] and fx["12429"]["sum"] == 0 and all(t["diophantine_ok"] for t in fx["12429"]["tknn"]))
    np_path = A / "search_drivers_12373" / "newparents_summary.json"
    if np_path.exists():
        npr = json.loads(np_path.read_text())
        res["12430_12432"] = npr
        checks["12430-12432: 65 new parents, 15600 shifts -> 66 three-doublet models (22 parents), 40 large-radius safe, 23 exotic-free, "
               "no hypercharge in any pairing; all 23 colour-blocked (no twin sector)"] = (
            npr["parents"] == 65 and npr["sampled"] == 15600 and npr["three_doublet"] == 66 and npr["three_doublet_parents"] == 22
            and npr["large_safe"] == 40 and npr["exotic_free"] == 23 and npr["pairing_hypercharge_found"] == 0
            and npr["colour_only_feasible"] == 0 and npr["twin_present"] == 0)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
