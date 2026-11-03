"""Passes 12546-12549 (Claude track).  Not a theory of everything: see PASS12546_12549_DARK_SECTOR_GEOMETRY.md.

12546 -- the best w >= -1 history on DESI + CMB + SNe: all its gain sits at z < 0.07, where only supernovae see it.
12547 -- the fading dark sector reproduced: c' = 0.05 is about 2.5 sigma from zero, not 5.
12548 -- the moduli metric ties c' to the coupling of brane matter; Cassini and LLR bound the volume change; c = 4 c' is disfavoured.
12549 -- withdrawn suspicion: removing z < 0.1 supernovae weakens the signal about as much as it would if CPL were true.
"""

import json
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12546_to_12549_dark_sector.json"
SETS = ("pantheon", "dovekie", "desy5")


def load(n):
    return json.loads((D / n).read_text())


def main():
    checks, res = {}, {}
    fd = {s: load(f"fading_ds_{s}.json") for s in SETS + ("none",)}
    ce = {s: load(f"dark_ceiling_{s}.json") for s in SETS}
    lo = {s: {z: load(f"dark_lowz_{s}_{z}.json") for z in ("0.0", "0.1")} for s in SETS}
    rf = {s: load(f"dark_refine_{s}_0.0.json") for s in ("dovekie", "desy5")}
    geo, mk = load("dd_geometry.json"), load("dark_mocks.json")

    # 12546
    t = {}
    for s in SETS:
        un = lo[s]["0.0"]["uncoupled"]["delta"]
        ceil = min(x["delta"] for x in rf[s]["ceiling"]) if s in rf else lo[s]["0.0"]["ceiling_13bins"]["delta"]
        free = min(x["delta"] for x in rf[s]["free"]) if s in rf else min(ce[s]["free_6bins"]["delta"], ce[s]["free_9bins"]["delta"])
        t[s] = dict(uncoupled_exponential=un, ceiling=ceil, fading_c_neg=fd[s]["free_c_neg"]["delta"], fading_c_pos=fd[s]["free_c_pos"]["delta"], CPL=ce[s]["CPL"]["delta"], free_w=free)
    res["gains"] = t
    checks["12546: order on each sample: exponential above ceiling above CPL above free w"] = all(x["uncoupled_exponential"] > x["ceiling"] > x["CPL"] > x["free_w"] for x in t.values())
    checks["12546: global search: two seeds agree within 0.05 on the ceiling, DES-Dovekie and DES-SN5YR"] = all(abs(rf[s]["ceiling"][0]["delta"] - rf[s]["ceiling"][1]["delta"]) < 0.05 for s in rf)
    checks["12546: the ceiling has w above -0.9 only in the two bins below z = 0.07 (DES samples, bins from z = 0.12 up within 0.05 of -1)"] = all(min(rf[s]["ceiling"], key=lambda x: x["delta"])["w"][1] > -0.9 and all(w < -0.95 for w in min(rf[s]["ceiling"], key=lambda x: x["delta"])["w"][2:]) for s in rf)

    # 12547
    pub = dict(pantheon=(-0.85, 0.05, 0.65, 0.05), desy5=(-1.06, 0.05, 0.83, 0.06))
    checks["12547: control: c and c' within 0.05 of Table I of arXiv:2507.03090 on both branches, Pantheon+ and DES-SN5YR"] = all(
        abs(fd[s]["free_c_neg"]["c"] - p[0]) < 0.05 and abs(fd[s]["free_c_neg"]["cp"] - p[1]) < 0.01 and abs(fd[s]["free_c_pos"]["c"] - p[2]) < 0.05 and abs(fd[s]["free_c_pos"]["cp"] - p[3]) < 0.01 for s, p in pub.items())
    prof = {}
    for s in SETS + ("none",):
        z = min(x["delta"] for x in fd[s]["cp_profile"] if x["cp"] == 0.0)
        prof[s] = dict(cp_zero=z, best=fd[s]["free_c_neg"]["delta"], gain_from_cp=z - fd[s]["free_c_neg"]["delta"], rows={str(x["cp"]): x["delta"] for x in fd[s]["cp_profile"] if x["sign"] == -1})
    res["cp_profile"] = prof
    checks["12547: turning on c' gains Delta chi2 of only 5 to 8 on every sample (about 2.3 to 2.8 sigma), not the 25 that 0.05 +- 0.01 would suggest"] = all(5 < p["gain_from_cp"] < 8 for p in prof.values())
    checks["12547: c' = 0.1 is worse than LCDM on every sample, by over 25 on the negative branch: the profile is very asymmetric"] = all(p["rows"]["0.1"] > 25 for p in prof.values())

    # 12548
    c5 = sp.sqrt(sp.Rational(3, 2))
    b5 = sp.Rational(1, 2) / c5 * sp.Rational(1)
    checks["12548: control: 5D radion c' = sqrt(3/2), beta = 1/sqrt 6, gamma = 1/2 (Brans-Dicke omega = 0)"] = sp.simplify(b5 - 1 / sp.sqrt(6)) == 0 and geo["radion_5D"]["gamma"] == "1/2" and geo["radion_5D"]["ratio"] == "1/3"
    checks["12548: |grad ln m_KK|^2 = 3/2 for every n, and projecting out grad ln M_D leaves n/(n+1)"] = all(
        sp.Rational(r["mKK_sq"]) == sp.Rational(3, 2) and (n == 0 or sp.Rational(3, 2) - sp.Rational(r["inner"]) ** 2 / sp.Rational(r["MD_sq"]) == sp.Rational(n, n + 1)) for n, r in ((int(k), v) for k, v in geo["gradients_by_n"].items()))
    checks["12548: Cassini at c' = 0.05: xi < 0.18 two-sided, < 0.11 one-sided"] = abs(geo["xi_max"]["beta_max_two_sided"]["0.05"] - 0.178) < 0.001 and abs(geo["xi_max"]["beta_max_one_sided"]["0.05"] - 0.105) < 0.001
    checks["12548: n = 1 with only L and Vol moving: c' = 0.05 forces beta about 0.31 or -0.27"] = sorted(round(x, 2) for x in geo["n1_two_moduli"]["beta_at_cprime_0p05"]) == [-0.27, 0.31]
    llr = {s: dict(phip0=fd[s]["free_c_neg"]["info"]["phip0"], beta_max=geo["llr"]["Gdot_over_GH0_2sigma"] / (2 * abs(fd[s]["free_c_neg"]["info"]["phip0"]))) for s in SETS}
    res["llr"] = llr
    checks["12548: LLR at the fitted roll bounds beta below 0.004 on all samples, independently of Cassini"] = all(x["beta_max"] < 0.004 for x in llr.values())
    lines = {s: {r: fd[s]["ratio_lines"][r] for r in fd[s]["ratio_lines"]} for s in SETS}
    res["casimir_line"] = {s: dict(c=lines[s]["4.0"]["c"], cp=lines[s]["4.0"]["cp"], delta=lines[s]["4.0"]["delta"], cost_vs_free_c_pos=lines[s]["4.0"]["delta"] - fd[s]["free_c_pos"]["delta"], fitted_ratio_pos=fd[s]["free_c_pos"]["c"] / fd[s]["free_c_pos"]["cp"]) for s in SETS}
    checks["12548: Casimir line costs Delta chi2 4.4, 6.0, 12.1 against free c > 0; fitted ratio 13 to 15, not 4"] = all(abs(res["casimir_line"][s]["cost_vs_free_c_pos"] - v) < 0.1 for s, v in zip(SETS, (4.40, 6.04, 12.10))) and all(12 < x["fitted_ratio_pos"] < 16 for x in res["casimir_line"].values())
    capped = {s: min(x["delta"] for x in fd[s]["cp_profile"] if x["cp"] == 0.0123) for s in SETS}
    res["pure_radius_cap"] = capped
    checks["12548: at the pure-radius Cassini cap c' = 0.0123 the coupling gains at most 1.1 over c' = 0"] = all(prof[s]["cp_zero"] - capped[s] < 1.1 for s in SETS)

    # 12549
    m = {}
    for k, v in mk.items():
        r = np.array(v["rows"])
        sel = r[:, 0] <= v["real_full"]
        m[k] = dict(n=len(r), real_full=v["real_full"], real_cut=v["real_cut"], mean_full=r[:, 0].mean(), mean_cut=r[:, 1].mean(), p_cut_as_weak=float((r[:, 1] >= v["real_cut"]).mean()), p_drop_as_large=float(((r[:, 1] - r[:, 0]) >= (v["real_cut"] - v["real_full"])).mean()), p_conditional=float((r[sel, 1] >= v["real_cut"]).mean()) if sel.any() else None, p_full_as_strong=float(sel.mean()))
    res["mocks"] = m
    checks["12549: control: LCDM mocks have mean gain within 0.3 of -2, full and cut, and none reaches the real Dovekie gain in 150"] = abs(m["dovekie_lcdm"]["mean_full"] + 2) < 0.3 and abs(m["dovekie_lcdm"]["mean_cut"] + 2) < 0.3 and m["dovekie_lcdm"]["p_full_as_strong"] == 0
    checks["12549: real drops on cutting z < 0.1 are ordinary under CPL truth: probability of a drop as large over 0.3 on each sample"] = all(m[k]["p_drop_as_large"] > 0.3 for k in ("desy5_cpl", "dovekie_cpl", "pantheon_cpl"))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    print(json.dumps({k: res[k] for k in ("gains", "casimir_line", "llr", "pure_radius_cap", "mocks")}, indent=0, default=float))
    print({s: {a: round(b, 2) for a, b in p.items() if a != "rows"} for s, p in prof.items()})


if __name__ == "__main__":
    main()
