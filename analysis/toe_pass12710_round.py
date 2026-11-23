"""Pass 12710 (Claude track): five follow-ups to Pass 12709.
 (1) Short-range gravity vs B' (R = 0.009-0.2 um): KK Yukawa alpha = 8/3 (one flat dimension; 2n in another convention), lambda = R.
     Sensitivity floor estimated from first principles: Yukawa pressure between gold half-spaces P_Y = 2 pi G rho^2 alpha lambda^2 e^{-d/lambda}
     vs Casimir pressure pi^2 hbar c / (240 d^4) at d = lambda, with 1% Casimir precision and a 10^3-10^4 isoelectronic suppression.
 (2) B''s mesogenesis mediator: the operator psi b u d needs a coloured scalar Y (3, 1, -1/3) (it cannot be the vectorlike fermion).
     Its Higgs portal lambda_HY |H|^2 |Y|^2 adds +3 K lambda_HY^2 to beta_lambda above M_Y (and Delta b3 = 1/6, Delta b_Y = 1/9):
     y'_B as a function of lambda_HY at M_Y = 2 TeV.
 (3) Hybrid in the evidence table (Pass 12709 setup): dy'/dm_t at M_SS = 1e10; with and without the light-Q+U tuning penalty
     (M_VL/M_GUT)^2 for the two tuned couplings of Pass 12705.
 (4) Warped throat at fixed KK spacing m_KK = 1 eV (the 2610.01825 bound applies to the spacing): species scale M5 from
     M_Pl^2 = (M5^3/k)(1 - e^{-2kL}), m_1 ~ x(kL) k/(e^{kL}-1) (x: pi flat -> 3.83 RS); y' for SM on the UV brane (cutoff M5) and on
     the IR brane (cutoff M5 e^{-kL}).
 (5) Face-pairing the 40 W33 tetrahedra into a closed 3-pseudomanifold: faces = flags (p, L) (triangle L minus p); at each point p pair
     its 4 lines (3 matchings) and glue the faces by a bijection (6 per pair).  Random search for a 3-manifold (every vertex link a
     connected 2-sphere); chi, orientability.
usage: py -3 analysis/toe_pass12710_round.py"""
import itertools, json, math, os, random
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CARD = json.load(open(os.path.join(HERE, "toe_inputs_card.json"), encoding="utf-8"))
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, beta_vl, OFF3, M5f = (G[k] for k in ("initial", "beta_sm", "beta_vl", "OFF3", "M5"))
K = 1 / (16 * math.pi ** 2); NC = 3; MT, A3, MVL = 172.57, 0.1180, 1740.0; MPL = 2.435e18; HBARC = 1.97327e-16
res = {}
dl_full = lambda y: (5 / 6) * NC * K * y[5] ** 4 - 2 * y[4] * NC * K * y[5] ** 2 / 3     # Pass 12707 threshold (lambda_VL - lambda_SM)


def run(Mt, a3, yp, mu_max, lamHY=0.0, MY=2000.0, withY=False):
    Mt0 = Mt - OFF3; kw = dict(rtol=1e-9, atol=1e-12, max_step=0.5)
    y = solve_ivp(lambda t, y: beta_sm(*y[:5]) + [0.0], (0, math.log(MVL / Mt0)), np.array(initial(Mt, 125.20, a3) + [yp]), **kw).y[:, -1].copy()
    y[4] += dl_full(y)

    def rhs(t, y):
        d = list(beta_vl(*y))
        if withY and Mt0 * math.exp(t) > MY:
            d[4] += 3 * K * lamHY ** 2; d[2] += K * y[2] ** 3 / 6; d[0] += K * y[0] ** 3 / 9
        return d
    return solve_ivp(rhs, (math.log(MVL / Mt0), math.log(mu_max / Mt0)), y, **kw).y[:, -1]


ypt = lambda tgt, Mt=MT, a3=A3, **kw: brentq(lambda p: run(Mt, a3, p, tgt, **kw)[4], 0.2, 1.0, xtol=1e-6)

# ======================================================================= (1) short-range gravity
Gn, rho = 6.674e-11, 19300.0
cas = []
for lam_nm in (8.8, 26.3, 87.7, 200.0, 1000.0):
    lam = lam_nm * 1e-9
    PY = 2 * math.pi * Gn * rho ** 2 * lam ** 2 * math.exp(-1)          # alpha = 1, d = lambda
    PC = math.pi ** 2 * 1.0546e-34 * 2.998e8 / (240 * lam ** 4)
    a_direct = 0.01 * PC / PY
    cas.append(dict(lambda_nm=lam_nm, P_yukawa_alpha1_Pa=PY, P_casimir_Pa=PC, alpha_floor_direct=a_direct,
                    alpha_floor_isoelectronic=[a_direct / 1e4, a_direct / 1e3], gap_vs_8_3=a_direct / 1e4 / (8 / 3)))
    print(f"(1) lambda = R = {lam_nm:6.1f} nm: Casimir {PC:.1e} Pa vs Yukawa(alpha=1) {PY:.1e} Pa -> alpha floor ~{a_direct:.0e} (direct), "
          f"~{a_direct / 1e4:.0e}-{a_direct / 1e3:.0e} (isoelectronic); B' needs alpha = 8/3: gap >= {a_direct / 1e4 / (8 / 3):.0e}")
res["short_range"] = dict(rows=cas, alpha_B=8 / 3,
                          note="order-of-magnitude floors (1% Casimir precision, 1e3-1e4 isoelectronic suppression); published limits in 1704.02920 are figures only")

# ======================================================================= (2) mediator portal
tB = M5f(0.0877e-6)
base = ypt(tB)
port = []
for MY in (2000.0, 5000.0):
    baseY = ypt(tB, withY=True, MY=MY)
    for lh in (0.0, 0.03, 0.1, 0.3):
        y = ypt(tB, lamHY=lh, withY=True, MY=MY)
        port.append(dict(M_Y=MY, lambda_HY=lh, yB=y, shift_vs_noY=y - base, shift_vs_Y0=y - baseY))
        print(f"(2) coloured mediator Y({MY / 1e3:.0f} TeV), portal lambda_HY = {lh:.2f}: y'_B(R = 0.088 um) = {y:.4f} "
              f"(vs no mediator {y - base:+.4f}; gauge-only part {baseY - base:+.4f})")
baseY = ypt(tB, withY=True)
lim = brentq(lambda lh: ypt(tB, lamHY=lh, withY=True) - baseY - 0.0036, 0.0, 0.3, xtol=1e-4)
print(f"(2) with Y at 2 TeV the portal must satisfy |lambda_HY| <= {lim:.3f} to move y' by less than the FCC-era error (0.0036)")
res["mediator"] = dict(rows=port, lambda_HY_max_for_FCC_sigma=lim, y_noY=base,
                       note="psi b u d needs a scalar Y(3,1,-1/3) (Elor-Escudero-Nelson); a vectorlike fermion cannot mediate it at tree level")

# ======================================================================= (3) hybrid evidence
dyH = abs(ypt(1e10, Mt=MT + 0.1) - ypt(1e10, Mt=MT - 0.1)) / 0.2
P09 = json.load(open(os.path.join(ROOT, "data", "toe_pass12709_round.json"), encoding="utf-8"))
tune = (MVL / 4e16) ** 2
hyb = {}
for width in (15.0, 5.0, 2.0):
    free = width * dyH
    hyb[f"width {width:g}"] = dict(hybrid_symmetric=free, hybrid_tuned=free * tune,
                                   B_prime=P09["evidence"]["rows"][f"exp + scheme | width {width:g}"]["B_prime"])
    print(f"(3) width {width:4g} GeV: hybrid {free:.2f} (light Q+U explained by a symmetry) / {free * tune:.1e} (two tunings ~ (M_VL/M_GUT)^2); "
          f"B' {hyb[f'width {width:g}']['B_prime']:.3f}")
res["hybrid_evidence"] = dict(dy_dmt=dyH, tuning_penalty=tune, rows=hyb,
                              note="hybrid DM generic-like; the M_SS <= mu_0 condition is automatic for M_SS = 1e10 at the central m_t")

# ======================================================================= (4) warped throat
mKK = 1e-9                                                       # GeV (1 eV)
warp = []
for kL in (0.0, 1.0, 3.0, 10.0, 20.0, 30.0):
    x = math.pi + (3.8317 - math.pi) * (1 - math.exp(-kL))
    if kL == 0:
        L = math.pi / mKK; M5 = (MPL ** 2 / (2 * L)) ** (1 / 3); cutIR = M5
    else:
        k = mKK * (math.exp(kL) - 1) / x; L = kL / k
        M5 = (MPL ** 2 * k / (1 - math.exp(-2 * kL))) ** (1 / 3); cutIR = M5 * math.exp(-kL)
    yUV = ypt(M5) if M5 < 1e17 else float("nan")
    yIR = ypt(cutIR) if 3e3 < cutIR < 1e17 else float("nan")
    warp.append(dict(kL=kL, L_um=L * HBARC * 1e6, M5=M5, cut_IR=cutIR, y_UV=yUV, y_IR=yIR))
    print(f"(4) kL = {kL:4.1f}: L = {L * HBARC * 1e6:.2e} um, M5 = {M5:.2e}, IR cutoff {cutIR:.2e} GeV: y'(SM on UV brane) = {yUV:.4f}, y'(IR brane) = {yIR:.4f}")
res["warped"] = dict(rows=warp, m_KK_eV=1.0,
                     note="flat limit reproduces Pass 12707 (R = 0.2 um, y' = 0.505); warping moves y' down (UV brane, toward the hybrid's 0.470) or up "
                          "(IR brane): B' predicts y' only once the throat and SM location are fixed")

# ======================================================================= (5) face-pairing W33 tetrahedra
pts = sorted({tuple((x * (1 if next(y for y in v if y) == 1 else 2)) % 3 for x in v) for v in itertools.product(range(3), repeat=4) if any(v)})
J = lambda x, y: (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3
adj = lambda i, j: J(pts[i], pts[j]) == 0
lines = [q for q in itertools.combinations(range(40), 4) if all(adj(a, b) for a, b in itertools.combinations(q, 2))]
assert len(lines) == 40
through = {p: [i for i, L in enumerate(lines) if p in L] for p in range(40)}
MATCH = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]


class UF:
    def __init__(s): s.p = {}
    def f(s, x):
        s.p.setdefault(x, x)
        while s.p[x] != x: s.p[x] = s.p[s.p[x]]; x = s.p[x]
        return x
    def u(s, a, b): s.p[s.f(a)] = s.f(b)


def build(rng):
    uf = UF(); glue = []
    for p in range(40):
        ls = through[p]; m = MATCH[rng.randrange(3)]
        for a, b in m:
            La, Lb = ls[a], ls[b]
            fa = [x for x in lines[La] if x != p]; fb = [x for x in lines[Lb] if x != p]
            perm = rng.sample(fb, 3); phi = dict(zip(fa, perm))
            glue.append((La, Lb, p, phi))
            for r in (1, 2, 3):
                for S in itertools.combinations(fa, r):
                    uf.u((La, frozenset(S)), (Lb, frozenset(phi[s] for s in S)))
    cls = {d: {uf.f((t, frozenset(S))) for t in range(40) for S in itertools.combinations(lines[t], d)} for d in (1, 2, 3)}
    V, E, F = len(cls[1]), len(cls[2]), len(cls[3])
    chi = V - E + F - 40
    # links: for each vertex class, link triangles = (tet, slot) in class; connectivity through glued faces containing the slot
    luf = UF(); vmem = {}
    for t in range(40):
        for s in lines[t]:
            vmem.setdefault(uf.f((t, frozenset([s]))), []).append((t, s))
    for La, Lb, p, phi in glue:
        for s, s2 in phi.items():
            luf.u((La, s), (Lb, s2))
    return V, E, F, chi, glue, uf, cls, vmem, luf


def links(glue, uf, cls, vmem, luf):
    rep = {}
    for t in range(40):
        for d in (2, 3):
            for S in itertools.combinations(lines[t], d):
                rep.setdefault(uf.f((t, frozenset(S))), (t, S))
    out = []
    for v, corners in vmem.items():
        ends = sum(sum(1 for s in S if uf.f((t, frozenset([s]))) == v) for c, (t, S) in rep.items() if len(S) == 2)
        tri = sum(sum(1 for s in S if uf.f((t, frozenset([s]))) == v) for c, (t, S) in rep.items() if len(S) == 3)
        out.append(dict(chi_link=ends - tri + len(corners), components=len({luf.f(c) for c in corners})))
    return out


rng = random.Random(12710); best = None; stats = []
for trial in range(400):
    V, E, F, chi, glue, uf, cls, vmem, luf = build(rng)
    lk = links(glue, uf, cls, vmem, luf)
    nsph = sum(1 for l in lk if l["chi_link"] == 2 and l["components"] == 1)
    stats.append((chi, nsph, V))
    if best is None or (nsph / V, -abs(chi)) > (best["sphere_frac"], -abs(best["chi"])):
        best = dict(trial=trial, V=V, E=E, F=F, T=40, chi=chi, sphere_links=nsph, sphere_frac=nsph / V, manifold=nsph == V,
                    link_chis=sorted({l["chi_link"] for l in lk}))
assert all(F == 80 for F in [best["F"]])
chis = [s[0] for s in stats]
print(f"(5) 400 random flag face-pairings: F = 80 always (closed pseudomanifold); chi range {min(chis)}..{max(chis)}, vertex classes "
      f"{min(s[2] for s in stats)}..{max(s[2] for s in stats)}; best: V={best['V']} E={best['E']} chi={best['chi']}, "
      f"{best['sphere_links']}/{best['V']} sphere links, link chis {best['link_chis']} -> manifold: {best['manifold']}")
res["face_pairing"] = dict(trials=400, chi_range=[min(chis), max(chis)], best=best,
                           note="each glued tetrahedron pair identifies vertices across lines, collapsing the 40 points; a 3-manifold needs chi = 0 and "
                                "every link a connected sphere")
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12710_round.json"), "w", encoding="utf-8"), indent=1, default=float)
print("wrote data/toe_pass12710_round.json")
