"""Two-Higgs variational radial resolvent on the real W33 monopole."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq
from scipy.sparse import bmat, csc_matrix
from scipy.sparse.linalg import spsolve

import toe_20261113_monopole_higgs_mixing as mixing


triplet = mixing.triplet
OUT = triplet.flat.ROOT / "data/toe_20261113_monopole_higgs_radial.json"


def quadratic_moments(direction, embedding):
    matter, adjoint = direction
    x, z = matter[:3], matter[3:]
    internal = adjoint @ adjoint.T-adjoint.T @ adjoint
    internal += np.sum(x @ x.transpose(0, 2, 1), axis=0)
    internal -= np.sum(z @ z.transpose(0, 2, 1), axis=0)
    family = np.sum(x.transpose(0, 2, 1) @ x, axis=0)
    family -= np.sum(z.transpose(0, 2, 1) @ z, axis=0)
    return np.r_[np.einsum("ij,aij->a", internal, embedding), family.ravel()]


def radial_coefficients(model, mesh):
    gauge, adjoint, directions, bases, higgs, _, embedding, residual, _, mass, _ = model
    _, _, cartan, color, weak, y = triplet.flat.compact_chart()
    core = triplet.adjoint_phase.core
    five = core.topology.representation_check(adjoint.astype(int), cartan, weak, y)["fundamental5_chart"]
    step, magnetic = core.monopole_root(adjoint.astype(int), five)
    grid, states = np.array(mesh["grid"]), np.array(mesh["state"])
    data = []
    for state, f in zip(states, residual(states)):
        a, matter = triplet.profile_fields(state, embedding)
        frames = mixing.horizontal_frames(a, matter, gauge, adjoint, bases)
        coeffs = [frame @ (frame.T @ vector) for (frame, rank), vector in zip(frames, higgs)]
        coeffs = [vector/np.linalg.norm(vector) for vector in coeffs]
        vectors = [vector @ basis for vector, basis in zip(coeffs, bases)]
        scalar_dirs = [(v[:405].reshape(5, 27, 3), v[405:].reshape(27, 27)) for v in vectors]
        block = mass(a, matter)
        fa, fm = triplet.profile_fields(np.r_[0., f[:37]], embedding)
        h = 1e-22
        b = float(coeffs[0] @ (mass(a+1j*h*fa, matter+1j*h*fm).imag/h) @ coeffs[1])
        mf = [np.linalg.norm(block.T @ coeffs[0])**2, np.linalg.norm(block @ coeffs[1])**2]
        diag = [value + f[37:] @ quadratic_moments(direction, embedding)
                for value, direction in zip(mf, scalar_dirs)]
        angular = []
        for direction in scalar_dirs:
            matter_d, adj_d = direction
            assert not np.any(magnetic[:, None]*matter_d.transpose(1, 0, 2).reshape(27, -1))
            assert not np.any((magnetic[:, None]-magnetic[None, :])*adj_d)
            batch = matter_d[None], adj_d[None]
            norm = sum(np.linalg.norm(mixing.flatten(triplet.chiral_action(op, batch)))**2
                       for op in (step, step.T))/2
            angular.append(norm*(state[0]/triplet.neutral.SQRT6)**2)
        data.append((vectors, diag, angular, b))
    return grid, data


def assemble(grid, data, exterior=False):
    # Reduced field u=r h. The endpoint constraints are u(0)=u(R)=0.
    n = len(grid)
    kinetic = np.zeros((2, n, n))
    norm = np.zeros((n, n))
    coupling = np.zeros((n, n))
    gauss, weights = np.polynomial.legendre.leggauss(4)
    for i, width in enumerate(np.diff(grid)):
        idx = slice(i, i+2)
        for node, weight in zip(gauss, weights):
            shape = np.array([1-node, 1+node])/2
            radius = shape @ grid[idx]
            weight *= width/2
            overlap = weight*np.outer(shape, shape)
            norm[idx, idx] += overlap
            left, right = data[i], data[i+1]
            coupling[idx, idx] += (shape @ [left[3], right[3]])*overlap
            for h in range(2):
                frame = shape @ np.array([left[0][h], right[0][h]])
                raw_deriv = (right[0][h]-left[0][h])/width
                length = np.linalg.norm(frame)
                frame /= length
                deriv = (raw_deriv-frame*(frame @ raw_deriv))/length
                columns = np.array([-1., 1.])[:, None]*frame/width + shape[:, None]*deriv
                potential = shape @ [left[1][h], right[1][h]]
                potential += (shape @ [left[2][h], right[2][h]])/radius**2
                kinetic[h, idx, idx] += weight*(columns @ columns.T) + potential*overlap
    interior = np.s_[1:, 1:] if exterior else np.s_[1:-1, 1:-1]
    return [block[interior] for block in kinetic], coupling[interior], norm[interior]


def cross_response(diagonal, coupling, norm, source, omega, exterior=False):
    blocks = [csc_matrix(block+omega**2*norm) for block in diagonal]
    if exterior:
        # The reduced free exterior is exp(-omega*(r-R)), including
        # the constant static solution corresponding to h proportional to 1/r.
        surface = csc_matrix(([omega], ([len(source)-1], [len(source)-1])), shape=norm.shape)
        blocks = [block + surface for block in blocks]
    cross = csc_matrix(coupling)
    operator = bmat([[blocks[0], cross], [cross, blocks[1]]], format="csc")
    rhs = np.r_[np.zeros_like(source), source]
    solution = spsolve(operator, rhs)
    residual = np.linalg.norm(operator @ solution-rhs)/np.linalg.norm(rhs)
    assert residual < 1e-5
    # The odd block is conjugate by diag(1,-1). Its inverse has the
    # opposite cross term, so the holomorphic propagator is this cross term.
    return dict(omega=omega, cross=float(source @ solution[:len(source)]),
                relative_residual=float(residual))


def solve(grid, data):
    diagonal, coupling, norm = assemble(grid, data)
    tail_diagonal, tail_coupling, tail_norm = assemble(grid, data, exterior=True)
    even = np.block([[diagonal[0], coupling], [coupling, diagonal[1]]])
    measure = np.kron(np.eye(2), norm)
    spectrum = eigh(even, measure, subset_by_index=[0, 2], eigvals_only=True)
    x = grid[1:-1]
    results = []
    for center, width in ((.03, .018), (.1, .05), (.24, .09)):
        profile = x*np.exp(-((x-center)/width)**2)
        profile /= np.sqrt(profile @ norm @ profile)
        source = norm @ profile
        tail_source = tail_norm @ np.r_[profile, 0.]
        responses = [cross_response(diagonal, coupling, norm, source, omega)
                     for omega in (0., .1, .3, 1., 3., 10., 1000.)]
        tails = [cross_response(tail_diagonal, tail_coupling, tail_norm, tail_source, omega, exterior=True)
                 for omega in (0., .1, .3, 1., 3., 10.)]
        moment = -profile @ coupling @ profile
        np.testing.assert_allclose(responses[-1]["cross"]*1000**4, moment, rtol=.03)
        assert responses[0]["cross"] < -1e-6 and tails[0]["cross"] < -1e-6
        zero = None
        if center == .03:
            def response_at(omega):
                return cross_response(diagonal, coupling, norm, source, omega)["cross"]

            zero = brentq(response_at, 1., 3., xtol=1e-9)
            assert abs(response_at(zero)) < 1e-12
        results.append(dict(center=center, width=width, high_frequency_moment=float(moment),
                            dirichlet_zero_between_one_and_three=zero,
                            responses=responses, vacuum_tail_responses=tails))
    return dict(lowest_ritz_values=spectrum.tolist(), profiles=results)


def calculate():
    model = mixing.higgs_model()
    results = []
    for mesh in model[8]:
        # Keep comparable coarsening on each stationary background mesh.
        step = 2 if mesh["record"]["elements"] < 160 else 3
        indices = sorted(set(range(0, len(mesh["grid"]), step)) | {len(mesh["grid"])-1})
        radial = dict(mesh, grid=[mesh["grid"][i] for i in indices],
                      state=[mesh["state"][i] for i in indices])
        grid, data = radial_coefficients(model, radial)
        result = solve(grid, data)
        result.update(background_elements=mesh["record"]["elements"], radial_nodes=len(grid), outer_radius=grid[-1])
        results.append(result)
        print(result["background_elements"], result["lowest_ritz_values"],
              [row["responses"][0]["cross"] for row in result["profiles"]], flush=True)
    return dict(status="PASS", scope="two horizontal Higgs directions in a fixed gauge background",
                meshes=results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    args.output.write_text(json.dumps(calculate(), indent=2) + "\n", encoding="utf-8")
