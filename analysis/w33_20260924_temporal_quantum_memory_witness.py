#!/usr/bin/env python3
"""Reference-entanglement witness for the Holonet SWAP-break-SWAP memory."""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260924_temporal_quantum_memory_witness.json"
D = 3
TOL = 2e-12


def bell_state():
    psi = np.zeros(D*D, dtype=complex)
    for j in range(D):
        psi[j*D + j] = 1/np.sqrt(D)
    return psi


def partial_transpose(rho, dims, subsystem):
    n = len(dims)
    t = rho.reshape(*(dims + dims))
    axes = list(range(2*n))
    axes[subsystem], axes[n+subsystem] = axes[n+subsystem], axes[subsystem]
    return np.transpose(t, axes).reshape(rho.shape)


def negativity(rho):
    vals = np.linalg.eigvalsh(partial_transpose(rho, [D, D], 1))
    return float(np.sum(np.abs(vals[vals < 0])))


def dephase_one_qutrit_on_second(rho):
    out = np.zeros_like(rho)
    for j in range(D):
        P = np.zeros((D,D), dtype=complex)
        P[j,j] = 1
        K = np.kron(np.eye(D), P)
        out += K @ rho @ K.conj().T
    return out


def isotropic_state(p):
    psi = bell_state()
    bell = np.outer(psi, psi.conj())
    return (1-p)*bell + p*np.eye(D*D)/(D*D)


def analytic_negativity(p):
    return max(0.0, (3.0 - 4.0*p)/3.0)


def bell_fidelity(rho):
    psi = bell_state()
    return float(np.real(np.vdot(psi, rho @ psi)))


def main():
    psi = bell_state()
    bell = np.outer(psi, psi.conj())
    classical = dephase_one_qutrit_on_second(bell)

    coherent_neg = negativity(bell)
    classical_neg = negativity(classical)
    coherent_F = bell_fidelity(bell)
    classical_F = bell_fidelity(classical)

    assert abs(coherent_neg - 1.0) < TOL
    assert abs(classical_neg) < TOL
    assert abs(coherent_F - 1.0) < TOL
    assert abs(classical_F - 1/3) < TOL

    rows = []
    for p in [0.0, 0.1, 0.25, 0.5, 0.74, 0.75, 0.9, 1.0]:
        rho = isotropic_state(p)
        n_num = negativity(rho)
        n_exact = analytic_negativity(p)
        F = bell_fidelity(rho)
        assert abs(n_num - n_exact) < 2e-12
        assert abs(F - (1 - 8*p/9)) < 2e-12
        rows.append({"p":p, "negativity":n_num, "bell_fidelity":F})


    out = {
        "schema": "w33.20260924.temporal_quantum_memory_witness.v1",
        "status": "PASS_REFERENCE_ENTANGLEMENT_TEMPORAL_MEMORY_WITNESS",
        "repo_parent": "BT3717 SWAP-break-SWAP qutrit causal memory",
        "coherent_memory": {
            "final_reference_system_state": "maximally entangled qutrit Bell state",
            "negativity": coherent_neg,
            "bell_fidelity": coherent_F,
        },
        "classical_label_memory": {
            "final_reference_system_state": "1/3 sum_j |jj><jj|",
            "negativity": classical_neg,
            "bell_fidelity": classical_F,
            "passes_basis_retrieval_test": True,
            "fails_reference_entanglement_test": True,
        },
        "depolarizing_memory": {
            "state": "(1-p)|Omega_3><Omega_3| + p I_9/9",
            "negativity_formula": "max(0,(3-4p)/3)",
            "bell_fidelity_formula": "1-8p/9",
            "recovered_channel_entanglement_breaking_boundary": "p=3/4",
            "samples": rows,
        },

        "theorem": (
            "Retrieval after a causal break certifies operational memory. "
            "Preservation of reference entanglement across the break certifies "
            "coherent quantum memory and separates it from a classical trit memory."
        ),
        "process_tensor_boundary": (
            "Reference-entanglement preservation is a sufficient witness of coherent "
            "quantum memory, but its loss is not a necessary-and-sufficient test for "
            "classical multitime memory. Entanglement-breaking channels can still "
            "support genuinely nonclassical temporal correlations. A full classification "
            "requires explicit process-tensor instrument slots and causal constraints."
        ),
        "literature": [
            "Pollock et al., Phys. Rev. A 97, 012127 (2018), process tensor framework",
            "Pollock et al., Phys. Rev. Lett. 120, 040405 (2018), operational Markov condition",
            "Phys. Rev. Research (2025), Entanglement-breaking channels are a quantum memory resource",
        ],
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "coherent_negativity": coherent_neg,
        "classical_negativity": classical_neg,
        "boundary_p": 0.75,
    }, indent=2))


if __name__ == "__main__":
    main()
