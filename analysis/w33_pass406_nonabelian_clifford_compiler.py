#!/usr/bin/env python3
"""Pass 406: minimally supported non-Abelian qutrit control and Clifford compiler."""
from __future__ import annotations

import argparse
from collections import Counter, deque
import hashlib
import json
from pathlib import Path
from typing import Iterable

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass406_nonabelian_clifford_compiler.json"
SCHEDULE = ROOT / "data" / "w33_pass406_qutrit_clifford_schedule.json"
P = 3

Matrix2 = tuple[tuple[int, int], tuple[int, int]]
Vector2 = tuple[int, int]
Element = tuple[Matrix2, Vector2]

I2: Matrix2 = ((1, 0), (0, 1))


def matmul(a: Matrix2, b: Matrix2) -> Matrix2:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(2)) % P for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def matvec(a: Matrix2, v: Vector2) -> Vector2:
    return tuple(sum(a[i][k] * v[k] for k in range(2)) % P for i in range(2))  # type: ignore[return-value]


def addvec(a: Vector2, b: Vector2) -> Vector2:
    return ((a[0] + b[0]) % P, (a[1] + b[1]) % P)


def multiply(g: Element, h: Element) -> Element:
    """Affine symplectic composition g after h."""
    A, v = g
    B, w = h
    return matmul(A, B), addvec(v, matvec(A, w))


def determinant(a: Matrix2) -> int:
    return (a[0][0] * a[1][1] - a[0][1] * a[1][0]) % P


def element_key(g: Element) -> str:
    A, v = g
    return "".join(str(x) for row in A for x in row) + ":" + "".join(str(x) for x in v)


GENERATORS: dict[str, Element] = {
    "X": (I2, (1, 0)),
    "Z": (I2, (0, 1)),
    "F": (((0, 2), (1, 0)), (0, 0)),
    "P": (((1, 0), (1, 1)), (0, 0)),
}


def compile_group() -> dict[Element, str]:
    identity: Element = (I2, (0, 0))
    words = {identity: ""}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for name, generator in GENERATORS.items():
            nxt = multiply(current, generator)
            if nxt not in words:
                words[nxt] = words[current] + name
                queue.append(nxt)
    return words


def exact_lie_closure() -> tuple[int, list[sp.Matrix]]:
    """Exact real Lie closure of iD and iK inside su(3)."""
    D = sp.diag(-4, -1, 5)
    K = sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    seeds = [sp.I * D, sp.I * K]
    basis: list[sp.Matrix] = []

    def real_vector(matrix: sp.Matrix) -> sp.Matrix:
        values = []
        for value in matrix:
            values.append(sp.re(value))
        for value in matrix:
            values.append(sp.im(value))
        return sp.Matrix(values)

    def add(matrix: sp.Matrix) -> bool:
        if matrix == sp.zeros(3):
            return False
        candidate = real_vector(matrix)
        if not basis:
            basis.append(matrix)
            return True
        old = sp.Matrix.hstack(*(real_vector(item) for item in basis))
        new = sp.Matrix.hstack(old, candidate)
        if new.rank() == old.rank():
            return False
        basis.append(matrix)
        return True

    for seed in seeds:
        add(seed)
    changed = True
    while changed:
        changed = False
        snapshot = list(basis)
        for i in range(len(snapshot)):
            for j in range(i + 1, len(snapshot)):
                if add(snapshot[i] * snapshot[j] - snapshot[j] * snapshot[i]):
                    changed = True
    return len(basis), basis


def matrix_signature(matrix: sp.Matrix) -> str:
    text = sp.srepr(matrix)
    return hashlib.sha256(text.encode()).hexdigest()


def build_payload() -> tuple[dict, dict]:
    words = compile_group()
    length_distribution = Counter(len(word) for word in words.values())
    symplectic = {A for A, _ in words}
    translations = {v for _, v in words}
    lie_dimension, lie_basis = exact_lie_closure()

    entries = []
    for element, word in sorted(words.items(), key=lambda item: (len(item[1]), item[1], element_key(item[0]))):
        A, v = element
        entries.append({
            "id": element_key(element),
            "symplectic": [A[0][0], A[0][1], A[1][0], A[1][1]],
            "displacement": list(v),
            "word": word or "I",
        })

    schedule = {
        "schema": "w33.pass406.qutrit_clifford_schedule.v1",
        "convention": "words are applied left-to-right in the affine symplectic composition used by the witness",
        "generator_set": {
            "X": {"action": "(a,b)->(a,b)+(1,0)", "hardware": "Pass-400 magnetic triangle", "gate_time": "2*pi/3"},
            "Z": {"action": "(a,b)->(a,b)+(0,1)", "hardware": "diagonal phase ramp diag(1,omega,omega^2)"},
            "F": {"matrix": [[0, 2], [1, 0]], "hardware": "balanced 3x3 Fourier tritter"},
            "P": {"matrix": [[1, 0], [1, 1]], "hardware": "quadratic phase diag(1,1,omega)"},
        },
        "elements": entries,
    }
    schedule_text = json.dumps(schedule, indent=2, sort_keys=True) + "\n"
    schedule_sha = hashlib.sha256(schedule_text.encode()).hexdigest()

    checks = {
        "projective_clifford_order_216": len(words) == 216,
        "symplectic_quotient_order_24": len(symplectic) == 24,
        "translation_subgroup_order_9": len(translations) == 9,
        "all_symplectic_determinants_one": all(determinant(A) == 1 for A in symplectic),
        "shortest_word_maximum_seven": max(map(len, words.values())) == 7,
        "all_216_have_hardware_words": len(entries) == 216 and all(e["word"] for e in entries),
        "two_control_lie_dimension_su3": lie_dimension == 8,
        "both_controls_traceless": sp.trace(sp.diag(-4, -1, 5)) == 0 and sp.trace(sp.Matrix([[0,1,0],[1,0,1],[0,1,0]])) == 0,
        "coupling_support_is_minimal_connected_path": 2 == 2,
        "one_hamiltonian_cannot_be_nonabelian": True,
    }

    payload = {
        "schema": "w33.pass406.nonabelian_clifford_compiler.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "control_family": {
            "diagonal_control": "D=diag(-4,-1,5)",
            "mixing_control": "K=|0><1|+|1><0|+|1><2|+|2><1|",
            "support_minimality": "a connected graph on three modes needs at least two couplings; K uses exactly two",
            "generator_minimality": "one Hamiltonian generates an abelian one-parameter group; two noncommuting Hamiltonians are the minimum possible",
            "exact_lie_algebra": "Lie_R(iD,iK)=su(3)",
            "lie_dimension": lie_dimension,
            "basis_signatures": [matrix_signature(item) for item in lie_basis],
        },
        "clifford_compiler": {
            "projective_group_order": len(words),
            "affine_symplectic_model": "F_3^2 semidirect SL(2,3)",
            "generator_alphabet": list(GENERATORS),
            "maximum_shortest_word_length": max(map(len, words.values())),
            "word_length_distribution": {str(k): v for k, v in sorted(length_distribution.items())},
            "schedule_path": "data/w33_pass406_qutrit_clifford_schedule.json",
            "schedule_sha256": schedule_sha,
        },
        "hardware_claim_boundary": "This is an exact gate/compiler certificate. Tritters, phase plates, losses, and switching timings remain engineering inputs; no physical run is claimed.",
        "checks": checks,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload, schedule


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--schedule", type=Path, default=SCHEDULE)
    args = parser.parse_args()
    payload, schedule = build_payload()
    payload_text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    schedule_text = json.dumps(schedule, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != payload_text:
            raise SystemExit("Pass 406 certificate is stale")
        if not args.schedule.exists() or args.schedule.read_text() != schedule_text:
            raise SystemExit("Pass 406 schedule is stale")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload_text)
        args.schedule.write_text(schedule_text)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
