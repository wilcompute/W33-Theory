"""TOE64: exact signed-phase square decomposition, W33 flux robustness.

Retains the sign of the phi_2-phi_3 winding. Strictly improves TOE62 and
TOE63 worst-case independent positive-edge-hopping *sufficient* thresholds.
Physical continuum, interacting gauge and all-temperature claims stay open.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_20261013_toe62_global_flat_flux_proof import get_coefficients, folded

EDGES = ((0, 1, 1), (0, 2, 1), (1, 2, -1))


def matrices(a, c):
    """D=single-axis counts; M=sum c_ij*(e_i+sign*e_j) outer-product."""
    D = np.diag(a)
    M = np.zeros((3, 3))
    for z, (i, j, sign) in zip(c, EDGES):
        v = np.zeros(3)
        v[i], v[j] = 1, sign
        M += float(z) * np.outer(v, v)
    return D, M


def exact_square_decomposition(delta, a, c):
    """Exact identity, not a trigonometric inequality or Taylor series."""
    a, c = np.asarray(a, dtype=float), np.asarray(c, dtype=float)
    u = 1 - np.cos(delta)
    t = np.sin(delta) / math.sqrt(2)
    D, M = matrices(a, c)
    H = D - M
    # Each cross factor subtracts one incidence from both diagonal entries.
    hdiag = np.diag(H)
    square = float(t @ H @ t)
    quartic = float(0.5 * (hdiag @ (u * u)) +
                    c[0] * u[0] * u[1] +
                    c[1] * u[0] * u[2] +
                    c[2] * u[1] * u[2])
    energy = float(a @ u -
                   c[0] * (1 - np.cos(delta[0] + delta[1])) -
                   c[1] * (1 - np.cos(delta[0] + delta[2])) -
                   c[2] * (1 - np.cos(delta[1] - delta[2])))
    return energy, square, quartic


def certificate():
    native = get_coefficients()
    counts = np.array([native[folded((1, 0, 0))],
                       native[folded((0, 1, 0))],
                       native[folded((0, 0, 1))]], float)
    mixed = np.array([native[folded((1, 1, 0))],
                      native[folded((1, 0, 1))],
                      native[folded((0, 1, -1))]], float)
    assert counts.tolist() == [79, 77, 77]
    assert mixed.tolist() == [1, 1, 3]
    assert sum(native.values()) == 238
    D, M = matrices(counts, mixed)
    assert np.array_equal(M, [[2, 1, 1], [1, 4, -3], [1, -3, 4]])
    # Split into anti-(2,3): 77-7*r and symmetric 2x2 determinant
    # (79-2*r)*(77-r)-2*r*r = 6083-233*r.
    assert 6083 / 233 > 11
    ratio = 11
    threshold = (ratio ** (1 / 8) - 1) / (ratio ** (1 / 8) + 1)
    assert 0.148 < threshold < 0.149
    checks = []
    for eps in (0, 0.14, 0.145, 0.1487, threshold, 0.149):
        r = ((1 + eps) / (1 - eps)) ** 8
        eigen = np.linalg.eigvalsh(D - r * M)
        checks.append({"epsilon": eps, "ratio": r, "eig": eigen.tolist()})
        if eps < threshold - 1e-10:
            assert min(eigen) > 0
        if eps > threshold + 1e-10:
            assert min(eigen) < 0
        if abs(eps - threshold) < 1e-10:
            assert abs(min(eigen)) < 1e-10
        # The positive quartic remainder stays strict even at threshold:
        # hdiag_i >= L * (79-2*11, 77-4*11, 77-4*11).
        if eps <= threshold:
            L, U = (1-eps)**8, (1+eps)**8
            assert min(np.diag(L*D - U*M)) > 0
    rng = np.random.default_rng(641013)
    max_abs_identity_error = 0.0
    for eps in (0.1, 0.145, 0.1487):
        L, U = (1-eps)**8, (1+eps)**8
        baseH = L*D-U*M
        assert np.linalg.eigvalsh(baseH)[0] > 0
        for _ in range(250):
            a = counts*rng.uniform(L,U,3)
            c = mixed*rng.uniform(L,U,3)
            delta = rng.uniform(-math.pi, math.pi,3)
            energy, square, quartic = exact_square_decomposition(delta,a,c)
            max_abs_identity_error = max(max_abs_identity_error,
                                         abs(energy-square-quartic))
            assert abs(energy-square-quartic) < 1e-10
            assert square > -1e-9 and quartic >= -1e-9
            assert energy >= -1e-9
    # Sharp ONLY for the *independent Fourier coefficient interval relaxation*:
    # simultaneous extreme coefficient choices need not arise from W33 link weights.
    eps = 0.155
    L, U = (1-eps)**8, (1+eps)**8
    constructed_negative, _, _ = exact_square_decomposition(
        np.array([0, 0.01, -0.01]), counts*L, mixed*U
    )
    assert constructed_negative < 0
    return {
        "status": "PASS_TOE64_SIGNED_SQUARE_FLUX_ROBUSTNESS",
        "native_winding_cycle_count": 238,
        "signed_cross_outer_product_matrix": M.astype(int).tolist(),
        "critical_ratio": ratio,
        "critical_epsilon": threshold,
        "compared_to_toe62_epsilon": ((77/8)**(1/8)-1)/((77/8)**(1/8)+1),
        "compared_to_toe63_epsilon": (((707-math.sqrt(207865))/24)**(1/8)-1) /
                                    (((707-math.sqrt(207865))/24)**(1/8)+1),
        "anti_23_eigenvalue_formula": "77-7*r",
        "symmetric_2x2_determinant_formula": "6083-233*r",
        "eigenvalue_checks": checks,
        "stress_independent_coefficient_trials": 750,
        "max_abs_exact_square_identity_error": max_abs_identity_error,
        "box_only_counterexample_epsilon": eps,
        "box_only_negative_energy_example": constructed_negative,
        "theorem": "The leading beta^7 free-fermion flat W33 U(1)^3 holonomy potential has unique global three-pi minimum for all independent positive link hopping magnitudes in [1-e,1+e] when e <= (11^(1/8)-1)/(11^(1/8)+1). Exact signed square identity supplies a nonnegative quadratic plus strictly positive quartic remainder.",
        "scope": "Sharp for independent Fourier-coefficient box relaxation, not proved optimal for realizable edge-product coefficients. This is NOT an all-temperature flux theorem, dynamical gauge vacuum, physical CP or TOE.",
    }


if __name__ == "__main__":
    result = certificate()
    out = ROOT / "data/w33_20261013_toe64_signed_square_flux_robustness.json"
    out.write_text(json.dumps(result,indent=2)+"\n", encoding="utf-8")
    print(result["status"],result["critical_epsilon"])
