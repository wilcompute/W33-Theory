"""The knife-edge V_min = 0: between no-AdS4 (V_min >= 0) and the strong dS conjecture (V_min <= 0).  It is a slice of the x_0 family in casimir_massive_fine_*.json, the point where the minimum crosses zero, so no new fit is needed: fit quality, x_0, R and M are interpolated there.  Lambda = -Zn h_min is then not a free number, and dark energy is the radion's height above a zero-energy minimum.  Why V_min is exactly 0 is the cosmological constant problem restated, not solved.
Along the radion the minimum is global: V -> +infinity at small x, V -> Lambda > V_min at large x.  So a V_min > 0 minimum cannot decay along the radion, and TCC, which allows dS only for T < (1/H) ln(M_Pl/H), would need another channel; its T is computed for the relaxing radion.
Future at the row nearest V_min = 0: when acceleration ends, using the integrator of casimir_massive.py.  Also the slope |V'/V| today and at the end, against the dS conjecture.
Compressed CMB.  usage: py -3 casimir_mink.py dataset data_dir"""
import json
import math
import sys
import numpy as np

ds_, dd_ = sys.argv[1], sys.argv[2]
sys.argv = ["x", ds_, dd_]
src = open("casimir_massive.py", encoding="utf-8").read().split("S = [1e-4, 1e-3, 3e-3]\nlc =")[0]
exec(src)
fine = json.load(open(f"casimir_massive_fine_{ds}.json"))
rx = json.load(open(f"casimir_relax_{ds}.json"))
rows = sorted((r for r in fine["rows"].values() if "future" in r), key=lambda r: r["x0"])
xs = np.array([r["x0"] for r in rows])
vm = np.array([r["future"]["V_at_minimum_over_crit"] for r in rows])
i = int(np.where((vm[:-1] > 0) & (vm[1:] <= 0))[0][0])
t = vm[i] / (vm[i] - vm[i + 1])
itp = lambda k: rows[i][k] + t * (rows[i + 1][k] - rows[i][k])
out = dict(dataset=ds, x0=float(xs[i] + t * (xs[i + 1] - xs[i])), delta=itp("delta"), R_micron=itp("R_micron"), M_eV=itp("M_eV"), prod=itp("prod"), eps=itp("eps"))
b = 0.7071
near = rows[i] if abs(vm[i]) < abs(vm[i + 1]) else rows[i + 1]
x_i = math.exp(math.log(near["x0"]) - b * near["chi0"])
E, inf = solve(b, near["prod"], x_i, near["Zn"], near["wb"], near["wbc"], near["h"], want=True)
lu = math.log(x_i)
Zn, ol = near["Zn"], inf["ol"]
fo, uo = inf["fo"], inf["uo"]
orr = L.OMEGA_R_H2 / near["h"] ** 2


def rhs(t_, y):
    la, chi, cd, H = y
    a3 = math.exp(-3 * la)
    rc = fo * a3 * math.exp(-b * chi)
    return [H, cd, -3 * H * cd + 3 * (b * rc - Zn * b * dVc_du(lu + b * chi)), -0.5 * (cd * cd + 3 * (uo * a3 + rc + 4 / 3 * orr * a3 * math.exp(-la)))]


s = solve_ivp(rhs, (0, 4.0), [0.0, inf["chi0"], inf["chiN0"], 1.0], rtol=1e-8, atol=1e-10, method="LSODA", dense_output=True)
ts = np.linspace(0, s.t[-1], 3000)
y = s.sol(ts)
dH = -0.5 * (y[2] ** 2 + 3 * ((uo + fo * np.exp(-b * y[1])) * np.exp(-3 * y[0])))
acc = dH + y[3] ** 2
Gyr = 977.8 / (100 * near["h"])
out["future_near_row"] = dict(x0=near["x0"], V_min=near["future"]["V_at_minimum_over_crit"], acceleration_ends_Gyr=float(ts[np.argmax(acc < 0)] * Gyr) if (acc < 0).any() else None, turnaround_Gyr=near["future"]["t_turnaround_Gyr"], H_end=float(y[3, -1]), t_end_Gyr=float(ts[-1] * Gyr), chiN0=inf["chiN0"])
V0 = ol + Zn * Vc_over_h(lu + b * inf["chi0"])
out["slope_today"] = abs(Zn * b * dVc_du(lu + b * inf["chi0"]) / V0)
r0 = rx["rows"]["0.7071"]
Hm = math.sqrt(r0["future"]["V_at_minimum_over_crit"]) * 100 * r0["h"] * 1000 / 3.085677581491367e22 * 6.582119569e-16
out["TCC_relax"] = dict(H_min_eV=Hm, ln_MPl_over_H=math.log(2.435e27 / Hm), T_max_Gyr=math.log(2.435e27 / Hm) / Hm * 6.582119569e-16 / 3.156e16)
out["global_along_radion"] = bool(max(Zn * Vc_over_h(u) for u in np.linspace(umin + 0.01, math.log(50), 200)) > Zn * Vc_over_h(umin))
print({k: (round(float(v), 4) if isinstance(v, (float, np.floating)) else v) for k, v in out.items()}, flush=True)
json.dump(out, open(f"casimir_mink_{ds}.json", "w"), indent=1, default=float)
print("done", flush=True)
