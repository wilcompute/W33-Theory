"""Separate open-closed mixing and closed-block effects on a W33 monopole shell."""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm

import toe_20261113_monopole_open_tail as open_tail

tail = open_tail.tail
line = tail.line
OUT = tail.OUT.with_name("toe_20261114_monopole_closed_shell_sign.json")


def core_basis(system, energy):
    _, grid, flux, regular, *_rest, base = system
    for width, cell in zip(np.diff(grid), base, strict=True):
        regular = np.linalg.qr(expm(width * (cell + 1j * energy * flux)) @ regular)[0]
    return regular


def exterior_match(regular, stable, outgoing, incoming, transfers):
    # Backward QR decompositions track the maps on the incoming quotient.
    width = incoming.shape[1]
    allowed = np.column_stack((stable, outgoing, incoming))
    factors = []
    incoming_quotient = np.eye(width, dtype=complex)
    for transfer in reversed(transfers):
        allowed, factor = np.linalg.qr(transfer @ allowed)
        factors.append(factor)
        incoming_quotient = factor[-width:, -width:] @ incoming_quotient
    matrix = np.column_stack((regular, -allowed[:, :-width]))
    solution = np.linalg.solve(matrix, allowed[:, -width:] @ incoming_quotient)
    coeff = np.vstack((solution[regular.shape[1]:], incoming_quotient))
    # Recover only the outgoing/incoming amplitudes. Triangularity makes
    # these coordinates independent of the massive amplitudes above them.
    for factor in reversed(factors):
        coeff = np.linalg.solve(factor[-2*width:, -2*width:], coeff[-2*width:])
    np.testing.assert_allclose(coeff[-width:], np.eye(width), atol=1e-10)
    return coeff[-2*width:-width]


def calculate(elements, cells, radii):
    energy = .002
    inner = 36.
    nodes = np.unique(np.concatenate([np.geomspace(a, b, cells+1)[1:]
                                       for a, b in zip([inner, *radii[:-1]], radii)]))
    system, _, _, report = tail.prepare_tail(9., elements, exterior_nodes=nodes)
    _, grid, flux, _, stable, incoming, outgoing, decay, base = system
    w = np.column_stack((outgoing, incoming))
    start = int(np.flatnonzero(grid == inner)[0])
    shell = base[start:]
    widths = np.diff(grid[start:])
    core = tail.split_transfers(tail.cut.truncate(system, inner))
    regular = core_basis(core, energy)
    rates = np.sqrt(decay**2 - energy**2)
    decaying = stable - (flux @ stable) * (1j*energy/(decay + rates))
    baseline = exterior_match(regular, decaying, outgoing, incoming, [])
    expected = line.residues.matching(core, energy)
    np.testing.assert_allclose(baseline, expected, atol=1e-9, rtol=0)
    pin = w @ w.conj().T
    q = np.eye(len(pin))-pin
    vacuum = (flux @ stable*decay) @ (flux @ stable).conj().T - (stable*decay) @ stable.conj().T
    open_part = pin @ shell @ pin
    closed_part = q @ shell @ q
    mixed = shell-open_part-closed_part
    change_in, change_out = line.flavors.flavor_frames()

    def conversion(reflection):
        np.testing.assert_allclose(reflection.conj().T @ reflection, np.eye(4), atol=1e-9)
        return float(line.conversion(change_out.conj().T @ reflection @ change_in))

    # Same discretized open and closed blocks, three signs of their coupling.
    # Reuse only moderate transfer lengths to avoid the growing massive modes.
    matrices = {"plus": shell, "minus": shell-2*mixed, "zero": open_part+closed_part,
                "vacuum_closed": open_part+vacuum}
    rows = []
    for radius in radii:
        end = int(np.flatnonzero(grid == radius)[0])-start
        results = {}
        for label, branch in matrices.items():
            pieces = np.maximum(1, np.ceil(widths[:end]/.18).astype(int))
            steps = (branch[:end]+1j*energy*flux)*(widths[:end]/pieces)[:, None, None]
            transfers = np.repeat(expm(-steps), pieces, axis=0)
            results[label] = exterior_match(regular, decaying, outgoing, incoming, transfers)
        projected = open_tail.extend(baseline, grid[start:start+end+1],
                                     w.conj().T @ shell[:end] @ w, energy)
        np.testing.assert_allclose(projected, results["vacuum_closed"], atol=1e-9, rtol=0)
        if radius == radii[0]:
            check = line.residues.matching(tail.split_transfers(tail.cut.truncate(system, radius)), energy)
            np.testing.assert_allclose(check, results["plus"], atol=1e-9, rtol=0)
        plus, minus, zero = (results[key] for key in ("plus", "minus", "zero"))
        p, m, z, b = map(conversion, (plus, minus, zero, projected))
        row = dict(radius=radius, projected=b, full=p, full_minus_projected=p-b,
                   closed_block_only=z-b, coupling_odd=(p-m)/2, coupling_even=(p+m)/2-z,
                   matrix_odd_norm=float(np.linalg.norm((plus-minus)/2, ord=2)),
                   matrix_even_norm=float(np.linalg.norm((plus+minus)/2-zero, ord=2)))
        assert abs(row["full_minus_projected"]-sum(row[key] for key in
                   ("closed_block_only", "coupling_odd", "coupling_even"))) < 2e-16
        print(row, flush=True)
        rows.append(row)
    return dict(energy=energy, inner_radius=inner, cells_per_interval=cells, rows=rows, profile=report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", type=int, default=32)
    parser.add_argument("--radii", type=float, nargs="+", default=[72., 144., 288.])
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    assert args.cells > 0 and sorted(set(args.radii)) == args.radii and args.radii[0] > 36.
    result = calculate(120, args.cells, args.radii)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
