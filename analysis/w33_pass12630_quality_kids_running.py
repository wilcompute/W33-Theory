"""Pass 12630 producer (claude track): Z_N size for periodic fading couplings (quality vs loops vs monotonic history); qutrit symplectic element orders; monodromy refits scoring S6; KiDS-Legacy fixed-background shear replication with a DES control.
Reads analysis/toe_uv/{quality_N,sp_orders,sp_orders_4_5,mono_fit,sign_des,sign_des_kids}.json; writes data/w33_pass12630_quality_kids_running.json.
usage: py -3 analysis/w33_pass12630_quality_kids_running.py"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UV = os.path.join(ROOT, "analysis", "toe_uv")


def L(n):
    return json.load(open(os.path.join(UV, n), encoding="utf-8"))


q, s23, s45, mf, sd, sk = (L(n) for n in ("quality_N.json", "sp_orders.json", "sp_orders_4_5.json", "mono_fit.json", "sign_des.json", "sign_des_kids.json"))
rowq = {r["f_over_MP"]: r for r in q["rows"]}
tot = lambda d, m: d[m]["des"] + d[m]["desp"]  # noqa: E731
kid = {m: tot(sk, m) - tot(sk, "LCDM") for m in sk}
des = {m: tot(sd, m) - tot(sd, "LCDM") for m in sd}
checks = dict(
    quality_binds_not_loops=all(r["N_quality"] > 3 * r["N_loop"] for r in q["rows"] if r["f_over_MP"] >= 0.01),
    monotonic_floor_needs_N_above_90=rowq[0.08]["N_quality"] > 90 and rowq[0.27]["N_quality"] > 160,
    sp43_max_18_control=s23["Sp(4,3)"]["max_found"] == 18,
    sp63_reaches_21_not_96=s23["Sp(6,3)"]["max_found"] >= 21 and s23["Sp(6,3)"]["max_found"] < 96,
    sp83_below_96=s45["Sp(8,3)"]["max_found"] < 96,
    sp103_above_167=s45["Sp(10,3)"]["max_found"] > 167,
    running_free_after_refit=max(v["chi2"] for v in mf.values()) - mf["Fi0"]["chi2"] < 1.0,
    S6_not_falsified=all(v["chi2"] - mf["Fi0"]["chi2"] < 4 for v in mf.values()),
    kids_penalises_cpl_most=kid["CPL"] > max(kid["free_neg"], kid["free_pos"]) + 3,
    kids_replicates_des_ordering=sorted(kid, key=kid.get) == sorted(des, key=des.get),
)
out = dict(pass_number=12630, track="claude", quality=q, orders=dict(two_three=s23, four_five=s45), mono_fit=mf, shear_fixed_bg_rel_lcdm=dict(des=des, kids=kid), checks=checks, all_checks_pass=all(checks.values()))
json.dump(out, open(os.path.join(ROOT, "data", "w33_pass12630_quality_kids_running.json"), "w"), indent=1, default=float)
for k, v in checks.items():
    print(k, v)
print("KiDS rel LCDM", {k: round(v, 2) for k, v in kid.items()}, "DES", {k: round(v, 2) for k, v in des.items()})
print("all_checks_pass", out["all_checks_pass"])
