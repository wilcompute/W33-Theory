"""Which Standard Model branes allow a rolling dark dimension, and what tower coupling b does each then predict?
Set-up: string frame in 10D, dilaton plus six radii, one of them the dark radius R.  All lengths in string units, sigma_i = ln r_i, f = ln g_s.  Planck mass: M_Pl^2 / M_s^2 = exp(sum sigma_i - 2 f).  4D Einstein frame moduli metric (kinetic term (1/2)(d phi)^2 in reduced Planck units):
    ds^2 = sum_i d sigma_i^2 + 2 d phi4^2,  phi4 = f - (1/2) sum sigma_i   (the 4D dilaton)
which is the standard reduction; control: pure R with phi10 fixed in M-theory language reproduces the known 5D radion below.
Constraints on the roll, for SM on a Dp-brane wrapping p-3 of the small radii:
   alpha fixed: alpha^-1 = exp(sum_{wrapped} sigma_i - f)            (clock bound, 1e-7)
   brane scale fixed in Planck units: M_s/M_Pl fixed, i.e. sum_all sigma_i - 2 f fixed   (Cassini + LLR)
m_KK/M_Pl = exp(-sigma_R) (M_s/M_Pl), so with M_s/M_Pl fixed d ln m_KK = -d sigma_R.
For each class, b = max over allowed unit directions of |d ln m_KK / d phi|: the gradient of ln m_KK projected on the constraint surface.  This is the largest tower coupling allowed; smaller b is possible if other fields carry part of the motion.
Then compare with the swampland bound b >= 1/sqrt(d-2) = 1/sqrt 2 (Etheredge et al 2022, sharpened distance conjecture), and with the b the N-body and fits used, 1/sqrt 2 and sqrt(3/2).
Also the Hořava-Witten row, by the same metric with no free dilaton.
usage: py -3 dd_brane_classes.py"""
import json
import math
import numpy as np


def metric():
    """coordinates (sigma_R, sigma_1..sigma_5, f).  Kinetic: L = (1/2) G dq dq in reduced Planck units."""
    G = np.zeros((7, 7))
    for i in range(6):
        G[i, i] = 1.0
    v = np.r_[-0.5 * np.ones(6), 1.0]  # d phi4 = df - (1/2) sum d sigma
    G += 2 * np.outer(v, v)
    return G


def best_b(constraints, grad, G):
    """largest |grad.q| over q with q^T G q = 1 and C q = 0.  grad, C are covectors."""
    Gi = np.linalg.inv(G)
    C = np.array(constraints) if len(constraints) else np.zeros((0, G.shape[0]))
    g = np.array(grad, float)
    if len(C):
        A = C @ Gi @ C.T
        lam = np.linalg.lstsq(A, C @ Gi @ g, rcond=None)[0]
        gp = g - C.T @ lam
    else:
        gp = g
    return math.sqrt(max(gp @ Gi @ gp, 0.0)), Gi @ gp


G = metric()
sum_all = np.r_[np.ones(6), -2.0]  # ln (M_Pl/M_s)^2
grad_mKK_free = -np.r_[1.0, np.zeros(6)] - 0.5 * sum_all  # ln m_KK/M_Pl = -sigma_R - (1/2) ln(M_Pl/M_s)^2
out = {}
# controls: radion at fixed everything else, in M_D units with dilaton adjusted.
# (a) unconstrained gradient must give |grad ln m_KK|^2 = 3/2 for any n, Pass 12548
b0, _ = best_b([], grad_mKK_free, G)
out["control_free_gradient_b2"] = b0 ** 2
# (b) M_s fixed only: b^2 = n/(n+1) with n small dimensions at fixed dilaton is Pass 12548; here dilaton also free
rows = {}
for p in (3, 4, 5, 6, 7, 8, 9):
    k = p - 3  # wrapped small radii
    if k > 5:
        continue
    wrapped = np.r_[0.0, np.ones(k), np.zeros(5 - k), -1.0]  # ln 1/alpha
    grad = -np.r_[1.0, np.zeros(6)]
    b, q = best_b([wrapped, sum_all], grad_mKK_free, G)
    b_fix_dil, _ = best_b([wrapped, sum_all, np.r_[np.zeros(6), 1.0]], grad_mKK_free, G)
    rows[f"D{p}"] = dict(wrapped_radii=k, b_max=b, b2=b ** 2, dsigma_R=float(q[0] / b), dsigma_small=[float(x / b) for x in q[1:6]], df=float(q[6] / b), b_max_dilaton_fixed=b_fix_dil, passes_sharpened_SDC=bool(b >= 1 / math.sqrt(2) - 1e-12))
# brane wrapping the dark dimension too: alpha depends on sigma_R
for k in (0, 1):
    wrapped = np.r_[1.0, np.ones(k), np.zeros(5 - k), -1.0]
    b, q = best_b([wrapped, sum_all], grad_mKK_free, G)
    rows[f"wraps_R_plus_{k}"] = dict(b_max=b, b2=b ** 2)
out["D_branes"] = rows

# Horava-Witten: 11D, coordinates (ln rho, ln V) with six equal CY radii, metric as dd_geometry: ds^2 = sum d sigma_i^2 + (1/2)(sum d sigma_i)^2
G11 = np.zeros((7, 7))
G11 += np.eye(7) + 0.5 * np.ones((7, 7))
sum11 = np.ones(7)
vol6 = np.r_[0.0, np.ones(6)]
grad11 = -np.r_[1.0, np.zeros(6)] - 0.5 * sum11
b_free, _ = best_b([], grad11, G11)
out["HW"] = dict(control_free_b2=b_free ** 2, with_V_fixed=best_b([vol6], grad11, G11)[0], note="both constraints set d ln rho = 0: rank check below")
C = np.array([vol6, sum11])
out["HW"]["rho_direction_allowed"] = bool(abs(best_b([vol6, sum11], grad11, G11)[0]) > 1e-9)
out["HW"]["b_with_both_constraints"] = best_b([vol6, sum11], grad11, G11)[0]

# Fit-relevant number: for a given b, the Casimir slope and c/c' relation.  V_C prop e^{-4 b phi}; c_eff = 4 b eps; c' = f b, so c/c' = 4 eps / f independent of b.
tab = {}
for name, b in (("1/sqrt2", 1 / math.sqrt(2)), ("sqrt(5/6)", math.sqrt(5 / 6)), ("1", 1.0), ("sqrt(3/2)", math.sqrt(1.5))):
    tab[name] = dict(b=b, c_bare=4 * b, f_for_cprime_005=0.05 / b, c_eff_at_eps_033=4 * b * 0.33, c_over_cprime=4 * 0.33 / (0.05 / b))
out["casimir_relation"] = tab
out["TCC_bound"] = 2 / math.sqrt(6)

# radion floor if the radius is frozen on an E8 wall
HC = 0.1973269804  # eV micron
MP = 2.435e27  # eV
beta = 1 / math.sqrt(6)
floor = {}
for lam in (40.0, 30.0, 50.0):  # microns: rough Yukawa bound at alpha = 1/3 from sub-mm tests; memory, not re-read
    m = HC / lam
    rho4 = (m * MP / (4 * beta)) ** 2  # m^2 = (n beta)^2 rho / M^2 for a term rho e^{n beta phi} with n = 4
    floor[str(lam)] = dict(m_eV=m, stabiliser_scale_TeV=rho4 ** 0.25 / 1e12)
floor_ew = dict(rho_EW_GeV4=0.13 / 4 * 246.22 ** 4)
floor_ew["m_eV"] = 4 * beta * math.sqrt(floor_ew["rho_EW_GeV4"]) * 1e18 / MP
floor_ew["range_micron"] = HC / floor_ew["m_eV"]
out["radion_floor"] = dict(needed=floor, from_EW_vacuum_energy=floor_ew)

# bubble of nothing: Witten 1982, 5D, B = pi R^2 / (4 G_4) = 2 pi^2 M_bar^2 R^2.  Exists for antiperiodic fermions (omega = 1/2) on a circle.
bon = {}
for R in (10.0, 15.0):
    Re = R / HC
    B = 2 * math.pi ** 2 * (MP * Re) ** 2
    bon[str(R)] = dict(M_R=MP * Re, B=B, log10_B=math.log10(B))
# how small must R be for the bounce to matter, B ~ 400 (lifetime ~ age of the universe in Planck units)
bon["R_for_B400_Planck_lengths"] = math.sqrt(400 / (2 * math.pi ** 2))
out["bubble_of_nothing"] = bon
json.dump(out, open("dd_brane_classes.json", "w"), indent=1, default=float)


def f(x):
    if isinstance(x, float):
        return float(f"{x:.4g}")
    if isinstance(x, dict):
        return {k: f(v) for k, v in x.items()}
    if isinstance(x, list):
        return [f(v) for v in x]
    return x


for k, v in out.items():
    print(k, f(v))
