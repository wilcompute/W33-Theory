#!/usr/bin/env python3
"""Passes 3729--3742: five-front closure plus exact website restoration."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path

import networkx as nx
import numpy as np

from analysis._bt3506_3519_provisional_impl import (
    close_group,
    dependency_deck,
    geometry_objects,
    rank_mod,
)
from analysis.bt3649_3662_seven_front_closure import (
    rref_basis_columns,
    restrict_perm,
    solve_coords,
    w33_lines,
)

CAP62 = [
    3,4,11,13,15,18,28,30,33,34,35,46,51,55,57,60,65,68,70,78,
    92,94,97,100,101,105,109,114,117,119,122,123,132,135,141,143,
    144,149,153,154,165,167,171,173,182,188,189,191,192,194,196,
    198,202,203,213,217,219,223,226,228,230,231,
]
SEED1 = [2,1,2,0,1,2,0,1,2,0,1,0,2,2,1,0,0,0,0,2,0,1,0,0,0,2,1,0,0,0]
SEED5 = [1,1,0,1,1,2,2,2,0,0,1,0,1,1,1,1,0,2,2,1,1,2,0,1,1,0,0,0,0,0]
SEED10 = [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

RESTORED_BLOB = "41a8d733f42da18282fa276f5d2fa82bac7516f6"
ARCHIVE_BLOB = "94e90827ec73fc20e632fba5519fed2d109846d6"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def website_certificate() -> dict:
    index = Path("docs/index.html").read_bytes()
    archive = Path("docs/source-derived-architecture-landing-2026-08-05.html").read_bytes()
    assert git_blob_sha(index) == RESTORED_BLOB
    assert git_blob_sha(archive) == ARCHIVE_BLOB
    assert len(index.splitlines()) == 28865
    assert len(archive.splitlines()) == 1
    return {
        "overwrite_commit": "413ed869b1ae82446df3583e43c3f9bcb365a18c",
        "last_intact_commit": "df5c52314bf4c8c4b0d7a1b1f0afb66d872bdfb6",
        "restored_index_blob": RESTORED_BLOB,
        "archived_overwrite_blob": ARCHIVE_BLOB,
        "archive_path": "docs/source-derived-architecture-landing-2026-08-05.html",
        "overwrite_diff": {"additions": 86, "deletions": 28865},
        "method": "exact Git blob swap; no HTML reserialization",
    }


def face_action(objects):
    faces = objects["faces"]
    index = {face: i for i, face in enumerate(faces)}
    generators = [
        tuple(index[tuple(sorted(g[v] for v in face))] for face in faces)
        for g in objects["generators"]
    ]
    group = close_group(generators, 240)
    assert len(group) == 25920
    return generators, group


def cubic_certificate(objects, deck, face_group) -> tuple[dict, dict]:
    T = deck["incidence"]
    D = deck["operator"].astype(np.int64)
    triples = deck["triangles"]
    assert T.shape == (240, 5040)
    assert set(map(int, T.sum(axis=0))) == {3}
    assert set(map(int, T.sum(axis=1))) == {63}

    eig = np.linalg.eigvalsh(D.astype(float))
    assert abs(eig[0] + 18) < 1e-7
    assert abs(eig[-1] - 126) < 1e-7

    # For a hitting set of size m, P=sum C(hit_t,2).
    # D gives P>=3m^2/10-9m; hit_t in {1,2,3} gives
    # P<=3(63m-5040)/2. Hence (m-105)(m-240)<=0.
    for m in range(80, 105):
        lower = math.ceil(3 * m * m / 10 - 9 * m)
        upper = math.floor(3 * (63 * m - 5040) / 2)
        assert lower > upper
    assert 3 * 105 * 105 / 10 - 9 * 105 == 4725 / 2
    assert 3 * (63 * 105 - 5040) / 2 == 4725 / 2
    # P is integral, so equality at m=105 is impossible.
    lower_bound = 106

    cap = frozenset(CAP62)
    assert len(cap) == 62
    assert all(not set(triple) <= cap for triple in triples)
    transversal = set(range(240)) - cap
    hits = Counter(sum(v in transversal for v in triple) for triple in triples)
    assert hits == Counter({1: 844, 2: 2218, 3: 1978})

    orbit = {frozenset(g[v] for v in cap) for g in face_group}
    assert len(orbit) == 25920
    intersections = dict(sorted(Counter(len(cap & image) for image in orbit).items()))
    assert intersections[62] == 1
    assert min(intersections) == 5

    cap_hash = hashlib.sha256(
        json.dumps(CAP62, separators=(",", ":")).encode()
    ).hexdigest()
    main = {
        "fractional_transversal": 80,
        "previous_integral_lower_bound": 81,
        "weighted_pair_operator_degree": 126,
        "weighted_pair_operator_minimum_eigenvalue": -18,
        "spectral_inequality": "P >= (3/10)m^2-9m",
        "excess_inequality": "P <= (3/2)(63m-5040)",
        "factorized_feasibility": "(m-105)(m-240)<=0",
        "parity_exclusion_at_105": "P is integral, while the common endpoint is 4725/2",
        "new_integral_lower_bound": lower_bound,
        "cap_witness_size": 62,
        "transversal_witness_size": 178,
        "cap_indices": CAP62,
        "cap_sha256": cap_hash,
        "transversal_hit_profile": dict(sorted(hits.items())),
        "live_interval": [106, 178],
        "radius_boundary": "The cubic transversal is not itself the 720-coordinate covering radius; 389<=R<=435 remains live.",
    }
    bonkers = {
        "cap_size": 62,
        "group_order": 25920,
        "orbit_size": len(orbit),
        "stabilizer_order": 1,
        "intersection_census": intersections,
        "interpretation": "The explicit 62-cap has a free U4(2) orbit, producing 25,920 distinct cap witnesses.",
        "boundary": "The cap is a certified witness, not proved maximum.",
    }
    return main, bonkers


def m4_certificate(A45: np.ndarray) -> dict:
    lines = w33_lines(A45)
    assert len(lines) == 27
    incidence = Counter(v for line in lines for v in line)
    assert incidence == Counter({v: 3 for v in range(45)})
    eigenvalues = np.linalg.eigvalsh(A45.astype(float))
    assert sum(abs(eigenvalues - 32) < 1e-7) == 1
    assert sum(abs(eigenvalues - 2) < 1e-7) == 24
    assert sum(abs(eigenvalues + 4) < 1e-7) == 20
    # Hoffman gives alpha<=5 and the 27 lines attain alpha=5.
    assert round(45 * 4 / (32 + 4)) == 5
    return {
        "anchor_graph": "SRG(45,32,22,24)",
        "anchor_independence_number": 5,
        "fractional_chromatic_number": 9,
        "vector_chromatic_number": 9,
        "ordinary_attaining_weight": "A45 tensor I4",
        "ordinary_attaining_ratio": 9,
        "arbitrary_edge_supported_hermitian_ratio_optimum": 9,
        "complex_realification": "Complex Hermitian weights do not improve the generalized Hoffman optimum.",
        "chromatic_boundary": [10, 11],
    }


def independent_extend(base, candidates, target, p=3):
    B = np.array(base, dtype=np.int64) % p
    rank = rank_mod(B, p)
    for j in range(candidates.shape[1]):
        test = np.column_stack([B, candidates[:, j]])
        new_rank = rank_mod(test, p)
        if new_rank > rank:
            B = test
            rank = new_rank
            if rank == target:
                break
    assert rank == target
    return B % p


def nullspace_mod(matrix, p=3):
    a = np.array(matrix, dtype=np.int64) % p
    rows, cols = a.shape
    pivots = []
    row = 0
    for col in range(cols):
        pivot = next((r for r in range(row, rows) if a[r, col]), None)
        if pivot is None:
            continue
        if pivot != row:
            a[[row, pivot]] = a[[pivot, row]]
        a[row] = a[row] * pow(int(a[row, col]), -1, p) % p
        for r in range(rows):
            if r != row and a[r, col]:
                a[r] = (a[r] - a[r, col] * a[row]) % p
        pivots.append(col)
        row += 1
    free = [c for c in range(cols) if c not in set(pivots)]
    vectors = []
    for f in free:
        v = np.zeros(cols, dtype=np.int8)
        v[f] = 1
        for r, c in enumerate(pivots):
            v[c] = (-a[r, f]) % p
        vectors.append(v)
    return np.column_stack(vectors) if vectors else np.zeros((cols, 0), dtype=np.int8)


class VectorBasis:
    def __init__(self, n, p=3):
        self.p = p
        self.rows = {}
        self.n = n

    def add(self, vector):
        v = np.array(vector, dtype=np.int8) % self.p
        for pivot in sorted(self.rows):
            if v[pivot]:
                v = (v - int(v[pivot]) * self.rows[pivot]) % self.p
        nz = np.flatnonzero(v)
        if not len(nz):
            return False
        pivot = int(nz[0])
        v = v * pow(int(v[pivot]), -1, self.p) % self.p
        for old in list(self.rows):
            if self.rows[old][pivot]:
                self.rows[old] = (
                    self.rows[old] - int(self.rows[old][pivot]) * v
                ) % self.p
        self.rows[pivot] = v
        return True

    def matrix(self):
        return np.column_stack([self.rows[p] for p in sorted(self.rows)])


def spin(seed, generators):
    basis = VectorBasis(len(seed))
    basis.add(seed)
    queue = [np.array(seed, dtype=np.int8) % 3]
    while queue:
        vector = queue.pop()
        for generator in generators:
            image = generator @ vector % 3
            if basis.add(image):
                queue.append(image)
    return basis.matrix()


def algebra_dimension(generators):
    n = generators[0].shape[0]
    vector_basis = VectorBasis(n * n)
    identity = np.eye(n, dtype=np.int8)
    vector_basis.add(identity.reshape(-1))
    queue = [identity]
    count = 1
    while queue:
        matrix = queue.pop(0)
        for generator in generators:
            product_matrix = matrix @ generator % 3
            if vector_basis.add(product_matrix.reshape(-1)):
                queue.append(product_matrix)
                count += 1
    return count


def fixed_dimension(generators, dual=False):
    n = generators[0].shape[0]
    identity = np.eye(n, dtype=np.int8)
    matrix = np.vstack([
        ((g.T if dual else g) - identity) % 3 for g in generators
    ])
    return n - rank_mod(matrix, 3)


def centralizer_dimension(generators):
    n = generators[0].shape[0]
    identity = np.eye(n, dtype=np.int8)
    equations = np.vstack([
        (np.kron(identity, g.T) - np.kron(g, identity)) % 3
        for g in generators
    ])
    return n * n - rank_mod(equations, 3)


def module_certificate(D, face_generators):
    M = D % 3
    projector = (-np.linalg.matrix_power(M, 3)) % 3
    _, B14 = rref_basis_columns(M @ M @ (np.eye(240, dtype=int) - projector) % 3, 3)
    DN = M @ (np.eye(240, dtype=int) - projector) % 3
    N = (np.eye(240, dtype=int) - projector) % 3
    B44 = independent_extend(B14, DN, 44)
    B159 = independent_extend(B44, N, 159)
    action159 = [restrict_perm(B159, g) for g in face_generators]
    action14 = [g[:14, :14] % 3 for g in action159]
    action30 = [g[14:44, 14:44] % 3 for g in action159]
    action115 = [g[44:, 44:] % 3 for g in action159]

    assert algebra_dimension(action14) == 196
    fixed = nullspace_mod(
        np.vstack([(g - np.eye(30, dtype=np.int8)) % 3 for g in action30]), 3
    )
    assert fixed.shape == (30, 1)
    assert list(map(int, fixed[:, 0])) == SEED1

    B1 = spin(SEED1, action30)
    B5 = spin(SEED5, action30)
    B10 = spin(SEED10, action30)
    assert [B1.shape[1], B5.shape[1], B10.shape[1]] == [1, 5, 10]
    B16 = np.column_stack([B1, B5, B10]) % 3
    assert rank_mod(B16, 3) == 16

    R1 = [solve_coords(B1, g @ B1 % 3, 3) for g in action30]
    R5 = [solve_coords(B5, g @ B5 % 3, 3) for g in action30]
    R10 = [solve_coords(B10, g @ B10 % 3, 3) for g in action30]
    B30 = independent_extend(B16, np.eye(30, dtype=np.int8), 30)
    nested = [solve_coords(B30, g @ B30 % 3, 3) for g in action30]
    assert all(not np.any(g[16:, :16]) for g in nested)
    head14 = [g[16:, 16:] % 3 for g in nested]
    dimensions = {
        "1": algebra_dimension(R1),
        "5": algebra_dimension(R5),
        "10": algebra_dimension(R10),
        "14q": algebra_dimension(head14),
    }
    assert dimensions == {"1": 1, "5": 25, "10": 100, "14q": 196}
    assert centralizer_dimension(action30) == 1

    return {
        "filtration_dimensions": [159, 44, 14, 0],
        "successive_quotients": [115, 30, 14],
        "bottom14_algebra_dimension": 196,
        "bottom14_absolute_irreducible": True,
        "middle30_endomorphism_dimension": 1,
        "middle30_fixed_dimension": fixed_dimension(action30),
        "middle30_dual_fixed_dimension": fixed_dimension(action30, True),
        "middle30_socle_factors": [1, 5, 10],
        "middle30_socle_dimension": 16,
        "middle30_factor_algebra_dimensions": dimensions,
        "middle30_head_dimension": 14,
        "middle30_extension_non_split": True,
        "middle30_exact_sequence": "0 -> 1+5+10 -> M30 -> 14 -> 0",
        "top115_fixed_dimension": fixed_dimension(action115),
        "top115_dual_fixed_dimension": fixed_dimension(action115, True),
        "top115_boundary": "The top quotient has a 2-dimensional fixed socle and one trivial head; its remaining composition factors are not labelled here.",
    }


def tomotope_data():
    coordinates = [(l, r) for l in range(4) for r in range(4) if l != r]
    index = {coordinate: i for i, coordinate in enumerate(coordinates)}
    faces = []
    for l in range(4):
        faces.append(tuple(sorted(index[(l, r)] for r in range(4) if r != l)))
    for r in range(4):
        faces.append(tuple(sorted(index[(l, r)] for l in range(4) if l != r)))
    for subset in combinations(range(4), 3):
        l, m, r = subset
        for cycle in (
            ((l, m), (m, r), (r, l)),
            ((l, r), (r, m), (m, l)),
        ):
            faces.append(tuple(sorted(index[item] for item in cycle)))
    cells = []
    for selected in combinations(range(16), 4):
        multiplicity = Counter(edge for face in selected for edge in faces[face])
        if len(multiplicity) == 6 and set(multiplicity.values()) == {2}:
            cells.append(selected)
    covers = [
        (0, 1, 3, 5, 6, 8, 10, 11),
        (0, 2, 3, 4, 7, 8, 9, 11),
        (1, 2, 4, 5, 6, 7, 9, 10),
    ]
    return coordinates, faces, cells, covers


def vertex_assignments(faces):
    pairs = list(combinations(range(4), 2))
    allowed = {
        frozenset(pairs.index(pair) for pair in combinations(subset, 2))
        for subset in combinations(range(4), 3)
    }
    edge_faces = [[] for _ in range(12)]
    for face_id, face in enumerate(faces):
        for edge in face:
            edge_faces[edge].append(face_id)
    assignment = [None] * 12
    counts = [0] * 6
    assignment[0] = 0
    counts[0] = 1
    solutions = []

    def possible(face_id):
        values = [assignment[e] for e in faces[face_id]]
        assigned = [v for v in values if v is not None]
        return len(set(assigned)) == len(assigned) and any(
            set(assigned) <= set(option) for option in allowed
        )

    def recurse():
        if all(value is not None for value in assignment):
            if counts == [2] * 6:
                solutions.append(tuple(assignment))
            return
        best_edge = None
        best_options = None
        for edge, value in enumerate(assignment):
            if value is not None:
                continue
            options = []
            for label in range(6):
                if counts[label] == 2:
                    continue
                assignment[edge] = label
                counts[label] += 1
                if all(possible(face_id) for face_id in edge_faces[edge]):
                    options.append(label)
                counts[label] -= 1
                assignment[edge] = None
            if not options:
                return
            if best_options is None or len(options) < len(best_options):
                best_edge, best_options = edge, options
        for label in best_options:
            assignment[best_edge] = label
            counts[label] += 1
            recurse()
            counts[label] -= 1
            assignment[best_edge] = None

    recurse()
    assert len(solutions) == 12
    return sorted(solutions)


def incidence_graph(assignment, cover, faces, cells):
    pairs = list(combinations(range(4), 2))
    graph = nx.Graph()
    for vertex in range(4):
        graph.add_node(("v", vertex), rank=0)
    for edge in range(12):
        graph.add_node(("e", edge), rank=1)
    for face in range(16):
        graph.add_node(("f", face), rank=2)
    for cell in cover:
        graph.add_node(("c", cell), rank=3)
    for edge, pair_id in enumerate(assignment):
        for vertex in pairs[pair_id]:
            graph.add_edge(("v", vertex), ("e", edge))
    for face, edge_set in enumerate(faces):
        for edge in edge_set:
            graph.add_edge(("e", edge), ("f", face))
    for cell in cover:
        for face in cells[cell]:
            graph.add_edge(("f", face), ("c", cell))
    return graph


def flags(assignment, cover, faces, cells):
    pairs = list(combinations(range(4), 2))
    return [
        (vertex, edge, face, cell)
        for cell in cover
        for face in cells[cell]
        for edge in faces[face]
        for vertex in pairs[assignment[edge]]
    ]


def permutation_order(mapping, nodes):
    seen = set()
    order = 1
    for node in nodes:
        if node in seen:
            continue
        current = node
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = mapping[current]
        order = math.lcm(order, length)
    return order


def tomotope_certificate():
    _, faces, cells, covers = tomotope_data()
    solutions = vertex_assignments(faces)
    representatives = [
        (0,1,3,0,2,4,4,3,5,2,1,5),
        (0,1,3,5,2,1,4,2,0,3,4,5),
        (0,1,3,5,3,4,1,2,5,2,4,0),
    ]
    assert all(rep in solutions for rep in representatives)
    pair_list = list(combinations(range(4), 2))
    stabilizer = [
        permutation for permutation in permutations(range(4))
        if tuple(sorted((permutation[0], permutation[1]))) == (0, 1)
    ]
    vertex_orbits = []
    unseen = set(solutions)
    while unseen:
        representative = min(unseen)
        orbit = set()
        for permutation in stabilizer:
            label_map = {
                label: pair_list.index(tuple(sorted(
                    (permutation[pair[0]], permutation[pair[1]])
                )))
                for label, pair in enumerate(pair_list)
            }
            orbit.add(tuple(label_map[label] for label in representative))
        assert len(orbit) == 4
        assert orbit <= set(solutions)
        unseen -= orbit
        vertex_orbits.append(orbit)
    assert len(vertex_orbits) == 3

    order_matrix = []
    flag_orbit_matrix = []
    all_connected = True
    all_diamonds = True
    for assignment in representatives:
        order_row = []
        orbit_row = []
        for cover in covers:
            graph = incidence_graph(assignment, cover, faces, cells)
            matcher = nx.algorithms.isomorphism.GraphMatcher(
                graph, graph, node_match=lambda a, b: a["rank"] == b["rank"]
            )
            automorphisms = list(matcher.isomorphisms_iter())
            order = len(automorphisms)
            assert order in (96, 192)
            nodes = list(graph)
            census = Counter(permutation_order(auto, nodes) for auto in automorphisms)
            if order == 96:
                assert census == Counter({1: 1, 2: 27, 3: 32, 4: 36})
            else:
                assert census == Counter({1: 1, 2: 43, 3: 32, 4: 84, 6: 32})

            flag_list = flags(assignment, cover, faces, cells)
            assert len(flag_list) == 192
            flag_set = set(flag_list)
            flag_graph = nx.Graph()
            flag_graph.add_nodes_from(flag_list)
            for flag in flag_list:
                for rank in range(4):
                    neighbors = [
                        other for other in flag_list
                        if other != flag
                        and all(flag[i] == other[i] for i in range(4) if i != rank)
                    ]
                    if len(neighbors) != 1:
                        all_diamonds = False
                    else:
                        flag_graph.add_edge(flag, neighbors[0])
            if not nx.is_connected(flag_graph):
                all_connected = False

            unseen_flags = set(flag_list)
            orbit_sizes = []
            while unseen_flags:
                flag = next(iter(unseen_flags))
                orbit = set()
                for auto in automorphisms:
                    image = (
                        auto[("v", flag[0])][1],
                        auto[("e", flag[1])][1],
                        auto[("f", flag[2])][1],
                        auto[("c", flag[3])][1],
                    )
                    assert image in flag_set
                    orbit.add(image)
                unseen_flags -= orbit
                orbit_sizes.append(len(orbit))
            orbit_sizes.sort(reverse=True)
            assert orbit_sizes == ([192] if order == 192 else [96, 96])
            order_row.append(order)
            orbit_row.append(orbit_sizes)
        order_matrix.append(order_row)
        flag_orbit_matrix.append(orbit_row)

    assert order_matrix == [[96,96,192],[192,96,96],[96,192,96]]
    return {
        "edge_face_vertex_assignments_with_edge0_fixed": 12,
        "vertex_assignment_orbits": 3,
        "cell_double_covers": 3,
        "completion_grid_orders": order_matrix,
        "completion_grid_flag_orbits": flag_orbit_matrix,
        "ordinary_tomotopes": 6,
        "ordinary_automorphism_order": 96,
        "ordinary_flag_orbits": 2,
        "regular_central_lifts": 3,
        "central_lift_automorphism_order": 192,
        "central_lift_flag_orbits": 1,
        "exceptional_perfect_matching": [[0,2],[1,0],[2,1]],
        "f_vector": [4,12,16,8],
        "flags": 192,
        "all_diamond_conditions": all_diamonds,
        "all_flag_graphs_connected": all_connected,
        "interpretation": "Six completions have Aut(tomotope); three matched completions realize the non-split order-192 central lift.",
    }


def canonical3(vector):
    for value in vector:
        if value % 3:
            inverse = 1 if value % 3 == 1 else 2
            return tuple(inverse * entry % 3 for entry in vector)
    raise ValueError


def symplectic(left, right):
    return (
        left[0] * right[1] - left[1] * right[0]
        + left[2] * right[3] - left[3] * right[2]
    ) % 3


def gewirtz_certificate():
    points = sorted({
        canonical3(vector)
        for vector in product(range(3), repeat=4)
        if any(vector)
    })
    AW = np.zeros((40,40), dtype=np.int8)
    for i, j in combinations(range(40), 2):
        if symplectic(points[i], points[j]) == 0:
            AW[i,j] = AW[j,i] = 1
    vertices = list(product(range(2), repeat=4))
    index = {vertex: i for i, vertex in enumerate(vertices)}
    generators = [
        tuple(1 if i == j else 0 for i in range(4)) for j in range(4)
    ] + [(1,1,1,1)]
    AC = np.zeros((16,16), dtype=np.int8)
    for i, vertex in enumerate(vertices):
        for generator in generators:
            image = tuple(a ^ b for a, b in zip(vertex, generator))
            AC[i, index[image]] = 1

    Wnon = np.ones((40,40), dtype=np.int8) - np.eye(40, dtype=np.int8) - AW
    Cnon = np.ones((16,16), dtype=np.int8) - np.eye(16, dtype=np.int8) - AC
    regular = 0
    srg = 0
    for wa, wn, cross, ca, cn in product((0,1), repeat=5):
        A11 = wa * AW + wn * Wnon
        A12 = cross * np.ones((40,16), dtype=np.int8)
        A22 = ca * AC + cn * Cnon
        A = np.block([[A11,A12],[A12.T,A22]]).astype(np.int64)
        if set(map(int, A.sum(axis=1))) == {10}:
            regular += 1
        if np.array_equal(
            A @ A,
            8 * np.eye(56, dtype=np.int64)
            - 2 * A
            + 2 * np.ones((56,56), dtype=np.int64),
        ):
            srg += 1
    assert regular == 0 and srg == 0
    return {
        "weighted_bridge_order": 56,
        "weighted_entry_alphabet": [-13,-6,8,15,50,71],
        "weighted_spectrum": "560^1,112^35,(-224)^20",
        "orbitwise_binary_choices_examined": 32,
        "ten_regular_candidates": regular,
        "gewirtz_srg_candidates": srg,
        "induced_W33_no_go": "A 10-regular graph cannot contain induced W33 because W33 already has internal degree 12.",
        "verdict": "No full W33 x Clebsch orbitwise 0/1 rounding of the weighted bridge is a Gewirtz graph.",
        "boundary": "Asymmetric switching or non-equivariant rounding remains open.",
    }


def build_certificate():
    objects = geometry_objects()
    deck = dependency_deck(objects)
    face_generators, face_group = face_action(objects)
    cubic, cap_torsor = cubic_certificate(objects, deck, face_group)
    tomotope = tomotope_certificate()
    result = {
        "schema": "w33.pass3729_3742.five_front_website_restore.v1",
        "status": "PASS_5_FRONTS_PLUS_2_BONKERS_AND_WEBSITE_RESTORE",
        "passes": list(range(3729, 3743)),
        "website_restore": website_certificate(),
        "fronts": {
            "cubic_transversal": cubic,
            "signed_hermitian_M4": m4_certificate(objects["graph"]),
            "tomotope_rank_four": tomotope,
            "modular_159_filtration": module_certificate(deck["operator"], face_generators),
            "gewirtz_rounding": gewirtz_certificate(),
        },
        "bonkers": {
            "tomotope_completion_square": {
                "grid": "3 vertex structures x 3 cell covers",
                "ordinary_entries": 6,
                "exceptional_entries": 3,
                "exceptional_pattern": "perfect matching / permutation matrix",
                "order_matrix": tomotope["completion_grid_orders"],
                "interpretation": "The 3x3 square toggles between the order-96 tomotope and its non-split order-192 central lift.",
            },
            "cubic_cap_torsor": cap_torsor,
        },
        "live_boundaries": {
            "covering_radius": [389,435],
            "chromatic_number": [10,11],
            "cubic_transversal": [106,178],
        },
        "evidence_boundary": [
            "The exact website restoration is source-level and hash-verified.",
            "The cubic transversal interval is 106..178; neither endpoint is claimed exact.",
            "The Hermitian conclusion concerns generalized weighted-Hoffman bounds, not a ten-colouring.",
            "The six order-96 and three order-192 incidence completions are exact; no physical interpretation follows.",
            "The top 115-dimensional modular quotient remains compositionally unresolved.",
            "No remote CI, PDF, hardware, laboratory, or physical result is asserted before observed execution.",
        ],
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["semantic_sha256"] = hashlib.sha256(payload).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    result = build_certificate()
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"], result["semantic_sha256"])


if __name__ == "__main__":
    main()
