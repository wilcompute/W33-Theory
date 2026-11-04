"""No-AdS3 at the actual fitted (R, M) of casimir_massive_fine_*.json, rather than at the fixed eps of dd_massive_fermions.py, and the conjunction with no-AdS4: V at the radion minimum must not be negative.  Reports for N_f = 2 which x_0 pass both, and the resulting window for R and M, on each sample; and the m1 bound there.
Interval convention for the tower (n >= 1 gravitons, n >= 0 fermions); a circle would double the levels and move R by 2^(1/4).  usage: py -3 dd_massive_check.py"""
import json
import math
import numpy as np
from scipy.optimize import brentq

src = open("dd_massive_fermions.py", encoding="utf-8").read().split("# control 1, no tower")[0]
g = {"__name__": "x"}
exec(src, g)
v_of_L, HC = g["v_of_L"], g["HC"]
out = {}
for ds in ("pantheon", "dovekie", "desy5"):
    d = json.load(open(f"casimir_massive_fine_{ds}.json"))
    rows = {}
    for k, r in d["rows"].items():
        if "R_micron" not in r:
            continue
        R = r["R_micron"] / HC
        x0 = r["x0"]
        v = v_of_L(0.0, R, 2, x0)
        ads3 = bool(v.min() < 0)
        m1 = None
        if not ads3:
            fn = lambda m: float(v_of_L(m, R, 2, x0).min())
            hi = 1e-4
            while fn(hi) > 0 and hi < 0.2:
                hi *= 1.5
            m1 = brentq(fn, hi / 1.5, hi, xtol=1e-5) if hi < 0.2 else None
        fu = r["future"]
        rows[k] = dict(x0=x0, R_micron=r["R_micron"], M_eV=r["M_eV"], delta=r["delta"], eps=r["eps"], ads3=ads3, m1_bound_eV=m1, V_min=fu["V_at_minimum_over_crit"], ads4=bool(fu["V_at_minimum_over_crit"] < 0), turnaround_Gyr=fu["t_turnaround_Gyr"])
        print(ds, k, {a: (round(b, 4) if isinstance(b, float) else b) for a, b in rows[k].items()}, flush=True)
    ok = [v for v in rows.values() if not v["ads3"] and not v["ads4"]]
    out[ds] = dict(rows=rows, window=dict(x0=[min(v["x0"] for v in ok), max(v["x0"] for v in ok)], R_micron=[min(v["R_micron"] for v in ok), max(v["R_micron"] for v in ok)], M_eV=[min(v["M_eV"] for v in ok), max(v["M_eV"] for v in ok)], delta=[min(v["delta"] for v in ok), max(v["delta"] for v in ok)]) if ok else None)
    print(ds, "window", out[ds]["window"], flush=True)
json.dump(out, open("dd_massive_check.json", "w"), indent=1, default=float)
print("done", flush=True)
