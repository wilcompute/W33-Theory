"""Probe native holomorphic neutral Higgs mixing on the smooth W33 core."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.linalg import svd
import sympy as sp

import toe_20261113_monopole_triplet_shooting as shooting


triplet = shooting.triplet
OUT = triplet.flat.ROOT / "data/toe_20261113_monopole_higgs_mixing.json"
UP = (0, 0, -1, 3)
DOWN = (0, 0, 1, -3)


def flatten(direction):
    matter, adjoint = direction
    return np.column_stack((matter.reshape(-1, 405), adjoint.reshape(-1, 729)))


def horizontal_frames(a, matter, gauge, adjoint, bases):
    x, z = np.split(matter.reshape(5, 81), [3])
    internal = np.concatenate((adjoint, np.zeros((len(gauge)-len(adjoint), 27, 27))))
    variations = np.column_stack(((x @ gauge.transpose(0, 2, 1)).reshape(len(gauge), -1),
                                  (-z @ gauge).reshape(len(gauge), -1),
                                  (internal @ a-a @ internal).reshape(len(gauge), -1)))
    result = []
    for basis in bases:
        u, s, _ = svd(basis @ variations.T, full_matrices=True)
        rank = int(np.sum(s > 1e-9))
        horizontal = u[:, rank:]
        np.testing.assert_allclose(horizontal.T @ basis @ variations.T, 0., atol=1e-8)
        result.append((horizontal, rank))
    return result


def higgs_model():
    flat = triplet.flat
    gauge, adjoint, _, color, weak, y = flat.compact_chart()
    gauge = np.asarray(gauge, dtype=float)
    adjoint = adjoint.astype(float)
    records = np.array(flat.vacuum.native.build_records())
    _, _, _, _, spaces, (_, _, weights) = triplet.flavor.projected_space(
        gauge.astype(int), adjoint.astype(int), color, weak, y, records)
    fixture = flat.read(triplet.flavor.OUT)
    rules = triplet.tensor_and_rules(fixture)
    words = flat.read(flat.OUT)["repair"]["centered_trace_squared_terms"]
    hd_coefficients, = sp.Matrix(fixture["completion"]["lepton_covectors"]).nullspace()
    hd = np.array(hd_coefficients, dtype=float).ravel() @ np.array(spaces[DOWN], dtype=float)
    directions = [triplet.normalize_chiral(triplet.directions(
        np.flatnonzero((weights == weight).all(axis=1)), adjoint)) for weight in (UP, DOWN)]
    bases = [flatten(direction) for direction in directions]
    higgs = []
    for basis, lift in zip(bases, (spaces[UP][0], hd)):
        matter = np.asarray(lift[:405], dtype=float)
        assert not np.any(lift[405:])
        vector = basis[:, :405] @ (matter / np.linalg.norm(matter))
        np.testing.assert_allclose(np.linalg.norm(vector), 1.)
        higgs.append(vector)

    vacuum, embedding, _, residual, _ = triplet.neutral.model()
    meshes = flat.read(shooting.adjoint.MESH)

    def mass(a, matter):
        fixed, varying, _ = triplet.holomorphic_masses(a, matter, *directions, records, words, rules)
        return fixed + varying

    return gauge, adjoint, directions, bases, higgs, vacuum, embedding, residual, meshes, mass, (records, words, rules)


def calculate():
    gauge, adjoint, directions, bases, higgs, vacuum, embedding, residual, meshes, mass, native = higgs_model()
    records, words, rules = native
    results = []
    for mesh in meshes:
        state = np.array(mesh["state"])
        f = residual(state, holomorphic_only=True)
        samples = 33 if mesh is meshes[-1] else 13
        nodes = sorted(set(np.linspace(0, len(state)-1, samples, dtype=int))
                       | {int(np.argmax(np.linalg.norm(f, axis=1)))})
        rows = []
        for i in nodes:
            a, matter = triplet.profile_fields(state[i], embedding)
            fa, fm = triplet.profile_fields(np.r_[0., f[i]], embedding)
            h = 1e-22
            mixing = mass(a+1j*h*fa, matter+1j*h*fm).imag/h
            (u, up_rank), (v, down_rank) = horizontal_frames(a, matter, gauge, adjoint, bases)
            up, down = u.T @ higgs[0], v.T @ higgs[1]
            block = u.T @ mixing @ v
            direct = float(up @ block @ down)
            check_error = None
            gradient_error = None
            if i in (nodes[0], nodes[len(nodes)//3], nodes[-1]):
                h = 1e-5/max(1., np.linalg.norm(f[i]))
                difference = (mass(a+h*fa, matter+h*fm)-mass(a-h*fa, matter-h*fm))/(2*h)
                check_error = float(np.max(np.abs(mixing-difference)))
                probe = np.cos(np.arange(37, dtype=float))
                pa, pm = triplet.profile_fields(np.r_[0., probe], embedding)
                native_jet = triplet.direct_superpotential(a+1e-22j*pa, matter+1e-22j*pm,
                                                           records, words, rules).imag / 1e-22
                np.testing.assert_allclose(native_jet[1:], 0., atol=1e-10)
                np.testing.assert_allclose(native_jet.sum(), f[i] @ probe, atol=1e-8)
                gradient_error = float(abs(native_jet.sum() - f[i] @ probe))
                np.testing.assert_allclose(mixing, difference, atol=5e-4, rtol=5e-6)
            assert (up_rank, down_rank) == (1, 1)
            rows.append(dict(radius=mesh["grid"][i], f_norm=float(np.linalg.norm(f[i])),
                             gauge_ranks=[up_rank, down_rank],
                             retained_higgs_norms=[float(np.linalg.norm(up)), float(np.linalg.norm(down))],
                             horizontal_mixing_frobenius=float(np.linalg.norm(block)),
                             higgs_pair_f_hessian=direct, finite_difference_max_error=check_error,
                             native_gradient_error=gradient_error))
        np.testing.assert_allclose(state[-1], vacuum, atol=1e-10)
        assert rows[-1]["horizontal_mixing_frobenius"] < 1e-6
        peak = max(rows, key=lambda row: abs(row["higgs_pair_f_hessian"]))
        assert abs(peak["higgs_pair_f_hessian"]) > 10
        assert any(row["radius"] > 0 and row["higgs_pair_f_hessian"] > 1 for row in rows)
        assert any(row["higgs_pair_f_hessian"] < -1 for row in rows)
        results.append(dict(mesh=mesh["record"]["elements"], peak_higgs_pair=peak, samples=rows))
    return dict(status="PASS", scope="real smooth-core profiles; local horizontal holomorphic Hessian",
                charge_sector_dimensions=list(map(len, bases)), meshes=results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = calculate()
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for mesh in result["meshes"]:
        print(mesh["mesh"], mesh["peak_higgs_pair"])
