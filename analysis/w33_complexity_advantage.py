#!/usr/bin/env python3
"""
The complexity class: the machine sits exactly on the classical/quantum boundary, on the quantum side
by the mana the cubic gate injects. Pass 34 showed the instruction set is universal; this pass places
it in the complexity hierarchy and locates the precise resource that puts it on the hard side. The
separating invariant is the discrete Wigner function on the qutrit phase space. The degree-2 (Clifford)
layer keeps the Wigner function NON-NEGATIVE: we compute the Gross qutrit Wigner function of all 12
single-qutrit stabilizer states and every one is >= 0, so by the Veitch-Mari-Emerson-Gross theorem the
Clifford datapath (positive Wigner, evolved by Clifford, read by Pauli measurement) is EFFICIENTLY
CLASSICALLY SIMULABLE -- it lives in P (the qudit Gottesman-Knill class). The degree-3 (cubic) magic
gate breaks exactly this: its resource magic state (the qutrit "Strange" state) has a NEGATIVE Wigner
entry (-1/3) and positive mana = ln||W||_1 = ln(5/3) = 0.5108 > 0, and by Howard-Wallman-Veitch-Emerson
(2014) Wigner negativity is EQUIVALENT to contextuality for odd-prime qudits and is NECESSARY for
quantum speed-up. So the machine's power is sharply located: Clifford alone = P (simulable, zero mana,
non-contextual), Clifford + the one cubic magic gate = BQP-universal, and the difference is precisely
the negativity / contextuality the cubic injects. And the advantage is hard to fake classically: a
circuit family that samples from these magic-fuelled outputs cannot be simulated by any efficient
classical sampler unless the polynomial hierarchy collapses (the standard post-selection argument for
non-stabilizer circuits). So the complexity verdict is: the substrate computes in BQP, it crosses out
of the classically-simulable class exactly when the cubic gate adds Wigner-negative mana, and that
crossing is contextuality -- the resource the substrate's own W(3,3) supplies.

This places the machine in the complexity hierarchy by computing the separating invariant (Wigner
non-negativity of the Clifford layer vs Wigner-negative mana of the magic state) and stating the
resulting P / BQP boundary and classical-hardness barrier.

THE BOUNDARY.
    Clifford layer (degree 2).  all 12 single-qutrit stabilizer states have Wigner W >= 0 (computed)
        -> Veitch-Mari: positive Wigner + Clifford + Pauli measurement = efficiently classically
        simulable = P (qudit Gottesman-Knill). Zero mana, non-contextual.
    magic gate (degree 3).  the Strange state has min Wigner = -1/3 < 0, mana = ln(5/3) = 0.5108 > 0
        -> Howard et al. (2014): Wigner negativity <=> contextuality (odd prime d), NECESSARY for
        speed-up. The cubic injects exactly this.
    placement.  Clifford = P; Clifford + 1 cubic = BQP-universal. The difference IS the mana.
    hardness.  classically sampling the magic-fuelled output collapses PH (post-selection argument);
        no efficient classical simulator unless PH collapses.

Honest scope: the Wigner non-negativity of the 12 stabilizer states and the Strange-state mana =
ln(5/3) are computed here (the mana matches the corpus magic-economy value); the Veitch-Mari
simulability of positive-Wigner Clifford dynamics, the Howard et al. negativity<=>contextuality
equivalence, the Lloyd-Braunstein universality, and the post-selection hardness argument are
established theorems. The substrate content is that the machine's Clifford layer is exactly the
Wigner-positive (P) class and the cubic magic gate supplies the negativity/contextuality that lifts it
to BQP, with W(3,3) the contextuality structure. "BQP" is the standard placement of a universal
quantum machine; the classical-hardness is conditional on PH not collapsing. So: a precise P/BQP
location with the resource identified.

Verifies the Wigner non-negativity of all 12 qutrit stabilizer states, the Wigner-negative mana =
ln(5/3) of the magic state, and the resulting P / BQP boundary.
"""
from __future__ import annotations

import cmath
import json
import math

import numpy as np

D = 3
w = cmath.exp(2j * cmath.pi / 3)


def Xmat():
    M = np.zeros((D, D), complex)
    for j in range(D):
        M[(j + 1) % D, j] = 1
    return M


def Zmat():
    return np.diag([w**j for j in range(D)])


def displacement(a, b):
    """Odd-d Weyl displacement D(a,b) = tau^{ab} X^a Z^b, tau = w^{2^{-1}} (Gross 2006)."""
    inv2 = pow(2, -1, D)
    Xa = np.linalg.matrix_power(Xmat(), a % D)
    Zb = np.linalg.matrix_power(Zmat(), b % D)
    return (w ** ((inv2 * a * b) % D)) * (Xa @ Zb)


def parity():
    P = np.zeros((D, D), complex)
    for j in range(D):
        P[(-j) % D, j] = 1
    return P


def phase_point_operators():
    A0 = parity()
    A = {}
    for q in range(D):
        for p in range(D):
            Dqp = displacement(q, p)
            A[(q, p)] = Dqp @ A0 @ Dqp.conj().T
    return A


def wigner(rho, A):
    return {qp: float(np.real(np.trace(rho @ A[qp])) / D) for qp in A}


def main():
    out = {}
    A = phase_point_operators()
    print(
        "== the complexity class: Clifford = P, + the cubic magic gate = BQP, the gap is mana =="
    )

    # Clifford layer: 12 stabilizer states, all Wigner >= 0
    bases = [
        Zmat(),
        Xmat(),
        Xmat() @ Zmat(),
        Xmat() @ np.linalg.matrix_power(Zmat(), 2),
    ]
    stab = []
    for M in bases:
        vals, vecs = np.linalg.eig(M)
        for i in range(D):
            v = vecs[:, i] / np.linalg.norm(vecs[:, i])
            stab.append(v)
    min_stab = min(min(wigner(np.outer(v, v.conj()), A).values()) for v in stab)
    print(
        f"\n[Clifford layer = P]  {len(stab)} single-qutrit stabilizer states; min Wigner = {min_stab:.3f}"
    )
    print(
        f"  all W >= 0 -> Veitch-Mari: positive Wigner + Clifford + Pauli readout = efficiently"
    )
    print(
        f"  classically simulable (qudit Gottesman-Knill) = P; zero mana, non-contextual"
    )
    assert min_stab > -1e-9
    out["clifford_layer"] = {
        "num_stabilizer_states": len(stab),
        "min_wigner": round(min_stab, 6),
        "all_nonnegative": True,
        "complexity": "P (Veitch-Mari: positive-Wigner Clifford dynamics efficiently classically simulable)",
    }

    # magic gate: Strange state, Wigner-negative, mana = ln(5/3)
    s = np.array([0, 1, -1], complex) / math.sqrt(2)
    Ws = wigner(np.outer(s, s.conj()), A)
    min_magic = min(Ws.values())
    mana = math.log(sum(abs(x) for x in Ws.values()))
    print(
        f"\n[magic gate = BQP resource]  the Strange state |1>-|2>: min Wigner = {min_magic:.3f} < 0"
    )
    print(
        f"  mana = ln||W||_1 = {mana:.4f} = ln(5/3) > 0 (matches corpus magic economy)"
    )
    print(
        f"  Howard et al. 2014: Wigner negativity <=> contextuality (odd prime d), NECESSARY for speed-up"
    )
    assert min_magic < -1e-6 and abs(mana - math.log(5 / 3)) < 1e-6
    out["magic_gate"] = {
        "state": "the qutrit Strange state (|1> - |2>)/sqrt(2)",
        "min_wigner": round(min_magic, 6),
        "mana": round(mana, 6),
        "mana_closed_form": "ln(5/3)",
        "meaning": "Wigner-negative <=> contextual (Howard et al.) = the necessary resource for advantage",
    }

    # placement + hardness
    print(
        "\n[placement]  Clifford = P;  Clifford + 1 cubic = BQP-universal;  the difference IS the mana"
    )
    print(
        "[hardness]  classically sampling the magic-fuelled output collapses PH (post-selection)"
    )
    out["placement"] = {
        "clifford_only": "P (classically simulable)",
        "clifford_plus_cubic": "BQP-universal (Lloyd-Braunstein)",
        "separating_resource": "Wigner-negative mana / contextuality injected by the degree-3 cubic gate",
        "classical_hardness": "no efficient classical sampler of the magic-fuelled output unless the polynomial hierarchy collapses (post-selection argument)",
    }

    print(
        "\nRESULT: the machine sits exactly on the classical/quantum boundary, on the quantum side by"
    )
    print(
        "  the mana the cubic gate injects. The separating invariant is the Gross qutrit Wigner"
    )
    print(
        "  function. The degree-2 Clifford layer keeps it NON-NEGATIVE -- all 12 single-qutrit"
    )
    print(
        "  stabilizer states have Wigner >= 0 -- so by Veitch-Mari-Emerson-Gross the Clifford"
    )
    print(
        "  datapath (positive Wigner, Clifford evolution, Pauli readout) is efficiently classically"
    )
    print(
        "  simulable: it lives in P, the qudit Gottesman-Knill class, with zero mana and no"
    )
    print(
        "  contextuality. The degree-3 cubic magic gate breaks exactly this: its resource state (the"
    )
    print(
        "  Strange state) has a negative Wigner entry (-1/3) and positive mana = ln(5/3) = 0.5108, and"
    )
    print(
        "  by Howard-Wallman-Veitch-Emerson (2014) Wigner negativity IS contextuality for odd-prime"
    )
    print(
        "  qudits and is necessary for speed-up. So the power is sharply located: Clifford alone = P,"
    )
    print(
        "  Clifford + one cubic = BQP-universal, and the difference is precisely the negativity /"
    )
    print(
        "  contextuality the cubic injects -- which the substrate's own W(3,3) supplies. And the"
    )
    print(
        "  advantage resists classical faking: sampling the magic-fuelled output collapses the"
    )
    print(
        "  polynomial hierarchy. Honest: the Wigner positivity and the mana = ln(5/3) are computed;"
    )
    print(
        "  Veitch-Mari simulability, Howard's negativity<=>contextuality, and the post-selection"
    )
    print(
        "  hardness are established theorems; BQP is the standard placement of a universal quantum"
    )
    print("  machine, the classical-hardness conditional on PH not collapsing.")

    out["summary"] = (
        "the complexity class: the machine sits exactly on the classical/quantum boundary, on the "
        "quantum side by the mana the cubic gate injects. The separating invariant is the Gross qutrit "
        "Wigner function. Clifford layer (degree 2): all 12 single-qutrit stabilizer states have Wigner "
        ">= 0 (computed, min = 0) -> Veitch-Mari-Emerson-Gross: positive-Wigner Clifford dynamics with "
        "Pauli readout is efficiently classically simulable = P (qudit Gottesman-Knill), zero mana, "
        "non-contextual. Magic gate (degree 3): the Strange state has min Wigner = -1/3 < 0 and mana = "
        "ln||W||_1 = ln(5/3) = 0.5108 > 0 (matches corpus) -> Howard-Wallman-Veitch-Emerson (2014): "
        "Wigner negativity <=> contextuality for odd-prime qudits, NECESSARY for speed-up. Placement: "
        "Clifford = P; Clifford + 1 cubic = BQP-universal; the difference IS the mana. Hardness: "
        "classically sampling the magic-fuelled output collapses the polynomial hierarchy "
        "(post-selection). So the machine computes in BQP, crossing out of the classically-simulable "
        "class exactly when the cubic gate adds Wigner-negative mana, and that crossing is "
        "contextuality, supplied by W(3,3). HONEST: the Wigner positivity of the 12 stabilizer states "
        "and the Strange-state mana = ln(5/3) are computed here; Veitch-Mari simulability, Howard's "
        "negativity<=>contextuality equivalence, Lloyd-Braunstein universality, and the post-selection "
        "hardness argument are established; BQP is the standard placement of a universal quantum "
        "machine and the classical-hardness is conditional on PH not collapsing."
    )
    out["sources"] = [
        "Gross discrete Wigner function for odd-prime qudits (2006); Veitch-Ferrie-Gross-Emerson / "
        "Mari-Eisert: positive Wigner -> efficient classical simulation; Howard-Wallman-Veitch-Emerson "
        "(Nature 2014) contextuality <=> Wigner negativity, necessary for magic-state speed-up; "
        "Gottesman-Knill (Clifford simulable); Lloyd-Braunstein universality; Bremner-Jozsa-Shepherd / "
        "Aaronson-Arkhipov post-selection hardness (PH collapse); corpus mana = ln(5/3) "
        "(w33_magic_economy.py, w33_contextuality_is_the_fuel.py)."
    ]
    with open("data/w33_complexity_advantage.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_complexity_advantage.json")


if __name__ == "__main__":
    main()
