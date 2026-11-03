"""Passes 12550-12557 (Claude track).  Not a theory of everything: see PASS12550_12557_DARK_MATTER_DRAG.md.

12550 -- CLASS patched for the fading dark sector, with controls that a sabotaged build fails.
12551 -- full Planck spectra + DESI + SNe reproduce the published (c, c'); c' = 0.05 stays near 2.6 sigma, about 3 with lensing added post hoc.
12552 -- dark matter drags light moduli along grad ln m: fixed point w_eff = 2 b^2/3, exact; KK dark matter on free moduli dilutes as a^-6.
12553 -- two-field fits: the data constrain b, the gradient norm in the light subspace, not a projection on the path.
12554 -- what is left: stabilise the modulus (mass at least 1e5 H0, not Hubble mass), couple only 4 to 7 percent of the dark matter, or a steep wall.
12555 -- beta fitted directly: cosmology alone gives |beta| of order 0.1, so the solar system decides.
12556 -- crossing w = -1 is not required: p = 0.1 to 0.27 under w >= -1 truth.
12557 -- clocks and neutrinos: alpha sequestered to 1e-7; rolling neutrino masses shift 12 times too little to see.
"""

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12550_to_12557_dark_drag.json"
SETS = ("dovekie", "desy5", "pantheon")


def load(n):
    return json.loads((D / n).read_text())


def main():
    checks, res = {}, {}

    # 12550
    ct = load("class_controls.json")
    res["controls"] = {k: ct[k] for k in ("port", "lambda_limit", "background", "trace", "growth", "noise")}
    checks["12550: plik-lite port returns planck-lite-py's reference chi2 to 1e-9"] = abs(ct["port"]["chi2"] - ct["port"]["expected"]) < 1e-9
    checks["12550: background agrees with the independent solver: H ratio within 3e-5 from z = 0 to 2"] = all(abs(a - b) < 3e-5 for a, b in zip(ct["background"]["Hratio_class"], ct["background"]["Hratio_py"]))
    t = ct["trace"]
    checks["12550: Einstein trace equation holds below 3e-5 at a > 0.1; the build with the Klein-Gordon source sign flipped fails above 0.3"] = max(t["patched"].values()) < 3e-5 and min(t["sabotage_kg_sign"].values()) > 0.3
    g = ct["growth"]
    checks["12550: growth at k = 0.2/Mpc follows G_eff = 1 + 2 c'^2 within 1e-4; G = 1 misses by 3 and 18 percent; the build with the CDM force sign flipped misses by over 100 percent"] = all(abs(g[k]["Geff"]) < 1e-4 for k in ("0.0", "0.1", "0.3")) and abs(g["0.1"]["G1"]) > 0.02 and abs(g["0.3"]["G1"]) > 0.15 and abs(g["sabotage_theta_sign_0.3"]["Geff"]) > 1
    pl = ct["planck_lcdm"]
    checks["12550: Planck-only LCDM: omega_b, omega_c, h, n_s within 0.5 sigma of the published plik values, chi2(plik-lite) near 586"] = abs(pl["p"]["wb"] - 0.02236) < 0.0001 and abs(pl["p"]["wc"] - 0.1202) < 0.0007 and abs(pl["p"]["h"] - 0.6727) < 0.003 and abs(pl["p"]["ns"] - 0.9649) < 0.003 and 580 < pl["parts"]["cmb"] < 592
    checks["12550: numerical floor is stated: scf at lambda = 0 against native Lambda differs by 0.29, and chi2 jitters by about 0.1"] = abs(ct["noise"]["native"] - ct["noise"]["scf"] - 0.29) < 0.02 and max(ct["noise"]["h_steps"].values()) < 0.1

    # 12551
    fits, lens = {}, {}
    for s in SETS + ("none",):
        p = D / f"class_fit_{s}.json"
        if p.exists() and "casimir" in load(p.name):  # a sample enters the table only when its fit grid is complete
            fits[s] = load(p.name)
        p = D / f"class_lens_{s}.json"
        if p.exists():
            lens[s] = load(p.name)
    table = {}
    for s, f in fits.items():
        l0 = f["LCDM"]["chi2"]
        row = {k: dict(delta=v["chi2"] - l0, c=v["p"].get("c"), cp=v["p"].get("cp"), S8=v["info"]["S8"], s8=v["info"]["s8"], w0=v["p"].get("w0"), wa=v["p"].get("wa"), lens=lens.get(s, {}).get(k, {}).get("chi2_lens")) for k, v in f.items() if isinstance(v, dict) and "chi2" in v}
        if "CPL" in row and "LCDM_native" in row:
            row["CPL"]["delta_vs_native"] = f["CPL"]["chi2"] - f["LCDM_native"]["chi2"]
        table[s] = row
    res["planck_table"] = table
    do = table["dovekie"]
    pub = dict(neg=(-0.92, 0.05), pos=(0.69, 0.05))
    checks["12551: Dovekie: both branches within 0.03 in c and 0.01 in c' of Table I of arXiv:2507.03090, which uses full Planck too"] = abs(do["free_neg"]["c"] - pub["neg"][0]) < 0.03 and abs(do["free_neg"]["cp"] - pub["neg"][1]) < 0.01 and abs(do["free_pos"]["c"] - pub["pos"][0]) < 0.03 and abs(do["free_pos"]["cp"] - pub["pos"][1]) < 0.01
    gain = do["exp_neg"]["delta"] - min(do["free_neg"]["delta"], do["prof_neg_0.05"]["delta"])
    res["cp_gain_dovekie_planck"] = gain
    checks["12551: full Planck: turning on c' gains 7.0 on Dovekie, the same as the compressed CMB within 0.5, so not an artefact of compression"] = 6.5 < gain < 7.5
    glens = gain + do["exp_neg"]["lens"] - do["prof_neg_0.05"]["lens"]
    res["cp_gain_dovekie_with_lens_post_hoc"] = glens
    checks["12551: lensing control: chi2 near the 19 bandpowers for LCDM; post hoc lensing adds 2.7 to the c' gain, and rejects c' = 0.1 by over 40"] = abs(do["LCDM"]["lens"] - 19) < 4 and 2 < do["exp_neg"]["lens"] - do["prof_neg_0.05"]["lens"] < 3.2 and do["prof_neg_0.1"]["lens"] - do["LCDM"]["lens"] > 40
    checks["12551: the c' profile is asymmetric: gain to c' = 0.05, then +54.7 against LCDM at c' = 0.1"] = do["prof_neg_0.02"]["delta"] > do["prof_neg_0.03"]["delta"] > do["prof_neg_0.05"]["delta"] and do["prof_neg_0.07"]["delta"] > do["prof_neg_0.05"]["delta"] and do["prof_neg_0.1"]["delta"] > 50
    cas = do["casimir"]["delta"] - do["free_pos"]["delta"]
    res["casimir_cost_dovekie_planck"] = cas
    checks["12551: Casimir line c = 4 c' costs 5.4 against free c > 0 on full Planck (compressed: 6.0)"] = 5 < cas < 6
    checks["12551: CPL control: w0 and wa near the DESI + CMB + Dovekie region"] = -0.9 < do["CPL"]["w0"] < -0.7 and -0.9 < do["CPL"]["wa"] < -0.5

    # 12552
    fx = load("dm_drag_fixed.json")
    x, b = sp.symbols("x b", positive=True)
    Om = 1 - x ** 2 / 6
    dl = -sp.Rational(1, 2) * (x ** 2 + 3 * Om)
    checks["12552: chi_N = 2 b is an exact fixed point with w_eff = 2 b^2/3"] = sp.simplify((-(3 + dl) * x + 3 * b * Om).subs(x, 2 * b)) == 0 and sp.simplify((-2 * dl / 3 - 1).subs(x, 2 * b) - 2 * b ** 2 / 3) == 0
    r = fx["rows"]
    res["fixed_points"] = {k: dict(b2=v["b_squared"], w_eff=v["w_eff_exact"], rho_slope=v["rho_c_slope_exact"]) for k, v in r.items()}
    checks["12552: KK dark matter on free moduli: w_eff = 1, rho_c ~ a^-6; fixed volume n = 1: w_eff = 1/3, rho_c ~ a^-4"] = r["m_KK all moduli free"]["w_eff_exact"] == "1" and r["m_KK all moduli free"]["rho_c_slope_exact"] == "-6" and r["m_KK fixed volume n=1"]["w_eff_exact"] == "1/3" and r["m_KK fixed volume n=1"]["rho_c_slope_exact"] == "-4"
    checks["12552: numerics reach each fixed point: chi_N within 1e-6 below b^2 = 3/2 and within 0.5 percent at the boundary"] = all(abs(v["chi_N_num"] - v["chi_N_exact"]) < 1e-6 for k, v in r.items() if k != "m_KK all moduli free") and abs(r["m_KK all moduli free"]["chi_N_num"] / r["m_KK all moduli free"]["chi_N_exact"] - 1) < 0.005

    # 12553
    dr = {s: load(f"dm_drag_{s}.json") for s in SETS}
    checks["12553: control: two-field code with V and m along one field returns the single-field chi2 within 1e-5"] = all(abs(d["control_two_field_vs_single"]["two_field"] - d["control_two_field_vs_single"]["single"]) < 1e-5 for d in dr.values())
    li = {s: {k: v["delta"] for k, v in d["light"].items()} for s, d in dr.items()}
    res["light_profile"] = li
    res["light_V_slopes_b005"] = {s: dict(c=d["light"]["0.05"]["c"], a=d["light"]["0.05"]["a"], delta=d["light"]["0.05"]["delta"], single=d["single_field"]["delta"]) for s, d in dr.items()}
    checks["12553: b = 0.05 reaches the single-field gain within 0.2 with V largely off the chi axis, so V's direction is not what the data fix"] = all(abs(v["delta"] - v["single"]) < 0.2 and abs(v["c"]) > 0.5 for v in res["light_V_slopes_b005"].values())
    checks["12553: light moduli, best found: b = 0.1 worse than LCDM by over 20; b = 0.2 by over 600; b = 1/sqrt 2 by over 3000; b = sqrt(3/2) by over 8000"] = all(v["0.1"] > 20 and v["0.2"] > 600 and v["0.7071"] > 3000 and v["1.2247"] > 8000 for v in li.values())

    # 12554
    md = load("dm_drag_mod.json")
    res["stabiliser"] = {k: {m: {q: x[q] for q in ("f", "range_kpc", "mu_eV", "stabiliser_scale_eV", "tuning_vs_Lambda")} for m, x in v["rows"].items()} for k, v in md.items() if k in ("0.7071", "1.2247")}
    checks["12554: control: mu -> 0 returns chi_N = 2 b"] = abs(md["control_light_chiN"]["num"] - md["control_light_chiN"]["exact"]) < 1e-6
    a7 = md["0.7071"]["rows"]
    checks["12554: b = 1/sqrt 2: range below 44 kpc needs mu >= 1e5 H0, where the modulus holds as much energy as the dark matter; f falls to 0.11 at 1e7 H0, 0.036 at 1e8 H0"] = abs(a7["5"]["range_kpc"] - 44.09) < 0.1 and 0.9 < a7["5"]["f"] < 1.05 and 0.1 < a7["7"]["f"] < 0.13 and 0.03 < a7["8"]["f"] < 0.04
    fr = {s: d["fraction"] for s, d in dr.items()}
    res["fraction"] = fr
    checks["12554: fraction escape: f b = c' keeps the gain within 2.2 of the single-field fit on all samples, b = 1/sqrt 2 and sqrt(3/2); f = 0.3 costs over 170"] = all(abs(v["delta"] - dr[s]["single_field"]["delta"]) < 2.2 for s in SETS for k, v in fr[s].items() if abs(v["product"] - dr[s]["single_field"]["cp"]) < 1e-6) and all(v["delta"] > 170 for s in SETS for k, v in fr[s].items() if abs(v["f"] - 0.3) < 1e-9)
    res["wall"] = {s: d.get("wall", {}) for s, d in dr.items()}
    checks["12554: a steep wall reduces the drag: lambda = 200 is far better than lambda = 50, but both remain worse than LCDM"] = all(d["wall"]["200.0"]["delta"] < d["wall"]["50.0"]["delta"] / 5 and d["wall"]["200.0"]["delta"] > 50 for d in dr.values())

    # 12555
    be = {s: load(f"dark_beta_{s}.json") for s in SETS}
    res["beta"] = {s: {k: d[k] for k in d if k.startswith("free_") or k.startswith("profile_")} for s, d in be.items()}
    checks["12555: control: beta = 0 returns fading_ds.py"] = all(abs(d["control_beta0"] - d["single"]["delta"]) < 1e-6 for d in be.values())
    flat = lambda d, s: {r["beta"]: r["delta"] for r in d[f"profile_{s}"]}
    checks["12555: |beta| = 0.03 costs at most 0.5 on all samples and both SN assumptions, so cosmology is at least about 7 times weaker than Cassini"] = all(abs(flat(d, s)[bb] - d["single"]["delta"]) < 0.5 for d in be.values() for s in ("s1", "s0") for bb in (-0.03, 0.03))
    checks["12555: with Cassini and LLR the joint fit has beta below 0.001 and xi about 0.03, on all samples and both SN assumptions"] = all(abs(d[k]["beta"]) < 0.001 and abs(d[k]["xi"]) < 0.04 for d in be.values() for k in ("free_s1_priors", "free_s0_priors"))

    # 12556
    pr = {s: load(f"dark_premium_{s}.json") for s in SETS}
    p2 = {s: load(f"dark_premium2_{s}.json") for s in SETS}
    res["premium"] = {s: dict(ceiling=pr[s]["ceiling"], free=pr[s]["free"], premium=pr[s]["premium"], p_linear=pr[s]["linear"]["p_real"], p_nonlinear=pr[s]["nonlinear"]["p_real"], n_nonlinear=pr[s]["nonlinear"]["n"], mean_linear=pr[s]["linear"]["mean"], mean_nonlinear=pr[s]["nonlinear"]["mean"], p_lcdm_ceiling=p2[s]["p_ceiling"], p_lcdm_free=p2[s]["p_free"]) for s in SETS}
    checks["12556: control: nine starts agree on the ceiling within 1e-5, and agree with differential evolution within 0.1 on the DES samples"] = all(max(pr[s]["ceiling_starts"]) - min(pr[s]["ceiling_starts"]) < 1e-5 for s in SETS) and abs(pr["dovekie"]["ceiling"] + 7.9) < 0.1 and abs(pr["desy5"]["ceiling"] + 14.8) < 0.1
    checks["12556: control: unbounded gain has mean near 16, the number of parameters; nonlinear and linear mock means agree within 1"] = all(abs(pr[s]["linear"]["control_unbounded_mean"] - 16) < 0.3 and abs(pr[s]["linear"]["mean"] - pr[s]["nonlinear"]["mean"]) < 1 for s in SETS)
    checks["12556: crossing w = -1 not required: premium p above 0.05 on all samples, linear and nonlinear"] = all(v["p_linear"] > 0.05 and v["p_nonlinear"] > 0.05 for v in res["premium"].values())
    checks["12556: LCDM against a w >= -1 history: DES-SN5YR p below 0.01, Dovekie below 0.05, Pantheon+ above 0.1"] = res["premium"]["desy5"]["p_lcdm_ceiling"] < 0.01 and res["premium"]["dovekie"]["p_lcdm_ceiling"] < 0.05 and res["premium"]["pantheon"]["p_lcdm_ceiling"] > 0.1

    # 12557
    ck = load("dd_clocks.json")
    res["clocks"] = ck
    checks["12557: optical clocks: d ln alpha / d phi below about 1e-7 and d ln mu / d phi below about 3e-6 at the fitted roll"] = all(v["kappa_alpha_max"] < 1.2e-7 and v["kappa_mu_max"] < 3e-6 for s in SETS for v in ck[s].values())
    checks["12557: rolling bulk neutrinos: at most 2.5 percent from recombination to today; a resolvable shift needs 12 times more"] = all(abs(v["dln_mnu_rec_to_0"]) < 0.025 for s in SETS for v in ck[s].values()) and 11 < ck["neutrino_scale"]["shortfall_factor"] < 13

    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    print({k: res[k] for k in ("cp_gain_dovekie_planck", "cp_gain_dovekie_with_lens_post_hoc", "casimir_cost_dovekie_planck")})
    print(json.dumps(res["premium"], indent=0, default=float))


if __name__ == "__main__":
    main()
