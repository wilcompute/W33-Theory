"""Continue nonlinear capped M5 spectator graphs across their first-order crossing."""

import json
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import eigh
from scipy.optimize import brentq, minimize_scalar, root

from toe_20261116_Tpq_M5_cap_sixth_order import geometric_data, sixth_order
from toe_20261116_Tpq_M5_cap_spectator_branch import reduced_quartic


class Continuation:
    def __init__(self, alpha, meridian_count, harmonic_count):
        fields = reduced_quartic(geometric_data(alpha), meridian_count, 220,
                                 include_response=True)
        levels, modes = eigh(fields["radial_hessian"], fields["overlap"])
        if modes[:, 0] @ fields["ground"] < 0:
            modes[:, 0] *= -1
        self.levels = levels
        self.critical = -levels[0]
        self.value = modes.T @ fields["values"]
        self.gradient = modes.T @ fields["gradients"]
        self.weight = fields["weights"]
        self.pressure = fields["pressure"]
        self.speed = fields["speed"][:, None]
        self.angular = fields["angular_curvature"][:, None]
        self.meridian = fields["meridian_curvature"][:, None]
        self.harmonics = np.arange(harmonic_count)
        theta = 2*np.pi*(np.arange(40)+.5)/40
        self.cosine = np.cos(self.harmonics[:, None]*theta)
        self.sine = np.sin(self.harmonics[:, None]*theta)
        self.fourier_derivative = -self.harmonics[:, None]*self.sine
        self.shape = (harmonic_count, meridian_count)
        self.mask = np.ones(self.shape, dtype=bool)
        self.mask[1, 0] = False
        self.solver_scale = abs(levels+self.harmonics[:, None]**2*self.critical)
        self.solver_scale[~self.mask] = 1
        guess = np.zeros(self.shape)
        for n, response in zip((0, 2), fields["second_order"]):
            guess[n] = modes.T @ fields["overlap"] @ response
        self.guess = guess
        self.integral_nodes, self.integral_weights = leggauss(8)

    def tube(self, f):
        x = self.speed*f
        angular_shift = 2*np.sinh(x/2)**2 + (self.angular/self.speed)*np.sinh(x)
        angular = 1+angular_shift
        meridian = 1+self.meridian*f
        # Avoid subtracting one from the full tube determinant.
        angular_area_shift = angular_shift*(4+angular_shift*(6+angular_shift*(4+angular_shift)))
        area_shift = angular_area_shift+self.meridian*f*(1+angular_area_shift)
        derivative = (self.meridian*angular**4+4*meridian*angular**3*
                      (self.speed*np.sinh(x)+self.angular*np.cosh(x)))
        return area_shift, derivative, meridian

    def graph(self, coefficients):
        f = (coefficients @ self.value).T @ self.cosine
        ds = (coefficients @ self.gradient).T @ self.cosine
        dt = (coefficients @ self.value).T @ self.fourier_derivative
        return f, ds, dt

    def stationarity(self, coefficients, k, *, calculate_action=False):
        f, ds, dt = self.graph(coefficients)
        d_area, j_prime, meridian = self.tube(f)
        j = 1+d_area
        gradient_sq = (ds/meridian)**2+k*dt**2
        metric_root = np.sqrt(1+gradient_sq)
        metric_shift = gradient_sq/(metric_root+1)
        if calculate_action:
            primitive_shift = np.zeros_like(f)
            for node, weight in zip(self.integral_nodes, self.integral_weights):
                primitive_shift += weight*self.tube(f*(node+1)/2)[0]
            energy = (d_area-self.pressure*f
                      -self.pressure*f*primitive_shift/2+j*metric_shift)
            return float(np.mean(energy, axis=1) @ self.weight)
        field = j_prime-self.pressure*j+j_prime*metric_shift
        field -= j*self.meridian*ds**2/(meridian**3*metric_root)
        ds_force = j*ds/(meridian**2*metric_root)
        dt_force = j*k*dt/metric_root
        return (
            ((self.value*self.weight) @ field @ self.cosine.T).T
            +((self.gradient*self.weight) @ ds_force @ self.cosine.T).T
            +((self.value*self.weight) @ dt_force @ self.fourier_derivative.T).T
        )/self.cosine.shape[1]

    def solve(self, amplitude):
        def unpack(vector):
            coefficients = np.zeros(self.shape)
            coefficients[1, 0] = amplitude
            coefficients[self.mask] = amplitude**2*vector[:-1]
            return coefficients, self.critical+amplitude**2*vector[-1]

        def equations(vector):
            coefficients, k = unpack(vector)
            residual = self.stationarity(coefficients, k)/self.solver_scale
            return np.r_[residual[self.mask]/amplitude**2, residual[1, 0]/amplitude**3]

        fitted = root(equations, np.r_[self.guess[self.mask], 0], tol=5e-9)
        coefficients, k = unpack(fitted.x)
        residual = float(np.max(abs(self.stationarity(coefficients, k))))
        assert residual < 1e-10, (amplitude, residual, fitted.message)
        return {"amplitude": float(amplitude), "detuning": float(k-self.critical),
                "action_excess": self.stationarity(coefficients, k, calculate_action=True),
                "max_projected_force": residual}


def transitions(alpha, meridian_count, harmonic_count, coefficients):
    b, d = coefficients["quartic"], coefficients["reduced_sixth"]
    assert b < 0 < d
    model_fold = np.sqrt(-b/(3*d))
    model_crossing = np.sqrt(-b/(2*d))
    simulation = Continuation(alpha, meridian_count, harmonic_count)
    fold = minimize_scalar(lambda x: -simulation.solve(x)["detuning"],
                           bounds=(.85*model_fold, 1.15*model_fold),
                           method="bounded", options={"xatol": 3e-7})
    assert fold.success and abs(fold.x/model_fold-1) < 0.1
    crossing = brentq(lambda x: simulation.solve(x)["action_excess"],
                      .90*model_crossing, 1.10*model_crossing, xtol=1e-7)
    fold_row = simulation.solve(fold.x)
    crossing_row = simulation.solve(crossing)
    assert 0 < crossing_row["detuning"] < fold_row["detuning"]
    assert abs(crossing_row["action_excess"]) < 5e-14
    assert simulation.solve(.95*crossing)["action_excess"] > 0
    assert simulation.solve(1.05*crossing)["action_excess"] < 0
    result = {"alpha": alpha, "fold": fold_row, "equal_action": crossing_row,
            "model_fold_detuning": 4*b*b/(3*d), "model_crossing_detuning": b*b/d,
            "model_fold_amplitude": float(model_fold),
            "model_crossing_amplitude": float(model_crossing)}
    if harmonic_count >= 7:
        common_detuning = .9*crossing_row["detuning"]

        def at_detuning(amplitude):
            return simulation.solve(amplitude)["detuning"]-common_detuning

        small = simulation.solve(brentq(at_detuning, .4*fold.x, fold.x, xtol=1e-7))
        large = simulation.solve(brentq(at_detuning, crossing, 1.15*crossing, xtol=1e-7))
        assert small["action_excess"] > 0 > large["action_excess"]
        assert abs(small["detuning"]-large["detuning"]) < 5e-13
        result["coexisting_at_shared_detuning"] = {"small": small, "large": large}
    return result


def main():
    data_dir = Path(__file__).resolve().parents[1]/"data"
    previous = json.loads((data_dir/"toe_20261116_Tpq_M5_cap_sixth_order.json").read_text(encoding="utf-8"))
    crossing = previous["crossing"]["alpha"]
    rows = []
    for distance in (.0001, .0003):
        alpha = crossing-distance
        coefficients = sixth_order(alpha, 24, 330)
        coarse = transitions(alpha, 12, 5, coefficients)
        fine = transitions(alpha, 17, 7, coefficients)
        for label in ("fold", "equal_action"):
            assert abs(coarse[label]["amplitude"]/fine[label]["amplitude"]-1) < .006, (
                distance, label, coarse[label], fine[label]
            )
            assert abs(coarse[label]["detuning"]/fine[label]["detuning"]-1) < .006, (
                distance, label, coarse[label], fine[label]
            )
        rows.append({"alpha_distance_below_quartic_zero": distance,
                     "coarse": coarse, "fine": fine})
        print(f"Resolved fold and equal-action point at alpha={alpha:.10f}.", flush=True)
    output = data_dir/"toe_20261116_Tpq_M5_cap_nonlinear_fold.json"
    output.write_text(json.dumps({"continuations": rows}, indent=2)+"\n", encoding="utf-8")
    print("Verified the capped M5 fold and equal-action point with the nonlinear graph equation.")


if __name__ == "__main__":
    main()
