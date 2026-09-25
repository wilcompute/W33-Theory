#!/usr/bin/env python3
"""Pass 10952: complete-positivity firewall for the order-eight clock.

Pass 10951 identifies a determinant-odd order-eight clock element g in GL(2,3).
Pass 5730 already proves the general dictionary det=+1 -> unitary Clifford and
det=-1 -> antiunitary extended Clifford.  This pass applies that dictionary
objectwise to the new clock, then tests the induced density-operator maps.

Odd powers are unitary-conjugated transposition: positive and trace preserving
but not completely positive.  Even powers are unitary Clifford channels.
A doubled qutrit/conjugate-qutrit carrier linearizes the odd tick unitarily.
"""
from __future__ import annotations

import json
import math
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass10951_clock_pin_spin_central_sign_bridge as p51

OUT = ROOT / "data/w33_pass10952_clock_complete_positivity_firewall.json"
TOL = 1e-8
omega = np.exp(2j * np.pi / 3)
X = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
ZQ = np.diag([1, omega, omega * omega])
F = np.array(
    [[omega ** (j * k) for k in range(3)] for j in range(3)],
    dtype=complex,
) / math.sqrt(3)
P = np.diag([1, 1, omega])

I2 = p51.I
J = ((1, 0), (0, 2))
MF = ((0, 2), (1, 0))
MP = ((1, 0), (1, 1))


def phase_residual(a, b):
    nz = np.argwhere(np.abs(b) > 1e-10)
    i, j = map(int, nz[0])
    phase = a[i, j] / b[i, j]
    return phase, float(np.linalg.norm(a - phase * b))


def weyl(a, b):
    return np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(ZQ, b)
def check_unitary_action(u, m):
    residuals = []
    for col, op in ((0, X), (1, ZQ)):
        target = weyl(m[0][col], m[1][col])
        image = u @ op @ u.conj().T
        residuals.append(phase_residual(image, target)[1])
    return max(residuals)


def build_sl23_representatives():
    reps = {I2: np.eye(3, dtype=complex)}
    todo = deque([I2])
    generators = ((MF, F), (MP, P))
    while todo:
        m = todo.popleft()
        u = reps[m]
        for n, v in generators:
            mn = p51.mm(m, n)
            uv = u @ v
            if mn not in reps:
                reps[mn] = uv
                todo.append(mn)
    assert len(reps) == 24
    err = max(check_unitary_action(u, m) for m, u in reps.items())
    assert err < TOL
    return reps, err
def unitary_channel(u):
    return lambda a: u @ a @ u.conj().T


def transpose_conjugated_map(u):
    return lambda a: u @ a.T @ u.conj().T


def choi_matrix(fn):
    c = np.zeros((9, 9), dtype=complex)
    for i in range(3):
        for j in range(3):
            e = np.zeros((3, 3), dtype=complex)
            e[i, j] = 1
            c += np.kron(e, fn(e))
    assert np.linalg.norm(c - c.conj().T) < TOL
    return (c + c.conj().T) / 2


def choi_inertia(c):
    vals = np.linalg.eigvalsh(c)
    pos = int(np.sum(vals > TOL))
    neg = int(np.sum(vals < -TOL))
    zero = len(vals) - pos - neg
    return [pos, neg, zero], vals


def partial_trace_output(c):
    return np.einsum("iaja->ij", c.reshape(3, 3, 3, 3))
def mat_power(m, n):
    out = I2
    for _ in range(n):
        out = p51.mm(out, m)
    return out


def antiunitary_phase_action(u, m):
    residuals = []
    for col, op in ((0, X), (1, ZQ)):
        target = weyl(m[0][col], m[1][col])
        image = u @ op.conj() @ u.conj().T
        residuals.append(phase_residual(image, target)[1])
    return max(residuals)


def projective_order(u, max_order=32):
    eye = np.eye(u.shape[0], dtype=complex)
    for n in range(1, max_order + 1):
        phase, err = phase_residual(np.linalg.matrix_power(u, n), eye)
        if err < TOL:
            return n, phase
    raise AssertionError("projective order not found")


def round_eigs(vals):
    return [float(np.round(x.real, 12)) for x in vals]
def main():
    p51_data = json.loads(
        (ROOT / "data/w33_pass10951_clock_pin_spin_central_sign_bridge.json")
        .read_text(encoding="utf-8")
    )
    g = tuple(tuple(x for x in row)
              for row in p51_data["clock_power_ladder"]["g"])
    assert p51.order(g) == 8
    assert p51.p46.det2(g) == 2

    reps, rep_error = build_sl23_representatives()
    s = p51.mm(g, J)
    assert p51.p46.det2(s) == 1
    u = reps[s]

    anti_error = antiunitary_phase_action(u, g)
    assert anti_error < TOL

    # A = U K.  Its even square is the ordinary unitary V=U U*.
    v = u @ u.conj()
    assert abs(np.linalg.det(v)) > 1e-8
    even_order, even_phase = projective_order(v)
    assert even_order == 4

    # The doubled linear lift on H + conjugate(H).
    zero = np.zeros((3, 3), dtype=complex)
    doubled = np.block([[zero, u], [u.conj(), zero]])
    doubled_unitarity_error = float(
        np.linalg.norm(doubled @ doubled.conj().T - np.eye(6))
    )
    assert doubled_unitarity_error < TOL
    doubled_order, doubled_phase = projective_order(doubled)
    assert doubled_order == 8

    doubled_sq = doubled @ doubled
    doubled_sq_error = max(
        float(np.linalg.norm(doubled_sq[:3, :3] - v)),
        float(np.linalg.norm(doubled_sq[3:, 3:] - v.conj())),
        float(np.linalg.norm(doubled_sq[:3, 3:])),
        float(np.linalg.norm(doubled_sq[3:, :3])),
    )
    assert doubled_sq_error < TOL

    # Reference-state test: one odd tick turns |Omega><Omega| into Choi/3,
    # whose negative spectrum is the complete-positivity obstruction.
    theta = transpose_conjugated_map(u)
    c_odd = choi_matrix(theta)
    odd_inertia, odd_vals = choi_inertia(c_odd)
    assert odd_inertia == [6, 3, 0]
    assert np.linalg.norm(partial_trace_output(c_odd) - np.eye(3)) < TOL
    power_table = []
    max_action_error = 0.0
    max_tp_error = 0.0
    for n in range(8):
        m = mat_power(g, n)
        det = p51.p46.det2(m)
        if n % 2 == 0:
            w_n = np.linalg.matrix_power(v, n // 2)
            action_error = check_unitary_action(w_n, m)
            fn = unitary_channel(w_n)
            kind = "unitary_CPTP"
        else:
            w_n = np.linalg.matrix_power(v, (n - 1) // 2) @ u
            action_error = antiunitary_phase_action(w_n, m)
            fn = transpose_conjugated_map(w_n)
            kind = "positive_TP_not_CP"

        c = choi_matrix(fn)
        inertia, vals = choi_inertia(c)
        tp_error = float(np.linalg.norm(partial_trace_output(c) - np.eye(3)))
        max_action_error = max(max_action_error, action_error)
        max_tp_error = max(max_tp_error, tp_error)
        cp = inertia[1] == 0
        assert cp == (n % 2 == 0)
        assert det == (1 if n % 2 == 0 else 2)
        power_table.append({
            "power": n,
            "det_mod3": det,
            "kind": kind,
            "completely_positive": cp,
            "choi_inertia_pos_neg_zero": inertia,
            "choi_eigenvalues": round_eigs(vals),
            "phase_space_action_error": action_error,
            "trace_preservation_error": tp_error,
        })

    assert max_action_error < TOL
    assert max_tp_error < TOL
    assert all(
        row["choi_inertia_pos_neg_zero"] == ([1, 0, 8] if row["power"] % 2 == 0
                                             else [6, 3, 0])
        for row in power_table
    )

    bell_output_eigs = np.linalg.eigvalsh(c_odd / 3)
    assert np.sum(bell_output_eigs < -TOL) == 3
    assert np.allclose(
        np.sort(bell_output_eigs),
        np.array([-1/3] * 3 + [1/3] * 6),
        atol=TOL,
    )
    four_tick = v @ v
    four_tick_action_error = check_unitary_action(four_tick, p51.Z)
    assert four_tick_action_error < TOL
    four_tick_eigs = np.linalg.eigvals(four_tick)
    four_tick_scalarity = float(abs(np.trace(four_tick)) / 3)
    assert abs(four_tick_scalarity - 1/3) < TOL

    eight_tick = np.linalg.matrix_power(v, 4)
    _, eight_tick_scalar_error = phase_residual(
        eight_tick, np.eye(3, dtype=complex)
    )
    assert eight_tick_scalar_error < TOL

    prior_path = ROOT / "analysis/w33_pass5727_5730_torsion_family_heisenberg.py"
    prior_text = prior_path.read_text(encoding="utf-8")
    assert "'det_minus_one_generator':'complex conjugation K'" in prior_text
    assert "'antiunitary':True" in prior_text

    out = {
        "schema": "w33.pass10952.clock-complete-positivity-firewall.v1",
        "status": "PASS_CLOCK_COMPLETE_POSITIVITY_FIREWALL",
        "parents": {
            "pass10951": p51_data["status"],
            "pass5730": "prior producer confirms det-minus-one antiunitary",
        },
        "qutrit_extended_clifford": {
            "clock_matrix_g": [list(row) for row in g],
            "clock_order": p51.order(g),
            "clock_det_mod3": p51.p46.det2(g),
            "factorization_g_equals_SJ": {
                "S": [list(row) for row in s],
                "J": [list(row) for row in J],
                "S_det_mod3": p51.p46.det2(s),
            },
            "SL23_representatives": len(reps),
            "SL23_action_max_error": rep_error,
            "antiunitary_clock_action_error": anti_error,
            "antiunitary_form": "A = U_S K",
        },
        "complete_positivity_firewall": {
            "single_tick_density_map": "Theta(rho)=U_S rho^T U_S^dagger",
            "single_tick_positive": True,
            "single_tick_trace_preserving": True,
            "single_tick_completely_positive": False,
            "single_tick_choi_inertia_pos_neg_zero": odd_inertia,
            "single_tick_choi_eigenvalues": round_eigs(odd_vals),
            "reference_Bell_output_eigenvalues": round_eigs(bell_output_eigs),
            "all_eight_powers": power_table,
        },
        "even_tick_physical_subgroup": {
            "two_tick_unitary": True,
            "two_tick_channel_projective_order": even_order,
            "two_tick_closure_phase_real": float(even_phase.real),
            "two_tick_closure_phase_imag": float(even_phase.imag),
            "four_tick_phase_space_matrix": "-I2",
            "four_tick_qutrit_action_error": four_tick_action_error,
            "four_tick_qutrit_eigenvalues": [
                [float(z.real), float(z.imag)] for z in four_tick_eigs
            ],
            "four_tick_is_scalar": False,
            "four_tick_scalarity_abs_trace_over_3": four_tick_scalarity,
            "eight_tick_scalar_identity_error": eight_tick_scalar_error,
            "operational_clock": "even powers form a C4 of unitary qutrit channels",
        },
        "representation_firewall": {
            "abstract_group_fact": "g^4=-I in GL(2,3)",
            "spin_representation": "-I maps to scalar -1 in 2T subset Spin(3)",
            "qutrit_Clifford_representation":
                "-I maps to a non-scalar parity Clifford (eigenvalues 1,-1,-1)",
            "consequence":
                "Pass10951 matter-parity weld is a central-character statement, "
                "not equality with the 3D qutrit four-tick unitary.",
        },
        "doubled_conjugate_sector_escape": {
            "carrier_dimension": 6,
            "matrix_form": "[[0,U],[U*,0]] on H plus conjugate(H)",
            "unitarity_error": doubled_unitarity_error,
            "projective_order": doubled_order,
            "closure_phase_real": float(doubled_phase.real),
            "closure_phase_imag": float(doubled_phase.imag),
            "square_block_error": doubled_sq_error,
            "square": "diag(V,V*) with V=U U* the two-tick unitary",
            "reading":
                "odd clock tick can be linearized unitarily only after retaining "
                "a conjugate sector; this is an enlarged carrier, not a qutrit channel",
        },
        "process_consequence": {
            "single_qutrit_slot":
                "odd tick is excluded from deterministic quantum-channel slots by "
                "complete positivity",
            "coarse_grained_option":
                "use two algebraic ticks as one physical unitary clock step",
            "doubled_option":
                "use the 6D qutrit-plus-conjugate carrier for an order-8 unitary lift",
        },
        "theorem": (
            "For the Pass10951 order-eight determinant-odd clock lift, every odd "
            "power acts on qutrit density matrices as a unitary-conjugated transpose. "
            "Its Choi operator has inertia (6,3,0), so it is positive and trace "
            "preserving but not completely positive. Every even power is a unitary "
            "Clifford channel with Choi inertia (1,0,8). Thus the operational "
            "single-qutrit clock is the even C4 subgroup. A 6D carrier H plus "
            "conjugate(H) restores a unitary order-eight lift. The abstract fourth "
            "power -I is scalar in the 2T spin representation but non-scalar in the "
            "3D qutrit Clifford representation."
        ),
        "boundary": (
            "This is a quantum-channel and representation theorem. It does not "
            "identify the algebraic tick with physical time, antiunitarity with a "
            "thermodynamic arrow, or the doubled conjugate sector with literal "
            "past/future degrees of freedom. Process-tensor use of the result means "
            "only that deterministic local operation slots require CP maps."
        ),
    }

    OUT.write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": out["status"],
        "odd_choi_inertia": odd_inertia,
        "even_clock_order": even_order,
        "doubled_order": doubled_order,
        "four_tick_scalarity": four_tick_scalarity,
        "max_action_error": max_action_error,
    }, indent=2))


if __name__ == "__main__":
    main()
