"""Lambda + the Casimir energy of gravitons and N_f massive bulk Dirac fermions + sparse tower.  The window of dd_massive_fermions.py (N_f = 2, M R = 0.5 to 3) removes AdS3 and keeps the sign negative today, and it changes the potential: at fixed M,
    V_C(chi) = Z x^-4 (-5 + 4 N_f C(2 pi x)) / (x0^-4 |...|), x = M R = x_0 exp(b (chi - chi_0))
is positive at small x, so it has a minimum rather than running to minus infinity.  So the exponent is no longer free or 4: it follows from M.  Parameters: Z sets eps, x_0 is on a grid, prod = f b as before.
Fits (compressed CMB, background) at each x_0 with N_f = 2, then the future from the same state: does the field settle in the minimum, is V there positive, does expansion turn around?  Control: x_0 large (fermions decoupled) must return the n = 4 model of casimir_fits.py.  Control: the minimum location from a direct scan.
usage: py -3 casimir_massive.py dataset data_dir"""
import json
import math
import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize, brentq
from scipy.special import kv, zeta
import dark_like as L

ds, dd = sys.argv[1], sys.argv[2]
sn = L.load_sn(ds, dd)
NI = -12.0
NG = np.log(1 / (1 + L.ZGRID))[::-1]
NREC = -math.log(1090.0)
MASK = NG >= NI
NEFF = 2


def C_ratio(x):
    if x < 1e-6:
        return 1.0
    s = 0.0
    for w in range(1, 60):
        s += w ** -2.5 * kv(2.5, w * x)
        if w * x > 60:
            break
    return 2 * (4 * math.pi) ** -2.5 * (2 * x) ** 2.5 * s / (3 * zeta(5) / (4 * math.pi ** 2))


lx = np.linspace(math.log(0.005), math.log(60.0), 900)
hv = np.array([math.exp(-4 * u) * (-5 + 4 * NEFF * C_ratio(2 * math.pi * math.exp(u))) for u in lx])
# V_C as a function of u = ln x; scaled by exp(4 u) inside the spline for accuracy
gv = np.array([(-5 + 4 * NEFF * C_ratio(2 * math.pi * math.exp(u))) for u in lx])
G = CubicSpline(lx, gv)
dG = G.derivative()


def Vc_over_h(u):
    return math.exp(-4 * u) * float(G(u))


def dVc_du(u):
    return math.exp(-4 * u) * (float(dG(u)) - 4 * float(G(u)))


umin = brentq(dVc_du, math.log(0.05), math.log(5.0))
xmin = math.exp(umin)
xzero = math.exp(brentq(lambda u: float(G(u)), math.log(0.05), math.log(5.0)))
print("x at V_C = 0", xzero, "x at the minimum", xmin, "h(xmin)", Vc_over_h(umin), flush=True)


def solve(b, prod, x_i, Zn, wb, wbc, h, want=False):
    """x_i = M R at chi = 0; V_C = Zn * h(u) with u = ln x_i + b chi; Zn > 0 and h < 0 where negative."""
    f = prod / b
    h2 = h * h
    orr, ob, onu = L.OMEGA_R_H2 / h2, wb / h2, L.OMEGA_NU_H2 / h2
    oc_rec = (wbc - wb) / h2
    obn = ob + onu
    lu = math.log(x_i)

    def mk(ol, oci):
        fo, uo = f * oci, (1 - f) * oci + obn

        def rhs(N, y):
            chi, x = y
            ea = math.exp(-3 * N)
            rcc = fo * ea * math.exp(-b * chi)
            rr = orr * ea * math.exp(-N)
            u = lu + b * chi
            Vc = Zn * Vc_over_h(u)
            E2 = (rcc + uo * ea + rr + ol + Vc) / (1 - x * x / 6)
            if not (x * x < 5.9 and E2 > 0):
                raise RuntimeError("left the domain")
            dl = -0.5 * (x * x + 3 * (rcc + uo * ea + 4 / 3 * rr) / E2)
            return [x, -(3 + dl) * x + 3 * (b * rcc - Zn * b * dVc_du(u)) / E2]

        return rhs, fo, uo

    oci = oc_rec
    ol = 1 - (wbc + L.OMEGA_NU_H2) / h2
    closed = False
    for _ in range(40):
        rhs, fo, uo = mk(ol, oci)
        s = solve_ivp(rhs, (NI, 0.0), [0.0, 0.0], rtol=1e-8, atol=1e-11, method="LSODA")
        if not s.success:
            raise RuntimeError
        chi_end, x_end = s.y[:, -1]
        rc0 = oci * ((1 - f) + f * math.exp(-b * chi_end))
        E0 = (rc0 + obn + orr + ol + Zn * Vc_over_h(lu + b * chi_end)) / (1 - x_end * x_end / 6)
        chi_rec = float(np.interp(NREC, s.t, s.y[0]))
        oci2 = oc_rec / ((1 - f) + f * math.exp(-b * chi_rec))
        if abs(E0 - 1) < 2e-6 and abs(oci2 / oci - 1) < 1e-6:
            closed = True
            break
        ol += 1 - E0
        oci = oci2
    if not closed:
        raise RuntimeError("budget")
    rhs, fo, uo = mk(ol, oci)
    s = solve_ivp(rhs, (NI, 0.0), [0.0, 0.0], rtol=1e-7, atol=1e-10, method="LSODA", t_eval=NG[MASK])
    chi = np.zeros_like(NG)
    xx = np.zeros_like(NG)
    chi[MASK], xx[MASK] = s.y
    a3 = np.exp(-3 * NG)
    Vcv = np.array([Zn * Vc_over_h(lu + b * c) for c in chi])
    E2 = (fo * a3 * np.exp(-b * chi) + uo * a3 + orr * a3 * np.exp(-NG) + ol + Vcv) / (1 - xx ** 2 / 6)
    E = np.sqrt(E2)[::-1]
    if want:
        return E, dict(ol=ol, oci=oci, chi0=float(chi[-1]), chiN0=float(xx[-1]), x0=math.exp(lu + b * chi[-1]), eps=float(Vcv[-1]), f=f, fo=fo, uo=uo, dlnm=float(-b * (chi[-1] - chi_rec)))
    return E


def future(b, prod, x_i, Zn, wb, wbc, h):
    E, i = solve(b, prod, x_i, Zn, wb, wbc, h, want=True)
    lu = math.log(x_i)
    ol, chi0, x0 = i["ol"], i["chi0"], i["chiN0"]
    h2 = h * h
    orr = L.OMEGA_R_H2 / h2
    fo, uo = i["fo"], i["uo"]

    def rhs(t, y):
        la, chi, cd, H = y
        a3 = math.exp(-3 * la)
        rc = fo * a3 * math.exp(-b * chi)
        rm = uo * a3
        rr = orr * a3 * math.exp(-la)
        cdd = -3 * H * cd + 3 * (b * rc - Zn * b * dVc_du(lu + b * chi))
        return [H, cd, cdd, -0.5 * (cd * cd + 3 * (rm + rc + 4 / 3 * rr))]

    def turn(t, y):
        return y[3]

    turn.terminal = True
    turn.direction = -1
    s = solve_ivp(rhs, (0, 60.0), [0.0, chi0, x0, 1.0], rtol=1e-9, atol=1e-11, method="LSODA", events=[turn])
    tH = float(s.t_events[0][0]) if len(s.t_events[0]) else None
    Vmin = ol + Zn * Vc_over_h(umin)
    return dict(t_turnaround_Gyr=None if tH is None else tH * 977.8 / (100 * h), V_at_minimum_over_crit=Vmin, V_today=ol + i["eps"], Lambda_over_crit=ol, x_final=math.exp(lu + b * s.y[1, -1]), N_end=float(s.y[0, -1]), t_end=float(s.t[-1]))


def X(b, prod, x_i, Zn, wb, wbc, h):
    if not (0 < prod <= b) or Zn <= 0:
        return 1e8
    try:
        return L.chi2(solve(b, prod, x_i, Zn, wb, wbc, h), h, wb, wbc, sn)
    except Exception:
        return 1e8


def nm(fn, x0, steps, maxiter):
    x0 = np.asarray(x0, float)
    return minimize(fn, x0, method="Nelder-Mead", options=dict(xatol=3e-5, fatol=3e-3, maxiter=maxiter, maxfev=maxiter, initial_simplex=np.vstack([x0] + [x0 + np.eye(len(x0))[i] * steps[i] for i in range(len(x0))])))


S = [1e-4, 1e-3, 3e-3]
lc = nm(lambda p: L.chi2(L.E_lcdm(p[1], p[2]), p[2], p[0], p[1], sn), [0.02223, 0.142, 0.675], S, 800)
fit4 = json.load(open(f"casimir_fits_{ds}.json"))["best"]["0.7071_-1"]
out = dict(dataset=ds, LCDM=lc.fun, n4_delta=fit4["delta"], xmin=xmin, xzero=xzero, h_min=Vc_over_h(umin), rows={})
b = 0.7071
XS = (0.40, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.85, 1.0, 1.5, 2.0, 3.0, 8.0)
for x_target in XS:
    # x at chi = 0 from the n = 4 chi_0, then refined by the fit through Zn
    x_i = x_target * math.exp(-b * fit4["info"]["chi0"])
    # Zn from eps at x_target
    h0 = Vc_over_h(math.log(x_target))
    if h0 >= 0:
        out["rows"][str(x_target)] = dict(skipped="V_C is not negative today at this x")
        print(x_target, "skip", flush=True)
        continue
    Zn0 = fit4["eps"] / h0
    r = nm(lambda p: X(b, p[3], x_i, p[4], p[0], p[1], p[2]), [fit4["wb"], fit4["wbc"], fit4["h"], fit4["prod"], Zn0], S + [0.006, 0.08 * Zn0], 450)
    try:
        E, inf = solve(b, r.x[3], x_i, r.x[4], *r.x[:3], want=True)
        fu = future(b, r.x[3], x_i, r.x[4], *r.x[:3])
        rho = 3 * (100 * r.x[2] * 1000 / 3.085677581491367e22 * 6.582119569e-16) ** 2 * (2.435e27) ** 2
        lk = 2 * math.pi
        # |V_C| = (1/2)(3 zeta(5)/(4 pi^2 (2 pi R)^4)) |net|, interval convention of dd_massive_fermions.py
        net = -5 + 4 * NEFF * C_ratio(2 * math.pi * inf["x0"])
        Rm = (0.5 * abs(net) * 3 * 1.0369277551433699 / (4 * math.pi ** 2 * lk ** 4) / (abs(inf["eps"]) * rho)) ** 0.25 * 0.1973269804
        rowd = dict(delta=r.fun - lc.fun, wb=r.x[0], wbc=r.x[1], h=r.x[2], chi0=inf["chi0"], prod=r.x[3], Zn=r.x[4], x0=inf["x0"], eps=inf["eps"], dlnm=inf["dlnm"], R_micron=Rm, M_eV=inf["x0"] * 0.1973269804 / Rm, future=fu)
    except Exception as e:
        rowd = dict(delta=r.fun - lc.fun, failed=str(e))
    out["rows"][str(x_target)] = rowd
    print(x_target, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in rowd.items()}, flush=True)
    json.dump(out, open(f"casimir_massive_fine_{ds}.json", "w"), indent=1, default=float)
print("done", flush=True)
