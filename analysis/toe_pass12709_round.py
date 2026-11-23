"""Pass 12709 (Claude track): five follow-ups to Pass 12708.
 (1) B' = dark dimension + top partner + B-mesogenesis against the literature: required BR (2211.10553: >~1e-5 neutral, >~1e-6 charged,
     >~1e-7 most general; Dark_CP 2509.18246: A_CP Br >~ 1.3e-8 (60 MeV/T_R)(m_Phi/2m_M)); Belle/BaBar B_d -> Lambda psi limits
     1e-5 - 1e-4.  Overlap of the dark-dimension reheating window (Pass 12707) with Dark_CP's 5-60 MeV and the A_CP Br it then needs.
 (2) Discrete curvature of the W33 tetrahedral (clique) complex: face incidences (is it a pseudomanifold?), vertex links, Banchoff
     combinatorial curvature k(v) = sum_i (-1)^i f_{i-1}(lk v)/(i+1) (sum = chi), and the equilateral angle deficits.
 (3) Warped cascades: literature status (2609.36234 universal q^5 rate; 2610.01825).
 (4) FCC-ee forecast for vacuum stability: critical pole mass M_t^c (min lambda = 0 below M_Pl) vs alpha_s; probability that the SM
     vacuum is absolutely stable today (exp; exp + 0.5 GeV scheme) and at FCC-ee.
 (5) Bayesian evidence of Pass 12698 updated: scheme error on m_t, B -> B' (DM no longer graviton/T_i^3-tuned; penalties for the
     surviving lambda range and the reheating overlap), dy'/dm_t from the Pass 12707 setup.
usage: py -3 analysis/toe_pass12709_round.py"""
import itertools, json, math, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CARD = json.load(open(os.path.join(HERE, "toe_inputs_card.json"), encoding="utf-8"))
P07 = json.load(open(os.path.join(ROOT, "data", "toe_pass12707_round.json"), encoding="utf-8"))
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, OFF3 = (G[k] for k in ("initial", "beta_sm", "OFF3"))
res = {}

# ======================================================================= (1) B'
mB, Rmax = 5.28, CARD["dark_dimension"]["R_max_um"]
rows = []
for r in P07["reheating"]["rows"]:
    lo, hi = max(r["T_RH_min"], 5.0), min(r["T_RH_max_est"], 60.0)
    need = {f"m_Phi={mp:g}": [1.3e-8 * (60 / T) * (mp / (2 * mB)) for T in (hi, lo)] for mp in (11.0, 100.0)}
    rows.append(dict(R_um=r["R_um"], window_MeV=[lo, hi], overlap=hi > lo, ACP_Br_needed=need))
    print(f"(1) R = {r['R_um']:.4f} um: T_RH window [{lo:.1f}, {hi:.1f}] MeV inside Dark_CP's 5-60 MeV; needs A_CP*Br >= "
          f"{need['m_Phi=11'][0]:.1e}-{need['m_Phi=11'][1]:.1e} (m_Phi = 11 GeV), {need['m_Phi=100'][0]:.1e}-{need['m_Phi=100'][1]:.1e} (100 GeV)")
res["B_prime"] = dict(rows=rows, literature={
    "2211.10553": "Br(B0 -> psi + baryon) >~ 1e-5 (neutral), >~ 1e-6 (charged), >~ 1e-7 (CPV all dark); max exclusive Br(B_d -> psi Lambda) 1.2e-5 / 3.2e-5",
    "2509.18246 (Dark_CP)": "Y_B/Y_B^obs = (Br/1.3e-8)|A_CP|(T_R/60 MeV)(2 m_M/m_Phi); T_R 5-60 MeV; Belle II reach ~1e-7",
    "Belle PRD 105 L051101 / BaBar": "B_d -> Lambda psi 1e-5 - 1e-4 over m_psi; disfavours some channels of the original neutral mechanism"},
    correction="Pass 12708 quoted BR >~ 1e-4 (from the 2101.02706 summary); the requirement is 1e-8 (Dark_CP) - 1e-5 (minimal neutral).")

# ======================================================================= (2) W33 tetrahedral complex: curvature
pts = sorted({tuple((x * (1 if next(y for y in v if y) == 1 else 2)) % 3 for x in v) for v in itertools.product(range(3), repeat=4) if any(v)})
J = lambda x, y: (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3
A = {(i, j) for i in range(40) for j in range(40) if i != j and J(pts[i], pts[j]) == 0}
cl = lambda k: [s for s in itertools.combinations(range(40), k) if all(p in A for p in itertools.combinations(s, 2))]
E, T3, T4 = cl(2), cl(3), cl(4)
tri_in_tet = {t: sum(set(t) <= set(q) for q in T4) for t in T3}
edge_in_tet = {e: sum(set(e) <= set(q) for q in T4) for e in E}
kappa = []
for v in range(40):
    lk = [tuple(x for x in q if x != v) for q in T4 if v in q]               # link: triangles (and their faces)
    f2 = len(lk); f1 = len({tuple(sorted(e)) for t in lk for e in itertools.combinations(t, 2)}); f0 = len({x for t in lk for x in t})
    kappa.append(1 - f0 / 2 + f1 / 3 - f2 / 4)
th_dih = math.acos(1 / 3); om = math.acos(23 / 27)                          # regular tetrahedron: dihedral angle, vertex solid angle
pm = all(c == 1 for c in tri_in_tet.values())
print(f"(2) W33 complex: every triangle in exactly {set(tri_in_tet.values())} tetrahedron, every edge in {set(edge_in_tet.values())}: "
      f"tetrahedra share only vertices -> not a pseudomanifold (Regge hinges unshared)")
print(f"(2) vertex link = {len([q for q in T4 if 0 in q])} disjoint triangles; Banchoff curvature k(v) = {set(kappa)} at every vertex; sum = {sum(kappa):.0f} = chi")
print(f"(2) equilateral metric: edge deficit 2pi - arccos(1/3) = {2 * math.pi - th_dih:.4f} rad (one tetrahedron per hinge); "
      f"vertex solid-angle deficit 4pi - 4 Omega = {4 * math.pi - 4 * om:.4f} sr")
assert pm and set(edge_in_tet.values()) == {1} and set(kappa) == {-2.0} and sum(kappa) == -80
res["w33_curvature"] = dict(triangle_in_tet=1, edge_in_tet=1, link="4 disjoint triangles", banchoff=-2.0, chi=-80,
                            edge_deficit=2 * math.pi - th_dih, vertex_solid_deficit=4 * math.pi - 4 * om,
                            note="uniformly negative combinatorial curvature (-2 per point), like a tree of 40 tetrahedra with 81 independent loops; "
                                 "Regge calculus needs shared faces, which this complex lacks: a 4D Regge model would need a different gluing (e.g. along the 160 triangles)")

# ======================================================================= (3) warped cascades
res["warped"] = dict(status="Lee-Randall-Riojas 2609.36234: universal q^5 near-threshold rate (RS-like and flat), rules out existing Dark Dimension DM "
                            "models; Langhoff 2610.01825: d-wave for any static warping, cascade estimate for weak warping; reproduced kinematically in 12708",
                     open="strongly warped spectra change the freeze-in relic (eq. 28 assumes m_n = n m_KK): the R <~ 0.2 um bound is flat-spectrum only")
print("(3) warped: universal q^5 (2609.36234) -> warping does not revive graviton DM; the R bound itself assumes a flat KK spectrum (open)")

# ======================================================================= (4) stability forecast


def min_lam(Mt, a3):
    Mt0 = Mt - OFF3
    s = solve_ivp(lambda t, y: beta_sm(*y), (0, math.log(1.22e19 / Mt0)), initial(Mt, 125.20, a3), rtol=1e-9, atol=1e-12, max_step=0.2, dense_output=True)
    return float(s.sol(np.linspace(0, s.t[-1], 3000))[4].min())


crit = {a3: brentq(lambda m: min_lam(m, a3), 168.0, 174.0, xtol=1e-4) for a3 in (0.1171, 0.1180, 0.1183, 0.1189)}
dMc = (crit[0.1189] - crit[0.1171]) / 0.0018
for a3, m in crit.items():
    print(f"(4) alpha_s = {a3}: absolute stability (min lambda >= 0 up to M_Pl) needs M_t <= {m:.3f} GeV")
fore = {}
for lab, mt, smt, sas in (("today exp (PDG)", 172.57, 0.29, 0.0009), ("today exp + scheme", 172.57, math.hypot(0.29, 0.5), 0.0009),
                          ("today ATLAS+CMS + scheme", 172.52, math.hypot(0.33, 0.5), 0.0009), ("FCC-ee (central PDG)", 172.57, 0.04, 0.0002)):
    sig = math.hypot(smt, dMc * sas); z = (crit[0.1180] - mt) / sig
    fore[lab] = dict(Mt=mt, sigma_eff=sig, z_to_stability=z, P_stable=float(norm.cdf(z)))
    print(f"(4) {lab:26s}: M_t = {mt} +- {sig:.2f} (incl. alpha_s) -> {-z:.1f} sigma from stability, P(absolutely stable) = {norm.cdf(z):.2e}")
res["stability"] = dict(Mt_crit=crit, dMc_dalpha_s=dMc, forecast=fore,
                        note="2-loop running + Buttazzo matching with the repo's 3-loop offset; Buttazzo et al. find M_t^c ~ 171.0-171.4 at 2-3 loops")

# ======================================================================= (5) evidence update


def N(x, m, s): return math.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))


dy_dmt = abs(P07["sensitivity"]["dy_dMt"])
lam_frac = math.log(Rmax / CARD["dark_dimension"]["Lambda_inv_quarter_um"] / 1e-4) / math.log(1 / 1e-4)        # log-prior lambda in [1e-4, 1]
tfr = [math.log(r["window_MeV"][1] / r["window_MeV"][0]) / math.log(60 / 5) for r in rows]
T_frac = float(np.mean(tfr))
ev = {}
for sname, smt in (("exp only (12698: 0.43)", 0.43), ("exp + scheme", math.hypot(0.43, 0.5))):
    for width in (15.0, 5.0, 2.0):
        st = math.hypot(smt, 0.1)
        bnd = N(172.57, 172.57, st) * width
        lf = np.linspace(9, 13, 4001)
        mt_pred = 172.57 + (math.log10(5.41e10) - lf) / 1.56; om_pred = 0.12 * (10 ** lf / 1.04e11) ** 1.17
        Lmt = np.exp(-0.5 * ((mt_pred - 172.57) / st) ** 2) / (st * math.sqrt(2 * math.pi))
        sl = math.hypot(0.30, 0.01); Lom = np.exp(-0.5 * (np.log(0.12 / om_pred) / sl) ** 2) / (0.12 * sl * math.sqrt(2 * math.pi))
        IA = float((Lmt * Lom).sum() * (lf[1] - lf[0]) / 4.0)
        lb = np.linspace(-3, -1, 2001); ns_pred = 0.9653 + 0.22 * 10 ** lb
        IB = float((np.exp(-0.5 * ((ns_pred - 0.9743) / 0.0034) ** 2) / (0.0034 * math.sqrt(2 * math.pi))).sum() * (lb[1] - lb[0]) / 2.0)
        A_bf = IA * IB * 0.5 * width / ((1 / 0.06) * (1 / 0.3))
        Bp = width * dy_dmt * lam_frac * T_frac
        ev[f"{sname} | width {width:g}"] = dict(boundary=bnd, boundary_trials=bnd / 8, A=A_bf, A_trials=A_bf / 8, B_prime=Bp)
        print(f"(5) {sname:24s} width {width:4g} GeV: boundary {bnd:5.2f} (/8 {bnd / 8:.2f}), A {A_bf:.2f} (/8 {A_bf / 8:.3f}), B' {Bp:.3f}")
chk = ev["exp only (12698: 0.43) | width 15"]
assert abs(chk["boundary"] - 13.5) < 0.6 and abs(chk["A"] - 2.6) < 0.4
res["evidence"] = dict(rows=ev, dy_dmt=dy_dmt, lambda_prior_fraction=lam_frac, T_RH_overlap_fraction=T_frac,
                       note="B' (dark dimension + top partner + mesogenesis) replaces B: DM generic-like (no T_i^3 tuning), penalised by the surviving "
                            "lambda range and the reheating overlap with Dark_CP's 5-60 MeV; reproduces Pass 12698 at sigma = 0.43")
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12709_round.json"), "w", encoding="utf-8"), indent=1, default=float)
print("wrote data/toe_pass12709_round.json")
