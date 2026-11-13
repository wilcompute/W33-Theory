"""Bound tail-generated closed-channel feedback and compare full scattering."""

import argparse
import json
from pathlib import Path

import numpy as np

import toe_20261113_monopole_open_tail as open_tail


tail = open_tail.tail
line = tail.line
OUT = tail.OUT.with_name("toe_20261113_monopole_closed_feedback.json")


def calculate(outer, elements):
    energy = .002
    inner = 4*outer
    end = 2*inner
    nodes = np.geomspace(inner, end, 33)[1:]
    system, _, _, profile = tail.prepare_tail(outer, elements, exterior_nodes=nodes)
    _, grid, flux, _, stable, incoming, outgoing, decay, base = system
    w = np.column_stack((outgoing, incoming))
    q = np.column_stack((stable, flux @ stable))
    np.testing.assert_allclose(q.conj().T @ q, np.eye(q.shape[1]), atol=1e-12)
    np.testing.assert_allclose(q.conj().T @ w, 0., atol=1e-12)
    np.testing.assert_allclose(flux @ q, q @ (q.conj().T @ flux @ q), atol=1e-12)
    vacuum = (flux @ stable*decay) @ (flux @ stable).conj().T - (stable*decay) @ stable.conj().T
    start = int(np.flatnonzero(grid == inner)[0])
    perturbation = 1j*flux @ (base[start:]-vacuum)
    np.testing.assert_allclose(perturbation, perturbation.conj().transpose(0, 2, 1), atol=1e-10)
    mixing = q.conj().T @ perturbation @ w
    closed = q.conj().T @ perturbation @ q
    mixing_norm = np.linalg.norm(mixing, ord=2, axis=(1, 2))
    closed_norm = float(np.max(np.linalg.norm(closed, ord=2, axis=(1, 2))))
    gap = float(min(decay)-abs(energy))
    assert gap > closed_norm
    integrated_mixing_sq = float(np.diff(grid[start:]) @ mixing_norm**2)
    estimate = integrated_mixing_sq/(gap-closed_norm)
    print("shell feedback bound", estimate, flush=True)

    core = tail.split_transfers(tail.cut.truncate(system, inner))
    baseline = line.residues.matching(core, energy)
    projected = open_tail.extend(baseline, grid[start:], w.conj().T @ base[start:] @ w, energy)
    full = line.residues.matching(tail.split_transfers(system), energy)
    change_in, change_out = line.flavors.flavor_frames()

    def conversion(reflection):
        assert np.linalg.norm(reflection.conj().T @ reflection-np.eye(4)) < 1e-8
        return float(line.conversion(change_out.conj().T @ reflection @ change_in))

    return dict(status="PASS", profile=profile, energy=energy, shell=[inner, end],
                vacuum_resolvent_gap=gap, closed_perturbation_norm=closed_norm,
                integrated_coupling_norm_squared=integrated_mixing_sq,
                source_feedback_Linf_to_L1_bound=estimate,
                conversion_at_inner=conversion(baseline),
                projected_conversion_at_outer=conversion(projected),
                full_conversion_at_outer=conversion(full),
                reflection_operator_error=float(np.linalg.norm(full-projected, ord=2)),
                conversion_error=abs(conversion(full)-conversion(projected)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outer", type=float, default=9.)
    parser.add_argument("--elements", type=int, default=120)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = calculate(args.outer, args.elements)
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
