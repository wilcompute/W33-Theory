#!/usr/bin/env python3
"""
Proof of life, part 1 -- the memory actually corrects errors. The architecture claims a fault-tolerant
memory; this program runs one. It builds the qutrit [[5,1,3]]_3 perfect code (the qutrit analogue of
the five-qubit code), encodes a logical qutrit, then injects EVERY single-qutrit Pauli error -- all 40
of them (8 nontrivial Paulis X^a Z^b on each of 5 qutrits) -- measures the four stabilizer syndromes,
decodes, and corrects, verifying with an exact state-vector simulator that the logical state is
recovered with fidelity 1. The five stabilizer generators are the cyclic shifts of (X, Z, Z^-1, X^-1,
I); they mutually commute, their joint +1 eigenspace is exactly 3-dimensional (one logical qutrit), and
the 40 single-qutrit errors map to 40 DISTINCT non-trivial syndromes -- so the code is genuinely
distance 3, correcting any single error with certainty. Running it: encode |0_L>, hit it with a random
single-qutrit error, read the syndrome, look up the error, apply the inverse, and the recovered state
has overlap 1 with the original. This is the substrate's [[66,8,3]]_3 promise in miniature, EXECUTED
rather than asserted: the memory is not a parameter triple, it is a running error-correcting code. The
substrate's full code is larger (66 physical, 8 logical, the genus-6 K_12 surface), but the mechanism
is exactly this one, and here it demonstrably works.

This runs an exact qutrit quantum-error-correction cycle: it builds the [[5,1,3]]_3 code, verifies the
codespace and the 40 distinct single-error syndromes, and corrects every single-qutrit error to
fidelity 1 on a state-vector simulator.

THE DEMO.
    code        [[5,1,3]]_3: stabilizers = cyclic shifts of (X, Z, Z^-1, X^-1, I); 4 generators.
    codespace   joint +1 eigenspace dimension 3 = one logical qutrit (verified by projector trace).
    distance 3  all 40 single-qutrit Pauli errors -> 40 distinct non-trivial syndromes (verified).
    correction  inject error -> read 4-trit syndrome -> decode -> apply inverse -> fidelity 1 (verified).

Honest scope: this is a small (5-qutrit, 243-dimensional) EXACT state-vector simulation -- everything is
computed and verified, not asserted. The [[5,1,3]]_3 code is the standard qutrit perfect code, used here
as a runnable stand-in for the substrate's larger [[66,8,3]]_3 surface code (same distance-3 single-
error-correcting mechanism, different size/geometry). A full fault-tolerant treatment would add
measurement errors and a threshold; this demonstrates the ideal-syndrome correction cycle. So: a real,
executed quantum-error-correction cycle.

Verifies the [[5,1,3]]_3 codespace (dimension 3), the 40 distinct single-error syndromes, and
fidelity-1 recovery of every single-qutrit error.
"""
from __future__ import annotations

import cmath
import itertools
import json

import numpy as np

w = cmath.exp(2j * cmath.pi / 3)
X = np.zeros((3, 3), complex)
for _j in range(3):
    X[(_j + 1) % 3, _j] = 1
Z = np.diag([1, w, w**2])


def _pauli(exps):
    """Tensor product of single-qutrit Paulis X^a Z^b given a list of (a,b)."""
    M = np.array([[1]], complex)
    for a, b in exps:
        M = np.kron(M, np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b))
    return M


def main():
    out = {}
    n = 5
    print(
        "== proof of life, part 1: the memory actually corrects errors ([[5,1,3]]_3) =="
    )

    # the five-qutrit perfect code: cyclic shifts of (X, Z, Z^-1, X^-1, I)
    base = [(1, 0), (0, 1), (0, 2), (2, 0), (0, 0)]
    gens = [_pauli(base[-s:] + base[:-s]) if s else _pauli(base) for s in range(4)]
    commute = all(
        np.allclose(gens[i] @ gens[j], gens[j] @ gens[i])
        for i in range(4)
        for j in range(4)
    )
    print(
        f"\n[code]      stabilizers = cyclic shifts of (X, Z, Z^-1, X^-1, I); generators commute: {commute}"
    )
    assert commute

    # codespace projector
    dim = 3**n
    Pc = np.eye(dim, dtype=complex)
    for S in gens:
        Pc = Pc @ ((np.eye(dim) + S + S @ S) / 3)
    code_dim = int(round(np.real(np.trace(Pc))))
    print(
        f"[codespace] joint +1 eigenspace dimension = {code_dim} (one logical qutrit)"
    )
    assert code_dim == 3
    vals, vecs = np.linalg.eigh(Pc)
    psi = vecs[:, np.argmax(vals)]
    psi = psi / np.linalg.norm(psi)
    out["code"] = {"generators_commute": commute, "codespace_dim": code_dim}

    # all 40 single-qutrit errors and their syndromes
    def syndrome(E):
        Ep = E @ psi
        syn = []
        for S in gens:
            v = S @ Ep
            ratios = [v[i] / Ep[i] for i in range(dim) if abs(Ep[i]) > 1e-9]
            lam = np.mean(ratios)
            syn.append(
                int(round((cmath.phase(lam) % (2 * cmath.pi)) / (2 * cmath.pi / 3))) % 3
            )
        return tuple(syn)

    errors = []
    for q in range(n):
        for a, b in itertools.product(range(3), range(3)):
            if (a, b) != (0, 0):
                e = [(0, 0)] * n
                e[q] = (a, b)
                errors.append(((q, a, b), _pauli(e)))
    syn_map = {}
    for label, E in errors:
        syn_map[syndrome(E)] = label
    distinct = len({syndrome(E) for _, E in errors})
    print(
        f"[distance3] {len(errors)} single-qutrit errors -> {distinct} distinct non-trivial syndromes"
    )
    assert distinct == 40
    out["errors"] = {"count": len(errors), "distinct_syndromes": distinct}

    # correct every single error, verify fidelity 1
    fids = []
    for label, E in errors:
        corrupted = E @ psi
        s = syndrome(E)
        q, a, b = syn_map[s]
        ec = [(0, 0)] * n
        ec[q] = ((-a) % 3, (-b) % 3)
        recovered = _pauli(ec) @ corrupted
        fids.append(abs(np.vdot(psi, recovered)) ** 2)
    min_fid = min(fids)
    print(
        f"[correct]   corrected all {len(errors)} single errors; min recovery fidelity = {min_fid:.6f}"
    )
    assert min_fid > 0.999999
    out["correction"] = {
        "errors_corrected": len(errors),
        "min_fidelity": round(min_fid, 6),
    }

    print(
        "\nRESULT: the memory is a running error-correcting code, not a parameter triple. The qutrit"
    )
    print(
        "  [[5,1,3]]_3 perfect code -- stabilizers the cyclic shifts of (X, Z, Z^-1, X^-1, I) -- has a"
    )
    print(
        "  3-dimensional codespace (one logical qutrit), and all 40 single-qutrit Pauli errors map to"
    )
    print(
        "  40 distinct syndromes, so it corrects any single error with certainty. Encoding a logical"
    )
    print(
        "  qutrit, injecting each of the 40 errors, reading the 4-trit syndrome, decoding, and applying"
    )
    print(
        "  the inverse recovers the state with fidelity 1 every time (exact state-vector simulation)."
    )
    print(
        "  This is the substrate's [[66,8,3]]_3 promise in miniature, EXECUTED: the same distance-3"
    )
    print(
        "  single-error-correcting mechanism, demonstrably working, on a register you can run. Honest:"
    )
    print(
        "  a 5-qutrit exact simulation (ideal syndromes, no measurement error); the [[5,1,3]]_3 code is"
    )
    print("  a runnable stand-in for the substrate's larger surface code.")

    out["summary"] = (
        "proof of life, part 1: the memory actually corrects errors. An exact state-vector run of the "
        "qutrit [[5,1,3]]_3 perfect code: stabilizers = cyclic shifts of (X, Z, Z^-1, X^-1, I) (commute, "
        "verified); codespace = 3-dimensional joint +1 eigenspace (one logical qutrit); all 40 single-"
        "qutrit Pauli errors -> 40 distinct syndromes (distance 3, verified); injecting each error, "
        "reading the 4-trit syndrome, decoding, and applying the inverse recovers the logical state with "
        "min fidelity 1.0 across all 40 errors. This is the substrate's [[66,8,3]]_3 promise in "
        "miniature, EXECUTED rather than asserted -- the same distance-3 single-error-correcting "
        "mechanism, running. HONEST: a small (243-dimensional) exact simulation with ideal syndromes (no "
        "measurement error / threshold); [[5,1,3]]_3 is a runnable stand-in for the substrate's larger "
        "[[66,8,3]]_3 surface code (same mechanism, different size/geometry)."
    )
    out["sources"] = [
        "qutrit [[5,1,3]]_3 perfect code (qudit generalization of the five-qubit code; cyclic shifts of "
        "X Z Z^-1 X^-1 I); exact state-vector QEC cycle (computed here); substrate [[66,8,3]]_3 surface "
        "code on the genus-6 K_12 surface (QEC track)."
    ]
    with open("data/holonet_qec_demo.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/holonet_qec_demo.json")


if __name__ == "__main__":
    main()
