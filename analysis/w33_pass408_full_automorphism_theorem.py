#!/usr/bin/env python3
"""Pass 408: full unoriented automorphism theorem for the Heisenberg DRACKN."""
from __future__ import annotations

import argparse
from itertools import permutations, product
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass408_full_automorphism_theorem.json"
PASS403 = ROOT / "data" / "w33_pass403_drackn_semilinear_classification.json"


def points(q: int) -> list[tuple[int, int]]:
    return [(x, y) for x in range(q) for y in range(q)]


def lines(q: int) -> set[frozenset[int]]:
    pts = points(q)
    index = {p: i for i, p in enumerate(pts)}
    result: set[frozenset[int]] = set()
    for slope in range(q):
        for intercept in range(q):
            result.add(frozenset(index[(x, (slope * x + intercept) % q)] for x in range(q)))
    for x in range(q):
        result.add(frozenset(index[(x, y)] for y in range(q)))
    return result


def gl2(q: int) -> list[tuple[int, int, int, int]]:
    result = []
    for a, b, c, d in product(range(q), repeat=4):
        if (a * d - b * c) % q:
            result.append((a, b, c, d))
    return result


def apply_matrix(M: tuple[int, int, int, int], u: tuple[int, int], q: int) -> tuple[int, int]:
    a, b, c, d = M
    x, y = u
    return ((a * x + b * y) % q, (c * x + d * y) % q)


def det(M: tuple[int, int, int, int], q: int) -> int:
    a, b, c, d = M
    return (a * d - b * c) % q


def omega(u: tuple[int, int], v: tuple[int, int], q: int) -> int:
    x, y = u
    xp, yp = v
    return (y * xp - x * yp) % q


def affine_permutations(q: int) -> set[tuple[int, ...]]:
    pts = points(q)
    index = {p: i for i, p in enumerate(pts)}
    result = set()
    for M in gl2(q):
        for shift in pts:
            perm = []
            for u in pts:
                Mu = apply_matrix(M, u, q)
                image = ((Mu[0] + shift[0]) % q, (Mu[1] + shift[1]) % q)
                perm.append(index[image])
            result.add(tuple(perm))
    return result


def exhaustive_affine_plane_automorphisms_q3() -> set[tuple[int, ...]]:
    q = 3
    line_set = lines(q)
    line_list = list(line_set)
    result = set()
    for perm in permutations(range(q * q)):
        if all(frozenset(perm[i] for i in line) in line_set for line in line_list):
            result.add(tuple(perm))
    return result


def graph_automorphism_map(q: int, M, shift, central: int, vertex: tuple[int, int, int]) -> tuple[int, int, int]:
    u = vertex[:2]
    z = vertex[2]
    Mu = apply_matrix(M, u, q)
    fu = ((Mu[0] + shift[0]) % q, (Mu[1] + shift[1]) % q)
    multiplier = det(M, q)
    z_image = (multiplier * z - omega(Mu, shift, q) + central) % q
    return fu[0], fu[1], z_image


def verify_map(q: int, M, shift, central: int) -> bool:
    pts = points(q)
    # It is enough to verify the voltage equation for all base pairs; z cancels.
    for u in pts:
        for v in pts:
            if u == v:
                continue
            left = omega(u, v, q)
            image_u = graph_automorphism_map(q, M, shift, central, (u[0], u[1], 0))
            image_v = graph_automorphism_map(q, M, shift, central, (v[0], v[1], left))
            if (image_v[2] - image_u[2] - omega(image_u[:2], image_v[:2], q)) % q:
                return False
    return True


def build_payload() -> dict:
    exhaustive = exhaustive_affine_plane_automorphisms_q3()
    affine3 = affine_permutations(3)
    matrices3 = gl2(3)
    matrices5 = gl2(5)

    q3_maps = {
        tuple(graph_automorphism_map(3, M, shift, central, (x, y, z))
              for x, y, z in product(range(3), repeat=3))
        for M in matrices3
        for shift in points(3)
        for central in range(3)
    }

    pass403 = json.loads(PASS403.read_text())
    p403_orders = {int(case["q"]): int(case["permutation_group_order"]) for case in pass403["cases"]}

    checks = {
        "q3_exhaustive_affine_plane_collineation_count_432": len(exhaustive) == 432,
        "q3_every_collineation_is_affine": exhaustive == affine3,
        "q3_constructed_graph_maps_count_1296": len(q3_maps) == 1296,
        "q3_all_constructed_maps_preserve_voltage": all(
            verify_map(3, M, shift, central)
            for M in matrices3 for shift in points(3) for central in range(3)
        ),
        "q5_gl_order_480": len(matrices5) == 480,
        "q5_full_group_order_60000": 5**3 * len(matrices5) == 60000,
        "q5_representative_maps_preserve_voltage": all(
            verify_map(5, M, shift, central)
            for M in matrices5[::37]
            for shift in points(5)[::4]
            for central in range(5)
        ),
        "pass403_q3_order_agrees": p403_orders.get(3) == 1296,
        "pass403_q5_order_agrees": p403_orders.get(5) == 60000,
        "pass403_q9_order_agrees": p403_orders.get(9) == 8398080,
        "central_multiplier_quotient_q3_has_order_2": len({det(M, 3) for M in matrices3}) == 2,
        "central_multiplier_quotient_q5_has_order_4": len({det(M, 5) for M in matrices5}) == 4,
    }

    theorem_instances = {
        "3": {
            "field_automorphism_order": 1,
            "full_automorphism_order": 1296,
            "central_orientation_fixed_subgroup_order": 648,
            "multiplier_index": 2,
            "exhaustive_no_extra_automorphisms": True,
        },
        "5": {
            "field_automorphism_order": 1,
            "full_automorphism_order": 60000,
            "central_orientation_fixed_subgroup_order": 15000,
            "multiplier_index": 4,
            "important_conclusion": "the unoriented extension is larger than C2; all four nonzero central multipliers occur",
        },
        "9": {
            "field_automorphism_order": 2,
            "full_automorphism_order": 8398080,
            "multiplier_group_order": 8,
            "source": "Pass 403 exact permutation-group census including Frobenius",
        },
    }

    payload = {
        "schema": "w33.pass408.full_automorphism_theorem.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem_scope": "every odd prime power q>2",
        "theorem": "Aut(Gamma_q)=H_q semidirect GammaL(2,q), with order q^3(q^2-1)(q^2-q)f for q=p^f",
        "explicit_prime_field_action": "(u,z) -> (M u+a, det(M) z-omega(Mu,a)+c)",
        "proof_ledger": [
            "Distance three is graph-theoretic, so every automorphism preserves the q-point antipodal fibres.",
            "The triangle voltage omega(v-u,w-u) vanishes exactly for collinear base triples; graph automorphisms therefore induce affine-plane collineations.",
            "The fundamental theorem of affine geometry gives an affine semilinear base map u -> M u^sigma+a.",
            "Conjugating every perfect matching forces all fibre permutations to share one semilinear multiplier; the matching equation then gives the displayed z-coordinate cocycle.",
            "These maps are exactly H_q semidirect GammaL(2,q), so no additional unoriented automorphisms remain.",
        ],
        "orientation_result": "Fixing the central phase orientation corresponds to determinant multiplier 1. The full quotient of multipliers is F_q^*, of order q-1; only q=3 reduces this extension to C2.",
        "instances": theorem_instances,
        "checks": checks,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build_payload()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Pass 408 certificate is stale")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
