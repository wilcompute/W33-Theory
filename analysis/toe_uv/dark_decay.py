"""Does the signal need a scalar at all?  The fading fit amounts to dark matter losing about 1.3 percent of its energy after recombination.  Lambda + decaying dark matter loses energy with no field, no fifth force and no drag: rho_d' = -Gamma rho_d / H into dark radiation.
Models, all with a true cosmological constant:
 D1: a fraction F of the cold dark matter decays with rate Gamma (two parameters, same count as fading); F = 1 is one parameter.
 Decay products are dark radiation only; a warm product is not modelled.
Compressed CMB, background only; omega_bc at recombination as elsewhere.  usage: py -3 dark_decay.py dataset data_dir"""
import json
import math
import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import dark_like as L

ds, ddir = sys.argv[1], sys.argv[2]
sn = L.load_sn(ds, ddir)
NI = -12.0
NG = np.log(1 / (1 + L.ZGRID))[::-1]
NREC = -math.log(1090.0)


def nm(fn, x0, steps, maxiter):
    x0 = np.asarray(x0, float)
    return minimize(fn, x0, method="Nelder-Mead", options=dict(xatol=3e-5, fatol=3e-3, maxiter=maxiter, maxfev=maxiter, initial_simplex=np.vstack([x0] + [x0 + np.eye(len(x0))[i] * steps[i] for i in range(len(x0))])))


def E_decay(F, G, wb, wbc, h):
    """G = Gamma/H0.  State: rho_d a^3, rho_dr a^4, in units of 3 H0^2.  Lambda closes E(0) = 1."""
    h2 = h * h
    orr, ob, onu = L.OMEGA_R_H2 / h2, wb / h2, L.OMEGA_NU_H2 / h2
    oc = (wbc - wb) / h2

    def run(ol, oci):
        def rhs(N, y):
            d, r = y
            a = math.exp(N)
            E = math.sqrt(max(((1 - F) * oci + ob + onu + d) / a ** 3 + (orr + r) / a ** 4 + ol, 1e-12))
            return [-G * d / E, G * d * a / E]
        return solve_ivp(rhs, (NI, 0), [F * oci, 0.0], rtol=1e-8, atol=1e-12, method="LSODA", dense_output=True)

    oci = oc
    ol = 1 - (wbc + L.OMEGA_NU_H2) / h2
    for _ in range(6):
        s = run(ol, oci)
        d0, r0 = s.y[:, -1]
        ol2 = 1 - ((1 - F) * oci + ob + onu + d0) - orr - r0
        drec = float(s.sol(NREC)[0])
        oci2 = oc / ((1 - F) + drec / oci)
        conv = abs(ol2 - ol) < 1e-8 and abs(oci2 / oci - 1) < 1e-8
        ol, oci = ol2, oci2
        if conv:
            break
    s = run(ol, oci)
    y = s.sol(NG)
    a = np.exp(NG)
    E2 = ((1 - F) * oci + ob + onu + y[0]) / a ** 3 + (orr + y[1]) / a ** 4 + ol
    lost = 1 - ((1 - F) * oci + float(s.y[0, -1])) / oc
    return np.sqrt(E2)[::-1], lost


def chi(F, G, wb, wbc, h):
    if not (0 < F <= 1) or G < 0 or G > 60:
        return 1e8
    try:
        return L.chi2(E_decay(F, G, wb, wbc, h)[0], h, wb, wbc, sn)
    except Exception:
        return 1e8


S = [1e-4, 1e-3, 3e-3]
lc = nm(lambda p: L.chi2(L.E_lcdm(p[1], p[2]), p[2], p[0], p[1], sn), [0.02223, 0.142, 0.675], S, 800)
prev = json.load(open(f"fading_ds_{ds}.json"))
out = dict(dataset=ds, LCDM=lc.fun, fading=prev["free_c_neg"]["delta"])
assert abs(chi(1.0, 0.0, *lc.x) - lc.fun) < 1e-3
out["control_G0_equals_LCDM"] = chi(1.0, 0.0, *lc.x) - lc.fun
best = None
for F0, G0 in ((0.05, 0.3), (0.2, 0.1), (1.0, 0.02), (0.02, 3.0), (0.05, 10.0), (0.3, 1.0)):
    r = nm(lambda p: chi(p[3], p[4], p[0], p[1], p[2]), list(lc.x) + [F0, G0], S + [0.02, 0.1], 500)
    print("start", F0, G0, round(r.fun - lc.fun, 3), np.round(r.x[3:], 4), flush=True)
    if best is None or r.fun < best.fun:
        best = r
_, lost = E_decay(best.x[3], best.x[4], *best.x[:3])
out["D1_free"] = dict(delta=best.fun - lc.fun, F=best.x[3], G=best.x[4], lost_rec_to_0=lost, wbc=best.x[1], h=best.x[2])
r = nm(lambda p: chi(1.0, p[3], p[0], p[1], p[2]), list(lc.x) + [0.02], S + [0.01], 400)
out["D1_F1"] = dict(delta=r.fun - lc.fun, G=r.x[3], lost_rec_to_0=E_decay(1.0, r.x[3], *r.x[:3])[1])
print(out["D1_free"], out["D1_F1"], flush=True)


out["D1_note"] = "Gamma in units of H0; F is the decaying fraction of CDM at early times."
json.dump(out, open(f"dark_decay_{ds}.json", "w"), indent=1, default=float)
print("done", flush=True)
