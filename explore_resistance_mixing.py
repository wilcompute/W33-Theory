#!/usr/bin/env python3
"""
Resistance distance, Kirchhoff index, random walk mixing time,
and information-theoretic invariants of W(3,3).
"""

import numpy as np
import itertools
from collections import defaultdict
from fractions import Fraction

# Build W(3,3)
J = np.array([[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]], dtype=int)
def symp_form(u, v):
    return int(np.dot(u, np.dot(J, v))) % 3

points = []
for combo in itertools.product(range(3), repeat=4):
    if any(x != 0 for x in combo):
        v = np.array(combo, dtype=int)
        for i in range(4):
            if v[i] != 0:
                if v[i] == 1:
                    points.append(v.copy())
                break

n = len(points)
A = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if symp_form(points[i], points[j]) == 0:
            A[i,j] = A[j,i] = 1

k = int(A.sum(axis=1)[0])

print("=" * 70)
print(" RESISTANCE DISTANCE, MIXING TIME, AND INFORMATION THEORY: W(3,3)")
print("=" * 70)

# ========================================================
# 1. Kirchhoff Index (Resistance Distance Sum)
# ========================================================
print(f"\n[1] Kirchhoff Index (Total Effective Resistance)")

# For a connected k-regular graph with n vertices and Laplacian eigenvalues
# 0 = μ_0 < μ_1 ≤ ... ≤ μ_{n-1}:
# Kf = n * Σ_{i=1}^{n-1} 1/μ_i

# Laplacian spectrum: {0^1, 10^24, 16^15}
Kf = n * (24 / 10 + 15 / 16)
print(f"    Kf(W) = n * Σ 1/μ_i = 40 * (24/10 + 15/16)")
print(f"    = 40 * ({24/10} + {15/16})")
print(f"    = 40 * {24/10 + 15/16}")
Kf_exact = Fraction(40) * (Fraction(24, 10) + Fraction(15, 16))
print(f"    = {Kf_exact}")
print(f"    = {float(Kf_exact):.4f}")
print(f"    Kf = {Kf_exact} = {Kf_exact.numerator}/{Kf_exact.denominator}")

# Effective resistance between two vertices
# For vertex-transitive graph: R(u,v) is constant for each orbit
# In distance-transitive graph with 2 classes:
# R(u,v) for adjacent vertices: R_adj
# R(u,v) for non-adjacent vertices: R_non
# Total: Kf = C(n,2) * R_avg

# For SRG: R(u,v) = (1/n) * Σ_{i≥1} (φ_i(u) - φ_i(v))^2 / μ_i
# where φ_i are orthonormal eigenvectors
# For distance-transitive: depends only on graph distance

# Using formula for k-regular SRG:
# R_adjacent = (2/n) * Σ 1/μ_i * (1 - cos(angle_i)) for appropriate angles
# Simpler: use Kirchhoff index / C(n,2) for average
R_avg = float(Kf_exact) / (n * (n - 1) / 2)
print(f"    Average resistance: R_avg = Kf / C(n,2) = {float(Kf_exact):.4f} / {n*(n-1)//2} = {R_avg:.6f}")

# More precise: use pseudoinverse of Laplacian
L = k * np.eye(n) - A.astype(float)
L_pinv = np.linalg.pinv(L)

# R(i,j) = L_pinv[i,i] + L_pinv[j,j] - 2*L_pinv[i,j]
# For vertex-transitive: L_pinv[i,i] is constant = trace(L_pinv)/n

trace_Lpinv = np.trace(L_pinv)
print(f"    tr(L⁺) = {trace_Lpinv:.6f}")
print(f"    Exact: Σ 1/μ_i = 24/10 + 15/16 = {float(Fraction(24, 10) + Fraction(15, 16)):.6f}")

# Compute actual resistance distances
# Separate into adjacent and non-adjacent
R_adj_vals = []
R_non_vals = []
for i in range(n):
    for j in range(i+1, n):
        R_ij = L_pinv[i,i] + L_pinv[j,j] - 2*L_pinv[i,j]
        if A[i,j] == 1:
            R_adj_vals.append(R_ij)
        else:
            R_non_vals.append(R_ij)

R_adj_mean = np.mean(R_adj_vals)
R_non_mean = np.mean(R_non_vals)
print(f"\n    Effective resistance (adjacent): R_1 = {R_adj_mean:.8f}")
print(f"    Effective resistance (non-adj):  R_2 = {R_non_mean:.8f}")
print(f"    # adjacent pairs: {len(R_adj_vals)}, # non-adjacent pairs: {len(R_non_vals)}")
print(f"    Std dev (adj): {np.std(R_adj_vals):.2e}")
print(f"    Std dev (non-adj): {np.std(R_non_vals):.2e}")

# Exact formulas for SRG resistance distance
# R(adj) and R(non-adj) for SRG(n,k,λ,μ)
# Using spectral decomposition:
# E_0 = (1/n) J, E_1 = projection onto r-eigenspace, E_2 = projection onto s-eigenspace
# L = (k - r) E_1 + (k - s) E_2
# L^+ = E_1/(k-r) + E_2/(k-s)
r_val, s_val = 2, -4
f_r, f_s = 24, 15

# For SRG, if vertices i,j are adjacent:
# R_adj = (1/(k-r))(1 - (λ-s)/(n(r-s))*n/f_r ...) -- complex formula
# Easier to rationalize from numerical values

# Try to express as fraction
R_adj_frac = Fraction(R_adj_mean).limit_denominator(1000)
R_non_frac = Fraction(R_non_mean).limit_denominator(1000)
print(f"    R_1 ≈ {R_adj_frac} = {float(R_adj_frac):.8f}")
print(f"    R_2 ≈ {R_non_frac} = {float(R_non_frac):.8f}")

# Kirchhoff index check
Kf_check = sum(R_adj_vals) + sum(R_non_vals)
print(f"\n    Kirchhoff index from resistances: {Kf_check:.4f}")
print(f"    From formula: {float(Kf_exact):.4f}")
print(f"    Match: {abs(Kf_check - float(Kf_exact)) < 0.01}")

# ========================================================
# 2. Random Walk Mixing Time
# ========================================================
print(f"\n[2] Random Walk Mixing Time")

# Transition matrix P = A / k (lazy or simple)
# Spectrum of P: {1, r/k, s/k} = {1, 2/12, -4/12} = {1, 1/6, -1/3}
lambda_2_P = Fraction(2, 12)  # = 1/6
lambda_min_P = Fraction(-4, 12)  # = -1/3
lambda_star = max(abs(float(lambda_2_P)), abs(float(lambda_min_P)))

print(f"    Transition matrix P = A/k (simple random walk)")
print(f"    Spectrum of P: {{1¹, (1/6)²⁴, (-1/3)¹⁵}}")
print(f"    λ*(P) = max(|1/6|, |-1/3|) = 1/3")
print(f"    Spectral gap: γ = 1 - λ* = 1 - 1/3 = 2/3")

spectral_gap = Fraction(2, 3)
print(f"    Spectral gap = {spectral_gap}")

# Mixing time bound: t_mix(ε) ≤ (1/γ) * log(n/ε)
import math
eps = 0.25
t_mix_upper = (1 / float(spectral_gap)) * math.log(n / eps)
print(f"\n    Mixing time upper bound: t_mix(1/4) ≤ (1/γ) * ln(n/ε)")
print(f"    = (3/2) * ln(40/0.25) = (3/2) * ln(160)")
print(f"    = (3/2) * {math.log(160):.4f} = {t_mix_upper:.4f}")
print(f"    ⌈t_mix(1/4)⌉ ≤ {math.ceil(t_mix_upper)}")

# For lazy random walk: P_lazy = (I + P)/2
# Spectrum: {1, (1 + 1/6)/2, (1 - 1/3)/2} = {1, 7/12, 1/3}
print(f"\n    Lazy random walk P_lazy = (I + P)/2:")
lambda2_lazy = Fraction(7, 12)
lambdan_lazy = Fraction(1, 3)
print(f"    Spectrum: {{1¹, (7/12)²⁴, (1/3)¹⁵}}")
lambda_star_lazy = max(abs(float(lambda2_lazy)), abs(float(lambdan_lazy)))
gap_lazy = 1 - lambda_star_lazy
print(f"    λ* = {lambda_star_lazy} = 7/12")
print(f"    Spectral gap = 1 - 7/12 = 5/12 ≈ {float(Fraction(5,12)):.4f}")

# Relaxation time
tau_rel = 1 / float(spectral_gap)
print(f"\n    Relaxation time (simple): τ_rel = 1/γ = {tau_rel:.4f}")
print(f"    Relaxation time = 3/2")
print(f"    Very fast mixing due to expander-like spectral gap!")

# ========================================================
# 3. Return Probability
# ========================================================
print(f"\n[3] Return Probability (Random Walk)")

# p^(t)(v,v) = (1/n) Σ_i λ_i(P)^t * n/n = (1/n)(1 + f_r*(r/k)^t + f_s*(s/k)^t)
for t in [1, 2, 3, 4, 5, 10, 20]:
    p_return = (1/n) * (1 + f_r * (2/k)**t + f_s * (-4/k)**t)
    print(f"    p^({t:2d})(v,v) = {p_return:.8f}")

print(f"    Stationary: π(v) = 1/n = {1/n:.6f}")

# ========================================================
# 4. Expected Hitting Time
# ========================================================
print(f"\n[4] Expected Hitting and Commute Times")

# For vertex-transitive k-regular graph:
# E[T_{u→v}] for adjacent: related to resistance
# Commute time: C(u,v) = 2|E| * R(u,v)
E_total = n * k // 2
C_adj = 2 * E_total * R_adj_mean
C_non = 2 * E_total * R_non_mean
print(f"    |E| = {E_total}")
print(f"    Commute time (adjacent): C_1 = 2|E|·R_1 = {C_adj:.4f}")
print(f"    Commute time (non-adj):  C_2 = 2|E|·R_2 = {C_non:.4f}")
print(f"    Expected hitting (adj):  H_1 = C_1/2 = {C_adj/2:.4f}")
print(f"    Expected hitting (non):  H_2 = C_2/2 = {C_non/2:.4f}")

C_adj_frac = Fraction(C_adj).limit_denominator(1000)
C_non_frac = Fraction(C_non).limit_denominator(1000)
print(f"    C_1 ≈ {C_adj_frac}")
print(f"    C_2 ≈ {C_non_frac}")

# Cover time upper bound
# For vertex-transitive graph: E[Cover] ≤ (4/27) n^2 * ln(n)^2 (Spencer bound)
# Simpler: Matthews bound: E[Cover] ≤ n * H_max * H_n
# where H_n = harmonic number
H_n = sum(1/i for i in range(1, n))  # n-1 terms
H_max = C_non / 2  # Maximum hitting time
cover_upper = H_max * H_n
print(f"\n    Cover time (Matthews upper): E[Cover] ≤ H_max · H_{n-1}")
print(f"    ≤ {H_max:.2f} · {H_n:.4f} = {cover_upper:.2f}")

# ========================================================
# 5. Cheeger Constant (Isoperimetric Number)
# ========================================================
print(f"\n[5] Cheeger Constant Bounds")

# Cheeger inequality: γ/2 ≤ h(G) ≤ √(2γ)
# where γ = spectral gap = 1 - max(|λ_2/k|, |λ_n/k|) = 2/3
gamma = float(spectral_gap)
h_lower = gamma / 2
h_upper = np.sqrt(2 * gamma)
print(f"    Spectral gap γ = {spectral_gap}")
print(f"    Discrete Cheeger inequality: γ/2 ≤ h ≤ √(2γk)")
# Actually for k-regular: h ≥ (k - λ_2)/2 and h ≤ √(2k(k - λ_2))
# where λ_2 = second eigenvalue of A
lambda_2 = 2  # second eigenvalue
cheeger_lower = (k - lambda_2) / 2
cheeger_upper_bound = np.sqrt(2 * k * (k - lambda_2))
print(f"    h(G) ≥ (k - λ_2)/2 = ({k} - {lambda_2})/2 = {cheeger_lower}")
print(f"    h(G) ≤ √(2k(k-λ_2)) = √(2·{k}·{k-lambda_2}) = √{2*k*(k-lambda_2)} = {cheeger_upper_bound:.4f}")

print("\n" + "=" * 70)
print(" SUMMARY")
print("=" * 70)
print(f"  • Kirchhoff index: Kf = {Kf_exact} (exact)")
print(f"  • Effective resistance (adj):  R_1 ≈ {R_adj_frac}")
print(f"  • Effective resistance (non):  R_2 ≈ {R_non_frac}")
print(f"  • Random walk spectral gap: γ = 2/3")
print(f"  • Mixing time: t_mix(1/4) ≤ {math.ceil(t_mix_upper)}")
print(f"  • Relaxation time: τ_rel = 3/2")
print(f"  • Determinant: det(A) = -3·2^56")
print(f"  • Cheeger constant: {cheeger_lower} ≤ h ≤ {cheeger_upper_bound:.4f}")
print()
