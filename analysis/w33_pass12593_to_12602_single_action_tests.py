"""Passes 12593-12602 (Claude track).  Not a theory of everything: see PASS12593_12602_SINGLE_ACTION_TESTS.md.

12593 -- E8 wall versus rolling radius: fixing alpha and fixing brane scales together freeze the radius.
12594 -- E8 x anti-E8: omega = 1/2 is discrete, Casimir coefficient 4 (n_H - n_V - 2) = -2 chi; G-flux must vanish, which removes the standard embedding.
12595 -- D3 at C^3/Z_3 needs M_s = 8e11 GeV while a 10 micron interval caps it near 1e8 GeV.
12596 -- real DES Y3 cosmic shear in the joint fit.
12597 -- out-of-sample prediction, with the leaked first version withdrawn; Laplace evidence.
12598 -- frozen predictions and brane classes, radion floor, bubble of nothing.
12599 -- random-chain flavour: the label bug and what survives.
12600 -- light cones and gravitons on F_q^4.
12601 -- one action, one scale: the closed loop fails.
12602 -- everpresent Lambda on DESI DR2.
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12593_to_12602_single_action_tests.json"


def load(n):
    return json.loads((D / n).read_text())


def main():
    checks, res = {}, {}

    # 12593, 12594
    hw = load("hw_wall_radius.json")
    res["hw"] = hw
    checks["12593: control: pure radius has beta = 1/sqrt 6 and d ln m_KK/d phi = sqrt(3/2)"] = abs(hw["branches"]["V_fixed"]["beta"] - 1 / math.sqrt(6)) < 1e-9 and abs(hw["branches"]["V_fixed"]["c_prime_mKK"] - math.sqrt(1.5)) < 1e-9
    checks["12593: V fixed misses Cassini by 163 in beta; V rho fixed misses the alpha clock by about 9e6"] = 160 < hw["beta_ratio_to_cassini_V_fixed"] < 166 and hw["alpha_ratio_to_clock_Vrho_fixed"] > 9e6
    checks["12593: no mix helps: best violation is still at least 160"] = hw["best_mix"]["max_violation"] > 160
    checks["12594: mode sums: gravity 8, vector 4, hyper -4 in units of S"] = all(abs(hw["mode_sums_over_S"][k] - v) < 1e-9 for k, v in dict(gravity=8, vector=4, hyper=-4).items())
    checks["12594: the net coefficient is -2 chi for every Hodge pair listed"] = all(r["net"] == -2 * r["chi"] for r in hw["hodge"].values())
    checks["12594: Witten's critical length is about 1e-19 of a 10 micron interval, so flux must vanish"] = hw["scales"]["10.0"]["rho_c_over_rho"] < 1e-18

    # 12595
    z3 = load("dd_d3_z3.json")
    res["d3"] = z3
    checks["12595: control: reproduces the paper's M_s = 9e11 within 10 percent and sin^2 within 0.001"] = abs(z3["control"]["Ms_GeV"] / 9e11 - 1) < 0.1 and abs(z3["control"]["sin2"] - 0.231) < 0.001
    checks["12595: control: the SM spectrum gives the paper's wrong sign 0.204"] = abs(z3["sm_spectrum_wrong_sign"]["sin2_b3m3"] - 0.204) < 0.001
    checks["12595: a 10 micron interval caps M_s below 2e8 GeV, over 4000 times below what the running needs"] = z3["ceiling"]["R10.0_alpha"]["Ms_max_GeV"] < 2e8 and z3["control"]["Ms_GeV"] / z3["ceiling"]["R10.0_alpha"]["Ms_max_GeV"] > 4000

    # 12596
    so = load("class_des_dovekie_shearonly.json")
    j = load("class_des_dovekie_joint.json")
    c = load("class_des_dovekie_joint_cut20.json")
    res["des"] = dict(shearonly=dict(S8=so["rows"]["LCDM"]["info"]["S8"], chi2=so["rows"]["LCDM"]["parts"]["des"], ndata=so["ndata"]))
    t = {k: j["rows"][k]["chi2"] - j["rows"]["LCDM"]["chi2"] for k in ("exp", "free_neg", "relax")}
    tc = {k: c["rows"][k]["chi2"] - c["rows"]["LCDM"]["chi2"] for k in ("exp", "free_neg")}
    res["des"].update(joint=t, joint_cut20=tc, ndata_joint=j["ndata"], ndata_cut20=c["ndata"], shear_chi2={k: j["rows"][k]["parts"]["des"] for k in j["rows"]}, S8={k: j["rows"][k]["info"]["S8"] for k in j["rows"]}, gain=t["exp"] - t["free_neg"], gain_cut20=tc["exp"] - tc["free_neg"])
    checks["12596: control: shear alone returns S8 = 0.789, within about 1 sigma of DES's 0.759 to 0.776, chi2 about 201 on 200"] = 0.76 < so["rows"]["LCDM"]["info"]["S8"] < 0.80 and 180 < so["rows"]["LCDM"]["parts"]["des"] < 220
    checks["12596: c' gain with real shear is 7.7, and shear chi2 moves by under 1"] = abs(res["des"]["gain"] - 7.74) < 0.05 and abs(j["rows"]["free_neg"]["parts"]["des"] - j["rows"]["LCDM"]["parts"]["des"]) < 1
    checks["12596: tighter cuts leave the gain near 7.4"] = abs(res["des"]["gain_cut20"] - 7.39) < 0.1

    # 12597
    sn = load("class_holdout_dovekie_sn_neutral.json")
    bao = load("class_holdout_dovekie_bao_neutral.json")
    ev = load("class_holdout_dovekie_evidence.json")
    res["holdout"] = dict(sn={m: [dict(start=r["start"], train=r["train_chi2"], held=r["held_chi2"]) for r in v] for m, v in sn["rows"].items()}, bao={m: [dict(start=r["start"], train=r["train_chi2"], held=r["held_chi2"]) for r in v] for m, v in bao["rows"].items()}, lnB=ev["lnB"])
    bestf = min(sn["rows"]["free_neg"], key=lambda r: r["train_chi2"])
    l0 = sn["rows"]["LCDM"][0]
    res["holdout"]["sn_best_train_gain"] = l0["held_chi2"] - bestf["held_chi2"]
    checks["12597: the lowest-training fading fit predicts held-out SN 5.2 better than LCDM"] = abs(res["holdout"]["sn_best_train_gain"] - 5.25) < 0.05
    checks["12597: the exponential does not: every start within 0.6 of LCDM on held SN"] = all(abs(r["held_chi2"] - l0["held_chi2"]) < 0.6 for r in sn["rows"]["exp"])
    fbao = bao["rows"]["free_neg"]
    checks["12597: BAO held out is not determined: fits within 0.6 in training scatter from 16 to 31 on BAO"] = max(r["held_chi2"] for r in fbao if r["train_chi2"] < 2244.5) - min(r["held_chi2"] for r in fbao if r["train_chi2"] < 2244.5) > 10
    bm = lambda rows: min(rows, key=lambda r: r["train_chi2"])
    cv = {m: bm(sn["rows"][m])["held_chi2"] + bm(bao["rows"][m])["held_chi2"] for m in ("LCDM", "exp", "free_neg", "cpl")}
    res["holdout"]["cross_validation_total"] = cv
    res["holdout"]["fading_best_case_total"] = bestf["held_chi2"] + min(r["held_chi2"] for r in fbao if r["train_chi2"] < 2244.0)
    checks["12597: CPL trained without SN is 14 to 18 worse than LCDM on SN at all starts, converged at w0 near -0.6"] = all(14 < r["held_chi2"] - l0["held_chi2"] < 18 and abs(r["p"]["w0"] + 0.6) < 0.05 for r in sn["rows"]["cpl"])
    checks["12597: CPL predicts BAO well: 15 to 17 at all starts against LCDM 36.8"] = all(15 < r["held_chi2"] < 17 for r in bao["rows"]["cpl"])
    checks["12597: cross-validation: fading beats CPL by over 6 and LCDM by over 10 even at its worse BAO fit"] = cv["cpl"] - cv["free_neg"] > 6 and cv["LCDM"] - cv["free_neg"] > 10
    checks["12597: Laplace ln B is under 2 for every model: weak by any scale"] = all(v["lnB"] < 2 for v in ev["lnB"].values())

    # 12598
    pr = load("class_prereg_dovekie.json")
    br = load("dd_brane_classes.json")
    res["prereg"] = dict(sha256=pr["sha256_of_models"], best={m: pr["models"][m]["best"] for m in pr["models"]}, sd={m: pr["models"][m].get("sd") for m in pr["models"]})
    res["brane"] = br
    checks["12598: predictions are frozen with a hash"] = len(pr["sha256_of_models"]) == 64
    checks["12598: cross-check with the parallel track: m_DM(rec)/m_DM(today) = 1.014 against their 1.0149"] = abs(pr["models"]["free_neg"]["best"]["rhoc_a3_ratio_1090.0"] - 1.0149) < 0.002
    checks["12598: b^2 = 5/6 for every Dp with the dilaton free, and control free gradient 3/2"] = abs(br["control_free_gradient_b2"] - 1.5) < 1e-9 and all(abs(r["b2"] - 5 / 6) < 1e-9 for k, r in br["D_branes"].items())
    checks["12598: dilaton fixed gives n/(n+1): D3 5/6 down to D7 1/2"] = abs(br["D_branes"]["D7"]["b_max_dilaton_fixed"] ** 2 - 0.5) < 1e-9 and abs(br["D_branes"]["D3"]["b_max_dilaton_fixed"] ** 2 - 5 / 6) < 1e-9
    checks["12598: Horava-Witten rank check: both constraints give b = 0"] = br["HW"]["b_with_both_constraints"] < 1e-9
    checks["12598: bubble of nothing: log10 B about 59 today"] = 59 < br["bubble_of_nothing"]["10.0"]["log10_B"] < 60

    # 12599
    fl = load("flavor_lyapunov.json")
    ch = load("flavor_chain2.json")
    uni = {k: load(f"flavor_unified_{k}.json") for k in ("fwd", "inv", "sym")}
    res["flavour"] = dict(quark_best={k: dict(lnL=v["lnL"], chi2=v["chi2"]) for k, v in fl["best"].items()}, marginal=ch["chain_marginal"], FN=dict(n=ch["FN_marginal"]["n"], lnZ=ch["FN_marginal"]["lnZ"], best=ch["FN_marginal"]["best"]), universal=ch["universality"], unified={k: dict(lnZ=v["chain"]["lnZ"], best=v["chain"]["best"]["lnL"], LT=v["chain"]["best"]["LT"], LR=v["chain"]["best"]["LR"], p=v["chain"]["best"]["p"], cond=v["conditional_tol3.0"]) for k, v in uni.items()}, unified_FN=dict(lnZ=uni["fwd"]["FN"]["lnZ"], best=uni["fwd"]["FN"]["best"]["lnL"]))
    checks["12599: control: r -> 1/2 for Ginibre at large L, 1 for symmetric hops"] = abs(fl["control_r"]["L40_fwd"]["median_r"] - 0.5) < 0.05 and abs(ch["universality"]["1.0"]["median_r"] - 1) < 0.05
    checks["12599: control: inverse chain r -> 2"] = abs(fl["control_r"]["L40_inv"]["median_r"] - 2) < 0.1
    checks["12599: corrected forward chain has th12 < th23, opposite to data"] = fl["best"]["fwd"]["mean"][4] < fl["best"]["fwd"]["mean"][5]
    checks["12599: corrected inverse chain has th12 > th23, as in data"] = fl["best"]["inv"]["mean"][4] > fl["best"]["inv"]["mean"][5]
    checks["12599: SL(3) hops make arg det zero, a tautology for masses and angles: no change in score over 0.1"] = ch["sl3"]["max_abs_argdet_sl3"] < 1e-9 and abs(ch["chain_marginal"]["None_sl3False"]["lnZ"] - ch["chain_marginal"]["None_sl3True"]["lnZ"]) < 0.1
    checks["12599: all flavour: chains and FN within 1 in lnZ: no decision"] = all(abs(uni[k]["chain"]["lnZ"] - uni["fwd"]["FN"]["lnZ"]) < 1 for k in uni)
    checks["12599: FN beats chains at best point on quarks"] = fl["best"]["FN"]["lnL"] > fl["best"]["fwd"]["lnL"]

    # 12600
    nc = load("null_cone_dims.json")
    fg = load("finite_graviton.json")
    res["cone"] = dict(order=nc["order_by_dim"], d4=nc["d4_pattern"])
    res["graviton"] = fg
    checks["12600: control: d = 3 spectra match the parallel track at q = 3 and 5"] = nc["control_d3_q3"] and nc["control_d3_q5"]
    checks["12600: q = 3, (1, 3) is SRG(81, 20, 1, 6), prior art in Pass 11831"] = any(r["q"] == 3 and r["d"] == 4 and r["signature"] == [1, 3] and r.get("srg") == [81, 20, 1, 6] for r in nc["rows"])
    checks["12600: q = 3 mod 4 separates (1, 3) from (2, 2) by Witt index; q = 5 does not"] = nc["d4_pattern"]["3"]["(1, 3)"]["witt"] == 1 and nc["d4_pattern"]["3"]["(2, 2)"]["witt"] == 2 and nc["d4_pattern"]["7"]["(1, 3)"]["witt"] == 1 and nc["d4_pattern"]["5"]["(1, 3)"]["witt"] == 2
    checks["12600: control over Q: null rank 4, non-null 6, massive 5"] = fg["control_Q"]["rank_null"] == 4 and fg["control_Q"]["rank_nonnull"] == 6 and fg["control_Q"]["massive_kernel"] == 5
    checks["12600: two polarisations at every sampled null momentum over all fields, zero Bianchi and gauge failures"] = all(r["bad_gauge"] == 0 and r["bad_bianchi"] == 0 and not any(k.startswith("('null'") and not k.endswith(", 2)") for k in r["census"]) for r in fg["rows"].values())
    checks["12600: my characteristic-3 worry is false: massive kernel 5 at q = 3"] = fg["rows"]["3"]["massive_kernel"] == {"5": 60}
    checks["12600: at q = 3 helicities +2 and -2 coincide in SO(2) and in Omega, and in Omega equal a scalar"] = fg["rows"]["3"]["helicity"]["SO2"]["graviton_pm2_distinct"] is False and fg["rows"]["3"]["helicity"]["Omega"]["graviton_same_as_scalar"] is True
    checks["12600: compact q = 7 separates +-2 in SO(2) but not in Omega; 11 in both"] = fg["rows"]["7"]["helicity"]["SO2"]["graviton_pm2_distinct"] and not fg["rows"]["7"]["helicity"]["Omega"]["graviton_pm2_distinct"] and fg["rows"]["11"]["helicity"]["Omega"]["graviton_pm2_distinct"]

    # 12601
    os_ = load("toe_one_scale.json")
    res["one_scale"] = os_
    checks["12601: control: the paper's 0.2315 and 8.3e11 with TeV SUSY"] = abs(os_["control_paper"]["sin2"] - 0.2315) < 0.0005 and abs(os_["control_paper"]["Ms"] / 8.3e11 - 1) < 0.01
    checks["12601: closing the loop at kappa = 1 misses sin^2 by -8.4 percent"] = abs(os_["closed_loop"]["k1.0_r1.0"]["pull_percent"] + 8.4) < 0.1
    checks["12601: neutrino v^2/M_s is over 700 times too heavy: the 0.04 eV estimate was an arithmetic slip"] = os_["sectors"]["paper"]["m_nu_over_atm"] > 700
    checks["12601: dark energy is about 60 orders below M_SUSY^4"] = os_["sectors"]["closed_k1"]["rho_DE_over_MSUSY4"] < 1e-55

    # 12602
    cone = load("everpresent_lambda_dovekie_cone.json")
    como = load("everpresent_lambda_dovekie_comoving.json")
    wide = load("everpresent_lambda_dovekie_comoving_wide.json")
    res["everpresent"] = dict(LCDM=cone["LCDM_chi2"], cone=cone["rows"], comoving_large=como["rows"], comoving_wide=wide["rows"])
    checks["12602: light-cone form: no history in the h window at alpha <= 1; the alpha = 3 row reaches it, the control, and is ruined"] = all(cone["rows"][a]["h_window"] == 0 for a in ("0.003", "0.01", "0.03", "0.1", "0.3", "1.0")) and cone["rows"]["3.0"]["h_window"] > 0 and cone["rows"]["3.0"]["best_delta"] > 1000
    checks["12602: comoving form spares recombination: early fraction under 1 percent at alpha = 0.3"] = como["rows"]["0.3"]["early_fraction_rms"] < 0.01
    checks["12602: comoving form fails: best history +46 and mean ln Z -37 against best-fit LCDM at the best alpha"] = abs(como["rows"]["0.2"]["best_delta"] - 46.1) < 0.2 and abs(como["rows"]["0.2"]["lnZ_minus_LCDM"] + 36.9) < 0.2

    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    for k, v in checks.items():
        print(("PASS" if v else "FAIL"), k.encode("ascii", "replace").decode())
    print("all_checks_pass", res["all_checks_pass"])


if __name__ == "__main__":
    main()
