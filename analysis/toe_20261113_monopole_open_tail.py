"""Open-channel transfer on the weak scalar tail of the native monopole."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm

import toe_20261113_monopole_triplet_tail as tail


line = tail.line
OUT = tail.OUT.with_name("toe_20261113_monopole_open_tail.json")


def extend(reflection, grid, generators, energy):
    """Apply the shell transfer to the outgoing-vs-incoming graph."""
    velocity = np.diag([1]*4+[-1]*4)
    frame = np.vstack((reflection, np.eye(4)))
    for width, generator in zip(np.diff(grid), generators):
        frame = expm(width*(generator + 1j*energy*velocity)) @ frame
        frame = np.linalg.solve(frame[4:].T, frame.T).T
    result = frame[:4]
    assert np.linalg.norm(result.conj().T @ result-np.eye(4)) < 1e-8
    return result


def calculate(outer, elements):
    boundary = 4*outer
    requested = boundary*np.array([1, 2, 4, 8])
    nodes = np.unique(np.r_[np.geomspace(boundary, requested[-1], 97)[1:], requested[1:]])
    system, _, _, profile = tail.prepare_tail(outer, elements, exterior_nodes=nodes)
    _, grid, flux, _, _, incoming, outgoing, _, base = system
    open_frame = np.column_stack((outgoing, incoming))
    velocity = np.diag([1]*4+[-1]*4)
    np.testing.assert_allclose(open_frame.conj().T @ flux @ open_frame, velocity, atol=1e-12)
    start = np.flatnonzero(grid == boundary)[0]
    previous = np.argmin(abs(grid-boundary/2))
    base = base[previous:]
    projection = open_frame.conj().T @ base @ open_frame
    np.testing.assert_allclose(projection.conj().transpose(0, 2, 1) @ velocity
                               + velocity @ projection, 0., atol=1e-10)
    leakage = base @ open_frame-open_frame @ projection
    cuts = [np.flatnonzero(grid == r)[0] for r in requested]
    internal = [tail.split_transfers(tail.cut.truncate(system, grid[j])) for j in (previous, start)]
    change_in, change_out = line.flavors.flavor_frames()
    rows = []
    for energy in (0., .002, .004):
        first, reference = (line.residues.matching(s, energy) for s in internal)
        def conversion(r):
            return float(line.conversion(change_out.conj().T @ r @ change_in))
        approximation = extend(first, grid[previous:start+1], projection[:start-previous], energy)
        entry = dict(energy=energy, full_conversion_at_validation_start=conversion(first),
                     full_at_boundary=conversion(reference), projected_at_boundary=conversion(approximation),
                     validation_matrix_error=float(np.linalg.norm(approximation-reference)), extensions=[])
        result = reference
        left = start
        for right in cuts[1:]:
            result = extend(result, grid[left:right+1], projection[left-previous:right-previous], energy)
            entry["extensions"].append(dict(radius=float(grid[right]), conversion=conversion(result)))
            left = right
        rows.append(entry)
        print(entry, flush=True)
    return dict(status="PASS", profile=profile, validation_start=float(grid[previous]),
                boundary=boundary, max_open_closed_coupling_beyond_boundary=float(
                    np.max(np.linalg.norm(leakage[start-previous:], axis=(1, 2)))),
                max_direct_open_coupling_beyond_boundary=float(
                    np.max(np.linalg.norm(projection[start-previous:], axis=(1, 2)))),
                rows=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outer", type=float, default=9.)
    parser.add_argument("--elements", type=int, default=120)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    args.output.write_text(json.dumps(calculate(args.outer, args.elements), indent=2)+"\n",
                           encoding="utf-8")
