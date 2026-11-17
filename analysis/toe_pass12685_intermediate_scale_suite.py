"""Pass 12685: intermediate-scale suite following Pass 12684 (Higgs quartic zero ~ 5e10 GeV = sqrt(v M_Pl) = post-inflation axion f_a).
 (1) SMASH-type threshold: PQ radial mode m_rho = sqrt(2 lambda_sigma) f_a with tree-level shift delta = lambda_Hsigma^2/lambda_sigma above
     m_rho.  Stability needs m_rho <= mu_0 (SM lambda positive below the threshold) and delta > -min_{mu > m_rho} lambda_SM.  With f_a in
     the 2025 lattice window this bounds lambda_sigma above and lambda_Hsigma below, as functions of M_t.
 (2) Dark-dimension rescue: one vectorlike quark family (doublet Q + singlet T, Dirac mass M_VL, Yukawa y' H Q T) added to the running
     (one-loop extra terms on top of the two-loop SM): which y' makes lambda(M_5) = 0 for R = 1 and 30 um at the measured M_t?
 (3) Seesaw at M_N ~ 1e11 GeV: neutrino Yukawa needed for m_nu3 = 0.05 eV and its effect on lambda(M_Pl).
 (4) Future precision (FCC-ee m_t, lattice alpha_s, M_h, theory matching): error on log10 mu_0, separation of the sqrt(v M_Pl) variants,
     significance of excluding the Planck boundary lambda(M_Pl) = 0.
 (5) Can the intermediate-scale QCD axion be the early-dark-energy field?  Order-of-magnitude comparison of m^2 f^2 scales.
SM running and validation: as in toe_pass12684 (Buttazzo et al. NNLO matching, 2-loop RGEs, 3-loop offset +0.155 GeV in M_t).
usage: py -3 analysis/toe_pass12685_intermediate_scale_suite.py"""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
K = 1 / (16 * math.pi ** 2); MPL = 2.435e18; MPL_FULL = 1.2209e19; OFF3 = 0.155; v = 246.22


def beta_sm(gY, g2, g3, yt, lam):
    gY2, g22, g32, yt2 = gY * gY, g2 * g2, g3 * g3, yt * yt
    b1 = [41 / 6 * gY ** 3, -19 / 6 * g2 ** 3, -7 * g3 ** 3,
          yt * (9 / 2 * yt2 - 8 * g32 - 9 / 4 * g22 - 17 / 12 * gY2),
          24 * lam ** 2 - 6 * yt2 ** 2 + 12 * lam * yt2 - 3 * lam * (3 * g22 + gY2) + 3 / 8 * (2 * g22 ** 2 + (g22 + gY2) ** 2)]
    b2 = [gY ** 3 * (199 / 18 * gY2 + 9 / 2 * g22 + 44 / 3 * g32 - 17 / 6 * yt2),
          g2 ** 3 * (3 / 2 * gY2 + 35 / 6 * g22 + 12 * g32 - 3 / 2 * yt2),
          g3 ** 3 * (11 / 6 * gY2 + 9 / 2 * g22 - 26 * g32 - 2 * yt2),
          yt * (-12 * yt2 ** 2 + yt2 * (131 / 16 * gY2 + 225 / 16 * g22 + 36 * g32 - 12 * lam)
                + 1187 / 216 * gY2 ** 2 - 3 / 4 * g22 * gY2 + 19 / 9 * g32 * gY2 - 23 / 4 * g22 ** 2 + 9 * g22 * g32 - 108 * g32 ** 2 + 6 * lam ** 2),
          (-312 * lam ** 3 - 144 * lam ** 2 * yt2 + 36 * lam ** 2 * (3 * g22 + gY2) - 3 * lam * yt2 ** 2 + 80 * lam * g32 * yt2
           + 45 / 2 * lam * g22 * yt2 + 85 / 6 * lam * gY2 * yt2 - 73 / 8 * lam * g22 ** 2 + 39 / 4 * lam * g22 * gY2 + 629 / 24 * lam * gY2 ** 2
           + 30 * yt2 ** 3 - 32 * g32 * yt2 ** 2 - 8 / 3 * gY2 * yt2 ** 2 - 9 / 4 * g22 ** 2 * yt2 + 21 / 2 * g22 * gY2 * yt2 - 19 / 4 * gY2 ** 2 * yt2
           + 305 / 16 * g22 ** 3 - 289 / 48 * g22 ** 2 * gY2 - 559 / 48 * g22 * gY2 ** 2 - 379 / 48 * gY2 ** 3)]
    return [K * a + K * K * b for a, b in zip(b1, b2)]


def initial(Mt, Mh=125.20, a3=0.1180, MW=80.369):
    Mt = Mt - OFF3          # absorb the uniform 2- vs 3-loop offset into an effective top mass
    dt, da, dh, dw = Mt - 173.34, (a3 - 0.1184) / 0.0007, Mh - 125.15, (MW - 80.384) / 0.014
    return [0.35830 + 0.00011 * dt - 0.00020 * dw, 0.64779 + 0.00004 * dt + 0.00011 * dw, 1.1666 + 0.00314 * da - 0.00046 * dt,
            0.93690 + 0.00556 * dt - 0.00042 * da, 0.12604 + 0.00206 * dh - 0.00004 * dt]


def run(Mt, Mh=125.20, a3=0.1180, vl=None, ynu=None, MN=None, mu_max=MPL):
    """vl = (M_VL, y'_at_M_VL): vectorlike Q + T with Yukawa y' (one-loop extra terms); ynu: neutrino Yukawa above MN (3 equal, one-loop)."""
    y0 = initial(Mt, Mh, a3) + [vl[1] if vl else 0.0]
    Mt0 = Mt - OFF3

    def rhs(t, y):
        gY, g2, g3, yt, lam, yp = y
        mu = Mt0 * math.exp(t)
        d = beta_sm(gY, g2, g3, yt, lam) + [0.0]
        if vl and mu > vl[0]:
            d[0] += K * 2 * gY ** 3; d[1] += K * 2 * g2 ** 3; d[2] += K * 2 * g3 ** 3
            d[3] += K * yt * 3 * yp ** 2
            d[4] += K * (12 * lam * yp ** 2 - 6 * yp ** 4)
            d[5] = K * yp * (9 / 2 * yp ** 2 + 3 * yt ** 2 - 8 * g3 ** 2 - 9 / 4 * g2 ** 2 - 17 / 12 * gY ** 2)
        if ynu and mu > MN:
            d[3] += K * yt * ynu ** 2 * 3
            d[4] += K * (4 * lam * 3 * ynu ** 2 - 2 * 3 * ynu ** 4)
        return d
    sol = solve_ivp(rhs, (0, math.log(mu_max / Mt0)), y0, rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.5)
    return sol, Mt0


def mu0(Mt, **kw):
    sol, Mt0 = run(Mt, **kw)
    ts = np.linspace(0, sol.t[-1], 4000); lam = sol.sol(ts)[4]
    i = np.where(lam < 0)[0]
    if not len(i): return float("inf")
    j = i[0]; t = brentq(lambda tt: sol.sol(tt)[4], ts[j - 1], ts[j])
    return Mt0 * math.exp(t)


def lam_profile(Mt, **kw):
    sol, Mt0 = run(Mt, **kw)
    ts = np.linspace(0, sol.t[-1], 4000)
    return Mt0 * np.exp(ts), sol.sol(ts)


res = {}
MT, SMT, A3, SA3 = 172.57, 0.29, 0.1180, 0.0009
# check against Pass 12684: lambda = 0 at sqrt(v M_Pl) needs M_t ~ 172.57
chk = brentq(lambda m: math.log(mu0(m)) - math.log(math.sqrt(v * MPL_FULL)), 171.5, 174)
print(f"control: lambda = 0 at sqrt(v M_Pl) needs M_t = {chk:.3f} (Pass 12684: 172.57)"); res["control_Mt_sqrt_vMPl"] = chk
assert abs(chk - 172.57) < 0.05

# ---------------- (1) SMASH threshold
fa_lo, fa_hi = 57.2e11 / 65, 57.2e11 / 45
smash = []
for Mt in (172.14, 172.57, 173.00, 173.43):
    m0 = mu0(Mt); mus, Y = lam_profile(Mt)
    lam_min = float(Y[4].min())
    # m_rho <= mu_0 ; m_rho = sqrt(2 l_s) f_a  ->  l_s <= mu0^2 / (2 f_a^2)
    ls_max = (m0 ** 2 / (2 * fa_hi ** 2), m0 ** 2 / (2 * fa_lo ** 2))
    # delta >= -lambda_min (delta evaluated with the SM-like running above m_rho; conservative)
    smash.append(dict(Mt=Mt, mu0=m0, lambda_SM_min=lam_min, lambda_sigma_max_for_fa_window=ls_max,
                      portal_min_over_sqrt_lambda_sigma=math.sqrt(max(0.0, -lam_min))))
    print(f"(1) M_t={Mt}: mu0={m0:.2e}, min lambda_SM={lam_min:+.4f}; PQ threshold below mu0 needs lambda_sigma < {ls_max[0]:.2e}..{ls_max[1]:.2e}; "
          f"stability needs lambda_Hsigma >= {math.sqrt(max(0, -lam_min)):.3f} sqrt(lambda_sigma)")
res["smash_threshold"] = smash

# ---------------- (2) dark-dimension rescue by a vectorlike quark family
GEV_INV_M = 1.97327e-16
M5 = {R: (MPL ** 2 / (2 * math.pi * R / GEV_INV_M)) ** (1 / 3) for R in (1e-6, 30e-6)}
rescue = []
for MVL in (1.5e3, 3e3, 1e4):
    for R, m5 in M5.items():
        f = lambda yp: math.log(mu0(MT, vl=(MVL, yp))) - math.log(m5)
        try:
            yp = brentq(f, 0.05, 1.5, xtol=1e-5)
            sol, _ = run(MT, vl=(MVL, yp), mu_max=m5)
            ypmax = float(np.max(sol.y[5])); ok = ypmax < math.sqrt(4 * math.pi)
        except ValueError:
            yp, ypmax, ok = float("nan"), float("nan"), False
        rescue.append(dict(M_VL=MVL, R_um=R * 1e6, M5=m5, y_prime_at_MVL=yp, y_prime_max_below_M5=ypmax, perturbative=ok))
        print(f"(2) M_VL={MVL:.0f} GeV, R={R * 1e6:.0f} um (M5={m5:.2e}): lambda(M5)=0 needs y'(M_VL) = {yp:.3f} (max below M5 {ypmax:.3f})")
res["dark_dimension_rescue_vectorlike"] = rescue

# ---------------- (3) seesaw at M_N ~ 1e11
seesaw = []
for MN in (1e10, 1e11, 1e12):
    ynu = math.sqrt(0.05e-9 * MN) / 174.1
    sol0, _ = run(MT); solN, _ = run(MT, ynu=ynu, MN=MN)
    seesaw.append(dict(MN=MN, y_nu=ynu, dlambda_MPl=float(solN.y[4, -1] - sol0.y[4, -1])))
    print(f"(3) M_N={MN:.0e}: y_nu={ynu:.4f} for m_nu3=0.05 eV; shift of lambda(M_Pl) = {solN.y[4, -1] - sol0.y[4, -1]:+.2e}")
res["seesaw"] = seesaw

# ---------------- (4) precision forecast
h = 0.05
dl_dmt = (math.log10(mu0(MT + h)) - math.log10(mu0(MT - h))) / (2 * h)
dl_da = (math.log10(mu0(MT, a3=A3 + 0.0002)) - math.log10(mu0(MT, a3=A3 - 0.0002))) / 0.0004
dl_dmh = (math.log10(mu0(MT, Mh=125.30)) - math.log10(mu0(MT, Mh=125.10))) / 0.2
TH_MT_EQ = 0.0005 / 0.00556          # y_t matching theory error -> GeV-equivalent (Buttazzo +-0.0005)
TH_LAM = 0.0003                      # lambda(M_t) matching theory error
dl_dlam = dl_dmh / 0.00206           # d log10 mu0 / d lambda(M_t)
def sig(dmt, da, dmh, th=True):
    terms = [dl_dmt * dmt, dl_da * da, dl_dmh * dmh] + ([dl_dmt * TH_MT_EQ, dl_dlam * TH_LAM] if th else [])
    return math.sqrt(sum(t * t for t in terms))
now = sig(math.hypot(0.29, 0.5), 0.0009, 0.11); fut = sig(0.05, 0.0003, 0.02); fut_noth = sig(0.05, 0.0003, 0.02, th=False)
variants = {"sqrt(v M_Pl)": math.sqrt(v * MPL_FULL), "sqrt(Mz M_Pl)": math.sqrt(91.19 * MPL_FULL), "sqrt(v Mbar)": math.sqrt(v * MPL), "sqrt(mt Mbar)": math.sqrt(172.57 * MPL)}
spread = math.log10(max(variants.values())) - math.log10(min(variants.values()))
# Planck-boundary exclusion: M_t required 170.98 (Pass 12684) vs measured; in M_t-equivalent units
sig_mt_now = math.hypot(SMT, abs(dl_da / dl_dmt) * SA3); sig_mt_fut = math.hypot(0.05, abs(dl_da / dl_dmt) * 0.0003, TH_MT_EQ, abs(dl_dlam / dl_dmt) * TH_LAM)
fc = dict(dlog10mu0_dMt=dl_dmt, dlog10mu0_dalpha_s=dl_da, dlog10mu0_dMh=dl_dmh, sigma_log10mu0_now_incl_pole_ambiguity=now,
          sigma_log10mu0_future=fut, sigma_log10mu0_future_no_theory=fut_noth, variant_spread_decades=spread,
          planck_boundary_sigma_now=(MT - 170.98) / sig_mt_now, planck_boundary_sigma_future=(MT - 170.98) / sig_mt_fut,
          mt_equivalent_sigma_future=sig_mt_fut)
print(f"(4) dlog10mu0/dMt = {dl_dmt:.2f}/GeV, /dalpha_s = {dl_da:.0f}, /dMh = {dl_dmh:.2f}/GeV; sigma(log10 mu0): now {now:.2f}, FCC-era {fut:.2f} "
      f"(no theory {fut_noth:.2f}); variant spread {spread:.2f} decades; Planck boundary excluded at {fc['planck_boundary_sigma_now']:.1f} sigma now, "
      f"{fc['planck_boundary_sigma_future']:.1f} sigma future (if the central value stays)")
res["forecast"] = fc

# ---------------- (5) axion as early dark energy?
# EDE (e.g. Poulin et al. n=3): f ~ 0.2 M_Pl, m ~ 1e-27 eV (fraction ~0.1 at z_c ~ 3500): m^2 f^2 ~ (1e-27 eV)^2 (5e26 eV)^2
ede = (1e-27) ** 2 * (0.2 * MPL * 1e9) ** 2          # eV^4
qcd = (5.7e-5) ** 2 * (1e11 * 1e9) ** 2                # m_a^2 f_a^2 = chi_top ~ (75.5 MeV)^4
res["axion_ede"] = dict(ede_m2f2_eV4=ede, qcd_axion_m2f2_eV4=qcd, log10_ratio=math.log10(qcd / ede))
print(f"(5) EDE needs m^2 f^2 ~ {ede:.1e} eV^4; the QCD axion has {qcd:.1e} eV^4 (ratio 10^{math.log10(qcd / ede):.0f}); "
      f"and its mass is 10^{math.log10(5.7e-5 / 1e-27):.0f} times too large to stay frozen until z ~ 3500")
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12685_intermediate_scale_suite.json"), "w"), indent=1)
