"""Pass 12731 (Claude track).
 (1) Two-loop orbifold window for the hybrid: the Pass 12703 two-loop unification (SM -> +Q+U at 1.74 TeV -> MSSM at M_SS = 1e10) with the
     localised orbifold running added above M_c = 1/R: extra one-loop coefficient b_extra = beta^H = (-3/5, 1, 3) (U(1)_GUT, SU(2), SU(3);
     Contino-Pilo-Rattazzi-Trincherini) between M_c and the alpha_1 = alpha_2 crossing, with M_c = M_12 / (Lambda R) iterated to self-consistency.
 (2) Unwin's heavy higgsino in the hybrid: Dirac higgsino with unsuppressed Z coupling needs m_chi >~ 8e10 GeV (direct detection); the gaugino-induced
     neutral splitting delta m0 ~ m_Z^2 / M_gaugino must exceed ~100 keV to make scattering inelastic; freeze-in needs T_RH ~ m_chi / 27.
 (3) Trinification's cyclic Z3 (and E6's centre) as protecting symmetries: both are elements of E6 itself, so they act trivially on every
     E6-invariant operator (including Hbar Sigma^2 H): no protection.
 (4) Resonance-free PQ relaxation for A: requirements (quadratic-dominated potential / flat direction, resonance parameter q <~ 1).
usage: py -3 analysis/explore_pass12731_round.py"""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (2)")[0], G)
B1, BIJ, DU, CU, YC, AINV, MZ, K, content = (G[k] for k in ("B1", "BIJ", "DU", "CU", "YC", "AINV", "MZ", "K", "content"))
beta_extra = np.array([-0.6, 1.0, 3.0])


def unify_orb(Mc, MVL=1740.0, yp=0.46, MSS=1e10, tanb=1.0):
    dbVL, dBVL = content(["Q", "U"])
    segs = [("SM", MZ, False, False), ("SM", MVL, True, False), ("MSSM", MSS, True, False), ("MSSM", Mc, True, True)]
    g = list(np.sqrt(4 * math.pi / AINV)); y = 0.97; mu = MZ
    for i, (th, ms, on, orb) in enumerate(segs):
        if i == 2: y = y / math.sin(math.atan(tanb))
        mend = segs[i + 1][1] if i + 1 < len(segs) else 1e19
        bb = B1[th] + (dbVL * (1.5 if th == "MSSM" else 1.0) if on else 0) + (beta_extra if orb else 0)
        Bm = BIJ[th] + (dBVL * (1.5 if th == "MSSM" else 1.0) if on else 0)
        ypp = yp if on else 0.0
        def fn(t, z, bb=bb, Bm=Bm, th=th, ypp=ypp):
            gg, yy = z[:3], z[3]; g2 = gg ** 2
            return list(K * gg ** 3 * bb + K * K * gg ** 3 * (Bm @ g2 - DU[th] * (yy ** 2 + ypp ** 2))) + [K * yy * (YC[th] * yy ** 2 - CU[th] @ g2)]
        ev = lambda t, z: z[0] - z[1]; ev.terminal = True
        if mend <= mu: continue
        s = solve_ivp(fn, (math.log(mu), math.log(mend)), g + [y], events=ev, rtol=1e-9, atol=1e-12, dense_output=True)
        if s.t_events[0].size:
            z = s.sol(s.t_events[0][0]); ai = 4 * math.pi / z[:3] ** 2
            return math.exp(s.t_events[0][0]), float(ai[2] - ai[0])
        g = list(s.y[:3, -1]); y = s.y[3, -1]; mu = mend
    return float("nan"), float("nan")


ref = unify_orb(1e30)
print(f"(1) reference (no orbifold): M12 = {ref[0]:.2e}, delta = {ref[1]:+.3f}")
rows = []
for LR in (3, 5, 7, 10, 14, 20, 40):
    Mc = ref[0] / LR
    for _ in range(6):
        M12, dl = unify_orb(Mc); Mc = M12 / LR
    rows.append(dict(Lambda_R=LR, M_c=Mc, M12=M12, delta=dl))
    print(f"(1) Lambda R = {LR}: M_c = {Mc:.2e}, M12 = {M12:.2e}, two-loop delta = {dl:+.3f}")
good = [r["Lambda_R"] for r in rows if abs(r["delta"]) < 0.1]
print(f"(1) |delta| < 0.1 at Lambda R in {good}")
res["two_loop_orbifold"] = dict(reference=ref, rows=rows, window_0p1=good)

mz = 91.19
hig = []
for Mg in (1e9, 8.45e9, 1e11):
    dm0 = mz ** 2 / Mg * 1e6                      # keV
    hig.append(dict(M_gaugino=Mg, delta_m0_keV=dm0, inelastic=dm0 > 100))
    print(f"(2) gaugino mass {Mg:.1e} GeV: neutral higgsino splitting ~ {dm0:.2f} keV ({'enough' if dm0 > 100 else 'too small'} for inelastic scattering, needs ~100 keV)")
res["higgsino"] = dict(rows=hig, need_mchi=8e10, M_SS=8.45e9,
                       verdict="with M_SS = 8.45e9 the splitting is ~1 keV, so the higgsino stays Dirac-like and must be heavier than ~8e10 GeV, i.e. mu ~ 10 M_SS; "
                               "then it is not the LSP. The hybrid's DM must be a bino/gaugino-type LSP at ~M_SS produced by freeze-in (T_RH < M_SS), or an axion")
print("(2) hybrid: higgsino DM needs mu >~ 8e10 ~ 10 M_SS (not the LSP); DM falls back to a gaugino LSP via freeze-in or an axion")
res["z3"] = dict(statement="E6's centre Z3 and trinification's cyclic Z3 are both elements of E6 (the cyclic permutation is a Weyl-group element), so "
                           "every E6-invariant operator is invariant under them: neither can forbid Hbar Sigma^2 H. 'Ternary' structures inside E6 cannot "
                           "protect the accidental symmetry; a symmetry outside E6 (Pass 12718's Z10) is needed")
print("(3) E6's centre and trinification's cyclic Z3 lie inside E6: they cannot forbid any E6-invariant operator (no protection)")
fa, fI = 2.48e10, 1.8e17
res["pq_relaxation"] = dict(amplitude_ratio=fI / fa,
                            requirements=["radial potential quadratic-dominated along a flat direction (W = lambda X (P Q - f_a^2) with soft masses)",
                                          "resonance parameter q = g^2 Phi_0^2 / 4 m^2 <~ 1 for couplings to the axion and other fields",
                                          "saxion decays before BBN without restoring PQ"],
                            note="a pure lambda |Phi|^4 radial potential restores PQ for Phi_0/f_a ~ 7e6 (conformal preheating); a SUSY flat direction is required")
print(f"(4) A's PQ field must drop by a factor {fI / fa:.0e}: only a quadratic flat direction with q <~ 1 avoids non-thermal restoration")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12731_round.json"), "w"), indent=1)
