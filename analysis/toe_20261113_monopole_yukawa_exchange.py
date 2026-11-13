"""Match native Yukawa currents against the two-Higgs W33 radial inverse."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.linalg import qr
from scipy.sparse import bmat, csc_matrix
from scipy.sparse.linalg import spsolve
import sympy as sp

import toe_20261113_monopole_higgs_radial as radial


triplet = radial.triplet
OUT = triplet.flat.ROOT / "data/toe_20261113_monopole_yukawa_exchange.json"
QU = ((1, -1, 1, 1), (-1, 1, 0, -4))
LE = ((0, 0, -1, -3), (0, 0, 0, 6))


def flavors(model):
    gauge, adjoint, *_ = model
    flat = triplet.flat
    _, _, _, color, weak, y = flat.compact_chart()
    records = model[-1][0]
    _, _, _, _, spaces, _ = triplet.flavor.projected_space(
        gauge.astype(int), adjoint.astype(int), color, weak, y, records)
    fixture = flat.read(triplet.flavor.OUT)
    h = sp.Matrix([fixture["completion"]["down_higgs_covector"]])
    # The Higgs covector is recorded on the upper doublet lift basis.
    upper = spaces[(0, 0, 1, -3)]
    lower = np.array([triplet.flavor.lower_doublet(v, weak) for v in upper], dtype=float)
    lepton_coefficients = np.array(h.nullspace(), dtype=float).reshape(3, 4)
    leptons = lepton_coefficients @ lower
    np.testing.assert_allclose(lepton_coefficients @ np.array(h, float).ravel(), 0.)
    assert np.linalg.matrix_rank(np.vstack((lower, np.array(spaces[LE[0]], float)))) == 4
    weights = (*QU, *LE)
    for pair, higgs_weight in zip((QU, LE), (radial.mixing.UP, radial.mixing.DOWN)):
        assert all(a+b+c == 0 for a, b, c in zip(*pair, higgs_weight))
    result = []
    for weight in weights:
        lifts = leptons if weight == LE[0] else np.array(spaces[weight], dtype=float)
        assert lifts.shape == (3, 483) and not np.any(lifts[:, 405:])
        result.append(qr(lifts[:, :405].T, mode="economic")[0].T.reshape(3, 5, 27, 3))
    return result


def current(a, matter, scalar, first, second, native, step):
    # Differentiate in the scalar direction by complex step, and in the
    # two fermion flavor directions by symmetric polarization.
    scalar_a = scalar[405:].reshape(27, 27)
    scalar_m = scalar[:405].reshape(5, 27, 3)
    eps = 1e-22
    total = 0.
    for i, j in ((1, 1), (-1, -1), (1, -1), (-1, 1)):
        fields = matter + step*(i*first+j*second) + 1j*eps*scalar_m
        total += i*j*triplet.direct_superpotential(a+1j*eps*scalar_a, fields, *native).imag.sum()
    return total/(4*step**2*eps)


def sources(model, mesh, grid, data, flavor):
    native = model[-1]
    embedding = model[6]
    state = CubicSpline(mesh["grid"], mesh["state"])(grid)
    sample = sorted(set(np.linspace(0, len(grid)-1, 27, dtype=int))
                    | {int(np.argmin(abs(grid-r))) for r in (.025, .055, .1, .2, .4)})
    sampled_grid = grid[sample]
    matrices = []
    controls = []
    for idx in sample:
        a, matter = triplet.profile_fields(state[idx], embedding)
        row = []
        for higgs, (first, second) in zip(data[idx][0], (flavor[:2], flavor[2:])):
            jac = np.array([[current(a, matter, higgs, f, g, native, 1e-4) for g in second] for f in first])
            if idx in (sample[0], sample[len(sample)//2], sample[-1]):
                other = np.array([[current(a, matter, higgs, f, g, native, 2e-4) for g in second] for f in first])
                np.testing.assert_allclose(jac, other, atol=2e-5, rtol=2e-5)
                controls.append(float(np.max(abs(jac-other))))
            row.append(jac)
        matrices.append(row)
    matrices = np.array(matrices)
    sv = np.linalg.svd(matrices[-1], compute_uv=False)
    assert np.min(sv) > 0.05
    return CubicSpline(sampled_grid, matrices)(grid), dict(
        samples=len(sample), vacuum_singular_values=sv.tolist(),
        maximum_polarization_step_difference=max(controls),
        sampled_yukawa_matrices=matrices.tolist(), sample_radii=sampled_grid.tolist())


def contract(grid, data, matrices, exterior):
    diagonal, mixing, measure = radial.assemble(grid, data, exterior=exterior)
    cross = csc_matrix(mixing)
    stiffness = bmat([[csc_matrix(diagonal[0]), cross],
                      [cross, csc_matrix(diagonal[1])]], format="csc")
    interior = np.s_[1:] if exterior else np.s_[1:-1]
    r = grid[interior]
    results = []
    for width in (.08, .16, .32):
        # Both reduced fermions use r exp(-r^2/(2 width^2)), giving
        # a reduced scalar source proportional to r exp(-r^2/width^2).
        packet = r*np.exp(-(r/width)**2)
        packet /= np.sqrt(packet @ measure @ packet)
        first, second = [measure @ (packet[:, None]*matrices[interior, i].reshape(-1, 9))
                         for i in (0, 1)]
        rhs = np.vstack((np.zeros_like(second), second))
        solution = spsolve(stiffness, rhs)
        error = float(np.linalg.norm(stiffness @ solution-rhs)/np.linalg.norm(rhs))
        assert error < 1e-7
        tensor = first.T @ solution[:len(r)]
        # Three quartics absorb one copy of every flavor in all four slots.
        # Use exterior cubes rather than a rank test of the flattened tensor.
        saturated = winding_coefficient(tensor.reshape(3, 3, 3, 3))
        results.append(dict(width=width, frobenius=float(np.linalg.norm(tensor)),
                            winding_flavor_coefficient=saturated,
                            relative_residual=error, tensor=tensor.reshape(3, 3, 3, 3).tolist()))
    return results


def winding_coefficient(tensor):
    epsilon = np.zeros((3, 3, 3))
    epsilon[0, 1, 2] = epsilon[1, 2, 0] = epsilon[2, 0, 1] = 1
    epsilon[0, 2, 1] = epsilon[2, 1, 0] = epsilon[1, 0, 2] = -1
    return float(np.einsum("aei,bfj,cgk,dhl,abcd,efgh,ijkl->", epsilon, epsilon,
                           epsilon, epsilon, tensor, tensor, tensor, optimize=True)/6)


def calculate():
    identity = np.eye(3)
    np.testing.assert_allclose(winding_coefficient(np.einsum("ab,cd->abcd", identity, identity)), 6.)
    model = radial.mixing.higgs_model()
    flavor = flavors(model)
    results = []
    for mesh in (model[8][0], model[8][-1]):
        stride = 3 if mesh is model[8][-1] else 2
        indices = sorted(set(range(0, len(mesh["grid"]), stride)) | {len(mesh["grid"])-1})
        reduced = dict(mesh, grid=[mesh["grid"][i] for i in indices], state=[mesh["state"][i] for i in indices])
        grid, data = radial.radial_coefficients(model, reduced)
        matrices, audit = sources(model, mesh, grid, data, flavor)
        wall = contract(grid, data, matrices, False)
        tail = contract(grid, data, matrices, True)
        assert all(row["frobenius"] > 1e-6 for row in wall+tail)
        assert all(abs(row["winding_flavor_coefficient"]) > 1e-16 for row in wall+tail)
        results.append(dict(background_elements=mesh["record"]["elements"], source_checks=audit,
                            dirichlet=wall, free_exterior=tail))
        print(results[-1]["background_elements"], [(r["width"], r["frobenius"], r["winding_flavor_coefficient"])
                                                    for r in tail], flush=True)
    return dict(status="PASS", scope="vacuum light flavor lifts, smooth trial fermion packets, two Higgs directions",
                results=results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    args.output.write_text(json.dumps(calculate(), indent=2) + "\n", encoding="utf-8")
