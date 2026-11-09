"""Can the dark-energy field be the level-3 flavour modulus?  [N] numerics + published clock bound; illustrative proxy.
The corpus's flavour sector is a level-3 modulus (genus-2 Siegel; at genus 1 the Gamma(3) ~ A4 modular forms).  If the field that rolls as
dark energy (phi_N ~ 0.46 M_P per e-fold today in the fading fits, dd_clocks.json) were that modulus, fermion mass ratios would drift with it;
the atomic-clock bound |mudot/mu| (Lange et al 2021) gives |d ln mu / d phi| < 2.5e-6 per M_P (dd_clocks.py: kappa_mu_max).
Loophole tested: at an elliptic fixed point every modular-invariant real function is stationary (the stabiliser rotates the tangent plane by
120 or 180 degrees; the only invariant gradient is zero), so the LINEAR coupling vanishes there.  Does the quadratic one survive?
Proxy observable: ln of eigenvalue ratios of M^dag M, M = Feruglio's A4 weight-2 Weinberg texture (1706.08749)
    M = [[2Y1, -Y3, -Y2], [-Y3, 2Y2, -Y1], [-Y2, -Y1, 2Y3]],
with the level-3 weight-2 triplet from its q-expansion.  Ratios are modular invariant (M -> (c tau + d)^2 rho^T M rho, rho unitary), so
stationarity at omega and i is also a CHECK on the forms: a wrong expansion would not be stationary.
Canonical field: K = -h ln(2 Im tau) gives dphi^2 = h |dtau|^2 / (2 (Im tau)^2); reported for h = 3 and h = 1.
Control: a generic tau, where the gradient must not vanish.
usage: py -3 flavour_modulus_clock.py"""
import cmath
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
# divisor-sum coefficients of the level-3 weight-2 triplet (Feruglio 2017): Y1 = 1 + 12 sum, Y2 = -6 q^(1/3) sum, Y3 = -18 q^(2/3) sum
def sigma_mod(n, r):
    return sum(d for d in range(1, n + 1) if n % d == 0 and d % 3 == r)


def forms(tau, nmax=40):
    q = cmath.exp(2j * math.pi * tau)
    # Y1 = 1 + 12 sum_n (sigma_1(n) - 3 sigma_1(n/3)) q^n ... use the standard closed forms in terms of E2-type Lambert series:
    # Y1 = 1 + 12 sum_{n>=1} [d(n)] with d(n) = sum_{d|n, 3 not| d} d ; Y2 = -6 sum_{n>=0} sigma(3n+1) q^(n+1/3); Y3 = -18 sum_{n>=0} sigma(3n+2) q^(n+2/3)
    s1 = sum(sum(d for d in range(1, n + 1) if n % d == 0 and d % 3 != 0) * q ** n for n in range(1, nmax))
    Y1 = 1 + 12 * s1
    q13 = cmath.exp(2j * math.pi * tau / 3)
    Y2 = -6 * q13 * sum(sum(d for d in range(1, 3 * n + 2) if (3 * n + 1) % d == 0) * q ** n for n in range(nmax))
    Y3 = -6 * q13 ** 2 * sum(sum(d for d in range(1, 3 * n + 3) if (3 * n + 2) % d == 0) * q ** n for n in range(nmax))
    return Y1, Y2, Y3


def obs(tau):
    Y1, Y2, Y3 = forms(tau)
    M = np.array([[2 * Y1, -Y3, -Y2], [-Y3, 2 * Y2, -Y1], [-Y2, -Y1, 2 * Y3]])
    ev = np.sort(np.linalg.eigvalsh(M.conj().T @ M))
    return np.log(ev[1] / ev[0]), np.log(ev[2] / ev[1])


def deriv(tau, h, eps=1e-4):
    """gradient and Hessian of each observable in canonical-field units at tau (real coordinates x, y of tau)"""
    s = math.sqrt(2) * tau.imag / math.sqrt(h)  # dtau_real per unit dphi along a coordinate direction
    f = lambda dx, dy: np.array(obs(tau + complex(dx, dy) * s))
    f0 = f(0, 0)
    gx = (f(eps, 0) - f(-eps, 0)) / (2 * eps)
    gy = (f(0, eps) - f(0, -eps)) / (2 * eps)
    hxx = (f(eps, 0) - 2 * f0 + f(-eps, 0)) / eps ** 2
    hyy = (f(0, eps) - 2 * f0 + f(0, -eps)) / eps ** 2
    hxy = (f(eps, eps) - f(eps, -eps) - f(-eps, eps) + f(-eps, -eps)) / (4 * eps ** 2)
    out = []
    for k in range(2):
        H = np.array([[hxx[k], hxy[k]], [hxy[k], hyy[k]]])
        out.append(dict(value=float(f0[k]), grad_norm=float(math.hypot(gx[k], gy[k])), hess_eig=[float(v) for v in np.linalg.eigvalsh(H)]))
    return out


# self-check of the q-expansions: the known closed forms must satisfy Y2^2 + 2 Y1 Y3 = 0 (Feruglio's weight-4 constraint)
def constraint(tau):
    Y1, Y2, Y3 = forms(tau)
    return abs(Y2 ** 2 + 2 * Y1 * Y3) / abs(Y1) ** 2


omega = complex(-0.5, math.sqrt(3) / 2)
pts = dict(omega=omega, i=1j, generic=complex(0.13, 1.21))
dd = json.load(open(os.path.join(HERE, "dd_clocks.json")))
kmu = dd["dovekie"]["free_c_neg"]["kappa_mu_max"]
dphi = dd["dovekie"]["free_c_neg"]["phi_N_today"]  # field speed per e-fold today (M_P)
# The Hessian route fails at the fixed points: the residual symmetry forces degenerate (omega) or vanishing (i) eigenvalues, so the
# ratios are not smooth there (eigenvalues split linearly in the distance: a cone).  Measure instead the radial sensitivity
#   S(delta) = max over directions and observables of |d obs / d phi| at canonical distance delta from the point.
def sens(t, h, delta, ndir=24, eps_rel=1e-3):
    s = math.sqrt(2) * t.imag / math.sqrt(h)
    best = 0.0
    for j in range(ndir):
        u = cmath.exp(2j * math.pi * (j + 0.5) / ndir)
        e = delta * eps_rel
        a = np.array(obs(t + u * (delta + e) * s)); b = np.array(obs(t + u * (delta - e) * s))
        v = np.abs(a - b) / (2 * e)
        v = v[np.isfinite(v)]
        if v.size:
            best = max(best, float(v.max()))
    return best


res = dict(kappa_mu_max=kmu, phi_N_today=dphi, constraint_check={k: constraint(v) for k, v in pts.items()}, values={k: [float(x) for x in obs(v)] for k, v in pts.items()}, scan={})
DEL = (1e-3, 1e-2, 3e-2, 1e-1, 3e-1)
for name, t in pts.items():
    res["scan"][name] = {f"h{h}": {str(d): sens(t, h, d) for d in DEL} for h in (3, 1)}
# what the clock bound requires: the coupling is |d ln mu/d phi|; with an O(1) map from these ratios to mu, it is S itself
res["violation_factor_h3"] = {name: {d: v / kmu for d, v in r["h3"].items()} for name, r in res["scan"].items()}
json.dump(res, open(os.path.join(HERE, "flavour_modulus_clock.json"), "w"), indent=1)
print("constraint |Y2^2+2Y1Y3|/|Y1|^2:", {k: "%.1e" % v for k, v in res["constraint_check"].items()})
print("ln ratios at the points:", {k: [round(x, 4) for x in v] for k, v in res["values"].items()})
for name in pts:
    print(name, "h=3 S(delta):", {d: "%.3g" % v for d, v in res["scan"][name]["h3"].items()}, "| h=1:", {d: "%.3g" % v for d, v in res["scan"][name]["h1"].items()})
print("kappa_mu_max %.2e -> violation factors (h=3):" % kmu, {n: {d: "%.1e" % v for d, v in r.items()} for n, r in res["violation_factor_h3"].items()})
