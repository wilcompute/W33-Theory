"""Boltzmann solution for the coupled sterile-neutrino candidate (replaces the order-one estimates of Pass 12628 addenda 2-4).
Fields: real singlet S (mass m_S, vev v_S, portal (lambda/2) S^2 |H|^2), Majorana N with (y/2) S N N, M_N = y v_S / sqrt2.
x = m_S/T, H(x) = H_m / x^2, s = (2 pi^2/45) g* T^3, Y = n/s, <gamma> = K1/K2 (time dilation), Y_eq = (45/(4 pi^4)) (1/g*) x^2 K2(x):
  dY_S/dx = -[Gamma_hh <gamma> (Y_S - Y_eq) + Gamma_NN <gamma> Y_S] / (H x) - s <sigma v> (Y_S^2 - Y_eq^2) / (H x)
  dY_N/dx = 2 Gamma_NN <gamma> Y_S / (H x)
Gamma_NN = y^2 m_S/(16 pi); Gamma_hh = lambda^2 v_S^2/(8 pi m_S) (four Higgs-doublet states, rough); <sigma v>(SS -> HH) = lambda^2 / (16 pi (4 m_S^2 + 9 T^2)) (rough interpolation between the relativistic and non-relativistic regimes).
Two initial conditions at x = 0.05: Y_S = Y_eq (thermal) and Y_S = 0 (built up by the portal).  For each (M_N, m_S, lambda), v_S is solved so that Omega_N h^2 = 0.12; the point is viable if lambda <= lambda_max(v_S) (clocks, 2 sigma mu-dot 7e-17/yr: Lange et al. 2021) and M_N >= 15.8 keV (Lyman-alpha, rms match, Pass 12628 addendum 3).
The momentum (Lyman-alpha) is not re-derived for late decays; points where S decays at x >> 1 produce hotter N than assumed, flagged by x_decay.
usage: py -3 sterile_boltzmann.py"""
import json
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import kn

MPL, GS, mh, b = 1.22e19, 106.75, 125.25, 0.053
phid = math.sqrt(3 * 0.05 * 0.69) * 6.93e-11
AMAX = 7e-17 / phid


def yeq(x):
    return 45 / (4 * math.pi ** 4) / GS * x ** 2 * kn(2, x)


def omega(M, mS, vS, lam, init):
    y = math.sqrt(2) * M / vS
    Gnn = y ** 2 * mS / (16 * math.pi)
    Ghh = lam ** 2 * vS ** 2 / (8 * math.pi * mS)
    Hm = 1.66 * math.sqrt(GS) * mS ** 2 / MPL

    def rhs(lx, Y):
        x = math.exp(lx)
        g = kn(1, x) / kn(2, x)
        T = mS / x
        H = Hm / x ** 2
        s = 2 * math.pi ** 2 / 45 * GS * T ** 3
        sv = lam ** 2 / (16 * math.pi * (4 * mS ** 2 + 9 * T ** 2))
        ye = yeq(x)
        dS = -(Ghh * g * (Y[0] - ye) + Gnn * g * Y[0]) / H - s * sv * (Y[0] ** 2 - ye ** 2) / H
        dN = 2 * Gnn * g * Y[0] / H
        return [dS, dN]  # d/dlnx = x d/dx, and the 1/x in d/dx cancels

    y0 = [yeq(0.05) if init == "thermal" else 0.0, 0.0]
    sol = solve_ivp(rhs, (math.log(0.05), math.log(200.0)), y0, method="LSODA", rtol=1e-7, atol=1e-30)
    YN = sol.y[1, -1]
    # decay epoch: x where Gamma_tot = H
    xd = math.sqrt(Hm / max(Ghh + Gnn, 1e-300)) ** -1 if False else math.sqrt((Ghh + Gnn) / Hm) ** -1
    return 2.744e8 * M * YN, 1 / xd if xd > 0 else None


out = []
for Mk in (16.0, 18.0, 20.0):
    M = Mk * 1e-6
    for mS in (1000.0, 2000.0, 3000.0, 5000.0, 10000.0):
        for lam in np.geomspace(1e-8, 1e-4, 13):
            for init in ("thermal", "zero"):
                lo, hi = 10.0, 1e6
                fl = omega(M, mS, lo, lam, init)[0] - 0.12
                fh = omega(M, mS, hi, lam, init)[0] - 0.12
                if fl * fh > 0:
                    continue
                for _ in range(40):
                    mid = math.sqrt(lo * hi)
                    fm = omega(M, mS, mid, lam, init)[0] - 0.12
                    if fm * fl > 0:
                        lo, fl = mid, fm
                    else:
                        hi = mid
                vS = math.sqrt(lo * hi)
                lmax = AMAX * mh ** 2 / (b * vS ** 2)
                Ghh = lam ** 2 * vS ** 2 / (8 * math.pi * mS)
                Hm = 1.66 * math.sqrt(GS) * mS ** 2 / MPL
                xdec = math.sqrt(Hm / Ghh) if Ghh > 0 else None
                row = dict(M_keV=Mk, m_S=mS, lam=float(lam), init=init, v_S=vS, lambda_max=lmax, viable=bool(lam <= lmax), x_decay_hh=xdec)
                out.append(row)
viable = [r for r in out if r["viable"]]
for r in viable:
    print("VIABLE M %.0f keV m_S %.0f lambda %.1e (%s): v_S %.0f GeV, lambda_max %.1e, S->hh decays at x ~ %.1f" % (r["M_keV"], r["m_S"], r["lam"], r["init"], r["v_S"], r["lambda_max"], r["x_decay_hh"]))
print("solutions with Omega = 0.12:", len(out), " viable:", len(viable))
json.dump(dict(rows=out, n_solutions=len(out), n_viable=len(viable), clock_alpha_max=AMAX), open("sterile_boltzmann.json", "w"), indent=1)
