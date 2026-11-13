"""Grand-spin-zero angular currents for the W33 semileptonic exchange."""

import argparse
import json
from pathlib import Path

import numpy as np

import toe_20261113_monopole_yukawa_exchange as exchange


triplet = exchange.triplet
mixing = exchange.radial.mixing
OUT = triplet.flat.ROOT / "data/toe_20261113_monopole_yukawa_angular.json"


def act(op, matter):
    return triplet.chiral_action(op, (matter, np.zeros((len(matter), 27, 27))))[0]


def doublet(root, magnetic, matter, sign):
    generator = root if sign == -1 else root.T
    partner = act(generator, matter)
    np.testing.assert_allclose(act(generator.T, partner), matter, atol=1e-13)
    np.testing.assert_allclose(act(np.diag(magnetic), matter), sign*matter, atol=1e-13)
    np.testing.assert_allclose(act(np.diag(magnetic), partner), -sign*partner, atol=1e-13)
    return (matter, partner) if sign == 1 else (partner, matter)


def vertex(a, matter, scalar, first, second, native):
    return np.array([[exchange.current(a, matter, scalar, f, g, native, 1e-4)
                      for g in second] for f in first])


def angular_control():
    epsilon = np.array([[0, 1], [-1, 0]])
    sigma_x = np.array([[0, 1], [1, 0]])
    sigma_y = np.array([[0, -1j], [1j, 0]])
    sigma_z = np.diag([1, -1])
    error = 0.
    for n in ([0., 0., 1.], [1., 0., 0.], [0., 1., 0.], [1/3, 2/3, 2/3]):
        sigma = sum(x*s for x, s in zip(n, (sigma_x, sigma_y, sigma_z)))
        for u, v, p, q in ((2., 3., -1., .7), (1., 0., 1., 0.), (.2j, 3., 2., -.3j)):
            lhs = ((u*np.eye(2)+v*sigma) @ epsilon).T @ epsilon @ ((p*np.eye(2)+q*sigma) @ epsilon)
            rhs = (u*p-v*q)*epsilon - (v*p-u*q)*sigma @ epsilon
            error = max(error, float(np.max(abs(lhs-rhs))))
    assert error < 1e-13
    return error


def calculate():
    identity_error = angular_control()
    model = mixing.higgs_model()
    gauge, adjoint, _, bases, higgs, _, embedding, _, meshes, _, native = model
    _, _, cartan, color, weak, y = triplet.flat.compact_chart()
    core = triplet.adjoint_phase.core
    five = core.topology.representation_check(adjoint.astype(int), cartan, weak, y)["fundamental5_chart"]
    root, magnetic = core.monopole_root(adjoint.astype(int), five)
    fields = exchange.flavors(model)
    # In the native slot order Q and E^c have n=-1.
    doublets = [doublet(root, magnetic, matter, sign) for matter, sign in zip(fields, (-1, 1, 1, -1))]
    rows = []
    max_scalar_action = 0.
    for mesh in (meshes[0], meshes[-1]):
        grid = np.array(mesh["grid"])
        indices = sorted({int(np.argmin(abs(grid-r))) for r in (0., .025, .05, .1, .2, .4, 1., 5.)})
        for i in indices:
            a, matter = triplet.profile_fields(mesh["state"][i], embedding)
            frames = mixing.horizontal_frames(a, matter, gauge, adjoint, bases)
            for label, ((frame, _), basis, light, first, second) in zip(
                ("QUc", "LEc"), zip(frames, bases, higgs, doublets[::2], doublets[1::2])
            ):
                vector = frame @ (frame.T @ light)
                scalar = (vector @ basis)/np.linalg.norm(vector)
                direction = scalar[:405].reshape(1, 5, 27, 3), scalar[405:].reshape(1, 27, 27)
                for op in (root, root.T):
                    action = mixing.flatten(triplet.chiral_action(op, direction))
                    max_scalar_action = max(max_scalar_action, float(np.linalg.norm(action)))
                forward = vertex(a, matter, scalar, first[0], second[1], native)
                reverse = vertex(a, matter, scalar, first[1], second[0], native)
                singlet = (forward-reverse)/2
                triplet_part = (forward+reverse)/2
                if i == 0:
                    np.testing.assert_allclose(triplet_part, 0., atol=1e-8)
                rows.append(dict(mesh=mesh["record"]["elements"], radius=float(grid[i]), vertex=label,
                                 forward=forward.tolist(), reverse=reverse.tolist(),
                                 singlet_norm=float(np.linalg.norm(singlet)),
                                 triplet_norm=float(np.linalg.norm(triplet_part))))
    assert max_scalar_action < 1e-12
    return dict(status="PASS", max_scalar_root_action=max_scalar_action,
                angular_identity_error=identity_error, samples=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = calculate()
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for row in result["samples"]:
        if row["mesh"] == 160:
            print(row["radius"], row["vertex"], row["singlet_norm"], row["triplet_norm"])
