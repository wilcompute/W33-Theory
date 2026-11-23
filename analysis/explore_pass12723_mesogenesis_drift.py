"""Pass 12723 add-on (outside-the-box): does the DESI-preferred dark-matter coupling of B' resolve the mesogenesis dark-matter mass puzzle?
 B-mesogenesis makes one dark baryon psi per baryon, so Omega_DM / Omega_b = m_psi / m_p (if psi is all of DM) -> m_psi(today) = 5.36 m_p =
 5.03 GeV; but the production B -> psi + baryon needs m_psi < m_B - m_p = 4.34 GeV at T ~ 10 MeV.  With m_psi ~ e^{beta phi} (Pass 12723 (2)),
 the mass grows as phi rolls.  Ratio m_psi(today) / m_psi(early) = e^{beta (phi_0 - phi_early)}; the field is frozen in radiation domination
 (beta rho_DM / H^2 ~ a), so phi_early ~ phi(z = 1100).  Needed ratio >= 5.03 / 4.34 = 1.16.  Also: the change of the DM density between
 recombination and today relative to uncoupled DM (affects the CMB-vs-late-time matter normalisation, i.e. S8).
usage: py -3 analysis/explore_pass12723_mesogenesis_drift.py"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "explore_pass12723_round.py"), encoding="utf-8").read()
blk = src.split("# ======================================================================= (2)")[1].split("w0c, s0, wac, sa, rho")[0]
G = {"np": np, "math": math}
exec("from scipy.integrate import solve_ivp\nfrom scipy.optimize import fsolve\n" + blk, G)
run, state, fsolve = G["run"], G["state"], G["fsolve"]
Ob, Om = G["Ob"], G["Om"]
w0c, s0, wac, sa, rho = -0.857, 0.057, -0.55, 0.235, -0.9
Cinv = np.linalg.inv(np.array([[s0 ** 2, rho * s0 * sa], [rho * s0 * sa, sa ** 2]]))
chi2 = lambda w0, wa: float(np.array([w0 - w0c, wa - wac]) @ Cinv @ np.array([w0 - w0c, wa - wac]))
need = 5.36 * 0.938 / (5.279 - 0.938)
rows = []
for lam in (0.8, 1.0, 1.2):
    for beta in (0.05, 0.1, 0.15, 0.2, 0.3):
        def eqs(p):
            V0, A = abs(p[0]), abs(p[1]); sol = run(lam, beta, V0, A); H2, rb, rc = state(sol, lam, beta, V0, A, 0.0)
            return [H2 - 1.0, (rb + rc) / (3 * H2) - Om]
        V0, A = fsolve(eqs, [3 * 0.69, 3 * (Om - Ob)], xtol=1e-12); V0, A = abs(V0), abs(A)
        sol = run(lam, beta, V0, A)
        dphi = float(sol.sol(0.0)[0] - sol.sol(-7.0)[0])
        ratio = math.exp(beta * dphi)
        w0, wa, wmin, _ = G["fit"](lam, beta)
        rows.append(dict(lam=lam, beta=beta, dphi=dphi, mass_ratio=ratio, meets_kinematics=ratio >= need, w0=w0, wa=wa, chi2=chi2(w0, wa),
                         S8_shift_proxy=ratio - 1))
        print(f"lambda {lam}, beta {beta:.2f}: Delta phi = {dphi:.3f}, m_psi(today)/m_psi(z=1100) = {ratio:.3f} (need {need:.3f}: "
              f"{'yes' if ratio >= need else 'no'}); DESI chi2 = {chi2(w0, wa):.2f} (w0 {w0:.3f}, wa {wa:.3f})")
both = [r for r in rows if r["meets_kinematics"] and r["chi2"] < 6.33]
print(f"points that both lift m_psi enough and beat LambdaCDM on DESI (chi2 < 6.33): {[(r['lam'], r['beta'], round(r['chi2'], 2)) for r in both] or 'none'}")
json.dump(dict(needed_ratio=need, rows=rows, both=both), open(os.path.join(ROOT, "data", "explore_pass12723_mesogenesis_drift.json"), "w"), indent=1)
