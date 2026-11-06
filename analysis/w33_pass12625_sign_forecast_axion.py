"""Pass 12625 producer (claude track): sign of the fading coupling (Laplace two-mode weights, growth), frozen DR3 BAO predictions and forecast, axion-DM coupling routes, SPT check.
Reads analysis/toe_uv/{modes_laplace,dr3_forecast,sign_growth,axion_de_route,dr3_prereg}.json and dr3_prereg.sha256; writes data/w33_pass12625_sign_forecast_axion.json.
usage: py -3 analysis/w33_pass12625_sign_forecast_axion.py"""
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UV = os.path.join(ROOT, "analysis", "toe_uv")


def L(n):
    return json.load(open(os.path.join(UV, n), encoding="utf-8"))


ml, fc, sg, ax = L("modes_laplace.json"), L("dr3_forecast.json"), L("sign_growth.json"), L("axion_de_route.json")
sha_file = open(os.path.join(UV, "dr3_prereg.sha256")).read().split()[0]
sha_now = hashlib.sha256(open(os.path.join(UV, "dr3_prereg.json"), "rb").read().replace(b"\r\n", b"\n")).hexdigest()
dr3 = {k: v for k, v in fc.items() if k.endswith("DR3_sqrt35")}
routes = ax["routes"]
checks = dict(
    dovekie_full_mildly_prefers_c_negative=0.1 < ml["dovekie_full"]["P_c_positive"] < 0.5,
    desy5_bao_held_laplace_flagged_invalid=ml["desy5_bao_held"]["neg"]["sigma_cp"] > 0.2,
    bao_blind_to_sign_even_at_dr3=all(v["free_neg_vs_free_pos"] < 0.5 for v in dr3.values()),
    dr3_bao_cannot_split_fading_cpl=all(v["CPL_vs_free_neg"] < 5 for v in dr3.values()),
    dr3_bao_separates_evolving_from_lcdm=all(min(v["LCDM_vs_CPL"], v["LCDM_vs_free_neg"]) > 4 for v in dr3.values()),
    growth_S8_separates_sign=all(abs(sg[f"{d}_free_neg"]["S8"] - sg[f"{d}_free_pos"]["S8"]) > 0.008 for d in ("dovekie", "desy5")),
    fs8_nearly_blind_to_sign=all(max(abs(sg[f"{d}_free_neg"]["fs8"][z] - sg[f"{d}_free_pos"]["fs8"][z]) for z in sg[f"{d}_free_neg"]["fs8"]) < 0.003 for d in ("dovekie", "desy5")),
    lambda_qcd_route_excluded=all(r["Lambda_QCD"]["cassini_ratio"] > 10 and r["Lambda_QCD"]["clock_ratio"] > 1e3 for r in routes.values()),
    higgs_vev_route_excluded=all(r["higgs_vev"]["cassini_ratio"] > 10 and r["higgs_vev"]["clock_ratio"] > 1e3 for r in routes.values()),
    fa_route_needs_portal_below_1e18=all(v < 1e-18 for v in ax["higgs_portal_cap"].values()),
    dr3_prereg_hash_intact=sha_file == sha_now,
)
out = dict(pass_number=12625, track="claude", laplace=ml, dr3_forecast=fc, sign_growth=sg, axion_routes=ax, dr3_prereg_sha256=sha_file, checks=checks, all_checks_pass=all(checks.values()))
json.dump(out, open(os.path.join(ROOT, "data", "w33_pass12625_sign_forecast_axion.json"), "w"), indent=1, default=float)
for k, v in checks.items():
    print(k, v)
print("all_checks_pass", out["all_checks_pass"])
