"""Test the far-tail projected reflection and the possible Coulomb term."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.special import exp1

import toe_20261113_monopole_open_tail as open_tail


tail = open_tail.tail
line = tail.line
OUT = tail.OUT.with_name("toe_20261113_monopole_far_tail.json")


def calculate(outer, elements, cells_per_octave):
    solution = tail.solve_profile(outer, elements)
    _, vacuum, masses, modes, amplitudes, report = solution
    boundary = 4*outer
    endpoint = boundary*128
    cuts = boundary*2.**np.arange(8)
    nodes = np.geomspace(boundary, endpoint, 7*cells_per_octave+1)
    nodes[::cells_per_octave] = cuts
    system, _, _, _ = tail.prepare_tail(outer, elements, exterior_nodes=nodes[1:], solution=solution)
    _, grid, flux, _, _, incoming, outgoing, _, base = system
    w = np.column_stack((outgoing, incoming))
    begin = int(np.flatnonzero(grid == boundary)[0])
    g = w.conj().T @ base[begin:] @ w
    energy = .002
    core = tail.split_transfers(tail.cut.truncate(system, boundary))
    reflection = line.residues.matching(core, energy)
    incoming_flavors, outgoing_flavors = line.flavors.flavor_frames()
    rows = []
    i = 0
    for j in range(cells_per_octave, len(nodes), cells_per_octave):
        reflection = open_tail.extend(reflection, nodes[i:j+1], g[i:j], energy)
        value = line.conversion(outgoing_flavors.conj().T @ reflection @ incoming_flavors)
        rows.append(dict(radius=float(nodes[j]), conversion=float(value)))
        print(rows[-1], flush=True)
        i = j

    # Evaluate the massless-direction derivative in the same native
    # operator. The finite probe grid is used solely to reuse its evaluator.
    zero = masses == 0
    direction = np.r_[0., (outer*amplitudes[zero]) @ modes[zero]]
    h = .01
    probe_nodes = np.arange(1., 7.)
    strengths = np.array([0., h, -h, h/2, -h/2])
    def probe(radius):
        index = int(radius-1.)
        return vacuum + strengths[np.clip(index, 0, len(strengths)-1)]*direction
    threshold = tail.threshold
    probe_system = next(threshold.prepare(1, sectors=("L",), outer_radius=1.,
                                          exterior_nodes=probe_nodes[1:], profile_override=probe))
    probe_w = np.column_stack((probe_system[6], probe_system[5]))
    p = probe_w.conj().T @ probe_system[-1][-5:] @ probe_w
    derivative = (p[1]-p[2])/(2*h)
    finer = (p[3]-p[4])/h
    coulomb = (4*finer-derivative)/3
    diagonal = np.zeros_like(coulomb)
    diagonal[:4, :4] = coulomb[:4, :4]
    diagonal[4:, 4:] = coulomb[4:, 4:]
    midpoint = (nodes[1:]+nodes[:-1])/2
    norms = np.linalg.norm(g, ord=2, axis=(1, 2))
    rate = float(min(masses[~zero]))
    # A diagnostic only. This envelope excludes the possible Coulomb
    # contribution and its multiplier is inferred on a finite grid.
    scaled = np.linalg.norm(g-coulomb/midpoint[:, None, None], ord=2, axis=(1, 2))*midpoint
    envelope = float(np.max(scaled*np.exp(rate*(midpoint-outer))))
    return dict(status="PASS", energy=energy, profile=report, cells_per_octave=cells_per_octave,
                projected_rows=rows, max_sampled_generator_norm=float(max(norms)),
                massless_tail_coefficient_norm=float(np.linalg.norm(direction)),
                sampled_coulomb_derivative_norm=float(np.linalg.norm(coulomb, ord=2)),
                coulomb_off_diagonal_norm=float(np.linalg.norm(coulomb-diagonal, ord=2)),
                derivative_refinement_difference=float(np.linalg.norm(finer-derivative, ord=2)),
                slowest_positive_scalar_mass=rate, sampled_yukawa_envelope=envelope,
                conditional_yukawa_integral=float(envelope*np.exp(rate*outer)*exp1(rate*endpoint)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outer", type=float, default=9.)
    parser.add_argument("--elements", type=int, default=120)
    parser.add_argument("--cells-per-octave", type=int, default=16)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = calculate(args.outer, args.elements, args.cells_per_octave)
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print({k:v for k,v in result.items() if k != "profile"}, flush=True)
