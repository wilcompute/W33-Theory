"""One Einstein-Hilbert flow in one scheme, with the regulator as the only thing varied (Reuter; Lauscher-Reuter; Reuter-Saueressig, Feynman-de Donder gauge):
eta = g B1 / (1 - g B2), beta_g = (2 + eta) g, beta_lam = (eta - 2) lam + (g / pi) [5 Phi^2_1(-2 lam) - 4 Phi^2_1(0) - (5/2) eta Phit^2_1(-2 lam)],
B1 = (1/3 pi) [5 Phi^1_1(-2 lam) - 18 Phi^2_2(-2 lam) - 4 Phi^1_1(0) - 6 Phi^2_2(0)], B2 = -(1/6 pi) [5 Phit^1_1(-2 lam) - 18 Phit^2_2(-2 lam)].
Phi^n_m(w) = (1/Gamma(n)) int_0^inf z^(n-1) (R0 - z R0') / (z + R0 + w)^m dz, Phit the same with R0 in the numerator.
Matter, as in Dona-Eichhorn-Percacci eqs. 35, 36, massless: eta picks up g (N_S + 2 N_D - 4 N_V) / (6 pi) with no regulator dependence; beta_lam picks up (g / 4 pi) (N_S - 4 N_D + 2 N_V) Q, with Q = Phi^2_1(0) / (optimised value 1/2): regulator dependent.  This matter term is the simplest consistent choice, and it is not the only one.
Controls: pure gravity optimised (0.707, 0.193) and exponential (g about 0.403, lam about 0.330) as quoted in the literature from memory; SM against Dona Table 3 scheme II, full (1.735, -2.348).
The question: how far do g*, Lam*, g* Lam* and the exponents move with the regulator, for the same matter?  usage: py -3 frg_regulators.py"""
import json
import math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import fsolve
from scipy.special import gamma


def make(reg):
    if reg[0] == "opt":
        def Phi(n, m, w):
            return 1 / gamma(n + 1) / (1 + w) ** m
        def Phit(n, m, w):
            return 1 / gamma(n + 2) / (1 + w) ** m
        return Phi, Phit
    s = reg[1]
    if reg[0] == "exp":
        def R(z):
            x = z ** s
            return z / np.expm1(x)
        def dR(z):
            h = 1e-5 * max(z, 1e-3)
            return (R(z + h) - R(z - h)) / (2 * h)
    else:
        raise ValueError
    cache = {}
    def Phi(n, m, w):
        k = ("P", n, m, round(w, 8))
        if k not in cache:
            cache[k] = quad(lambda z: z ** (n - 1) * (R(z) - z * dR(z)) / (z + R(z) + w) ** m, 1e-7, 60, limit=300)[0] / gamma(n)
        return cache[k]
    def Phit(n, m, w):
        k = ("T", n, m, round(w, 8))
        if k not in cache:
            cache[k] = quad(lambda z: z ** (n - 1) * R(z) / (z + R(z) + w) ** m, 1e-7, 60, limit=300)[0] / gamma(n)
        return cache[k]
    return Phi, Phit


def betas(v, Phi, Phit, m):
    g, lam = v
    Ns, Nd, Nv = m
    w = -2 * lam
    B1 = (5 * Phi(1, 1, w) - 18 * Phi(2, 2, w) - 4 * Phi(1, 1, 0) - 6 * Phi(2, 2, 0)) / (3 * math.pi) + (Ns + 2 * Nd - 4 * Nv) / (6 * math.pi)
    B2 = -(5 * Phit(1, 1, w) - 18 * Phit(2, 2, w)) / (6 * math.pi)
    eta = g * B1 / (1 - g * B2)
    Q = Phi(2, 1, 0) / 0.5
    bl = (eta - 2) * lam + g / math.pi * (5 * Phi(2, 1, w) - 4 * Phi(2, 1, 0) - 5 / 2 * eta * Phit(2, 1, w)) + g / (4 * math.pi) * (Ns - 4 * Nd + 2 * Nv) * Q
    return [(2 + eta) * g, bl], eta


def fp(reg, m, starts):
    Phi, Phit = make(reg)
    best = []
    for s0 in starts:
        try:
            sol, info, ok, _ = fsolve(lambda v: betas(v, Phi, Phit, m)[0], s0, full_output=True, xtol=1e-9)
        except Exception:
            continue
        if ok == 1 and sol[0] > 1e-3 and sol[1] < 0.45 and abs(1 + (-2 * sol[1])) > 1e-3:
            r = [round(float(x), 5) for x in sol]
            if r not in best:
                best.append(r)
    res = []
    for g, lam in best:
        e = 1e-5
        J = np.zeros((2, 2))
        for i in range(2):
            a, b = [g, lam], [g, lam]
            a = list(a)
            b = list(b)
            a[i] += e
            b[i] -= e
            fa, fb = betas(a, Phi, Phit, m)[0], betas(b, Phi, Phit, m)[0]
            J[:, i] = [(fa[k] - fb[k]) / (2 * e) for k in range(2)]
        th = -np.linalg.eigvals(J)
        res.append(dict(g=g, Lam=lam, gLam=g * lam, eta=betas([g, lam], Phi, Phit, m)[1], theta=[complex(round(x.real, 3), round(x.imag, 3)) for x in th]))
    return res


regs = [("opt",), ("exp", 1), ("exp", 2), ("exp", 3), ("exp", 5)]
matter = dict(pure=(0, 0, 0), SM=(4, 22.5, 12), SM_3nuR=(4, 24, 12), SM_3nuR_axion_dm=(6, 24, 12))
starts = dict(pure=[(0.7, 0.2), (0.4, 0.33), (0.3, 0.3), (0.5, 0.25), (1.0, 0.15), (0.2, 0.2)], SM=[(1.7, -2.3), (1.5, -2), (2, -2.5), (1, -1.5), (0.8, -1), (2.5, -3), (0.6, -0.5), (3, -4), (1.2, -1), (2, -5), (3, -8)])
out = {}
for name, m in matter.items():
    out[name] = {}
    for r in regs:
        rr = fp(r, m, starts.get(name, starts["SM"]))
        # physical branch: UV-attractive (both Re theta > 0) with the largest g in range
        ph = [x for x in rr if all(complex(t).real > 0 for t in x["theta"])]
        out[name][str(r)] = ph
        print(name, r, [(x["g"], x["Lam"], round(x["gLam"], 3), x["theta"]) for x in ph][:2], flush=True)
summary = {}
for name in matter:
    g_, L_, P_ = [], [], []
    for k, v in out[name].items():
        if v:
            g_.append(v[0]["g"])
            L_.append(v[0]["Lam"])
            P_.append(v[0]["gLam"])
    if g_:
        summary[name] = dict(n=len(g_), g=(min(g_), max(g_)), Lam=(min(L_), max(L_)), gLam=(min(P_), max(P_)), spread_Lam=(max(L_) - min(L_)), spread_frac_Lam=(max(L_) - min(L_)) / abs(np.mean(L_)), spread_frac_gLam=(max(P_) - min(P_)) / abs(np.mean(P_)))
out["summary"] = summary
print(json.dumps(summary, default=str))
json.dump(out, open("frg_regulators.json", "w"), indent=1, default=str)
