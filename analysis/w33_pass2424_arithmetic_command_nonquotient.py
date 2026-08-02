#!/usr/bin/env python3
"""Pass 2424: minimal and full identity-word obstruction to arithmetic phase descent."""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
TRICHOTOMY = ROOT / "data" / "w33_pass2306_controller_representation_trichotomy.json"
HARDWARE = ROOT / "data" / "w33_pass2313_theorem_hardware_contract.json"
OUT = ROOT / "data" / "w33_pass2424_arithmetic_command_nonquotient.json"
EXPECTED = "TO_BE_FROZEN"

R = ((0, -1, 0), (1, 0, 0), (0, 0, 1))
U = ((1, 0, 0), (0, 0, 1), (0, -1, 1))
I = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
INVERSE = {"R": "r", "r": "R", "U": "u", "u": "U"}


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def mpow(a, n):
    if n < 0:
        order = 4 if a == R else 6
        n %= order
    z = I
    while n:
        if n & 1:
            z = mm(z, a)
        a = mm(a, a)
        n //= 2
    return z


def digest(d):
    x = dict(d)
    x.pop("sha256_without_hash_field", None)
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def reduced_words(n):
    alphabet = "RrUu"
    def rec(prefix):
        if len(prefix) == n:
            yield prefix
            return
        for c in alphabet:
            if prefix and INVERSE[prefix[-1]] == c:
                continue
            yield from rec(prefix + c)
    yield from rec("")


def evaluate(word):
    matrices = {"R": R, "r": mpow(R, -1), "U": U, "u": mpow(U, -1)}
    increments = {"R": 3, "r": -3, "U": 2, "u": -2}
    z, phase = I, 0
    for c in word:
        z = mm(z, matrices[c])
        phase = (phase + increments[c]) % 12
    return z, phase


def inverse_word(word):
    return "".join(INVERSE[c] for c in reversed(word))


def free_reduce(word):
    stack = []
    for c in word:
        if stack and INVERSE[stack[-1]] == c:
            stack.pop()
        else:
            stack.append(c)
    return "".join(stack)


def dihedral_word_orbits(words):
    universe = set(words)
    orbits = []
    while universe:
        w = min(universe)
        rotations = {w[i:] + w[:i] for i in range(len(w))}
        iw = inverse_word(w)
        rotations |= {iw[i:] + iw[:i] for i in range(len(iw))}
        orbit = sorted(rotations & universe)
        orbits.append(orbit)
        universe -= set(orbit)
    return orbits


def half_ball(max_length):
    """Map exact matrices to shortest words by command phase through max_length."""
    reps = defaultdict(dict)
    matrix, phase = evaluate("")
    reps[matrix][phase] = ""
    for n in range(1, max_length + 1):
        for word in reduced_words(n):
            matrix, phase = evaluate(word)
            old = reps[matrix].get(phase)
            if old is None or (len(word), word) < (len(old), old):
                reps[matrix][phase] = word
    return reps


def build():
    tri = json.loads(TRICHOTOMY.read_text())
    hw = json.loads(HARDWARE.read_text())
    assert tri["sha256_without_hash_field"] == "b4c9da10fa1320f58b916a145fa8048a8aef095b41041c1a080b137fd301a41b"
    assert hw["sha256_without_hash_field"] == "631638ab847f20d6e39124624f1e40850ac4992d7f70e42a900c125b76141574"

    relation_left = mm(mpow(U, 3), R)
    relation_right = mm(mpow(R, -1), mpow(U, 3))
    obstruction_word = "UUURuuuR"
    obstruction_matrix, obstruction_phase = evaluate(obstruction_word)

    defect_counts = {}
    shortest = []
    for n in range(1, 9):
        hits = []
        for word in reduced_words(n):
            matrix, phase = evaluate(word)
            if matrix == I and phase != 0:
                hits.append((word, phase))
        defect_counts[str(n)] = len(hits)
        if hits and not shortest:
            shortest = hits
    shortest_words = [w for w, _ in shortest]
    shortest_phases = sorted({p for _, p in shortest})
    word_orbits = dihedral_word_orbits(shortest_words)

    # Meet in the middle: any identity word of length <=16 splits into two
    # words of length <=8 representing the same matrix.  Phase differences in
    # this table therefore exhaust all identity phases through length 16.
    halves = half_ball(8)
    phase_differences = set()
    for by_phase in halves.values():
        phases = list(by_phase)
        phase_differences.update((a - b) % 12 for a in phases for b in phases)
    phase_differences.discard(0)

    phase_one_word = "RRUruRuRuruRuRurU"
    phase_one_matrix, phase_one_value = evaluate(phase_one_word)

    x = sp.symbols("x")
    Rs, Us = sp.Matrix(R), sp.Matrix(U)
    charpolys = {
        "R4_U6_squared_plastic": str(sp.factor((Rs * Us**2).charpoly(x).as_expr())),
        "R4_U6_supergolden": str(sp.factor((Rs * Us).charpoly(x).as_expr())),
        "R4_squared_U6_golden": str(sp.factor((Rs**2 * Us).charpoly(x).as_expr())),
    }

    checks = {
        "R_order_4": mpow(R, 4) == I and mpow(R, 2) != I,
        "U_order_6": mpow(U, 6) == I and mpow(U, 3) != I,
        "exact_inversion_relation": relation_left == relation_right,
        "obstruction_word_is_identity": obstruction_matrix == I,
        "obstruction_phase_is_half_turn": obstruction_phase == 6,
        "no_defect_below_length_8": all(defect_counts[str(n)] == 0 for n in range(1, 8)),
        "exactly_32_shortest_defects": defect_counts["8"] == 32,
        "all_shortest_defects_phase_6": shortest_phases == [6],
        "three_cyclic_inverse_word_shapes": len(word_orbits) == 3 and sorted(map(len, word_orbits)) == [8, 8, 16],
        "phase_one_absent_through_length_16": 1 not in phase_differences,
        "phase_one_identity_at_length_17": len(phase_one_word) == 17 and phase_one_matrix == I and phase_one_value == 1,
        "full_C12_identity_holonomy": math_gcd(phase_one_value, 12) == 1,
        "short_word_polynomials": charpolys == {"R4_U6_squared_plastic": "x**3 - x - 1", "R4_U6_supergolden": "x**3 - x**2 - 1", "R4_squared_U6_golden": "(x + 1)*(x**2 - x - 1)"},
        "hardware_kernel_matches_single_J": hw["phase_controller"]["delta_kernel"] == [[0, 0], [2, 3]],
    }
    assert all(checks.values())

    d = {
        "schema": "w33.pass2424.arithmetic_command_nonquotient.v1",
        "status": "PASS_MINIMAL_DEFECT_AND_FULL_C12_IDENTITY_HOLONOMY",
        "sources": {
            "controller_trichotomy": {"path": str(TRICHOTOMY.relative_to(ROOT)), "sha256_without_hash_field": tri["sha256_without_hash_field"]},
            "hardware_contract": {"path": str(HARDWARE.relative_to(ROOT)), "sha256_without_hash_field": hw["sha256_without_hash_field"]},
        },
        "arithmetic_generators": {"R4": [list(r) for r in R], "U6": [list(r) for r in U], "generated_group": "SL3(Z) by Passes 1942/1953"},
        "finite_command_label": {"R4_increment": 3, "U6_increment": 2, "phase_modulus": 12, "abstract_map": "(a,b)->3a+2b mod 12", "single_J_kernel": [[0, 0], [2, 3]]},
        "first_exact_relation": {"matrix_equation": "U6^3 R4 = R4^-1 U6^3", "identity_word": obstruction_word, "identity_word_matrix": "I3", "hardware_phase": obstruction_phase},
        "minimality_search": {
            "alphabet": ["R", "R^-1", "U", "U^-1"],
            "freely_reduced_word_counts_checked_through_length": 8,
            "nonzero_phase_identity_counts_by_length": defect_counts,
            "shortest_length": 8,
            "shortest_word_count": len(shortest_words),
            "shortest_phase_support": shortest_phases,
            "cyclic_inverse_orbits": word_orbits,
            "cyclic_inverse_orbit_sizes": sorted(map(len, word_orbits)),
        },
        "full_holonomy_witness": {
            "meet_in_middle_identity_phase_support_through_length_16": sorted(phase_differences),
            "phase_one_absent_through_length": 16,
            "phase_one_word": phase_one_word,
            "phase_one_word_length": len(phase_one_word),
            "phase_one_word_matrix": "I3",
            "phase_one_word_phase": phase_one_value,
            "consequence": "Concatenating this identity word realizes every element of C12 as path holonomy while leaving the arithmetic matrix unchanged.",
        },
        "short_word_characteristic_polynomials": charpolys,
        "checks": checks,
        "theorem": "The exponent-sum phase map R4->3, U6->2 mod 12 does not descend from <R4,U6>=SL3(Z). The shortest failure has length eight and phase 6; the first phase-1 identity has length seventeen, proving that matrix-identity words realize the full C12 phase group.",
        "interpretation": "The phase is path/word holonomy for the overlapping arithmetic carrier, not a function of the resulting SL3(Z) matrix. A single duo bit captures the first defect but cannot globally repair relation-blind compilation; the full C12 holonomy or the original word path must be retained.",
        "boundary": "No finite hardware semantic contract is refuted. The result forbids only matrix-only rewriting followed by exponent-total phase emission and any identification of the current single-J image as a quotient representation of the overlapping arithmetic group.",
    }
    d["sha256_without_hash_field"] = digest(d)
    return d


def math_gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def main():
    d = build()
    if EXPECTED != "TO_BE_FROZEN":
        assert d["sha256_without_hash_field"] == EXPECTED
        assert d == json.loads(OUT.read_text())
    print(json.dumps({"status": d["status"], "certificate": d["sha256_without_hash_field"], "shortest_defect": 8, "phase_one_length": 17}, sort_keys=True))


if __name__ == "__main__":
    main()
