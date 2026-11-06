"""Pass 12626 producer (claude track): prior-truncated posterior-predictive reruns, the model scorecard, coupled-dark-matter criteria (axion vs sterile neutrino), seesaw neutrino-mass drift and the redshift drift of a dark-matter decay line.
Reads analysis/toe_uv/{scorecard,line_drift,axion_de_route,class_fit_dovekie,class_fit_desy5}.json and the class_ppd_*_trunc.json files; writes data/w33_pass12626_scorecard_dm_criteria.json.
usage: py -3 analysis/w33_pass12626_scorecard_dm_criteria.py"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UV = os.path.join(ROOT, "analysis", "toe_uv")


def L(n):
    return json.load(open(os.path.join(UV, n), encoding="utf-8"))


sc, ld, ax = L("scorecard.json"), L("line_drift.json"), L("axion_de_route.json")
tr = {f"{ds}_{h}": L(f"class_ppd_{ds}_{h}_trunc.json")["rows"] for ds in ("dovekie", "desy5") for h in ("sn", "bao")}
src = open(os.path.join(UV, "class_ppd.py"), encoding="utf-8").read()
# seesaw drift since recombination: m_nu ~ 1/M ~ exp(+c' dphi)
nu = {}
for ds in ("dovekie", "desy5"):
    f = L(f"class_fit_{ds}.json")
    for m in ("free_neg", "free_pos"):
        i, cp = f[m]["info"], f[m]["p"]["cp"]
        nu[f"{ds}_{m}"] = math.exp(cp * (i["phi0"] - i["phi_rec"])) - 1
# sterile-neutrino route: Higgs-portal cap with a singlet vev v_S (same clock bound and 1 + w = 0.05 as Pass 12625)
b, mh = ax["b"], 125.25
phid = math.sqrt(3 * 0.05 * 0.69) * ax["H0_per_yr"]
amax = 5e-17 / phid
cap = {str(v): amax * mh ** 2 / (b * v ** 2) for v in (1e2, 1e3, 1e4, 1e11)}
gains = {ds: {m: sc[m][f"oos_gain_{ds}"] for m in ("fading_cneg", "CPL", "exp")} for ds in ("dovekie", "desy5")}
checks = dict(
    truncation_default_on='os.environ.get("TRUNC", "1")' in src,
    truncated_rows_record_rejections=all("rejected_outside_prior" in r for t in tr.values() for r in t.values()),
    evolving_spread_below_4_elpd=all(max(g.values()) - min(g.values()) < 4 for g in gains.values()),
    cpl_leads_desy5_by_more_than_2=gains["desy5"]["CPL"] - max(gains["desy5"]["fading_cneg"], gains["desy5"]["exp"]) > 2,
    every_evolving_model_beats_lcdm=all(v > 3 for g in gains.values() for v in g.values()),
    line_drift_sign_follows_c=all(ld[f"{d}_free_neg"]["rows"]["0.5"]["M_over_M0"] < 1 < ld[f"{d}_free_pos"]["rows"]["0.5"]["M_over_M0"] for d in ("dovekie", "desy5")),
    line_drift_at_z05_is_0p5_to_1p2_percent=all(0.005 < abs(ld[k]["rows"]["0.5"]["M_over_M0"] - 1) < 0.012 for k in ld),
    seesaw_nu_drift_since_recombination_below_6_percent=all(0 < v < 0.06 for v in nu.values()),
    sterile_route_portal_cap_natural_at_TeV=cap["1000.0"] > 1e-7,
    axion_scale_cap_hopeless=cap["100000000000.0"] < 1e-18,
)
out = dict(pass_number=12626, track="claude", scorecard=sc, oos_gains=gains, truncated_rows=tr, line_drift=ld, seesaw_nu_drift_since_rec=nu, portal_cap_vs_vS=cap, checks=checks, all_checks_pass=all(checks.values()))
json.dump(out, open(os.path.join(ROOT, "data", "w33_pass12626_scorecard_dm_criteria.json"), "w"), indent=1, default=float)
for k, v in checks.items():
    print(k, v)
print("portal cap vs v_S", {k: "%.1e" % v for k, v in cap.items()})
print("all_checks_pass", out["all_checks_pass"])
