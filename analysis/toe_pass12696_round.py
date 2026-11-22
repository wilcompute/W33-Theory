"""Pass 12696: follow-ups to Pass 12695.
 (1) PQ anomaly-coefficient scan for completion A: integer PQ charges on the third family (up-type x_u, down-type x_d, charged lepton x_e;
     light families neutral -> flavour-safe at the CKM level, Pass 12694) plus an optional KSVZ quark (colour triplet, hypercharge Y_Q,
     charge x_Q).  N = (x_u + x_d + x_Q)/2, E = 3(4/9 x_u + 1/9 x_d) + x_e + 3 Q_Q^2 x_Q, N_DW = |2N|.  Keep N_DW = 1 and report g_agg/g_KSVZ
     = |E/N - 1.92|/1.92.  (Anomaly bookkeeping only, not a full Higgs-sector model.)
 (2) FCC-hh precision on y' (completion B): sigma ~ 2.4 pb per state at 1.65-1.7 TeV (Pass 12692), 30/ab; a reconstructed-sample
     efficiency eps; per-state mass resolution 5%; delta(Delta M) ~ sigma_M sqrt(2/N_rec); delta y' = sqrt2 delta(Delta M)/v.
 (3) A decaying particle X for the keV entropy window (Pass 12695): lifetime from t(T) = 1.32 s (MeV/T)^2 (g* = 3.36), energy fraction
     rho_X/rho_gamma = F^(4/3) - 1 for F = 1.048, required zeta_X = m_X n_X/n_gamma ~ 0.173 (F^(4/3)-1)/0.064 T.
 (4) Superallowed Ft shift that would reconcile V_ud(superallowed) with V_ud(neutron, bottle): V_ud^2 ~ 1/Ft.
usage: py -3 analysis/toe_pass12696_round.py"""
import json, math, os, itertools

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
# (1)
sols = []
for xu, xd, xe in itertools.product(range(-2, 3), repeat=3):
    for xQ, YQ in [(0, 0.0)] + [(x, y) for x in range(-2, 3) if x for y in (0.0, -1 / 3, 2 / 3)]:
        N = 0.5 * (xu + xd + xQ)
        if abs(2 * N) != 1: continue
        QQ = YQ          # colour-triplet, SU(2)-singlet KSVZ quark: Q = Y
        E = 3 * (4 / 9 * xu + 1 / 9 * xd) + xe + 3 * QQ ** 2 * xQ
        g = abs(E / N - 1.92) / 1.92
        third_family = (xu, xd) != (0, 0)
        sols.append(dict(x_u=xu, x_d=xd, x_e=xe, x_Q=xQ, Y_Q=round(YQ, 3), E_over_N=E / N, g_rel=g, third_family_charged=third_family))
good = [s for s in sols if s["third_family_charged"] and s["g_rel"] >= 0.5]
good.sort(key=lambda s: (abs(s["x_u"]) + abs(s["x_d"]) + abs(s["x_e"]) + abs(s["x_Q"]), -s["g_rel"]))
res["pq_scan"] = dict(n_NDW1=len(sols), n_third_family_visible=len(good), simplest=good[:8])
print(f"(1) N_DW = 1 assignments: {len(sols)}; with third-family charges and g_agg >= 0.5 g_KSVZ: {len(good)}; simplest:")
for s in good[:8]:
    print(f"    x_u={s['x_u']:+d} x_d={s['x_d']:+d} x_e={s['x_e']:+d} | KSVZ x_Q={s['x_Q']:+d} Y_Q={s['Y_Q']:+.3f}: E/N = {s['E_over_N']:.3f}, g/g_KSVZ = {s['g_rel']:.2f}")
# (2)
v = 246.22
fcc = []
for eps in (1e-3, 1e-2):
    N = 2.4e3 * 30000 * eps          # fb * fb^-1 * eps
    sM = 0.05 * 1690
    ddm = sM * math.sqrt(2 / N)
    fcc.append(dict(eps=eps, N_rec=N, delta_DeltaM=ddm, delta_yprime=math.sqrt(2) * ddm / v))
    print(f"(2) FCC-hh 30/ab, efficiency {eps:g}: N_rec ~ {N:.1e} per state, delta(Delta M) ~ {ddm:.2f} GeV -> delta y' ~ {math.sqrt(2) * ddm / v:.4f}")
res["fcc_yprime"] = fcc
# (3)
F = 1.0479; frac = F ** (4 / 3) - 1
kev = []
for TkeV in (5.3, 10.0, 30.0):
    T = TkeV * 1e-6       # GeV
    t = 1.32 / (TkeV * 1e-3) ** 2
    zeta = (math.pi ** 2 / 15) * frac * T / (2 * 1.2020569 / math.pi ** 2)
    kev.append(dict(T_keV=TkeV, lifetime_s=t, rho_frac=frac, zeta_X_GeV=zeta))
    print(f"(3) decay at T = {TkeV} keV: lifetime ~ {t:.1e} s, rho_X/rho_gamma = {frac:.3f}, zeta_X = m_X n_X/n_gamma ~ {zeta:.1e} GeV")
res["kev_particle"] = dict(rows=kev, note="tau ~ 1.5e3-5e4 s with zeta_X ~ 1e-6 GeV; EM cascades below the 2.22 MeV D threshold for T > 5.3 keV; "
                                          "neutrino or hadronic branchings must be tiny (hadronic BBN bounds at these lifetimes are ~1e-9 GeV or stronger)")
# (4)
Ft, sFt = 3072.24, 1.85
vn, vs = 0.97456, 0.97373
dFt = Ft * ((vs / vn) ** 2 - 1)
res["ft_shift"] = dict(Ft=Ft, sigma=sFt, shift_needed_s=dFt, in_sigma=dFt / sFt)
print(f"(4) reconciling superallowed with the neutron needs Delta Ft = {dFt:.1f} s ({dFt / sFt:.1f} sigma of the quoted 1.85 s)")
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12696_round.json"), "w"), indent=1)
