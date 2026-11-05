"""Model A in a 5D SU(5) orbifold GUT on S1/(Z2 x Z2'), Kawamura (hep-ph/9902423) and Hall-Nomura (hep-ph/0103125): boundary conditions split multiplets, so Model A's light fragments need no tuning.
(1) Exact parity table.  P = +1 on all of SU(5); P' = diag(+,+,+,-,-) on the 5.  A field in representation R with intrinsic sign eta' gets P' = eta' x product of the index parities.  A fragment has a massless mode only if (P, P') = (+, +).  For a vectorlike light pair two bulk fields are needed, with the zero-mode chiralities of opposite type: here tabulated per fragment.
    Control: gauge 24: SM (+,+), X Y (+,-); Higgs 5: doublet light, triplet heavy for eta' = -1 (the orbifold doublet-triplet splitting).
(2) Unification with the KK spectrum instead of random thresholds.  Mass levels: (+,+) 2n/R, (+,-) and (-,+) (2n+1)/R, (-,-) (2n+2)/R.  One loop: each state of mass m below mu shifts alpha_i^-1 by -b_i ln(mu/m)/(2 pi).  Coefficients: Dirac fermion 4/3 S, complex scalar 1/3 S, real scalar 1/6 S, massive vector with its eaten scalar -(11/3 - 1/6) S_adj = -7/2 S per real vector field.  Zero modes as in the SM; the light Q's get M_X from the PQ field.  Matching: at the cutoff Lambda the 5D theory is SU(5) symmetric, so require alpha_1 = alpha_2 = alpha_3 at Lambda; brane kinetic terms, which break this, are neglected (the usual assumption, with an error of order 1/(4 pi) x ln, not estimated here).  Unknowns M_X and 1/R for a chosen Lambda R in {3, 10, 30}.
    Control: Lambda R = 1, with no KK states below Lambda, must reduce to the 4D two-loop-free one-loop result of pq_unification for Model A.
(3) Proton: X, Y at 1/R.  Matter on the SU(5)-symmetric brane couples to X and gives dimension-6 decay with M_X^eff ~ 1/R (times an order-one sum over KK modes, not computed); matter on the SM brane does not couple to X at tree level, and proton decay is then suppressed.  Reported as the two cases; the 4D estimate formula is used for the first with M_V = 1/R.
usage: py -3 orbifold_gut.py"""
import json
import math
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import root

out = {}
# (1) parity table
IDX = ["c", "c", "c", "w", "w"]


def frag_parity(kind, eta):
    """kind: '5' or '10' or '24'.  returns dict fragment -> P'."""
    if kind == "5":
        return {"(3,1,-1/3)": eta * 1, "(1,2,1/2)": eta * -1}
    if kind == "10":
        return {"(3bar,1,-2/3)": eta * 1 * 1, "(3,2,1/6)": eta * 1 * -1, "(1,1,1)": eta * -1 * -1}
    if kind == "24":
        return {"(8,1,0)+(1,3,0)+(1,1,0)": eta * 1, "(3,2,-5/6)+cc": eta * -1}


tab = {}
for kind in ("5", "10", "24"):
    for eta in (1, -1):
        tab[f"{kind}_eta{eta}"] = {k: ("light" if v == 1 else "heavy (+,-)") for k, v in frag_parity(kind, eta).items()}
out["parity"] = tab
for k, v in tab.items():
    print(k, v, flush=True)
model_a = dict(five=[k for k, v in tab["5_eta1"].items() if v == "light"], ten=[k for k, v in tab["10_eta-1"].items() if v == "light"])
out["model_A_by_parity"] = model_a
print("Model A light fragments from eta' = +1 for the 5 and -1 for the 10:", model_a, flush=True)

# (2) KK unification at one loop
MZ = 91.1876
AEMI, S2, AS = 127.955, 0.23122, 0.1180
a0 = np.array([(3 / 5) * AEMI * (1 - S2), AEMI * S2, 1 / AS])
B_SM = np.array([41 / 10, -19 / 6, -7.0])


def S(c, w, y):
    T3 = {1: 0, 3: 0.5, 6: 2.5, 8: 3.0}
    T2 = {1: 0, 2: 0.5, 3: 2.0}
    return np.array([0.6 * y * y * c * w, T2[w] * c, T3[c] * w])


DQ = 4 / 3 * (S(3, 1, -1 / 3) + 2 * S(3, 2, 1 / 6))  # Model A light Dirac fermions
# KK content: list of (b vector, parity type) per KK tower
towers = []
# gauge: SM adjoint (+,+) massive levels n >= 1 at 2n/R; X,Y (+,-) at (2n+1)/R; each massive vector -7/2 S_adj
adjSM = np.array([0.0, 2.0, 3.0])  # S for SU(2) adj = 2, SU(3) adj = 3, U(1) 0
SXY = S(3, 2, -5 / 6) * 2  # complex X,Y: count both (3,2)+(3bar,2) as two real vectors per complex
towers.append((-3.5 * adjSM, "pp"))
towers.append((-3.5 * SXY, "pm"))
# Higgs 5_H bulk, eta' = -1: doublet (+,+) zero mode is the SM Higgs (already in B_SM), doublet KK 2n/R, triplet (2n+1)/R; complex scalars
towers.append((1 / 3 * S(1, 2, 1 / 2), "pp"))
towers.append((1 / 3 * S(3, 1, -1 / 3), "pm"))
# SM matter: assume on the SM brane (no KK)
# Model A bulk fermions: each light fragment has a zero mode and Dirac KK states at 2n/R; heavy partners at (2n+1)/R.  Two bulk 10s and one bulk 5, each doubled for vectorlike pairing: KK levels Dirac.
towers.append((4 / 3 * (S(3, 1, -1 / 3) + 2 * S(3, 2, 1 / 6)) * 2, "pp"))  # the KK partners of light fragments, two bulk fields each
towers.append((4 / 3 * (S(1, 2, 1 / 2) + 2 * (S(3, 1, 2 / 3) + S(1, 1, 1))) * 2, "pm"))


def ainv_at(mu, MX, invR):
    a = a0 - B_SM * math.log(mu / MZ) / (2 * math.pi)
    if mu > MX:
        a = a - DQ * math.log(mu / MX) / (2 * math.pi)
    for b, typ in towers:
        start = 2 if typ == "pp" else 1
        m = start * invR
        while m < mu:
            a = a - b * math.log(mu / m) / (2 * math.pi)
            m += 2 * invR
    return a


def solve(LR, x0):
    def f(x):
        MX, invR = math.exp(x[0]), math.exp(x[1])
        a = ainv_at(LR * invR, MX, invR)
        return [a[0] - a[1], a[1] - a[2]]
    s = root(f, x0, tol=1e-10)
    if not s.success:
        return None
    MX, invR = math.exp(s.x[0]), math.exp(s.x[1])
    a = ainv_at(LR * invR, MX, invR)
    return dict(MX=MX, invR=invR, Lambda=LR * invR, inv_alpha=float(a.mean()), spread=float(a.max() - a.min()))


rows = {}
x0 = [math.log(6.6e9), math.log(8.4e15)]
for LR in (1.0, 3.0, 10.0, 30.0, 100.0):
    r = solve(LR, x0)
    if r:
        x0 = [math.log(r["MX"]), math.log(r["invR"])]
        r["tau_brane_O"] = 1.6e36 * (r["invR"] / 1e16) ** 4 * (35 / r["inv_alpha"]) ** 2
    rows[str(LR)] = r
    print("Lambda R", LR, r, flush=True)
out["kk_unification"] = rows
out["control_LR1_vs_4D_one_loop"] = dict(orbifold=rows["1.0"], four_d=dict(MX=6.6e9, MU=8.4e15))
json.dump(out, open("orbifold_gut.json", "w"), indent=1, default=float)
