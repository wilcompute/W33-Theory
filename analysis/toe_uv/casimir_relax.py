"""The radion starts at its Casimir minimum, x_i = x_min for N_f = 2, the dark matter drag displaces it, and it relaxes back as matter dilutes.  This removes x_0: free parameters are f b and Zn (R), the same count as (c, c'), and no choice of branch is left.  The field at rest at the minimum feels only the drag, so nothing else initiates the motion.
Why it would start there is not explained: at H >> mu the field does not relax by itself, so this is an initial condition, and it is tested here as such.
Also: how close does the free x_i fit come to it, the mass of the field about the minimum, the field's oscillation today and the future.  Compressed CMB.  usage: py -3 casimir_relax.py dataset data_dir"""
import json
import math
import sys
import numpy as np

ds_, dd_ = sys.argv[1], sys.argv[2]
sys.argv = ["x", ds_, dd_]
src = open("casimir_massive.py", encoding="utf-8").read().split('fit4 = json.load(open(f"casimir_fits_{ds}.json"))')[0]
exec(src)
fit4 = json.load(open(f"casimir_fits_{ds}.json"))["best"]["0.7071_-1"]
fine = json.load(open(f"casimir_massive_fine_{ds}.json"))
fading = json.load(open(f"fading_ds_{ds}.json"))["free_c_neg"]["delta"]
out = dict(dataset=ds, LCDM=lc.fun, fading=fading, xmin=xmin, rows={})
for b in (0.7071, 0.9258, 1.0):
    start = fine["rows"]["0.5"]
    best = None
    for z0 in (start["Zn"], 0.7 * start["Zn"], 1.4 * start["Zn"]):
        r = nm(lambda p: X(b, p[3], xmin, p[4], p[0], p[1], p[2]), [start["wb"], start["wbc"], start["h"], start["prod"], z0], S + [0.006, 0.1 * z0], 500)
        if best is None or r.fun < best.fun:
            best = r
    E, inf = solve(b, best.x[3], xmin, best.x[4], *best.x[:3], want=True)
    fu = future(b, best.x[3], xmin, best.x[4], *best.x[:3])
    rho = 3 * (100 * best.x[2] * 1000 / 3.085677581491367e22 * 6.582119569e-16) ** 2 * (2.435e27) ** 2
    net = -5 + 4 * NEFF * C_ratio(2 * math.pi * inf["x0"])
    Rm = (0.5 * abs(net) * 3 * 1.0369277551433699 / (4 * math.pi ** 2 * (2 * math.pi) ** 4) / (abs(inf["eps"]) * rho)) ** 0.25 * 0.1973269804
    eh = 1e-3
    d2 = (Vc_over_h(umin + eh) - 2 * Vc_over_h(umin) + Vc_over_h(umin - eh)) / eh ** 2
    mu2 = 3 * b * b * best.x[4] * d2  # field mass squared about the minimum in H0^2 units; V in units of rho_crit = 3 H0^2
    out["rows"][str(b)] = dict(delta=best.fun - lc.fun, prod=best.x[3], f=best.x[3] / b, Zn=best.x[4], wb=best.x[0], wbc=best.x[1], h=best.x[2], x0=inf["x0"], eps=inf["eps"], chi0=inf["chi0"], chiN0=inf["chiN0"], dlnm=inf["dlnm"], R_micron=Rm, M_eV=xmin * 0 + inf["x0"] * 0.1973269804 / Rm, mu_over_H0=math.sqrt(abs(mu2)), future=fu)
    v = out["rows"][str(b)]
    print(b, {k: (round(float(a), 4) if isinstance(a, (float, np.floating)) else a) for k, a in v.items() if k != "future"}, "Vmin", round(fu["V_at_minimum_over_crit"], 3), "turn", fu["t_turnaround_Gyr"], flush=True)
    json.dump(out, open(f"casimir_relax_{ds}.json", "w"), indent=1, default=float)
print("done", flush=True)
