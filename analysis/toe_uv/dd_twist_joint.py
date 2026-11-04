"""The twist omega is a modulus unless fixed discretely.  casimir_sugra.py set omega = 1/2 by hand.  Test the joint vacuum of radius and twist.
V(x, omega) proportional to x^-4 net(x, omega), net = -8 S(omega, 0) + 4 N_H S(omega, x), S(omega, x) = sum_w (1 - cos 2 pi w omega) G_w(2 pi x) / zeta(5), G_w(y) = exp(-z)(z^2 + 3z + 3)/(3 w^5), z = w y.  x = M R at fixed M.
Everything vanishes at omega = 0, where supersymmetry is restored at this order: V = 0 for all x.  So a vacuum with V < 0 competes with that flat direction, and with the positive uplift that sets today's dark energy the question is which point is a local minimum.
For each N_H: (1) at omega = 1/2, x_min from the radion condition; (2) the Hessian in (ln x, omega) there; (3) a brute minimum of V over the grid in (x, omega).  Control: at N_H = 0, omega = 1/2 is the minimum at every x, known for gravity alone, and the omega derivative at 1/2 is zero by the symmetry omega -> 1 - omega.
No uplift, no Kahler metric: the Hessian sign in omega does not depend on the field normalisation, the mass does.
usage: py -3 dd_twist_joint.py"""
import json
import numpy as np
from scipy.optimize import brentq
from scipy.special import zeta

W = np.arange(1, 400)
Z5 = float(zeta(5))


def G(x):
    z = W * 2 * np.pi * x
    return np.exp(-np.minimum(z, 700)) * (z * z + 3 * z + 3) / (3 * W ** 5.0)


def S(om, x):
    return float(np.sum((1 - np.cos(2 * np.pi * W * om)) * G(x))) / Z5


def net(x, om, nh):
    return -8 * S(om, 0.0) + 4 * nh * S(om, x)


def lnV(u, om, nh):
    x = np.exp(u)
    return x ** -4 * net(x, om, nh)


def xmin_half(nh):
    f = lambda u: (lnV(u + 1e-4, 0.5, nh) - lnV(u - 1e-4, 0.5, nh)) / 2e-4
    us = np.linspace(np.log(0.03), np.log(5), 500)
    fs = [f(u) for u in us]
    for a, b, fa, fb in zip(us[:-1], us[1:], fs[:-1], fs[1:]):
        if fa < 0 < fb:
            return float(np.exp(brentq(f, a, b)))
    return None


def hess(u, om, nh, du=2e-3, dw=2e-3):
    V = lambda a, b: lnV(a, b, nh)
    uu = (V(u + du, om) - 2 * V(u, om) + V(u - du, om)) / du ** 2
    ww = (V(u, om + dw) - 2 * V(u, om) + V(u, om - dw)) / dw ** 2
    uw = (V(u + du, om + dw) - V(u + du, om - dw) - V(u - du, om + dw) + V(u - du, om - dw)) / (4 * du * dw)
    return np.array([[uu, uw], [uw, ww]])


out = dict(rows={})
# control: gravity alone
oms = np.linspace(0, 1, 401)
c0 = [oms[int(np.argmin([net(x, o, 0) for o in oms]))] for x in (0.3, 1.0, 3.0)]
out["control_NH0_omega_min"] = [float(c) for c in c0]
print("control N_H=0 omega at minimum", c0, flush=True)
for nh in (3, 4, 6, 8):
    xm = xmin_half(nh)
    row = dict(xmin=xm)
    if xm:
        u = np.log(xm)
        H = hess(u, 0.5, nh)
        row.update(V_at_min=lnV(u, 0.5, nh), net_at_min=net(xm, 0.5, nh), H=H.tolist(), eig=np.linalg.eigvalsh(H).tolist(), dVdom=(lnV(u, 0.51, nh) - lnV(u, 0.49, nh)) / 0.02)
    # omega scan at several x: where is the minimum in omega, at this radius?
    scan = {}
    for x in (0.3, 0.4, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0):
        vals = [net(x, o, nh) for o in oms[:201]]
        i = int(np.argmin(vals))
        scan[str(x)] = dict(omega=float(oms[i]), net=float(vals[i]), net_half=float(net(x, 0.5, nh)))
    row["omega_scan"] = scan
    # brute grid: lowest V, and every local minimum
    us = np.linspace(np.log(0.05), np.log(6), 140)
    om2 = np.linspace(0, 0.5, 101)
    M = np.array([[lnV(a, b, nh) for b in om2] for a in us])
    lm = []
    for i in range(1, len(us) - 1):
        for j in range(1, len(om2)):
            nb = [M[i - 1, j], M[i + 1, j], M[i, j - 1], M[i, j + 1] if j + 1 < len(om2) else M[i, j - 1]]
            if M[i, j] < min(nb):
                lm.append(dict(x=float(np.exp(us[i])), omega=float(om2[j]), V=float(M[i, j])))
    row["local_minima"] = lm
    i, j = np.unravel_index(np.argmin(M), M.shape)
    row["grid_lowest"] = dict(x=float(np.exp(us[i])), omega=float(om2[j]), V=float(M[i, j]))
    out["rows"][str(nh)] = row
    print(nh, {k: v for k, v in row.items() if k != "omega_scan"}, flush=True)
    print("   scan", {k: (round(v["omega"], 3), round(v["net"], 3), round(v["net_half"], 3)) for k, v in scan.items()}, flush=True)
json.dump(out, open("dd_twist_joint.json", "w"), indent=1, default=float)
print("done", flush=True)
