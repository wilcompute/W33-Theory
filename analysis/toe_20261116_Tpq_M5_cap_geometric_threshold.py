"""Compute the geometric spectator threshold for the capped M5 probe."""

import json
from math import pi
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import Legendre, leggauss
from scipy.linalg import eigh
from scipy.special import hyp2f1
import sympy as sp


def exact_limits():
    # Limiting cone coordinate s scales as meridian arclength divided by the round radius.
    s = sp.Symbol("s", positive=True)
    ground = 1/sp.sin(s)
    operator = -sp.diff(ground, s, 2)-4*sp.cot(s)*sp.diff(ground, s)-2*ground/sp.sin(s)**2
    assert sp.trigsimp(operator/ground) == -3
    test = sp.Function("u")(s)
    weight_root = sp.sin(s)**2
    transformed = -sp.diff(weight_root**2*sp.diff(test/weight_root, s), s)/weight_root
    transformed -= 2*test/sp.sin(s)**2
    assert sp.trigsimp(transformed+sp.diff(test, s, 2)+4*test) == 0
    # Round Euclidean S^5 cap radius is (5/4) times the reference S^4 radius.
    assert -5/sp.Rational(5, 4)**2 == -sp.Rational(16, 5)


def volume_ratio(r):
    """V(r)/sinh(r)^4, retaining accuracy at the tip."""
    sinh = np.sinh(r)
    small = r < 0.35
    result = np.empty_like(r)
    result[small] = sinh[small]*hyp2f1(0.5, 2.5, 3.5, -sinh[small]**2)/5
    rr = r[~small]
    result[~small] = (np.sinh(4*rr)/32-np.sinh(2*rr)/4+3*rr/8)/sinh[~small]**4
    return result


def eigenvalue(alpha, bulge, modes, sample_count):
    grid, weights = leggauss(sample_count)
    angle = (1+grid)*pi/4
    r = bulge*np.sin(angle)
    dr_dangle = bulge*np.cos(angle)
    pressure = 4/alpha
    radius = np.sinh(r)
    torus_speed = pressure*volume_ratio(r)
    speed_deficit = 1-torus_speed
    distance_to_bulge = bulge-r
    near_turn = distance_to_bulge < 1e-5
    turn_derivative = pressure-4/np.tanh(bulge)
    turn_second_derivative = 4/np.sinh(bulge)**2-4*turn_derivative/np.tanh(bulge)
    delta = distance_to_bulge[near_turn]
    speed_deficit[near_turn] = delta*(turn_derivative-delta*turn_second_derivative/2)
    radial_speed = np.sqrt(speed_deficit*(1+torus_speed))
    curvature = torus_speed/np.tanh(r)
    potential = (pressure-4*curvature)**2+4*curvature**2/np.cosh(r)**2
    measure = weights*(pi/4)*radius**4*dr_dangle/radial_speed
    kinetic_weight = weights*(pi/4)*radius**4*radial_speed/dr_dangle
    coordinate = 2*np.sin(angle)**2-1
    derivative = 4*np.sin(angle)*np.cos(angle)
    basis = [Legendre.basis(i) for i in range(modes)]
    values = np.array([p(coordinate) for p in basis])
    gradients = np.array([p.deriv()(coordinate)*derivative for p in basis])
    overlap = (values*measure) @ values.T
    jacobi = (gradients*kinetic_weight) @ gradients.T-(values*(measure*potential)) @ values.T
    level, vectors = eigh(jacobi, overlap, subset_by_index=[0, 0])
    solution = Legendre(vectors[:, 0])
    profile = solution(coordinate)
    first = solution.deriv()(coordinate)*4*r/bulge**2
    second = (solution.deriv(2)(coordinate)*(4*r/bulge**2)**2
              +solution.deriv()(coordinate)*4/bulge**2)
    torus_acceleration = pressure-4*curvature
    laplacian = (radial_speed**2*second
                 +(4*radial_speed**2/np.tanh(r)-torus_speed*torus_acceleration)*first)
    residual = -laplacian-(potential+level[0])*profile
    residual_norm = np.sqrt(np.dot(measure, residual**2)/np.dot(measure, profile**2))
    return float(level[0]), float(residual_norm)


def track(row):
    alpha = row["alpha"]
    bulge = row["cap_bulge_radius"]
    radius = np.sinh(row["round_radius_in_local_ads_units"])
    coarse, _ = eigenvalue(alpha, bulge, 16, 280)
    fine, residual = eigenvalue(alpha, bulge, 24, 420)
    change = abs(fine-coarse)*radius**2
    assert fine < 0 and change < 4e-6, (alpha, coarse, fine, change)
    assert residual*radius**2 < 3e-6, (alpha, residual*radius**2)
    assert fine > -(4/alpha)**2/4
    return {"alpha": alpha, "negative_eigenvalue_in_local_ads_units": fine,
            "eigenvalue_times_round_sphere_radius_squared": fine*radius**2,
            "spectator_index_one_circumference_threshold": 2*pi/np.sqrt(-fine),
            "spectator_threshold_over_round_radial_period": 2/(radius*np.sqrt(-fine)),
            "scaled_eigenvalue_change_under_resolution_check": change,
            "scaled_weighted_differential_residual": residual*radius**2}


def main():
    exact_limits()
    data_dir = Path(__file__).resolve().parents[1]/"data"
    reference = json.loads((data_dir/"toe_20261116_Tpq_M5_finite_stripe.json").read_text(encoding="utf-8"))
    data = {
        "small_alpha_scaled_eigenvalue_limit": "-16/5",
        "formal_near_planar_limit_operator_ground_eigenvalue": -3,
        "control_families": [track(row) for row in reference["families"]],
        "actual_warped_backgrounds": [{"chern_pair": row["chern_pair"], **track(row)}
                                      for row in reference["actual_warped_backgrounds"]],
    }
    output = data_dir/"toe_20261116_Tpq_M5_cap_geometric_threshold.json"
    output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Verified the resolved geometric eigenvalue and the cap spectator thresholds.")


if __name__ == "__main__":
    main()
