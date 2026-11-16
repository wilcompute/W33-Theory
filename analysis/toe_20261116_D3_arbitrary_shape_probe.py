"""Verify the determinant bound and spherical controls for the D3 probe theorem."""

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import sympy as sp


def born_infeld_identities():
    flux = sp.zeros(4)
    for entry, (i, j) in zip(sp.symbols("f:6", real=True), combinations(range(4), 2)):
        flux[i, j], flux[j, i] = entry, -entry
    metric = sp.eye(4)
    determinant = (metric + flux).det().expand()
    assert determinant == (metric - flux).det().expand()
    assert sp.expand((metric - flux**2).det() - determinant**2) == 0
    # Multiply the asserted identity for the symmetric inverse by its common denominator.
    assert ((metric + flux)*(metric - flux) - (metric - flux**2)).expand() == sp.zeros(4)
    assert (metric + flux) + (metric - flux) == 2*metric


def spherical_identities():
    radius, length, tension, critical = sp.symbols("r L T Qeff", positive=True)
    area = (length*sp.sinh(radius/length))**4
    action_derivative = tension*sp.diff(area, radius)-4*critical*area/length
    assert sp.simplify((action_derivative/(4*area/length)) -
                       (tension*sp.coth(radius/length)-critical)) == 0
    on_shell_second_derivative = sp.diff(action_derivative, radius).subs(
        critical, tension*sp.coth(radius/length))
    assert sp.simplify(on_shell_second_derivative + 4*tension*area**sp.Rational(1, 2)) == 0
    principal_curvature = sp.coth(radius/length)/length
    assert sp.simplify(4*(principal_curvature**2-1/length**2)-4/sp.sqrt(area)) == 0
    inverse_radius = sp.Symbol("z", positive=True)
    tension_ratio = 1/sp.sqrt(1+inverse_radius**2)
    assert sp.limit((1-tension_ratio)/inverse_radius**2, inverse_radius, 0) == sp.Rational(1, 2)
    harmonics = [{"ell": ell, "multiplicity": (ell+1)*(ell+2)*(2*ell+3)//6,
                  "normal_eigenvalue_times_radius_squared_over_tension": ell*(ell+3)-4}
                 for ell in range(7)]
    return harmonics


def warp_identity():
    warp = sp.Function("A")
    coordinate, length, flux = sp.symbols("y L f", real=True)
    value = warp(coordinate)
    flux_curvature = -sp.factorial(4)*flux**2*sp.exp(-10*value)/96
    assert flux_curvature == -flux**2*sp.exp(-10*value)/4
    warp_laplacian = sp.diff(sp.exp(5*value), coordinate, 2)
    expected = 5*sp.exp(5*value)*(sp.diff(value, coordinate, 2)
                                   + 5*sp.diff(value, coordinate)**2)
    assert sp.simplify(warp_laplacian-expected) == 0
    source = 5*sp.exp(5*value)*(-4*sp.exp(-2*value)/length**2-flux_curvature)
    weighted_source = (20/length**2)*sp.exp(-5*value)*(
        (flux*length/4)**2-sp.exp(8*value)
    )
    assert sp.simplify(source - weighted_source) == 0


def conifold_warp_gap():
    normalized_warp = sp.Symbol("u", positive=True)
    source = 20*(normalized_warp**-1-normalized_warp**sp.Rational(3, 5))
    assert source.subs(normalized_warp, 1) == 0
    assert sp.diff(source, normalized_warp).subs(normalized_warp, 1) == -32

    # Twice the spins are integers. For a fixed absolute fiber charge,
    # the two spins start at half that charge and advance in unit steps.
    eigenvalues_times_four = set()
    for charge in range(5):
        for twice_j in range(charge, 5, 2):
            for twice_k in range(charge, 5, 2):
                eigenvalues_times_four.add(3*(2*twice_j*(twice_j+2) +
                                              2*twice_k*(twice_k+2) - charge**2))
    # A spin above two contributes at least 6*(5/2)*(7/2) to the eigenvalue.
    assert 6*sp.Rational(5, 2)*sp.Rational(7, 2) > 36
    assert min(abs(value-128) for value in eigenvalues_times_four) == 16
    assert 144 in eigenvalues_times_four  # The charge-zero (2,0) mode remains on every quotient.
    return {"warp_linearization_eigenvalue": 32, "scalar_spectrum_distance": 4}


def tilted_flux_checks():
    rng = np.random.default_rng(813)
    rows = []
    for rank in range(5):
        minimum_trace_margin = float("inf")
        for _ in range(256):
            frame, _ = np.linalg.qr(rng.normal(size=(4, 4)))
            singular_values = rng.uniform(0.01, 1, size=rank)
            external = (frame[:, :rank]*singular_values) @ frame[:, :rank].T
            seed = rng.normal(size=(4, 4))
            flux = (seed-seed.T)*10**rng.uniform(-1, 1)
            weight = np.sqrt(np.linalg.det(np.eye(4)+flux))
            weighted_trace = weight*np.trace(np.linalg.solve(np.eye(4)-flux@flux, external))
            projection = np.prod(np.sqrt(singular_values)) if rank == 4 else 0
            margin = weighted_trace-4*projection
            assert margin >= -1e-11
            if rank:
                assert weighted_trace > 0
            minimum_trace_margin = min(minimum_trace_margin, float(margin))
        rows.append({"external_rank": rank, "samples": 256,
                     "smallest_weighted_trace_minus_four_times_projection": minimum_trace_margin})
    # Nonzero self-dual flux saturates the full-rank trace bound for an external tangent plane.
    flux = np.array([[0., 3., 0., 0.], [-3., 0., 0., 0.],
                     [0., 0., 0., 3.], [0., 0., -3., 0.]])
    unit = np.eye(4)
    weight = np.sqrt(np.linalg.det(unit+flux))
    assert np.isclose(weight*np.trace(np.linalg.solve(unit-flux@flux, unit)), 4)
    return rows


def main():
    born_infeld_identities()
    warp_identity()
    data = {
        "external_flux_threshold": "4 T exp(4 A_min) / (L q)",
        "pure_five_form_integral": "(f L/4)^2 = integral exp(3 A) / integral exp(-5 A)",
        "equal_flux_conifold_and_fiber_quotients": conifold_warp_gap(),
        "spherical_normal_harmonics": spherical_identities(),
        "tilted_worldvolume_with_real_flux": tilted_flux_checks(),
    }
    destination = Path(__file__).resolve().parents[1] / "data" / "toe_20261116_D3_arbitrary_shape_probe.json"
    destination.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Verified the Born-Infeld and warp identities, tilted flux controls, and spherical harmonics.")


if __name__ == "__main__":
    main()
