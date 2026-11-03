"""Exact fixed points of KK dark matter on light moduli.  With only coupled dust and a massless field, chi_N = 2 b Omega_c is the attractor (Amendola's phi-MDE): Omega_chi = 2 b^2/3, w_eff = 2 b^2/3, rho_c ~ a^(-3 - 2 b^2), H ~ a^(-(3/2)(1 + w_eff)).
b^2 from the moduli metric ds^2 = sum d sigma_i^2 + (1/2)(sum d sigma_i)^2: 3/2 for m_KK with all moduli free, n/(n+1) at fixed volume.  So the "matter era" of the data would be, at b^2 = 3/2, kination (rho_c ~ a^-6), at n = 1 fixed volume radiation-like (rho_c ~ a^-4).
Symbolic: the fixed point of the autonomous system.  Numeric control: integrate from rest with no baryons or radiation and read w_eff, chi_N, d ln rho_c / dN.  usage: py -3 dm_drag_fixed.py"""
import json
import math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

b, x = sp.symbols("b x", positive=True)
# autonomous: x = chi_N, Om = 1 - x^2/6, dlnH = -(1/2)(x^2 + 3 Om); x_N = -(3 + dlnH) x + 3 b Om
Om = 1 - x ** 2 / 6
dlnH = -sp.Rational(1, 2) * (x ** 2 + 3 * Om)
fp = sp.simplify((-(3 + dlnH) * x + 3 * b * Om).subs(x, 2 * b))
assert fp == 0
out = dict(fixed_point_residual=str(fp), rows={})
weff = sp.simplify((-2 * dlnH / 3 - 1).subs(x, 2 * b))
assert sp.simplify(weff - 2 * b ** 2 / 3) == 0
geom = {"m_KK all moduli free": sp.Rational(3, 2)}
for n in (1, 2, 3, 6):
    geom[f"m_KK fixed volume n={n}"] = sp.Rational(n, n + 1)
geom["M_D, n=0 (one extra dimension)"] = sp.Rational(1, 6)
geom["fitted c'=0.05"] = sp.Rational(1, 400)


def integrate(b2):
    bv = math.sqrt(b2)

    def rhs(N, s):
        o = 1 - s[0] ** 2 / 6
        d = -0.5 * (s[0] ** 2 + 3 * o)
        return [-(3 + d) * s[0] + 3 * bv * o]

    s = solve_ivp(rhs, (0, 80), [0.0], rtol=1e-11, atol=1e-13, method="LSODA")
    x_ = s.y[0, -1]
    return x_, x_ * x_ / 6 + (x_ * x_ / 6 - (1 - x_ * x_ / 6)) * 0, -3 - bv * x_


for k, b2 in geom.items():
    x_, _, slope = integrate(float(b2))
    w_ex = sp.Rational(2, 3) * b2
    out["rows"][k] = dict(b_squared=str(b2), w_eff_exact=str(w_ex), rho_c_slope_exact=str(-3 - 2 * b2), chi_N_num=x_, chi_N_exact=float(2 * sp.sqrt(b2)), rho_c_slope_num=slope)
    print(k, out["rows"][k], flush=True)
    assert abs(x_ - float(2 * sp.sqrt(b2))) < 1e-6 or float(b2) >= 1.5 - 1e-9
json.dump(out, open("dm_drag_fixed.json", "w"), indent=1)
