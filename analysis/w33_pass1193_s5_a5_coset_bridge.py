#!/usr/bin/env python3
"""Pass 1193: exact S5/A5 stabilizer-intersection bridge on the 432 carriers."""
from __future__ import annotations

from collections import Counter, deque
import json
from pathlib import Path

import numpy as np

from w33_we6_exact_core import (
    a2_orbits,
    a2_triples,
    compose,
    e6_generators,
    group_invariants,
    permutation_order,
    we6_group,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1193_s5_a5_coset_bridge.json"


def group_with_reflection_parity() -> tuple[tuple[np.ndarray, ...], tuple[int, ...]]:
    """Enumerate W(E6) and its unique reflection-length parity character."""
    generators = e6_generators()
    identity = np.arange(240, dtype=np.uint8)
    elements = [identity]
    parity = [0]
    index = {identity.tobytes(): 0}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        x = elements[i]
        for generator in generators:
            y = compose(generator, x)
            key = y.tobytes()
            py = parity[i] ^ 1
            if key not in index:
                index[key] = len(elements)
                elements.append(y)
                parity.append(py)
                queue.append(len(elements) - 1)
            else:
                assert parity[index[key]] == py
    assert len(elements) == 51840
    reference = we6_group()
    assert {g.tobytes() for g in elements} == {g.tobytes() for g in reference}
    return tuple(elements), tuple(parity)


def fixes_triple(permutation: np.ndarray, triple: tuple[int, int, int]) -> bool:
    return tuple(sorted(int(permutation[x]) for x in triple)) == triple


def main() -> dict:
    triples = a2_triples()
    group, parity = group_with_reflection_parity()
    even_indices = [i for i, value in enumerate(parity) if value == 0]
    assert len(even_indices) == 25920

    records = []
    for orbit_number, orbit in enumerate(orb for orb in a2_orbits() if len(orb) == 432):
        representative = triples[orbit[0]]
        stabilizer_indices = [
            i for i, element in enumerate(group)
            if fixes_triple(element, representative)
        ]
        even_stabilizer = tuple(group[i] for i in stabilizer_indices if parity[i] == 0)
        odd_stabilizer_count = sum(parity[i] == 1 for i in stabilizer_indices)
        assert len(stabilizer_indices) == 120
        assert len(even_stabilizer) == odd_stabilizer_count == 60

        invariants = group_invariants(even_stabilizer)
        order_distribution = Counter(permutation_order(x) for x in even_stabilizer)
        assert order_distribution == Counter({1: 1, 2: 15, 3: 20, 5: 24})
        assert invariants["center_order"] == 1
        assert invariants["derived_order"] == 60
        assert invariants["abelianization_order"] == 1
        assert len(even_indices) // len(even_stabilizer) == 432

        records.append({
            "orbit_number": orbit_number,
            "orbit_size": 432,
            "representative_a2_triple": list(representative),
            "we6_stabilizer": {
                "order": 120,
                "identification": "S5 = SmallGroup(120,34)",
                "even_elements": 60,
                "odd_elements": 60,
            },
            "psp43_intersection": {
                **invariants,
                "element_order_distribution": dict(sorted(order_distribution.items())),
                "identification": "A5 = SmallGroup(60,5)",
            },
            "coset_models": {
                "we6_over_s5_index": 51840 // 120,
                "psp43_over_a5_index": 25920 // 60,
                "same_432_carrier": True,
            },
        })

    result = {
        "schema": "w33.pass1193.s5_a5_coset_bridge.v1",
        "status": "PASS",
        "headline": "Each 432-point W(E6)/S5 carrier restricts transitively to PSp(4,3)/A5, with S5 intersect PSp(4,3)=A5.",
        "orders": {"W(E6)": 51840, "PSp(4,3)": 25920, "S5": 120, "A5": 60},
        "normal_subgroup": {
            "definition": "kernel of reflection-length parity",
            "order": len(even_indices),
            "identification": "PSp(4,3)",
        },
        "records": records,
        "theorem": {
            "intersection": "S5 ∩ PSp(4,3) = A5",
            "coset_equivalence": "W(E6)/S5 ≅ PSp(4,3)/A5 as PSp(4,3)-sets",
            "index_identity": "51840/120 = 25920/60 = 432",
            "three_copies": len(records),
        },
        "checks": {
            "we6_order_51840": len(group) == 51840,
            "parity_kernel_order_25920": len(even_indices) == 25920,
            "three_432_orbits": len(records) == 3,
            "all_intersections_a5": all(r["psp43_intersection"]["order"] == 60 for r in records),
            "all_indices_432": all(r["coset_models"]["we6_over_s5_index"] == r["coset_models"]["psp43_over_a5_index"] == 432 for r in records),
        },
        "scope": "Exact finite permutation computation on the 240 E8 roots; the A5 identification uses order, perfectness, trivial center, and the A5 element-order census.",
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1193 W(E6)/S5 = PSp(4,3)/A5 on all three 432 carriers")
    return result


if __name__ == "__main__":
    main()
