"""Kill test for the apparent no-fit hit M_t = 172.7 GeV of SM + 3 nu_R + axion + DM in matter_scan.py.  (1) The same SM matter in the four published schemes of arXiv:1311.2898 Table 3.  (2) dM_t/dLambda and dM_t/dG near the hit.  (3) The fraction of the published scheme-spread region that gives M_t within 1 GeV of data: the look-elsewhere estimate.  (4) The band in the (G*, Lambda*) plane that gives M_t = 172.57 +- 1.  Gaussian hypercharge throughout.
usage: py -3 scheme_test.py"""
import json
import numpy as np

src = open("matter_scan.py", encoding="utf-8").read().split("models = dict(SM=")[0]
exec(src)
gauss = lambda G_, L: predict(G_, L, "gaussian")
out = {}
schemes = {"1L-II": (1.762, -2.399), "full-II": (1.735, -2.348), "1L-Ia": (2.627, -3.591), "full-Ia": (2.580, -3.504)}
out["SM_matter_by_scheme"] = {k: {a: gauss(*v).get(a) for a in ("Mt", "MH", "status", "f_y")} for k, v in schemes.items()}
hit = (2.50, -3.62)
h0 = gauss(*hit)
eps = 0.02
out["hit"] = dict(Mt=h0["Mt"], MH=h0["MH"])
out["dMt_dLambda"] = (gauss(hit[0], hit[1] + eps)["Mt"] - gauss(hit[0], hit[1] - eps)["Mt"]) / (2 * eps)
out["dMt_dG"] = (gauss(hit[0] + eps, hit[1])["Mt"] - gauss(hit[0] - eps, hit[1])["Mt"]) / (2 * eps)
out["dMH_dLambda"] = (gauss(hit[0], hit[1] + eps)["MH"] - gauss(hit[0], hit[1] - eps)["MH"]) / (2 * eps)
Gs = np.linspace(1.6, 3.4, 37)
Ls = np.linspace(-4.6, -2.3, 47)
grid = []
inside = total = 0
window = []
for G_ in Gs:
    for L in Ls:
        r = gauss(float(G_), float(L))
        if r.get("status") != "ok":
            grid.append(None)
            total += 1
            continue
        total += 1
        if abs(r["Mt"] - 172.57) < 1.0:
            inside += 1
            window.append((round(float(G_), 3), round(float(L), 3), round(r["Mt"], 2), round(r["MH"], 2)))
out["grid_points"] = total
out["grid_within_1_GeV_of_Mt"] = inside
out["fraction_within_1_GeV"] = inside / total
out["window_samples"] = window[:: max(1, len(window) // 10)]
out["MH_range_on_the_Mt_band"] = (min(w[3] for w in window), max(w[3] for w in window)) if window else None
print(json.dumps(out, default=float))
json.dump(out, open("scheme_test.json", "w"), indent=1, default=float)
