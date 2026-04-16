from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
from fractions import Fraction

# Ensure exploration/ is on sys.path so modules using bare imports work
ROOT = Path(__file__).resolve().parents[1]
EXPLORATION_DIR = ROOT / "exploration"
if str(EXPLORATION_DIR) not in sys.path:
    sys.path.insert(0, str(EXPLORATION_DIR))

from w33_k3_integral_h2_lattice_bridge import (
    primitive_hyperbolic_plane_coefficients,
    integral_k3_h2_intersection_matrix,
)
from w33_k3_three_u_decomposition_bridge import k3_three_u_block_coefficients
import importlib

# Inspect whether the integral_h2 bridge used the deterministic fallback
int_bridge = importlib.import_module("w33_k3_integral_h2_lattice_bridge")
print("_FALLBACK_USED:", getattr(int_bridge, "_FALLBACK_USED", None))
print("_PRECOMPUTED_INTERSECTION is not None:", getattr(int_bridge, "_PRECOMPUTED_INTERSECTION") is not None)


def rational_approx_matrix(mat, max_den=10**6):
    rows, cols = mat.shape
    R = [[None]*cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            R[i][j] = Fraction(mat[i,j]).limit_denominator(max_den)
    return R


def is_integer_matrix(mat, tol=1e-12):
    return np.allclose(mat, np.rint(mat), atol=tol)


def lcm(a, b):
    from math import gcd
    return abs(a*b) // gcd(a, b) if a and b else 0


def lcm_list(lst):
    from functools import reduce
    from math import gcd
    def lcm2(a,b):
        return abs(a*b)//gcd(a,b) if a and b else 0
    return reduce(lcm2, lst, 1)


def main():
    primitive = primitive_hyperbolic_plane_coefficients().astype(int)
    three_u = k3_three_u_block_coefficients().astype(int)
    u_blocks = [three_u[:, 2*i:2*i+2] for i in range(3)]

    print("primitive_plane_coeffs:")
    print(primitive.tolist())
    print("\nthree_u_factor_one_coeffs:")
    print(u_blocks[0].tolist())

    # direct equality checks
    for i, ub in enumerate(u_blocks):
        eq = np.array_equal(primitive, ub)
        eq_neg = np.array_equal(primitive, -ub)
        print(f"equal to u_block[{i}] exact? {eq}, equal up to overall sign? {eq_neg}")

    # Solve rational least squares for each u_block: find P such that ub @ P = primitive
    for i, ub in enumerate(u_blocks):
        try:
            # Solve for P (2x2) in rationals via least squares (should be exact if ub full rank)
            P, *_ = np.linalg.lstsq(ub.astype(float), primitive.astype(float), rcond=None)
            print(f"u_block[{i}] -> P (float approx):\n{P}")
            if is_integer_matrix(P):
                Pint = np.rint(P).astype(int)
                det = int(round(np.linalg.det(Pint)))
                print(f"P is integer with det={det}")
            else:
                # try rational approximation
                R = rational_approx_matrix(P)
                dens = [fr.denominator for row in R for fr in row]
                common_den = lcm_list([d for d in dens if d != 0])
                print(f"P rational approx common denominator: {common_den}")
                if common_den <= 10000:
                    # scale and test
                    Pscaled = np.array([[int(fr*common_den) for fr in row] for row in R], dtype=int)
                    # check if ub @ (Pscaled/common_den) == primitive
                    recon = ub.dot(Pscaled)  # equals primitive * common_den if exact
                    if np.array_equal(recon, primitive*common_den):
                        det = round(np.linalg.det(Pscaled))
                        print(f"primitive == ub @ (Pscaled/common_den) with common_den={common_den}; det(Pscaled)={det}")
                    else:
                        print("No exact integer P found at this denominator level.")
                else:
                    print("Rational approximation denominators too large to attempt exact check")
        except Exception as e:
            print(f"Error solving for block {i}: {e}")

    # Check if primitive is in rational span of entire three_u block
    rank_three_u = np.linalg.matrix_rank(three_u.astype(float))
    rank_aug = np.linalg.matrix_rank(np.column_stack((three_u.astype(float), primitive.astype(float))))
    print(f"rank(three_u)={rank_three_u}, rank(three_u | primitive)={rank_aug}")
    if rank_aug == rank_three_u:
        print("primitive is in the rational span of three_u")
        # compute least squares solution X (6x2)
        X, *_ = np.linalg.lstsq(three_u.astype(float), primitive.astype(float), rcond=None)
        print("least-squares X (float approx):")
        print(X)
        # rational approx
        R = rational_approx_matrix(X)
        dens = [fr.denominator for row in R for fr in row]
        common_den = lcm_list([d for d in dens if d != 0])
        print(f"common denominator for X approx: {common_den}")
        if common_den <= 10000:
            Xscaled = np.array([[int(fr*common_den) for fr in row] for row in R], dtype=int)
            recon = three_u.dot(Xscaled)
            if np.array_equal(recon, primitive*common_den):
                print("Found exact integer combination of 3U that yields primitive (scaled)")
            else:
                print("No exact integer combination found at this denominator level")
        else:
            print("Denominator too large to attempt integer reconstruction")
    else:
        print("primitive is NOT in the rational span of three_u")

if __name__ == '__main__':
    main()
