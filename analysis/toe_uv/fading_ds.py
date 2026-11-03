"""Fading dark sector (Bedroya, Obied, Vafa, Wu, arXiv:2507.03090): V = V0 exp(-c phi), CDM mass m0 exp(-c' phi), reduced Planck units; phi = 0 at rest deep in the radiation era.
Background only, with the compressed CMB of dark_like.py: perturbations, which they include via CLASS, are not seen here, so a control against their Table I is required (values below).  omega_bc is taken at recombination.
Fits: free (c, c') on both signs of c; c' = 0 (uncoupled, must obey the dark_ceiling.py ceiling); c' capped; and the one-parameter Casimir line c = 4 c', where V ~ m_KK^4 with constant coefficient (the relation that motivates the dark dimension).
usage: py -3 fading_ds.py dataset data_dir"""
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
NGRID = np.log(1 / (1 + L.ZGRID))[::-1]


def solve(c, cp, wb, wbc, h, want=False):
    """wbc at recombination. Returns E on ZGRID, phi(N), phi'(N)."""
    h2 = h * h
    orr, ob, onu = L.OMEGA_R_H2 / h2, wb / h2, L.OMEGA_NU_H2 / h2
    oc_rec = (wbc - wb) / h2
    Nrec = -math.log(1090.0)
    oc_i = oc_rec

    def run(lV, oci):
        V0 = math.exp(lV)

        def rhs(N, s):
            phi, p = s
            ea = math.exp(-3 * N)
            rc = oci * ea * math.exp(-cp * phi)
            rb = (ob + onu) * ea
            rr = orr * ea * math.exp(-N)
            V = V0 * math.exp(-c * phi)
            E2 = (rc + rb + rr + V) / (1 - p * p / 6)
            dlnH = -0.5 * (p * p + 3 * (rc + rb + 4 / 3 * rr) / E2)
            return [p, -(3 + dlnH) * p + 3 * (c * V + cp * rc) / E2]

        return solve_ivp(rhs, (NI, 0), [0.0, 0.0], rtol=1e-8, atol=1e-11, method="LSODA", dense_output=True)

    def e1(lV, oci):
        s = run(lV, oci)
        if not s.success:
            raise RuntimeError
        phi, p = s.y[:, -1]
        return (oci * math.exp(-cp * phi) + ob + onu + orr + math.exp(lV) * math.exp(-c * phi)) / (1 - p * p / 6) - 1, s

    lV = math.log(max(1 - (wbc + L.OMEGA_NU_H2) / h2, 0.05))
    for _ in range(3):
        # fix oc_i so that CDM at recombination equals oc_rec
        for __ in range(14):
            d, s = e1(lV, oc_i)
            if abs(d) < 1e-7:
                break
            dd, _s = e1(lV + 1e-4, oc_i)
            slope = (dd - d) / 1e-4
            if slope == 0:
                raise RuntimeError
            lV -= d / slope
        phi_rec = float(s.sol(Nrec)[0])
        new = oc_rec * math.exp(cp * phi_rec)
        if abs(new / oc_i - 1) < 1e-8:
            oc_i = new
            break
        oc_i = new
    d, s = e1(lV, oc_i)
    phi, p = s.sol(NGRID)
    a3 = np.exp(-3 * NGRID)
    rc = oc_i * a3 * np.exp(-cp * phi)
    E2 = (rc + (ob + onu) * a3 + orr * a3 * np.exp(-NGRID) + math.exp(lV) * np.exp(-c * phi)) / (1 - p * p / 6)
    E = np.sqrt(E2)[::-1]
    if want:
        Vv = math.exp(lV) * np.exp(-c * phi)
        kin = E2 * p * p / 6
        w = (kin - Vv) / (kin + Vv)
        idx = {z: int(np.argmin(abs(NGRID + math.log(1 + z)))) for z in (0, 0.5, 1, 2, 1090)}
        return E, dict(phi0=float(phi[-1]), phip0=float(p[-1]), phi_rec=phi_rec, dln_mDM_rec_to_0=float(-cp * (phi[-1] - phi_rec)), Om0=float(rc[-1] + (ob + onu)), Ophi0=float(kin[-1] + Vv[-1]), resid=d, w_phi={str(z): float(w[i]) for z, i in idx.items() if z != 1090}, phi_at={str(z): float(phi[i]) for z, i in idx.items()}, phip_at={str(z): float(p[i]) for z, i in idx.items()})
    return E


def nm(fn, x0, steps=None, maxiter=500):
    opts = dict(xatol=3e-5, fatol=3e-3, maxiter=maxiter, maxfev=maxiter)
    if steps is not None:
        opts["initial_simplex"] = np.vstack([x0] + [x0 + np.eye(len(x0))[i] * steps[i] for i in range(len(x0))])
    return minimize(fn, np.asarray(x0, float), method="Nelder-Mead", options=opts)


def like(c, cp, wb, wbc, h):
    try:
        return L.chi2(solve(c, cp, wb, wbc, h), h, wb, wbc, sn)
    except Exception:
        return 1e8


out = dict(dataset=ds)
lc = nm(lambda p: L.chi2(L.E_lcdm(p[1], p[2]), p[2], p[0], p[1], sn), [0.02223, 0.142, 0.675], [1e-4, 1e-3, 3e-3], 800)
out["LCDM"] = dict(chi2=lc.fun, x=list(lc.x))
ctrl = like(0.0, 0.0, *lc.x)
out["solver_control_LCDM"] = ctrl - lc.fun
print("LCDM", lc.fun, lc.x, "solver at c=c'=0 differs by", ctrl - lc.fun, flush=True)
S = [1e-4, 1e-3, 3e-3]


def rec(r, c, cp):
    E, info = solve(c, cp, *r.x[:3], want=True)
    return dict(c=c, cp=cp, chi2=r.fun, delta=r.fun - lc.fun, wb=r.x[0], wbc=r.x[1], h=r.x[2], info=info, parts=L.chi2(E, r.x[2], r.x[0], r.x[1], sn, parts=True))


def write():
    json.dump(out, open(f"fading_ds_{ds}.json", "w"), indent=1, default=float)


# free (c, c') on each sign
for label, c0, sc in (("free_c_neg", -0.9, 0.2), ("free_c_pos", 0.7, 0.2)):
    r = None
    for cp0 in (0.05, 0.02):
        t = nm(lambda p: like(p[3], p[4], p[0], p[1], p[2]) if p[3] * c0 > 0 and p[4] >= 0 else 1e8, list(lc.x) + [c0, cp0], S + [sc, 0.02], 700)
        if r is None or t.fun < r.fun:
            r = t
    out[label] = rec(r, float(r.x[3]), float(r.x[4]))
    print(label, {k: round(v, 4) for k, v in out[label].items() if isinstance(v, float)}, out[label]["info"]["dln_mDM_rec_to_0"], flush=True)
    write()
# c' profile at free c, each sign
out["cp_profile"] = []
for cp in (0.0, 0.0123, 0.02, 0.03, 0.05, 0.07, 0.1, 0.2, 0.7071):
    for sign, c0 in ((-1, out["free_c_neg"]["c"]), (1, out["free_c_pos"]["c"])):
        r = nm(lambda p: like(p[3], cp, p[0], p[1], p[2]) if p[3] * sign >= 0 else 1e8, [out["free_c_pos"]["wb"], out["free_c_pos"]["wbc"], out["free_c_pos"]["h"], c0], S + [0.2], 450)
        out["cp_profile"].append(rec(r, float(r.x[3]), cp) | dict(sign=sign))
        print("cp", cp, "sign", sign, "c", round(float(r.x[3]), 3), "delta", round(r.fun - lc.fun, 3), flush=True)
    write()
# Casimir line c = r c'
out["ratio_lines"] = {}
for ratio in (4.0, 2.0, 8.0):
    rows = []
    for cp0 in (0.02, 0.05, 0.1, 0.2):
        r = nm(lambda p: like(ratio * p[3], p[3], p[0], p[1], p[2]) if p[3] >= 0 else 1e8, list(lc.x) + [cp0], S + [0.02], 450)
        rows.append(rec(r, ratio * float(r.x[3]), float(r.x[3])))
    best = min(rows, key=lambda x: x["chi2"])
    out["ratio_lines"][str(ratio)] = best
    print("ratio", ratio, {k: round(best[k], 4) for k in ("c", "cp", "delta")}, flush=True)
    write()
print("done", flush=True)
