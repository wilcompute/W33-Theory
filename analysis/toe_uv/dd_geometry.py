"""Geometry of a rolling dark dimension: what the moduli-space metric ties together.  [E] from the standard reduction; no fit.
D = 4 + 1 + n, internal radii exp(sigma_i).  M_Pl^2 = M_D^(n+3) Vol, in units M_D = 1.  4D Einstein-frame kinetic metric, M_Pl = 1:
    ds^2 = sum d sigma_i^2 + (1/2) (sum d sigma_i)^2.
Scales in Planck units: m_KK = exp(-u - nu/2), M_D = exp(-nu/2), u = d sigma_dark, nu = d ln Vol.
c' = -d ln m_KK / d phi, beta = -d ln M_D / d phi along a unit-speed trajectory.  A brane sector whose scales are fixed in units of M_D has universal coupling beta.
Controls: the 5D radion must give m_KK ~ exp(-sqrt(3/2) phi) and Brans-Dicke omega = 0, gamma = 1/2 (known for one extra dimension).
usage: py -3 dd_geometry.py"""
import json
import math
import sympy as sp

out = {}
u, n, xi = sp.symbols("u n xi", positive=True)

# 5D radion: pure radius, n = 0
norm5 = sp.sqrt(1 + sp.Rational(1, 2))
c5 = sp.simplify((1 + sp.Rational(1, 2)) / norm5)
b5 = sp.simplify(sp.Rational(1, 2) / norm5)
alpha5 = 2 * b5 ** 2
gamma5 = (1 - alpha5) / (1 + alpha5)
out["radion_5D"] = dict(c_prime=str(c5), beta=str(b5), alpha=str(alpha5), gamma=str(gamma5), ratio=str(sp.simplify(b5 / c5)))
assert c5 == sp.sqrt(sp.Rational(3, 2)) and alpha5 == sp.Rational(1, 3) and gamma5 == sp.Rational(1, 2)

# general volume-change fraction: nu = xi u
ratio = sp.simplify((xi / 2) / (1 + xi / 2))
assert sp.simplify(ratio - xi / (2 + xi)) == 0
out["beta_over_cprime"] = "xi/(2+xi), xi = dlnVol/dlnL"

# fixed volume, n isotropic other dimensions: v = -u, nu = 0
norm_fix = sp.sqrt(1 + 1 / n)
cfix = sp.simplify(1 / norm_fix)
out["cprime_fixed_volume"] = str(cfix)
out["cprime_fixed_volume_values"] = {str(k): float(cfix.subs(n, k)) for k in (1, 2, 3, 5, 6)}
assert abs(cfix.subs(n, 1) - 1 / sp.sqrt(2)) == 0

# minimum c' given only that L moves: minimise slope over all geometric directions (sigma_dark, Vol), with n others
# c'^2 / metric: maximum of |dlnm_KK| per unit length is the gradient norm, so geometric directions have c' from 0 to |grad|.
# inverse metric on (sigma_i): G^ij = delta^ij - 1/(n+3); grad ln m_KK in sigma space = (1 + 1/2, 1/2, ..., 1/2)
N = 4
sig = sp.symbols("s0:%d" % N)
G = sp.eye(N) + sp.Rational(1, 2) * sp.ones(N, N)
g = sp.Matrix([sp.Rational(3, 2)] + [sp.Rational(1, 2)] * (N - 1))
gb = sp.Matrix([sp.Rational(1, 2)] * N)
Ginv = G.inv()
gm2 = (g.T * Ginv * g)[0]
gb2 = (gb.T * Ginv * gb)[0]
gmb = (g.T * Ginv * gb)[0]
out["gradient_norms_n3"] = dict(mKK=str(gm2), MD=str(gb2), inner=str(gmb))
# with N = 1 + n radii: |grad ln m_KK|^2 = (n+3)/(n+2) * ... recomputed for each n
rows = {}
for nn in (0, 1, 2, 3, 5, 6):
    N_ = nn + 1
    G_ = sp.eye(N_) + sp.Rational(1, 2) * sp.ones(N_, N_)
    gk = sp.Matrix([sp.Rational(3, 2)] + [sp.Rational(1, 2)] * nn)
    gd = sp.Matrix([sp.Rational(1, 2)] * N_)
    Gi = G_.inv()
    rows[nn] = dict(mKK_sq=str((gk.T * Gi * gk)[0]), MD_sq=str((gd.T * Gi * gd)[0]), inner=str((gk.T * Gi * gd)[0]))
out["gradients_by_n"] = rows
assert rows[0]["mKK_sq"] == "3/2" and rows[0]["MD_sq"] == "1/6" and rows[0]["inner"] == "1/2"

# Observational bounds.  Cassini: gamma - 1 = (2.1 +- 2.3) e-5 (Bertotti, Iess, Tortora 2003).  LLR: Gdot/G = (7.1 +- 7.6) e-14 / yr (Hofmann, Mueller 2018).
gm1_2sig = 2.1e-5 + 2 * 2.3e-5
# gamma - 1 = -2 alpha / (1 + alpha), alpha = 2 beta^2.  The sign of a scalar force gives gamma < 1, so the one-sided bound is the 2 sigma lower limit.
gm1_low = abs(2.1e-5 - 2 * 2.3e-5)
out["cassini"] = dict(gamma_minus_1_lower_2sigma=-gm1_low, beta_max_one_sided=math.sqrt(gm1_low / 4), beta_max_two_sided=math.sqrt(gm1_2sig / 4))
H0_per_yr = 67.5 / 3.0857e19 * 3.156e7
out["llr"] = dict(Gdot_over_GH0_2sigma=(7.1e-14 + 2 * 7.6e-14) / H0_per_yr, H0_per_yr=H0_per_yr)
for cp in (0.03, 0.05, 0.07):
    for key in ("beta_max_one_sided", "beta_max_two_sided"):
        bm = out["cassini"][key]
        out.setdefault("xi_max", {}).setdefault(key, {})[str(cp)] = 2 * (bm / cp) / (1 - bm / cp)
    out.setdefault("pure_radius", {})[str(cp)] = dict(beta=cp / 3, gamma_minus_1=-2 * (2 * (cp / 3) ** 2) / (1 + 2 * (cp / 3) ** 2))
json.dump(out, open("dd_geometry.json", "w"), indent=1)
print(json.dumps(out, indent=1))

# n = 1, moduli (L, Vol) only: a unit vector is fixed by (c', beta), so c' = 0.05 fixes beta.  Gram matrix of the gradients: [[3/2, 1/2], [1/2, 1/4]], giving 2 c'^2 - 8 c' beta + 12 beta^2 = 1.
b_, cpv = sp.symbols("b cp")
gram = sp.Matrix([[sp.Rational(3, 2), sp.Rational(1, 2)], [sp.Rational(1, 2), sp.Rational(1, 4)]])
vec = sp.Matrix([cpv, b_])
quad = sp.expand((vec.T * gram.inv() * vec)[0])
assert quad == 2 * cpv ** 2 - 8 * cpv * b_ + 12 * b_ ** 2
sols = sp.solve(quad.subs(cpv, sp.Rational(1, 20)) - 1, b_)
out["n1_two_moduli"] = dict(unit_condition=str(quad) + " = 1", beta_at_cprime_0p05=[float(s) for s in sols], cprime_at_beta_0=float(sp.sqrt(sp.Rational(1, 2))))
out["kinetic_fraction_along_grad_mKK"] = {str(cp): cp ** 2 / 1.5 for cp in (0.03, 0.05, 0.07)}
json.dump(out, open("dd_geometry.json", "w"), indent=1)
print(out["n1_two_moduli"], out["kinetic_fraction_along_grad_mKK"])
