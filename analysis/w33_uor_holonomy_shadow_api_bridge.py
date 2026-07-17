#!/usr/bin/env python3
"""Dependency-light W33/UOR holonomy shadow bridge."""

from __future__ import annotations

import json
from itertools import permutations
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "w33_uor_holonomy_shadow_api_bridge.json"

Perm = tuple[int, int, int]
IDENTITY: Perm = (0, 1, 2)
GENERATORS: dict[str, Perm] = {
    "s0": (1, 0, 2),
    "s1": (0, 2, 1),
}


def compose(left: Perm, right: Perm) -> Perm:
    """Composition left after right."""
    return tuple(left[right[i]] for i in range(3))  # type: ignore[return-value]


def sign(perm: Perm) -> int:
    inversions = 0
    for i in range(3):
        for j in range(i + 1, 3):
            if perm[i] > perm[j]:
                inversions += 1
    return inversions % 2


def word_value(word: list[str]) -> Perm:
    value = IDENTITY
    for token in word:
        value = compose(GENERATORS[token], value)
    return value


def closure() -> set[Perm]:
    group = {IDENTITY, *GENERATORS.values()}
    changed = True
    while changed:
        changed = False
        for left in list(group):
            for right in list(group):
                product = compose(left, right)
                if product not in group:
                    group.add(product)
                    changed = True
    return group


def classify_perm(perm: Perm) -> str:
    if perm == IDENTITY:
        return "identity"
    fixed = sum(1 for idx, value in enumerate(perm) if idx == value)
    if fixed == 1:
        return "transposition"
    return "three_cycle"


def uor_holonomy_payload(word: list[str]) -> dict[str, Any]:
    codes = [0]
    codes.extend(1 if token == "s0" else 2 for token in word)
    codes.append(0)
    while len(codes) < 3:
        codes.append(0)
    return {"path": codes, "quantum": 1}


def build_bridge() -> dict[str, Any]:
    group = closure()
    all_s3 = set(permutations(range(3)))
    words = {
        "identity": [],
        "s0": ["s0"],
        "s1": ["s1"],
        "s0s1": ["s0", "s1"],
        "s1s0": ["s1", "s0"],
        "s0s1s0": ["s0", "s1", "s0"],
    }
    rows = []
    for name, word in words.items():
        perm = word_value(word)
        rows.append(
            {
                "word": name,
                "generators": word,
                "permutation": list(perm),
                "cycle_type": classify_perm(perm),
                "z2_shadow": sign(perm),
                "uor_holonomy_payload": uor_holonomy_payload(word),
            }
        )

    kernel = [perm for perm in group if sign(perm) == 0]
    coset = [perm for perm in group if sign(perm) == 1]
    bridge = {
        "schema": "w33.uor.holonomy_shadow_api_bridge.v1",
        "uor_endpoint": "https://uor.foundation/bridge/observable/holonomy",
        "native_transport_group": "Weyl(A2) ~= S3",
        "coefficient_shadow": "sign: S3 -> Z2",
        "checks": {
            "generated_group_order": len(group),
            "all_s3_generated": group == all_s3,
            "sign_kernel_order": len(kernel),
            "sign_coset_order": len(coset),
            "sign_surjective": bool(kernel and coset),
            "identity_and_three_cycles_conflated_by_z2": any(
                classify_perm(perm) == "three_cycle" and sign(perm) == 0
                for perm in group
            ),
            "transpositions_are_nontrivial_shadow": all(
                sign(perm) == 1
                for perm in group
                if classify_perm(perm) == "transposition"
            ),
        },
        "word_table": rows,
        "boundary": (
            "This verifies the coefficient-shadow bridge and emits UOR holonomy "
            "payloads. It does not re-run the older center-quad W33 transport "
            "atlas, which requires optional networkx/numpy stack dependencies."
        ),
    }
    checks = bridge["checks"]
    bridge["status"] = (
        "PASS"
        if (
            checks["generated_group_order"] == 6
            and checks["all_s3_generated"]
            and checks["sign_kernel_order"] == 3
            and checks["sign_coset_order"] == 3
            and checks["sign_surjective"]
            and checks["identity_and_three_cycles_conflated_by_z2"]
            and checks["transpositions_are_nontrivial_shadow"]
        )
        else "FAIL"
    )
    return bridge


def main(argv: list[str] | None = None) -> int:
    output = DEFAULT_OUTPUT
    if argv:
        output = Path(argv[0])
        if not output.is_absolute():
            output = ROOT / output
    bridge = build_bridge()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(bridge, indent=2), encoding="utf-8")
    print(f"status: {bridge['status']}")
    print(f"group order: {bridge['checks']['generated_group_order']}")
    print(
        f"kernel/coset: {bridge['checks']['sign_kernel_order']}/{bridge['checks']['sign_coset_order']}"
    )
    print(f"uor endpoint: {bridge['uor_endpoint']}")
    print(f"wrote: {output.relative_to(ROOT)}")
    return 0 if bridge["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
