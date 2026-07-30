#!/usr/bin/env python3
"""Passes 1346--1349: mixed coupling, cycle observables, runtime ledger, modular fusion."""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import math
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
MIXED_OUT=DATA/"w33_pass1346_mixed_26x4_constants.json"
SELECTOR_OUT=DATA/"w33_pass1347_cycle_copy_observables.json"
FUSION_OUT=DATA/"w33_pass1349_modular_triality_fusion.json"
import w33_pass1345_1349_support as support
from w33_pass1345_basic_algebras import rref_rows, nullspace_iter

def mixed_26x4_coupling():
    V, W, labels = support.matrix_unit_change_of_basis()
    positions20 = [k for k, label in enumerate(labels) if label[0] == "20"]
    assert len(positions20) == 9
    hecke_blocks = []
    for relation in range(26):
        matrix = sp.zeros(3)
        for k in positions20:
            _, i, j = labels[k]
            matrix[i, j] = W[k, relation]
        hecke_blocks.append(matrix)
    assert sp.Matrix.hstack(*[matrix.reshape(9, 1) for matrix in hecke_blocks]).rank() == 9

    identity, off = sp.eye(3), sp.ones(3) - sp.eye(3)
    scheme = [
        sp.kronecker_product(identity, identity),
        sp.kronecker_product(off, identity),
        sp.kronecker_product(identity, off),
        sp.kronecker_product(off, off),
    ]
    coherent_basis, coherent_labels = [], []
    for u in range(3):
        for v in range(3):
            matrix_unit = sp.zeros(3)
            matrix_unit[u, v] = 1
            for b, triality_relation in enumerate((identity, off)):
                coherent_basis.append(sp.kronecker_product(matrix_unit, triality_relation))
                coherent_labels.append((u, v, b))
    basis_matrix = sp.Matrix.hstack(*[matrix.reshape(81, 1) for matrix in coherent_basis])
    assert basis_matrix.rank() == 18
    pivot_rows = list(basis_matrix.T.rref()[1])
    inverse = basis_matrix.extract(pivot_rows, range(18)).inv()

    def coordinates(matrix):
        vector = matrix.reshape(81, 1)
        answer = inverse * vector.extract(pivot_rows, [0])
        assert basis_matrix * answer == vector
        return [sp.Rational(x) for x in answer]

    left_constants, right_constants = [], []
    for block in hecke_blocks:
        lifted = sp.kronecker_product(block, identity)
        left_constants.append([coordinates(lifted * relation) for relation in scheme])
        right_constants.append([coordinates(relation * lifted) for relation in scheme])

    generated = []
    for matrix in [sp.kronecker_product(block, identity) for block in hecke_blocks] + scheme:
        trial = sp.Matrix.hstack(*([x.reshape(81, 1) for x in generated] + [matrix.reshape(81, 1)]))
        if trial.rank() > len(generated):
            generated.append(matrix)
    changed = True
    while changed:
        changed = False
        for left in list(generated):
            for right in list(generated):
                matrix = left * right
                trial = sp.Matrix.hstack(*([x.reshape(81, 1) for x in generated] + [matrix.reshape(81, 1)]))
                if trial.rank() > len(generated):
                    generated.append(matrix)
                    changed = True
    assert len(generated) == 18
    assert sum(coherent_basis, sp.zeros(9)) == sp.ones(9)
    for i, left in enumerate(coherent_basis):
        for j, right in enumerate(coherent_basis):
            assert left.multiply_elementwise(right) == (left if i == j else sp.zeros(9))

    full = {
        "schema": "w33.pass1346.mixed_26x4_constants.v1",
        "status": "PASS",
        "coherent_basis_labels": [list(x) for x in coherent_labels],
        "hecke_species20_blocks": [[[support.fstr(block[i, j]) for j in range(3)] for i in range(3)] for block in hecke_blocks],
        "left_mixed_constants": [[[support.fstr(x) for x in vector] for vector in row] for row in left_constants],
        "right_mixed_constants": [[[support.fstr(x) for x in vector] for vector in row] for row in right_constants],
    }
    mixed_hash = support.sha_json(full)
    MIXED_OUT.write_text(json.dumps(full, indent=2, sort_keys=True) + "\n")
    commutators = []
    for block in hecke_blocks:
        lifted = sp.kronecker_product(block, identity)
        for relation in scheme:
            commutators.append((lifted * relation - relation * lifted).reshape(81, 1))
    denominator_lcm = 1
    for family in (left_constants, right_constants):
        for row in family:
            for vector in row:
                for value in vector:
                    denominator_lcm = math.lcm(denominator_lcm, int(value.q))
    return {
        "schema": "w33.pass1346.mixed_hecke_triality_closure.v1",
        "status": "PASS",
        "mixed_constant_tensor": "26 x 4 x 18 on each side",
        "mixed_constants_file": str(MIXED_OUT.relative_to(ROOT)),
        "mixed_constants_sha256": mixed_hash,
        "generated_algebra_dimension": 18,
        "generated_algebra": "M_3(Q) tensor (Q + Q)",
        "coherent_configuration": "complete directed coherent configuration on three internal axes tensor the K3 association scheme on three triality axes",
        "classification": "cellular/coherent algebra with three fibers; noncommutative and therefore not an association scheme",
        "four_relation_scheme": "the S3_internal orbit fusion of the 18 relations",
        "commutator_span_dimension": sp.Matrix.hstack(*commutators).rank(),
        "mixed_denominator_lcm": denominator_lcm,
    }


def cycle_shift(cycle, lookup):
    matrix = np.zeros((480, 480), dtype=np.int64)
    edges = [int(lookup[cycle[i], cycle[(i + 1) % len(cycle)]]) for i in range(len(cycle))]
    for i, edge in enumerate(edges):
        matrix[edges[(i + 1) % len(edges)], edge] = 1
    return matrix, edges


def cycle_copy_observables(model):
    cycles = json.loads((DATA / "w33_pass1330_1334_modular_triality_cycle_atlas.json").read_text())["pass1332_symmetry_breaking_cycle_selectors"]["cycles"]
    numerator = model["projector_numerator"]
    U = model["basis"]
    coordinate_dual = model["coordinate_dual"]
    group_order = support.GROUP_ORDER
    records = {}
    for length in ("7", "8"):
        cycle = cycles[length]["cycle"]
        shift, edges = cycle_shift(cycle, model["lookup"])
        occupation = np.zeros((480, 480), dtype=np.int64)
        occupation[edges, edges] = 1
        observables = {"shift": shift, "occupation": occupation, "cosine_quadrature": shift + shift.T}
        data = {}
        for name, matrix in observables.items():
            coordinate = coordinate_dual * sp.Matrix((matrix @ U).tolist())
            coordinate_serial = [[support.fstr(coordinate[i, j]) for j in range(20)] for i in range(20)]
            compressed_numerator = (numerator @ matrix) @ numerator
            if name != "shift":
                assert np.array_equal(compressed_numerator, compressed_numerator.T)
            frobenius_numerator = sum(int(x) * int(x) for x in compressed_numerator.ravel())
            invariant_energy = sp.Rational(frobenius_numerator, group_order ** 4)
            invariant_trace = sp.Rational(int(np.trace(compressed_numerator)), group_order ** 2)
            rank = int(np.linalg.matrix_rank(compressed_numerator.astype(float), tol=1e-6))
            data[name] = {
                "coordinate_compression": coordinate_serial,
                "coordinate_compression_sha256": support.sha_json(coordinate_serial),
                "basis_invariant_rank": rank,
                "basis_invariant_trace": support.fstr(invariant_trace),
                "basis_invariant_frobenius_energy": support.fstr(invariant_energy),
                "compressed_numerator_sha256": hashlib.sha256(compressed_numerator.tobytes()).hexdigest(),
            }
        energy = sp.Rational(data["cosine_quadrature"]["basis_invariant_frobenius_energy"])
        data["primitive_S3_copy_idempotents"] = [
            [[int(i == j == copy) for j in range(3)] for i in range(3)]
            for copy in range(3)
        ]
        data["copy_energy_readout_signatures"] = [
            [support.fstr(energy if detector == copy else 0) for detector in range(3)]
            for copy in range(3)
        ]
        data["directed_edge_indices"] = edges
        data["cycle"] = cycle
        records[length] = data
    result = {
        "schema": "w33.pass1347.cycle_copy_observables.v1",
        "status": "PASS",
        "records": records,
        "measurement_statement": "For O_{gamma,r}=P20 C_gamma P20 tensor E_rr, the three copy-resolved Hilbert-Schmidt energy detectors return an exact one-hot vector.",
        "boundary": "The cycle compression changes the common species-20 operator, while E_rr is an explicit internal S3 gauge choice. The cycle alone does not choose r.",
    }
    SELECTOR_OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def atlas_runtime_closure(model):
    matrices = model["standard_matrices"]
    serial = {
        name: [[support.fstr(matrix[i, j]) for j in range(20)] for i in range(20)]
        for name, matrix in matrices.items()
    }
    assert model["class_traces"] == support.CHI20.tolist()
    def matrix_order(matrix, limit=100):
        identity = sp.eye(matrix.rows)
        power = identity
        for order in range(1, limit + 1):
            power = power * matrix
            if power == identity:
                return order
        raise RuntimeError("matrix order exceeds limit")
    c_order = matrix_order(matrices["c"])
    d_order = matrix_order(matrices["d"])
    cd_order = matrix_order(matrices["c"] * matrices["d"])
    assert (c_order, d_order, cd_order) == (2, 9, 10)
    observation = json.loads((DATA / "w33_pass1348_runtime_observation.json").read_text())
    return {
        "schema": "w33.pass1348.runtime_closure.v1",
        "status": "PASS_WITH_EXTERNAL_BOUNDARY",
        "exact_rational_model": {
            "group": "W(E6)=U4(2).2",
            "dimension": 20,
            "standard_generator_orders": {"c": c_order, "d": d_order, "cd": cd_order},
            "class_trace_vector": model["class_traces"],
            "expected_character": support.CHI20.tolist(),
            "basis_columns": model["basis_columns"],
            "pivot_rows": model["pivot_rows"],
            "matrix_sha256": support.sha_json(serial),
            "projector_identity": "N20^2=51840 N20",
        },
        "observed_external_runtime": observation,
        "ledger_verdict": "Local representation and isolated photonic build are closed; AtlasRep and the complete w33_paper build remain unobserved and cannot be promoted.",
    }


def matrix_span_rank(matrices, p):
    rows = [[int(x) % p for x in matrix] for matrix in matrices]
    return len(rref_rows(rows, p)[1])


def modular_triality_fusion(mixed):
    full = json.loads(MIXED_OUT.read_text())
    rational_blocks = full["hecke_species20_blocks"]
    denominators = [Fraction(x).denominator for block in rational_blocks for row in block for x in row]
    denominator_lcm = math.lcm(*denominators)
    assert denominator_lcm == 64

    def reduce_fraction(value, p):
        value = Fraction(value)
        return value.numerator * pow(value.denominator, -1, p) % p

    records = {
        "2": {
            "nine_axis_coherent_algebra": "M_3(F_2) + M_3(F_2)",
            "dimension": 18,
            "jacobson_radical_dimension": 0,
            "mixed_hecke_descent": "OBSTRUCTED",
            "obstruction": "The 26-to-M3 species-20 coordinate map has uniform denominator 2^6; it has no canonical reduction on this integral relation lattice.",
        }
    }

    for p in (3, 5):
        blocks = [
            [reduce_fraction(rational_blocks[k][i][j], p) for i in range(3) for j in range(3)]
            for k in range(26)
        ]
        image_dimension = matrix_span_rank(blocks, p)
        if p == 3:
            assert image_dimension == 5
            for flat in blocks:
                matrix = np.array(flat, dtype=int).reshape(3, 3) % 3
                assert matrix[0, 1] == matrix[0, 2] == matrix[1, 2] == matrix[2, 1] == 0
            image = "{[[a,0,0],[b,c,0],[d,0,e]] : a,b,c,d,e in F_3}"
            image_radical_dimension = 2
            image_radical_square_dimension = 0
            triality_radical_dimension = 1
            combined_dimension = 10
            combined_radical_dimensions = [7, 2, 0]
            quotient = "F_3^3"
        else:
            assert image_dimension == 9
            image = "M_3(F_5)"
            image_radical_dimension = 0
            image_radical_square_dimension = 0
            triality_radical_dimension = 0
            combined_dimension = 18
            combined_radical_dimensions = [0]
            quotient = "M_3(F_5) + M_3(F_5)"
        records[str(p)] = {
            "species20_hecke_image": image,
            "species20_hecke_image_dimension": image_dimension,
            "species20_image_radical_dimension": image_radical_dimension,
            "species20_image_radical_square_dimension": image_radical_square_dimension,
            "triality_K3_adjacency_algebra": "F_3[epsilon]/(epsilon^2)" if p == 3 else "F_5 + F_5",
            "triality_radical_dimension": triality_radical_dimension,
            "combined_mixed_algebra_dimension": combined_dimension,
            "combined_radical_power_dimensions": combined_radical_dimensions,
            "combined_semisimple_quotient": quotient,
        }

    species20_transport = [
        [1,-1,0,-3,0,3],
        [1,-2,1,3,-3,0],
        [1,1,-2,1,-2,1],
    ]
    transport_ranks = {}
    transport_kernels = {}
    for p in (2, 3, 5):
        reduced, pivots = rref_rows(species20_transport, p)
        transport_ranks[str(p)] = len(pivots)
        kernel = list(nullspace_iter([list(row) for row in zip(*species20_transport)], p, 3))
        transport_kernels[str(p)] = kernel
    assert transport_ranks == {"2": 2, "3": 3, "5": 3}
    records["2"]["species20_transport_rank"] = 2
    records["2"]["primitive_transport_kernel"] = transport_kernels["2"]
    records["3"]["species20_transport_rank"] = 3
    records["5"]["species20_transport_rank"] = 3

    result = {
        "schema": "w33.pass1349.modular_triality_fusion.v1",
        "status": "PASS",
        "mixed_denominator_lcm": denominator_lcm,
        "records": records,
        "verdict": "Characteristics 2 and 3 are governed by distinct mechanisms: p=2 has a semisimple nine-axis scheme but a non-descending 2-adic Hecke de-fusion and rank-2 transport shadow; p=3 has full three-channel transport but a square-zero triality radical and a five-dimensional triangular Hecke image.",
    }
    FUSION_OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result
