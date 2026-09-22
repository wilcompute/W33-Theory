"""Executable qutrit stabilizer extraction and bare-ancilla hook census.

The [[9,1,3]]_3 carrier, stabilizers, decoder, and six-handle assignment are
owned by ``w33_harmonic_qutrit_redundancy.py``. This file adds an explicit
ten-qutrit state interpreter for the serialized SUM/CZ/Fourier circuits and a
complete ancilla-X suffix-fault audit. It does not claim a fault-tolerant cat
preparation or a circuit-level threshold.
"""

from itertools import product
import json
from pathlib import Path

import numpy as np

from w33_harmonic_qutrit_redundancy import pairing, rank, stabilizers


W = np.exp(2j * np.pi / 3)
DATA_QUTRITS = 9


def encoded_state(alpha=None):
    """Return an arbitrary or basis logical state as a sparse data state."""
    if alpha is None:
        alpha = np.array([1, 2j, -1 + 1j], dtype=complex)
    alpha = np.asarray(alpha, dtype=complex)
    alpha = alpha / np.linalg.norm(alpha)
    return {
        tuple([a] * 3 + [b] * 3 + [c] * 3):
        sum(alpha[j] * W ** (j * (a + b + c)) for j in range(3)) / np.sqrt(27)
        for a, b, c in product(range(3), repeat=3)
    }


def apply_pauli(state, x, z):
    """Apply P(x,z)=X^x Z^z to a sparse nine-qutrit state."""
    out = {}
    for word, amplitude in state.items():
        target = tuple((value + int(dx)) % 3 for value, dx in zip(word, x))
        phase = W ** (sum(value * int(dz) for value, dz in zip(word, z)) % 3)
        out[target] = out.get(target, 0j) + amplitude * phase
    return out


def circuit(stabilizer):
    """Serialize controlled-P(stabilizer), inverse Fourier, measure, reset."""
    operations = [{"gate": "PREPARE_PLUS", "ancilla": 0}]
    for site in range(DATA_QUTRITS):
        if stabilizer[site]:
            operations.append({
                "gate": "SUM", "control": "ancilla0", "target": site,
                "power": int(stabilizer[site]),
            })
        if stabilizer[DATA_QUTRITS + site]:
            operations.append({
                "gate": "CZ", "control": "ancilla0", "target": site,
                "power": int(stabilizer[DATA_QUTRITS + site]),
            })
    operations.extend([
        {"gate": "FOURIER_INVERSE", "target": "ancilla0"},
        {"gate": "MEASURE_Z", "target": "ancilla0"},
        {"gate": "RESET", "target": "ancilla0"},
    ])
    return operations


def interpret_circuit(data_state, operations):
    """Execute the serialized circuit on one ancilla plus nine data qutrits."""
    joint = None
    measured = None
    for operation in operations:
        gate = operation["gate"]
        if gate == "PREPARE_PLUS":
            assert joint is None
            joint = {
                (ancilla,) + word: amplitude / np.sqrt(3)
                for ancilla in range(3)
                for word, amplitude in data_state.items()
            }
        elif gate == "SUM":
            assert joint is not None and operation["control"] == "ancilla0"
            target = int(operation["target"]) + 1
            power = int(operation["power"]) % 3
            updated = {}
            for word, amplitude in joint.items():
                result = list(word)
                result[target] = (result[target] + power * result[0]) % 3
                result = tuple(result)
                updated[result] = updated.get(result, 0j) + amplitude
            joint = updated
        elif gate == "CZ":
            assert joint is not None and operation["control"] == "ancilla0"
            target = int(operation["target"]) + 1
            power = int(operation["power"]) % 3
            joint = {
                word: amplitude * W ** (power * word[0] * word[target] % 3)
                for word, amplitude in joint.items()
            }
        elif gate == "FOURIER_INVERSE":
            assert joint is not None and operation["target"] == "ancilla0"
            updated = {}
            for word, amplitude in joint.items():
                for outcome in range(3):
                    result = (outcome,) + word[1:]
                    value = amplitude * W ** (-outcome * word[0]) / np.sqrt(3)
                    updated[result] = updated.get(result, 0j) + value
            joint = updated
        elif gate == "MEASURE_Z":
            assert joint is not None and operation["target"] == "ancilla0"
            measured = [dict() for _ in range(3)]
            for word, amplitude in joint.items():
                data_word = word[1:]
                branch = measured[word[0]]
                branch[data_word] = branch.get(data_word, 0j) + amplitude
        elif gate == "RESET":
            assert measured is not None and operation["target"] == "ancilla0"
        else:
            raise ValueError(f"unsupported gate {gate}")
    assert measured is not None
    probabilities = [
        float(sum(abs(value) ** 2 for value in branch.values()))
        for branch in measured
    ]
    return probabilities, measured


def state_fidelity(left, right):
    overlap = sum(
        np.conjugate(left.get(word, 0j)) * value for word, value in right.items()
    )
    norm_left = sum(abs(value) ** 2 for value in left.values())
    norm_right = sum(abs(value) ** 2 for value in right.values())
    return float(abs(overlap) ** 2 / (norm_left * norm_right))


def propagated_ancilla_x_error(operations, completed_couplings, power):
    """Propagate X_a^power inserted after a coupling boundary to the data."""
    couplings = [
        operation for operation in operations
        if operation["gate"] in ("SUM", "CZ")
    ]
    if not 0 <= completed_couplings <= len(couplings):
        raise ValueError("coupling boundary out of range")
    error = np.zeros(2 * DATA_QUTRITS, dtype=int)
    for operation in couplings[completed_couplings:]:
        site = int(operation["target"])
        exponent = power * int(operation["power"]) % 3
        if operation["gate"] == "SUM":
            error[site] = (error[site] + exponent) % 3
        else:
            error[DATA_QUTRITS + site] = (
                error[DATA_QUTRITS + site] + exponent
            ) % 3
    return error


def audit():
    checks = stabilizers()
    serialized = [circuit(stabilizer) for stabilizer in checks]
    state = encoded_state()
    assert abs(sum(abs(value) ** 2 for value in state.values()) - 1) < 1e-12

    errors = [np.zeros(2 * DATA_QUTRITS, dtype=int)]
    for site in range(DATA_QUTRITS):
        for x_power, z_power in product(range(3), repeat=2):
            if not (x_power or z_power):
                continue
            error = np.zeros(2 * DATA_QUTRITS, dtype=int)
            error[site] = x_power
            error[DATA_QUTRITS + site] = z_power
            errors.append(error)

    worst_probability_error = 0.0
    decoder = {}
    for error in errors:
        errored_state = apply_pauli(
            state, error[:DATA_QUTRITS], error[DATA_QUTRITS:]
        )
        outcomes = []
        for stabilizer, operations in zip(checks, serialized):
            probabilities, _ = interpret_circuit(errored_state, operations)
            expected = (-pairing(stabilizer, error)) % 3
            worst_probability_error = max(
                worst_probability_error,
                abs(probabilities[expected] - 1),
                *(probabilities[outcome] for outcome in range(3) if outcome != expected),
            )
            outcomes.append(expected)
        decoder.setdefault(tuple(outcomes), error)
    assert worst_probability_error < 1e-12

    for error in errors:
        syndrome = tuple(
            (-pairing(stabilizer, error)) % 3 for stabilizer in checks
        )
        residual = (error - decoder[syndrome]) % 3
        assert rank(np.vstack([checks, residual])) == 8

    x0 = np.zeros(18, dtype=int)
    x0[0] = 1
    z0 = np.zeros(18, dtype=int)
    z0[9] = 1
    explicit_sign_checks = {
        "Z0_Z1inv_against_X0": int((-pairing(checks[0], x0)) % 3),
        "weight6_X_against_Z0": int((-pairing(checks[6], z0)) % 3),
    }
    assert explicit_sign_checks == {
        "Z0_Z1inv_against_X0": 1,
        "weight6_X_against_Z0": 2,
    }

    postmeasurement_checks = 0
    maximum_postmeasurement_infidelity = 0.0
    for logical in range(3):
        alpha = np.zeros(3, dtype=complex)
        alpha[logical] = 1
        logical_state = encoded_state(alpha)
        for operations in serialized:
            probabilities, branches = interpret_circuit(logical_state, operations)
            assert abs(probabilities[0] - 1) < 1e-12
            fidelity = state_fidelity(logical_state, branches[0])
            maximum_postmeasurement_infidelity = max(
                maximum_postmeasurement_infidelity, abs(1 - fidelity)
            )
            postmeasurement_checks += 1
    assert maximum_postmeasurement_infidelity < 1e-12

    fault_cases = []
    malignant = []
    undetected_logical = []
    for stabilizer_index, operations in enumerate(serialized):
        coupling_count = sum(
            operation["gate"] in ("SUM", "CZ") for operation in operations
        )
        for completed in range(coupling_count + 1):
            for fault_power in (1, 2):
                error = propagated_ancilla_x_error(
                    operations, completed, fault_power
                )
                syndrome = tuple(
                    (-pairing(stabilizer, error)) % 3 for stabilizer in checks
                )
                representative = decoder.get(syndrome)
                decoder_defined = representative is not None
                logical_after_decoder = False
                if decoder_defined:
                    residual = (error - representative) % 3
                    logical_after_decoder = (
                        rank(np.vstack([checks, residual])) == 9
                    )
                record = {
                    "stabilizer": stabilizer_index,
                    "weight": coupling_count,
                    "completed_couplings": completed,
                    "fault_power": fault_power,
                    "data_error_XZ": error.tolist(),
                    "syndrome": list(syndrome),
                    "decoder_defined": decoder_defined,
                    "logical_after_single_error_decoder": logical_after_decoder,
                }
                fault_cases.append(record)
                if logical_after_decoder:
                    malignant.append(record)
                    if not any(syndrome):
                        undetected_logical.append(record)

    assert len(fault_cases) == 64
    assert len(malignant) == 12
    assert len(undetected_logical) == 4
    assert {
        (row["stabilizer"], row["completed_couplings"])
        for row in malignant
    } == {(6, 2), (6, 3), (6, 4), (7, 2), (7, 3), (7, 4)}
    assert {
        (row["stabilizer"], row["completed_couplings"])
        for row in undetected_logical
    } == {(6, 3), (7, 3)}

    conditional_cat_cases = 0
    for stabilizer in checks:
        support = [
            site for site in range(DATA_QUTRITS)
            if stabilizer[site] or stabilizer[DATA_QUTRITS + site]
        ]
        for site in support:
            for fault_power in (1, 2):
                error = np.zeros(2 * DATA_QUTRITS, dtype=int)
                error[site] = fault_power * stabilizer[site] % 3
                error[DATA_QUTRITS + site] = (
                    fault_power * stabilizer[DATA_QUTRITS + site] % 3
                )
                assert sum(
                    bool(error[j] or error[DATA_QUTRITS + j])
                    for j in range(DATA_QUTRITS)
                ) == 1
                syndrome = tuple(
                    (-pairing(row, error)) % 3 for row in checks
                )
                residual = (error - decoder[syndrome]) % 3
                assert rank(np.vstack([checks, residual])) == 8
                conditional_cat_cases += 1
    assert conditional_cat_cases == 48

    return {
        "status": "PASS",
        "circuits": serialized,
        "measurement_checks": len(errors) * len(checks),
        "max_probability_error": worst_probability_error,
        "logical_basis_postmeasurement_checks": postmeasurement_checks,
        "maximum_postmeasurement_infidelity": maximum_postmeasurement_infidelity,
        "outcome_convention": (
            "measured m = -symplectic_pairing(stabilizer,error) mod3"
        ),
        "explicit_sign_checks": explicit_sign_checks,
        "decoder": [
            {
                "outcomes": list(key),
                "correction_XZ": ((-value) % 3).tolist(),
            }
            for key, value in decoder.items()
        ],
        "two_qutrit_gates_per_block_round": sum(
            operation["gate"] in ("SUM", "CZ")
            for operations in serialized for operation in operations
        ),
        "six_handle_gates_per_round": 144,
        "bare_ancilla_x_fault_cases": len(fault_cases),
        "bare_ancilla_x_malignant_cases": malignant,
        "bare_ancilla_x_undetected_logical_cases": undetected_logical,
        "conditional_cat_single_site_cases": conditional_cat_cases,
        "conditional_cat_scheme": (
            "Assume an independently prepared and verified qutrit cat with one ancilla per "
            "support site; each ancilla controls one data Pauli factor, Fourier-basis outcomes "
            "are summed mod 3, and each postverification ancilla shift reaches one data site."
        ),
        "scope": (
            "The serialized ideal extraction circuits are executed exactly and the complete "
            "single ancilla-X suffix census is stored. The bare circuit is not fault tolerant. "
            "The cat statement is conditional: no cat preparation/verification circuit, ancilla-Z "
            "measurement-fault decoder, hardware noise model, repeated rounds, or threshold is claimed."
        ),
        "prior": [
            "w33_harmonic_qutrit_redundancy.py",
            "https://arxiv.org/abs/1807.01863",
            "https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/Efficient-Quantum-Circuits-for-Non-Qubit-Quantum-Error-Correcting-Codes.pdf",
            "https://arxiv.org/abs/2108.02184",
        ],
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    arguments = parser.parse_args()
    result = audit()
    if arguments.write:
        Path(__file__).with_suffix(".json").write_text(
            json.dumps(result, indent=2) + "\n"
        )
    print({
        key: result[key]
        for key in (
            "status", "measurement_checks", "max_probability_error",
            "bare_ancilla_x_fault_cases", "conditional_cat_single_site_cases",
        )
    })
