#!/usr/bin/env python3
"""Pass 10947: execute five post-Pass10944 computational/hardware fronts.

The packet lowers the cubic controlled-X into the seven-qutrit VM, constructs
exact Golay logical input states plus an accepted-fault factory model, computes
the residual symmetry of the 36+18 quotient projector, synthesizes a sparse
four-mode router, and determines the precise projective compatibility between
the order-108 coloring action and the signed E6 cubic.

The [[11,1,5]]_3 code and 66-location logical core are prior repo results in
analysis/w33_dark_strange_golay11_ft_lane.py, analysis/PASS10943_RESERVATION.md,
analysis/PASS10944_RESERVATION.md, and
analysis/2026-09-23_execute_all5_hybrid_lie_golay_calibration.md.  This pass's
increment is the explicit encoded-state factory contract, extended 552-location
ledger, and malignant-triple enumeration.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "analysis") not in sys.path:
    sys.path.insert(0, str(ROOT / "analysis"))

from bt2767_m36_factory import controls_to_ray, ray_controls
from w33_pass10941_qutrit_universal_instruction_bridge import (
    MODES, compose, cz, eye, fourier, inv,
)
from w33_pass10944_five_front_computational_closure import load_signed_cubic

OUT = ROOT / "data/w33_pass10947_five_front_execution.json"
P = 3


def front1_cubic_vm_microcode() -> dict:
    """Lower the Pass10944 primitive onto four of the seven VM modes."""
    control, copy, fixed, target = 0, 1, 2, 3

    # SUM(c->t): x_t += x_c, z_c -= z_t in the Pass10941 symplectic ABI.
    sum_matrix = eye()
    sum_matrix[copy, control] = 1
    sum_matrix[MODES + control, MODES + copy] = -1
    sum_matrix %= P
    sum_macro = [
        (f"F{copy}", fourier(copy)),
        (f"CZ{control},{copy}", cz(control, copy)),
        (f"F{copy}^-1", inv(fourier(copy))),
    ]
    unsum_macro = [
        (f"F{copy}^-1", inv(fourier(copy))),
        (f"CZ{control},{copy}", cz(control, copy)),
        (f"F{copy}", fourier(copy)),
    ]
    assert np.array_equal(compose(sum_macro), sum_matrix)
    assert np.array_equal(compose(unsum_macro), inv(sum_matrix))

    triads = load_signed_cubic()
    chosen_triad, sign = min(triads.items())
    tick_direction = (-pow(sign, -1, P)) % P
    tick_coefficient = tick_direction * sign % P
    assert tick_coefficient == 2

    rows = []
    for x, t in itertools.product(range(3), repeat=2):
        registers = [0] * 7
        registers[control] = x
        registers[target] = t
        # Clean fixed rail |0> -> |1> and copy rail |0> -> |x>.
        registers[fixed] = (registers[fixed] + 1) % P
        registers[copy] = (registers[copy] + registers[control]) % P
        registers[target] = (registers[target] + 1) % P
        registers[target] = (
            registers[target]
            + tick_coefficient * registers[control]
            * registers[copy] * registers[fixed]
        ) % P
        registers[copy] = (registers[copy] - registers[control]) % P
        registers[fixed] = (registers[fixed] - 1) % P
        expected = (t + (1 if x == 0 else 0)) % P
        assert registers[target] == expected
        assert registers[copy] == registers[fixed] == 0
        rows.append({"control": x, "target_in": t, "target_out": expected})

    primitive_program = [
        "HX_TRANSLATE(2,+1)",
        "F(1)", "CZ(0,1)", "F(1)^-1",
        "HX_TRANSLATE(3,+1)",
        f"E6_CUBIC_LOCAL_TICK(triad={list(chosen_triad)},direction={tick_direction}; modes=0,1,2 -> 3)",
        "F(1)^-1", "CZ(0,1)", "F(1)",
        "HX_TRANSLATE(2,-1)",
    ]
    depth_layers = [
        ["HX_TRANSLATE(2,+1)", "HX_TRANSLATE(3,+1)", "F(1)"],
        ["CZ(0,1)"],
        ["F(1)^-1"],
        ["E6_CUBIC_LOCAL_TICK(0,1,2->3)"],
        ["HX_TRANSLATE(2,-1)", "F(1)^-1"],
        ["CZ(0,1)"],
        ["F(1)"],
    ]
    return {
        "opcode": "C0X_VM(control=0,target=3,copy=1,fixed=2)",
        "logical_modes_used": [0, 1, 2, 3],
        "unused_modes": [4, 5, 6],
        "chosen_E6_triad": list(chosen_triad),
        "chosen_triad_sign_mod3": sign,
        "sign_corrected_tick_direction": tick_direction,
        "program": primitive_program,
        "primitive_counts": {
            "Heisenberg_X_translations": 3,
            "local_F_or_inverse": 4,
            "CZ": 2,
            "E6_cubic_tick": 1,
            "total": len(primitive_program),
        },
        "parallel_depth": len(depth_layers),
        "depth_layers": depth_layers,
        "clean_ancillas": 2,
        "ancillas_returned_to_zero": True,
        "VM_P7_pair_edges_used": [[0, 1]],
        "VM_bridge_generator_used": False,
        "truth_table": rows,
        "all_nine_logical_cases_pass": True,
        "boundary": (
            "This is exact seven-qutrit logical microcode conditional on one native "
            "signed E6 cubic-tick port. It does not synthesize the microscopic "
            "four-body Hamiltonian or assign a pulse duration."
        ),
    }


GOLAY_CHECKS = np.array([
    [-1, 1, 1, -1, -1, 0, 1, 0, 0, 0, 0],
    [-1, 1, -1, 1, 0, -1, 0, 1, 0, 0, 0],
    [-1, -1, 1, 0, 1, -1, 0, 0, 1, 0, 0],
    [-1, -1, 0, 1, -1, 1, 0, 0, 0, 1, 0],
    [-1, 0, -1, -1, 1, 1, 0, 0, 0, 0, 1],
], dtype=int) % 3


def ternary_span(generator: np.ndarray) -> set[tuple[int, ...]]:
    return {
        tuple(int(x) for x in (np.array(c, dtype=int) @ generator) % 3)
        for c in itertools.product(range(3), repeat=generator.shape[0])
    }


def front2_verified_golay_factories() -> dict:
    code = ternary_span(GOLAY_CHECKS)
    dual = {
        word for word in itertools.product(range(3), repeat=11)
        if all(sum(x*y for x, y in zip(word, row)) % 3 == 0
               for row in GOLAY_CHECKS)
    }
    assert (len(code), len(dual)) == (3**5, 3**6)
    logical = (1,) * 11
    assert logical in dual and logical not in code
    cosets = []
    for a in range(3):
        coset = {tuple((x + a) % 3 for x in word) for word in code}
        assert len(coset) == 243
        cosets.append(coset)
    assert not (cosets[0] & cosets[1] or cosets[0] & cosets[2] or cosets[1] & cosets[2])
    assert set().union(*cosets) == dual

    stabilizer_checks = 0
    for row in GOLAY_CHECKS:
        g = tuple(map(int, row))
        for coset in cosets:
            for word in coset:
                assert tuple((x+y) % 3 for x, y in zip(word, g)) in coset
                assert sum(x*y for x, y in zip(word, g)) % 3 == 0
                stabilizer_checks += 2
    assert stabilizer_checks == 5 * 3 * 243 * 2

    column_weights = np.count_nonzero(GOLAY_CHECKS, axis=0).astype(int).tolist()
    assert column_weights == [5, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1]

    locations = []
    # A verified cat gadget is used for each weight-six stabilizer so every
    # data coupling is coordinate-local. Two complete syndrome rounds are
    # compared and the block is accepted only on zero agreement.
    for block in ("ZERO_L", "PLUS_L", "R_L"):
        for coordinate in range(11):
            locations.append((block, "CANDIDATE_PREP", coordinate, None))
        for round_id in (1, 2):
            for basis in ("X", "Z"):
                for check, row in enumerate(GOLAY_CHECKS):
                    for coordinate in np.flatnonzero(row):
                        hazard = int(coordinate) if round_id == 2 else None
                        locations.append((block, f"{basis}_R{round_id}_COUPLE_C{check}",
                                          int(coordinate), hazard))
                for check in range(5):
                    locations.append((block, f"{basis}_R{round_id}_READOUT", check, None))
        for coordinate in range(11):
            locations.append((block, "ACCEPTED_HANDOFF", coordinate, coordinate))
    factory_locations = len(locations)
    assert factory_locations == 3 * 162 == 486

    core_banks = (
        "X_SYNDROME_SUM", "Z_SYNDROME_SUM", "R_INJECTION_CX2",
        "X_ANCILLA_MEASURE", "Z_ANCILLA_MEASURE", "INJECTION_DATA_MEASURE",
    )
    for bank in core_banks:
        for coordinate in range(11):
            locations.append(("CORE", bank, coordinate, coordinate))
    assert len(locations) == 552

    hazards = [(i, row[3]) for i, row in enumerate(locations) if row[3] is not None]
    assert len(hazards) == 279
    malicious = 0
    coordinate_profile = Counter()
    for a, b, c in itertools.combinations(hazards, 3):
        coords = (a[1], b[1], c[1])
        if len(set(coords)) == 3:
            malicious += 1
            coordinate_profile[tuple(sorted(coords))] += 1
    assert malicious == 2_576_205
    assert len(coordinate_profile) == math.comb(11, 3)
    total_triples = math.comb(len(locations), 3)
    hazard_triples = math.comb(len(hazards), 3)

    def upper_bound(p: float) -> float:
        exactly_three_malignant = malicious * p**3 * (1-p)**(len(locations)-3)
        at_least_four = 1 - sum(
            math.comb(len(locations), j) * p**j * (1-p)**(len(locations)-j)
            for j in range(4)
        )
        return exactly_three_malignant + at_least_four

    lo, hi = 1e-12, 0.01
    for _ in range(100):
        mid = (lo + hi) / 2
        if upper_bound(mid) < mid:
            lo = mid
        else:
            hi = mid
    conservative_pseudothreshold = (lo + hi) / 2
    assert abs(conservative_pseudothreshold - 0.000531703523611593) < 1e-15

    samples = [
        {"physical_location_error": p, "accepted_extended_gadget_failure_upper_bound": upper_bound(p)}
        for p in (1e-5, 1e-4, 1e-3)
    ]
    return {
        "encoded_states": {
            "code": "[[11,1,5]]_3 CSS from C=G11^perp",
            "C_size": len(code),
            "C_perp_size": len(dual),
            "logical_coset_sizes": [len(x) for x in cosets],
            "ZERO_L": "uniform support on C",
            "PLUS_L": "uniform support on C_perp=C union (C+1) union (C+2)",
            "R_L": "coset amplitudes proportional to (1,1,-1)",
            "X_and_Z_stabilizer_checks": stabilizer_checks,
            "all_checks_pass": True,
        },
        "factory": {
            "blocks": ["ZERO_L", "PLUS_L", "R_L"],
            "protocol": (
                "candidate encoding; two complete X/Z syndrome rounds using verified "
                "weight-six cat gadgets with coordinate-local data coupling; accept only "
                "two agreeing zero syndromes; then one coordinate-local handoff"
            ),
            "candidate_prep_locations_per_block": 11,
            "data_couplings_per_syndrome_round_per_block": 60,
            "readouts_per_syndrome_round_per_block": 10,
            "syndrome_rounds": 2,
            "handoff_locations_per_block": 11,
            "locations_per_block": 162,
            "three_factory_locations": factory_locations,
            "core_locations": 66,
            "extended_locations": len(locations),
            "accepted_late_hazard_locations": len(hazards),
        },
        "malignant_triples": {
            "all_location_triples": total_triples,
            "candidate_late_hazard_triples_enumerated": hazard_triples,
            "malignant_distinct_coordinate_triples": malicious,
            "coordinate_triples_covered": len(coordinate_profile),
            "leading_failure_coefficient": malicious,
            "conservative_bound_crosses_physical_p_at": conservative_pseudothreshold,
            "exact_uniform_independent_bound": (
                "M*p^3*(1-p)^(552-3) + Pr[Binomial(552,p)>=4], M=2576205"
            ),
            "samples": samples,
            "replaces_symbolic_q": True,
        },
        "fault_model": (
            "Adversarial qutrit-Pauli support with independent uniform location-fault "
            "probability p. Verified-cat gadgets enforce one-data-coordinate propagation. "
            "A prep/round-one fault needs later syndrome corruption to be accepted, so three "
            "total faults can then occupy at most two output coordinates. Only round-two "
            "couplings, handoffs, and the 66 core locations are order-three hazards."
        ),
        "boundary": (
            "This closes the previously symbolic q inside the declared coordinate-local, "
            "postselected verified-cat model. It is not a device threshold: correlated "
            "faults, leakage, cat-gadget construction errors outside the stated contract, "
            "and acceptance-rate optimization require a hardware noise model."
        ),
        "literature_context": "Prakash 2020, arXiv:2003.02717, owns the ternary-Golay Strange distillation map.",
        "repo_prior_art": [
            "analysis/w33_dark_strange_golay11_ft_lane.py",
            "analysis/2026-09-23_execute_all5_hybrid_lie_golay_calibration.md",
            "analysis/PASS10943_RESERVATION.md",
            "analysis/PASS10944_RESERVATION.md",
        ],
    }


def front3_quotient_centralizer() -> dict:
    parent = json.loads((ROOT / "data/w33_pass10945_choi_fourier_three_channel_weld.json").read_text())
    assert parent["three_phase_quotient"]["identity"] == "54 = 18 + 18 + 18"
    assert parent["three_phase_quotient"]["pair_quotient_dimensions"] == {"01": 36, "02": 36, "12": 36}

    per_channel = {"linear_character_each": 1, "V_omega": 0, "V_omega2": 3}
    all_channels = {"linear_character_each": 3, "V_omega": 0, "V_omega2": 9}
    end_h27_dimension = 9 * 3**2 + 9**2
    end_h27_c3_dimension = 27 * 1**2 + 3 * 3**2
    assert end_h27_dimension == 162
    assert end_h27_c3_dimension == 54

    bridge = json.loads((ROOT / "data/w33_e6id_current_h27_gauge_bridge.json").read_text())
    addresses = [tuple(map(int, bridge["maps"]["e6id_to_current_H27_address"][str(i)])) for i in range(27)]
    address_id = {h: i for i, h in enumerate(addresses)}

    def hmul(g, h):
        a, b, c = g
        A, B, C = h
        return ((a+A) % 3, (b+B) % 3, (c+C-b*A) % 3)

    carriers = set()
    centralizer = set()
    for h in addresses:
        hp = tuple(address_id[hmul(h, x)] for x in addresses)
        for phase_perm in itertools.permutations(range(3)):
            perm = tuple(3*hp[eid] + phase_perm[p] for eid in range(27) for p in range(3))
            carriers.add(perm)
            if set(phase_perm[p] for p in (0, 1)) == {0, 1} and phase_perm[2] == 2:
                centralizer.add(perm)
    assert len(carriers) == 27 * 6 == 162
    assert len(centralizer) == 27 * 2 == 54

    return {
        "quotient": "Q=(ambient 81)/S1 = Q0 direct_sum Q1 direct_sum Q2",
        "channel_dimensions": [18, 18, 18],
        "per_channel_H27_multiplicities": per_channel,
        "full_quotient_H27_multiplicities": all_channels,
        "linear_commutants_over_Qomega": {
            "End_H27_Q_dimension": end_h27_dimension,
            "End_H27xC3_Q_dimension": end_h27_c3_dimension,
            "End_H27_structure": "product over nine linear characters of M3, times M9 on V_omega2 multiplicity",
            "End_H27xC3_structure": "27 scalar blocks plus three M3 multiplicity blocks",
        },
        "discrete_carrier_group": {
            "group": "H27 x S3_phase",
            "order": len(carriers),
            "action": "diagonal H27 address translation and permutation of the three 18D clock channels",
        },
        "parabolic_36_plus_18_projector": {
            "P_channels": [0, 1],
            "Q_channel": 2,
            "centralizer_inside_discrete_carrier": "H27 x S2",
            "centralizer_order": len(centralizer),
            "S2_role": "swap the two positive channels while fixing the opposite channel",
        },
        "theorem": (
            "The 36+18 split is a projector choice inside the canonical 18+18+18 "
            "quotient. Its largest permutation symmetry inherited from the H27-by-channel "
            "carrier is H27 x S2 of order 54. The full H27 commutant has dimension 162, "
            "while retaining the external C3 clock action cuts it to dimension 54."
        ),
        "no_go_compatibility": (
            "None of these residual commutants changes the H27 irreducible multiplicities. "
            "The Pass10944 rank-36 ceiling for an equivariant map from two regular H27 "
            "modules therefore remains unchanged."
        ),
    }


def swap_matrix(i: int, j: int) -> np.ndarray:
    out = np.eye(4, dtype=int)
    out[[i, j]] = out[[j, i]]
    return out


def front4_m36_router() -> dict:
    family_names = {0: "A", 1: "B", 2: "C", 3: "D"}
    rows = []
    checks = 0
    for family in range(4):
        dark = family
        U = np.eye(4, dtype=int) if dark == 3 else swap_matrix(dark, 3)
        W = U[:3, :].astype(complex)
        projector = np.eye(4)
        projector[dark, dark] = 0
        assert np.allclose(W @ W.conjugate().T, np.eye(3))
        assert np.allclose(W.conjugate().T @ W, projector)
        for ray in (r for r in ray_controls() if r["family"] == family):
            state = controls_to_ray(ray)
            assert abs(state[dark]) < 4e-11
            assert abs(np.vdot(W @ state, W @ state).real - 1) < 4e-11
            checks += 1
        rows.append({
            "family": family,
            "family_name": family_names[family],
            "dark_input": dark,
            "dump_output": 3,
            "active_crossbar_pair": None if dark == 3 else [dark, 3],
            "MZI_mixing_angle": 0.0 if dark == 3 else math.pi/2,
            "local_phase_trim": "cancel the i phases of the swap-state MZI",
            "transfer_U4": U.tolist(),
            "logical_W3x4": U[:3, :].tolist(),
        })
    assert checks == 36

    star_counts = [1, 1, 1, 0]
    adjacent_counts = [3, 2, 1, 0]
    assert max(star_counts) < max(adjacent_counts)
    target = 0.99
    factor = target**(1/3)
    phase_total = math.acos(math.sqrt(factor))
    loss_total = 20 * math.acosh(1/math.sqrt(factor)) / math.log(10)

    def limits(max_active):
        return {
            "per_active_switch_process_fidelity_at_least": factor**(1/max_active),
            "per_active_switch_phase_radians_at_most": phase_total/max_active,
            "per_active_switch_differential_loss_dB_at_most": loss_total/max_active,
            "per_active_switch_leakage_probability_at_most": 1e-3/max_active,
            "per_active_switch_extinction_dB_at_least": -10*math.log10(1e-3/max_active),
        }

    return {
        "architecture": "four-mode star crossbar with mode 3 as the dump bus",
        "installed_pair_switches": [[0, 3], [1, 3], [2, 3]],
        "family_program_table": rows,
        "all_36_M36_rays_checked": checks,
        "optimization": {
            "objective": "lexicographically minimize worst active switches, then mean active switches, at fixed three installed switches",
            "star_active_counts_by_dark_mode": star_counts,
            "adjacent_chain_active_counts_by_dark_mode": adjacent_counts,
            "star_worst": max(star_counts),
            "adjacent_worst": max(adjacent_counts),
            "star_mean": sum(star_counts)/4,
            "adjacent_mean": sum(adjacent_counts)/4,
            "winner": "star crossbar",
            "optimality_witness": (
                "a nontrivial family must change which input reaches the fixed dump, so "
                "at least one active switch is necessary; the star attains one"
            ),
        },
        "per_switch_targets": {
            "star_crossbar": limits(1),
            "three_stage_adjacent_baseline": limits(3),
            "target_conditional_fidelity": target,
            "separate_total_dark_leakage": 1e-3,
        },
        "pump_and_tomography": {
            "Strange_pump_coherence_settling_gamma_t_at_least": 2*math.log(100),
            "router_falsifier": (
                "tomographically reconstruct all four 4x4 transfers; reject if the selected "
                "input does not reach the dump, if any bright input leaks above 1e-3 into "
                "the dump, or if the conditional 3x4 process misses the stated budget"
            ),
            "wrong_family_falsifier": (
                "program every incorrect family on every M36 ray and verify that its known "
                "dark input is no longer routed to the dump; failure to distinguish the "
                "four settings falsifies selector calibration"
            ),
        },
        "literature_context": (
            "Clements et al., Optica 3 (2016) 1460, DOI 10.1364/OPTICA.3.001460, "
            "supplies the standard programmable multiport context; the sparse star optimum "
            "here follows from the four committed deletion maps."
        ),
        "boundary": (
            "These are exact ideal transfer matrices and sufficient component targets. "
            "They are not fabricated-device measurements and do not include off-state "
            "thermal crosstalk or wavelength dependence."
        ),
    }


H27 = tuple(itertools.product(range(3), repeat=3))
F3_2 = tuple(itertools.product(range(3), repeat=2))


def hmul(g, h):
    a, b, c = g
    A, B, C = h
    return ((a+A) % 3, (b+B) % 3, (c+C-b*A) % 3)


def hinv(g):
    return next(h for h in H27 if hmul(g, h) == (0, 0, 0) and hmul(h, g) == (0, 0, 0))


def gl2_elements():
    out = []
    for a, b, c, d in itertools.product(range(3), repeat=4):
        determinant = (a*d-b*c) % 3
        if determinant:
            out.append(((a, b, c, d), determinant))
    assert len(out) == 48
    return out


def act2(matrix, u):
    a, b, c, d = matrix
    return ((a*u[0]+b*u[1]) % 3, (c*u[0]+d*u[1]) % 3)


def cocycle(u, v):
    return (-u[1]*v[0]) % 3


def solve_linear_mod(matrix, modulus):
    work = [list(map(lambda x: int(x) % modulus, row)) for row in matrix]
    variables = len(work[0]) - 1
    rank = 0
    pivots = []
    for column in range(variables):
        pivot = next((i for i in range(rank, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        z = pow(work[rank][column], -1, modulus)
        work[rank] = [(z*x) % modulus for x in work[rank]]
        for i in range(len(work)):
            if i != rank and work[i][column]:
                z = work[i][column]
                work[i] = [(x-z*y) % modulus for x, y in zip(work[i], work[rank])]
        pivots.append(column)
        rank += 1
    assert not any(not any(row[:-1]) and row[-1] for row in work)
    solution = [0] * variables
    for row, pivot in zip(work[:rank], pivots):
        solution[pivot] = row[-1]
    return rank, variables-rank, solution


def q_particular(matrix, determinant):
    variables = [u for u in F3_2 if u != (0, 0)]
    index = {u: i for i, u in enumerate(variables)}
    equations = []
    for u in F3_2:
        for v in F3_2:
            w = ((u[0]+v[0]) % 3, (u[1]+v[1]) % 3)
            row = [0] * len(variables)
            for x, coefficient in ((u, 1), (v, 1), (w, -1)):
                if x != (0, 0):
                    row[index[x]] = (row[index[x]] + coefficient) % 3
            rhs = (determinant*cocycle(u, v)
                   - cocycle(act2(matrix, u), act2(matrix, v))) % 3
            equations.append(row + [rhs])
    rank, nullity, solution = solve_linear_mod(equations, 3)
    assert (rank, nullity) == (6, 2)
    return {(0, 0): 0, **{u: solution[index[u]] for u in variables}}


def front5_coloring_cubic_compatibility() -> dict:
    bridge = json.loads((ROOT / "data/w33_e6id_current_h27_gauge_bridge.json").read_text())
    e6_to_h = {
        int(i): tuple(map(int, h))
        for i, h in bridge["maps"]["e6id_to_current_H27_address"].items()
    }
    h_to_e6 = {h: i for i, h in e6_to_h.items()}
    signed = load_signed_cubic()
    triads = tuple(sorted(signed))
    address_triads = {
        tuple(sorted(e6_to_h[i] for i in triad)) for triad in triads
    }

    def unique_line_lift(matrix, determinant):
        q0 = q_particular(matrix, determinant)
        candidates = []
        for alpha, beta in itertools.product(range(3), repeat=2):
            q = {u: (q0[u] + alpha*u[0] + beta*u[1]) % 3 for u in F3_2}

            def automorphism(x):
                u = x[:2]
                return (*act2(matrix, u), (determinant*x[2] + q[u]) % 3)

            mapped = {
                tuple(sorted(automorphism(x) for x in triad))
                for triad in address_triads
            }
            if mapped == address_triads:
                candidates.append(q)
        assert len(candidates) == 1
        return candidates[0]

    def normalize(u):
        x, y = u
        z = pow(x if x else y, -1, 3)
        return ((z*x) % 3, (z*y) % 3)

    calibration_direction = (1, 2)
    linear_stabilizer = []
    for matrix, determinant in gl2_elements():
        if normalize(act2(matrix, calibration_direction)) == calibration_direction:
            linear_stabilizer.append((matrix, determinant, unique_line_lift(matrix, determinant)))
    assert len(linear_stabilizer) == 12

    def support_permutation(h, matrix, determinant, q):
        out = []
        for i in range(27):
            x = e6_to_h[i]
            u = x[:2]
            transformed = (*act2(matrix, u), (determinant*x[2]+q[u]) % 3)
            out.append(h_to_e6[hmul(h, transformed)])
        return tuple(out)

    # The 45x27 unsigned incidence matrix has binary rank 21. For each support
    # automorphism, the inhomogeneous sign equation has the same rank and a
    # six-dimensional affine solution set.
    sign_rows = []
    for triad in triads:
        row = [0] * 27
        for i in triad:
            row[i] = 1
        sign_rows.append(row)

    supports = {}
    quotient_keys = Counter()
    sign_rank_hist = Counter()
    representative_hashes = []
    for h in H27:
        for matrix, determinant, q in linear_stabilizer:
            perm = support_permutation(h, matrix, determinant, q)
            assert perm not in supports
            equations = []
            for triad, row in zip(triads, sign_rows):
                image = tuple(sorted(perm[i] for i in triad))
                assert image in signed
                rhs = 0 if signed[image] == signed[triad] else 1
                equations.append(row + [rhs])
            rank, nullity, solution = solve_linear_mod(equations, 2)
            assert (rank, nullity) == (21, 6)
            sign_rank_hist[(rank, nullity)] += 1
            supports[perm] = solution
            quotient_keys[(h[0], h[1], matrix)] += 1
            if len(representative_hashes) < 12:
                digest = hashlib.sha256(
                    json.dumps({"perm": perm, "sign": solution}, separators=(",", ":")).encode()
                ).hexdigest()
                representative_hashes.append(digest)
    assert len(supports) == 324
    assert len(quotient_keys) == 108 and set(quotient_keys.values()) == {3}
    assert sign_rank_hist == Counter({(21, 6): 324})

    support_set = set(supports)
    for left in support_set:
        for right in support_set:
            composed = tuple(left[right[i]] for i in range(27))
            assert composed in support_set

    # The affine F3^2 translation quotient has no subgroup section in H27:
    # every lift of its two basis translations has the same nontrivial central
    # commutator, irrespective of the two central gauge choices.
    commutators = set()
    for za, zb in itertools.product(range(3), repeat=2):
        a = (1, 0, za)
        b = (0, 1, zb)
        comm = hmul(hmul(hmul(a, b), hinv(a)), hinv(b))
        commutators.add(comm)
    assert len(commutators) == 1
    commutator = next(iter(commutators))
    assert commutator in ((0, 0, 1), (0, 0, 2))

    return {
        "coloring_group": {
            "affine_group": "F3^2 : B, where B fixes projective family D",
            "B_order": len(linear_stabilizer),
            "order": len(quotient_keys),
        },
        "cubic_support_lift": {
            "group": "H27 : B",
            "order": len(supports),
            "central_kernel": "Z(H27)=C3",
            "three_support_lifts_per_coloring_operation": True,
            "quotient_order": len(quotient_keys),
        },
        "signed_cubic_lift": {
            "binary_sign_equation_rank": 21,
            "homogeneous_sign_gauge_dimension": 6,
            "diagonal_sign_lifts_per_support_permutation": 2**6,
            "all_324_support_permutations_lift": True,
            "full_monomial_signed_lift_order": len(supports) * 2**6,
            "sample_lift_sha256": representative_hashes,
        },
        "non_split_firewall": {
            "basis_translation_lift_pairs_checked": 9,
            "common_commutator": list(commutator),
            "order108_strict_section_exists": False,
            "reason": (
                "the two affine translation generators commute in F3^2, but every pair "
                "of H27 lifts has the same nonidentity central commutator"
            ),
        },
        "theorem": (
            "The order-108 M36 coloring stabilizer is compatible with the signed E6 "
            "cubic only projectively. Its exact cubic-support lift is the order-324 "
            "central extension H27:B; every support element has 64 diagonal sign repairs, "
            "forming a 20,736-element monomial signed-cubic lift. The central C3 extension "
            "does not split, so no strict order-108 subgroup acts on the 27 signed cubic "
            "coordinates with the requested affine translation law."
        ),
        "VM_consequence": (
            "A selector relabeling must carry a tracked central qutrit phase and one of "
            "the certified diagonal sign gauges. Treating the 108 coloring operations "
            "as literal unsigned cubic permutations would drop required phase data."
        ),
    }


def main() -> None:
    output = {
        "schema": "w33.pass10947.five_front_execution.v1",
        "status": "PASS_CUBIC_VM_GOLAY_FACTORY_QUOTIENT_CENTRALIZER_ROUTER_AND_PROJECTIVE_COMPATIBILITY",
        "front1_cubic_VM_microcode": front1_cubic_vm_microcode(),
        "front2_verified_Golay_factories": front2_verified_golay_factories(),
        "front3_quotient_centralizer": front3_quotient_centralizer(),
        "front4_M36_physical_router": front4_m36_router(),
        "front5_coloring_cubic_compatibility": front5_coloring_cubic_compatibility(),
        "global_boundary": (
            "The packet proves finite logical, coding, representation, transfer-matrix, "
            "and group-extension statements inside explicit models. It does not claim a "
            "microscopic cubic interaction, a measured fault threshold, or fabricated photonics."
        ),
    }
    OUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": output["status"],
        "VM_depth": output["front1_cubic_VM_microcode"]["parallel_depth"],
        "malignant_triples": output["front2_verified_Golay_factories"]["malignant_triples"]["malignant_distinct_coordinate_triples"],
        "quotient_projector_centralizer": output["front3_quotient_centralizer"]["parabolic_36_plus_18_projector"]["centralizer_order"],
        "router_worst_switches": output["front4_M36_physical_router"]["optimization"]["star_worst"],
        "signed_cubic_lift_order": output["front5_coloring_cubic_compatibility"]["signed_cubic_lift"]["full_monomial_signed_lift_order"],
    }, indent=2))


if __name__ == "__main__":
    main()
