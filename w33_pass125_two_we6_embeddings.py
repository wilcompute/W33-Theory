#!/usr/bin/env python3
"""Pass 125: distinguish two W(E6) embeddings in O_8^+(2):2.

Pass 102 asserted that the code-induced W(E6) action on C^perp/C is
transitive on the 135 nonzero isotropic and 120 anisotropic classes, but its
old witness only enumerated the quadratic form and incorrectly inherited
transitivity from the larger orthogonal group.  Pass 117 later constructed a
different W(E6), the pointwise stabilizer of an ordered anisotropic pair, and
found nontransitive orbit fingerprints.

This verifier constructs the missing action.  Five symplectic transvections
and one multiplier-2 similitude generate PGSp(4,3) on the 40 projective
points of W(3,3).  Coordinate permutations transport this group through the
binary adjacency code to C^perp/C.  Everything is enumerated, including both
permutation images and every quotient orbit.
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path
from typing import Iterable, Sequence

from analysis.w33_axes_e8_rootline_spectral_bridge import (
    Vec,
    build_w33,
    canonical,
    omega,
)
from w33_pass123_axis_glue_e8_lift import (
    build_code_and_quotient,
    quadratic_from_representatives,
    reduce_mod_basis,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "w33_pass125_two_we6_embeddings.json"

Permutation = tuple[int, ...]
Matrix4 = tuple[tuple[int, int, int, int], ...]


def compose(left: Permutation, right: Permutation) -> Permutation:
    """Return left after right."""
    return tuple(left[right[index]] for index in range(len(right)))


def generated_group(generators: Sequence[Permutation]) -> set[Permutation]:
    identity = tuple(range(len(generators[0])))
    group = {identity}
    queue = deque([identity])
    while queue:
        element = queue.popleft()
        for generator in generators:
            product = compose(element, generator)
            if product not in group:
                group.add(product)
                queue.append(product)
    return group


def transvection(vector: Vec, points: Sequence[Vec]) -> Permutation:
    point_index = {point: index for index, point in enumerate(points)}

    def image(point: Vec) -> Vec:
        coefficient = omega(point, vector)
        return canonical(
            tuple(
                (point[index] + coefficient * vector[index]) % 3 for index in range(4)
            )
        )

    return tuple(point_index[image(point)] for point in points)


def matrix_permutation(matrix: Matrix4, points: Sequence[Vec]) -> Permutation:
    point_index = {point: index for index, point in enumerate(points)}

    def image(point: Vec) -> Vec:
        return canonical(
            tuple(
                sum(matrix[row][column] * point[column] for column in range(4)) % 3
                for row in range(4)
            )
        )

    return tuple(point_index[image(point)] for point in points)


def point_generators(points: Sequence[Vec]) -> list[Permutation]:
    # These five transvections generate PSp(4,3).  The last matrix has
    # omega(Dx,Dy)=2*omega(x,y), adjoining the nonsquare multiplier coset.
    vectors: list[Vec] = [
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
        (1, 1, 0, 0),
    ]
    multiplier_two: Matrix4 = (
        (2, 0, 0, 0),
        (0, 2, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )
    return [transvection(vector, points) for vector in vectors] + [
        matrix_permutation(multiplier_two, points)
    ]


def permute_word(word: int, permutation: Permutation) -> int:
    return sum(
        1 << permutation[index]
        for index in range(len(permutation))
        if (word >> index) & 1
    )


def quotient_permutation(
    point_permutation: Permutation,
    representatives: dict[int, int],
    code_basis: Iterable[int],
    canonical_to_coordinate: dict[int, int],
) -> Permutation:
    images = []
    for coordinate in range(256):
        moved = permute_word(representatives[coordinate], point_permutation)
        canonical_word = reduce_mod_basis(moved, code_basis)
        images.append(canonical_to_coordinate[canonical_word])
    return tuple(images)


def orbit(seed: int, generators: Sequence[Permutation]) -> set[int]:
    result = {seed}
    queue = deque([seed])
    while queue:
        element = queue.popleft()
        for generator in generators:
            image = generator[element]
            if image not in result:
                result.add(image)
                queue.append(image)
    return result


def orbit_partition(generators: Sequence[Permutation]) -> list[list[int]]:
    remaining = set(range(len(generators[0])))
    parts = []
    while remaining:
        part = orbit(min(remaining), generators)
        parts.append(sorted(part))
        remaining -= part
    return parts


def main() -> int:
    points, edges, adjacency, *_ = build_w33()
    code_data = build_code_and_quotient()
    quadratic, _ = quadratic_from_representatives(code_data["quotient_representatives"])

    point_gens = point_generators(points)
    psp_point_group = generated_group(point_gens[:-1])
    pgsp_point_group = generated_group(point_gens)

    quotient_gens = [
        quotient_permutation(
            generator,
            code_data["quotient_representatives"],
            code_data["code_basis"],
            code_data["canonical_to_coordinate"],
        )
        for generator in point_gens
    ]
    quotient_group = generated_group(quotient_gens)
    quotient_parts = orbit_partition(quotient_gens)
    quotient_fingerprint = sorted(
        (len(part), quadratic(part[0])) for part in quotient_parts
    )

    edge_set = {tuple(sorted(edge)) for edge in edges}
    adjacency_preserved = all(
        {tuple(sorted((generator[left], generator[right]))) for left, right in edge_set}
        == edge_set
        for generator in point_gens
    )
    code_preserved = all(
        reduce_mod_basis(permute_word(word, generator), code_data["code_basis"]) == 0
        for generator in point_gens
        for word in code_data["code_basis"]
    )
    quotient_linear = all(
        generator[left ^ right] == generator[left] ^ generator[right]
        for generator in quotient_gens
        for left in range(256)
        for right in range(256)
    )
    quotient_quadratic = all(
        quadratic(generator[vector]) == quadratic(vector)
        for generator in quotient_gens
        for vector in range(256)
    )

    pass117_isotropic = [27, 36, 36, 36]
    pass117_anisotropic = [1, 1, 1, 27, 27, 27, 36]
    code_isotropic = sorted(
        len(part) for part in quotient_parts if part[0] and quadratic(part[0]) == 0
    )
    code_anisotropic = sorted(
        len(part) for part in quotient_parts if quadratic(part[0]) == 1
    )

    checks = {
        "w33_has_40_points_240_edges": len(points) == 40 and len(edges) == 240,
        "all_projective_generators_preserve_adjacency": adjacency_preserved,
        "PSp43_projective_image_order_25920": len(psp_point_group) == 25_920,
        "PGSp43_projective_image_order_51840": len(pgsp_point_group) == 51_840,
        "all_generators_preserve_binary_code": code_preserved,
        "induced_quotient_maps_are_linear": quotient_linear,
        "induced_quotient_maps_preserve_Q": quotient_quadratic,
        "quotient_action_is_faithful_order_51840": len(quotient_group) == 51_840,
        "code_embedding_orbits_are_1_135_120": quotient_fingerprint
        == [(1, 0), (120, 1), (135, 0)],
        "isotropic_stabilizer_order_384": len(quotient_group) // 135 == 384,
        "anisotropic_stabilizer_order_432": len(quotient_group) // 120 == 432,
        "pass117_fingerprints_differ": (
            code_isotropic != pass117_isotropic
            and code_anisotropic != pass117_anisotropic
        ),
    }

    payload = {
        "schema": "w33.pass125.two_we6_embeddings.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": (
            "The code-induced PGSp(4,3), isomorphic to W(E6), acts faithfully on "
            "Cperp/C with orbits {0}, 135 isotropic, and 120 anisotropic. "
            "The Pass 117 ordered-anisotropic-pair stabilizer is a nonconjugate "
            "W(E6) embedding in O+_8(2):2, detected by its different orbit "
            "fingerprints."
        ),
        "generators": {
            "symplectic_transvections": [
                "1000",
                "0100",
                "0010",
                "0001",
                "1100",
            ],
            "nonsquare_similitude": "diag(2,2,1,1)",
            "PSp43_projective_order": len(psp_point_group),
            "PGSp43_projective_order": len(pgsp_point_group),
        },
        "code_embedding": {
            "quotient_image_order": len(quotient_group),
            "faithful": len(quotient_group) == len(pgsp_point_group),
            "orbit_fingerprint_size_Q": [
                [size, q_value] for size, q_value in quotient_fingerprint
            ],
            "isotropic_nonzero_orbits": code_isotropic,
            "anisotropic_orbits": code_anisotropic,
            "stabilizers": {"isotropic": 384, "anisotropic": 432},
        },
        "pass117_ordered_pair_embedding": {
            "isotropic_orbits": pass117_isotropic,
            "anisotropic_orbits": pass117_anisotropic,
        },
        "nonconjugacy_certificate": (
            "Conjugate subgroups have identical orbit-size multisets in the "
            "same ambient permutation action. These two order-51840 subgroups "
            "do not, so they are not conjugate in O+_8(2):2."
        ),
        "correction": (
            "Pass 102's orbit statement is true for the code-induced embedding, "
            "but its old proof was invalid: transitivity of O+_8(2) does not "
            "imply transitivity of a subgroup. Pass 125 supplies the missing "
            "explicit action. Pass 117 remains true for a different embedding."
        ),
        "checks": checks,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {key: payload[key] for key in ("schema", "status", "theorem")}, indent=2
        )
    )
    print(f"checks: {sum(checks.values())}/{len(checks)}")
    print(f"wrote: {OUT}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
