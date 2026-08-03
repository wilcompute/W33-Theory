#!/usr/bin/env python3
"""Pass 2784: exhaustive two-copy stabilizer search for an M36 distiller.

The native M36 resource is treated as a two-qubit/ququart pure state.  We
exhaust all binary [[4,2]] stabilizer subspaces (two commuting independent
checks on two copies), all four syndromes, and one representative of each of
the four two-qubit Clifford orbits inside M36.  A protocol is retained when
its ideal decoded output is Clifford-equivalent to an M36 ray.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
S = np.diag([1, 1j]).astype(complex)


def canon_unitary(u: np.ndarray, tol: float = 1e-9) -> tuple[float, ...]:
    z = next(x for x in u.ravel() if abs(x) > tol)
    v = u * np.exp(-1j * np.angle(z))
    return tuple(np.round(v.real, 10).ravel()) + tuple(np.round(v.imag, 10).ravel())


def canon_state(v: np.ndarray, tol: float = 1e-9) -> tuple[float, ...]:
    z = next(x for x in v if abs(x) > tol)
    w = v * np.exp(-1j * np.angle(z))
    return tuple(np.round(w.real, 10)) + tuple(np.round(w.imag, 10))


def two_qubit_clifford() -> tuple[list[np.ndarray], dict[tuple[float, ...], list[str]]]:
    cnot = np.zeros((4, 4), dtype=complex)
    for a, b in itertools.product(range(2), repeat=2):
        cnot[2 * a + (b ^ a), 2 * a + b] = 1
    generators = [
        ("H0", np.kron(H, I2)),
        ("H1", np.kron(I2, H)),
        ("S0", np.kron(S, I2)),
        ("S1", np.kron(I2, S)),
        ("CX01", cnot),
    ]
    ident = np.eye(4, dtype=complex)
    seen: dict[tuple[float, ...], tuple[np.ndarray, list[str]]] = {canon_unitary(ident): (ident, [])}
    q = deque([ident])
    while q:
        u = q.popleft()
        word = seen[canon_unitary(u)][1]
        for name, g in generators:
            v = u @ g
            key = canon_unitary(v)
            if key not in seen:
                seen[key] = (v, word + [name])
                q.append(v)
    assert len(seen) == 11520
    return [x[0] for x in seen.values()], {k: x[1] for k, x in seen.items()}


def m36_rays() -> tuple[list[np.ndarray], list[tuple[int, int, int]]]:
    omega = np.exp(2j * np.pi / 3)
    rays: list[np.ndarray] = []
    metadata: list[tuple[int, int, int]] = []
    for family, mu, nu in itertools.product(range(4), range(3), range(3)):
        if family == 0:
            raw = [0, 1, -(omega**mu), omega**nu]
        elif family == 1:
            raw = [1, 0, -(omega**mu), -(omega**nu)]
        elif family == 2:
            raw = [1, -(omega**mu), 0, omega**nu]
        else:
            raw = [1, omega**mu, omega**nu, 0]
        rays.append(np.array(raw, dtype=complex) / math.sqrt(3))
        metadata.append((family, mu, nu))
    return rays, metadata


def symp(a: int, b: int) -> int:
    ax, az = a & 15, (a >> 4) & 15
    bx, bz = b & 15, (b >> 4) & 15
    return ((ax & bz).bit_count() + (az & bx).bit_count()) & 1


def span_set(basis: list[int]) -> set[int]:
    out = {0}
    for b in basis:
        out |= {x ^ b for x in list(out)}
    return out


def isotropic_rank2_subspaces() -> list[tuple[int, int, int]]:
    spaces = {
        tuple(sorted((u, v, u ^ v)))
        for u in range(1, 256)
        for v in range(u + 1, 256)
        if symp(u, v) == 0
    }
    out = sorted(spaces)
    assert len(out) == 5355
    return out


def pauli_matrix(v: int) -> np.ndarray:
    x, z = v & 15, (v >> 4) & 15
    out = np.array([[1]], dtype=complex)
    phase = 0
    for q in range(4):
        xb, zb = (x >> q) & 1, (z >> q) & 1
        phase += xb * zb
        out = np.kron(out, np.linalg.matrix_power(X, xb) @ np.linalg.matrix_power(Z, zb))
    return (1j**phase) * out


PAULI = {v: pauli_matrix(v) for v in range(256)}
I16 = np.eye(16, dtype=complex)


def logical_completion(space: tuple[int, int, int]) -> tuple[int, int, int, int, int, int]:
    s1, s2, _ = space
    stabilizer = span_set([s1, s2])
    central = [v for v in range(1, 256) if symp(v, s1) == 0 and symp(v, s2) == 0]
    z1 = next(v for v in central if v not in stabilizer)
    z2 = next(v for v in central if v not in span_set([s1, s2, z1]) and symp(v, z1) == 0)
    x1 = next(v for v in central if symp(v, z1) == 1 and symp(v, z2) == 0)
    x2 = next(v for v in central if symp(v, z1) == 0 and symp(v, z2) == 1 and symp(v, x1) == 0)
    assert len(span_set([s1, s2, z1, z2, x1, x2])) == 64
    return s1, s2, z1, z2, x1, x2


def code_basis(space: tuple[int, int, int], signs: tuple[int, int]) -> np.ndarray:
    s1, s2, z1, z2, x1, x2 = logical_completion(space)
    proj = I16.copy()
    for check, sign in zip((s1, s2), signs):
        proj = proj @ ((I16 + sign * PAULI[check]) / 2)
    for logical_z in (z1, z2):
        proj = proj @ ((I16 + PAULI[logical_z]) / 2)
    norms = np.linalg.norm(proj, axis=0)
    col = int(np.argmax(norms))
    v00 = proj[:, col] / norms[col]
    basis = np.column_stack([v00, PAULI[x2] @ v00, PAULI[x1] @ v00, PAULI[x1] @ PAULI[x2] @ v00])
    assert np.max(np.abs(basis.conj().T @ basis - np.eye(4))) < 1e-8
    return basis


def label(v: int) -> str:
    x, z = v & 15, (v >> 4) & 15
    out = []
    for q in range(4):
        xb, zb = (x >> q) & 1, (z >> q) & 1
        out.append("I" if not xb and not zb else "X" if xb and not zb else "Z" if zb and not xb else "Y")
    return "".join(out)


def build() -> dict:
    cliffords, clifford_words = two_qubit_clifford()
    rays, metadata = m36_rays()
    ray_orbit = {canon_state(u @ ray) for u in cliffords for ray in rays}

    # Four Clifford-orbit representatives inside M36.
    representative_meta = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 2)]
    inputs = []
    for meta in representative_meta:
        psi = rays[metadata.index(meta)]
        psi2 = np.kron(psi, psi)
        single = np.outer(psi, psi.conj())
        delta = np.eye(4) / 4 - single
        first_order = np.kron(delta, single) + np.kron(single, delta)
        inputs.append((meta, psi2, first_order))

    retained: list[tuple[float, float, tuple[int, int, int], tuple[int, int], tuple[int, int, int], np.ndarray]] = []
    for space in isotropic_rank2_subspaces():
        for signs in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            basis = code_basis(space, signs)
            bd = basis.conj().T
            for meta, psi2, first_order in inputs:
                decoded = bd @ psi2
                success0 = float(np.vdot(decoded, decoded).real)
                if success0 < 1e-10:
                    continue
                ideal = decoded / math.sqrt(success0)
                if canon_state(ideal) not in ray_orbit:
                    continue
                e1 = bd @ first_order @ basis
                success1 = float(np.trace(e1).real)
                numerator1 = float(np.vdot(ideal, e1 @ ideal).real)
                infidelity_slope = (success1 - numerator1) / success0
                retained.append((infidelity_slope, success0, space, signs, meta, ideal))

    assert len(retained) == 9264
    improving = [x for x in retained if x[0] < 0.75 - 1e-9]
    optimal = [x for x in retained if abs(x[0] - 0.5) < 1e-9]
    assert len(improving) == 48 and len(optimal) == 12

    chosen = next(x for x in optimal if label(x[2][0]) == "IYYX" and label(x[2][1]) == "YXIY")
    slope, success0, space, signs, input_meta, ideal = chosen
    completion = logical_completion(space)

    # Find a shortest logical Clifford carrying the decoded ideal state to an M36 ray.
    correction = None
    for key, word in sorted(clifford_words.items(), key=lambda kv: (len(kv[1]), kv[1])):
        u = next(u for u in cliffords if canon_unitary(u) == key)
        out = u @ ideal
        for target_meta, target in zip(metadata, rays):
            if abs(np.vdot(target, out)) ** 2 > 1 - 1e-9:
                correction = {"matrix_word_product": word, "target_ray": list(target_meta)}
                break
        if correction:
            break
    assert correction is not None

    # Exact white-noise map for the selected protocol.
    # Input rho_p=(1-p)|m><m|+p I/4.
    # Psucc=(p^2-2p+2)/4, Fout=(5p^2-12p+8)/(4(p^2-2p+2)).
    return {
        "schema": "w33.pass2784.m36_two_copy_distillation.v1",
        "status": "EXACT_EXHAUSTIVE_TWO_COPY_SEARCH",
        "search": {
            "rank2_isotropic_stabilizer_subspaces": 5355,
            "syndromes_per_subspace": 4,
            "m36_clifford_orbit_representatives": 4,
            "protocol_instances": 5355 * 4 * 4,
            "m36_closed_instances": len(retained),
            "strictly_distilling_instances": len(improving),
            "optimal_instances": len(optimal),
            "best_output_infidelity_slope_in_p": slope,
            "input_infidelity_slope_in_p": 0.75,
        },
        "selected_protocol": {
            "input_ray": list(input_meta),
            "input_vector": "(0,1,-omega,omega^2)/sqrt(3)",
            "checks": [label(space[0]), label(space[1])],
            "accepted_eigenvalues": list(signs),
            "logical_Z": [label(completion[2]), label(completion[3])],
            "logical_X": [label(completion[4]), label(completion[5])],
            "ideal_success_probability": success0,
            "logical_clifford_correction": correction,
            "success_probability": "(p^2-2p+2)/4",
            "output_fidelity": "(5p^2-12p+8)/(4*(p^2-2p+2))",
            "output_infidelity": "p*(4-p)/(4*(p^2-2p+2))",
            "distillation_region": "0<p<2/3",
            "equivalent_input_fidelity_threshold": "F_in>1/2",
            "fixed_points_in_p": [0, 2 / 3, 1],
        },
        "scope_boundary": (
            "This is exhaustive for two-copy binary [[4,2]] stabilizer projections, all syndromes, "
            "and the four two-qubit Clifford orbits represented inside M36. It is not an exhaustive "
            "classification of arbitrary multi-copy ququart stabilizer protocols."
        ),
    }


def main() -> None:
    out = build()
    path = ROOT / "data" / "PART_BT2784_M36_TWO_COPY_DISTILLATION.json"
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
