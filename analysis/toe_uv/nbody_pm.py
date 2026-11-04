"""A real N-body test of the sparse tower: a particle-mesh code with two species in a periodic box, on the relaxing radion's own background.
Uncoupled species: gravity from total density.  Coupled species, a fraction F of the mass at the start: gravity + scalar force 2 b^2 times gravity sourced by its own density only, mass m ~ exp(-b chi(a)), and momentum drift dp/da = +b chi_a p.  The field is homogeneous at this order: its local shift is b F Phi, about 1e-6, so the force is linear; there is no screening, and no finite range, as mu ~ 4 H0.
Units: H0 = 1, x in Mpc/h, p = a^2 dx/dt; dx/da = p/(a^3 E), dp/da = -grad Phi/(a E) + (coupled) b chi_a p, lap Phi = (3/2) drho/a, drho in units of the critical density today.  KDK leapfrog in ln a, CIC, spectral Poisson and gradient.
ICs: Zel'dovich from CLASS P_cb at z = 49, with the coupled species' overdensity scaled by the CLASS two-fluid ratio.  Same seed for every run, so ratios cancel sample variance.
Runs: control (b = 0 on the same E(a)) and coupled.  Controls: low-k growth against linear theory; the low-k ratio of the two species' amplitudes against CLASS (1.054 at k = 0.2/Mpc); P_tot of the control against CLASS halofit in shape.
Measures: P_total ratio, P_cc/P_uu, cross-correlation, coupled mass fraction inside dense peaks, peak counts by mass.
usage: py -3 nbody_pm.py ic.npz out.json Ng Npart box steps"""
import json
import math
import os
import sys
import time
import numpy as np

icf, outf, NG, NP, L, STEPS = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6])
ic = np.load(icf)
AI = 1 / 50.0
_o = np.argsort(ic["a"])  # the CLASS table runs from today backwards, and np.interp needs ascending a
Eg_a, Eg = ic["a"][_o], ic["E"][_o]
chi_a, chi = ic["a"][_o], ic["chi"][_o]
b0, F0, Om_cb = float(ic["b"]), float(ic["F"]), float(ic["Om_cb"])
if "B" in os.environ:  # keep f b, so the background is unchanged at this order
    _b = float(os.environ["B"])
    F0, b0 = F0 * b0 / _b, _b
ratio_i = float(ic["ratio_ai"])
E_of = lambda a: float(np.interp(a, Eg_a, Eg))
chi_of = lambda a: float(np.interp(a, chi_a, chi))
dchi = np.gradient(chi, chi_a)
dchi_of = lambda a: float(np.interp(a, chi_a, dchi))
dx = L / NG
kf = 2 * np.pi / L
k1 = np.fft.fftfreq(NG, 1 / NG) * kf
kz = np.fft.rfftfreq(NG, 1 / NG) * kf
KX, KY, KZ = np.meshgrid(k1, k1, kz, indexing="ij", sparse=True)
K2 = KX ** 2 + KY ** 2 + KZ ** 2
K2[0, 0, 0] = 1.0


def cic_deposit(x, w):
    g = x / dx
    i = np.floor(g).astype(np.int64)
    d = g - i
    i %= NG
    ip = (i + 1) % NG
    rho = np.zeros(NG ** 3)
    for ax, wx in ((i[:, 0], 1 - d[:, 0]), (ip[:, 0], d[:, 0])):
        for ay, wy in ((i[:, 1], 1 - d[:, 1]), (ip[:, 1], d[:, 1])):
            for az, wz in ((i[:, 2], 1 - d[:, 2]), (ip[:, 2], d[:, 2])):
                rho += np.bincount((ax * NG + ay) * NG + az, weights=w * wx * wy * wz, minlength=NG ** 3)
    return rho.reshape(NG, NG, NG)


def cic_interp(f, x):
    g = x / dx
    i = np.floor(g).astype(np.int64)
    d = g - i
    i %= NG
    ip = (i + 1) % NG
    v = np.zeros(len(x))
    for ax, wx in ((i[:, 0], 1 - d[:, 0]), (ip[:, 0], d[:, 0])):
        for ay, wy in ((i[:, 1], 1 - d[:, 1]), (ip[:, 1], d[:, 1])):
            for az, wz in ((i[:, 2], 1 - d[:, 2]), (ip[:, 2], d[:, 2])):
                v += f[ax, ay, az] * wx * wy * wz
    return v


def zeldovich():
    rng = np.random.default_rng(1234)
    gauss = rng.normal(size=(NP, NP, NP))
    dk = np.fft.rfftn(gauss)
    kf1 = np.fft.fftfreq(NP, 1 / NP) * kf
    kfz = np.fft.rfftfreq(NP, 1 / NP) * kf
    QX, QY, QZ = np.meshgrid(kf1, kf1, kfz, indexing="ij", sparse=True)
    Q2 = QX ** 2 + QY ** 2 + QZ ** 2
    Q2[0, 0, 0] = 1.0
    P = np.interp(np.log(np.sqrt(Q2)), np.log(ic["k"]), ic["P"], left=0, right=0)
    amp = np.sqrt(P / L ** 3) * NP ** 1.5 * float(os.environ.get("AMP", "1"))  # AMP << 1 keeps the whole run linear: a control against the linear equations
    dk = dk / NP ** 1.5 * amp
    dk[0, 0, 0] = 0
    psi = [np.fft.irfftn(1j * Qi / Q2 * dk, s=(NP, NP, NP), axes=(0, 1, 2)) * NP ** 1.5 for Qi in (QX, QY, QZ)]
    q = (np.indices((NP, NP, NP)).reshape(3, -1).T + 0.5) * (L / NP)
    return q, np.stack([p.ravel() for p in psi], axis=1)


def power(rho1, rho2=None):
    d1 = rho1 / rho1.mean() - 1
    F1 = np.fft.rfftn(d1)
    F2 = F1 if rho2 is None else np.fft.rfftn(rho2 / rho2.mean() - 1)
    p = (F1 * np.conj(F2)).real * L ** 3 / NG ** 6
    kk = np.sqrt(K2).ravel()
    edges = np.geomspace(kf, kf * NG / 2, 22)
    idx = np.digitize(kk, edges)
    wt = np.ones_like(kk) * 2
    wt[np.isclose(KZ.ravel() if False else (np.ones(K2.shape) * KZ).ravel(), 0)] = 1
    s = np.bincount(idx, weights=p.ravel() * wt, minlength=len(edges) + 1)
    n = np.bincount(idx, weights=wt, minlength=len(edges) + 1)
    k_ = np.bincount(idx, weights=kk * wt, minlength=len(edges) + 1)
    good = n[1:-1] > 0
    return (k_[1:-1][good] / n[1:-1][good]).tolist(), (s[1:-1][good] / n[1:-1][good]).tolist()


def run(b, label):
    t0 = time.time()
    q, psi = zeldovich()
    ai = AI
    # f = dlnD/dlna from the IC table
    fg = float(ic["f_growth"])
    Ei = E_of(ai)
    xu = (q + psi) % L
    xc = (q + ratio_i * psi) % L
    pu = ai ** 2 * Ei * fg * psi
    pc = ai ** 2 * Ei * fg * ratio_i * psi
    npart = len(q)
    F = F0
    Mu = Om_cb * (1 - F) * L ** 3 / npart / dx ** 3
    chi_i = chi_of(ai)
    lna = np.linspace(math.log(ai), 0.0, STEPS + 1)
    om_cb_i = Om_cb

    def forces(a, xu, xc):
        mc = Om_cb * F * L ** 3 / npart / dx ** 3 * math.exp(-b0 * (chi_of(a) - chi_i)) if b > 0 else Om_cb * F * L ** 3 / npart / dx ** 3
        ru = cic_deposit(xu, np.full(npart, Mu))
        rc = cic_deposit(xc, np.full(npart, mc))
        tot = ru + rc
        tk = np.fft.rfftn(tot - tot.mean())
        phi = -1.5 / a * tk / K2
        res = []
        gu = []
        for Ki in (KX, KY, KZ):
            gu.append(np.fft.irfftn(1j * Ki * phi, s=(NG, NG, NG), axes=(0, 1, 2)))
        if b > 0:
            ck = np.fft.rfftn(rc - rc.mean())
            phis = -1.5 / a * 2 * b * b * ck / K2
            gs = [np.fft.irfftn(1j * Ki * phis, s=(NG, NG, NG), axes=(0, 1, 2)) for Ki in (KX, KY, KZ)]
        else:
            gs = None
        au = np.stack([-cic_interp(g, xu) for g in gu], axis=1)
        ac = np.stack([-cic_interp(g, xc) for g in gu], axis=1)
        if gs is not None:
            ac += np.stack([-cic_interp(g, xc) for g in gs], axis=1)
        return au, ac

    au, ac = forces(ai, xu, xc)
    for s in range(STEPS):
        a0, a1 = math.exp(lna[s]), math.exp(lna[s + 1])
        am = math.exp(0.5 * (lna[s] + lna[s + 1]))
        dlna = lna[s + 1] - lna[s]
        # half kick: dp/dlna = -grad Phi / E + b chi_N p
        cN0 = dchi_of(a0) * a0 if b > 0 else 0.0
        pu += 0.5 * dlna * au / E_of(a0)
        pc += 0.5 * dlna * (ac / E_of(a0) + (b * cN0 * pc if b > 0 else 0.0))
        # drift: dx/dlna = p / (a^2 E)
        drift = dlna / (am ** 2 * E_of(am))
        xu = (xu + pu * drift) % L
        xc = (xc + pc * drift) % L
        au, ac = forces(a1, xu, xc)
        cN1 = dchi_of(a1) * a1 if b > 0 else 0.0
        pu += 0.5 * dlna * au / E_of(a1)
        pc += 0.5 * dlna * (ac / E_of(a1) + (b * cN1 * pc if b > 0 else 0.0))
        if s % 10 == 0:
            mc_ = Om_cb * F * L ** 3 / npart / dx ** 3
            ru_, rc_ = cic_deposit(xu, np.full(npart, Mu)), cic_deposit(xc, np.full(npart, mc_))
            k_, puu_ = power(ru_)
            _, pcc_ = power(rc_)
            print(label, s, round(a1, 4), round(time.time() - t0, 1), "amp ratio, lowest bins", np.round(np.sqrt(np.array(pcc_[:6]) / np.array(puu_[:6])), 4).tolist(), flush=True)
    mc = Om_cb * F * L ** 3 / npart / dx ** 3 * (math.exp(-b0 * (chi_of(1.0) - chi_i)) if b > 0 else 1.0)
    ru = cic_deposit(xu, np.full(npart, Mu))
    rc = cic_deposit(xc, np.full(npart, mc))
    return ru, rc, xu, xc


def peaks(tot, ru, rc):
    """local maxima of the total density smoothed over a cell, with coupled fraction in spheres of 1, 2, 4 cells"""
    from scipy.ndimage import maximum_filter, uniform_filter

    s = uniform_filter(tot, size=3, mode="wrap")
    m = (s == maximum_filter(s, size=5, mode="wrap")) & (s > 20 * tot.mean())
    idx = np.argwhere(m)
    Fg = rc.sum() / tot.sum()
    rows = []
    rad = {1: 1, 2: 2, 4: 4}
    grids = {}
    for r in rad:
        z = np.indices((2 * r + 1,) * 3) - r
        grids[r] = z[:, (z ** 2).sum(0) <= r * r]
    for p in idx:
        row = dict(height=float(s[tuple(p)] / tot.mean()))
        for r, g in grids.items():
            ii = (p[0] + g[0]) % NG, (p[1] + g[1]) % NG, (p[2] + g[2]) % NG
            mt = tot[ii].sum()
            row[f"F{r}"] = float(rc[ii].sum() / mt / Fg)
            row[f"M{r}"] = float(mt)
        rows.append(row)
    return rows, Fg


out = dict(Ng=NG, Np=NP, L=L, steps=STEPS, b=b0, F=F0, Om_cb=Om_cb, ratio_ai=ratio_i)
res = {}
for lab, b in (("control", 0.0), ("coupled", b0)):
    ru, rc, xu, xc = run(b, lab)
    k, Ptot = power(ru + rc)
    _, Puu = power(ru)
    _, Pcc = power(rc)
    _, Puc = power(ru, rc)
    rows, Fg = peaks(ru + rc, ru, rc)
    res[lab] = dict(k=k, Ptot=Ptot, Puu=Puu, Pcc=Pcc, Puc=Puc, npeaks=len(rows), Fglobal=Fg, peaks_M4=np.percentile([r["M4"] for r in rows], [50, 90, 99]).tolist() if rows else [], F1=np.median([r["F1"] for r in rows]) if rows else None, F2=np.median([r["F2"] for r in rows]) if rows else None, F4=np.median([r["F4"] for r in rows]) if rows else None)
    hb = [r for r in rows if r["height"] > np.percentile([q["height"] for q in rows], 90)]
    res[lab].update(F1_top=np.median([r["F1"] for r in hb]) if hb else None, F2_top=np.median([r["F2"] for r in hb]) if hb else None, F4_top=np.median([r["F4"] for r in hb]) if hb else None)
    out[lab] = res[lab]
    json.dump(out, open(outf, "w"), indent=1, default=float)
    print(lab, {a: res[lab][a] for a in ("npeaks", "Fglobal", "F1", "F2", "F4", "F1_top", "F2_top", "F4_top")}, flush=True)
    del ru, rc, xu, xc
c, m = res["control"], res["coupled"]
n = min(len(c["k"]), len(m["k"]))
print("k", np.round(c["k"][:n], 3).tolist())
lin = np.interp(np.log(c["k"][:n]), np.log(ic["P0k"]), ic["P0"])
nl = np.interp(np.log(c["k"][:n]), np.log(ic["P0k"]), ic["P0nl"])
print("control Ptot / CLASS linear", np.round(np.array(c["Ptot"][:n]) / lin, 3).tolist())
print("control Ptot / CLASS halofit", np.round(np.array(c["Ptot"][:n]) / nl, 3).tolist())
out["P_over_linear_control"] = (np.array(c["Ptot"][:n]) / lin).tolist()
out["P_over_halofit_control"] = (np.array(c["Ptot"][:n]) / nl).tolist()
out["P_ratio"] = (np.array(m["Ptot"][:n]) / np.array(c["Ptot"][:n])).tolist()
out["amp_ratio_coupled"] = np.sqrt(np.array(m["Pcc"][:n]) / np.array(m["Puu"][:n])).tolist()
out["amp_ratio_control"] = np.sqrt(np.array(c["Pcc"][:n]) / np.array(c["Puu"][:n])).tolist()
out["k_common"] = c["k"][:n]
out["class_ratio_0"] = float(ic["ratio_0"])
json.dump(out, open(outf, "w"), indent=1, default=float)
print("Ptot ratio", np.round(np.array(m["Ptot"][:n]) / np.array(c["Ptot"][:n]), 4).tolist())
print("sqrt(Pcc/Puu)", np.round(np.sqrt(np.array(m["Pcc"][:n]) / np.array(m["Puu"][:n])), 4).tolist())
print("control sqrt(Pcc/Puu)", np.round(np.sqrt(np.array(c["Pcc"][:n]) / np.array(c["Puu"][:n])), 4).tolist())
print("done", flush=True)
