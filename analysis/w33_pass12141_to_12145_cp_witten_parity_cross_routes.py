"""Passes 12141-12145: CP and the B-field instability of S002, the Witten-parity protection of T115's doublet, the twisted
obstruction to a fraction-free k_Y = 5/3, T115's moduli, and fraction-free A8 models with a single heavy top (Claude track).

12141 -- the potential of S002 is exactly even under Re T_WL -> -Re T_WL (Lambda(-0.1 + 0.9i) = Lambda(+0.1 + 0.9i) to all printed
  digits; tachyon levels at +-0.1 + 0.55i identical): T -> -Tbar is CP on the modulus, so the imaginary axis is the CP-invariant
  locus. Its lowest Witten-sector level is a 56-state multiplet with Delta = +0.00039 at 0.55i and +0.033 at 0.9i; 0.02 off the
  axis it is already Delta = -0.0099 (slope ~ -0.5 in |Re T|). So S002's potential minimum sits on the CP-invariant line with a
  near-marginal multiplet, and any CP-odd B-field drives that multiplet tachyonic: CP cannot be broken spontaneously along
  Re T_WL without a tachyon.
12142 -- T115's protected doublet is protected by the WITTEN Z2: every SM-singlet scalar of T115 lies in the theta or theta^2
  sector (69 + 69 components, mm = 0), while the deficient block (structural rank 5 of 6) is the beta-theta sector (mm = 1): 4
  Rbar doublets against 3 R. A mass term linking beta-theta to theta^2 fermions needs sum mm odd from mm = 0 vevs -- forbidden at
  every order. One vector-like lepton doublet pair is exactly massless as long as only SM-singlet vevs are switched on.
12143 -- why no fraction-free k_Y = 5/3: every admissible root candidate (1060 in the 104 A8 models, 44 in the five e6+a2 models;
  97 of the A8 ones even give the SM spectrum) has NO fractional untwisted state (as the 12131 lattice argument requires) and
  ALWAYS a fractional state in the beta-theta (Witten x theta) sector -- 1104/1104. The obstruction is twisted, and universal.
12144 -- T115's moduli: Lambda/M^4 = 862.2 (1.75i, 2i, 2i) and 863.8 (2i, 2i, 1.75i), between the diagonal values 987.6 (2i) and
  663.8 (1.75i) -- the three tori act almost symmetrically; with B-field Re T = 0.2 at 1.75i Lambda = 663.907 > 663.839: for T115
  the CP-invariant axis is a transverse MINIMUM (unlike S002), and all these points are tachyon-free. T115 rolls only along the
  radius, into its tachyon onset between 1.75i and 1.5i.
12145 -- crossing the routes: under the fraction-free k_Y = 17/3 hypercharges of the A8 models (218 checked, 81 models, all with
  net 3 quark doublets) the quark sector is reassigned; 16 models acquire a SINGLE heavy up-type quark (light up Yukawa rank 1),
  13 with a single heavy down-type quark too, every one through mixing with a vector-like Y = 1/6 doublet (27/27) -- the S002
  mechanism inside an A8 model: fraction-free, three generations, one heavy top. (Ranks at random couplings are upper bounds;
  extra light d^c can remain at trilinear order.)
"""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12141_to_12145_cp_witten_parity_cross_routes.json"
D = ROOT / "analysis" / "search_drivers_12141"
D36 = ROOT / "analysis" / "search_drivers_12136"


def lam(p):
    return json.loads(p.read_text())["Lambda_over_M4"]


def main():
    checks, res = {}, {}
    lp = lam(D36 / "oneloop_N004_F1_03_S002_0.1+0.9j_rho_K2.json")
    lm = lam(D / "oneloop_N004_F1_03_S002_m0.1+0.9j_rho_K2.json")
    tf = json.loads((D / "tachF.json").read_text())
    tc = json.loads((D36 / "tachC.json").read_text())
    ll = json.loads((D / "lowlev.json").read_text())
    res["12141"] = dict(Lambda_pm=[lp, lm], lowest_levels=ll)
    checks["12141: S002 potential CP-even: Lambda(-0.1+0.9i) = Lambda(+0.1+0.9i) (1e-12), tachyon levels at +-0.1+0.55i equal"] = (
        abs(lp - lm) < 1e-9 and abs(tf["S002 -0.1+0.55i"]["Delta"] - tc["0.1+0.55i"]["Delta"]) < 1e-9 and tf["S002 -0.1+0.9i"]["n"] == 0)
    checks["12141: lowest axis level = 56-state multiplet, Delta = +0.00039 (0.55i), +0.033 (0.9i); Delta = -0.0099 at 0.02 off axis"] = (
        ll["0.55i"]["n_below_0p05"] == 56 and 0 < ll["0.55i"]["lowest"][0] < 0.001 and 0.03 < ll["0.9i"]["lowest"][0] < 0.04
        and -0.011 < ll["0.02+0.55i"]["lowest"][0] < -0.009)
    b = json.loads((D / "block.json").read_text())
    ss = json.loads((D / "t115_singlet_sectors.json").read_text())
    res["12142"] = dict(singlet_sectors=ss, block=b)
    checks["12142: T115 SM-singlet scalars only in theta/theta^2 (mm = 0); deficient block = beta-theta sector, 4 Rbar vs 3 R; other block theta^2"] = (
        set(ss) == {"(1, 0)", "(2, 0)"} and len(b["deficient_columns"]) == 4 and len(b["their_rows"]) == 3
        and all(tuple(x["sector"]) == (1, 1) for x in b["deficient_columns"] + b["their_rows"])
        and all(tuple(x["sector"]) == (2, 0) for x in b["other_rows"] + b["other_cols"]))
    k = json.loads((D / "kyroot.json").read_text())
    a8 = [v for kk, v in k.items() if kk.startswith("A8")]
    e6 = [v for kk, v in k.items() if kk.startswith("N0")]
    res["12143"] = dict(A8_candidates=sum(v["n"] for v in a8), A8_SM=sum(v["sm"] for v in a8), e6a2_candidates=sum(v["n"] for v in e6))
    checks["12143: all 1104 k_Y = 5/3 root candidates: no untwisted fractional state, always a fractional beta-theta state; none fraction-free"] = (
        sum(v["n"] for v in a8) == 1060 and sum(v["n"] for v in e6) == 44 and sum(v["sm"] for v in a8) == 97
        and all(v["untwisted_fractional"] == 0 and v["fraction_free"] == 0 for v in a8 + e6)
        and all(v["sectors"].get("T1b", 0) == v["n"] for v in a8 + e6))
    L = {"175_2_2": lam(D / "oneloop3_T115_1.75j_2j_2j.json"), "2_2_175": lam(D / "oneloop3_T115_2j_2j_1.75j.json"),
         "B0.2_175": lam(D / "oneloop3_T115_B0.2_1.75j.json"), "diag2": lam(D36 / "oneloop3_T115_2j_2j_2j.json"),
         "diag175": lam(D36 / "oneloop3_T115_1.75j_1.75j_1.75j.json")}
    res["12144"] = dict(Lambda=L, tachyons={kk: v for kk, v in tf.items() if kk.startswith("T115")})
    checks["12144: T115 single-torus shrink 862.2 / 863.8 between diagonals 987.6 and 663.8; B-field raises Lambda (axis = transverse minimum); all tachyon-free"] = (
        L["diag175"] < L["175_2_2"] < L["diag2"] and L["diag175"] < L["2_2_175"] < L["diag2"] and abs(L["175_2_2"] - L["2_2_175"]) < 5
        and L["B0.2_175"] > L["diag175"] and all(v["n"] == 0 for kk, v in tf.items() if kk.startswith("T115")))
    c = json.loads((D / "a8cross.json").read_text())
    allr = [(lab, x) for lab, r in c.items() for x in r]
    up1 = [(lab, x) for lab, x in allr if x["up"]["rank"] == 1]
    both = [(lab, x) for lab, x in up1 if x["down"]["rank"] == 1]
    res["12145"] = dict(hypercharges=len(allr), models=len(c), rank_pairs={str(kk): v for kk, v in Counter((x["up"]["rank"], x["down"]["rank"]) for _, x in allr).items()},
                        single_heavy_up_models=sorted({lab for lab, _ in up1}), single_heavy_up_and_down_models=sorted({lab for lab, _ in both}))
    checks["12145: 218 fraction-free k_Y = 17/3 hypercharges (81 A8 models, all net 3 Q); 16 models with a single heavy up quark, 13 with up and down; all via vector-like Q mixing"] = (
        len(allr) == 218 and len(c) == 81 and all(x["netQ"] == 3 for _, x in allr) and len({lab for lab, _ in up1}) == 16
        and len({lab for lab, _ in both}) == 13 and all(x["up"]["nQb"] > 0 for _, x in up1))
    checks = {kk: bool(v) for kk, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
