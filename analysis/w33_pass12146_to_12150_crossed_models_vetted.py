"""Passes 12146-12150: vetting the 16 fraction-free single-heavy-top A8 models, their flavour structure and Witten-parity
protection, why S002's minimum sits at the tachyon edge, and the beta-theta obstruction as a lattice congruence (Claude track).

12146 -- the 16 crossed models of 12145: one-loop Lambda/M^4 (11106 engine, T_WL = 2i, T* = rho) in [643.7, 703.0], all positive;
  12/16 tachyon-free down to Im T_WL = 1.5 (11107 enumerator), four tachyonic at 1.5 (1295, 17724: Delta = -0.0028; 5110, 6052:
  -0.067). Exotic masses to quartic order (12133 method; quartic terms with gauge + space group, so a lift is an upper bound):
  A8SM_10006 (11 -> 0) and A8SM_16222 (15 -> 0) keep NO light vector-like pair; the others keep 3-15.
12147 -- flavour: in the 12 models with a single heavy top AND bottom the two heavy directions coincide in the light-Q space,
  |V_tb| = 1; adding quartic Q u H <s> terms (upper bound) raises the up rank from 1 to 3 in all 16 -- charm and up arise one
  order higher, m_c/m_t ~ <s>/M.
12148 -- Witten parity: in all 16 every SM-singlet scalar has mm = 0, so masses cannot cross Witten-parity sectors; 10 models then
  carry exactly protected vector-like pairs (some colour triplets), six carry none (10006, 16222, 17724, 4168, 438, 6052).
  BEST CANDIDATES: A8SM_10006 and A8SM_16222 -- fraction-free (k_Y = 17/3), three generations, single heavy top and bottom with
  |V_tb| = 1, no Witten-protected exotic, every exotic lifted by quartic order, Lambda > 0, tachyon-free to Im T_WL = 1.5.
12149 -- S002's potential minimum (Lambda/M^4 = 115.14 at 0.58i; 115.39 at 0.55i, 115.77 at 0.6i, 117.27 at 0.52i) sits where the
  lowest Witten-sector multiplet (56 states) TOUCHES masslessness: Delta_min = 0.0062 (0.7i), 0.00085 (0.62i), 3.5e-6 (0.58i),
  0.00016 (0.56i), 0.00039 (0.55i), 0.00075 (0.54i), 0.0035 (0.5i) -- a double zero at the minimum, the familiar stationarity of
  string potentials where extra states become massless. At Im T_WL = 1/sqrt3 exactly the 56 states are massless (Delta = -4e-16).
12150 -- the beta-theta obstruction as a lattice congruence: a colour-singlet beta-theta state at fixed point f has Q = v.pi + v.U_f
  (U_f = V0 + V1 + sum c_i W_i), so it is integral iff v.U_f in Z; this congruence reproduces the direct test on all 1080 k_Y = 5/3
  candidates (A8 + S002 + T115), and NO admissible root has v.(V0 + V1) and every v.W_i integral (0/1080): in 982 the obstruction
  is v.(V0 + V1) (residues 1/6, 1/3, 1/2, 2/3, 5/6), in the other 98 a Wilson-line residue 1/3 or 2/3.
"""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12146_to_12150_crossed_models_vetted.json"
D = ROOT / "analysis" / "search_drivers_12146"
D36 = ROOT / "analysis" / "search_drivers_12136"


def lam(p):
    return json.loads(p.read_text())["Lambda_over_M4"]


def main():
    checks, res = {}, {}
    cv = json.loads((D / "crossvac.json").read_text())
    ce = json.loads((D / "crossexo.json").read_text())
    cf = json.loads((D / "crossflavor.json").read_text())
    L = [v["Lambda_over_M4"] for v in cv.values()]
    tf = [k for k, v in cv.items() if all(t["n"] == 0 for t in v["tachyons"].values())]
    res["12146"] = dict(Lambda_range=[min(L), max(L)], tachyon_free_to_1p5=sorted(tf),
                        light_exotics={k: [v["light_trilinear"], v["light_up_to_quartic"]] for k, v in ce.items()})
    checks["12146: 16 models, Lambda/M^4 in [643.7, 703.0] > 0; 12 tachyon-free to Im T_WL = 1.5"] = (
        len(cv) == 16 and 643 < min(L) and max(L) < 704 and len(tf) == 12)
    zero = sorted(k for k, v in ce.items() if v["light_up_to_quartic"] == 0)
    checks["12146: exactly two models lift every exotic by quartic order: A8SM_10006 (11->0), A8SM_16222 (15->0)"] = (
        zero == ["A8SM_20260928_10006_TF", "A8SM_20260928_16222_TF"] and len(ce) == 16)
    both = [k for k, v in cf.items() if v["up"]["rank3"] == 1 and v["down"]["rank3"] == 1]
    res["12147"] = dict(Vtb={k: v["Vtb"] for k, v in cf.items()}, up_rank_with_quartic={k: v["up"]["rank_with_quartic"] for k, v in cf.items()})
    checks["12147: |V_tb| = 1 in all 12 single-heavy-top-and-bottom models; quartic terms raise the up rank 1 -> 3 in all 16"] = (
        len(both) == 12 and all(abs(cf[k]["Vtb"] - 1) < 1e-9 for k in both) and all(v["up"]["rank_with_quartic"] == 3 for v in cf.values()))
    none = sorted(k for k, v in cf.items() if not v["witten_protected_pairs"])
    res["12148"] = dict(singlet_mm={k: v["singlet_mm"] for k, v in cf.items()}, protected={k: v["witten_protected_pairs"] for k, v in cf.items()})
    checks["12148: all singlet scalars mm = 0 in 16/16; six models without Witten-protected exotics"] = (
        all(v["singlet_mm"] == [0] for v in cf.values()) and len(none) == 6)
    best = [k for k in zero if k in none and k in both and k in tf]
    res["best_candidates"] = best
    checks["12148: best candidates = A8SM_10006 and A8SM_16222 (fraction-free, 3 gens, heavy t+b, |V_tb| = 1, no protected or light exotic, Lambda > 0, tachyon-free to 1.5)"] = (
        best == ["A8SM_20260928_10006_TF", "A8SM_20260928_16222_TF"])
    ed = json.loads((D / "edge.json").read_text())
    lm = {"0.52": lam(D / "oneloop_N004_F1_03_S002_0.52j_rho_K4.json"), "0.55": lam(D36 / "oneloop_N004_F1_03_S002_0.55j_rho_K4.json"),
          "0.58": lam(D / "oneloop_N004_F1_03_S002_0.58j_rho_K4.json"), "0.6": lam(D36 / "oneloop_N004_F1_03_S002_0.6j_rho_K3.json")}
    res["12149"] = dict(Lambda=lm, Delta_min={k: v["lowest"] for k, v in ed.items()})
    checks["12149: Lambda minimum among samples at 0.58i (115.14 < 115.39 (0.55i), 115.77 (0.6i), 117.27 (0.52i))"] = (
        lm["0.58"] < lm["0.55"] < lm["0.52"] and lm["0.58"] < lm["0.6"])
    dmin = min(ed, key=lambda k: ed[k]["lowest"])
    checks["12149: the 56-state level touches zero at the minimum (Delta_min = 3.5e-6 at 0.58i) and rises on both sides"] = (
        dmin == "0.58" and ed["0.58"]["lowest"] < 1e-5 and all(ed[k]["mult"] == 56 for k in ed)
        and ed["0.56"]["lowest"] > ed["0.58"]["lowest"] < ed["0.62"]["lowest"] and all(v["lowest"] >= 0 for v in ed.values()))
    sq = D / "edge_sqrt3.json"
    if sq.exists():
        s3 = json.loads(sq.read_text())
        res["12149_sqrt3"] = s3
        checks["12149: at Im T_WL = 1/sqrt3 the 56-state level is massless to 1e-9 (the touching point)"] = abs(s3["1/sqrt3"]["lowest"]) < 1e-9
    cg = json.loads((D / "congr.json").read_text())["summary"]
    res["12150"] = cg
    checks["12150: congruence v.U_f in Z reproduces the direct test 1080/1080; no admissible root has v.(V0+V1) and all v.W_i integral (0/1080)"] = (
        cg["n"] == 1080 and cg["agree"] == 1080 and cg["direct_fails"] == 1080 and cg["all_integral"] == 0 and cg["vV0V1"].get("0", 0) == 98)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
