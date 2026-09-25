#!/usr/bin/env python3
"""Pass 10941 addendum: lower the seven-qutrit VM to Clifford+T.

The bare h7/Z compiler is a Clifford machine.  This producer connects every
one of its 25 symplectic transvections to the fixed-interaction photonic ADQC
primitives already certified on master, then freezes two equivalent ideal
non-Clifford ports: a programmed T analyzer and Pass 411 Choi injection.

The point of the certificate is also negative: the analyzer vectors are a
Pauli orbit of the conjugate qutrit T magic state.  Measurement programming
therefore relocates the cyclotomic resource; it does not make magic free.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass10941_qutrit_universal_instruction_bridge.json"
P = 3
MODES = 7
N = 2 * MODES


def load_data(name: str) -> dict:
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def eye() -> np.ndarray:
    return np.eye(N, dtype=np.int64)


def mm(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return (a @ b) % P


def fourier(mode: int) -> np.ndarray:
    """Symplectic action F: (x,z) -> (-z,x)."""
    out = eye()
    out[mode, mode] = 0
    out[mode, MODES + mode] = -1
    out[MODES + mode, mode] = 1
    out[MODES + mode, MODES + mode] = 0
    return out % P


def phase(mode: int) -> np.ndarray:
    """P=diag(1,1,omega): (x,z) -> (x,z+x)."""
    out = eye()
    out[MODES + mode, mode] = 1
    return out % P


def cz(left: int, right: int) -> np.ndarray:
    """CZ: z_left += x_right and z_right += x_left."""
    out = eye()
    out[MODES + left, right] = 1
    out[MODES + right, left] = 1
    return out % P


def inv(a: np.ndarray) -> np.ndarray:
    # All primitives used here have order 3 or 4; brute force keeps the
    # certificate independent of floating-point linear algebra.
    out = eye()
    for _ in range(1, 13):
        out = mm(a, out)
        if np.array_equal(mm(out, a), eye()):
            return out
    raise AssertionError("primitive inverse not found")


def symplectic_form() -> np.ndarray:
    j = np.zeros((N, N), dtype=np.int64)
    for i in range(MODES):
        j[i, MODES + i] = 1
        j[MODES + i, i] = -1
    return j % P


def transvection(direction: list[int]) -> np.ndarray:
    v = np.asarray(direction, dtype=np.int64).reshape(N, 1) % P
    return (eye() + v @ (v.T @ symplectic_form())) % P


def compose(operations: list[tuple[str, np.ndarray]]) -> np.ndarray:
    out = eye()
    for _label, matrix in operations:
        out = mm(matrix, out)
    return out


def lower_direction(direction: list[int]) -> list[tuple[str, np.ndarray]]:
    e_support = [i for i, x in enumerate(direction[:MODES]) if x % P]
    f_support = [i for i, x in enumerate(direction[MODES:]) if x % P]
    assert not (e_support and f_support)
    support = e_support or f_support
    assert len(support) in (1, 2)

    # T_f=P^-1.  For two modes,
    # T_(f_i+f_j)=P_i^-1 P_j^-1 CZ_ij^-1.
    f_core: list[tuple[str, np.ndarray]] = [
        (f"P{mode}^-1", inv(phase(mode))) for mode in support
    ]
    if len(support) == 2:
        f_core.append((f"CZ{support[0]},{support[1]}^-1", inv(cz(*support))))
    if f_support:
        return f_core

    # F f=-e, and T_v=T_-v, so conjugating the f circuit by local F
    # gives the requested e-direction transvection exactly.
    pre = [(f"F{mode}^-1", inv(fourier(mode))) for mode in support]
    post = [(f"F{mode}", fourier(mode)) for mode in support]
    return pre + f_core + post


def analyzer_phase_exponents() -> dict:
    # Exponents are modulo 9 in the zeta_9 basis.  Pass 411 uses
    # |M_T>=T|+> with exponents (0,1,-1).  The ADQC measurement vectors are
    # |b_m>=Z^-m |M_T^*>, hence e_j=-t_j-3mj (mod 9).
    magic = [0, 1, 8]
    conjugate = [(-x) % 9 for x in magic]
    rows = []
    for m in range(3):
        exponents = [(conjugate[j] - 3 * m * j) % 9 for j in range(3)]
        rows.append({
            "outcome": m,
            "zeta9_exponents": exponents,
            "exact_identity": f"|b_{m}>=Z^-{m}|M_T^*>",
        })

    zeta = np.exp(2j * np.pi / 9)
    basis = np.column_stack([
        np.asarray([zeta**e for e in row["zeta9_exponents"]]) / np.sqrt(3)
        for row in rows
    ])
    error = float(np.linalg.norm(basis.conj().T @ basis - np.eye(3)))
    assert error < 2e-12
    return {
        "pass411_magic_zeta9_exponents": magic,
        "conjugate_magic_zeta9_exponents": conjugate,
        "analyzer_vectors": rows,
        "basis_unitarity_error": error,
    }


def compile_feedforward(entries: list[dict], mode: int = 0) -> list[dict]:
    rows = []
    for entry in entries:
        word = entry["correction_word"]
        micro_ops = []
        for letter in (() if word == "I" else word):
            if letter == "X":
                micro_ops.append(f"HX_TRANSLATE({mode},+1)")
            elif letter == "Z":
                micro_ops.append(f"HZ_TRANSLATE({mode},+1)")
            elif letter == "P":
                # VM T_f=P^-1 has order three, so P=T_f^2.
                micro_ops += [f"T_f{mode}", f"T_f{mode}"]
            else:
                raise AssertionError(f"unknown Pass 411 opcode {letter}")
        rows.append({
            "bell_outcome": entry["bell_outcome"],
            "clifford_word": word,
            "vm_micro_ops": micro_ops,
            "vm_micro_op_count": len(micro_ops),
        })
    return rows


def main() -> None:
    vm = load_data("w33_pass10941_symplectic_vm_gate_compiler.json")
    adqc = load_data("w33_20260924_single_photon_adqc_qutrit_universality.json")
    magic = load_data("w33_pass411_qutrit_magic_injection.json")
    feedforward = load_data("w33_pass411_clifford_feedforward.json")
    distillation = load_data("w33_pass416_qutrit_distillation_search.json")
    strange = load_data("w33_hesse36_dark_schrodinger_strange_state.json")

    p3 = next(row for row in vm["prime_packets"] if row["prime"] == 3)
    lowerings = []
    for name, direction in zip(p3["gate_names"], p3["gate_directions"]):
        operations = lower_direction(direction)
        got = compose(operations)
        want = transvection(direction)
        assert np.array_equal(got, want), name
        lowerings.append({
            "vm_gate": name,
            "clifford_macro": [label for label, _matrix in operations],
            "macro_length": len(operations),
            "exact_mod3_matrix_match": True,
        })
    assert len(lowerings) == 25

    phase_bridge = analyzer_phase_exponents()
    assert magic["magic_state"]["maximum_single_qutrit_stabilizer_fidelity"] < 1
    analyzer_fidelity = adqc["non_clifford_gate"]["analyzer_max_single_qutrit_stabilizer_fidelity"]
    assert abs(analyzer_fidelity - magic["magic_state"]["maximum_single_qutrit_stabilizer_fidelity"]) < 2e-12

    ff = compile_feedforward(feedforward["entries"])
    assert len(ff) == 9
    assert max(row["vm_micro_op_count"] for row in ff) == 5
    assert magic["gate_teleportation"]["deterministic_after_feedforward"] is True

    pure_return = distillation["result"]["pure_input_best_return_fidelity"]
    assert pure_return < 1
    assert strange["strange_bridge"]["same_projective_Clifford_orbit"] is True

    out = {
        "schema": "w33.pass10941.qutrit_universal_instruction_bridge.v1",
        "status": "PASS_SEVEN_QUTRIT_CLIFFORD_T_ABI_WITH_RESOURCE_CONSERVATION",
        "seven_qutrit_clifford_lowering": {
            "source_vm_status": vm["status"],
            "connected_lie_closure_dimension": p3["connected_Lie_closure_dimension"],
            "target": "Sp(14,3) plus seven-mode Heisenberg translations",
            "adqc_primitive_alphabet": ["F_i", "P_i", "CZ_ij"],
            "primitive_realization": {
                "F_i": "ADQC LOCAL(theta=(0,0,0)); track X byproduct",
                "P_i": "ADQC LOCAL(R=P) followed by F_i^-1",
                "CZ_ij": "ADQC TWO_NODE(i,j) followed by F_i^-1 tensor F_j^-1",
                "inverses": "finite-order Clifford powers",
            },
            "all_25_vm_generators_lowered_exactly_mod3": True,
            "maximum_clifford_macro_length": max(row["macro_length"] for row in lowerings),
            "lowerings": lowerings,
        },
        "nonclifford_resource_equivalence": {
            "gate": "T=diag(1,zeta9,zeta9^-1)",
            "programmed_analyzer": phase_bridge,
            "maximum_stabilizer_fidelity": analyzer_fidelity,
            "identity": "the three T-analyzer kets are the Z orbit of |M_T^*>",
            "consequence": (
                "Analyzer programming and T-magic injection are two interfaces to the same "
                "basis-dependent mu9 resource; the non-Clifford resource is relocated, not erased."
            ),
            "rank_one_stabilizer_firewall": (
                "No rank-one stabilizer output is used. The resource is independently certified "
                "non-stabilizer by maximum stabilizer fidelity 0.712386014201 < 1."
            ),
        },
        "universal_instruction": {
            "opcode": "T_ANALYZER(mode)",
            "ideal_branch": "X_mode^-m F_mode T_mode / sqrt(3), m in F3",
            "branch_probability": "1/3 independent of input",
            "determinization": "track X^-m then apply compiled F^-1",
            "portability": "the opcode may target any of the seven modes",
            "entangling_support": "the lowered bridge plus local generators closes Sp(14,3)",
            "gate_set": "seven-qutrit Clifford+T",
            "universality": "approximate universal quantum computation in the ideal resource model",
            "literature_basis": (
                "Glaudell-Ross-van de Wetering-Yeh: qutrit Clifford+T is approximately universal"
            ),
        },
        "alternative_choi_injection": {
            "opcode": "T_INJECT_CHOIPAIR(mode)",
            "resource": magic["gate_teleportation"]["resource"],
            "bell_outcomes": 9,
            "outcome_probability": "1/9",
            "all_feedforward_compiles_to_vm": True,
            "maximum_vm_feedforward_micro_ops": max(row["vm_micro_op_count"] for row in ff),
            "feedforward": ff,
        },
        "claim_lattice": {
            "bare_pass10941_vm_is_universal": False,
            "ideal_nonstabilizer_analyzer_or_choi_port_closes_logical_universality": True,
            "endogenous_fault_tolerant_magic_factory_is_proved": False,
            "physical_fixed_photon_memory_interaction_is_demonstrated": False,
            "fault_tolerance_threshold_is_proved": False,
        },
        "distillation_and_source_boundary": {
            "pass416_direct_five_qutrit_T_orbit_return_fidelity": pure_return,
            "pass416_direct_five_qutrit_T_orbit_distills": False,
            "pass411_five_qutrit_bound_role": (
                "distance-three combinatorial upper bound only; not a selected-code nonlinear map"
            ),
            "dark_strange_ray": strange["strange_bridge"]["exact_identity"],
            "dark_strange_boundary": (
                "exact Clifford orbit witness, but no dynamical preparation, conversion to T, "
                "or protected injection route"
            ),
            "remaining_physical_frontier": (
                "realize the fixed qutrit photon-memory interaction and a protected non-stabilizer "
                "analyzer or magic factory below a measured logical threshold"
            ),
        },
        "parents": [
            "data/w33_pass10941_symplectic_vm_gate_compiler.json",
            "data/w33_20260924_single_photon_adqc_qutrit_universality.json",
            "data/w33_20260924_bell_shell_clifford_cyclotomic_lift.json",
            "data/w33_pass411_qutrit_magic_injection.json",
            "data/w33_pass416_qutrit_distillation_search.json",
            "data/w33_hesse36_dark_schrodinger_strange_state.json",
        ],
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "lowered_vm_generators": len(lowerings),
        "maximum_clifford_macro_length": out["seven_qutrit_clifford_lowering"]["maximum_clifford_macro_length"],
        "analyzer_magic_identity": out["nonclifford_resource_equivalence"]["identity"],
        "maximum_feedforward_micro_ops": out["alternative_choi_injection"]["maximum_vm_feedforward_micro_ops"],
    }, indent=2))


if __name__ == "__main__":
    main()
