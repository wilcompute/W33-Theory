"""Does a 7 percent coupled component survive in halos?  Two species in a self-similar secondary infall halo (Fillmore and Goldreich 1984, Bertschinger 1985), radial shells, Einstein-de Sitter units with G = 1.
Coupled shells feel  a = -[M_tot(<r) + 2 b^2 M_c(<r)] / r^2 - (b chi_dot) v, uncoupled shells a = -M_tot(<r)/r^2.  The scalar force is sourced only by the coupled species, so the danger is self-reinforcement: a coupled core that gets denser feels a stronger force.  The field is massless on halo scales, and its local shift is of order b f Phi, about 1e-6, so the force stays linear.  The drag term is dropped in the run labelled nofric and included otherwise, with chi_dot from chi_N = 2 f b per e-fold in matter domination.
Birth: mass M_i turns around at t_i with M = t^(2/3) and r_ta = t^(8/9) (delta_i ~ 1/M); both species share the same births, which is conservative for the coupled one since it should turn around slightly earlier.  Radial orbits reflect at a small core radius standing in for angular momentum.
Controls: b = 0 must give rho ~ r^(-9/4) in the infall regime and identical species; f = 0 with b large must leave the uncoupled species unchanged.  Reported at t_end: rho_c/rho_u against r/r_ta, the coupled mass fraction inside radii, apocentres relative to the uncoupled.
This is a toy: spherical, radial orbits, no baryons, no halo mergers.  It tests the self-reinforcement question, nothing finer.
usage: py -3 halo_shells.py"""
import json
import math
import numpy as np


def run(b, f, n=8000, t0=0.02, tend=40.0, rcore=0.002, steps=60000, fric=True):
    M_end = tend ** (2 / 3)
    # births uniform in mass between M(t0) and M(tend)
    Mb = np.linspace(t0 ** (2 / 3), M_end, n)
    tb = Mb ** 1.5
    rb = tb ** (8 / 9)
    dM = (M_end - t0 ** (2 / 3)) / n
    mu, mc = np.full(n, dM * (1 - f)), np.full(n, dM * f)
    r = np.r_[rb, rb].astype(float)
    v = np.zeros(2 * n)
    m = np.r_[mu, mc]
    coupled = np.r_[np.zeros(n, bool), np.ones(n, bool)]
    born = np.zeros(2 * n, bool)
    tbb = np.r_[tb, tb]
    rcmin = rcore * tend ** (8 / 9)
    t = t0
    lt = np.linspace(math.log(t0), math.log(tend), steps + 1)
    alpha = 2 * b * b
    for s in range(steps):
        t = math.exp(lt[s])
        dt = math.exp(lt[s + 1]) - t
        born = tbb <= t
        idx = np.where(born)[0]
        if len(idx) == 0:
            continue
        order = idx[np.argsort(r[idx])]
        Mt = np.cumsum(m[order])
        Mc = np.cumsum(m[order] * coupled[order])
        a = np.zeros(len(order))
        rr = r[order]
        a = -Mt / rr ** 2
        cp = coupled[order]
        a[cp] -= alpha * Mc[cp] / rr[cp] ** 2
        vv = v[order]
        if fric and b > 0:
            # chi_N = 2 f b in matter domination, so chi_dot = 2 f b H with H = 2/(3 t)
            a[cp] += b * (2 * f * b * 2 / (3 * t)) * vv[cp]
        vv = vv + a * dt
        rr = rr + vv * dt
        low = rr < rcmin
        rr[low] = 2 * rcmin - rr[low]
        vv[low] = np.abs(vv[low])
        r[order] = rr
        v[order] = vv
    rta = tend ** (8 / 9)
    edges = np.geomspace(0.004, 1.0, 26) * rta
    cen = np.sqrt(edges[1:] * edges[:-1])
    vol = 4 / 3 * np.pi * (edges[1:] ** 3 - edges[:-1] ** 3)
    ru, rc = r[:n], r[n:]
    hu = np.histogram(ru, edges)[0] * (1 - f) * dM / vol
    hc = np.histogram(rc, edges)[0] * f * dM / vol if f > 0 else np.zeros(25)
    res = dict(b=b, f=f, fric=fric, r_over_rta=(cen / rta).tolist(), rho_u=hu.tolist(), rho_c=hc.tolist())
    if f > 0:
        res["ratio_over_f"] = [float((c / (u + c)) / f) if (u + c) > 0 else None for u, c in zip(hu, hc)]
        res["f_inside"] = {str(x): float(f * (rc < x * rta).sum() / max(f * (rc < x * rta).sum() + (1 - f) * (ru < x * rta).sum(), 1e-30)) for x in (0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0)}
    tot = hu + hc
    sel = (cen / rta > 0.008) & (cen / rta < 0.1) & (tot > 0)
    res["slope_total"] = float(np.polyfit(np.log(cen[sel]), np.log(tot[sel]), 1)[0])
    if f > 0:
        sc = (cen / rta > 0.008) & (cen / rta < 0.1) & (hc > 0)
        res["slope_coupled"] = float(np.polyfit(np.log(cen[sc]), np.log(hc[sc]), 1)[0])
    return res


out = {}
for lab, b, f, fr in (("control_b0", 0.0, 0.0708, True), ("b707_f7", 0.7071, 0.0708, True), ("b707_f7_nofric", 0.7071, 0.0708, False), ("b1225_f4", 1.2247, 0.0408, True), ("b1225_f4_nofric", 1.2247, 0.0408, False), ("b707_f30", 0.7071, 0.3, True), ("b1225_f30", 1.2247, 0.3, True)):
    out[lab] = run(b, f, fric=fr)
    r = out[lab]
    print(lab, "slope total", round(r["slope_total"], 3), "slope coupled", round(r.get("slope_coupled", 0), 3), "f_inside/f", {k: round(v / f, 3) for k, v in r.get("f_inside", {}).items()}, flush=True)
    json.dump(out, open("halo_shells.json", "w"), indent=1, default=float)
# resolution control
out["control_b707_n16000"] = run(0.7071, 0.0708, n=16000, steps=100000)
r = out["control_b707_n16000"]
print("n16000", round(r["slope_total"], 3), {k: round(v / 0.0708, 3) for k, v in r["f_inside"].items()}, flush=True)
# analytic reference: a test particle with extra force fraction eps at fixed potential has its apocentre shrink
out["excess_force_on_coupled_tracing"] = {f"b{b}_f{f}": 2 * b * b * f for b, f in ((0.7071, 0.0708), (1.2247, 0.0408))}
json.dump(out, open("halo_shells.json", "w"), indent=1, default=float)
print("done", flush=True)
