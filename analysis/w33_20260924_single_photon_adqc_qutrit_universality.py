#!/usr/bin/env python3
"""Exact qutrit ancilla-driven universality audit for the Photonic Holonet.

A flying photonic qutrit is treated as a programmable ancilla/head, not as an
exponentially large data register.  Stationary qutrits hold scalable quantum
state.  One fixed ancilla-register interaction plus adaptive ancilla
measurements compiles local gates and an entangling gate.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260924_single_photon_adqc_qutrit_universality.json"
D = 3
TOL = 2e-12
def phase_align_distance(a: np.ndarray, b: np.ndarray) -> float:
    z = np.vdot(b.reshape(-1), a.reshape(-1))
    phase = z / abs(z) if abs(z) else 1.0
    return float(np.linalg.norm(a - phase * b))


def embed_two_body(u: np.ndarray, dims: list[int], targets: tuple[int, int]) -> np.ndarray:
    total = math.prod(dims)
    out = np.zeros((total, total), dtype=complex)
    t0, t1 = targets
    for col in range(total):
        inp = list(np.unravel_index(col, dims))
        local_in = inp[t0] * dims[t1] + inp[t1]
        for local_out in range(dims[t0] * dims[t1]):
            amp = u[local_out, local_in]
            if abs(amp) <= 1e-15:
                continue
            nxt = inp.copy()
            nxt[t0], nxt[t1] = divmod(local_out, dims[t1])
            row = np.ravel_multi_index(tuple(nxt), dims)
            out[row, col] += amp
    return out
def build_operators():
    omega = np.exp(2j * np.pi / D)
    F = np.array([[omega ** (j * k) for k in range(D)] for j in range(D)]) / np.sqrt(D)
    X = np.zeros((D, D), dtype=complex)
    for j in range(D):
        X[(j + 1) % D, j] = 1
    Z = np.diag([omega**j for j in range(D)])
    CZ = np.diag([omega ** (a * r) for a in range(D) for r in range(D)])
    E = np.kron(F.conj().T, F) @ CZ
    plus = F[:, 0]
    return omega, F, X, Z, CZ, E, plus


def single_register_kraus(F, X, E, plus, phases):
    r = np.exp(1j * np.asarray(phases, dtype=float))
    R = np.diag(r)
    tensor = E.reshape(D, D, D, D)
    rows = []
    basis = []
    for m in range(D):
        b = np.array(
            [np.exp(-2j * np.pi * m * j / D) * np.conj(r[j]) for j in range(D)]
        ) / np.sqrt(D)
        basis.append(b)
        K = np.einsum("a,aobr,b->or", np.conj(b), tensor, plus)
        target = np.linalg.matrix_power(X, -m) @ F @ R / np.sqrt(D)
        rows.append((m, K, target))
    return np.column_stack(basis), rows
def two_register_kraus(F, X, CZ, E, plus):
    e01 = embed_two_body(E, [D, D, D], (0, 1))
    e02 = embed_two_body(E, [D, D, D], (0, 2))
    U = e02 @ e01
    tensor = U.reshape(D, D * D, D, D * D)
    Uent = np.kron(F, F) @ CZ
    rows = []
    for m in range(D):
        K = np.einsum("oai,a->oi", tensor[m], plus)
        target = np.kron(np.linalg.matrix_power(X, m), np.eye(D)) @ Uent / np.sqrt(D)
        rows.append((m, K, target))
    return Uent, rows


def pauli_projective_distance(U, X, Z):
    best = float("inf")
    best_label = None
    for a in range(D):
        for b in range(D):
            P = np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b)
            dist = phase_align_distance(U, P)
            if dist < best:
                best, best_label = dist, (a, b)
    return best, best_label


def single_qutrit_stabilizer_states(X, Z):
    states = [np.eye(D, dtype=complex)[:, j] for j in range(D)]
    for a in range(D):
        vals, vecs = np.linalg.eig(X @ np.linalg.matrix_power(Z, a))
        for j in range(D):
            states.append(vecs[:, j] / np.linalg.norm(vecs[:, j]))
    assert len(states) == D * (D + 1) == 12
    return states


def build_certificate():
    omega, F, X, Z, CZ, E, plus = build_operators()
    I = np.eye(D)
    I2 = np.eye(D * D)
    checks = {}
    for name, U in {"F": F, "X": X, "Z": Z, "CZ": CZ, "E": E}.items():
        eye = np.eye(U.shape[0])
        checks[f"{name}_unitary_error"] = float(np.linalg.norm(U.conj().T @ U - eye))
        assert checks[f"{name}_unitary_error"] < TOL
    checks["F4_error"] = float(np.linalg.norm(np.linalg.matrix_power(F, 4) - I))
    assert checks["F4_error"] < TOL

    # Generic measurement-program compiler: every diagonal R(theta) is induced
    # by choosing a 3-outcome unbiased analyzer basis on the ancilla.
    rng = np.random.default_rng(10942)
    phase_trials = [[0.0, 0.0, 0.0]]
    phase_trials += [list(rng.uniform(-np.pi, np.pi, D)) for _ in range(16)]
    local_rows = []
    for phases in phase_trials:
        basis, rows = single_register_kraus(F, X, E, plus, phases)
        basis_error = float(np.linalg.norm(basis.conj().T @ basis - I))
        branch_errors = [float(np.linalg.norm(K - target)) for _, K, target in rows]
        prob_errors = [float(np.linalg.norm(K.conj().T @ K - I / D)) for _, K, _ in rows]
        assert basis_error < TOL and max(branch_errors + prob_errors) < TOL
        local_rows.append({
            "phases_rad": phases,
            "basis_unitarity_error": basis_error,
            "max_gate_error": max(branch_errors),
            "max_probability_operator_error": max(prob_errors),
        })
    # The same fixed interaction, used sequentially on two memories, gives an
    # entangler with only a known Pauli byproduct.
    Uent, ent_rows = two_register_kraus(F, X, CZ, E, plus)
    ent_gate_errors = [float(np.linalg.norm(K - target)) for _, K, target in ent_rows]
    ent_prob_errors = [float(np.linalg.norm(K.conj().T @ K - I2 / D)) for _, K, _ in ent_rows]
    assert max(ent_gate_errors + ent_prob_errors) < TOL
    cz_recovery_error = float(np.linalg.norm(np.kron(F.conj().T, F.conj().T) @ Uent - CZ))
    assert cz_recovery_error < TOL

    # Standard qutrit T: zeta is a primitive ninth root.  It is not Clifford
    # because conjugating X does not return a Pauli (even projectively).
    zeta = np.exp(2j * np.pi / 9)
    Tgate = np.diag([1.0, zeta, zeta**8])
    tx = Tgate @ X @ Tgate.conj().T
    nonclifford_distance, nearest_pauli = pauli_projective_distance(tx, X, Z)
    assert nonclifford_distance > 1e-6
    t_phases = [0.0, 2 * np.pi / 9, 16 * np.pi / 9]
    t_basis, t_rows = single_register_kraus(F, X, E, plus, t_phases)
    t_errors = [float(np.linalg.norm(K - target)) for _, K, target in t_rows]
    assert max(t_errors) < TOL
    stabilizers = single_qutrit_stabilizer_states(X, Z)
    t_analyzer_max_stabilizer_fidelity = max(
        abs(np.vdot(s, t_basis[:, m])) ** 2 for s in stabilizers for m in range(D)
    )
    assert t_analyzer_max_stabilizer_fidelity < 1 - 1e-9

    # Pure one-particle mode encoding has an unavoidable dimension cost.
    mode_scaling = []
    for n in range(1, 13):
        modes = D**n
        mode_scaling.append({
            "logical_qutrits": n,
            "minimum_orthogonal_single_particle_modes": modes,
            "log2_modes": math.log2(modes),
        })
    assert mode_scaling[-1]["minimum_orthogonal_single_particle_modes"] == 531441

    certificate = {
        "schema": "w33.20260924.single_photon_adqc_qutrit_universality.v1",
        "status": "PASS_FIXED_INTERACTION_ADAPTIVE_MEASUREMENT_QUTRIT_UNIVERSALITY",
        "architecture": {
            "carrier": "one flying photonic qutrit ancilla active per interaction cycle",
            "memory": "scalable stationary qutrit register; not encoded solely in photon mode count",
            "fixed_interaction": "E_AR=(F_A^dagger tensor F_R) CZ_AR",
            "ancilla_preparation": "|+_0>=F|0>",
            "programming_surface": "three-outcome ancilla analyzer basis plus classical Pauli frame",
            "destructive_measurement_boundary": (
                "A detected photon is consumed; 'single photon' means one flying ancilla at a time "
                "unless a nondestructive measurement/reset interface is separately supplied."
            ),
        },
        "local_gate_theorem": {
            "measurement_basis_ket": (
                "|b_m(theta)>=1/sqrt(3) sum_j omega^(-m j) exp(-i theta_j)|j>"
            ),
            "branch_map": "K_m=(1/sqrt(3)) X^(-m) F R(theta)",
            "branch_probability": "1/3 for every input state and every m",
            "phase_trials": local_rows,
        },
        "two_memory_entangler": {
            "protocol": "ancilla interacts with R1 then R2 through the same E_AR; measure ancilla in computational basis",
            "branch_map": "K_m=(1/sqrt(3))(X^m tensor I)(F tensor F)CZ",
            "branch_probability": "1/3 for every input state and every m",
            "max_gate_error": max(ent_gate_errors),
            "max_probability_operator_error": max(ent_prob_errors),
            "recover_CZ_with_local_F_dagger_error": cz_recovery_error,
        },
        "non_clifford_gate": {
            "T": "diag(1,zeta,zeta^8), zeta=exp(2*pi*i/9)",
            "measurement_phases_rad": t_phases,
            "implemented_branch": "X^(-m) F T / sqrt(3)",
            "max_branch_error": max(t_errors),
            "T_X_Tdag_nearest_pauli_projective_distance": nonclifford_distance,
            "nearest_pauli_label_X_power_Z_power": list(nearest_pauli),
            "analyzer_max_single_qutrit_stabilizer_fidelity": t_analyzer_max_stabilizer_fidelity,
            "analyzer_resource_statement": (
                "Each T-program analyzer vector is non-stabilizer; the non-Clifford "
                "resource has been relocated from a memory-state injection to measurement."
            ),
            "conclusion": "T is outside the qutrit Clifford group and is available through analyzer programming",
        },
        "universal_gate_compiler": {
            "local_F": "theta=(0,0,0), with tracked X byproduct",
            "local_T": "apply measured F*T then F^dagger=F^3 using the same primitive",
            "entangling_CZ": "apply measured (F tensor F)CZ then local F^dagger on both memories",
            "gate_set": "qutrit Clifford+T with an entangling CZ",
            "universality_type": "approximate universal quantum computation on the stationary qutrit register",
            "resource_relocation": (
                "No online magic-state preparation/injection is required by this gate identity. "
                "The non-Clifford physical resource is instead the programmed ancilla measurement basis."
            ),
            "fault_tolerance_boundary": (
                "This does not make non-Clifford fault tolerance free: a protected implementation "
                "must still realize the non-Clifford analyzer basis below threshold."
            ),
        },
        "single_particle_scaling_no_go": {
            "fact": "n independent qutrits have Hilbert dimension 3^n",
            "implication": "a lone particle carrying them only as orthogonal mode labels needs at least 3^n modes",
            "table": mode_scaling,
            "architectural_decision": "use the photon as a mobile head/bus, not as the scalable quantum memory",
        },
        "holonet_reinterpretation": {
            "exact_existing_assets": [
                "81-state qutrit Pauli frame for feed-forward",
                "36 spreads furnishing complete stabilizer measurement frames",
                "finite qutrit Clifford transport and routing machinery",
                "remote qutrit SUM / entanglement-assisted network primitives",
            ],
            "new_mapping_hypothesis": {
                "W33_points": "candidate stationary memory-node/address layer",
                "W33_edges": "candidate flying-photon routing/interactions",
                "spread_frames": "candidate analyzer calibration/program frames",
                "72_tick_microframe": "candidate interact-measure-frame-update transaction",
            },
            "boundary": "The mapping is an architecture proposal; only the gate identities above are proved here.",
        },
        "checks": checks,
        "literature": [
            "Proctor et al., Phys. Rev. A 95, 052317 (2017), ancilla-driven qudit computation",
            "Glaudell et al., arXiv:2202.09235, qutrit Clifford+T approximate universality",
            "Cohen & Molmer, Phys. Rev. A 98, 030302(R) (2018), single-photon network bus",
            "Romanova & Dur, Quantum Sci. Technol. 11 015054 (2026), qudit stabilizer MBQC",
        ],
        "boundary": (
            "Exact finite-dimensional circuit theorem and scaling audit, not a hardware demonstration. "
            "The memory-photon qutrit interaction, loss, detector/analyzer fidelity, and fault-tolerant "
            "measurement implementation require separate physical certificates."
        ),
    }
    return certificate
def main():
    out = build_certificate()
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "local_trials": len(out["local_gate_theorem"]["phase_trials"]),
        "entangler_error": out["two_memory_entangler"]["max_gate_error"],
        "T_nonclifford_distance": out["non_clifford_gate"]["T_X_Tdag_nearest_pauli_projective_distance"],
        "single_particle_modes_for_12_qutrits": out["single_particle_scaling_no_go"]["table"][-1]["minimum_orthogonal_single_particle_modes"],
    }, indent=2))


if __name__ == "__main__":
    main()
