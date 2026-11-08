"""Pass 12629 producer (claude track): sign of the fading coupling by profile likelihood; the monodromy-law CLASS patch and its control; what natural completions cost (KLT epsilon, cyclic partners).
Reads analysis/toe_uv/{c_profile,mono_control,klt_check,modes_laplace}.json; writes data/w33_pass12629_sign_naturalness.json.
usage: py -3 analysis/w33_pass12629_sign_naturalness.py"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UV = os.path.join(ROOT, "analysis", "toe_uv")


def L(n):
    return json.load(open(os.path.join(UV, n), encoding="utf-8"))


cp, mc, kl, ml = L("c_profile.json"), L("mono_control.json"), L("klt_check.json"), L("modes_laplace.json")
rows = {k: v for k, v in cp.items() if k != "summary"}
ch = {round(v["c"], 2): v["chi2"] for v in rows.values()}
s = cp["summary"]
k100 = [r for r in kl if r["k"] == 4.0 and r["sigma_over_m0"] == 0.01 and r["m0_eV"] == 1e2][0]
checks = dict(
    mono_patch_reproduces_fading_at_Fi0=abs(mc["mono_Fi0"]["chi2"] - mc["fading"]["chi2"]) < 1e-3,
    minimal_running_costs_at_fixed_params=mc["mono_Fi0.01"]["chi2"] - mc["fading"]["chi2"] > 2,
    profile_prefers_cneg_mildly=0 < s["chi2_min_pos"] - s["chi2_min_neg"] < 4,
    profile_P_cpos_between_0p15_and_0p4=0.15 < s["P_c_positive_pchip"] < 0.4,
    profile_agrees_with_laplace=abs(s["P_c_positive_pchip"] - ml["dovekie_full"]["P_c_positive"]) < 0.1,
    modes_separated_by_barrier=min(ch[-0.2], ch[0.2]) - s["chi2_min_neg"] > 4,
    large_c_excluded=ch[-2.0] - s["chi2_min_neg"] > 100 and ch[1.4] - s["chi2_min_neg"] > 50,
    klt_needs_eps_below_their_perturbative_bound=k100["eps"] < 1e-12,
    klt_needs_many_ZN_copies=k100["N_z05"] > 40,
)
out = dict(pass_number=12629, track="claude", profile=dict(chi2_by_c=ch, summary=s), mono_control=mc, klt_100eV=k100, checks=checks, all_checks_pass=all(checks.values()))
json.dump(out, open(os.path.join(ROOT, "data", "w33_pass12629_sign_naturalness.json"), "w"), indent=1, default=float)
for k, v in checks.items():
    print(k, v)
print("all_checks_pass", out["all_checks_pass"])
