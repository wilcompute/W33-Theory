"""12459: can large-volume thresholds unify SM_2541_c22 with k_Y >= 11/3?  Same machinery as 12359 (thresholds.py): DKL large-volume form
4 pi/alpha_a(M_Z) = k_a 4 pi/alpha_s + b_a^low ln(M_s^2/M_Z^2) + sum_i c_i b_a^(i) x_i,  x_i = (pi/3) T2^(i),
c = 1/2 for the theta^2 sub-orbifold (file c22__t3: Geometry sub2, W lines on its fixed torus off) and 1/3 for theta^3 (c22__t2: sub3).
6D coefficients from the weights of the 6D massless spectra (beta.py of 12359), for EACH of the six enumerated anomaly-free hypercharges
of c22 (12444b).  Three equations, three unknowns (1/alpha_s, x_A, x_B): generically an exact solution exists, so the question is whether
it is PHYSICAL: x_i >= 0 (large volume) and alpha_s perturbative.  Control: the parent spectrum through the same weight code must give the
SM-like low-energy coefficients when restricted to the three chiral generations + Higgs (checked separately: b2, b3 of the full massless
spectrum are printed).  Argued, not computed: validity of DKL for the non-SUSY orbifold (12359)."""
import json, math, sys
import numpy as np
import sympy as sp
D = '../search_drivers_12373/'
my = json.load(open(D + 'multiY_Z6II_06_SM_20260917_2541_c22.json'))


def roots(p):
    return [[[sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in r.split()] for r in l.split('|')[1:]]
            for l in open(p, errors='ignore') if l.startswith('FACTOR')]


par = roots(D + 'spec/Z6II_06_SM_20260917_2541_c22.nsoq')
a3, a2 = par[4][0], par[5][0]
W = {13: sp.Rational(-11, 3), 19: sp.Rational(2, 3), 15: sp.Rational(1, 6), 16: sp.Rational(1, 6)}


def beta(p, Y):
    b = [sp.Integer(0)] * 3; cur = None
    for l in open(p, errors='ignore'):
        if l.startswith('FIELD'):
            cur = int(l.split()[2][2:])
        elif l.startswith('W ') and cur in W:
            P = [sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in l[2:].split(',')]
            y = sum(x * c for x, c in zip(P, Y)); d2 = sum(x * c for x, c in zip(P, a2)); d3 = sum(x * c for x, c in zip(P, a3))
            b[0] += W[cur] * y ** 2; b[1] += W[cur] * d2 ** 2 / 4; b[2] += W[cur] * d3 ** 2 / 4
    return b


MZ = 91.1876; ainv_em, s2, as_ = 127.95, 0.2312, 0.1180
ainv = [ainv_em * (1 - s2), ainv_em * s2, 1 / as_]
bSM = [41 / 6, -19 / 6, -7]
out = []
for row in my:
    Y = [sp.Rational(x) for x in row['t']]; kY = float(sp.Rational(row['kY']))
    bA = [float(v) for v in beta(D + 'c22__t3.nsoq', Y)]; bB = [float(v) for v in beta(D + 'c22__t2.nsoq', Y)]
    bP = [float(v) for v in beta(D + 'spec/Z6II_06_SM_20260917_2541_c22.nsoq', Y)]
    rec = dict(kY=row['kY'], b6_theta2=bA, b6_theta3=bB, b_parent_massless=bP)
    for low_name, bl in (('SM', bSM), ('full', bP)):
        u = 25.0
        for _ in range(300):
            gs = math.sqrt(4 * math.pi / u); Ms = 0.527 * gs * 1e18; L = math.log(Ms / MZ)
            M = np.array([[kY, 1, 1], [bA[a] / 2 / (4 * math.pi) for a in range(3)], [bB[a] / 3 / (4 * math.pi) for a in range(3)]]).T
            rhs = np.array([ainv[a] - bl[a] / (2 * math.pi) * L for a in range(3)])
            sol = np.linalg.solve(M, rhs)
            u = max(sol[0], 1.0)
        # control: no thresholds -> least-squares residual of the k_Y mismatch alone
        r0 = rhs - np.outer([kY, 1, 1], [1]).ravel() * (np.dot([kY, 1, 1], rhs) / np.dot([kY, 1, 1], [kY, 1, 1]))
        rec[low_name] = dict(inv_alpha_s=round(float(sol[0]), 3), x_theta2=round(float(sol[1]), 3), x_theta3=round(float(sol[2]), 3),
                             T2_theta2=round(3 * float(sol[1]) / math.pi, 3), T2_theta3=round(3 * float(sol[2]) / math.pi, 3),
                             physical=bool(sol[0] > 1 and sol[1] >= 0 and sol[2] >= 0), no_threshold_resid=round(float(abs(r0).max()), 2),
                             cond=round(float(np.linalg.cond(M)), 1))
    out.append(rec)
    print(row['kY'], 'b6A', [round(v, 2) for v in bA], 'b6B', [round(v, 2) for v in bB], '| SM', rec['SM'], '| full', rec['full'], flush=True)
json.dump(out, open('thresholds_c22.json', 'w'), indent=1)
