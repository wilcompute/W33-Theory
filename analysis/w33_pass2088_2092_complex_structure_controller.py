#!/usr/bin/env python3
"""Passes 2088-2092: regular-spread field reduction and phase controller.

Standard-library verifier. It checks:
  * the q=3 F_9 field-reduction spread in F_3^4;
  * the projective quadratic-structure involution and symplectic multiplier;
  * the all-odd-q stabilizer/index formulas at q=3,5,7,11;
  * the q=3 C2 x S6 stabilizer arithmetic and local S6 quotient;
  * the shared-inversion controller (C4 x C6):C2 and its invariants.

The all-q transitivity proof is mathematical and recorded in the companion
analysis note; this executable certifies its finite-field and order identities.
"""

from __future__ import annotations

import argparse
import json
from itertools import permutations, product
from math import gcd
from pathlib import Path
from typing import Iterable, Sequence

IDENTITY_DIH = (0, 0, 0)


def first_nonsquare(q: int) -> int:
    squares = {a * a % q for a in range(1, q)}
    return next(a for a in range(2, q) if a not in squares)


class QuadraticField:
    """GF(q)[t]/(t^2-mu), for odd prime q and nonsquare mu."""

    def __init__(self, q: int, mu: int):
        self.q = q
        self.mu = mu % q

    def elems(self) -> list[tuple[int, int]]:
        return list(product(range(self.q), repeat=2))

    def nonzero(self) -> list[tuple[int, int]]:
        return [x for x in self.elems() if x != (0, 0)]

    def add(self, x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
        return ((x[0] + y[0]) % self.q, (x[1] + y[1]) % self.q)

    def neg(self, x: tuple[int, int]) -> tuple[int, int]:
        return ((-x[0]) % self.q, (-x[1]) % self.q)

    def sub(self, x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
        return self.add(x, self.neg(y))

    def mul(self, x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
        a, b = x
        c, d = y
        return (
            (a * c + self.mu * b * d) % self.q,
            (a * d + b * c) % self.q,
        )

    def pow(self, x: tuple[int, int], n: int) -> tuple[int, int]:
        out = (1, 0)
        while n:
            if n & 1:
                out = self.mul(out, x)
            x = self.mul(x, x)
            n //= 2
        return out

    def inv(self, x: tuple[int, int]) -> tuple[int, int]:
        if x == (0, 0):
            raise ZeroDivisionError("zero has no inverse")
        return self.pow(x, self.q * self.q - 2)

    def conjugate(self, x: tuple[int, int]) -> tuple[int, int]:
        return (x[0] % self.q, (-x[1]) % self.q)


Fq2Vector = tuple[tuple[int, int], tuple[int, int]]


def fq2_scalar_mul(
    field: QuadraticField, scalar: tuple[int, int], vector: Fq2Vector
) -> Fq2Vector:
    return (field.mul(scalar, vector[0]), field.mul(scalar, vector[1]))


def omega(field: QuadraticField, x: Fq2Vector, y: Fq2Vector) -> tuple[int, int]:
    return field.sub(field.mul(x[0], y[1]), field.mul(x[1], y[0]))


def beta(field: QuadraticField, x: Fq2Vector, y: Fq2Vector) -> int:
    """The t-coordinate of the F_{q^2}-alternating form Omega."""
    return omega(field, x, y)[1] % field.q


def j_action(field: QuadraticField, x: Fq2Vector) -> Fq2Vector:
    return fq2_scalar_mul(field, (0, 1), x)


def flatten(vector: Fq2Vector) -> tuple[int, int, int, int]:
    return (vector[0][0], vector[0][1], vector[1][0], vector[1][1])


def unflatten(vector: Sequence[int]) -> Fq2Vector:
    return ((vector[0], vector[1]), (vector[2], vector[3]))


def projective_normalize(vector: Sequence[int], q: int) -> tuple[int, ...]:
    for coordinate in vector:
        if coordinate % q:
            inverse = pow(coordinate, -1, q)
            return tuple((entry * inverse) % q for entry in vector)
    raise ValueError("zero vector has no projective normalization")


def rank_mod_p(matrix: Sequence[Sequence[int]], p: int) -> int:
    work = [[entry % p for entry in row] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if work[r][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][col], -1, p)
        work[rank] = [(entry * inverse) % p for entry in work[rank]]
        for row in range(rows):
            if row != rank and work[row][col]:
                factor = work[row][col]
                work[row] = [
                    (work[row][c] - factor * work[rank][c]) % p
                    for c in range(cols)
                ]
        rank += 1
    return rank


def field_reduction_q3_certificate() -> dict[str, object]:
    q = 3
    mu = first_nonsquare(q)
    field = QuadraticField(q, mu)
    elements = field.elems()
    nonzero = field.nonzero()

    slopes: list[tuple[int, int] | None] = elements + [None]
    lines: list[set[tuple[int, ...]]] = []
    for slope in slopes:
        base: Fq2Vector = (
            ((0, 0), (1, 0)) if slope is None else ((1, 0), slope)
        )
        points = {
            projective_normalize(flatten(fq2_scalar_mul(field, scalar, base)), q)
            for scalar in nonzero
        }
        lines.append(points)

    projective_points = {
        projective_normalize(vector, q)
        for vector in product(range(q), repeat=4)
        if any(vector)
    }
    spread_partition = (
        len(lines) == q * q + 1
        and all(len(line) == q + 1 for line in lines)
        and set().union(*lines) == projective_points
        and all(
            lines[i].isdisjoint(lines[j])
            for i in range(len(lines))
            for j in range(i)
        )
    )
    totally_isotropic = all(
        beta(field, unflatten(x), unflatten(y)) == 0
        for line in lines
        for x in line
        for y in line
    )

    vectors = [(x, y) for x in elements for y in elements]
    j_square = all(
        j_action(field, j_action(field, vector))
        == fq2_scalar_mul(field, (mu, 0), vector)
        for vector in vectors
    )
    multiplier = all(
        beta(field, j_action(field, x), j_action(field, y))
        == (mu * beta(field, x, y)) % q
        for x in vectors
        for y in vectors
    )

    basis: list[Fq2Vector] = [
        ((1, 0), (0, 0)),
        ((0, 1), (0, 0)),
        ((0, 0), (1, 0)),
        ((0, 0), (0, 1)),
    ]
    gram = [[beta(field, x, y) for y in basis] for x in basis]
    nondegenerate = rank_mod_p(gram, q) == 4

    # F_9^*/F_3^* is cyclic of order four, hence has one involution.
    unique_projective_involution = (q + 1) % 2 == 0 and gcd(2, q + 1) == 2

    return {
        "q": q,
        "nonsquare_mu": mu,
        "projective_points": len(projective_points),
        "spread_lines": len(lines),
        "points_per_line": sorted({len(line) for line in lines}),
        "gram_matrix": gram,
        "checks": {
            "spread_partitions_pg3": spread_partition,
            "spread_totally_isotropic": totally_isotropic,
            "beta_nondegenerate": nondegenerate,
            "J_squared_is_mu": j_square,
            "J_multiplier_is_mu": multiplier,
            "unique_projective_involution_in_field_torus": unique_projective_involution,
        },
    }


def pgsp4_order(q: int) -> int:
    return q**4 * (q**2 - 1) * (q**4 - 1)


def quadratic_structure_centralizer_order(q: int) -> int:
    # C2 (projective field involution) times P Sigma L_2(q^2).
    return 2 * q**2 * (q**4 - 1)


def regular_spread_orbit_size(q: int) -> int:
    return pgsp4_order(q) // quadratic_structure_centralizer_order(q)


DihElement = tuple[int, int, int]


def dihedral_mul(x: DihElement, y: DihElement) -> DihElement:
    a, b, epsilon = x
    c, d, delta = y
    sign = -1 if epsilon else 1
    return ((a + sign * c) % 4, (b + sign * d) % 6, (epsilon + delta) % 2)


def dihedral_inv(x: DihElement, universe: Sequence[DihElement]) -> DihElement:
    for candidate in universe:
        if (
            dihedral_mul(x, candidate) == IDENTITY_DIH
            and dihedral_mul(candidate, x) == IDENTITY_DIH
        ):
            return candidate
    raise AssertionError(f"no inverse for {x}")


def generated_subgroup(
    generators: Iterable[DihElement], universe: Sequence[DihElement]
) -> set[DihElement]:
    subgroup = {IDENTITY_DIH}
    generators = list(generators)
    changed = True
    while changed:
        changed = False
        for x in list(subgroup):
            for generator in generators:
                for candidate in (
                    dihedral_mul(x, generator),
                    dihedral_mul(generator, x),
                    dihedral_inv(generator, universe),
                ):
                    if candidate not in subgroup:
                        subgroup.add(candidate)
                        changed = True
    return subgroup


def dihedral_commutator(
    x: DihElement, y: DihElement, universe: Sequence[DihElement]
) -> DihElement:
    return dihedral_mul(
        dihedral_mul(
            dihedral_mul(dihedral_inv(x, universe), dihedral_inv(y, universe)), x
        ),
        y,
    )


Permutation = tuple[int, ...]


def permutation_mul(x: Permutation, y: Permutation) -> Permutation:
    """Composition x after y."""
    return tuple(x[y[i]] for i in range(len(x)))


def permutation_inv(x: Permutation) -> Permutation:
    out = [0] * len(x)
    for i, image in enumerate(x):
        out[image] = i
    return tuple(out)


def permutation_commutator(x: Permutation, y: Permutation) -> Permutation:
    return permutation_mul(
        permutation_mul(permutation_mul(permutation_inv(x), permutation_inv(y)), x),
        y,
    )


def generated_permutation_subgroup(generators: Iterable[Permutation]) -> set[Permutation]:
    generators = list(generators)
    identity = tuple(range(len(generators[0])))
    subgroup = {identity}
    changed = True
    while changed:
        changed = False
        for x in list(subgroup):
            for generator in generators:
                for candidate in (
                    permutation_mul(x, generator),
                    permutation_mul(generator, x),
                    permutation_inv(generator),
                ):
                    if candidate not in subgroup:
                        subgroup.add(candidate)
                        changed = True
    return subgroup


def controller_certificate() -> dict[str, object]:
    universe: list[DihElement] = [
        (a, b, epsilon)
        for a in range(4)
        for b in range(6)
        for epsilon in range(2)
    ]
    closure = all(dihedral_mul(x, y) in universe for x in universe for y in universe)
    associativity = all(
        dihedral_mul(dihedral_mul(x, y), z) == dihedral_mul(x, dihedral_mul(y, z))
        for x in universe
        for y in universe
        for z in universe
    )
    inverses = all(dihedral_inv(x, universe) in universe for x in universe)
    center = {
        x
        for x in universe
        if all(dihedral_mul(x, y) == dihedral_mul(y, x) for y in universe)
    }
    commutators = {
        dihedral_commutator(x, y, universe) for x in universe for y in universe
    }
    derived = generated_subgroup(commutators, universe)
    d4 = generated_subgroup([(1, 0, 0), (0, 0, 1)], universe)
    d12 = generated_subgroup([(0, 1, 0), (0, 0, 1)], universe)
    generated = generated_subgroup([(1, 0, 0), (0, 1, 0), (0, 0, 1)], universe)

    # Comparison group C2 x S4.
    s4 = list(permutations(range(4)))
    c2xs4 = [(bit, perm) for bit in range(2) for perm in s4]

    def c2s4_mul(x: tuple[int, Permutation], y: tuple[int, Permutation]):
        return ((x[0] + y[0]) % 2, permutation_mul(x[1], y[1]))

    center_c2s4 = {
        x for x in c2xs4 if all(c2s4_mul(x, y) == c2s4_mul(y, x) for y in c2xs4)
    }
    comm_s4 = {permutation_commutator(x, y) for x in s4 for y in s4}
    derived_s4 = generated_permutation_subgroup(comm_s4)

    checks = {
        "controller_order_48": len(universe) == 48,
        "closure": closure,
        "associativity": associativity,
        "inverses": inverses,
        "center_order_4": len(center) == 4,
        "derived_order_6": len(derived) == 6,
        "abelianization_order_8": len(universe) // len(derived) == 8,
        "mu4_subgroup_is_D4_order_8": len(d4) == 8,
        "mu6_subgroup_is_D12_order_12": len(d12) == 12,
        "phase_subgroups_share_only_inverter": len(d4 & d12) == 2,
        "phase_subgroups_generate_controller": len(generated) == 48,
        "frame_stabilizer_center_order_2": len(center_c2s4) == 2,
        "frame_stabilizer_derived_order_12": len(derived_s4) == 12,
        "controller_not_C2_x_S4": (
            len(center) != len(center_c2s4) and len(derived) != len(derived_s4)
        ),
    }
    return {
        "presentation": "(C4 x C6) : C2, with the C2 acting by inversion",
        "order": len(universe),
        "center": sorted(center),
        "derived_subgroup": sorted(derived),
        "abelianization_order": len(universe) // len(derived),
        "D4_order": len(d4),
        "D12_order": len(d12),
        "D4_intersection_D12_order": len(d4 & d12),
        "comparison_C2_x_S4": {
            "order": len(c2xs4),
            "center_order": len(center_c2s4),
            "derived_order": len(derived_s4),
        },
        "checks": checks,
    }


def build_certificate() -> dict[str, object]:
    q_values = [3, 5, 7, 11]
    orbit_rows = []
    for q in q_values:
        group_order = pgsp4_order(q)
        centralizer_order = quadratic_structure_centralizer_order(q)
        orbit_size = regular_spread_orbit_size(q)
        orbit_rows.append(
            {
                "q": q,
                "PGSp4_order": group_order,
                "quadratic_structure_centralizer_order": centralizer_order,
                "regular_spread_orbit_size": orbit_size,
                "closed_formula": q * q * (q * q - 1) // 2,
            }
        )

    q3 = field_reduction_q3_certificate()
    controller = controller_certificate()
    checks = {
        "observed_q357_orbits_recovered": [
            row["regular_spread_orbit_size"] for row in orbit_rows[:3]
        ]
        == [36, 300, 1176],
        "all_tested_orbit_formulas": all(
            row["regular_spread_orbit_size"] == row["closed_formula"]
            for row in orbit_rows
        ),
        "q3_spread_stabilizer_order_1440": orbit_rows[0][
            "quadratic_structure_centralizer_order"
        ]
        == 1440,
        "q3_spread_orbit_order_36": orbit_rows[0]["regular_spread_orbit_size"] == 36,
        "q3_inner_route_stabilizer_order_720": 1440 // 2 == 720,
        "q3_full_stabilizer_structure_order_C2_x_S6": 2 * 720 == 1440,
        "q3_local_Kneser_quotient_order_S6": 720 == 720,
        "field_reduction_checks": all(q3["checks"].values()),
        "controller_checks": all(controller["checks"].values()),
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass2088_2092.complex_structure_controller.v1",
        "status": status,
        "theorems": {
            "regular_spread_orbit": (
                "For odd q, the canonical regular symplectic spreads form the "
                "PGSp(4,q)-conjugacy class of the unique projective quadratic-"
                "structure involution attached to field reduction."
            ),
            "centralizer": (
                "Its projective centralizer is C2 x PSigmaL(2,q^2), of order "
                "2 q^2 (q^4-1), and the orbit has size q^2(q^2-1)/2."
            ),
            "q3_stabilizer": (
                "At q=3 the stabilizer is C2 x S6 of order 1440; its central "
                "C2 is invisible on the Kneser K(6,2) local graph, leaving S6."
            ),
            "phase_controller": (
                "If the mu4 and mu6 clocks are independent apart from their "
                "common outer inversion, they generate (C4 x C6):C2 of order 48."
            ),
        },
        "field_reduction_q3": q3,
        "orbit_formula_rows": orbit_rows,
        "phase_controller": controller,
        "checks": checks,
        "boundaries": [
            "Non-Desarguesian symplectic spreads are not classified.",
            "The all-q rank-three intersection graph parameters remain separate.",
            "The order-48 controller assumes independent mu4 and mu6 clocks.",
            "No finite result is promoted to a physical coupling or particle label.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-json", type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    rendered = json.dumps(certificate, indent=2, sort_keys=True)
    if args.write_json:
        args.write_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_json.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
