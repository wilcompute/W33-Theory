"""Resolve the W33 triplet light reflection into charge and rotor sectors."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.linalg import null_space, schur

import toe_20261113_monopole_triplet_shooting as shooting


triplet = shooting.triplet
flat = triplet.flat
OUT = flat.ROOT / 'data/toe_20261113_monopole_triplet_charge.json'


def threshold_triplets(plus_weight, minus_weight):
    ledger = flat.read('data/toe_20261110_monopole_boundary_lattice.json')
    color_root = (2, -1, 0, 0)

    def negative(weight):
        return tuple(-entry for entry in weight)

    def triples(weights, target):
        assert target not in weights
        character = Counter(tuple(map(sum, zip(*group))) for group in combinations(weights, 3))
        raised = tuple(map(sum, zip(target, color_root)))
        witnesses = sorted({tuple(sorted(group)) for group in combinations(weights, 3)
                            if tuple(map(sum, zip(*group))) == target})
        assert all(all(negative(w) not in group for w in group) for group in witnesses)
        return dict(target_weight=list(map(int, target)), cartan_weight_multiplicity=character[target],
                    residual_color_singlet_multiplicity=character[target]-character[raised],
                    unordered_weight_witnesses=witnesses)

    incoming = [tuple(w) for w in ledger['incoming_signed_pair_order']]
    outgoing = [tuple(w) for w in ledger['outgoing_particle_order']]
    incoming += [negative(w) for w in incoming]
    outgoing += [negative(w) for w in outgoing]
    excluded = {tuple(minus_weight), negative(minus_weight)}
    extra_in = triples([w for w in incoming if w not in excluded], tuple(minus_weight))
    extra_out = triples(outgoing, tuple(plus_weight))
    assert extra_in['residual_color_singlet_multiplicity'] == 9
    assert extra_out['residual_color_singlet_multiplicity'] == 12
    return dict(incoming_without_Hu_or_its_hole=extra_in, outgoing_without_a_rotor_step=extra_out)


def chiral_lifts(lifts, direction, kernel):
    vectors = np.array(lifts, dtype=float)
    assert not np.any(vectors[:, 405:])
    matter = direction[0].reshape(len(direction[0]), 405)
    coordinates = matter @ vectors[:, :405].T
    coordinates = np.pad(coordinates, ((0, kernel.shape[0]-len(matter)), (0, 0)))
    projection = kernel @ (kernel.conj().T @ coordinates)
    assert np.linalg.matrix_rank(projection, tol=1e-9) == len(lifts)
    return projection


def flux_lift(vectors, side, sign, left_dim, right_dim):
    angular = np.vstack((vectors, -sign*vectors))/np.sqrt(2)
    if side == 'left':
        return np.vstack((angular, np.zeros((2*right_dim, angular.shape[1]))))
    return np.vstack((np.zeros((2*left_dim, angular.shape[1])), angular))


def physical_model():
    gauge, adjoint, cartan, color, weak, y = flat.compact_chart()
    records = flat.vacuum.native.build_records()
    x, dual, _, fundamental, spaces, (_, _, weights) = triplet.flavor.projected_space(
        gauge, adjoint, color, weak, y, records)
    triplet.flavor.check_old_cubic(spaces)
    core = triplet.adjoint_phase.core
    five = core.topology.representation_check(adjoint, cartan, weak, y)['fundamental5_chart']
    step, magnetic = core.monopole_root(adjoint, five)
    alpha = fundamental[five[0]]-fundamental[five[3]]
    plus_weight, minus_weight = np.array(triplet.WEIGHTS)
    assert np.array_equal(plus_weight-minus_weight, alpha)
    pairing = sp.Matrix(fundamental).gauss_jordan_solve(sp.Matrix(magnetic))[0]
    assert sp.Matrix([plus_weight.tolist(), minus_weight.tolist()])*pairing == sp.Matrix([1, -1])
    assert np.array_equal(fundamental[five[0]], plus_weight)

    frames, (right_dim, left_dim) = triplet.doublet_frames(adjoint, weights, step)
    words = flat.read(flat.OUT)['repair']['centered_trace_squared_terms']
    fixture = flat.read(triplet.flavor.OUT)
    rules = triplet.tensor_and_rules(fixture)
    evaluators = tuple(triplet.mass_evaluator(*frame, np.array(records), words, rules) for frame in frames)
    vacuum = np.diag(y).astype(float), np.concatenate((x, dual)).reshape(5, 27, 3).astype(float)
    mplus, mminus = [a+b for a, b in (evaluate(*vacuum) for evaluate in evaluators)]
    incoming_d = chiral_lifts(spaces[tuple(-plus_weight)], frames[0][0], null_space(mplus.T))
    incoming_h = chiral_lifts(spaces[tuple(minus_weight)], frames[1][1], null_space(mminus))
    assert incoming_d.shape[1] == 3 and incoming_h.shape[1] == 1
    d = np.linalg.qr(incoming_d)[0]
    hu = np.linalg.qr(incoming_h)[0]

    upper_weight = tuple(fundamental[15])
    lower_lifts = [triplet.flavor.lower_doublet(vector, weak) for vector in spaces[upper_weight]]
    assert len(lower_lifts) == 4 and all(
        not np.any(vector[(weights != -minus_weight).any(axis=1)]) for vector in lower_lifts)
    down = chiral_lifts(lower_lifts, frames[1][0], null_space(mminus.T))
    covector = np.array(fixture['completion']['down_higgs_covector'], dtype=float)
    lepton = np.linalg.qr(down @ null_space(covector[None]))[0]
    higgs = down @ np.linalg.solve(down.conj().T @ down, covector)
    higgs = higgs / np.linalg.norm(higgs)
    np.testing.assert_allclose(lepton.conj().T @ higgs, 0., atol=1e-12)
    outgoing = np.column_stack((lepton, higgs))

    light = np.column_stack((flux_lift(d, 'right', 1, left_dim, right_dim),
                             flux_lift(hu, 'left', -1, left_dim, right_dim),
                             flux_lift(outgoing, 'right', -1, left_dim, right_dim)))
    np.testing.assert_allclose(light.conj().T @ light, np.eye(8), atol=1e-12)
    flux, _ = triplet.radial_hamiltonian(mplus, mminus, 0.)
    np.testing.assert_allclose(flux @ light, light*np.array([-1]*4+[1]*4), atol=1e-12)
    charges = dict(incoming_weights=[plus_weight.tolist()]*3+[minus_weight.tolist()],
                   outgoing_weights=[minus_weight.tolist()]*4,
                   incoming_labels=['D^c conjugate']*3+['H_u'],
                   outgoing_labels=['L conjugate']*3+['H_d conjugate'],
                   rotor_root=alpha.tolist(), rotor_steps=[1, 1, 1, 0],
                   endpoint_character_of_each_light_state=-1,
                   incoming_outgoing_open_channel_counts_at_fixed_total_weight={
                       'between_thresholds_when_outgoing_rotor_energy_is_lower': [1, 4],
                       'between_thresholds_when_down_input_rotor_energy_is_lower': [3, 0],
                       'above_both_thresholds': [4, 4],
                   },
                   asymptotic_witten_shift=(3*plus_weight).tolist(),
                   fixed_outgoing_cartan_trace_at_winding_three=(3*minus_weight).tolist(),
                   incoming_electric_charges_in_sixths=[int(3*plus_weight[2]+plus_weight[3])]*3
                                                         +[int(3*minus_weight[2]+minus_weight[3])],
                   outgoing_electric_charges_in_sixths=[int(3*minus_weight[2]+minus_weight[3])]*4,
                   rotor_root_electric_charge_in_sixths=int(3*alpha[2]+alpha[3]))
    for weight, n in zip(charges['incoming_weights'], charges['rotor_steps']):
        assert np.array_equal(np.array(weight)-minus_weight, n*alpha)
    flow = flat.read('data/toe_20261113_monopole_heavy_phase_flow.json')['monopole_channel_count']
    adjoint_weights = np.array(flow[0]['unit_flux_weights']) @ fundamental[five]
    assert sp.Matrix(adjoint_weights)*pairing == sp.ones(3, 1)
    blocks = flat.read(triplet.adjoint_phase.OUT)['blocks']
    assert {tuple(2*w-alpha) for w in adjoint_weights} == {
        tuple(row['doubled_perpendicular_weight']) for row in blocks
    }
    assert all(row['vacuum_integer_gauge_commutator'][0][0] == 0
               and row['vacuum_integer_trace_hessian'][0][0] for row in blocks)
    charges['adjoint_light_weights_each_direction'] = adjoint_weights.tolist()
    charges['adjoint_rotor_steps'] = [0]*3
    charges['adjoint_fixed_outgoing_cartan_trace'] = adjoint_weights.sum(axis=0).tolist()
    charges['between_threshold_multiparticle_candidates'] = threshold_triplets(plus_weight, minus_weight)
    return (triplet.neutral.geometry()[0], evaluators, vacuum), light, charges


def unitary(matrix):
    u, _, vh = np.linalg.svd(matrix)
    return u @ vh


def projected_winding(reflections):
    incoming = np.zeros(4)
    outgoing = np.zeros(4)
    max_angle = 0.
    determinant_trace = 0.
    wraps = []
    for index, (current, after) in enumerate(zip(reflections, np.roll(reflections, -1, axis=0))):
        relative = after @ current.conj().T
        triangular, basis = schur(relative, output='complex')
        angles = np.angle(np.diag(triangular))
        max_angle = max(max_angle, max(abs(angles)))
        hermitian = (basis*angles) @ basis.conj().T
        outgoing += np.diag(hermitian).real/(2*np.pi)
        incoming += np.diag(current.conj().T @ hermitian @ current).real/(2*np.pi)
        determinant_angle = np.angle(np.linalg.det(relative))
        determinant_trace += determinant_angle/(2*np.pi)
        wrap = int(np.rint((sum(angles)-determinant_angle)/(2*np.pi)))
        if wrap:
            wraps.append(dict(interval=index, additional_matrix_wraps=wrap,
                              sum_eigenangles=float(sum(angles)), determinant_angle=float(determinant_angle)))
    np.testing.assert_allclose(sum(incoming), sum(outgoing), atol=1e-11)
    return dict(samples=len(reflections), trace_winding=float(sum(outgoing)),
                determinant_polygon_winding=float(determinant_trace), matrix_minus_determinant_wraps=wraps,
                maximum_relative_eigenangle=float(max_angle),
                input_D_conjugate_trace=float(sum(incoming[:3])), input_Hu_trace=float(incoming[3]),
                output_L_conjugate_trace=float(sum(outgoing[:3])), output_Hd_conjugate_trace=float(outgoing[3]),
                formal_input_minus_output_rotor_root_coefficient=float(sum(incoming[:3])))


def calculate(counts, phase_count):
    model, light, charges = physical_model()
    results = []
    for count in counts:
        data, widths, exterior = shooting.local_operators(count, 1e-6, model)
        pencil = shooting.transfer_pencil(data, widths)
        matrices = []
        gaps = []
        unitarity_errors = []
        for angle in np.linspace(0., 2*np.pi, phase_count, endpoint=False):
            gap, reflection, error = shooting.match(data, widths, exterior, np.exp(1j*angle),
                                                    light, pencil)
            gaps.append(gap)
            matrices.append(unitary(reflection))
            unitarity_errors.append(error)
        matrices = np.array(matrices)
        charge_traces = [projected_winding(matrices[::stride]) for stride in (1, 2, 4)]
        assert abs(charge_traces[0]['trace_winding']-3) < 1e-8
        assert charge_traces[0]['maximum_relative_eigenangle'] < 2.
        rotor_angle = .37
        rotated = matrices[0] @ np.diag(np.exp(1j*rotor_angle*np.array(charges['rotor_steps'])))
        np.testing.assert_allclose(np.linalg.det(rotated)/np.linalg.det(matrices[0]),
                                   np.exp(3j*rotor_angle), atol=1e-12)
        rotor_steps = np.array(charges['rotor_steps'])
        for q_in, q_out, root in zip(np.array(charges['incoming_weights']).T,
                                     np.array(charges['outgoing_weights']).T, charges['rotor_root']):
            np.testing.assert_allclose(
                matrices*q_out[None, :, None]+matrices*(root*rotor_steps),
                matrices*q_in, atol=1e-12)
        result = dict(radial_cells=2*count, phase_count=phase_count,
                      minimum_matching_sigma_min=float(min(gaps)),
                      maximum_reflection_unitarity_error=float(max(unitarity_errors)),
                      maximum_Hu_to_antiL_probability=float(np.max(np.sum(abs(matrices[:, :3, 3])**2, axis=1))),
                      maximum_antiD_to_Hd_probability_sum=float(np.max(np.sum(abs(matrices[:, 3, :3])**2, axis=1))),
                      winding_by_phase_resolution=charge_traces)
        print(result, flush=True)
        result['reflection_matrices_real'] = matrices.real.tolist()
        result['reflection_matrices_imaginary'] = matrices.imag.tolist()
        results.append(result)
    return dict(status='PASS', scope='fixed-core zero-energy reflection and conditional rotor dressing',
                exact_charge_ledger=charges, meshes=results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--counts', type=int, nargs='+', default=[60, 120])
    parser.add_argument('--phase-count', type=int, default=48)
    parser.add_argument('--output', type=Path, default=OUT)
    args = parser.parse_args()
    if min(args.counts) < 8 or args.phase_count < 48 or args.phase_count % 4:
        parser.error('invalid radial or phase grid')
    args.output.write_text(json.dumps(calculate(args.counts, args.phase_count), indent=2)+'\n',
                           encoding='utf-8')
