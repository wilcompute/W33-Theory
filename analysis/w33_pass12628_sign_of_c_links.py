"""Pass 12628 producer (claude track): the sign of the fading coupling ties phantom crossing, line drift and shear; minimal sterile-neutrino coupled DM window; Chat's Z9 sector fails as coupled DM; frozen statements.
Reads analysis/toe_uv/{weff_turnaround,sterile_window,line_drift,sign_des,prereg_statements}.json; writes data/w33_pass12628_sign_of_c_links.json.
usage: py -3 analysis/w33_pass12628_sign_of_c_links.py"""
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UV = os.path.join(ROOT, "analysis", "toe_uv")


def L(n):
    return json.load(open(os.path.join(UV, n), encoding="utf-8"))


wt, sw, ld, sd = L("weff_turnaround.json"), L("sterile_window.json"), L("line_drift.json"), L("sign_des.json")
sha = open(os.path.join(UV, "prereg_statements.sha256")).read().split()[0]
sha_now = hashlib.sha256(open(os.path.join(UV, "prereg_statements.json"), "rb").read().replace(b"\r\n", b"\n")).hexdigest()
rows = sw["rows"]
checks = dict(
    cneg_crosses_minus1_near_z08=all(len(wt[f"{d}_free_neg"]["crossings_of_minus1"]) == 1 and 0.6 < wt[f"{d}_free_neg"]["crossings_of_minus1"][0] < 1.0 for d in ("dovekie", "desy5")),
    cpos_never_phantom=all(not wt[f"{d}_free_pos"]["crossings_of_minus1"] and max(wt[f"{d}_free_pos"]["w_eff"].values()) < -0.8 and min(wt[f"{d}_free_pos"]["w_eff"].values()) > -1 for d in ("dovekie", "desy5")),
    cneg_field_turns_around=all(wt[f"{d}_free_neg"]["turnaround_z"] for d in ("dovekie", "desy5")),
    cpos_no_turnaround=all(not wt[f"{d}_free_pos"]["turnaround_z"] for d in ("dovekie", "desy5")),
    control_cpl_crosses=all(wt[f"{d}_CPL"]["crossings_of_minus1"] for d in ("dovekie", "desy5")),
    line_drift_sign_matches_phantom=all((ld[f"{d}_free_neg"]["rows"]["0.5"]["M_over_M0"] < 1) and (ld[f"{d}_free_pos"]["rows"]["0.5"]["M_over_M0"] > 1) for d in ("dovekie", "desy5")),
    sterile_window_at_7keV_all_mS=all(r["window"] for r in rows if r["M_keV"] == 7.1),
    sterile_window_closed_at_30keV=not any(r["window"] for r in rows if r["M_keV"] == 30.0),
    chat_gauged_needs_gX_below_1e11=all(r["chat_gX_max_no_thermalise"] < 1e-11 for r in rows),
    shear_prefers_fading_over_cpl=(sd["CPL"]["des"] + sd["CPL"]["desp"]) - (sd["free_neg"]["des"] + sd["free_neg"]["desp"]) > 2,
    prereg_hash_intact=sha == sha_now,
)
out = dict(pass_number=12628, track="claude", weff=wt, sterile_window=rows, prereg_sha256=sha, checks=checks, all_checks_pass=all(checks.values()))
json.dump(out, open(os.path.join(ROOT, "data", "w33_pass12628_sign_of_c_links.json"), "w"), indent=1, default=float)
for k, v in checks.items():
    print(k, v)
print("all_checks_pass", out["all_checks_pass"])
