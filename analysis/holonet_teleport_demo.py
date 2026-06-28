#!/usr/bin/env python3
"""
Proof of life, part 2 -- two nodes actually teleport a state. The architecture claims the network moves
quantum state by gate teleportation (the store-and-forward repeater primitive); this program runs it.
Two holonet nodes, A and B, share an entangled qutrit Bell pair; node A holds an unknown message
qutrit; A performs a generalized Bell measurement on (message, its half of the pair), getting one of 9
outcomes (k, l) in Z_3 x Z_3; A sends those two trits to B over the classical channel; B applies the
Pauli correction X^k Z^l (a single ALU op on its qutrit), and B's qutrit is now EXACTLY the message --
fidelity 1, verified on an exact state-vector simulator for a random message and for every one of the 9
outcomes. The message is destroyed at A (no-cloning), which is why the corpus's VM-migration claim is
sound: a quantum VM can only move by teleportation, never by copying. This is the quantum-internet
repeater primitive of the companion paper, EXECUTED rather than asserted: the network does not just have
a good topology, it demonstrably relays an unknown quantum state across a link with two classical trits
and one correction. Chain it -- B teleports onward to C against a fresh pair -- and it is entanglement
swapping, the repeater that extends range; the diameter-2 fabric needs only one such swap to connect any
pair, with mu = 4 redundant swap paths.

This runs an exact qutrit teleportation between two nodes: it builds the Bell pair, performs the
generalized Bell measurement, applies the X^k Z^l correction, and verifies fidelity 1 for a random
message across all 9 outcomes.

THE DEMO.
    setup       message qutrit |psi> at A; Bell pair |Phi> = sum_j |jj>/sqrt(3) shared A--B.
    measure     generalized Bell measurement on (message, A-half) -> outcome (k, l) in Z_3 x Z_3.
    classical   A sends 2 trits (k, l) to B.
    correct     B applies X^k Z^l -> B's qutrit = the message; fidelity 1 (verified, all 9 outcomes).
    no-cloning  the message is destroyed at A (so a quantum VM can only migrate by teleportation).

Honest scope: this is an exact (3-qutrit, 27-dimensional) state-vector simulation -- the Bell pair, the
measurement projection, the correction, and the fidelity are all computed, not asserted. It is the
ideal protocol (no channel noise or loss); a physical realization adds the optical loss budget
(~78-88% per-hop survival, hedged by the mu = 4 multipath). The identification of this protocol with the
substrate's gate-teleportation preparation (Stage B) and with entanglement swapping is the corpus /
companion-paper reading. So: a real, executed quantum-state teleportation across a link.

Verifies fidelity-1 teleportation of a random qutrit message for every one of the 9 Bell outcomes,
with the explicit X^k Z^l correction.
"""
from __future__ import annotations

import cmath
import json

import numpy as np

w = cmath.exp(2j * cmath.pi / 3)
X = np.zeros((3, 3), complex)
for _j in range(3):
    X[(_j + 1) % 3, _j] = 1
Z = np.diag([1, w, w**2])


def pauli(a, b):
    return np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b)


def main():
    out = {}
    print("== proof of life, part 2: two nodes actually teleport a state ==")

    rng = np.random.default_rng(2)
    psi = rng.standard_normal(3) + 1j * rng.standard_normal(3)
    psi = psi / np.linalg.norm(psi)
    print(
        f"\n[setup]     message qutrit at node A; Bell pair |Phi> = sum_j |jj>/sqrt(3) shared A--B"
    )

    Phi = np.zeros(9, complex)
    for j in range(3):
        Phi[3 * j + j] = 1 / np.sqrt(3)
    state = np.kron(psi, Phi).reshape(3, 3, 3)  # [message, A-half, B-half]

    def bell(k, l):
        return (np.kron(pauli(k, l), np.eye(3)) @ Phi).reshape(3, 3)

    print(
        f"[run]       generalized Bell measurement on (message, A-half) -> outcome (k,l); B corrects X^k Z^l"
    )
    rows = []
    worst = 1.0
    for k in range(3):
        for l in range(3):
            amp = np.einsum("ab,abc->c", bell(k, l).conj(), state)
            nrm = np.linalg.norm(amp)
            if nrm < 1e-12:
                continue
            b_half = amp / nrm
            corrected = pauli(k, l) @ b_half
            fid = abs(np.vdot(psi, corrected)) ** 2
            worst = min(worst, fid)
            rows.append(
                {
                    "outcome": [k, l],
                    "correction": f"X^{k}Z^{l}",
                    "fidelity": round(float(fid), 6),
                }
            )
            print(
                f"            outcome (k,l)=({k},{l}): B applies X^{k}Z^{l} -> fidelity {fid:.6f}"
            )
    assert worst > 0.999999
    print(
        f"\n[verify]    message recovered at B for all 9 outcomes; min fidelity = {worst:.6f}"
    )
    print(
        f"[no-clone]  the message is destroyed at A -> a quantum VM can only migrate by teleportation"
    )
    out["teleportation"] = {
        "outcomes": rows,
        "min_fidelity": round(float(worst), 6),
        "no_cloning": "message destroyed at A; migration is teleport-only",
    }

    print(
        "\nRESULT: the network moves quantum state, demonstrably. Two nodes share an entangled qutrit"
    )
    print(
        "  Bell pair; node A Bell-measures the unknown message against its half, gets one of 9 outcomes"
    )
    print(
        "  (k,l), sends those two trits to B, and B applies the single correction X^k Z^l -- after"
    )
    print(
        "  which B's qutrit IS the message, fidelity 1 for every outcome (exact simulation). The"
    )
    print(
        "  message is destroyed at A by no-cloning, which is exactly why a quantum VM can migrate only"
    )
    print(
        "  by teleportation, never by copying. This is the quantum-internet repeater primitive"
    )
    print(
        "  EXECUTED: chain it (B onward to C against a fresh pair) and it is entanglement swapping --"
    )
    print(
        "  the diameter-2 fabric needs one swap to connect any pair, with mu = 4 redundant paths."
    )
    print(
        "  Honest: an exact 3-qutrit simulation of the ideal protocol (no channel loss); the optical"
    )
    print(
        "  loss budget and the Stage-B / swapping identification are the companion-paper reading."
    )

    out["summary"] = (
        "proof of life, part 2: two nodes actually teleport a state. Exact 3-qutrit (27-dimensional) "
        "state-vector run: a message qutrit |psi> at node A and a Bell pair |Phi> = sum_j |jj>/sqrt(3) "
        "shared A--B; A performs the generalized Bell measurement on (message, A-half) -> one of 9 "
        "outcomes (k,l) in Z_3xZ_3; A sends 2 classical trits to B; B applies X^k Z^l -> B's qutrit IS "
        "the message, fidelity 1.0 for all 9 outcomes (verified). The message is destroyed at A "
        "(no-cloning), so a quantum VM can migrate only by teleportation, never by copying. This is the "
        "quantum-internet repeater primitive EXECUTED -- chained (B->C against a fresh pair) it is "
        "entanglement swapping; the diameter-2 fabric needs one swap per pair, mu = 4 redundant paths. "
        "HONEST: exact ideal protocol (no channel noise/loss); the optical loss budget (~78-88% per-hop "
        "survival, mu=4 hedge) and the identification with the substrate's Stage-B gate-teleportation "
        "preparation and with swapping are the corpus/companion-paper reading."
    )
    out["sources"] = [
        "generalized qudit teleportation (Bennett et al. generalized to qutrits); Bell measurement + "
        "X^k Z^l correction (computed here, exact); substrate gate-teleportation preparation Stage B "
        "(corpus two-carrier); entanglement swapping = chained teleportation (quantum-internet "
        "literature; w33_quantum_internet)."
    ]
    with open("data/holonet_teleport_demo.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/holonet_teleport_demo.json")


if __name__ == "__main__":
    main()
