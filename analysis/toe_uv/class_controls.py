"""Controls for class_fading_patch.py, before any fit is believed.
1 plik-lite port against planck-lite-py's own reference value.  2 scf with lambda = c' = 0 against native Lambda.  3 background against fading_ds.solve (an independent solver).
4 Einstein trace equation: the numerical derivative of h' (from the energy constraint) must equal h'' (from total pressure) when c' != 0, which needs energy-momentum conservation; two sabotaged builds must fail it.
5 growth at k = 0.2/Mpc against the analytic G_eff = 1 + 2 c'^2 ODE with friction -c' phi_N; G_eff = 1 must fail.
6 Planck-only LCDM best fit against the published plik-lite values.
usage: python3 class_controls.py"""
import json
import os
import sys
import numpy as np
from scipy.integrate import solve_ivp
import class_cmb as C

out = {}
HOME = C.HOME
SAVE = "class_controls.json"
# 1 port
pl = C.Planck()
ls, tt, te, ee = np.genfromtxt(HOME + "/planck-lite-py/data/Dl_planck2015fit.dat", unpack=True)
l0 = int(ls[0])
mk = lambda d: np.r_[np.zeros(l0), d / (ls * (ls + 1) / (2 * np.pi))]
r = pl.resid(dict(tt=mk(tt), te=mk(te), ee=mk(ee)), 1.0)
out["port"] = dict(chi2=float(r @ r), expected=2 * 293.95586501795134)
print("port", out["port"], flush=True)
P0 = dict(C.START, c=0.0, cp=0.0)
# 2 Lambda limit
c1 = C.run_class(P0)
c2 = C.run_class(P0, kind="lcdm")
sel = np.arange(30, 2500)
ra, rb = pl.resid(c1[0], 1.0), pl.resid(c2[0], 1.0)
out["lambda_limit"] = dict(max_frac_tt=float(np.max(abs(c1[0]["tt"][sel] / c2[0]["tt"][sel] - 1))), dchi2=float(ra @ ra - rb @ rb), rd=[c1[4]["rd"], c2[4]["rd"]], s8=[c1[4]["s8"], c2[4]["s8"]])
print("lambda", out["lambda_limit"], flush=True)
# 3 background against the independent solver
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fading_ds.py"), encoding="utf-8").read().split("out = dict(dataset=ds)")[0]
sys.argv = ["x", "none", C.SND]
ns = {}
exec(src, ns)
pf = dict(P0, c=-0.85, cp=0.05)
kp = {}
cf = C.run_class(pf, keep=kp)
h = pf["h"]
wc_rec = pf["wc"] * np.exp(-pf["cp"] * cf[4]["phi_rec"])
kl = {}
C.run_class(dict(P0, wc=wc_rec), keep=kl)
E, inf = ns["solve"](pf["c"], pf["cp"], pf["wb"], wc_rec + pf["wb"], h, want=True)
El = C.L.E_lcdm(wc_rec + pf["wb"], h)
zz = np.array([0.0, 0.3, 0.7, 1.0, 2.0])
rat_py = np.interp(zz, C.L.ZGRID, E / El)
rat_cl = np.interp(zz, kp["z"], kp["H"]) / np.interp(zz, kl["z"], kl["H"])
out["background"] = dict(phi0_class=cf[4]["phi0"], phi0_py=inf["phi0"], phi_rec_class=cf[4]["phi_rec"], phi_rec_py=inf["phi_rec"], Hratio_class=rat_cl.tolist(), Hratio_py=rat_py.tolist())
print("bg", out["background"], flush=True)


def pert(path):
    d = np.loadtxt(path)
    return d, C.titles(path)


# 4 trace equation
def trace_test(binp, label, cp=0.3):
    res = {}
    kp = {}
    C.run_class(dict(P0, c=0.5, cp=cp), binp=binp, keep=kp, extra="k_output_values=0.01,0.1")
    for i, k in enumerate((0.01, 0.1)):
        d, names = pert(f"{kp['tag']}/o_perturbations_k{i}_s.dat")
        tau, a, hp, hpp = d[:, names.index("tau [Mpc]")], d[:, names.index("a")], d[:, names.index("h_prime")], d[:, names.index("h_prime_prime")]
        m = a > 0.02
        num = np.gradient(hp[m], tau[m])
        e = np.abs(num[3:-3] - hpp[m][3:-3]) / np.abs(hpp[m][3:-3]).max()
        res[str(k)] = float(np.max(e[a[m][3:-3] > 0.1]))  # the neutrino approximation switch below a = 0.1 gives an isolated spike at c' = 0 too
    print("trace", label, res, flush=True)
    return res


out["trace"] = dict(patched=trace_test(C.CLASSBIN, "patched"), c0_patched=trace_test(C.CLASSBIN, "c'=0", cp=0.0))
for lab, bin_ in (("sabotage_kg_sign", HOME + "/class_sab1/class"), ("sabotage_theta_sign", HOME + "/class_sab2/class")):
    out["trace"][lab] = trace_test(bin_, lab)
json.dump(out, open(SAVE, "w"), indent=1, default=float)


# 5 growth with the fifth force
def growth(cp, k=0.2, binp=C.CLASSBIN):
    kp = {}
    C.run_class(dict(P0, c=0.5, cp=cp), binp=binp, keep=kp, extra=f"k_output_values={k}")
    d, names = pert(f"{kp['tag']}/o_perturbations_k0_s.dat")
    a = d[:, names.index("a")]
    dc, db = d[:, names.index("delta_cdm")], d[:, names.index("delta_b")]
    N = np.log(a)
    bc = kp["cols"]
    raw = kp["raw"]
    NB = -np.log(1 + raw[:, bc.index("z")])
    Hb = raw[:, bc.index("H [1/Mpc]")]
    phi = raw[:, bc.index("phi_scf")]
    crit = raw[:, bc.index("(.)rho_crit")]
    Oc, Ob = raw[:, bc.index("(.)rho_cdm")] / crit, raw[:, bc.index("(.)rho_b")] / crit
    phiN = np.gradient(phi, NB)
    dlnH = np.gradient(np.log(Hb), NB)
    Ni, Nf = np.log(0.02), -1e-6
    y0 = [np.interp(Ni, N, dc), np.interp(Ni, N, np.gradient(dc, N)), np.interp(Ni, N, db), np.interp(Ni, N, np.gradient(db, N))]
    res = {}
    for lab, G in (("Geff", 1 + 2 * cp ** 2), ("G1", 1.0)):
        def rhs(n, y):
            oc, ob, pn, dh = (np.interp(n, NB, x) for x in (Oc, Ob, phiN, dlnH))
            return [y[1], -(2 + dh - cp * pn) * y[1] + 1.5 * (G * oc * y[0] + ob * y[2]), y[3], -(2 + dh) * y[3] + 1.5 * (oc * y[0] + ob * y[2])]
        s = solve_ivp(rhs, (Ni, Nf), y0, rtol=1e-7, atol=1e-10)
        res[lab] = float(s.y[0, -1] / np.interp(Nf, N, dc) - 1)
    res["growth_class"] = float(np.interp(Nf, N, dc) / y0[0])
    return res


out["growth"] = {str(cp): growth(cp) for cp in (0.0, 0.1, 0.3)}
out["growth"]["sabotage_theta_sign_0.3"] = growth(0.3, binp=HOME + "/class_sab2/class")
print("growth", out["growth"], flush=True)
# noise: chi2 must be smooth in h, and scf with lambda = 0 must equal native Lambda, near the Planck best fit
bf = dict(wb=0.02238, wc=0.11984, h=0.6743, lnA=3.0503, ns=0.96535, tau=0.0576, A=1.0005, c=0.0, cp=0.0)


def X(p, kind="fading"):
    r_ = pl.resid(C.run_class(p, kind)[0], p["A"])
    return float(r_ @ r_)


x0 = X(bf)
out["noise"] = dict(scf=x0, native=X(bf, "lcdm"), h_steps={str(e): X(dict(bf, h=bf["h"] + e)) - x0 for e in (-5e-5, -2e-5, -1e-5, 1e-5, 2e-5, 5e-5)})
print("noise", out["noise"], flush=True)
json.dump(out, open(SAVE, "w"), indent=1, default=float)

# 6 Planck-only LCDM
F = C.Fitter("none", use_bao=False)
b = F.fit(P0, C.NAMES)
out["planck_lcdm"] = b
print("planck", b, flush=True)
json.dump(out, open(SAVE, "w"), indent=1, default=float)
print("done", flush=True)
