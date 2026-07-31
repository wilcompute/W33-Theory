#!/usr/bin/env python3
"""Derived exact Passes 1516--1520 from frozen selector certificates.

This worker intentionally uses only compact, already-frozen exact certificates.
It does not rerun the expensive 83-dimensional orbital-algebra construction.
Every new statement is either an exact algebraic consequence of those certificates
or is marked as a remaining boundary.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE1500 = ROOT / "data" / "w33_pass1500_1504_five_frontiers.json"
BASE1370 = ROOT / "data" / "w33_pass1370_1374_five_frontiers.json"
OUT = ROOT / "data" / "w33_pass1516_1520_five_frontiers.json"
EXPECTED_BASE_HASHES = {
    "1500_1504_sha256": "757b01bacbfc157484851ec76cc3322204116c3aeb9cdf81851a2dbee1a56b3e",
    "1370_1374_sha256": "284d9d7f9462a83f0709734d48a3ccf3284da2cb6b5ede159da5c719b84332b9",
}

P2_DEGREES = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3]
P3_DEGREES = [1, 1, 1, 2, 2]
MASKS = [
    (1, 1, 1, 0), (1, 1, 0, 1), (1, 0, 1, 1), (0, 1, 1, 1),
    (1, 1, 0, 0), (1, 0, 0, 1), (0, 1, 1, 0), (0, 0, 1, 1),
]


def sha(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def matmul(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    return [
        [sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def weighted(A: list[list[int]], d: list[int]) -> int:
    return sum(d[i] * A[i][j] * d[j] for i in range(len(d)) for j in range(len(d)))


def identity(n: int) -> list[list[int]]:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def connected_components(A: list[list[int]]) -> list[list[int]]:
    n = len(A)
    unseen = set(range(n))
    out = []
    while unseen:
        seed = min(unseen)
        comp = {seed}
        stack = [seed]
        unseen.remove(seed)
        while stack:
            i = stack.pop()
            for j in range(n):
                if (A[i][j] or A[j][i]) and j in unseen:
                    unseen.remove(j)
                    comp.add(j)
                    stack.append(j)
        out.append(sorted(comp))
    return out


def relation_frontier(A: list[list[int]], d: list[int], layers: list[int]) -> dict:
    powers = identity(len(A))
    path_dims = []
    graded_dims = []
    kernel_dims = []
    for n, layer in enumerate(layers):
        if n:
            powers = matmul(powers, A)
        p = weighted(powers, d)
        path_dims.append(p)
        graded_dims.append(layer)
        kernel_dims.append(p - layer)
    powers = matmul(powers, A)
    terminal_path = weighted(powers, d)
    path_dims.append(terminal_path)
    graded_dims.append(0)
    kernel_dims.append(terminal_path)
    assert kernel_dims[0] == kernel_dims[1] == 0
    assert all(x >= 0 for x in kernel_dims)
    comps = connected_components(A)
    component_records = []
    for comp in comps:
        semisimple = sum(d[i] ** 2 for i in comp)
        radical_head = sum(A[i][j] * d[i] * d[j] for i in comp for j in comp)
        component_records.append({
            "vertices": comp,
            "simple_degrees": [d[i] for i in comp],
            "semisimple_dimension": semisimple,
            "radical_head_dimension": radical_head,
        })
    return {
        "simple_degrees": d,
        "connected_components": component_records,
        "tensor_path_dimensions_degrees_0_through_loewy": path_dims,
        "associated_graded_radical_layer_dimensions": graded_dims,
        "relation_kernel_dimensions": kernel_dims,
        "quadratic_path_dimension": path_dims[2],
        "quadratic_radical_layer_dimension": graded_dims[2],
        "quadratic_relation_dimension": kernel_dims[2],
        "interpretation": (
            "For S=A/J and B=J/J^2, the canonical tensor-algebra map "
            "T_S(B) -> gr_J(A) is surjective. The listed kernel dimensions are "
            "therefore exact homogeneous relation-space dimensions."
        ),
        "boundary": (
            "These are relation spaces in the radical-associated graded algebra. "
            "They do not by themselves separate minimal higher-degree generators "
            "from consequences of lower-degree relations, and they do not yet give "
            "the complete Ext^2/Yoneda multiplication table."
        ),
    }


def d4_permutations() -> list[tuple[int, ...]]:
    out = set()
    for k in range(4):
        out.add(tuple((i + k) % 4 for i in range(4)))
        out.add(tuple((k - i) % 4 for i in range(4)))
    assert len(out) == 8
    return sorted(out)


def permute_mask(mask: tuple[int, ...], perm: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(mask[perm[i]] for i in range(4))


def mask_orbits() -> list[list[list[int]]]:
    perms = d4_permutations()
    remaining = set(MASKS)
    orbits = []
    while remaining:
        seed = min(remaining)
        orb = {permute_mask(seed, p) for p in perms}
        orb &= set(MASKS)
        remaining -= orb
        orbits.append([list(x) for x in sorted(orb)])
    return sorted(orbits, key=lambda o: (len(o), o))


def build() -> dict:
    base1500 = json.loads(BASE1500.read_text())
    base1370 = json.loads(BASE1370.read_text())

    ext = base1500["pass1500_modular_ext_quivers"]
    p2 = relation_frontier(ext["p2_ext1_matrix"], P2_DEGREES, ext["p2_loewy_layers"])
    p3 = relation_frontier(ext["p3_ext1_matrix"], P3_DEGREES, ext["p3_loewy_layers"])
    assert p2["quadratic_relation_dimension"] == 29
    assert p3["quadratic_relation_dimension"] == 70
    assert sum(x["semisimple_dimension"] for x in p2["connected_components"]) == 38
    assert sum(x["radical_head_dimension"] for x in p2["connected_components"]) == 29
    assert sum(x["semisimple_dimension"] for x in p3["connected_components"]) == 11
    assert sum(x["radical_head_dimension"] for x in p3["connected_components"]) == 23

    fourier = base1500["pass1501_tensor_fourier"]
    pairs = fourier["multiplicity_irreducible_pairs"]
    multiplicities = [x[0] for x in pairs]
    degrees = [x[1] for x in pairs]
    ranks = [m * d for m, d in pairs]
    commutant_dim = sum(m * m for m in multiplicities)
    image_dim = sum(d * d for d in degrees)
    module_dim = sum(ranks)
    factorization_gauge_dim = commutant_dim + image_dim - len(pairs)
    assert module_dim == 120 and commutant_dim == 83
    assert ranks == fourier["block_dimensions"]

    bridge = base1500["pass1502_bridge_classification"]
    orbits = mask_orbits()
    assert [len(x) for x in orbits] == [4, 4]
    sheet_counts = {int(k): v for k, v in bridge["sheet_rank_distribution"].items()}
    bridge_counts = {int(k): v for k, v in bridge["bridge_rank_distribution"].items()}
    sheet_obstruction = {str(k): v % 4 for k, v in sorted(sheet_counts.items())}
    assert sheet_obstruction == {"70": 0, "76": 1, "81": 3}
    assert all(v % 4 == 0 for v in bridge_counts.values())

    over = base1500["pass1503_maximal_overorder"]
    e2 = over["global_index_factorization"]["2"]
    e3 = over["global_index_factorization"]["3"]
    N = (2 ** e2) * (3 ** e3)
    assert str(N) == over["global_index"]
    rational_blocks = [1] * 7 + [2] * 2 + [3] * 3 + [4, 5]
    assert sum(n * n for n in rational_blocks) == 83

    linking = base1500["pass1504_linking_algebra"]
    natural = base1370["pass1374_selector_levi_bimodule_boundary"]
    n, m = 120, 81
    assert linking["left_corner_dimension"] == n * n
    assert linking["right_corner_dimension"] == m * m
    assert linking["bridge_bimodule_dimension"] == n * m
    assert natural["steinberg_81_channel_present"] is False

    result = {
        "schema": "w33.pass1516_1520.five_frontiers.v1",
        "status": "PASS",
        "base_certificates": dict(EXPECTED_BASE_HASHES),
        "pass1516_radical_graded_relations": {
            "theorem": "Exact tensor-algebra relation defects in characteristics 2 and 3",
            "p2": p2,
            "p3": p3,
            "headline": (
                "The quadratic multiplication kernels have dimensions 29 at p=2 "
                "and 70 at p=3. Characteristic 3 has the substantially denser "
                "relation ideal already in degree two."
            ),
        },
        "pass1517_coordinate_free_fourier": {
            "theorem": "Basis-free double-centralizer form of the selector Fourier decomposition",
            "isotypic_count": len(pairs),
            "multiplicity_irreducible_pairs": pairs,
            "canonical_isotypic_ranks": ranks,
            "module_dimension_sum_m_times_d": module_dim,
            "selector_commutant_dimension_sum_m_squared": commutant_dim,
            "dual_image_dimension_sum_d_squared": image_dim,
            "tensor_factorization_gauge_group_dimension": factorization_gauge_dim,
            "canonical_evaluation_map": "direct_sum Hom_H(W_chi,V) tensor W_chi -> V",
            "coordinate_free_content": (
                "The fourteen central isotypic summands and the evaluation isomorphism "
                "are canonical. A Fourier matrix is only a choice of bases in the two "
                "factors of each summand."
            ),
            "boundary": (
                "The frozen U and U^{-1} hashes certify one deterministic trivialization, "
                "not an invariant under arbitrary changes of models for the irreducibles."
            ),
        },
        "pass1518_apartment_d4_obstruction": {
            "theorem": "Cardinality obstruction to a global rank-preserving D4 lift",
            "local_mask_orbits": orbits,
            "local_mask_orbit_sizes": [len(x) for x in orbits],
            "sheet_rank_distribution": {str(k): v for k, v in sorted(sheet_counts.items())},
            "sheet_rank_count_mod_4": sheet_obstruction,
            "global_rank_preserving_d4_lift_exists": False,
            "proof": (
                "Every orbit of any D4-action on the 24 sheets that projects to the "
                "standard action on masks must project onto a four-element mask orbit, "
                "so each invariant rank level must have cardinality divisible by four. "
                "The unique rank-76 sheet violates this necessary condition."
            ),
            "sign_extended_bridge_distribution": {str(k): v for k, v in sorted(bridge_counts.items())},
            "bridge_census_alone_has_cardinality_obstruction": False,
            "correct_symmetry_object": (
                "Local D4 transport must be chart-dependent (an action groupoid with a "
                "residual-label cocycle), or it must leave the frozen 24-sheet family."
            ),
            "boundary": (
                "The cardinality argument proves nonexistence of a global rank-preserving "
                "lift. It does not compute the full rectangle-by-rectangle S3 residual cocycle."
            ),
        },
        "pass1519_maximal_order_arithmetic": {
            "theorem": "Prime support, conductor bound, and componentwise class triviality",
            "maximal_order_block_sizes": rational_blocks,
            "z_rank": sum(n * n for n in rational_blocks),
            "index": str(N),
            "local_defect_lengths": {"2": e2, "3": e3},
            "orbital_discriminant_valuations": {"2": 2 * e2, "3": 2 * e3},
            "good_local_primes": "all primes other than 2 and 3",
            "local_equality_away_from_2_3": True,
            "conductor_support_subset": [2, 3],
            "annihilator_bound": f"({N}) M_O is contained in the conductor f=(O:M_O)",
            "componentwise_labeled_locally_free_class_group": "trivial",
            "componentwise_reason": "Each labeled block M_n(Z) is Morita equivalent to Z, whose ideal class group is trivial.",
            "unlabeled_equal_block_permutation_group_order": 60480,
            "boundary": (
                "The index and discriminant determine prime support and total local lengths, "
                "but not the blockwise conductor exponents, Bass/Eichler status, or the Smith "
                "invariants of M_O/O. Those require the frozen transition matrix itself."
            ),
        },
        "pass1520_equivariant_morita": {
            "theorem": "The saturated full-matrix Morita context is G-equivariant; the fixed-bridge obstruction is not a Morita obstruction",
            "selector_dimension": n,
            "signed_steinberg_dimension": m,
            "left_algebra": "End_Q(V) = M_120(Q)",
            "right_algebra": "End_Q(W) = M_81(Q)",
            "equivalence_bimodule": "X = Hom_Q(W,V)",
            "inverse_bimodule": "Y = Hom_Q(V,W)",
            "equivalence_bimodule_dimension": n * m,
            "pairing_witnesses": {
                "End_V_matrix_unit": "E_ij = x_i0 y_0j",
                "End_W_matrix_unit": "F_ab = y_a0 x_0b",
            },
            "G_action": "g.x = rho_V(g) x rho_W(g)^(-1), and similarly on Y",
            "pairings_G_equivariant": True,
            "strict_G_equivariant_Morita_context": True,
            "equivariant_Brauer_obstruction": "zero",
            "G_fixed_cross_map_present": False,
            "fixed_cross_map_interpretation": (
                "Hom_G(W,V)=0 forbids a G-fixed bridge element. It does not forbid the "
                "full Hom(W,V) space from being a G-equivariant equivalence bimodule."
            ),
            "apartment_generator_span_dimension": linking["independent_bridge_dimension"],
            "saturated_bimodule_dimension": linking["bridge_bimodule_dimension"],
            "upgrade": (
                "Pass 1504's 75 gauge bridges are a generating frame, not an invariant "
                "bimodule. Their corner saturation is the full Hom(W,V), which is canonically "
                "G-stable and supplies the equivariant Morita equivalence."
            ),
            "boundary": (
                "This does not make any individual apartment bridge G-invariant, nor does it "
                "supply a preferred G-fixed identification between V and W (their dimensions differ)."
            ),
        },
    }
    result["sha256"] = sha(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    got = build()
    encoded = json.dumps(got, indent=2, sort_keys=True) + "\n"
    if args.write:
        OUT.write_text(encoded)
    if args.check:
        assert hashlib.sha256(BASE1500.read_bytes()).hexdigest() == EXPECTED_BASE_HASHES["1500_1504_sha256"]
        assert hashlib.sha256(BASE1370.read_bytes()).hexdigest() == EXPECTED_BASE_HASHES["1370_1374_sha256"]
        expected = json.loads(OUT.read_text())
        assert got == expected
        print("PASS Passes 1516-1520 derived certificate", got["sha256"])
    elif not args.write:
        print(encoded, end="")


if __name__ == "__main__":
    main()
