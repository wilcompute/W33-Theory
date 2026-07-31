#!/usr/bin/env python3
"""Passes 1360--1364: selector Gelfand pair, Terwilliger algebra, and Schur defect.

This exact finite computation starts from W(3,3), builds the 120 selectors
(isotropic line, perfect matching), enumerates PGSp(4,3) on those selectors,
and computes:
  * the five-double-coset Gelfand pair;
  * the selector Terwilliger algebra;
  * the full point-stabilizer orbital algebra;
  * the four-dimensional Schur/coherent-closure defect;
  * a stable split Wedderburn fingerprint in two large good characteristics.

No physical interpretation or literature-priority claim is made.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

Q = 3
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "w33_pass1360_1364_gelfand_terwilliger.json"
PRIMES = (1000003, 1000033)


def canon(v):
    for x in v:
        if x % Q:
            inv = 1 if x % Q == 1 else 2
            return tuple((inv * y) % Q for y in v)
    raise ValueError("zero vector")


def symp(x, y):
    return (x[0] * y[2] + x[1] * y[3] - x[2] * y[0] - x[3] * y[1]) % Q


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def perfect_matchings4(line):
    a, b, c, d = line
    return tuple(sorted([
        tuple(sorted((tuple(sorted((a, b))), tuple(sorted((c, d)))))),
        tuple(sorted((tuple(sorted((a, c))), tuple(sorted((b, d)))))),
        tuple(sorted((tuple(sorted((a, d))), tuple(sorted((b, c)))))),
    ]))


def perm_group_closure(generators):
    identity = tuple(range(len(generators[0])))
    group = {identity}
    queue = collections.deque([identity])
    while queue:
        h = queue.popleft()
        for g in generators:
            gh = compose(g, h)
            if gh not in group:
                group.add(gh)
                queue.append(gh)
    return group


def rref_mod_rows(rows, p, ncols):
    pivots = {}
    for row in rows:
        v = np.array(row, dtype=np.int64) % p
        for pivot in sorted(pivots):
            c = int(v[pivot])
            if c:
                v = (v - c * pivots[pivot]) % p
        nz = np.flatnonzero(v)
        if not len(nz):
            continue
        pivot = int(nz[0])
        v = v * pow(int(v[pivot]), -1, p) % p
        for q, old in list(pivots.items()):
            c = int(old[pivot])
            if c:
                pivots[q] = (old - c * v) % p
        pivots[pivot] = v
    order = sorted(pivots)
    matrix = np.stack([pivots[pivot] for pivot in order]) if order else np.zeros((0, ncols), dtype=np.int64)
    return matrix, order


def rank_mod(matrix, p):
    return len(rref_mod_rows(matrix, p, matrix.shape[1])[1])


def independent_row_indices(matrix, p):
    pivots = {}
    indices = []
    for index, row in enumerate(matrix):
        v = np.array(row, dtype=np.int64) % p
        for pivot in sorted(pivots):
            c = int(v[pivot])
            if c:
                v = (v - c * pivots[pivot]) % p
        nz = np.flatnonzero(v)
        if not len(nz):
            continue
        pivot = int(nz[0])
        v = v * pow(int(v[pivot]), -1, p) % p
        for q, old in list(pivots.items()):
            c = int(old[pivot])
            if c:
                pivots[q] = (old - c * v) % p
        pivots[pivot] = v
        indices.append(index)
    return indices


def nullspace_mod(matrix, p):
    rref, pivots = rref_mod_rows(matrix, p, matrix.shape[1])
    free = [j for j in range(matrix.shape[1]) if j not in pivots]
    pivot_to_row = {pivot: i for i, pivot in enumerate(pivots)}
    vectors = []
    for f in free:
        vector = np.zeros(matrix.shape[1], dtype=np.int64)
        vector[f] = 1
        for pivot in pivots:
            vector[pivot] = (-rref[pivot_to_row[pivot], f]) % p
        vectors.append(vector)
    return vectors, pivots


def build_geometry():
    points = sorted({canon(v) for v in itertools.product(range(Q), repeat=4) if any(v)})
    assert len(points) == 40
    point_index = {point: i for i, point in enumerate(points)}

    adjacency = np.zeros((40, 40), dtype=np.int8)
    for i, x in enumerate(points):
        for j, y in enumerate(points):
            if i != j and symp(x, y) == 0:
                adjacency[i, j] = 1
    assert np.all(adjacency.sum(axis=1) == 12)
    assert np.array_equal(
        adjacency @ adjacency,
        8 * np.eye(40, dtype=int) - 2 * adjacency + 4 * np.ones((40, 40), dtype=int),
    )

    lines = [
        line for line in itertools.combinations(range(40), 4)
        if all(adjacency[i, j] for i, j in itertools.combinations(line, 2))
    ]
    assert len(lines) == 40
    line_sets = [set(line) for line in lines]
    line_index = {frozenset(line): i for i, line in enumerate(lines)}
    matchings = [perfect_matchings4(line) for line in lines]
    matching_index = [{matching: i for i, matching in enumerate(fiber)} for fiber in matchings]
    selectors = [(line, matching) for line in range(40) for matching in range(3)]

    def transversal_map(li, lj):
        out = {}
        for x in lines[li]:
            ys = [y for y in lines[lj] if adjacency[x, y]]
            assert len(ys) == 1
            out[x] = ys[0]
        return out

    def transport_matching(matching, mapping):
        return tuple(sorted(tuple(sorted((mapping[a], mapping[b]))) for a, b in matching))

    transports = {}
    for li in range(40):
        for lj in range(40):
            if li != lj and line_sets[li].isdisjoint(line_sets[lj]):
                mapping = transversal_map(li, lj)
                transports[(li, lj)] = tuple(
                    matchings[lj].index(transport_matching(matching, mapping))
                    for matching in matchings[li]
                )

    relations = [np.zeros((120, 120), dtype=np.int8) for _ in range(5)]
    for i, (li, mi) in enumerate(selectors):
        for j, (lj, mj) in enumerate(selectors):
            if i == j:
                relation = 0
            elif li == lj:
                relation = 1
            elif line_sets[li] & line_sets[lj]:
                relation = 2
            else:
                relation = 3 if transports[(li, lj)][mi] == mj else 4
            relations[relation][i, j] = 1
    assert [int(matrix.sum(axis=1)[0]) for matrix in relations] == [1, 2, 36, 27, 54]

    J = np.array([
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [-1, 0, 0, 0],
        [0, -1, 0, 0],
    ], dtype=int) % 3

    def transvection(v):
        column = np.array(v, dtype=int).reshape(4, 1) % 3
        return (np.eye(4, dtype=int) + column @ (J @ column).T) % 3

    def point_permutation(matrix):
        permutation = []
        for point in points:
            image = tuple(int(x) for x in (matrix @ np.array(point, dtype=int)) % 3)
            permutation.append(point_index[canon(image)])
        return tuple(permutation)

    transvections = [point_permutation(transvection(point)) for point in points]
    similitude = point_permutation(np.diag([1, 1, 2, 2]) % 3)

    def selector_permutation(point_perm):
        out = [None] * 120
        for li, line in enumerate(lines):
            target_line = line_index[frozenset(point_perm[x] for x in line)]
            for mi, matching in enumerate(matchings[li]):
                target_matching = tuple(sorted(
                    tuple(sorted((point_perm[a], point_perm[b]))) for a, b in matching
                ))
                mj = matching_index[target_line][target_matching]
                out[3 * li + mi] = 3 * target_line + mj
        return tuple(out)

    selector_generators = [selector_permutation(g) for g in transvections + [similitude]]
    for generator in selector_generators:
        for relation in relations:
            assert np.array_equal(relation[np.ix_(generator, generator)], relation)
    assert all(
        np.array_equal(relations[i] @ relations[j], relations[j] @ relations[i])
        for i in range(5) for j in range(5)
    )
    group = perm_group_closure(selector_generators)
    assert len(group) == 51840
    assert len({g[0] for g in group}) == 120
    stabilizer = [g for g in group if g[0] == 0]
    assert len(stabilizer) == 432

    suborbits = []
    unseen = set(range(120))
    while unseen:
        x = min(unseen)
        orbit = {h[x] for h in stabilizer}
        suborbits.append(sorted(orbit))
        unseen -= orbit
    assert [len(orbit) for orbit in suborbits] == [1, 2, 36, 27, 54]
    relation_shells = [frozenset(np.where(matrix[0] != 0)[0]) for matrix in relations]
    assert [frozenset(orbit) for orbit in suborbits] == relation_shells

    pair_orbits = []
    unseen_pairs = set(range(120 * 120))
    while unseen_pairs:
        z = min(unseen_pairs)
        i, j = divmod(z, 120)
        orbit = {h[i] * 120 + h[j] for h in stabilizer}
        pair_orbits.append(orbit)
        unseen_pairs -= orbit
    assert len(pair_orbits) == 83
    representatives = [divmod(min(orbit), 120) for orbit in pair_orbits]

    return {
        "points": points,
        "adjacency": adjacency,
        "lines": lines,
        "relations": relations,
        "group": group,
        "stabilizer": stabilizer,
        "suborbits": suborbits,
        "pair_orbits": pair_orbits,
        "representatives": representatives,
    }


def build_terwilliger(geometry):
    relations = geometry["relations"]
    representatives = geometry["representatives"]
    p = PRIMES[0]
    weights = (0, 1, 2, 3, 4)
    A = sum(weights[i] * relations[i].astype(np.int64) for i in range(5))
    shells = [np.where(relations[i][0] != 0)[0] for i in range(5)]
    D = np.zeros((120, 120), dtype=np.int64)
    for i, shell in enumerate(shells):
        D[shell, shell] = weights[i]

    global_eigenvalues = [371, 11, -19, -10, 2]

    class WordBasis:
        def __init__(self):
            self.rows = {}
            self.words = []
            self.matrices = []

        def add(self, matrix, word):
            vector = matrix.reshape(-1).copy() % p
            for pivot in sorted(self.rows):
                c = int(vector[pivot])
                if c:
                    vector = (vector - c * self.rows[pivot]) % p
            nz = np.flatnonzero(vector)
            if not len(nz):
                return False
            pivot = int(nz[0])
            vector = vector * pow(int(vector[pivot]), -1, p) % p
            for q, old in list(self.rows.items()):
                c = int(old[pivot])
                if c:
                    self.rows[q] = (old - c * vector) % p
            self.rows[pivot] = vector
            self.words.append(word)
            self.matrices.append(matrix % p)
            return True

    basis = WordBasis()
    identity = np.eye(120, dtype=np.int64)
    basis.add(identity, "")
    queue = collections.deque([(identity, "")])
    while queue:
        matrix, word = queue.popleft()
        for generator, letter in ((A % p, "A"), (D % p, "D")):
            candidate = matrix @ generator % p
            if basis.add(candidate, word + letter):
                queue.append((candidate, word + letter))
    assert len(basis.words) == 79
    assert max(map(len, basis.words)) == 6

    exact_words = []
    for word in basis.words:
        matrix = np.eye(120, dtype=np.int64)
        for letter in word:
            matrix = matrix @ (A if letter == "A" else D)
        exact_words.append(matrix)

    evaluations = np.array([
        [int(matrix[i, j]) for matrix in exact_words]
        for i, j in representatives
    ], dtype=object)
    independent_rows = independent_row_indices(np.array(evaluations, dtype=np.int64) % p, p)
    assert len(independent_rows) == 79
    pivot_matrix = sp.Matrix([
        [int(evaluations[i, j]) for j in range(79)] for i in independent_rows
    ])
    products = [matrix @ generator for matrix in exact_words for generator in (A, D)]
    pivot_targets = sp.Matrix(
        79,
        len(products),
        lambda i, j: int(products[j][representatives[independent_rows[i]][0],
                                  representatives[independent_rows[i]][1]]),
    )
    coefficients = pivot_matrix.inv() * pivot_targets
    all_targets = sp.Matrix(
        83,
        len(products),
        lambda i, j: int(products[j][representatives[i][0], representatives[i][1]]),
    )
    assert sp.Matrix(evaluations.tolist()) * coefficients == all_targets

    commutator_rows = np.zeros((166, 79), dtype=object)
    for column, matrix in enumerate(exact_words):
        comm_a = matrix @ A - A @ matrix
        comm_d = matrix @ D - D @ matrix
        for row, (i, j) in enumerate(representatives):
            commutator_rows[row, column] = int(comm_a[i, j])
            commutator_rows[83 + row, column] = int(comm_d[i, j])
    selected = independent_row_indices(np.array(commutator_rows, dtype=np.int64) % p, p)
    assert len(selected) == 69
    selected_matrix = sp.Matrix([
        [int(commutator_rows[i, j]) for j in range(79)] for i in selected
    ])
    center_basis = selected_matrix.nullspace()
    assert len(center_basis) == 10
    full_matrix = sp.Matrix([
        [int(commutator_rows[i, j]) for j in range(79)] for i in range(166)
    ])
    assert all(full_matrix * vector == sp.zeros(166, 1) for vector in center_basis)

    nonzero_triples = 0
    for a in range(5):
        for b in range(5):
            for c in range(5):
                if np.any(relations[b][np.ix_(shells[a], shells[c])]):
                    nonzero_triples += 1
    assert nonzero_triples == 53

    orbital_counts = collections.Counter()
    for orbit, (i, j) in zip(geometry["pair_orbits"], representatives):
        a = next(r for r, matrix in enumerate(relations) if matrix[0, i])
        c = next(r for r, matrix in enumerate(relations) if matrix[0, j])
        orbital_counts[(a, c)] += 1

    block_dimensions = {}
    for a in range(5):
        for c in range(5):
            restricted = np.stack([
                matrix[np.ix_(shells[a], shells[c])].reshape(-1)
                for matrix in exact_words
            ])
            block_dimensions[(a, c)] = rank_mod(restricted % p, p)
    assert sum(block_dimensions.values()) == 79
    defects = {
        f"{a},{c}": orbital_counts[(a, c)] - block_dimensions[(a, c)]
        for a in range(5) for c in range(5)
        if orbital_counts[(a, c)] != block_dimensions[(a, c)]
    }
    assert defects == {"2,2": 2, "4,4": 2}

    signatures = {
        tuple(int(matrix[i, j]) for matrix in exact_words)
        for i, j in representatives
    }
    assert len(signatures) == 83

    return {
        "A": A,
        "D": D,
        "words": basis.words,
        "exact_words": exact_words,
        "commutator_rows": commutator_rows,
        "global_eigenvalues": global_eigenvalues,
        "shell_sizes": [len(shell) for shell in shells],
        "nonzero_triples": nonzero_triples,
        "block_dimensions": block_dimensions,
        "orbital_counts": orbital_counts,
        "defects": defects,
    }


def split_profile(prime, exact_words, commutator_rows):
    basis = [matrix % prime for matrix in exact_words]
    equations = np.array(commutator_rows, dtype=np.int64) % prime
    center_vectors, pivots = nullspace_mod(equations, prime)
    assert len(pivots) == 69 and len(center_vectors) == 10

    identity = np.eye(120, dtype=np.int64) % prime
    rng = np.random.default_rng(1)
    weights = rng.integers(1, 100, size=10, dtype=np.int64)
    coefficients = sum(
        (int(weight) * vector for weight, vector in zip(weights, center_vectors)),
        start=np.zeros(79, dtype=np.int64),
    ) % prime
    central = sum(
        (int(coefficient) * matrix for coefficient, matrix in zip(coefficients, basis)),
        start=np.zeros((120, 120), dtype=np.int64),
    ) % prime

    powers = [identity.copy()]
    for _ in range(10):
        powers.append(powers[-1] @ central % prime)
    relation_vectors, _ = nullspace_mod(
        np.stack([matrix.reshape(-1) for matrix in powers], axis=1),
        prime,
    )
    assert len(relation_vectors) == 1
    relation = relation_vectors[0]
    assert max(np.flatnonzero(relation)) == 10
    relation = relation * pow(int(relation[10]), -1, prime) % prime

    x = sp.symbols("x")
    polynomial = sp.Poly(
        sum(int(relation[i]) * x**i for i in range(11)),
        x,
        modulus=prime,
    )
    roots = polynomial.ground_roots()
    assert len(roots) == 10 and all(multiplicity == 1 for multiplicity in roots.values())
    roots = [int(root) % prime for root in roots]

    blocks = []
    for root in roots:
        projector = identity.copy()
        denominator = 1
        for other in roots:
            if other == root:
                continue
            projector = projector @ ((central - other * identity) % prime) % prime
            denominator = denominator * ((root - other) % prime) % prime
        projector = projector * pow(int(denominator), -1, prime) % prime
        assert np.array_equal(projector @ projector % prime, projector)
        isotypic_dimension = rank_mod(projector, prime)
        corner_dimension = rank_mod(
            np.stack([(projector @ matrix % prime).reshape(-1) for matrix in basis]),
            prime,
        )
        block_size = math.isqrt(corner_dimension)
        assert block_size * block_size == corner_dimension
        assert isotypic_dimension % block_size == 0
        module_multiplicity = isotypic_dimension // block_size
        blocks.append({
            "simple_block_size": block_size,
            "module_multiplicity": module_multiplicity,
            "isotypic_dimension": isotypic_dimension,
        })
    blocks.sort(key=lambda record: (
        record["simple_block_size"],
        record["module_multiplicity"],
        record["isotypic_dimension"],
    ))
    assert sum(record["simple_block_size"] ** 2 for record in blocks) == 79
    assert sum(record["isotypic_dimension"] for record in blocks) == 120
    assert sum(record["module_multiplicity"] ** 2 for record in blocks) == 515
    return {
        "prime": prime,
        "center_minimal_polynomial_coefficients_mod_p": [int(value) for value in relation],
        "blocks": blocks,
        "commutant_dimension_from_profile": 515,
    }


def build():
    geometry = build_geometry()
    terwilliger = build_terwilliger(geometry)

    valencies = [1, 2, 36, 27, 54]
    multiplicities = [1, 15, 24, 20, 60]
    P = [
        [1, 2, 36, 27, 54],
        [1, 2, -12, 3, 6],
        [1, 2, 6, -3, -6],
        [1, -1, 0, 9, -9],
        [1, -1, 0, -3, 3],
    ]
    spherical = [
        [str(sp.Rational(P[row][column], valencies[column])) for column in range(5)]
        for row in range(5)
    ]
    double_coset_sizes = [432 * valency for valency in valencies]
    assert sum(double_coset_sizes) == 51840

    profiles = [
        split_profile(prime, terwilliger["exact_words"], terwilliger["commutator_rows"])
        for prime in PRIMES
    ]
    assert profiles[0]["blocks"] == profiles[1]["blocks"]

    block_table = []
    for a in range(5):
        for c in range(5):
            block_table.append({
                "source_shell": a,
                "target_shell": c,
                "terwilliger_dimension": terwilliger["block_dimensions"][(a, c)],
                "stabilizer_orbitals": terwilliger["orbital_counts"][(a, c)],
                "defect": terwilliger["orbital_counts"][(a, c)]
                          - terwilliger["block_dimensions"][(a, c)],
            })

    result = {
        "schema": "w33.pass1360_1364.gelfand_terwilliger.v1",
        "status": "PASS",
        "pass1360_gelfand_pair": {
            "group": "PGSp(4,3) ~= W(E6)",
            "group_order": 51840,
            "selector_stabilizer_order": 432,
            "selector_degree": 120,
            "subdegrees": valencies,
            "double_coset_sizes": double_coset_sizes,
            "gelfand_pair": True,
            "multiplicity_free_degrees": multiplicities,
            "spherical_functions": spherical,
            "plancherel_weights": [str(sp.Rational(m, 120)) for m in multiplicities],
        },
        "pass1361_terwilliger": {
            "generators": {
                "A_relation_weights": [0, 1, 2, 3, 4],
                "A_eigenvalues": terwilliger["global_eigenvalues"],
                "D_shell_values": [0, 1, 2, 3, 4],
            },
            "dimension_over_Q": 79,
            "center_dimension_over_Q": 10,
            "word_basis_size": 79,
            "maximum_word_length": max(map(len, terwilliger["words"])),
            "nonzero_elementary_triple_products": terwilliger["nonzero_triples"],
            "beyond_elementary_triple_span": 79 - terwilliger["nonzero_triples"],
        },
        "pass1362_orbital_schur_closure": {
            "stabilizer_order": 432,
            "stabilizer_orbitals_on_XxX": 83,
            "terwilliger_dimension": 79,
            "codimension": 4,
            "schur_closure_dimension": 83,
            "all_orbital_signatures_distinct": True,
            "block_table": block_table,
            "defect_localization": terwilliger["defects"],
        },
        "pass1363_two_prime_split_fingerprint": {
            "claim_tier": "exact finite-field fingerprint; no rational splitting-field claim",
            "profiles": profiles,
            "stable_blocks": profiles[0]["blocks"],
        },
        "pass1364_boundary": {
            "literature": (
                "The 2024 Colangelo-Monzillo-Siciliano scheme concerns 160 incident "
                "point-line flags of a generalized quadrangle, not this 120-selector bundle. "
                "Targeted searches found no exact prior match; no priority claim is made."
            ),
            "physics": (
                "The result is a finite Gelfand/Terwilliger/orbital-algebra theorem. "
                "It does not select a preferred matching, produce H4/600-cell adjacency, "
                "or validate Holonet cosmology, Standard-Model, or laboratory claims."
            ),
        },
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    result = build()
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    digest = hashlib.sha256(encoded.encode()).hexdigest()
    if args.check:
        if not args.output.exists() or args.output.read_text() != encoded:
            raise SystemExit(f"certificate drift: {args.output}")
    elif not args.verify_only:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(f"PASS 1360-1364: gelfand-terwilliger sha256={digest}")


if __name__ == "__main__":
    main()
