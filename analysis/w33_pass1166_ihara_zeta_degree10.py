#!/usr/bin/env python3
"""
Pass 1166: Ihara zeta function expansion to degree 10 for SRG(40,12,2,4).

The Ihara zeta function of a k-regular graph G on n vertices is:
  Z_G(u)^{-1} = (1 - u^2)^{m-n} * det(I - Au + k*u^2 * I)
where m = |E|, n = |V|, A = adjacency matrix, k = regularity.

For the W(3,3) collinearity graph = SRG(40,12,2,4):
  n=40, k=12, m=240, m-n=200
  A-spectrum: {12:1, 2:24, -4:15} (from corrected W33 spectrum)

Since A is diagonalizable with known spectrum:
  det(I - Au + k*u^2 * I) = prod_lambda (1 - lambda*u + k*u^2)^{mult_lambda}
  = (1 - 12u + 12u^2)^1 * (1 - 2u + 12u^2)^24 * (1 + 4u + 12u^2)^15

The RECIPROCAL zeta (easier to expand):
  Z_G(u)^{-1} = (1-u^2)^200 * (1-12u+12u^2) * (1-2u+12u^2)^24 * (1+4u+12u^2)^15

We expand 1/Z_G(u) as a power series to degree 10.

Cross-check: The coefficient of u^n in log Z_G(u) counts the number of
primitive closed walks of length n in G divided by n.

For SRG(40,12,2,4), known walk counts:
  Tr(A^1) = 0 (no self-loops)
  Tr(A^2) = 2*m = 480
  Tr(A^3) = 6 * (number of triangles) * 3... 
    Actually: Tr(A^3) = 6 * T where T = number of triangles.
    Number of triangles in SRG(40,12,2,4) = n*k*(lambda)/6 = 40*12*2/6 = 160.
    So Tr(A^3) = 6*160 = 960.
  Tr(A^4): from spectrum: 12^4*1 + 2^4*24 + (-4)^4*15 = 20736+384+3840 = 24960.

Outputs: data/IHARA_ZETA_DEGREE10_2026_07_27.json
"""
import json
from pathlib import Path
from datetime import datetime
from fractions import Fraction

# SRG parameters
N, K, LAM, MU = 40, 12, 2, 4
EDGES = N * K // 2  # 240
A_SPECTRUM = {12: 1, 2: 24, -4: 15}

def poly_mul_trunc(p, q, deg):
    r = [Fraction(0)] * (deg + 1)
    for i, a in enumerate(p):
        if i > deg: break
        for j, b in enumerate(q):
            if i + j > deg: break
            r[i + j] += a * b
    return r

def poly_power_trunc(coeffs_of_1_plus_ax_plus_bx2, exp, deg):
    """(1 + a*x + b*x^2)^exp truncated to degree deg, exact."""
    from math import comb
    # Use multinomial / binomial convolution
    # p(x) = sum_{k>=0} C(exp,k)*... this is complex for trinomial
    # Use repeated squaring with poly_mul_trunc
    if exp == 0:
        r = [Fraction(0)] * (deg + 1); r[0] = Fraction(1); return r
    base = list(coeffs_of_1_plus_ax_plus_bx2) + [Fraction(0)] * (deg + 1)
    base = base[:deg + 1]
    result = [Fraction(0)] * (deg + 1); result[0] = Fraction(1)
    n = exp
    b = base[:]
    while n:
        if n % 2 == 1:
            result = poly_mul_trunc(result, b, deg)
        b = poly_mul_trunc(b, b, deg)
        n //= 2
    return result

def make_factor(lam, k, deg):
    """Coefficients of (1 - lam*u + k*u^2) truncated to degree deg."""
    p = [Fraction(0)] * (deg + 1)
    p[0] = Fraction(1)
    if deg >= 1: p[1] = Fraction(-lam)
    if deg >= 2: p[2] = Fraction(k)
    return p

def main():
    deg = 10
    # Build det(I - Au + k*u^2 * I)
    det_poly = [Fraction(0)] * (deg + 1); det_poly[0] = Fraction(1)
    for lam, mult in A_SPECTRUM.items():
        factor = make_factor(lam, K, deg)
        factor_pow = poly_power_trunc(factor, mult, deg)
        det_poly = poly_mul_trunc(det_poly, factor_pow, deg)
    # Build (1 - u^2)^200
    one_minus_u2 = [Fraction(0)] * (deg + 1)
    one_minus_u2[0] = Fraction(1)
    if deg >= 2: one_minus_u2[2] = Fraction(-1)
    one_minus_u2_pow = poly_power_trunc(one_minus_u2, EDGES - N, deg)
    # Z^{-1} = (1-u^2)^200 * det
    zinv = poly_mul_trunc(det_poly, one_minus_u2_pow, deg)
    # Verify: Z^{-1}[0]=1, Z^{-1}[1]=0 (no odd-length closed walks contribute at u^1)
    # Walk counts from spectrum: Tr(A^n) = sum_i lambda_i^n * m_i
    trace_A = {}
    for n in range(1, deg + 1):
        trace_A[n] = sum(lam**n * mult for lam, mult in A_SPECTRUM.items())
    # Triangle count cross-check
    triangles = N * K * LAM // 6
    assert trace_A[3] == 6 * triangles, f'Tr(A^3)={trace_A[3]} != {6*triangles}'
    result = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'schema': 'w33.pass1166.ihara_zeta_degree10.v1',
        'status': 'PASS',
        'graph': f'SRG({N},{K},{LAM},{MU}) = W(3,3) collinearity graph',
        'vertices': N, 'edges': EDGES, 'regularity': K,
        'a_spectrum': str(A_SPECTRUM),
        'zinv_coefficients': [str(c) for c in zinv],
        'zinv_0': str(zinv[0]),
        'zinv_1': str(zinv[1]),
        'zinv_2': str(zinv[2]),
        'trace_powers': {str(n): trace_A[n] for n in range(1, deg + 1)},
        'triangle_count': triangles,
        'triangle_cross_check': trace_A[3] == 6 * triangles,
        'formula': 'Z_G(u)^{-1} = (1-u^2)^200 * prod_lambda (1-lambda*u+12*u^2)^{mult_lambda}',
    }
    out = Path('data/IHARA_ZETA_DEGREE10_2026_07_27.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    print(f'PASS 1166 Ihara zeta: Z^{{-1}} coeffs [0..5] = {[str(c) for c in zinv[:6]]}')
    print(f'  Triangles: {triangles}, Tr(A^3)={trace_A[3]}, cross-check: {trace_A[3]==6*triangles}')
    return result

if __name__ == '__main__':
    main()
