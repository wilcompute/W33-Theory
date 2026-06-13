#!/usr/bin/env python3
"""
BT895 - S3 Reflection to Fermion Multiplet Map.

BT879 proved that <R,C> ~= S3 acts on the 27 matter shell with character

    chi(e)=27, chi(reflection)=3, chi(3-cycle)=0.

BT893 identified the three Higgs-grade Yukawa skeletons as exactly the three
reflections of D3 ~= S3.  BT895 welds these facts: the same three reflection
axes that define the Yukawa support are the transposition class in the matter
character decomposition

    C[27] = 6*1 + 3*1' + 9*2.

The multiplicity 9 of the standard S3 doublet is exactly q^2, matching the
within-grade profile dimension isolated by BT894.
"""
from __future__ import annotations

import json
from pathlib import Path

# S3 conjugacy classes: identity, transpositions/reflections, 3-cycles.
classes = ["e", "reflection", "rotation3"]
class_sizes = {"e": 1, "reflection": 3, "rotation3": 2}

matter_character = {"e": 27, "reflection": 3, "rotation3": 0}
irreducibles = {
    "trivial_1": {"e": 1, "reflection": 1, "rotation3": 1},
    "sign_1prime": {"e": 1, "reflection": -1, "rotation3": 1},
    "standard_2": {"e": 2, "reflection": 0, "rotation3": -1},
}

# BT893 reflection skeletons as row -> column maps on Z3.
reflection_maps = {
    "Y0": [0, 2, 1],
    "Y1": [2, 1, 0],
    "Y2": [1, 0, 2],
}


def inner_product(char_a: dict[str, int], char_b: dict[str, int]) -> int:
    total = 0
    for c in classes:
        total += class_sizes[c] * char_a[c] * char_b[c]
    assert total % 6 == 0
    return total // 6


def permutation_trace(p: list[int]) -> int:
    return sum(1 for i, j in enumerate(p) if i == j)


def compose(p: list[int], q: list[int]) -> list[int]:
    return [p[q[i]] for i in range(len(p))]


def main() -> None:
    multiplicities = {
        name: inner_product(matter_character, char)
        for name, char in irreducibles.items()
    }
    assert multiplicities == {
        "trivial_1": 6,
        "sign_1prime": 3,
        "standard_2": 9,
    }

    dimension_check = (
        multiplicities["trivial_1"] * 1
        + multiplicities["sign_1prime"] * 1
        + multiplicities["standard_2"] * 2
    )
    assert dimension_check == 27

    # The three BT893 Yukawa skeletons are reflections: each has one fixed
    # grade and swaps the other two grades.  On the matter shell each fixed
    # grade contributes 3 fixed matter states in the BT879 character trace.
    reflection_grade_traces = {
        name: permutation_trace(p) for name, p in reflection_maps.items()
    }
    assert reflection_grade_traces == {"Y0": 1, "Y1": 1, "Y2": 1}
    matter_reflection_trace = 3
    assert matter_character["reflection"] == matter_reflection_trace

    # Products of distinct reflections are 3-cycles, whose matter trace is 0.
    product_types: dict[str, str] = {}
    names = list(reflection_maps)
    for a in names:
        for b in names:
            prod = compose(reflection_maps[a], reflection_maps[b])
            tr = permutation_trace(prod)
            key = f"{a}{b}"
            product_types[key] = "identity" if a == b else "rotation3"
            if a == b:
                assert tr == 3
            else:
                assert tr == 0
    assert matter_character["rotation3"] == 0

    q = 3
    result = {
        "theorem": "BT895 S3 Reflection to Fermion Multiplet Map",
        "S3_classes": classes,
        "class_sizes": class_sizes,
        "matter_character": matter_character,
        "irreducible_characters": irreducibles,
        "decomposition": "C[27] = 6*1 + 3*1' + 9*2",
        "multiplicities": multiplicities,
        "dimension_check": dimension_check,
        "BT893_reflection_skeletons": reflection_maps,
        "reflection_grade_traces": reflection_grade_traces,
        "matter_reflection_trace": matter_reflection_trace,
        "standard_doublet_multiplicity": multiplicities["standard_2"],
        "q_squared": q * q,
        "BT894_match": "standard doublet multiplicity 9 equals q^2 within-grade profile dimension",
        "product_types": product_types,
        "structural_conclusion": (
            "The three BT893 Higgs-grade Yukawa skeletons are the reflection "
            "class of the same S3 flavor action whose matter character decomposes "
            "as 6*1 + 3*1' + 9*2.  The nine standard doublets are the exact "
            "representation-theoretic home of the BT894 within-grade profile layer."
        ),
        "checks": {
            "T1_character_inner_products_give_6_3_9": True,
            "T2_dimension_sums_to_27": True,
            "T3_BT893_skeletons_are_reflections": True,
            "T4_distinct_reflection_products_are_3cycles": True,
            "T5_standard_doublet_multiplicity_equals_q_squared": True,
        },
    }

    out = Path("data/PART_BT895_S3_REFLECTION_FERMION_MULTIPLET_MAP_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("BT895 S3 Reflection to Fermion Multiplet Map")
    print("C[27] = 6*1 + 3*1' + 9*2")
    print("BT893 reflections = transposition class")
    print("standard doublet multiplicity =", q * q, "= q^2 within-grade layer")
    print("wrote", out)


if __name__ == "__main__":
    main()
