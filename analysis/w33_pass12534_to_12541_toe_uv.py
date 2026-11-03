"""Passes 12534-12541 (Claude track): quantum-gravity constraints on the Standard Model, tested against measurement.  Not a theory of everything: see the verdict in PASS12534_12541_TOE_UV_CONSTRAINTS.md.

12534 -- no-AdS3: Dirac, normal ordering, sum m_nu in [58.8, 69.9] meV.
12535 -- asymptotic safety: branch A predicts M_t = 182 GeV (measured 172.57); branch B fits; the relevance table.
12536 -- criticality: lambda = beta_lambda = 0 cannot hit both masses; M_H = 125.20 needs M_t about 170.9.
12537 -- NNLO: lambda(M_Pl) = 0 needs M_t = 171.04 +- 0.37; pulls 3.0, 2.1, 1.2 sigma by measurement.
12538 -- no-fit gravity: an apparent hit at M_t = 172.74 is killed by scheme dependence; Lambda* must be known to about 1%.
12539 -- no-AdS3: at most 2 extra massless bosonic dof.
12540 -- regulator spread at one scheme: Lambda* 91% for SM matter, exponents 5% and 0.4%: 1% in Lambda* is not reachable.
12541 -- DESI: lam = sqrt 2 excluded about 4.4 sigma, sqrt(2/3) about 1.5 sigma; three generations not selected.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12534_to_12541_toe_uv.json"


def load(name):
    return json.loads((D / name).read_text())


def main():
    checks, res = {}, {}
    c, s, a, k, mp = (load(n) for n in ("sm_rge_control.json", "swampland_casimir.json", "as_fixedpoint.json", "criticality.json", "mpp_k.json"))
    res.update(control=c, swampland=s, asymptotic_safety=a, criticality=k, mpp=mp)
    checks["control: two-loop RGEs reproduce Buttazzo eq. 61 (g within 3e-4, y_t within 1e-3, lambda within 1e-3) and its slopes"] = (
        all(abs(c["got"][x] - c["published"][x]) < 3e-4 for x in ("g1", "g2", "g3")) and abs(c["got"]["yt"] - c["published"]["yt"]) < 1e-3 and abs(c["got"]["lam"] - c["published"]["lam"]) < 1e-3
        and abs(c["dlam_dmt"] + 0.0066) < 3e-4 and abs(c["dlam_dmh"] - 0.0029) < 2e-4)
    old = {(r["order"], r["kind"]): r for r in s["old"]}
    cur = {(r["order"], r["kind"]): r for r in s["current"]}
    checks["control: the Casimir code gives bounds near the published 7.7 and 2.5 meV"] = abs(cur[("NO", "Dirac")]["bound"] * 1e3 - 7.7) < 0.3 and abs(cur[("IO", "Dirac")]["bound"] * 1e3 - 2.5) < 0.2
    checks["12534: Majorana has AdS3 at every mass tested, for both orderings; Dirac NO and IO have upper bounds"] = (
        cur[("NO", "Majorana")]["bound"] is None and cur[("IO", "Majorana")]["bound"] is None and "AdS3" in cur[("NO", "Majorana")]["status"] and "below the bound" in cur[("NO", "Dirac")]["status"] and "below the bound" in cur[("IO", "Dirac")]["status"])
    checks["12534: NO window [58.8, 69.9] meV contains DESI's 64.2 meV limit; the IO floor exceeds it"] = (
        abs(s["sum_floor_NO_eV"] * 1e3 - 58.8) < 0.1 and abs(cur[("NO", "Dirac")]["sum_at_bound"] * 1e3 - 69.9) < 0.1 and s["sum_floor_NO_eV"] < s["desi_95_eV"] < cur[("NO", "Dirac")]["sum_at_bound"] and s["sum_floor_IO_eV"] > s["desi_95_eV"])
    main_ = a["k_1e19"]
    checks["12535: branch A predicts M_t = 182.0 GeV at k = 1e19, reproducing the paper and missing 172.57 by over 9 GeV"] = abs(main_["A"]["mt"] - 182.0) < 0.5 and main_["A"]["mt"] - 172.57 > 9
    sc = {x["k_tr"]: x for x in a["k_tr_scan"]}
    checks["12535: lowering k_tr to 1e16 still leaves M_t above 177 GeV"] = sc[1e16]["Mt_A"] > 177
    tb = main_["table_B"]
    checks["12535: relevance table branch B, b and Dirac and light-down IR-attractive to zero; up and leptons relevant"] = tb["third_gen_b"] > 0 and tb["dirac_neutrino"] > 0 and tb["down_light"] > 0 and tb["up_light"] < 0 and tb["charged_lepton"] < 0
    G = main_["gY_kt"] ** 2
    an = a["analytic_branch_A"]["values"]
    checks["12535: analytic branch A: Dirac +G/6, down +G/2, up -G/2, lepton -17G/6"] = abs(an["dirac"] - G / 6) < 1e-9 and abs(an["down_light"] - G / 2) < 1e-9 and abs(an["up_light"] + G / 2) < 1e-9 and abs(an["lepton"] + 17 * G / 6) < 1e-9
    checks["12535: branch B far-UV y_t* near the frontier's 0.25"] = abs(tb["t"] ** 0.5 - 0.25) < 0.03
    mh = [h["MH"] for h in a["higgs_at_measured_Mt"] if h["MH"]]
    checks["12535: fixed-point Higgs 127-129 GeV at measured M_t, above 125.20"] = all(127 < x < 129 for x in mh)
    checks["12536: critical points never hit both masses: M_t within 1 GeV and M_H within 1 GeV are not simultaneous"] = not any(abs(x["dMt"]) < 1 and abs(x["dMH"]) < 1 for x in k["scan"])
    checks["12536: M_H = 125.20 at criticality needs M_t near 170.8; lambda(1e19) = 0 needs M_t near 170.9"] = abs(mp["0.118"]["Mt"] - 170.83) < 0.1 and abs(a["Mt_for_lambda_MP_zero_at_measured_MH"] - 170.86) < 0.1
    n, ms, st = load("nnlo_top.json"), load("matter_scan.json"), load("scheme_test.json")
    res.update(nnlo=n, matter_scan=ms, scheme_test=st)
    cmp_ = n["comparisons"]
    checks["12537: lambda(M_Pl) = 0 needs M_t = 171.04 +- 0.37; pulls 3.0, 2.1, 1.2 sigma"] = abs(n["Mt_for_lambda_MPl_zero"] - 171.04) < 0.01 and abs(n["error_total"] - 0.37) < 0.01 and abs(cmp_["direct_run1_combination"]["pull_sigma"] - 3.0) < 0.05 and abs(cmp_["direct_with_0p5_interpretation"]["pull_sigma"] - 2.1) < 0.05 and abs(cmp_["preliminary_pole_combination"]["pull_sigma"] - 1.2) < 0.05
    pm = ms["published_models"]
    checks["12538: interacting hypercharge overshoots g_Y(M_Pl) by over a factor 2 for every published model with matter"] = all(pm[x]["interacting"]["gY_MP"] > 2 * 0.476 for x in ("SM", "SM_3nuR", "SM_dm_scalar", "SM_3nuR_axion_dm", "EH_1707"))
    checks["12538: the hit: SM + 3 nu_R + axion + DM, Gaussian, M_t 172.74, M_H 128.82; SM has no top fixed point in 1L-II"] = abs(pm["SM_3nuR_axion_dm"]["gaussian"]["Mt"] - 172.74) < 0.02 and abs(pm["SM_3nuR_axion_dm"]["gaussian"]["MH"] - 128.82) < 0.02 and "no top" in pm["SM"]["gaussian"]["status"]
    sm_ = st["SM_matter_by_scheme"]
    checks["12538: the kill: the same SM matter gives M_t 171.87 (1L-Ia), 167.94 (full-Ia), none in type II; dM_t/dLambda about -37; about 2% of the region within 1 GeV"] = (
        abs(sm_["1L-Ia"]["Mt"] - 171.87) < 0.02 and abs(sm_["full-Ia"]["Mt"] - 167.94) < 0.02 and sm_["1L-II"]["Mt"] is None and sm_["full-II"]["Mt"] is None and abs(st["dMt_dLambda"] + 37) < 1 and 0.01 < st["fraction_within_1_GeV"] < 0.04)
    ext_p = D / "swampland_ext.json"
    if ext_p.exists():
        ex = load("swampland_ext.json"); res["swampland_ext"] = ex
        r_ = {x["nb"]: x for x in ex["extra_massless_bosons"]}
        checks["12539: extra massless bosons: bounds 7.65, 5.29, 2.84 meV for 0, 1, 2; AdS3 at m1 = 0 for 3 or more"] = abs(r_[4]["m1_bound"] * 1e3 - 7.65) < 0.02 and abs(r_[5]["m1_bound"] * 1e3 - 5.29) < 0.02 and abs(r_[6]["m1_bound"] * 1e3 - 2.84) < 0.02 and r_[7]["m1_bound"] is None and r_[8]["m1_bound"] is None
        dd = {round(x["m_KK_eV"], 4): x for x in ex["dark_dimension_bulk_nuR"]}
        checks["12539: bulk right-handed tower leaves the m1 bound near 7.65 meV for m_KK >= 0.03 eV and tightens it below that; graviton tower alone has AdS3 at m1 = 0 at every m_KK"] = (
            abs(dd[0.1]["m1_bound_meV"] - 7.65) < 0.05 and abs(dd[0.03]["m1_bound_meV"] - 7.65) < 0.05 and dd[0.001]["m1_bound_meV"] < dd[0.01]["m1_bound_meV"] < 7.65 and all(x["AdS3_at_m1_0"] for x in ex["dark_dimension_graviton_only"]))
    fr, qd, ng = load("frg_regulators.json"), load("quintessence_desi.json"), load("ngen_scan.json")
    res.update(frg=fr, quintessence=qd, ngen=ng)
    pu = fr["pure"]["('opt',)"][0]
    checks["12540: control: pure gravity optimised g* = 0.7073, lam* = 0.1932; SM optimised within 5% of Eichhorn-Held's (3.29, -4.51)"] = abs(pu["g"] - 0.7073) < 2e-3 and abs(pu["Lam"] - 0.1932) < 1e-3 and abs(fr["SM"]["('opt',)"][0]["g"] / 3.29 - 1) < 0.05 and abs(fr["SM"]["('opt',)"][0]["Lam"] / -4.51 - 1) < 0.05
    su = fr["summary"]["SM"]
    checks["12540: SM matter over 5 regulators: Lambda* spread near 91%, far above 1%"] = su["n"] == 5 and abs(su["spread_frac_Lam"] - 0.91) < 0.02
    th = [sorted(abs(complex(str(x).replace(" ", ""))) for x in v[0]["theta"]) for k_, v in fr["SM"].items()]
    checks["12540: SM critical exponents stable: theta_1 within 2.0-2.2 and theta_2 within 3.9-4.0 for all regulators"] = all(2.0 < t[0] < 2.2 and 3.9 < t[1] < 4.0 for t in th)
    lc, cp = qd["LCDM"], qd["CPL"]
    checks["12541: control: LCDM Omega_m near 0.30; w0wa near the published -0.42, -1.75; improves LCDM"] = abs(lc["om"] - 0.303) < 0.005 and abs(cp["w0"] + 0.42) < 0.21 and abs(cp["wa"] + 1.75) < 0.58 and cp["delta_chi2"] < -5
    q_ = {round(x["lam"], 3): x for x in qd["quintessence"]}
    checks["12541: Delta chi2 rises monotonically with lam, about +2.2 at 0.816 and +19.7 at 1.414; quintessence never beats LCDM"] = abs(q_[0.816]["delta_chi2_vs_LCDM"] - 2.19) < 0.1 and abs(q_[1.414]["delta_chi2_vs_LCDM"] - 19.66) < 0.2 and all(x["delta_chi2_vs_LCDM"] > 0 for x in qd["quintessence"]) and all(a_["delta_chi2_vs_LCDM"] < b_["delta_chi2_vs_LCDM"] for a_, b_ in zip(qd["quintessence"], qd["quintessence"][1:]))
    checks["12541: generations: the constraints allow 3, 4, 5 and do not select 3"] = ng["allowed_by_all"] == [3, 4, 5]
    checks = {x: bool(v) for x, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
