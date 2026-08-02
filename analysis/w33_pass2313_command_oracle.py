#!/usr/bin/env python3
"""Pass 2313: exhaustive theorem-derived oracle for the packed D24 controller.

The oracle is independent of the RTL implementation.  It enumerates the full
1152-case input space of w33_single_j_action24 and certifies the two-to-one
C4 x C6 -> C12 command quotient, including its central duo kernel.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


def h(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def delta(a: int, b: int) -> int:
    return (3 * a + 2 * b) % 12


def action(phase: int, conjugated: int, a: int, b: int, reflect: int) -> tuple[int, int]:
    d = delta(a, b)
    out = (phase + d) % 12 if not conjugated else (phase - d) % 12
    return out, conjugated ^ reflect


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-json", type=Path)
    ap.add_argument("--write-vectors", type=Path)
    args = ap.parse_args()

    fibers = {d: [] for d in range(12)}
    for a in range(4):
        for b in range(6):
            fibers[delta(a, b)].append((a, b))
    kernel = fibers[0]
    assert kernel == [(0, 0), (2, 3)]
    assert all(len(v) == 2 for v in fibers.values())
    assert all(delta((a + 2) % 4, (b + 3) % 6) == delta(a, b) for a in range(4) for b in range(6))

    vectors = []
    for phase in range(12):
        for conjugated in range(2):
            for a in range(4):
                for b in range(6):
                    for reflect in range(2):
                        po, co = action(phase, conjugated, a, b, reflect)
                        vectors.append([phase, conjugated, a, b, reflect, po, co])
    assert len(vectors) == 1152

    # D24 action law on (phase, conjugation) with command (delta, reflect).
    def compose(c1, c2):
        d1, e1 = c1
        d2, e2 = c2
        return ((d1 + (-d2 if e1 else d2)) % 12, e1 ^ e2)

    group_checks = 0
    for d1 in range(12):
        for e1 in range(2):
            for d2 in range(12):
                for e2 in range(2):
                    for d3 in range(12):
                        for e3 in range(2):
                            assert compose(compose((d1, e1), (d2, e2)), (d3, e3)) == compose((d1, e1), compose((d2, e2), (d3, e3)))
                            group_checks += 1

    out = {
        "schema": "w33.pass2313.command_oracle.v1",
        "status": "PASS_EXHAUSTIVE_THEOREM_DERIVED_COMMAND_ORACLE",
        "input_cases": len(vectors),
        "truth_table_sha256": hashlib.sha256("\n".join(",".join(map(str, row)) for row in vectors).encode()).hexdigest(),
        "delta_fibers": {str(d): [list(x) for x in fibers[d]] for d in range(12)},
        "kernel": [list(x) for x in kernel],
        "duo_translation": "(a,b)->(a+2 mod 4,b+3 mod 6)",
        "d24_associativity_cases": group_checks,
        "checks": {
            "c4xc6_domain_size_24": sum(map(len, fibers.values())) == 24,
            "c12_surjective": all(fibers[d] for d in range(12)),
            "every_phase_has_two_preimages": all(len(v) == 2 for v in fibers.values()),
            "kernel_is_central_duo_pair": kernel == [(0, 0), (2, 3)],
            "duo_translation_preserves_delta": True,
            "all_1152_rtl_input_cases_generated": len(vectors) == 1152,
            "d24_group_law_exhaustive": group_checks == 24**3,
        },
        "theorem": "The packed command coordinates form a two-to-one quotient C4 x C6 -> C12 with kernel {(0,0),(2,3)}. Adding the independent reflection bit gives the standard D24 action on twelve phases and a conjugation bit.",
        "boundary": "This is the finite hardware command algebra. Pass 2314 tests whether it descends from the infinite arithmetic matrix group; it does not.",
    }
    out["sha256_without_hash_field"] = h(out)
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.write_json:
        args.write_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_json.write_text(text)
    if args.write_vectors:
        args.write_vectors.parent.mkdir(parents=True, exist_ok=True)
        args.write_vectors.write_text("phase,conjugated,step4,step6,reflect,phase_out,conjugated_out\n" + "\n".join(",".join(map(str, row)) for row in vectors) + "\n")
    print(text, end="")


if __name__ == "__main__":
    main()
