"""Item 3: minimal sterile-neutrino coupled dark matter.  Real singlet S (mass m_S, vev v_S) with L = (y/2) S N N, so M_N = y v_S / sqrt2, and S is the only field the dark-energy coupling acts on (M_N(phi) through v_S(phi)).
Relic: freeze-in from S -> N N decays with S in equilibrium (Hall, Jedamzik, March-Russell, West 2010, eq. for decays, from memory):
   Y_N = 2 * 135 g_S / (8 pi^3 * 1.66 * g*^(3/2)) * M_Pl Gamma / m_S^2,   Gamma = y^2 m_S / (16 pi),   Omega h^2 = 2.744e8 (M_N/GeV) Y_N.
Window on the Higgs portal lambda_hS:
   thermalisation of S by the portal (rate ~ lambda^2 T / (32 pi) > H at T = m_S): lambda_min = sqrt(32 pi * 1.66 sqrt(g*) m_S / M_Pl), a rough criterion;
   clocks with the fading coupling b on M_N (Pass 12625/12626): lambda_max = alpha_max m_h^2 / (b v_S^2), alpha_max = 2.2e-6 (1 + w = 0.05).
Item 5: Chat's Z9 sector (6e0f24d33): N_e^c (X = +9) gets its Majorana mass from S (X = -18), so it has the same structure, plus a Z' with m_Z' ~ 18 g_X v_S (X units) and electron charge X(L_e) = -9.
   The Z' must not thermalise N_e^c before freeze-in (g_X^2 m_Z'/(8 pi) < H(m_Z')), and a loop shift of m_e through the Z' threshold must pass clocks (g_X^2 (81)/(16 pi^2) b < alpha_max, my rough estimate).
usage: py -3 sterile_window.py"""
import json
import math

MPL, GS = 1.22e19, 106.75
mh, b, amax = 125.25, 0.053, 2.2e-6


def omega(y, M, mS):
    G = y ** 2 * mS / (16 * math.pi)
    Y = 2 * 135 / (8 * math.pi ** 3 * 1.66 * GS ** 1.5) * MPL * G / mS ** 2
    return 2.744e8 * M * Y


out = dict(rows=[])
for Mkev in (7.1, 15.0, 30.0):
    M = Mkev * 1e-6
    for mS in (100.0, 300.0, 1000.0, 3000.0):
        lo, hi = 1e-14, 1e-4
        for _ in range(200):
            mid = math.sqrt(lo * hi)
            lo, hi = (mid, hi) if omega(mid, M, mS) < 0.12 else (lo, mid)
        y = math.sqrt(lo * hi)
        vS = math.sqrt(2) * M / y
        lmin = math.sqrt(32 * math.pi * 1.66 * math.sqrt(GS) * mS / MPL)
        lmax = amax * mh ** 2 / (b * vS ** 2)
        # Chat-type gauged version: Z' mass and the two g_X conditions
        gX_therm = None
        mZ_over_g = 18 * vS
        # g^2 * (18 g vS) / (8 pi) < 1.66 sqrt(g*) (18 g vS)^2 / MPL  ->  g < ... solve: g^2 * m /(8pi) < 1.66 sqrt(g*) m^2/MPL, m = 18 g vS -> g < 8 pi * 1.66 sqrt(g*) * 18 vS / MPL  (linear after cancelling)
        gX_therm = 8 * math.pi * 1.66 * math.sqrt(GS) * 18 * vS / MPL
        mZ = 18 * gX_therm * vS
        gX_clock = math.sqrt(amax * 16 * math.pi ** 2 / (81 * b))
        row = dict(M_keV=Mkev, m_S=mS, y=y, v_S=vS, lambda_min=lmin, lambda_max=lmax, window=lmin < lmax, chat_gX_max_no_thermalise=gX_therm, chat_mZprime_GeV_at_that_g=mZ, chat_electron_coupling=9 * gX_therm, chat_gX_max_clock=gX_clock)
        out["rows"].append(row)
        print("M %5.1f keV m_S %6.0f: y %.2e v_S %.0f GeV  lambda in [%.1e, %.1e] window %s | Chat: g_X < %.1e -> m_Z' %.2e GeV, g_e %.1e" % (Mkev, mS, y, vS, lmin, lmax, lmin < lmax, gX_therm, mZ, 9 * gX_therm))
json.dump(out, open("sterile_window.json", "w"), indent=1)
