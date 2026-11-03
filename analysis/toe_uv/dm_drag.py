"""Dark matter drags the moduli along grad ln m.  Two canonical fields, reduced Planck units: chi along grad ln m (|grad ln m| = b), phi orthogonal.
    m = m0 exp(-b chi),  V = V0 exp(-c phi - a chi) + (1/2) mu^2 (chi - eps phi)^2 [+ wall M exp(lam chi)]
Single-field fits read c' as the slope of ln m along the path, and arXiv:2507.03090 footnote 2 lets it be small because grad m and grad V need not align.  But in matter domination the force is rho_c grad ln m, not grad V: for light fields chi_N -> 2 b Omega_c whatever V does, so d ln m / dN = -2 b^2 Omega_c, and the data constrain b itself (the gradient norm in the light subspace), not a projection.
Geometry: m ~ m_KK has |grad ln m| = sqrt(3/2) with all moduli light, sqrt(n/(n+1)) >= 1/sqrt 2 at fixed volume; the sharpened distance conjecture demands >= 1/sqrt 2.
Part A control: b = c', a = c, V and m along the one field chi, must reproduce the single-field fit exactly.  Part B: light moduli, profile in b.  Part C: chi massive, valley chi = eps phi with b eps/sqrt(1+eps^2) = 0.05, scan mu/H0.  Part D: a fraction f of the dark matter couples.  Part E: a steep wall stops the drag.
Compressed CMB and background only.  usage: py -3 dm_drag.py dataset data_dir"""
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
fname = f"dm_drag_{ds}.json"


def solve(M, wb, wbc, h, want=False, rtol=1e-7):
    """M: dict b, c, a, mu, eps, f, lam, lnM.  wbc at recombination."""
    b, c, a, mu, eps, f = M["b"], M.get("c", 0.0), M.get("a", 0.0), M.get("mu", 0.0), M.get("eps", 0.0), M.get("f", 1.0)
    lam, wall = M.get("lam", 0.0), math.exp(M["lnM"]) if "lnM" in M else 0.0
    h2 = h * h
    orr, ob, onu = L.OMEGA_R_H2 / h2, wb / h2, L.OMEGA_NU_H2 / h2
    oc_rec = (wbc - wb) / h2
    mu2 = mu * mu / 3.0

    def state(N, s, lV, oci):
        chi, cN, phi, pN = s
        ea = math.exp(-3 * N)
        rc0 = oci * ea
        rcc = f * rc0 * math.exp(-b * chi)
        rc = (1 - f) * rc0 + rcc
        rb, rr = (ob + onu) * ea, orr * ea * math.exp(-N)
        V1 = math.exp(lV - c * phi - a * chi)
        dif = chi - eps * phi
        Vw = wall * math.exp(lam * chi) if wall else 0.0
        V = V1 + 0.5 * mu2 * dif * dif + Vw
        kin = cN * cN + pN * pN
        E2 = (rc + rb + rr + V) / (1 - kin / 6)
        return rc, rcc, rb, rr, V, V1, dif, Vw, kin, E2

    def run(lV, oci):
        def rhs(N, s):
            rc, rcc, rb, rr, V, V1, dif, Vw, kin, E2 = state(N, s, lV, oci)
            dlnH = -0.5 * (kin + 3 * (rc + rb + 4 / 3 * rr) / E2)
            Vchi = -a * V1 + mu2 * dif + lam * Vw
            Vphi = -c * V1 - eps * mu2 * dif
            return [s[1], -(3 + dlnH) * s[1] + 3 * (b * rcc - Vchi) / E2, s[3], -(3 + dlnH) * s[3] - 3 * Vphi / E2]
        return solve_ivp(rhs, (NI, 0), [0.0, 0.0, 0.0, 0.0], rtol=rtol, atol=1e-10, method="LSODA", dense_output=True)

    def e1(lV, oci):
        s = run(lV, oci)
        if not s.success:
            raise RuntimeError
        return state(0.0, s.y[:, -1], lV, oci)[-1] - 1, s

    oc_i = oc_rec
    lV = math.log(max(1 - (wbc + L.OMEGA_NU_H2) / h2, 0.05))
    for _ in range(3):
        for __ in range(10):
            d, s = e1(lV, oc_i)
            if abs(d) < 1e-6:
                break
            dd, _s = e1(lV + 1e-4, oc_i)
            lV -= d / ((dd - d) / 1e-4)
        chi_rec = float(s.sol(NREC)[0])
        new = oc_rec / ((1 - f) + f * math.exp(-b * chi_rec))
        if abs(new / oc_i - 1) < 1e-7:
            oc_i = new
            break
        oc_i = new
    d, s = e1(lV, oc_i)
    y = s.sol(NG)
    a3 = np.exp(-3 * NG)
    rc = oc_i * a3 * ((1 - f) + f * np.exp(-b * y[0]))
    dif = y[0] - eps * y[2]
    Vv = math.exp(lV) * np.exp(-c * y[2] - a * y[0]) + 0.5 * mu2 * dif * dif + (wall * np.exp(lam * y[0]) if wall else 0.0)
    E2 = (rc + (ob + onu) * a3 + orr * a3 * np.exp(-NG) + Vv) / (1 - (y[1] ** 2 + y[3] ** 2) / 6)
    E = np.sqrt(E2)[::-1]
    if want:
        chi_rec, phi_rec = s.sol(NREC)[0], s.sol(NREC)[2]
        path = float(np.trapezoid(np.sqrt(y[1] ** 2 + y[3] ** 2)[NG > NREC], NG[NG > NREC]))
        dchi = float(y[0][-1] - chi_rec)
        return E, dict(chi0=float(y[0][-1]), chi_rec=float(chi_rec), phi0=float(y[2][-1]), phi_rec=float(phi_rec), path_rec_to_0=path, dln_m_rec_to_0=-b * dchi, slope_along_path=(b * abs(dchi) / path if path > 0 else 0.0), chiN0=float(y[1][-1]), phiN0=float(y[3][-1]), Om0=float(rc[-1] + (ob + onu)))
    return E


def chi2(M, wb, wbc, h):
    try:
        return L.chi2(solve(M, wb, wbc, h), h, wb, wbc, sn)
    except Exception:
        return 1e8


def nm(fn, x0, steps, maxiter):
    x0 = np.asarray(x0, float)
    return minimize(fn, x0, method="Nelder-Mead", options=dict(xatol=3e-5, fatol=3e-3, maxiter=maxiter, maxfev=maxiter, initial_simplex=np.vstack([x0] + [x0 + np.eye(len(x0))[i] * steps[i] for i in range(len(x0))])))


S = [1e-4, 1e-3, 3e-3]
lc = nm(lambda p: L.chi2(L.E_lcdm(p[1], p[2]), p[2], p[0], p[1], sn), [0.02223, 0.142, 0.675], S, 800)
prev = json.load(open(f"fading_ds_{ds}.json"))
fn = prev["free_c_neg"]
cached = json.load(open(fname))
out = dict(dataset=ds, LCDM=lc.fun, single_field=dict(c=fn["c"], cp=fn["cp"], delta=fn["delta"]))


def save():
    json.dump(out, open(fname, "w"), indent=1, default=float)


x0 = [fn["wb"], fn["wbc"], fn["h"]]
# A control: the single-field model written as two fields, with the published (c, c')
ctl = chi2(dict(b=fn["cp"], a=fn["c"]), *x0)
out["control_two_field_vs_single"] = dict(two_field=ctl - lc.fun, single=fn["delta"])
E_, inf = solve(dict(b=fn["cp"], a=fn["c"]), *x0, want=True)
out["control_info"] = inf
print("control", out["control_two_field_vs_single"], inf, flush=True)
# control of the claim: light chi, chi_N in matter era must approach 2 b Omega_c
mm = dict(b=0.7071, c=0.8)
_, inf2 = solve(mm, *x0, want=True)
out["light_b0.707_info"] = inf2
save()

# B light moduli: profile in b, V slope free in both directions
out["light"] = {}
for b in (0.02, 0.05, 0.1, 0.2, 0.4082, 0.7071, 1.0, 1.2247):
    if str(b) in cached.get("light", {}):
        out["light"][str(b)] = cached["light"][str(b)]
        continue
    best = None
    for c0, a0 in ((fn["c"], 0.0), (0.7, 0.0), (0.7, -0.5)):
        r = nm(lambda p: chi2(dict(b=b, c=p[3], a=p[4]), p[0], p[1], p[2]), x0 + [c0, a0], S + [0.2, 0.2], 350)
        if best is None or r.fun < best.fun:
            best = r
    _, inf = solve(dict(b=b, c=best.x[3], a=best.x[4]), *best.x[:3], want=True)
    out["light"][str(b)] = dict(delta=best.fun - lc.fun, c=best.x[3], a=best.x[4], wbc=best.x[1], h=best.x[2], info=inf)
    print("light b", b, round(best.fun - lc.fun, 2), np.round(best.x[3:], 3), round(inf["slope_along_path"], 3), flush=True)
    save()

# C stabilised chi: valley with c' = 0.05 on it
out["massive"] = {}
for b in (0.7071,):
    eps = (0.05 / b) / math.sqrt(1 - (0.05 / b) ** 2)
    rows = {}
    for mu in (1.0, 10.0):  # above this the shooting fails: dm_drag_mod.py integrates the kick directly
        cval = fn["c"] / math.sqrt(1 + eps * eps) if False else fn["c"]
        if mu <= 300:
            r = nm(lambda p: chi2(dict(b=b, c=p[3], mu=mu, eps=eps), p[0], p[1], p[2]), x0 + [cval], S + [0.2], 220)
            rows[str(mu)] = dict(delta=r.fun - lc.fun, c=r.x[3], refit=True, x=list(r.x))
        else:
            # oscillations make each solve slow: local refit of (wbc, h) only
            r = nm(lambda p: chi2(dict(b=b, c=cval, mu=mu, eps=eps), x0[0], p[0], p[1]), x0[1:], S[1:], 40)
            rows[str(mu)] = dict(delta=r.fun - lc.fun, c=cval, refit=False, x=list(r.x))
        print("massive b", b, "mu", mu, round(rows[str(mu)]["delta"], 2), flush=True)
        out["massive"][str(b)] = dict(eps=eps, rows=rows)
        save()

# D only a fraction f couples: at fixed f b = c' the background must match the single-field fit
out["fraction"] = {}
for b, f in ((0.7071, fn["cp"] / 0.7071), (1.2247, fn["cp"] / 1.2247), (0.7071, 0.3), (1.2247, 0.3), (0.7071, 1.0)):
    r = nm(lambda p: chi2(dict(b=b, f=f, c=p[3]), p[0], p[1], p[2]), x0 + [fn["c"]], S + [0.2], 260)
    out["fraction"][f"{b}_{round(f, 4)}"] = dict(b=b, f=f, product=b * f, delta=r.fun - lc.fun, c=r.x[3])
    print("fraction", b, round(f, 4), round(r.fun - lc.fun, 2), flush=True)
    save()

# E a steep wall against the drag: V_wall = M exp(lam chi), which also gives a scaling attractor with chi_N = 3/lam
out["wall"] = {}
for b, lam in ((0.7071, 50.0), (0.7071, 200.0), (0.7071, 700.0)):
    try:
        M = dict(b=b, lam=lam, lnM=math.log(1e-6), c=fn["c"])
        r = nm(lambda p: chi2(dict(M, c=p[3]), p[0], p[1], p[2]), x0 + [fn["c"]], S + [0.2], 120)
        _, inf = solve(dict(M, c=r.x[3]), *r.x[:3], want=True)
        out["wall"][str(lam)] = dict(b=b, lam=lam, delta=r.fun - lc.fun, c=r.x[3], info=inf)
        print("wall", lam, round(r.fun - lc.fun, 2), inf["slope_along_path"], inf["dln_m_rec_to_0"], flush=True)
    except Exception as e:
        out["wall"][str(lam)] = dict(failed=str(e))
    save()
print("done", flush=True)
