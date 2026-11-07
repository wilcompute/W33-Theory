"""Pass 12627 producer (claude track): MCMC held-BAO posterior of fading on DES-SN5YR, joint CPL + DES Y3 refit, shear-held posterior predictive, and the radiative cap (after Chat's audit 3869fe29c).
Reads analysis/toe_uv/{mcmc_desy5_bao_free_neg,des_joint_cpl,class_des_dovekie_joint,shear_ppd,class_ppd_desy5_bao}.json; writes data/w33_pass12627_mcmc_shear_radiative.json.
usage: py -3 analysis/w33_pass12627_mcmc_shear_radiative.py"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UV = os.path.join(ROOT, "analysis", "toe_uv")


def L(n):
    return json.load(open(os.path.join(UV, n), encoding="utf-8"))


mc, cj, dj, sp = L("mcmc_desy5_bao_free_neg.json"), L("des_joint_cpl.json"), L("class_des_dovekie_joint.json")["rows"], L("shear_ppd.json")
lcdm_bao = L("class_ppd_desy5_bao.json")["rows"]["LCDM_infl1"]["elpd"]
sh = lambda r: r["parts"]["des"] + r["parts"]["desp"]  # noqa: E731
H0, MP, b = 1.4466703e-33, 2.435e27, 0.053
mcap = (4 * math.pi ** 2 * H0 ** 2 * MP ** 2 / b ** 2) ** 0.25
curv16 = (16e3 / mcap) ** 4  # in units of H0^2 at mu = m (one Majorana)
checks = dict(
    mcmc_fading_beats_lcdm_on_held_bao=mc["elpd_held"] > lcdm_bao,
    mcmc_autocorrelation_short=max(mc["tau_int"]) < (mc["nstep"] - mc["burn"]) / 4,
    mcmc_cprime_consistent_with_zero_without_bao=mc["mean"]["cp"] / mc["sd"]["cp"] < 2,
    joint_shear_penalty_on_cpl_survives_refit=sh(cj) - sh(dj["free_neg"]) > 2,
    joint_totals_fading_lt_cpl_lt_lcdm=dj["free_neg"]["chi2"] < cj["chi2"] < dj["LCDM"]["chi2"],
    shear_ppd_cpl_worst=sp["CPL"]["elpd_shear"] < min(sp[m]["elpd_shear"] for m in ("LCDM", "free_neg", "free_pos")),
    shear_ppd_fading_beats_cpl_by_1=sp["free_neg"]["elpd_shear"] - sp["CPL"]["elpd_shear"] > 1,
    shear_ppd_lcdm_within_0p5_of_best=max(sp[m]["elpd_shear"] for m in sp) - sp["LCDM"]["elpd_shear"] < 0.5,
    radiative_cap_below_0p05_eV=mcap < 0.05,
    radiative_curvature_matches_chat_audit=abs(curv16 / 3.758e23 - 1) < 0.05,
)
out = dict(pass_number=12627, track="claude", mcmc=mc, lcdm_bao_elpd=lcdm_bao, joint_cpl=dict(chi2=cj["chi2"], parts=cj["parts"], w0=cj["p"]["w0"], wa=cj["p"]["wa"]), joint_rows={k: v["chi2"] for k, v in dj.items()}, shear_ppd=sp, radiative_mass_cap_eV=mcap, curvature_16keV_over_H0sq=curv16, checks=checks, all_checks_pass=all(checks.values()))
json.dump(out, open(os.path.join(ROOT, "data", "w33_pass12627_mcmc_shear_radiative.json"), "w"), indent=1, default=float)
for k, v in checks.items():
    print(k, v)
print("radiative cap %.4f eV; 16 keV curvature %.3e H0^2" % (mcap, curv16))
print("all_checks_pass", out["all_checks_pass"])
