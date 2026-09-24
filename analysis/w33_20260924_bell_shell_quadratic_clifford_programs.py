#!/usr/bin/env python3
"""Bell-shell histories as the exact two-qutrit quadratic Clifford shear group."""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "data/w33_20260924_bell_shell_quadratic_history_intertwiner.json"
OUT = ROOT / "data/w33_20260924_bell_shell_quadratic_clifford_programs.json"
P = 3
INV2 = 2
OMEGA = np.exp(2j*np.pi/P)
TOL = 3e-12


def vec2(i):
    return np.array(divmod(i, P), dtype=int)


def phase_gate(S):
    U = np.zeros((P*P, P*P), dtype=complex)
    for i in range(P*P):
        x = vec2(i)
        q = (INV2 * int(x @ S @ x)) % P
        U[i,i] = OMEGA**q
    return U


def X(a):
    U = np.zeros((P*P, P*P), dtype=complex)
    for i in range(P*P):
        x = vec2(i)
        y = (x + a) % P
        j = int(y[0]*P + y[1])
        U[j,i] = 1
    return U
def Z(b):
    return np.diag([
        OMEGA**(int(b @ vec2(i)) % P)
        for i in range(P*P)
    ])


def projective_distance(A,B):
    z = np.vdot(B.reshape(-1), A.reshape(-1))
    if abs(z) == 0:
        return float("inf")
    phase = z/abs(z)
    return float(np.linalg.norm(A-phase*B))


def skey(S):
    return tuple(int(x) for x in S.reshape(-1))


def main():
    h = json.loads(HISTORY.read_text(encoding="utf-8"))
    assert h["status"] == "PASS_BELL_SHELL_QUADRATIC_HISTORY_INTERTWINER"

    matrices = {}
    context_to_key = {}
    for ctx,row in h["histories"].items():
        S = np.array(row["symmetric_matrix"], dtype=int) % P
        matrices[skey(S)] = S
        context_to_key[ctx] = skey(S)
    assert len(matrices) == 27
    gates = {k: phase_gate(S) for k,S in matrices.items()}
    eye9 = np.eye(P*P)
    assert max(np.linalg.norm(U.conj().T@U-eye9) for U in gates.values()) < TOL

    # Additive F3^3 law: U_S U_T = U_{S+T}.
    max_group_error = 0.0
    for S in matrices.values():
        for T in matrices.values():
            K = skey((S+T)%P)
            err = np.linalg.norm(phase_gate(S)@phase_gate(T)-gates[K])
            max_group_error = max(max_group_error, float(err))
    assert max_group_error < TOL

    # Every U_S is Clifford: labels (a,b) -> (a,b+Sa).
    max_clifford_error = 0.0
    for S in matrices.values():
        U = phase_gate(S)
        for a_tuple in product(range(P), repeat=2):
            for b_tuple in product(range(P), repeat=2):
                a = np.array(a_tuple,dtype=int)
                b = np.array(b_tuple,dtype=int)
                W = X(a)@Z(b)
                lhs = U@W@U.conj().T
                b2 = (b + S@a) % P
                rhs = X(a)@Z(b2)
                err = projective_distance(lhs,rhs)
                max_clifford_error = max(max_clifford_error, err)
    assert max_clifford_error < TOL
    # The induced 4D phase-space shear is symplectic.
    J = np.block([
        [np.zeros((2,2),dtype=int), np.eye(2,dtype=int)],
        [-np.eye(2,dtype=int), np.zeros((2,2),dtype=int)],
    ]) % P
    shear_rows = {}
    for k,S in matrices.items():
        M = np.block([
            [np.eye(2,dtype=int), np.zeros((2,2),dtype=int)],
            [S, np.eye(2,dtype=int)],
        ]) % P
        assert np.array_equal((M.T@J@M)%P, J)
        shear_rows[str(k)] = M.tolist()

    # Rank/determinant class survives as a gate-class label under S4 congruence.
    census = {}
    for row in h["histories"].values():
        census[row["quadratic_type"]] = census.get(row["quadratic_type"],0)+1
    assert census == {"zero":1,"rank1":8,"invertible_det1":6,"invertible_det2":12}

    out = {
        "schema":"w33.20260924.bell_shell_quadratic_clifford_programs.v1",
        "status":"PASS_27_BELL_SHELL_QUADRATIC_CLIFFORD_PROGRAMS",
        "theorem":{
            "program_space":"Sym_2(F3) additive group = F3^3",
            "size":27,
            "unitary":"U_S|x> = omega^(1/2 x^T S x)|x>",
            "composition":"U_S U_T = U_(S+T)",
            "pauli_label_action":"(a,b) -> (a,b+S a)",
            "symplectic_shear":"[[I,0],[S,I]]",
            "conclusion":"the 27 Bell-shell skew contexts form an equivariant atlas of two-qutrit diagonal quadratic Clifford programs",
        },
        "checks":{
            "history_contexts":len(context_to_key),
            "distinct_symmetric_matrices":len(matrices),
            "max_additive_group_error":max_group_error,
            "max_projective_pauli_conjugation_error":max_clifford_error,
            "all_shears_symplectic":True,
            "rank_determinant_census":census,
        },
        "context_to_symmetric_matrix_key":{
            k:list(v) for k,v in context_to_key.items()
        },
        "shears":shear_rows,
        "computational_interpretation":{
            "balanced_geometry":"Bell line supplies the reference spine",
            "program_register":"the 27 skew contexts are the F3^3 quadratic-phase program register",
            "temporal_boundary":"a Clifford program is reversible dynamics; calling it a directed history requires an independent clock/orientation/process choice",
            "adqc_bridge":"these 27 reversible phase programs belong to the Clifford layer of the flying-photon-head architecture; non-Clifford analyzer programming remains the universality resource",
        },
        "literature":[
            "Appleby, arXiv:0909.5233, finite-field metaplectic/Clifford representation",
            "Labib, Quantum 6, 645 (2022), stabilizer states as quadratic phase functions",
        ],
        "boundary":"Exact Clifford/symplectic theorem, not a spacetime or thermodynamic identification.",
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":out["status"],"group_error":max_group_error,
                      "clifford_error":max_clifford_error,"census":census},indent=2))


if __name__=="__main__":
    main()
