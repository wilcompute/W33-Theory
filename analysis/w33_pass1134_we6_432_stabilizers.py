#!/usr/bin/env python3
"""Pass 1134: classify all three W(E6) stabilizers of the 432 A2-triple orbits."""
from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path

import numpy as np

from w33_we6_exact_core import (
    a2_orbits,
    a2_triples,
    compose,
    greedy_generators,
    group_invariants,
    inverse,
    we6_group,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1134_we6_432_stabilizers.json"


def fixes_triple(p: np.ndarray, triple: tuple[int, int, int]) -> bool:
    return tuple(sorted(int(p[x]) for x in triple)) == triple


def conjugacy_witness(source_gens, target_keys, group):
    for g in group:
        gi = inverse(g)
        if all(compose(g, compose(h, gi)).tobytes() in target_keys for h in source_gens):
            return g
    return None


def main() -> None:
    triples = a2_triples()
    group = we6_group()
    orbits432 = [orb for orb in a2_orbits() if len(orb) == 432]
    assert len(orbits432) == 3

    stabilizers = []
    records = []
    for orbit_index, orbit in enumerate(orbits432):
        representative = triples[orbit[0]]
        stab = tuple(p for p in group if fixes_triple(p, representative))
        assert len(stab) == 120
        inv = group_invariants(stab)
        assert inv["element_order_distribution"] == {1: 1, 2: 25, 3: 20, 4: 30, 5: 24, 6: 20}
        assert inv["center_order"] == 1
        assert inv["derived_order"] == 60
        assert inv["abelianization_order"] == 2
        records.append({
            "orbit_number": orbit_index,
            "orbit_size": len(orbit),
            "representative_a2_triple": list(representative),
            "stabilizer": {
                **inv,
                "small_group_identification": "S5 = SmallGroup(120,34)",
                "classification_reason": "order distribution {1:1,2:25,3:20,4:30,5:24,6:20}, trivial center, derived subgroup order 60, abelianization C2"
            }
        })
        stabilizers.append(stab)

    conjugacy = []
    for i, j in combinations(range(3), 2):
        source_gens = greedy_generators(stabilizers[i])
        target_keys = {x.tobytes() for x in stabilizers[j]}
        witness = conjugacy_witness(source_gens, target_keys, group)
        assert witness is not None
        conjugacy.append({
            "pair": [i, j],
            "conjugate_in_WE6": True,
            "source_generator_count": len(source_gens),
            "witness_sha256": __import__("hashlib").sha256(witness.tobytes()).hexdigest()
        })

    result = {
        "schema": "w33.pass1134.we6_432_stabilizers.v1",
        "status": "PASS",
        "headline": "All three 432-orbit stabilizers are S5 and are pairwise conjugate in W(E6). Hence the Steinberg carrier is three isomorphic copies of W(E6)/S5, not three subgroup types.",
        "group_order": len(group),
        "a2_orbit_sizes": [len(x) for x in a2_orbits()],
        "records": records,
        "pairwise_conjugacy": conjugacy,
        "theorem": {
            "carrier_decomposition": "Omega_432^(1) disjoint_union Omega_432^(2) disjoint_union Omega_432^(3)",
            "each_orbit_isomorphic_to": "W(E6)/S5",
            "three_orbits_pairwise_isomorphic_as_G_sets": True,
            "each_carries_one_81_minus": "imported from exact Pass 1126 orbit character decomposition"
        },
        "checks": {
            "we6_order_51840": len(group) == 51840,
            "three_432_orbits": len(orbits432) == 3,
            "all_stabilizers_order_120": all(r["stabilizer"]["order"] == 120 for r in records),
            "all_stabilizers_S5": all(r["stabilizer"]["small_group_identification"].startswith("S5") for r in records),
            "all_pairs_conjugate": all(x["conjugate_in_WE6"] for x in conjugacy)
        },
        "scope": "Exact finite permutation computation on the 240 E8 roots; no GAP installation required."
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "headline": result["headline"]}, indent=2))


if __name__ == "__main__":
    main()
