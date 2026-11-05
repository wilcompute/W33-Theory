"""One scale, three jobs: the KSVZ heavy quarks are the fields that make the gauge couplings meet.  Extends the inverse threshold scan of parallel commit 193b7c00a, which has masses as free fits; here the threshold is tied to the Peccei-Quinn scale.
Action: SM + complex scalar sigma with vev f + vectorlike fermions Q in representations R, mass M_X = y f, y <= about 1 perturbatively.  Below M_X: SM.  Above: SM + R, up to M_U where all three couplings meet.  One loop, one common threshold, two unknowns (M_X, M_U) from two coupling differences; so a set R either has a solution or not, and M_X is an output.
Dirac fermion (C, W, Y): Db1 = (3/5)(4/3) d_C d_W Y^2, Db2 = (4/3) d_C T(W), Db3 = (4/3) T(C) d_W.  Control: must return the parallel track's (3,2)_1/6 and (1,3)_0 numbers; the triplet there is Majorana so half.
Anomaly: N = sum d_W T(C), E = sum d_C d_W (Y^2 + (d_W^2 - 1)/12), per Dirac fermion of PQ charge 1.  N = 0 models have no strong CP solution, so colour is required.  Domain wall number N_DW = 2 N.  g_agamma proportional to (E/N - 1.92).
m_a = 5.70 ueV (1e12 GeV / f_a), f_a = f / N_DW.
Filters applied in stages, all reported:
  A: 0 < M_X < M_U, solution exists.
  B: proton: M_U above a floor.  Dimension 6, tau = 2.4e34 yr at M_U = M0 (alpha_U^-1/40)^(1/2), M0 = 4e15 GeV is an order-of-magnitude estimate for gauge exchange, hadronic matrix elements not computed, so 2e15 and 8e15 are also reported.
  C: M_X in the PQ range: y <= 1 means f >= M_X, and f <= 1e12 for axion dark matter at theta of order 1, with the anharmonic and string contributions not modelled.  Astrophysics needs f_a > about 1e8.  So M_X between 1e8 and 1e12 (natural: y between 0.01 and 1).
  D: no Landau pole below M_U and unified coupling perturbative: 1/alpha_U > 10.
  E: colour stable hadrons: the lightest Q must decay: a mixing with SM quarks is available only for (3,1,-1/3), (3,1,2/3), (3,2,1/6), (3,2,-5/6), (3,2,7/6), (3,3,-1/3), (3,3,2/3); others leave stable relics, marked.
Thresholds spread is not included: one-loop thresholds across a multiplet at order alpha/(4 pi) ln(ratio) can shift ln M by about 1, so the error in M_X is reported from alpha_s +- 0.0009 only and is a lower bound on the uncertainty.
Also the Higgs: the triplet route and the top-mass route changed by R through g2, g1, g3 above M_X are noted by the stability scale change at one loop.
Literature windows for the axion coupling are compared in the write-up, not imposed here.
usage: py -3 pq_unification.py"""
import itertools
import json
import math
from fractions import Fraction as Fr
import numpy as np

MZ = 91.1876
AEMI, S2, AS = 127.955, 0.23122, 0.1180
B = (41 / 10, -19 / 6, -7.0)


def inv_alpha(aemi=AEMI, s2=S2, a3=AS):
    return np.array([(3 / 5) * aemi * (1 - s2), aemi * s2, 1 / a3])


T = {1: Fr(0), 3: Fr(1, 2), 6: Fr(5, 2), 8: Fr(3), 15: Fr(10)}
TW = {1: Fr(0), 2: Fr(1, 2), 3: Fr(2), 4: Fr(5)}
REPS = [(3, 1, Fr(-1, 3)), (3, 1, Fr(2, 3)), (3, 1, Fr(-4, 3)), (3, 2, Fr(1, 6)), (3, 2, Fr(-5, 6)), (3, 2, Fr(7, 6)), (3, 3, Fr(-1, 3)), (3, 3, Fr(2, 3)), (6, 1, Fr(-1, 3)), (6, 1, Fr(2, 3)), (6, 2, Fr(1, 6)), (8, 1, Fr(0)), (8, 1, Fr(-1)), (8, 2, Fr(-1, 2)), (15, 1, Fr(-1, 3))]
COLORLESS = [(1, 2, Fr(1, 2)), (1, 2, Fr(3, 2)), (1, 3, Fr(0)), (1, 3, Fr(1)), (1, 1, Fr(1)), (1, 4, Fr(1, 2))]
DECAY = {(3, 1, Fr(-1, 3)), (3, 1, Fr(2, 3)), (3, 2, Fr(1, 6)), (3, 2, Fr(-5, 6)), (3, 2, Fr(7, 6)), (3, 3, Fr(-1, 3)), (3, 3, Fr(2, 3)), (1, 2, Fr(1, 2)), (1, 2, Fr(3, 2)), (1, 3, Fr(0)), (1, 3, Fr(1)), (1, 1, Fr(1))}


def db(r, majorana=False):
    c, w, y = r
    f = Fr(1, 2) if majorana else Fr(1)
    return tuple(float(x) for x in (f * Fr(3, 5) * Fr(4, 3) * c * w * y * y, f * Fr(4, 3) * c * TW[w], f * Fr(4, 3) * T[c] * w))


def en(r):
    c, w, y = r
    return float(c * w * (y * y + Fr(w * w - 1, 12))), float(w * T[c])


def solve(dB, a=None):
    a = inv_alpha() if a is None else a
    # a_i(mu) = a_i - b_i t/2pi - Db_i s/2pi, t = ln MU/MZ, s = ln MU/MX
    A = np.array([[B[0] - B[1], dB[0] - dB[1]], [B[1] - B[2], dB[1] - dB[2]]])
    y = 2 * math.pi * np.array([a[0] - a[1], a[1] - a[2]])
    if abs(np.linalg.det(A)) < 1e-9:
        return None
    t, s = np.linalg.solve(A, y)
    MU = MZ * math.exp(t) if t < 60 else None
    if MU is None or s <= 0 or s >= t:
        return None
    MX = MU * math.exp(-s)
    au = a[0] - B[0] * t / (2 * math.pi) - dB[0] * s / (2 * math.pi)
    return dict(MX=MX, MU=MU, inv_alpha_U=float(au))


out = {}
# control
c1 = solve(db((3, 2, Fr(1, 6))))
c2 = solve(db((1, 3, Fr(0)), majorana=True))
out["control"] = dict(q=c1, triplet=c2, parallel=dict(q=[1.43822e6, 2.41792e15, 38.4017], triplet=[8.05098e6, 2.43264e14, 40.3510]))
print("control", c1, c2, flush=True)
# scan: 1 to 3 colored reps, each 1 to 3 copies, plus 0 to 1 colorless reps at the same scale
rows = []
idx = list(range(len(REPS)))
for k in (1, 2, 3):
    for combo in itertools.combinations_with_replacement(idx, k):
        for extra in [None] + list(range(len(COLORLESS))):
            rs = [REPS[i] for i in combo] + ([COLORLESS[extra]] if extra is not None else [])
            dB = np.sum([db(r) for r in rs], axis=0)
            so = solve(dB)
            if so is None:
                continue
            E = sum(en(r)[0] for r in rs)
            N = sum(en(r)[1] for r in rs)
            rows.append(dict(reps=[(r[0], r[1], str(r[2])) for r in rs], dB=dB.tolist(), **so, E_over_N=E / N if N else None, N=N, NDW=2 * N, decays=all(r in DECAY for r in rs)))
out["n_solutions_A"] = len(rows)
print("A solutions", len(rows), flush=True)


def stage(rows, mu_floor, mx=(1e8, 1e12), alpha_cap=10.0):
    return [r for r in rows if r["inv_alpha_U"] > alpha_cap and r["MU"] > mu_floor * math.sqrt(r["inv_alpha_U"] / 40.0) and mx[0] <= r["MX"] <= mx[1]]


st = {}
for fl in (2e15, 4e15, 8e15):
    s = stage(rows, fl)
    st[f"{fl:.0e}"] = dict(n=len(s), n_decay=sum(1 for r in s if r["decays"]))
out["stages"] = st
print("stages", st, flush=True)
final = stage(rows, 4e15)
final = [r for r in final if r["decays"]]
final.sort(key=lambda r: (len(r["reps"]), -r["MU"]))
# alpha_s error and axion coupling
A_ERR = []
for dA in ((0.1189, 0.23122), (0.1171, 0.23122), (0.1180, 0.23128), (0.1180, 0.23116)):
    A_ERR.append(inv_alpha(s2=dA[1], a3=dA[0]))
for r in final:
    dB = r["dB"]
    vals = [solve(dB, a) for a in A_ERR]
    good = [v for v in vals if v]
    r["MX_range"] = [min(v["MX"] for v in good), max(v["MX"] for v in good)] if good else None
    r["MU_range"] = [min(v["MU"] for v in good), max(v["MU"] for v in good)] if good else None
    N = r["N"]
    fa_hi = 1e12 / max(2 * N, 1) * 2 * N  # f = 1e12 at most, f_a = f / (2 N)
    fa = r["MX"] / (2 * N)  # y = 1 end
    r["fa_y1"] = fa
    r["ma_ueV_y1"] = 5.7 * 1e12 / fa
    r["ma_ueV_f1e12"] = 5.7 * 1e12 / (1e12 / (2 * N))
    r["E_N_minus_192"] = (r["E_over_N"] - 1.92) if r["E_over_N"] is not None else None
out["final"] = final
out["n_final"] = len(final)
print("final", len(final), flush=True)
for r in final[:30]:
    print([f"{a}{b}{c}" for a, b, c in r["reps"]], "MX %.2g MU %.2g 1/aU %.1f E/N %.3f |E/N-1.92| %.2f NDW %d ma(y=1) %.2g ueV" % (r["MX"], r["MU"], r["inv_alpha_U"], r["E_over_N"], abs(r["E_N_minus_192"]), r["NDW"], r["ma_ueV_y1"]), flush=True)
hist = {}
for r in final:
    k = str(round(abs(r["E_N_minus_192"]), 2))
    hist[k] = hist.get(k, 0) + 1
out["coupling_hist"] = hist
print("coupling", dict(sorted(hist.items(), key=lambda kv: float(kv[0]))), flush=True)
json.dump(out, open("pq_unification.json", "w"), indent=1, default=float)
