#!/usr/bin/env python3
"""Pass 10941 front 2: compile h7=h4 *_Z h3 to a finite gate ABI.

The fourteen coordinates modulo the common center form a symplectic phase
space.  We compile rank-one symplectic transvections for the 8D data lane and
6D control lane, then add one bridge transvection.  Exact modular Lie closure
distinguishes the lane-local algebra sp8+sp6 from the connected algebra sp14.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass10941_symplectic_vm_gate_compiler.json"


def mm(A, B, p):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) % p
             for j in range(len(B[0]))] for i in range(len(A))]


def tr(A):
    return [list(x) for x in zip(*A)]


def flat(A, p):
    return tuple(x % p for row in A for x in row)


def add_basis(basis, pivots, v, p):
    w = list(v)
    for row, pivot in zip(basis, pivots):
        if w[pivot]:
            z = w[pivot]
            w = [(a - z * b) % p for a, b in zip(w, row)]
    try:
        pivot = next(i for i, x in enumerate(w) if x)
    except StopIteration:
        return False
    z = pow(w[pivot], -1, p)
    w = [(z * x) % p for x in w]
    for i, row in enumerate(basis):
        if row[pivot]:
            z = row[pivot]
            basis[i] = [(a - z * b) % p for a, b in zip(row, w)]
    k = next((i for i, q in enumerate(pivots) if q > pivot), len(pivots))
    pivots.insert(k, pivot)
    basis.insert(k, w)
    return True


def lie_closure(generators, p):
    n = len(generators[0])
    basis, pivots, matrices = [], [], []
    queue = []
    for A in generators:
        if add_basis(basis, pivots, flat(A, p), p):
            matrices.append(A)
            queue.append(A)
    qi = 0
    while qi < len(queue):
        A = queue[qi]
        qi += 1
        # Bracketing with the expanding basis is sufficient: every new
        # direction is queued and will meet every direction already present.
        snapshot = list(matrices)
        for B in snapshot:
            AB, BA = mm(A, B, p), mm(B, A, p)
            C = [[(AB[i][j] - BA[i][j]) % p for j in range(n)] for i in range(n)]
            if add_basis(basis, pivots, flat(C, p), p):
                matrices.append(C)
                queue.append(C)
    return len(basis)


def sp_order(m, q):
    out = q ** (m * m)
    for i in range(1, m + 1):
        out *= q ** (2 * i) - 1
    return out


def packet(p):
    modes, n = 7, 14
    J = [[0] * n for _ in range(n)]
    for i in range(modes):
        J[i][modes + i] = 1
        J[modes + i][i] = -1 % p

    def transvection(v):
        # T_v(x)=x+v*omega(v,x), omega(v,x)=v^T J x.
        vJ = [sum(v[k] * J[k][j] for k in range(n)) % p for j in range(n)]
        return [[(int(i == j) + v[i] * vJ[j]) % p for j in range(n)] for i in range(n)]

    names, directions = [], []
    for i in range(modes):
        for kind, pos in (("e", i), ("f", modes + i)):
            v = [0] * n
            v[pos] = 1
            names.append(f"T_{kind}{i}")
            directions.append(v)
    for lo, hi, lane in ((0, 4, "data"), (4, 7, "control")):
        for i in range(lo, hi - 1):
            for kind, off in (("e", 0), ("f", modes)):
                v = [0] * n
                v[off + i] = v[off + i + 1] = 1
                names.append(f"T_{kind}{i}+{kind}{i+1}_{lane}")
                directions.append(v)
    local_count = len(directions)
    bridge = [0] * n
    bridge[3] = bridge[4] = 1
    names.append("T_e3+e4_bridge")
    directions.append(bridge)
    matrices = [transvection(v) for v in directions]

    JT = tr(J)
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    for T in matrices:
        assert mm(mm(tr(T), J, p), T, p) == J
        # Characteristic-p transvections have order p.
        Tp = I
        for _ in range(p):
            Tp = mm(Tp, T, p)
        assert Tp == I

    nilpotents = []
    for T in matrices:
        nilpotents.append([[(T[i][j] - I[i][j]) % p for j in range(n)] for i in range(n)])
    local_dim = lie_closure(nilpotents[:local_count], p)
    full_dim = lie_closure(nilpotents, p)
    assert local_dim == 4 * 9 + 3 * 7 == 57
    assert full_dim == 7 * 15 == 105

    encoded = json.dumps(matrices, separators=(",", ":")).encode()
    return {
        "prime": p,
        "coordinates": [f"e{i}" for i in range(7)] + [f"f{i}" for i in range(7)],
        "data_modes": [0, 1, 2, 3],
        "control_modes": [4, 5, 6],
        "local_gate_count": local_count,
        "bridge_gate": names[-1],
        "gate_names": names,
        "gate_directions": directions,
        "gate_matrices_sha256": hashlib.sha256(encoded).hexdigest(),
        "all_gates_symplectic": True,
        "all_transvections_have_order_p": True,
        "local_Lie_closure_dimension": local_dim,
        "local_Lie_algebra": "sp(8,p) direct_sum sp(6,p)",
        "connected_Lie_closure_dimension": full_dim,
        "connected_Lie_algebra": "sp(14,p)",
        "local_symplectic_group_order": sp_order(4, p) * sp_order(3, p),
        "full_symplectic_group_order": sp_order(7, p),
    }


packets = [packet(3), packet(103)]
assert packets[0]["local_gate_count"] == packets[1]["local_gate_count"] == 24

out = {
    "schema": "w33.pass10941.symplectic_vm_gate_compiler.v1",
    "status": "PASS_H7_CENTRAL_PRODUCT_TO_SEVEN_QUTRIT_CLIFFORD_ABI",
    "source_abi": {
        "phase_space": "h7/Z = W8 orthogonal_sum U6orth",
        "central_product": "h7 = h4 *_Z h3",
        "logical_modes": 7,
        "shared_phase_registers": 1,
    },
    "compiler": {
        "local_generators": 24,
        "entangling_bridge_generators": 1,
        "bridge": "one transvection along e3+e4 couples the 4-mode data lane to the 3-mode control lane",
        "certification": (
            "exact modular commutator closure gives sp8+sp6 before the bridge "
            "and sp14 after it; the listed elementary symplectic transvections "
            "are the standard generators of the corresponding symplectic groups"
        ),
    },
    "prime_packets": packets,
    "universality": {
        "with_heisenberg_translations": "full seven-qutrit Clifford/stabilizer instruction set",
        "classically_simulable_boundary": "Clifford gates plus stabilizer preparation and Pauli measurement remain stabilizer computation",
        "scope_of_false_flag": "bare Clifford/stabilizer compiler without a supplied non-stabilizer resource",
        "universal_quantum_computation": False,
        "extension_status": "closed in the ideal-resource model by the Pass 10941 qutrit universal-instruction bridge",
        "extension_certificate": "data/w33_pass10941_qutrit_universal_instruction_bridge.json",
        "extension_routes": [
            "fixed-interaction ADQC T-program analyzer",
            "Pass 411 Choi-pair T injection with Clifford feedforward",
        ],
        "remaining_physical_resource": "protected non-stabilizer analyzer or endogenous magic factory below threshold",
    },
    "ramified_basis_boundary": (
        "The p=3 packet is the canonical logical qutrit ABI. The currently frozen "
        "rational Asai/U6orth chart has denominators divisible by 3, so it is not "
        "reduced coordinatewise at that ramified prime. The p=103 packet is a good-"
        "prime model compatible with the existing finite intertwiner workflow."
    ),
    "parents": [
        "analysis/w33_20260924_trialitarian_asai_cube_descent.py",
        "data/w33_20260924_trialitarian_asai_cube_descent.json",
    ],
}
OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": out["status"],
    "p3_dims": [packets[0]["local_Lie_closure_dimension"], packets[0]["connected_Lie_closure_dimension"]],
    "p103_dims": [packets[1]["local_Lie_closure_dimension"], packets[1]["connected_Lie_closure_dimension"]],
}, indent=2))
