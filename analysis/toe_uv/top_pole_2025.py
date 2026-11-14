"""Pass 12666: add the published ATLAS top-quark POLE mass (JHEP 12 (2025) 023, arXiv:2507.02632, ttbar + 1 jet, 2->3 calculation):
m_t^pole = 170.7 +- 0.3 (stat) +- 1.4 (syst) +- 0.3 (scale) +- 0.2 (PDF+alpha_s) GeV, to the comparison of nnlo_top.py (Pass 12537),
which found that lambda(M_Pl) = 0 (Buttazzo et al. eq. 61, three-loop running) needs M_t = 171.04 +- 0.37 GeV.
The vacuum-stability fit uses the pole mass, so a pole-mass measurement is the like-for-like comparison.
usage: py -3 analysis/toe_uv/top_pole_2025.py"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
g = {"__name__": "x", "__file__": os.path.join(HERE, "nnlo_top.py")}
src = open(os.path.join(HERE, "nnlo_top.py"), encoding="utf-8").read()
exec(src[: src.index("meas = dict(")], g)
mt0 = g["mt0"]; tot = g["tot"]
atlas = (170.7, math.sqrt(0.3 ** 2 + 1.4 ** 2 + 0.3 ** 2 + 0.2 ** 2))
rows = {"direct_run1_combination (MC mass, PDG 2026 still cites it)": (172.52, 0.33),
        "preliminary pole combination (Nov 2025 talk; Pass 12537)": (172.25, 0.95),
        "ATLAS pole mass, ttbar+1 jet, JHEP 12 (2025) 023": atlas}
out = dict(Mt_for_lambda_MPl_zero=mt0, error=tot, comparisons={k: dict(value=v, sigma=s, pull=(v - mt0) / math.hypot(s, tot)) for k, (v, s) in rows.items()})
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(HERE, "top_pole_2025.json"), "w"), indent=1)
