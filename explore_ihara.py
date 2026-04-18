#!/usr/bin/env python3
"""
Compute the Ihara zeta function for W(3,3) and evaluate at special points.
The Ihara zeta function encodes all closed walks in the graph.
"""

import numpy as np
from scipy.special import comb

n, k, r, s, fr, fs = 40, 12, 2, -4, 24, 15

print('=== IHARA ZETA FUNCTION FOR W(3,3) ===')
print()
print('The Ihara zeta function is:')
print('  Z(u) = (det(I - uA + u²(D-I)))⁻¹ / ((1-u²)^m)')
print('where A is adjacency matrix, D is degree matrix, m is circuit rank')
print()

# For W(3,3): n=40, regular with degree k=12
# Circuit rank m = n - 1 = 39 (for a connected graph with no parallel edges)
m = n - 1

print(f'Graph parameters: n={n}, k={k}, m={m}')
print()

# The Ihara formula: Z(u) = 1 / ((1-u²)^m * det(I - A*u + D*u²))
# For a k-regular graph: det(I - A*u + D*u²) = det(I - u*A + u²*k*I)
#                                            = det((1 + u²*k)*I - u*A)

# The eigenvalues of A are k=12, 2 (mult 24), -4 (mult 15)
# Eigenvalues of (1 + u²*k)*I - u*A are (1+u²*k) - u*λ for each eigenvalue λ

print('Evaluating Ihara zeta function:')
print()

def ihara_denominator_eigenvalues(u, eigs=[12, 2, -4], mults=[1, 24, 15]):
    """
    For the Ihara formula, the denominator is:
      (1-u²)^m * det(I - uA + u²(D-I))
    For a regular graph: det(I - uA + u²(k-1)I) = prod (1 - u*λ + u²(k-1))
    """
    # det(I - uA + u²(k-1)I) where k-1 = 11
    prod = 1.0
    for eig, mult in zip(eigs, mults):
        factor = 1 - u*eig + u**2 * (k-1)
        prod *= factor ** mult
    
    # Multiply by (1-u²)^m
    prod *= (1 - u**2) ** m
    
    return prod

print('Key evaluations:')
test_points = [0, 1/k, 1/np.sqrt(k), 1/(k-1), 0.1]
for u_val in test_points:
    try:
        denom = ihara_denominator_eigenvalues(u_val)
        zeta = 1 / denom if denom != 0 else float('inf')
        print(f'  Z(u={u_val:.4f}) = 1/{denom:.6e} = {zeta:.6e}')
    except Exception as e:
        print(f'  Z(u={u_val:.4f}) = undefined ({e})')

print()
print('Critical points (where denominator = 0):')

# det(I - uA + u²(k-1)I) = 0 means one of the factors (1 - u*λ + u²(k-1)) = 0
# Solving u²(k-1) - u*λ + 1 = 0:
# u = (λ ± sqrt(λ² - 4(k-1))) / (2(k-1))

eigs = [12, 2, -4]
mults = [1, 24, 15]

critical_u = []
for eig, mult in zip(eigs, mults):
    discriminant = eig**2 - 4*(k-1)
    print(f'  λ={eig:2}: λ²-4(k-1) = {eig**2} - 44 = {discriminant}', end='')
    
    if discriminant >= 0:
        sqrt_disc = np.sqrt(discriminant)
        u1 = (eig + sqrt_disc) / (2*(k-1))
        u2 = (eig - sqrt_disc) / (2*(k-1))
        print(f'  → u = {u1:.4f} or {u2:.4f}')
        if 0 < u1 < 1: critical_u.append(('1st', u1, eig))
        if 0 < u2 < 1: critical_u.append(('2nd', u2, eig))
    else:
        sqrt_disc = np.sqrt(-discriminant)
        u_real = eig / (2*(k-1))
        u_imag = sqrt_disc / (2*(k-1))
        print(f'  → u = {u_real:.4f} ± {u_imag:.4f}i (complex)')

print()
print('Radius of convergence (smallest |u| with Z(u) undefined):')
if critical_u:
    min_u = min(abs(cu[1]) for cu in critical_u)
    print(f'  |u| = {min_u:.6f} = 1/{1/min_u:.4f}')
else:
    print(f'  (no real critical points in (0,1))')

print()
print('Pole at u = 1:')
print(f'  This is a universal pole of Z(u) from the factor (1-u²)^m')
print(f'  Residue ∝ m = {m}')

print()
print('Connection to spectral theory:')
print(f'  Ihara formula: Z(u) ∝ 1 / ∏_λ (1 - uλ + u²(k-1))')
print(f'  Logarithmic derivative: Z\'/Z = d/du log Z')
print(f'  At u=0: Z\'(0)/Z(0) relates to triangle counting and clique structure')

# Count triangles: tr(A^3) / 6
num_triangles = int(960 / 6)
print()
print(f'Closed walks of length 3: tr(A³) = 960')
print(f'Number of triangles: tr(A³)/6 = {num_triangles}')
print(f'Expected: (n*k)/4 for random regular? {n*k//4} = {40*12//4}')
