"""Item 4: Lyman-alpha lower edge for the decay-produced coupled sterile neutrino, and the remaining window.
Free-streaming match to thermal WDM: decays of S at T ~ m_S give <p/T> = 2.5 at production (rough), diluted by entropy to p/T_nu,0 = 2.5 (g*S0/g*S_prod)^(1/3) (11/4)^(1/3).
Thermal WDM relic (g = 2 fermion) of mass m_th: (T_x/T_nu)^3 = 94 eV * omega_dm / m_th, <p> = 3.15 T_x.  Equal <p>/M  ->  M_N,min = m_th * (p_N/T_nu) / (3.15 T_x/T_nu).
Bounds used (from memory, not re-read): m_th > 5.3 keV (Irsic et al 2017), 5.7 keV (later analyses); omega_dm = 0.12.
Then rescan the freeze-in window of sterile_window.py on a finer grid: M_N 10..20 keV, m_S 0.1..10 TeV.
usage: py -3 sterile_lya.py"""
import json
import math

GS0, OM = 3.91, 0.12
pN = 2.5 * (GS0 / 106.75) ** (1 / 3) * (11 / 4) ** (1 / 3)
out = dict(p_over_Tnu=pN, Mmin={})
for mth in (5.3, 5.7):
    tx = (94.0 * OM / (mth * 1e3)) ** (1 / 3)
    Mmin = mth * pN / (3.15 * tx)
    out["Mmin"][str(mth)] = Mmin
    print("thermal-equivalent bound %.1f keV -> decay-produced M_N > %.1f keV" % (mth, Mmin))
MPL, GS, mh, b, amax = 1.22e19, 106.75, 125.25, 0.053, 2.2e-6


def omega(y, M, mS):
    G = y ** 2 * mS / (16 * math.pi)
    return 2.744e8 * M * 2 * 135 / (8 * math.pi ** 3 * 1.66 * GS ** 1.5) * MPL * G / mS ** 2


win = []
for Mk in (10, 12, 14, 15, 16, 18, 20):
    for mS in (100, 300, 1000, 3000, 10000):
        M = Mk * 1e-6
        lo, hi = 1e-14, 1e-4
        for _ in range(200):
            mid = math.sqrt(lo * hi)
            lo, hi = (mid, hi) if omega(mid, M, mS) < OM else (lo, mid)
        y = math.sqrt(lo * hi)
        vS = math.sqrt(2) * M / y
        lmin = math.sqrt(32 * math.pi * 1.66 * math.sqrt(GS) * mS / MPL)
        lmax = amax * mh ** 2 / (b * vS ** 2)
        ok = lmin < lmax and Mk >= out["Mmin"]["5.3"]
        win.append(dict(M_keV=Mk, m_S=mS, v_S=vS, lambda_min=lmin, lambda_max=lmax, portal_ok=lmin < lmax, lya_ok=Mk >= out["Mmin"]["5.3"], open=ok))
open_ = [(w["M_keV"], w["m_S"]) for w in win if w["open"]]
out["window"] = win
out["open_points"] = open_
print("open (M_keV, m_S):", open_)
print("portal-allowed but Ly-a excluded:", [(w["M_keV"], w["m_S"]) for w in win if w["portal_ok"] and not w["lya_ok"]])
json.dump(out, open("sterile_lya.json", "w"), indent=1)
