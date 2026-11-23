"""Pass 12708 (Claude track): five checks behind Pass 12707.
 (1) Independent check of the d-wave claim of arXiv:2610.01825: massive spin-1 'Yang-Mills-like' cubic vertex
     Y = (e1.e2)((p1-p2).e3) + cyclic and its double copy A = Y Y' for spin-2 (product polarisations span all helicities by
     bilinearity).  Near threshold (m1 = m2 + m3 + Q) the slope d ln|A| / d ln p must be 2 (|A|^2 p ~ p^5, d-wave), versus 0
     for a non-derivative s-wave structure tr(e1 e2 e3).
 (2) MS-bar top-mass route: m_t(m_t) = 162.5 +2.1 -1.5 GeV (PDG, from sigma_tt) -> pole with the four-loop relation
     m_pole/m = 1 + 0.4244 a + 0.8345 a^2 + 2.375 a^3 + (8.49 +- 0.25) a^4 (Marquard et al. PRL 114 142002), a = alpha_s^(6)(m_t);
     mu_0 from this route and the size of the last term (renormalon scale).
 (3) Cross-checks of the Pass 12707 threshold: (a) numeric fit of the exact CW potential; (b) Passarino-Veltman route for Z
     (2k.(k+p) = D1 + D2 + 2m^2 - p^2, B0'(0;m,m) = 1/6m^2); (c) heavy-fermion gauge thresholds vanish in MS-bar at mu = M,
     so only the two-loop y'^2 term moves the hybrid's unification: estimate.
 (4) kappa vs sin(theta_L) for a singlet T by width consistency with the ATLAS statements (2305.03401, 2408.08789):
     Gamma/M = g^2 s^2 M^2 / (32 pi m_W^2) (Goldstone limit, Gamma ~ 2 Gamma_W); which map (kappa = s or kappa = sqrt2 s)
     reproduces 'kappa = 0.53 excluded to 2.3 TeV with Gamma/m < 50%' and 'Gamma/m < 5% at kappa = 0.25, 1.5 TeV'.
 (5) B' status: B-mesogenesis needs BR(B -> psi + baryon (+X)) >~ 1e-4; recorded limits (no dedicated search; ALEPH recast).
usage: py -3 analysis/toe_pass12708_round.py"""
import itertools, json, math, os
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CARD = json.load(open(os.path.join(HERE, "toe_inputs_card.json"), encoding="utf-8"))
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, OFF3 = (G[k] for k in ("initial", "beta_sm", "OFF3"))
K = 1 / (16 * math.pi ** 2); NC = 3
res = {}

# ======================================================================= (1) d-wave check
ETA = np.diag([1.0, -1, -1, -1]); dot = lambda a, b: a @ ETA @ b


def pols(k, m):
    """three polarisation 4-vectors of a massive vector with 4-momentum k."""
    kv = k[1:]; pk = np.linalg.norm(kv)
    n = kv / pk if pk > 0 else np.array([0, 0, 1.0])
    t1 = np.cross(n, [1, 0, 0] if abs(n[0]) < .9 else [0, 1, 0]); t1 /= np.linalg.norm(t1); t2 = np.cross(n, t1)
    return [np.concatenate([[0], t1]), np.concatenate([[0], t2]), np.concatenate([[pk / m], k[0] / m * n])]


def amps(m1, m2, m3, Q):
    M1 = m2 + m3 + Q
    p = math.sqrt((M1 ** 2 - (m2 + m3) ** 2) * (M1 ** 2 - (m2 - m3) ** 2)) / (2 * M1)
    n = np.array([0.3, 0.4, math.sqrt(1 - .25)])
    k1 = np.array([M1, 0, 0, 0]); k2 = np.concatenate([[math.hypot(p, m2)], p * n]); k3 = np.concatenate([[math.hypot(p, m3)], -p * n])
    P1, P2, P3 = k1, -k2, -k3                                      # all incoming: P1 + P2 + P3 = 0
    E1, E2, E3 = pols(k1, M1), pols(k2, m2), pols(k3, m3)
    Y = lambda a, b, c: dot(a, b) * dot(P1 - P2, c) + dot(b, c) * dot(P2 - P3, a) + dot(c, a) * dot(P3 - P1, b)
    ys = [Y(a, b, c) for a in E1 for b in E2 for c in E3]
    s_wave = [dot(a, b) * 0 + np.einsum("i,ij,j", a, ETA, b) * np.einsum("i,ij,j", c, ETA, c) for a in E1 for b in E2 for c in E3]
    grav = max(abs(y1 * y2) for y1 in ys for y2 in ys)
    return p, max(abs(y) for y in ys), grav, max(abs(s) for s in s_wave)


rows = []
for Q in np.logspace(-7, -2, 6):
    p, ymax, gmax, smax = amps(1.0, 0.4, 0.6, Q)
    rows.append(dict(Q=Q, p=p, YM=ymax, grav=gmax, s_wave=smax))
lp = np.log([r["p"] for r in rows])
slopes = {k: float(np.polyfit(lp, np.log([r[k] for r in rows]), 1)[0]) for k in ("YM", "grav", "s_wave")}
print(f"(1) near-threshold slopes d ln|A|/d ln p: YM-like vertex {slopes['YM']:.3f}, spin-2 double copy {slopes['grav']:.3f}, s-wave contact {slopes['s_wave']:.3f}")
print(f"(1) -> Gamma ~ |A|^2 p ~ p^{2 * slopes['grav'] + 1:.2f} for the double copy (d-wave, Langhoff: p^5); s-wave would give p^{2 * slopes['s_wave'] + 1:.2f}")
assert abs(slopes["YM"] - 1) < 0.02 and abs(slopes["grav"] - 2) < 0.02 and abs(slopes["s_wave"]) < 0.02
res["dwave"] = dict(rows=rows, slopes=slopes, width_power=2 * slopes["grav"] + 1,
                    note="At threshold all momenta are parallel to the rest-frame time axis and every polarisation is spatial, so each p.e "
                         "vanishes: the YM-like vertex is O(p), its square O(p^2). Independent of 2610.01825's derivation; assumes its vertex form.")

# ======================================================================= (2) MS-bar route


def alpha_s_mu(mu, a_mz=CARD["alpha_s"]["value"], nf=5):
    b0 = (33 - 2 * nf) / (12 * math.pi); b1 = (153 - 19 * nf) / (24 * math.pi ** 2)
    f = lambda t, a: [-2 * a[0] ** 2 * (b0 + b1 * a[0])]
    return solve_ivp(f, (0, math.log(mu / 91.1876)), [a_mz], rtol=1e-10).y[0, -1]


def pole_from_msbar(mb):
    a = alpha_s_mu(mb)
    terms = [mb * c * a ** k for k, c in ((1, 0.4244), (2, 0.8345), (3, 2.375), (4, 8.49))]
    return mb + sum(terms), terms, a


def mu0(Mt, a3=CARD["alpha_s"]["value"]):
    Mt0 = Mt - OFF3
    s = solve_ivp(lambda t, y: beta_sm(*y), (0, math.log(2.4e18 / Mt0)), initial(Mt, 125.20, a3), rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.5)
    ts = np.linspace(0, s.t[-1], 3000); lam = s.sol(ts)[4]; i = np.where(lam < 0)[0]
    if not len(i): return float("inf")
    j = i[0]; return Mt0 * math.exp(brentq(lambda t: s.sol(t)[4], ts[j - 1], ts[j]))


ms = {}
for lab, mb in (("central", 162.5), ("-1.5", 161.0), ("+2.1", 164.6)):
    mp, terms, a = pole_from_msbar(mb)
    ms[lab] = dict(mbar=mb, alpha_s6=a, pole=mp, terms=terms, mu0=mu0(mp))
    print(f"(2) mbar_t = {mb}: alpha_s(mbar) = {a:.4f}, terms {[round(t, 3) for t in terms]} GeV -> pole {mp:.2f} GeV, mu_0 = {ms[lab]['mu0']:.2e}")
last = ms["central"]["terms"][3]
fcc = dict(sigma_mbar=0.04, sigma_conv=0.25 / 8.49 * last, note="FCC-ee threshold scan gives a short-distance (PS/MS-bar) mass; the MS-bar input has no renormalon")
print(f"(2) four-loop term = {last:.3f} GeV (renormalon-sized); FCC-ee: sigma(mbar) ~ 0.04 GeV, conversion-coefficient error {fcc['sigma_conv']:.3f} GeV")
res["msbar_route"] = dict(rows=ms, four_loop_term=last, fcc=fcc,
                          verdict="sigma_tt-based MS-bar input reproduces the pole central value (172.5) but with +2.2/-1.6 GeV: mu_0 unconstrained "
                                  "over 1e9-1e19 today by this route; the direct-reconstruction mass is precise but scheme-ambiguous (Pass 12707).")

# ======================================================================= (3) threshold cross-checks
M_, y_ = 1.0, 0.5


def Vcw(h):
    A = np.array([[M_, y_ * h / math.sqrt(2)], [0, M_]]); m2 = np.linalg.svd(A, compute_uv=False) ** 2
    return -NC * K * float(np.sum(m2 ** 2 * (np.log(m2 / M_ ** 2) - 1.5)))


hs = np.linspace(0.02, 0.25, 40); vv = np.array([Vcw(h) - Vcw(0) for h in hs])
c = np.polyfit(hs ** 2, vv, 4)                                   # coefficients of h^8..h^0 in powers of h^2
c4_num = c[-3]; c4_th = -(5 / 6) * NC * K * y_ ** 4 / 4
print(f"(3a) numeric h^4 coefficient {c4_num:.6e} vs (5/6)-formula {c4_th:.6e} (ratio {c4_num / c4_th:.5f})")
assert abs(c4_num / c4_th - 1) < 1e-3
B0p = quad(lambda x: x * (1 - x), 0, 1)[0]                        # d B0/dp^2 at 0 times m^2
x = 0.37; m = 1.0; p2 = 0.0                                         # algebraic identity check at a random point
k = np.array([0.7, 0.2, -0.4, 0.9]); pv = np.array([0.3, -0.5, 0.1, 0.2])
D1 = dot(k, k) - m ** 2; D2 = dot(k + pv, k + pv) - m ** 2
assert abs(2 * dot(k, k + pv) - (D1 + D2 + 2 * m ** 2 - dot(pv, pv))) < 1e-12
Zconst = 2 * B0p                                                   # Pi'(0) ~ -B0(0) + 2 m^2 B0'(0) = -[1/eps + ln(mu^2/m^2)] + 1/3
print(f"(3b) PV: 2 m^2 B0'(0;m,m) = {Zconst:.6f} (= 1/3) -> Z_kin(mu = M) = 1 - Nc K y'^2/3, as in Pass 12707")
assert abs(Zconst - 1 / 3) < 1e-10
dy2 = 2 * 0.470 * 0.006; T = math.log(4e16 / 1740)
dainv = {nm: C * dy2 * T / (32 * math.pi ** 3) for nm, C in (("alpha_1 (C~17/10)", 1.7), ("alpha_2 (C~3/2)", 1.5), ("alpha_3 (C~2)", 2.0))}
print(f"(3c) gauge thresholds vanish at mu = M (MS-bar); two-loop y'^2 shift moves alpha_i^-1 by {max(dainv.values()):.1e} (hybrid delta = +0.26 unchanged)")
res["threshold_checks"] = dict(cw_ratio=c4_num / c4_th, Z_const=Zconst, gauge_shift_alpha_inv=dainv)

# ======================================================================= (4) kappa vs sin theta_L by width consistency
g, mW = 0.652, 80.37
gw = lambda s, M: g ** 2 * s ** 2 * M ** 2 / (32 * math.pi * mW ** 2)       # Gamma/M, singlet, Goldstone limit, Gamma ~ 2 Gamma_W
kap = {}
for nm, f in (("kappa = sin", lambda kk: kk), ("kappa = sqrt2 sin", lambda kk: kk / math.sqrt(2))):
    a1 = gw(f(0.53), 2300.0); a2 = gw(f(0.25), 1500.0)
    kap[nm] = dict(GoverM_k053_2p3TeV=a1, GoverM_k025_1p5TeV=a2, consistent=(a1 <= 0.55 and a2 <= 0.055))
    print(f"(4) {nm:18s}: Gamma/M(kappa=0.53, 2.3 TeV) = {a1:.2f} [ATLAS: within the <50% region], Gamma/M(kappa=0.25, 1.5 TeV) = {a2:.3f} [ATLAS: ~5%] -> "
          f"{'consistent' if kap[nm]['consistent'] else 'inconsistent'}")
assert kap["kappa = sqrt2 sin"]["consistent"] and not kap["kappa = sin"]["consistent"]
res["kappa_map"] = dict(rows=kap, conclusion="kappa ~ sqrt2 sin(theta_L) for the singlet (width-consistent); B's theta_t <= 0.18 -> kappa <= 0.25, "
                                              "Gamma/M <= 5% at 1.5 TeV: below current single-T reach above 1.5 TeV")

# ======================================================================= (5) B' status
res["B_prime"] = dict(required="BR(B -> psi + baryon + X) >~ 1e-4 (Alonso-Alvarez, Elor, Escudero 2101.02706)",
                      limits={"dedicated search": "none found (2026-11)", "ALEPH recast": "BR <~ 1e-4 - 1e-2 (mode-dependent)",
                              "BaBar B- -> Lambdabar pbar nu nubar": "< 3e-5 (related mode, not the psi channel)"},
                      verdict="B' is untested by direct searches; Belle II / LHCb dedicated searches can cover BR ~ 1e-5 - 1e-4")
print("(5) B': BR >~ 1e-4 needed; no dedicated search yet (ALEPH recast 1e-4..1e-2): untested, decisive at Belle II/LHCb")
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12708_round.json"), "w", encoding="utf-8"), indent=1, default=float)
print("wrote data/toe_pass12708_round.json")
