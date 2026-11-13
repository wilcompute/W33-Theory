"""Light-channel residues of the finite-cut W33 Weyl resonances."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm, solve_triangular

import toe_20261113_monopole_winding_poles as poles


OUT = poles.OUT.with_name("toe_20261113_monopole_winding_residues.json")


def matching(system, energy):
    _, grid, flux, regular, stable, incoming, outgoing, decay, base = system
    rates = np.sqrt(decay**2-energy**2)
    decaying = stable - (flux @ stable)*(1j*energy/(decay+rates))
    allowed = np.column_stack((decaying, outgoing, incoming))
    mid = poles.threshold.matching_index(grid)
    generators = (base+1j*energy*flux)*np.diff(grid)[:, None, None]
    for generator in generators[:mid]:
        regular = np.linalg.qr(expm(generator) @ regular)[0]

    # Keep enough triangular factors to recover exterior amplitudes.
    right_factors = []
    for generator in generators[:mid-1:-1]:
        allowed, factor = np.linalg.qr(expm(-generator) @ allowed)
        right_factors.append(factor)
    count = incoming.shape[1]
    incoming_quotient = np.eye(count, dtype=complex)
    for factor in right_factors:
        incoming_quotient = factor[-count:, -count:] @ incoming_quotient
    a = np.column_stack((regular, -allowed[:, :-count]))
    forcing = allowed[:, -count:] @ incoming_quotient
    coefficients = np.linalg.solve(a, forcing)
    exterior = np.vstack((coefficients[regular.shape[1]:], incoming_quotient))
    for factor in reversed(right_factors):
        exterior = solve_triangular(factor, exterior)
    np.testing.assert_allclose(exterior[-count:], np.eye(count), atol=1e-10)
    return exterior[-2*count:-count]


def residue(system, center, radius, count):
    z = radius*np.exp(2j*np.pi*np.arange(count)/count)
    return sum(offset*matching(system, center+offset) for offset in z)/count


def inspect_pole(system, energy):
    coarse = residue(system, energy, 8e-5, 12)
    fine = residue(system, energy, 4e-5, 16)
    error = np.linalg.norm(coarse-fine)/np.linalg.norm(fine)
    assert error < 1e-5
    u, s, vh = np.linalg.svd(fine)
    assert s[0] > 1e-5 and s[1] < 1e-5*s[0]
    # A finite-difference Laurent fit provides a second residue estimate.
    h = 5e-6
    def symmetric_estimate(offset):
        return offset*(matching(system, energy+offset)-matching(system, energy-offset))/2

    extrapolated = (4*symmetric_estimate(h/2)-symmetric_estimate(h))/3
    extrap_error = np.linalg.norm(extrapolated-fine)/np.linalg.norm(fine)
    assert extrap_error < 1e-5
    return dict(energy=[energy.real, energy.imag], singular_values=s.tolist(),
                residue_to_width_ratio=float(s[0]/(-2*energy.imag)),
                incident_mode_weights=(abs(vh[0])**2).tolist(),
                outgoing_mode_weights=(abs(u[:, 0])**2).tolist(),
                contour_relative_error=float(error), laurent_relative_error=float(extrap_error),
                real=fine.real.tolist(), imag=fine.imag.tolist())


def calculate(count):
    old = json.loads(poles.OUT.read_text(encoding="utf-8"))
    sectors = {s["sector"]: s for s in old["sectors"]}
    rows = []
    for system in poles.threshold.prepare(count):
        name = system[0]
        real_scattering = [matching(system, e) for e in (0., .002)]
        unitary = max(np.linalg.norm(r.conj().T @ r-np.eye(len(r))) for r in real_scattering)
        assert unitary < 1e-7
        if sectors[name]["poles"]:
            seed = complex(*sectors[name]["poles"][0]["energy"])
            energy, _ = poles.pole(system, seed)
            positive = inspect_pole(system, energy)
            negative = inspect_pole(system, -energy.conjugate())
            np.testing.assert_allclose(positive["singular_values"], negative["singular_values"], atol=1e-10)
            rows.append(dict(sector=name, real_axis_unitarity_error=float(unitary),
                             positive=positive, negative=negative))
            print(name, positive["energy"], positive["singular_values"], positive["residue_to_width_ratio"], flush=True)
        else:
            rows.append(dict(sector=name, real_axis_unitarity_error=float(unitary)))
    return dict(status="PASS", cells=2*count, basis="unit flux at radius 5, numerical vacuum eigenspaces",
                sectors=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=40)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    args.output.write_text(json.dumps(calculate(args.count), indent=2) + "\n", encoding="utf-8")
