"""Passes 12558-12559 (Claude track).  Not a theory of everything: see PASS12558_12559_SPARSE_TOWER.md.

12558 -- full Planck on all samples: c' stays at 2.3 to 2.9 sigma; the Casimir tension comes from supernovae, not from DESI + CMB; the phi -> -phi symmetry at c' = 0 measures fit scatter.
12559 -- joining the drag (b5b4db003) to the one-particle loop benchmark (aae4f41f5): the regulated tower has no m_n^4, and its natural modulus mass is the Hubble mass the drag excludes; a sparse tower passes both, confirmed with two fluids on full Planck.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12558_to_12559_sparse_tower.json"
SETS = ("pantheon", "dovekie", "desy5", "none")
PUB = dict(pantheon=((-0.85, 0.05), (0.65, 0.05)), dovekie=((-0.92, 0.05), (0.69, 0.05)), desy5=((-1.06, 0.05), (0.83, 0.06)), none=((-1.03, 0.05), (0.42, 0.05)))


def load(n):
    return json.loads((D / n).read_text())


def main():
    checks, res = {}, {}

    # 12558
    fit = {s: load(f"class_fit_{s}.json") for s in SETS}
    lens = {s: load(f"class_lens_{s}.json") for s in SETS}
    tab = {}
    for s, f in fit.items():
        L = f["LCDM"]["chi2"]
        ex = min(f["exp_neg"]["chi2"], f["exp_pos"]["chi2"], L)
        ll = lens[s]
        lex = min(ll["exp_neg"]["chi2_lens"], ll["exp_pos"]["chi2_lens"], ll["LCDM"]["chi2_lens"])
        tab[s] = dict(
            exp_scatter=abs(f["exp_neg"]["chi2"] - f["exp_pos"]["chi2"]),
            exp_vs_lcdm=ex - L,
            free_neg=f["free_neg"]["chi2"] - L,
            free_pos=f["free_pos"]["chi2"] - L,
            c_neg=f["free_neg"]["p"]["c"],
            cp_neg=f["free_neg"]["p"]["cp"],
            c_pos=f["free_pos"]["p"]["c"],
            cp_pos=f["free_pos"]["p"]["cp"],
            gain_cp=ex - f["free_neg"]["chi2"],
            gain_cp_with_lens=ex - f["free_neg"]["chi2"] + lex - ll["free_neg"]["chi2_lens"],
            casimir_cost=f["casimir"]["chi2"] - f["free_pos"]["chi2"],
            casimir=f["casimir"]["chi2"] - L,
            cpl_vs_native=f["CPL"]["chi2"] - f["LCDM_native"]["chi2"],
            w0=f["CPL"]["p"]["w0"],
            wa=f["CPL"]["p"]["wa"],
            S8_lcdm=f["LCDM"]["info"]["S8"],
            S8_free=f["free_neg"]["info"]["S8"],
            lens_lcdm=ll["LCDM"]["chi2_lens"],
            lens_free=ll["free_neg"]["chi2_lens"],
        )
    res["table"] = tab
    checks["12558: every sample: both branches within 0.1 in c and 0.01 in c' of Table I of arXiv:2507.03090"] = all(abs(tab[s]["c_neg"] - PUB[s][0][0]) < 0.1 and abs(tab[s]["cp_neg"] - PUB[s][0][1]) < 0.01 and abs(tab[s]["cp_pos"] - PUB[s][1][1]) < 0.01 and abs(tab[s]["c_pos"] - PUB[s][1][0]) < 0.1 for s in SETS)
    checks["12558: phi -> -phi at c' = 0 makes the two exponential fits equal, so their difference measures fit scatter: at most 1.8, and the better branch is the reference"] = max(t["exp_scatter"] for t in tab.values()) < 1.9
    checks["12558: the c' gain is 5 to 9 on all samples (2.3 to 2.9 sigma), and 6.5 to 8.8 with lensing added post hoc, which replaces the 9.7 quoted in Pass 12551 as the top of the range"] = all(5 < t["gain_cp"] < 9 and 6.5 < t["gain_cp_with_lens"] < 8.8 for t in tab.values())
    checks["12558: Casimir cost rises with the supernova sample: under 0.1 on DESI + CMB, 3.5, 5.4, 10.9 with Pantheon+, Dovekie, DES-SN5YR"] = tab["none"]["casimir_cost"] < 0.1 and abs(tab["pantheon"]["casimir_cost"] - 3.47) < 0.05 and abs(tab["dovekie"]["casimir_cost"] - 5.38) < 0.05 and abs(tab["desy5"]["casimir_cost"] - 10.9) < 0.05
    checks["12558: c' raises S8 by 0.024 to 0.032 at the best fit, the direction weak lensing can test"] = all(0.024 < t["S8_free"] - t["S8_lcdm"] < 0.032 for t in tab.values())

    # 12559 loops
    tl = load("dd_tower_loops.json")
    res["tower_loops"] = tl
    checks["12559: Casimir direct sum equals -3 zeta(5)/(4 pi^2 l^4) within 1e-12; the l^-4 scaling is 16"] = all(abs(v["numeric"] / v["exact"] - 1) < 1e-12 for v in tl["casimir"].values()) and abs(tl["casimir_scaling_ratio_l1_over_l2"] - 16) < 1e-9
    u = tl["unsubtracted_grows_as_cutoff_falls"]
    checks["12559: control: without the bulk subtraction the integral grows without limit as the cutoff falls, by over 5 at each halving"] = abs(u["0.01"]) > 5 * abs(u["0.02"]) and abs(u["0.005"]) > 5 * abs(u["0.01"])
    checks["12559: control: the one-particle cap of aae4f41f5 reproduced to 1e-10"] = all(abs(tl["control_parallel_cap_eV"][k] / tl["parallel_track_cap_eV"][k] - 1) < 1e-10 for k in tl["parallel_track_cap_eV"])
    t = tl["tower_natural_mass"]
    checks["12559: natural tower modulus mass is at most 4.1 to 7.0 H0; to reach 1e5 H0 falls short by 1.4e4 to 2.5e4 in mass"] = all(4 < v["mu_max_over_H0"] < 7.1 and 1.4e4 < v["shortfall_mass_to_1e5"] < 2.5e4 for v in t.values())

    # 12559 sparse tower on Planck
    fr = {s: load(f"class_fraction_{s}.json") for s in ("dovekie", "desy5")}
    res["fraction"] = {s: {k: dict(delta=v.get("delta"), f=v.get("f"), b=v.get("b"), c=v.get("p", {}).get("c"), S8=v.get("info", {}).get("S8"), failed=v.get("failed")) for k, v in d.items() if isinstance(v, dict) and "f" in v} for s, d in fr.items()}
    res["fraction_growth"] = {s: d.get("growth") for s, d in fr.items()}
    for s, d in fr.items():
        res["fraction"][s]["single_delta"] = d["single"] - d["LCDM"]
    do = res["fraction"]["dovekie"]
    de = res["fraction"]["desy5"]
    checks["12559: control: f = 1 through the two-fluid route returns the direct single-field fit within 0.1"] = abs(do["f1_b005_control"]["delta"] - do["single_delta"]) < 0.1 and abs(de["f1_b005_control"]["delta"] - de["single_delta"]) < 0.1
    checks["12559: sparse tower with two fluids on full Planck, f b = 0.05: loses at most 0.6 at b = 1/sqrt 2 and at most 1.3 at b = sqrt(3/2) against the single-field fit, on both samples"] = all(abs(x["b707_product005"]["delta"] - x["single_delta"]) < 0.6 and abs(x["b1225_product005"]["delta"] - x["single_delta"]) < 1.3 for x in (do, de))
    checks["12559: f = 0.3 at b = 1/sqrt 2 is rejected: worse than LCDM by over 100"] = do["b707_f03"]["delta"] > 100 and de["b707_f03"]["delta"] > 100
    checks["12559: the product is what the data fix: f b = 0.03 and 0.07 are both worse than 0.05"] = all(x["b707_product003"]["delta"] > x["b707_product005"]["delta"] and x["b707_product007"]["delta"] > x["b707_product005"]["delta"] for x in (do, de))
    gr = res["fraction_growth"]
    checks["12559: the two fluids separate: delta_coupled/delta_uncoupled at k = 0.2/Mpc exceeds 1.03 today and at a = 0.02; the lead shrinks by today, the opposite of what I first asserted"] = all(g["ratio_today"] > 1.03 and g["ratio_a002"] > 1.03 and g["ratio_today"] < g["ratio_a002"] for g in gr.values())

    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    print(json.dumps(tab, indent=0, default=float))
    print(json.dumps(res["fraction"], indent=0, default=float))
    print(res["fraction_growth"])


if __name__ == "__main__":
    main()
