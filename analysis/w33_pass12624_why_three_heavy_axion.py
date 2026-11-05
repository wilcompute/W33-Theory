"""Pass 12624 producer (claude track): why three copies, heavy brane-instanton axion, joint n_s/r/w/c' target, cross-check of Chat's Z9 kinetic matrix.
Reads analysis/toe_uv/items_234.json, items_more.json, class_fit_dovekie.json (written by items_234.py and items_more.py in analysis/toe_uv) and writes data/w33_pass12624_why_three_heavy_axion.json.
usage: py -3 analysis/w33_pass12624_why_three_heavy_axion.py"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UV = os.path.join(ROOT, "analysis", "toe_uv")


def load(n):
    return json.load(open(os.path.join(UV, n), encoding="utf-8"))


a = load("items_234.json")
m = load("items_more.json")
fit = load("class_fit_dovekie.json")
cp = m["copies"]


def tau(MU, ia):
    return 1.6e36 * (MU / 1e16) ** 4 * (35 / ia) ** 2


q = {int(k): v for k, v in cp["quark_33b1"].items()}
MUs = [q[n]["MU"] for n in range(2, 6)]
# n_s along the fading profile -> c' band for an inflation prior n_s in [0.965, 0.968]
prof = [(float(k.split("_")[-1]), (fit[k].get("p") or fit[k])["ns"]) for k in fit if k.startswith("prof_neg_")]
prof.sort()


def cp_at(ns):
    for (c0, n0), (c1, n1) in zip(prof, prof[1:]):
        if (n0 - ns) * (n1 - ns) <= 0:
            return c0 + (c1 - c0) * (n0 - ns) / (n0 - n1)
    return None


band = [cp_at(0.968), cp_at(0.965)]
cpl = fit["CPL"].get("p") or fit["CPL"]
ha = a["heavy_axion"]
checks = dict(
    control_full_27_never_unifies=all(v is None for v in cp["full_27"].values()),
    quark_piece_one_copy_fails=q[1] is None,
    quark_piece_unifies_for_2_to_5=all(q[n] is not None for n in range(2, 6)),
    quark_piece_MU_nearly_n_independent=(max(MUs) - min(MUs)) / min(MUs) < 0.06,
    quark_piece_MX_rises_with_n=all(q[n]["MX"] < q[n + 1]["MX"] for n in range(2, 5)),
    quark_piece_proton_safe_all_n=all(tau(q[n]["MU"], q[n]["inv_alpha_U"]) > 1e37 for n in range(2, 6)),
    antiquark_piece_never_unifies=all(v is None for v in cp["antiquark_3b13"].values()),
    lepton_piece_MU_too_low_for_proton=all(v is None or v["MU"] < 1e13 for v in cp["lepton_133b"].values()),
    chat_kinetic_matrix_reproduced=m["chat_cross_check"]["agrees"],
    brane_dominates_below_alpha_inv_12_to_18=12 < ha["alpha_b_inv_brane_dominates_below"] < 18,
    misaligned_safe_above_alpha_inv_16_to_22=16 < ha["alpha_b_inv_safe_above"] < 22,
    heavy_axion_bbn_safe_only_alpha_inv_le_3=all(r["bbn_safe"] == (r["alpha_b_inv"] <= 3) for r in m["heavy_axion_lifetime"]),
    cprime_band_from_inflation_prior=band[0] is not None and band[1] is not None and 0.03 < band[0] < band[1] < 0.07,
    cprime_band_contains_fading_best_fit=band[0] <= (fit["free_neg"].get("p") or fit["free_neg"])["cp"] <= band[1],
    lcdm_ns_outside_inflation_band=(fit["LCDM"].get("p") or fit["LCDM"])["ns"] > 0.968,
)
out = dict(
    pass_number=12624,
    track="claude",
    copies=cp,
    proton_tau_quark_piece={n: tau(q[n]["MU"], q[n]["inv_alpha_U"]) for n in range(2, 6)},
    heavy_axion=ha,
    heavy_axion_lifetime=m["heavy_axion_lifetime"],
    chat_cross_check=m["chat_cross_check"],
    joint_target=dict(n_s_inflation_prior=[0.965, 0.968], r_SMASH_from_memory=0.004, cprime_band=band, cprime_fading_best=(fit["free_neg"].get("p") or fit["free_neg"])["cp"], CPL_w0=cpl["w0"], CPL_wa=cpl["wa"], ns_profile=prof),
    checks=checks,
    all_checks_pass=all(checks.values()),
)
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_pass12624_why_three_heavy_axion.json"), "w"), indent=1, default=float)
for k, v in checks.items():
    print(k, v)
print("c' band", band, "all_checks_pass", out["all_checks_pass"])
