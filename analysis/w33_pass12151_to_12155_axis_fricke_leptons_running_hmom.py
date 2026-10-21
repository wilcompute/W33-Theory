"""Passes 12151-12155: the candidates' Wilson-line axis, the Fricke symmetry behind i/sqrt3, leptons and neutrinos of the candidates,
gauge running at k_Y = 17/3, and the calibrated higher-point H-momentum rule -- with two CORRECTIONS (Claude track).

12155 -- CORRECTION to 12133/12138/12146. The corpus selection-rule engine (w33_so16_selection_rules.py, Pass 11102) fixes the
  higher-point H-momentum rule: sum R = 0 exactly for a cubic psi psi phi, 0 mod 3 once extra scalars are attached. Imposing it on the
  quartic psi psi <s1><s2> terms (which 12133/12146 had left out, so their lifts were only upper bounds): the two 'best candidates'
  keep 11 (A8SM_10006) and 12 (A8SM_16222) light vector-like pairs instead of 0; T115 keeps 7 (not 1); S002 29 (not 12); the 16
  crossed models lift at most one pair each. Quartic order lifts almost nothing. (12142's Witten-parity statement is unaffected.)
12154 -- gauge running: with the SM spectrum, string boundary conditions k_3 = k_2 = 1 and k_Y = 17/3 give sin^2 theta_W(M_Z) = 0.109
  (M_s solved from alpha_em, alpha_s: an absurd 7e5 GeV) or 0.088 at the heterotic M_s ~ 2.7e17 GeV (alpha_em^-1(M_Z) = 342);
  control k_Y = 5/3 gives 0.208 / 0.202 (the known non-SUSY shortfall). The measured value needs k_Y ~ 1.29. The fraction-free
  hypercharges (k_Y >= 17/3) are excluded by the Weinberg angle unless huge threshold corrections or light extra matter intervene.
12153 -- leptons (trilinear, local couplings, exact H-momentum): A8SM_10006 has NO charged-lepton Yukawa (rank 0) and no Dirac
  neutrino coupling; A8SM_16222 has charged-lepton rank 3 and Dirac couplings to exactly 3 singlets N, whose Majorana mass matrix
  is ZERO at trilinear and at quartic order (mod-3 H-momentum) -- Dirac neutrinos at the electroweak scale. With 12154 and 12155,
  CORRECTION to 12146-12148: the two 'best candidates' are NOT viable.
12152 -- the Fricke symmetry: S002's lowest Witten-sector level is EXACTLY invariant under T_WL -> -1/(3 T_WL) on the axis
  (Delta(0.5i) = Delta(0.6667i) = 0.0034543236939, Delta(0.52i) = Delta(0.6410i) = 0.0018258998578, 13 digits); i/sqrt3 is its
  fixed point, so the non-negative level is stationary there and touches zero (12149). The full one-loop Lambda is only
  approximately invariant (Lambda(0.52i) = 117.27 vs Lambda(0.641i) = 118.72; Lambda(0.55i) = 115.39 vs Lambda(0.606i) = 116.07).
12151 -- the axis of A8SM_10006: Lambda/M^4 = 652 (2i), 374 (1.5i), 175 (i), tachyon-free to i (lowest level a 40-state
  multiplet at Delta = 0.052; 0.9i: 16 states at +0.020), TACHYONIC at 0.8i (16 states, Delta = -0.038) and at i/sqrt3 (Delta =
  -1/6): no tachyon-free path to i/sqrt3. A8SM_16222 the same: 703 (2i), 421 (1.5i), 217 (i, 48 states at +0.052), tachyonic at
  0.8i (16 states, -0.038). Both roll toward small radius with Lambda > 0 into a tachyon between 0.9i and 0.8i.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12151_to_12155_axis_fricke_leptons_running_hmom.json"
D = ROOT / "analysis" / "search_drivers_12151"
D46 = ROOT / "analysis" / "search_drivers_12146"
D36 = ROOT / "analysis" / "search_drivers_12136"


def lam(p):
    return json.loads(p.read_text())["Lambda_over_M4"]


def main():
    checks, res = {}, {}
    hm = json.loads((D / "crossexo_hm.json").read_text())
    old = json.loads((D46 / "crossexo.json").read_text())
    tq = json.loads((D / "exomass4_hm.json").read_text())
    res["12155"] = dict(candidates={k: [old[k]["light_up_to_quartic"], hm[k]["light_up_to_quartic"]] for k in hm},
                        T115=tq["N008_F1_04_S037_T115"]["light_up_to_quartic"], S002=tq["N004_F1_03_S002"]["light_up_to_quartic"])
    checks["12155: with the mod-3 H-momentum rule at quartic order the candidates keep 11 / 12 light pairs (were 0 / 0); T115 7 (was 1); S002 29 (was 12)"] = (
        hm["A8SM_20260928_10006_TF"]["light_up_to_quartic"] == 11 and hm["A8SM_20260928_16222_TF"]["light_up_to_quartic"] == 12
        and tq["N008_F1_04_S037_T115"]["light_up_to_quartic"] == 7 and tq["N004_F1_03_S002"]["light_up_to_quartic"] == 29
        and all(v["light_trilinear"] - v["light_up_to_quartic"] <= 3 for v in hm.values()))
    rn = json.loads((D / "running.json").read_text())
    res["12154"] = rn
    k17 = rn["5.6667"]
    k5 = rn["1.6667"]
    checks["12154: k_Y = 17/3 gives sin^2(M_Z) = 0.109 (solved) / 0.088 (heterotic M_s); control 5/3: 0.208 / 0.202; measured needs k_Y ~ 1.29"] = (
        abs(k17["a_solve_from_aem_as"]["sin2_MZ"] - 0.1088) < 1e-3 and abs(k17["b_kaplunovsky"]["sin2"] - 0.0884) < 1e-3
        and abs(k5["a_solve_from_aem_as"]["sin2_MZ"] - 0.2076) < 1e-3 and abs(rn["kY_needed_for_measured"]["kY"] - 1.2916) < 1e-3)
    lp = json.loads((D / "leptons.json").read_text())
    lq = json.loads((D / "leptons_q.json").read_text())
    res["12153"] = dict(trilinear=lp, quartic_majorana=lq)
    a, b = lp["A8SM_20260928_10006_TF"], lp["A8SM_20260928_16222_TF"]
    checks["12153: 10006 charged-lepton rank 0, no Dirac nu; 16222 lepton rank 3, Dirac nu to 3 N with zero Majorana mass at trilinear and quartic order"] = (
        a["lepton_rank"] == 0 and a["dirac_rank"] == 0 and b["lepton_rank"] == 3 and b["dirac_rank"] == 3 and b["n_N_with_dirac"] == 3
        and b["majorana_rank_on_dirac_N"] == 0 and lq["A8SM_20260928_16222_TF"]["majorana_quartic_rank_on_dirac_N"] == 0)
    fr = json.loads((D / "fricke.json").read_text())
    pairs = [("0.500000", "0.666667"), ("0.520000", "0.641026")]
    res["12152"] = dict(levels=fr, Lambda={"0.52": lam(D46 / "oneloop_N004_F1_03_S002_0.52j_rho_K4.json"),
                                           "0.641": lam(D / "oneloop_N004_F1_03_S002_0.6410256410256411j_rho_K4.json"),
                                           "0.55": lam(D36 / "oneloop_N004_F1_03_S002_0.55j_rho_K4.json"),
                                           "0.606": lam(D / "oneloop_N004_F1_03_S002_0.6060606060606061j_rho_K4.json")})
    checks["12152: lowest Witten level exactly invariant under T -> -1/(3T) (two pairs, 1e-12); Lambda only approximately (within 1.5%)"] = (
        all(abs(fr[x]["lowest"][0] - fr[y]["lowest"][0]) < 1e-12 for x, y in pairs)
        and 0 < abs(res["12152"]["Lambda"]["0.641"] / res["12152"]["Lambda"]["0.52"] - 1) < 0.015
        and 0 < abs(res["12152"]["Lambda"]["0.606"] / res["12152"]["Lambda"]["0.55"] - 1) < 0.015)
    c10 = json.loads((D / "candaxis_10006.json").read_text())["A8SM_20260928_10006_TF"]
    res["12151_10006"] = c10
    checks["12151: A8SM_10006 Lambda 374 (1.5i), 175 (i) tachyon-free; tachyonic at 0.8i (16 states, Delta = -0.038)"] = (
        abs(c10["1.500000"]["Lambda"] - 373.55) < 0.1 and abs(c10["1.000000"]["Lambda"] - 174.65) < 0.1 and c10["1.000000"]["lowest"] > 0
        and c10["0.800000"]["lowest"] < 0 and c10["0.800000"]["mult"] == 16)
    p16 = D / "candaxis_16222.json"
    if p16.exists():
        c16 = json.loads(p16.read_text())["A8SM_20260928_16222_TF"]
        res["12151_16222"] = c16
        checks["12151: A8SM_16222 Lambda 421 (1.5i), 217 (i) tachyon-free; tachyonic at 0.8i (16 states, Delta = -0.038)"] = (
            abs(c16["1.500000"]["Lambda"] - 420.68) < 0.1 and abs(c16["1.000000"]["Lambda"] - 216.76) < 0.1 and c16["1.000000"]["lowest"] > 0
            and c16["0.800000"]["lowest"] < 0 and c16["0.800000"]["mult"] == 16)
    l10 = D / "lev10006.json"
    if l10.exists():
        lv = json.loads(l10.read_text())
        res["12151_10006_levels"] = lv
        checks["12151: A8SM_10006 tachyon-free at 0.9i (+0.020), tachyonic at i/sqrt3 (Delta = -1/6)"] = (
            lv["0.900000"]["lowest"] > 0 and abs(lv["0.577350"]["lowest"] + 1 / 6) < 1e-9)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
