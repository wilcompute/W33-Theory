"""Massive hypermultiplets give the gravitino route a minimum.  5D N = 1 supergravity with a Scherk-Schwarz twist omega, plus N_H bulk hypermultiplets of mass M: gravity contributes -8 S(omega, 0), each hyper +4 S(omega, x), where S(omega, x) = sum_w (1 - cos(2 pi w omega)) G_w(2 pi x)/zeta(5) and G_w(y) = exp(-z)(z^2 + 3 z + 3)/(3 w^5), z = w y, which is the massive Casimir series in closed form.  So
    V_C(x) = Z x^-4 [-8 S(omega, 0) + 4 N_H S(omega, x)],  x = M R
Multiplets are supersymmetric at short distance, so short circles cancel and no-AdS3 should hold without choosing M: that is tested in dd_sugra_ads3.py.  N_H >= 3 makes V_C positive at small x, which gives a minimum, as in the massive-hypermultiplet stabilisation of hep-th/0209178 here applied to the dark dimension.
For each N_H at omega = 1/2: x_min, V_C = 0, the fit with the radion started at the minimum, the x_0 grid and the x_0 where V_min = 0, the future.  Same machinery as casimir_massive.py and casimir_relax.py.  Compressed CMB.
usage: py -3 casimir_sugra.py dataset data_dir"""
import json
import math
import sys
import numpy as np

ds_, dd_ = sys.argv[1], sys.argv[2]
sys.argv = ["x", ds_, dd_]
src = open("casimir_massive.py", encoding="utf-8").read().split('fit4 = json.load(open(f"casimir_fits_{ds}.json"))')[0]
OM = 0.5
results = {}
for NH in (3, 4, 6, 8):
    s = src
    a = "gv = np.array([(-5 + 4 * NEFF * C_ratio(2 * math.pi * math.exp(u))) for u in lx])"
    assert a in s
    s = s.replace(a, f"gv = np.array([net_sugra(math.exp(u), {NH}) for u in lx])")
    a = "hv = np.array([math.exp(-4 * u) * (-5 + 4 * NEFF * C_ratio(2 * math.pi * math.exp(u))) for u in lx])\n"
    assert a in s
    s = s.replace(a, "")
    a = "lx = np.linspace(math.log(0.005), math.log(60.0), 900)\n"
    assert a in s
    s = s.replace(a, '''def S_om(x):
    y = 2 * math.pi * x
    t = 0.0
    for w in range(1, 200):
        z = w * y
        if z > 80:
            break
        t += (1 - math.cos(2 * math.pi * w * OM)) * math.exp(-z) * (z * z + 3 * z + 3) / (3 * w ** 5)
    return t / float(zeta(5))


def net_sugra(x, nh):
    return -8 * S_om(0.0) + 4 * nh * S_om(x)


''' + a)
    g = dict(OM=OM, __name__="x")
    exec(s, g)
    solve, future, X, nm, S, lc, Vc_over_h, dVc_du, umin, xmin, xzero = (g[k] for k in ("solve", "future", "X", "nm", "S", "lc", "Vc_over_h", "dVc_du", "umin", "xmin", "xzero"))
    fit4 = json.load(open(f"casimir_fits_{ds_}.json"))["best"]["0.7071_-1"]
    net = lambda x: net_sugra_outer(x, NH)
    b = 0.7071

    def run(x_i, zn0, start):
        best = None
        for z0 in (zn0, 0.7 * zn0, 1.4 * zn0):
            r = nm(lambda p: X(b, p[3], x_i, p[4], p[0], p[1], p[2]), [start["wb"], start["wbc"], start["h"], start["prod"], z0], S + [0.006, 0.1 * z0], 350)
            if best is None or r.fun < best.fun:
                best = r
        return best

    def net_sugra_outer(x, nh):
        return g["net_sugra"](x, nh)

    rows = {}
    xi_grid = [xmin, xmin * 1.1, xmin * 1.2, xmin * 1.35, xmin * 1.5, xmin * 2, xmin * 3]
    for k, xi in enumerate(xi_grid):
        x_target = xi * math.exp(b * fit4["info"]["chi0"] * 0.75)
        h0 = Vc_over_h(math.log(x_target))
        if h0 >= 0:
            continue
        zn0 = fit4["eps"] / h0
        r = run(xi, zn0, fit4)
        try:
            E, inf = solve(b, r.x[3], xi, r.x[4], *r.x[:3], want=True)
            fu = future(b, r.x[3], xi, r.x[4], *r.x[:3])
            rho = 3 * (100 * r.x[2] * 1000 / 3.085677581491367e22 * 6.582119569e-16) ** 2 * (2.435e27) ** 2
            nt = net_sugra_outer(inf["x0"], NH)
            Rm = (0.5 * abs(nt) * 3 * 1.0369277551433699 / (4 * math.pi ** 2 * (2 * math.pi) ** 4) / (abs(inf["eps"]) * rho)) ** 0.25 * 0.1973269804
            rows[str(round(xi / xmin, 2))] = dict(x_i=xi, delta=r.fun - lc.fun, prod=r.x[3], Zn=r.x[4], wb=r.x[0], wbc=r.x[1], h=r.x[2], x0=inf["x0"], eps=inf["eps"], chiN0=inf["chiN0"], R_micron=Rm, M_eV=inf["x0"] * 0.1973269804 / Rm, V_min=fu["V_at_minimum_over_crit"], turnaround_Gyr=fu["t_turnaround_Gyr"], net_today=nt)
            v = rows[str(round(xi / xmin, 2))]
            print("N_H", NH, "x_i/xmin", round(xi / xmin, 2), {a: (round(float(c), 4) if isinstance(c, (float, np.floating)) else c) for a, c in v.items() if a not in ("wb", "wbc", "h", "Zn", "x_i")}, flush=True)
        except Exception as e:
            rows[str(round(xi / xmin, 2))] = dict(delta=r.fun - lc.fun, failed=str(e))
        results[str(NH)] = dict(xmin=xmin, xzero=xzero, rows=rows, fading=json.load(open(f"fading_ds_{ds_}.json"))["free_c_neg"]["delta"])
        json.dump(results, open(f"casimir_sugra_{ds_}.json", "w"), indent=1, default=float)
print("done", flush=True)
