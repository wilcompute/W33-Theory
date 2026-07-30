#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction
import hashlib
import numpy as np
import sympy as sp
import w33_pass1315_1319_exact_frontiers as prior
from w33_pass1320_1324_common import COMMON_SPECIES,RelationAlgebra,fstr
from w33_pass1320_1324_transport_core import algebra_action_on_hom,x_composition_tensor
def matrix_unit_coordinates_to_blocks(
    coordinates: list[Fraction], ordered_labels: list[tuple[str, int, int]]
) -> dict[str, list[list[Fraction]]]:
    multiplicities = {}
    for name, i, j in ordered_labels:
        multiplicities[name] = max(multiplicities.get(name, 0), i + 1, j + 1)
    blocks = {
        name: [[Fraction(0) for _ in range(m)] for _ in range(m)]
        for name, m in multiplicities.items()
    }
    for coefficient, (name, i, j) in zip(coordinates, ordered_labels):
        blocks[name][i][j] = coefficient
    return blocks


def composition_and_linking(
    alg: RelationAlgebra,
    hecke: dict,
    transport: dict,
    left_action: np.ndarray,
    projections: dict[str, list[list[Fraction]]],
    matrix_units: dict,
    channels: list[dict],
) -> dict:
    x_tensor = x_composition_tensor(hecke, transport)
    x_blocks = {}
    x_vectors = []
    for i in range(6):
        for j in range(6):
            relation_vector = [Fraction(int(x)) for x in x_tensor[i, j]]
            coordinates = matrix_units["coordinates"](relation_vector)
            blocks = matrix_unit_coordinates_to_blocks(
                coordinates, matrix_units["ordered_labels"]
            )
            # Only common support can survive.
            for name, matrix in blocks.items():
                if name not in COMMON_SPECIES:
                    assert all(x == 0 for row in matrix for x in row)
            x_blocks[f"{i},{j}"] = {
                name: [[fstr(x) for x in row] for row in blocks[name]]
                for name in COMMON_SPECIES
            }
            x_vectors.append(relation_vector)

    # Right compositions T_i^* T_j are scalar on the four common Y species.
    y_scalars = {}
    for i in range(6):
        for j in range(6):
            entry = {}
            for name in COMMON_SPECIES:
                degree = prior.IRR_BY_NAME[name][0]
                scalar = projections[name][i][j] * transport["sizes"][j] / degree
                entry[name] = scalar
            y_scalars[f"{i},{j}"] = entry

    # Exact associativity of the linking products.
    for i in range(6):
        for j in range(6):
            x_product = [Fraction(int(x)) for x in x_tensor[i, j]]
            for k in range(6):
                left = algebra_action_on_hom(
                    x_product,
                    [Fraction(int(t == k)) for t in range(6)],
                    left_action,
                )
                right = [Fraction(0) for _ in range(6)]
                for name in COMMON_SPECIES:
                    scalar = y_scalars[f"{j},{k}"][name]
                    for target in range(6):
                        right[target] += scalar * projections[name][i][target]
                assert left == right, (i, j, k)

    x_span = sp.Matrix.hstack(
        *(alg.to_sympy(vector) for vector in x_vectors)
    ).rank()
    y_rows = []
    for i in range(6):
        for j in range(6):
            y_rows.append([y_scalars[f"{i},{j}"][name] for name in COMMON_SPECIES])
    y_span = sp.Matrix(
        [[sp.Rational(x.numerator, x.denominator) for x in row] for row in y_rows]
    ).rank()
    assert x_span == 12
    assert y_span == 4

    # Each aligned channel is an exact scaled partial isometry.
    channel_checks = []
    for channel in channels:
        q = channel["orbital_coefficients"]
        alpha = channel["squared_singular_scale"]
        name = channel["species"]
        copy = channel["copy"]
        x_relation = [Fraction(0) for _ in range(26)]
        for i in range(6):
            for j in range(6):
                if q[i] and q[j]:
                    for relation in range(26):
                        x_relation[relation] += q[i] * q[j] * int(x_tensor[i, j, relation])
        expected_x = alg.scale(
            matrix_units["units"][name][(copy, copy)], alpha
        )
        assert x_relation == expected_x
        y_entry = {}
        for species in COMMON_SPECIES:
            scalar = Fraction(0)
            for i in range(6):
                for j in range(6):
                    scalar += q[i] * q[j] * y_scalars[f"{i},{j}"][species]
            y_entry[species] = scalar
        assert y_entry[name] == alpha
        assert all(
            value == 0 for species, value in y_entry.items() if species != name
        )
        channel_checks.append(
            {
                "species": name,
                "copy": copy,
                "T_Tstar": f"{fstr(alpha)} * E_{name}[{copy},{copy}]",
                "Tstar_T": f"{fstr(alpha)} * P_{name}^{chr(89)}",
            }
        )

    linking_dimension = x_span + y_span + 2 * 6
    assert linking_dimension == 28
    return {
        "x_side_relation_tensor_sha256": hashlib.sha256(x_tensor.tobytes()).hexdigest(),
        "x_side_products_in_hecke_matrix_units": x_blocks,
        "x_side_product_span_dimension": x_span,
        "y_side_products_in_species_refined_hashimoto_basis": {
            key: {name: fstr(value) for name, value in entry.items()}
            for key, entry in y_scalars.items()
        },
        "y_side_product_span_dimension": y_span,
        "aligned_channel_partial_isometries": channel_checks,
        "linking_associativity_verified": True,
        "common_support_left_algebra": "C + C + M_3(C) + C",
        "common_support_right_algebra": "C^4",
        "hom_bimodule": "C + C + C^3 + C",
        "linking_algebra": "M_2(C) + M_2(C) + M_4(C) + M_2(C)",
        "linking_algebra_dimension": linking_dimension,
        "species20_morita_context": "M_3(C) -- C^3 -- C is full; the three channels generate both support algebras.",
    }


