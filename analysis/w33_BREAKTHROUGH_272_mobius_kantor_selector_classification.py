"""W(3,3) BREAKTHROUGH 272: Mobius-Kantor selector classification.

BT271 exhibited one decomposition

    K8,8 = Q4 disjoint-union Mobius-Kantor disjoint-union M8.

BT272 classifies the selector.  Inside the weight-3 complement C of Q4 in
K8,8, every perfect matching M leaves a cubic graph C \\ M.  There are 272
perfect matchings in C.  Exactly 8 of them leave a connected cubic graph of
girth 6, hence a Mobius-Kantor graph on 16 vertices.

The count is substrate-clean:

    8 = 2^q.

Moreover, the affine coordinate automorphism group of F_2^4 has order

    384 = 2^mu * 4! = lambda^mu * f,

and acts transitively on those 8 Mobius-Kantor selectors.  The stabilizer of
one selector has order

    384 / 8 = 48 = mu * k.

So the BT271 decomposition is not an isolated witness.  There are exactly
2^q identity-matchings that select the Mobius-Kantor layer, and they form one
octonion-sized orbit under the natural Q4 affine symmetry.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import permutations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_271_k88_q4_mobius_kantor_decomposition import (  # noqa: E402
    Q,
    MU,
    PHI6,
    adjacency,
    complete_bipartite_edges,
    degree_distribution,
    girth,
    hamming_weight,
    q4_edges,
)


K = 12
F = 24


def weight3_complement_edges() -> set[tuple[int, int]]:
    return complete_bipartite_edges() - q4_edges()


def perfect_matchings(edge_set: set[tuple[int, int]]) -> list[frozenset[tuple[int, int]]]:
    adj = adjacency(edge_set)
    left = sorted(vertex for vertex in range(16) if hamming_weight(vertex) % 2 == 0)
    matchings = []
    used = set()
    current = []

    def search(index: int) -> None:
        if index == len(left):
            matchings.append(frozenset(tuple(sorted(edge)) for edge in current))
            return
        source = left[index]
        for target in sorted(adj[source]):
            if target in used:
                continue
            used.add(target)
            current.append((source, target))
            search(index + 1)
            current.pop()
            used.remove(target)

    search(0)
    return matchings


def component_size_from_zero(edge_set: set[tuple[int, int]]) -> int:
    adj = adjacency(edge_set)
    seen = {0}
    queue = deque([0])
    while queue:
        current = queue.popleft()
        for nxt in adj[current]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return len(seen)


def profile_for_complement(edge_set: set[tuple[int, int]]) -> tuple[int, int]:
    return component_size_from_zero(edge_set), girth(edge_set)


def apply_coordinate_permutation(vertex: int, coordinate_permutation: tuple[int, ...]) -> int:
    image = 0
    for source, target in enumerate(coordinate_permutation):
        if vertex & (1 << source):
            image |= 1 << target
    return image


def affine_coordinate_automorphisms() -> list[tuple[tuple[int, ...], int]]:
    complement = weight3_complement_edges()
    autos = []
    for translation in range(16):
        for coordinate_permutation in permutations(range(4)):
            image = {
                tuple(
                    sorted(
                        (
                            apply_coordinate_permutation(left, coordinate_permutation) ^ translation,
                            apply_coordinate_permutation(right, coordinate_permutation) ^ translation,
                        )
                    )
                )
                for left, right in complement
            }
            if image == complement:
                autos.append((coordinate_permutation, translation))
    return autos


def apply_affine_to_matching(
    matching: frozenset[tuple[int, int]],
    automorphism: tuple[tuple[int, ...], int],
) -> frozenset[tuple[int, int]]:
    coordinate_permutation, translation = automorphism
    return frozenset(
        tuple(
            sorted(
                (
                    apply_coordinate_permutation(left, coordinate_permutation) ^ translation,
                    apply_coordinate_permutation(right, coordinate_permutation) ^ translation,
                )
            )
        )
        for left, right in matching
    )


def orbit_sizes(
    matchings: list[frozenset[tuple[int, int]]],
    automorphisms: list[tuple[tuple[int, ...], int]],
) -> list[int]:
    matching_set = set(matchings)
    visited = set()
    sizes = []
    for matching in matchings:
        if matching in visited:
            continue
        queue = deque([matching])
        visited.add(matching)
        size = 0
        while queue:
            current = queue.popleft()
            size += 1
            for automorphism in automorphisms:
                image = apply_affine_to_matching(current, automorphism)
                if image in matching_set and image not in visited:
                    visited.add(image)
                    queue.append(image)
        sizes.append(size)
    return sorted(sizes)


def matching_xor_direction_counts(matching: frozenset[tuple[int, int]]) -> dict[int, int]:
    return dict(sorted(Counter(left ^ right for left, right in matching).items()))


def mobius_kantor_selector_classification_packet() -> dict:
    complement = weight3_complement_edges()
    matchings = perfect_matchings(complement)
    profile_counts = Counter()
    selector_matchings = []
    for matching in matchings:
        cubic = complement - set(matching)
        profile = profile_for_complement(cubic)
        profile_counts[profile] += 1
        if profile == (16, 6) and degree_distribution(cubic) == {3: 16}:
            selector_matchings.append(matching)

    automorphisms = affine_coordinate_automorphisms()
    all_orbit_sizes = orbit_sizes(matchings, automorphisms)
    selector_orbit_sizes = orbit_sizes(selector_matchings, automorphisms)
    selector_xor_profiles = Counter(
        tuple(matching_xor_direction_counts(matching).items())
        for matching in selector_matchings
    )

    checks = {
        "weight3_complement_has_32_edges": len(complement) == 32,
        "perfect_matching_count_is_272": len(matchings) == 272,
        "profile_split_is_4_260_8": profile_counts == {
            (8, 4): 4,
            (16, 4): 260,
            (16, 6): 8,
        },
        "mk_selector_count_is_2_to_q": len(selector_matchings) == 2**Q == 8,
        "all_selectors_have_balanced_xor_profile": selector_xor_profiles
        == {((7, 2), (11, 2), (13, 2), (14, 2)): 8},
        "affine_coordinate_automorphism_order_is_384": len(automorphisms) == 384 == 2**MU * F,
        "mk_selectors_form_one_orbit": selector_orbit_sizes == [2**Q],
        "mk_selector_stabilizer_is_mu_k": len(automorphisms) // len(selector_matchings) == MU * K == 48,
        "all_matching_orbit_sizes_are_substrate_clean": all_orbit_sizes == [4, 8, 12, 24, 32, 48, 48, 96],
        "orbit_size_sum_is_272": sum(all_orbit_sizes) == len(matchings),
    }

    return {
        "breakthrough": 272,
        "title": "Mobius-Kantor selector classification",
        "weight3_complement_edge_count": len(complement),
        "perfect_matching_count": len(matchings),
        "profile_counts": {str(key): value for key, value in sorted(profile_counts.items())},
        "mobius_kantor_selector_count": len(selector_matchings),
        "selector_xor_profiles": {str(key): value for key, value in sorted(selector_xor_profiles.items())},
        "affine_coordinate_automorphism_order": len(automorphisms),
        "selector_orbit_sizes": selector_orbit_sizes,
        "selector_stabilizer_order": len(automorphisms) // len(selector_matchings),
        "all_matching_orbit_sizes": all_orbit_sizes,
        "selector_matchings": [
            sorted([list(edge) for edge in matching])
            for matching in selector_matchings
        ],
        "architectural_reading": (
            "The BT271 decomposition is one member of a complete selector system. "
            "The Q4 weight-3 complement has 272 perfect matchings, but exactly "
            "8 = 2^q of them select a Mobius-Kantor cubic complement. These "
            "8 identity matchings form one orbit under the 384-element affine "
            "coordinate symmetry of F_2^4, with stabilizer 48 = mu*k. The "
            "octonion-sized selector orbit is therefore intrinsic to the 16-point "
            "past/future carrier, not an arbitrary embedding."
        ),
        "boundary": (
            "This classifies selectors under the natural affine coordinate "
            "symmetry of the F_2^4 model. It does not yet identify which of the "
            "8 selectors is chosen by a W(3,3) now-fan or physical clock phase."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = mobius_kantor_selector_classification_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 272: MOBIUS-KANTOR SELECTOR CLASSIFICATION")
    print("=" * 78)
    print()
    print(f"perfect matchings    = {packet['perfect_matching_count']}")
    print(f"profile counts       = {packet['profile_counts']}")
    print(f"MK selectors         = {packet['mobius_kantor_selector_count']}")
    print(f"selector orbits      = {packet['selector_orbit_sizes']}")
    print(f"selector stabilizer  = {packet['selector_stabilizer_order']}")
    print(f"verified             = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_272_mobius_kantor_selector_classification.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
