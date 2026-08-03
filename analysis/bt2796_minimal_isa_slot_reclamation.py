#!/usr/bin/env python3
"""Pass 2796: exact minimal generating sets for the Holonet frame machine."""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Q = 3
I = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))

FP = ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
FF = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0))
SP = ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
SF = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1))
CXPF = ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1))
CXFP = ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))
GENS = {"F_p": FP, "F_f": FF, "S_p": SP, "S_f": SF, "CX_pf": CXPF, "CX_fp": CXFP}
ZP = (0, 1, 0, 0)


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % Q for j in range(4)) for i in range(4))


def mv(a, v):
    return tuple(sum(a[i][k] * v[k] for k in range(4)) % Q for i in range(4))


def closure(gens):
    seen = {I}
    queue = deque([I])
    while queue:
        x = queue.popleft()
        for g in gens:
            y = mm(g, x)
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return seen


def bfs_lengths(gens):
    distance = {I: 0}
    queue = deque([I])
    while queue:
        x = queue.popleft()
        for g in gens:
            y = mm(g, x)
            if y not in distance:
                distance[y] = distance[x] + 1
                queue.append(y)
    return distance


def vector_span(vectors):
    span = {(0, 0, 0, 0)}
    for v in vectors:
        span |= {tuple((x[i] + a * v[i]) % 3 for i in range(4)) for x in tuple(span) for a in (1, 2)}
    return span


def main():
    names = list(GENS)
    full_pairs = []
    for r in range(1, len(names) + 1):
        for subset in itertools.combinations(names, r):
            if len(closure([GENS[name] for name in subset])) == 51840:
                full_pairs.append(subset)
        if full_pairs:
            minimum = r
            break

    family_gens = {
        "F_p": [FP], "F_f": [FF], "S_p": [SP], "S_f": [SF], "CX": [CXPF, CXFP]
    }
    minimum_families = []
    for r in range(1, 6):
        for subset in itertools.combinations(family_gens, r):
            expanded = [g for name in subset for g in family_gens[name]]
            if len(closure(expanded)) == 51840:
                minimum_families.append(subset)
        if minimum_families:
            family_minimum = r
            break

    compiler_basis = [FP, CXPF, CXFP]
    lengths = bfs_lengths(compiler_basis)
    assert len(lengths) == 51840
    distribution = Counter(lengths.values())
    sp_group = set(lengths)
    orbit = {mv(g, ZP) for g in sp_group}
    translation_span = vector_span(orbit)

    checks = {
        "individual_minimum_three": minimum == 3,
        "six_minimal_triples": len(full_pairs) == 6,
        "family_minimum_two": family_minimum == 2,
        "fp_cx_family_generates_sp43": ("F_p", "CX") in minimum_families,
        "ff_cx_family_generates_sp43": ("F_f", "CX") in minimum_families,
        "compiler_basis_order_51840": len(lengths) == 51840,
        "one_translation_orbit_80": len(orbit) == 80,
        "one_translation_span_81": len(translation_span) == 81,
        "affine_order_4199040": len(lengths) * len(translation_span) == 4199040,
    }
    assert all(checks.values())

    output = {
        "schema": "w33.pass2796.minimal_affine_frame_isa.v1",
        "status": "EXACT",
        "individual_generator_minimum": minimum,
        "minimal_individual_generating_sets": [list(x) for x in full_pairs],
        "opcode_family_minimum": family_minimum,
        "minimal_opcode_family_sets": [list(x) for x in minimum_families],
        "selected_micro_isa": ["F_p", "CX_pf", "CX_fp", "Z_p"],
        "linear_order": len(lengths),
        "translation_orbit_nonzero": len(orbit),
        "translation_span": len(translation_span),
        "affine_order": len(lengths) * len(translation_span),
        "word_length": {
            "mean": sum(lengths.values()) / len(lengths),
            "maximum": max(lengths.values()),
            "distribution": {str(k): distribution[k] for k in sorted(distribution)},
        },
        "hardware_boundary": "Removing Z_f removes the register-select subencoding, not an entire global 3-bit opcode. The new 2-bit micro-ISA is a compressed frame engine beneath the public Holonet ISA.",
        "checks": checks,
    }
    path = ROOT / "data/PART_BT2796_MINIMAL_AFFINE_FRAME_ISA_results.json"
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
