"""Pass 12633 producer (claude track): the dark-energy field cannot be the level-3 flavour modulus (clock bound), fixed points included.
Reads analysis/toe_uv/flavour_modulus_clock.json; writes data/w33_pass12633_flavour_clock.json.
usage: py -3 analysis/w33_pass12633_flavour_clock.py"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
r = json.load(open(os.path.join(ROOT, "analysis", "toe_uv", "flavour_modulus_clock.json"), encoding="utf-8"))
s = {n: {float(k): v for k, v in d["h3"].items()} for n, d in r["scan"].items()}
checks = dict(
    forms_satisfy_weight4_identity=all(v < 1e-12 for v in r["constraint_check"].values()),
    omega_has_degenerate_pair=abs(r["values"]["omega"][0]) < 1e-9,
    omega_cone_no_suppression=s["omega"][1e-3] > 1.0 and abs(s["omega"][1e-3] / s["omega"][1e-2] - 1) < 0.1,
    i_sensitivity_grows_as_inverse_distance=8 < s["i"][1e-3] / s["i"][1e-2] < 12,
    generic_control_order_one=1.0 < s["generic"][1e-3] < 100,
    every_case_violates_clock_by_1e6=min(v for d in r["violation_factor_h3"].values() for v in d.values()) > 1e6,
)
out = dict(pass_number=12633, track="claude", kappa_mu_max=r["kappa_mu_max"], sensitivity_h3=s, min_violation_factor=min(v for d in r["violation_factor_h3"].values() for v in d.values()), checks=checks, all_checks_pass=all(checks.values()))
json.dump(out, open(os.path.join(ROOT, "data", "w33_pass12633_flavour_clock.json"), "w"), indent=1)
for k, v in checks.items():
    print(k, v)
print("all_checks_pass", out["all_checks_pass"])
