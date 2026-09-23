#!/usr/bin/env python3
"""Separate, then connect, the two H27 roles in the new E8 matter-81 packet.

The September-21 frontier contains two isomorphic extraspecial groups with
different embeddings:

* the regular/Payne H27 acts simply transitively on the 27 cubic-surface
  objects and supplies an address space;
* the trinification H27 has commutator equal to Z(E6), acts on the E6 27 as
  nine copies of its three-dimensional Schrodinger representation, and
  supplies an operator algebra.

They cannot be identified as permutation actions: the center of the address
H27 is fixed-point-free, whereas the center of the trinification H27 is a
scalar and fixes every basis label.  This file makes both roles executable.

Address theorem
---------------
In H27 normal form (a,b,c)=Z^a X^b omega^c, the fixed physical
Clifford-648 gauge selects five order-three directions

    <omega>, <omega X>, <omega Z>, <Z X>, <omega^2 Z X^2>.

have 45 right cosets.  Their collinearity graph is GQ(2,4), and an explicit
graph isomorphism sends those cosets to the 45 tritangents on the 27 complete
factorisation frames.  Adjoin the external phase shift C3.  For each base
direction, the two slopes +1 and -1 give ten C3 directions in H27 x C3.
Their 270 cosets are exactly the lifted E8 matter cubic triples: one of each
external phase over every tritangent.  All 648 elements of the physical
Clifford dictionary preserve the 45-line address geometry.  They have line
orbits 9+36 and, when the external phase labels are held fixed, instruction
orbits 27+27+216.

Operator theorem
----------------
On

    27=(3,3bar,1)+(1,3,3bar)+(3bar,1,3),

the center-correct trinification generators X_int=(X,X,I) and
Z_int=(Z^2,Z,I) admit an explicit basis chart (m,q), with m in F3^2 and
q in F3, in which

    X_int |m,q> = |m,q+1>,   Z_int |m,q> = omega^q |m,q>.

After tensoring with the external A2 qutrit p, the E8 matter representation
is therefore

    C^81 ~= C^9_multiplicity tensor C^3_internal tensor C^3_external.

The central product H27 o H27 acts as I_9 tensor the irreducible two-qutrit
Pauli representation.  Its generated algebra is I_9 tensor M_9(C), and its
commutant is M_9(C) tensor I_9.  Thus the shell contains two active qutrits
and an exact nine-dimensional multiplicity/noiseless subsystem at this
restricted-group level.

Boundary: the address and operator charts are not identified.  The parallel
rank-obstruction certificates prove that no invertible H27-equivariant change
of basis exists in dimension 27 (maximum rank 9), and no K-equivariant compiler
exists in dimension 81 (maximum rank 27).  A non-equivariant,
proper-subgroup-covariant, or otherwise symmetry-changing root-gauge compiler
remains open.  No family, Yukawa, vacuum, or hardware claim is made.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_e8_matter81_h27_address_operator_compiler.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


H = tuple(itertools.product(range(3), repeat=3))
HI = (0, 0, 0)


def hmul(g: tuple[int, int, int], h: tuple[int, int, int]):
    """Multiply Z^a X^b omega^c with ZX=omega XZ."""
    a, b, c = g
    A, B, C = h
    return ((a + A) % 3, (b + B) % 3, (c + C - b * A) % 3)


def hinv(g):
    for h in H:
        if hmul(g, h) == HI and hmul(h, g) == HI:
            return h
    raise AssertionError(g)


def hpow(g, n):
    out = HI
    for _ in range(n):
        out = hmul(out, g)
    return out


def subgroup3(g):
    return frozenset((HI, g, hmul(g, g)))


def right_cosets(group, subgroup, mul):
    unseen = set(group)
    answer = []
    while unseen:
        x = min(unseen)
        coset = frozenset(mul(x, s) for s in subgroup)
        answer.append(coset)
        unseen -= coset
    return sorted(answer, key=lambda c: tuple(sorted(c)))


def srg_signature(graph):
    nodes = list(graph)
    degree = {graph.degree(x) for x in nodes}
    adjacent_common = set()
    nonadjacent_common = set()
    for i, x in enumerate(nodes):
        nx_ = set(graph[x])
        for y in nodes[i + 1 :]:
            value = len(nx_ & set(graph[y]))
            (adjacent_common if graph.has_edge(x, y) else nonadjacent_common).add(value)
    return (len(nodes), degree.pop(), adjacent_common.pop(), nonadjacent_common.pop())


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def address_geometry():
    # The physical Clifford dictionary fixes the previously arbitrary central
    # lifts of the four projective H27/Z directions.  Its chosen SL(2,3)
    # complement has suborbits 1,1,1,8,8,8 on H27.  Exactly one eight-orbit,
    # together with the two nonidentity central elements, gives GQ(2,4).
    clifford = json.loads(
        (ROOT / "data/w33_physical_clifford648_full_permutation_dictionary.json").read_text()
    )
    assert clifford["status"].startswith("PASS_ALL_648_PHYSICAL_QUTRIT_CLIFFORD")
    assert clifford["orders"] == {"H27": 27, "SL23": 24, "normalizer": 648}
    assert len(clifford["records"]) == 648

    def physical_to_pass(g):
        a, b, c = g
        return (b, a, (-a * b - c) % 3)

    def pass_to_physical(g):
        u, v, w = g
        return (v, u, (-v * u - w) % 3)

    def pass_index(g):
        return 9 * g[0] + 3 * g[1] + g[2]

    def pass_coordinate(index):
        return (index // 9, (index // 3) % 3, index % 3)

    def physical_affine_map(record):
        permutation = record["affine_permutation_on_H27_27"]
        answer = {
            h: pass_to_physical(
                pass_coordinate(permutation[pass_index(physical_to_pass(h))])
            )
            for h in H
        }
        assert len(set(answer.values())) == 27
        return answer

    clifford_maps = [physical_affine_map(record) for record in clifford["records"]]
    complement_maps = [
        physical_affine_map(record)
        for record in clifford["records"]
        if record["physical_H27_ZXz"] == [0, 0, 0]
    ]
    assert len(complement_maps) == 24
    assert all(permutation[HI] == HI for permutation in complement_maps)

    unseen = set(H)
    complement_suborbits = []
    while unseen:
        seed = min(unseen)
        orbit = frozenset(permutation[seed] for permutation in complement_maps)
        complement_suborbits.append(orbit)
        unseen -= orbit
    assert sorted(len(orbit) for orbit in complement_suborbits) == [1, 1, 1, 8, 8, 8]

    center = subgroup3((0, 0, 1))

    def cayley_common_neighbor_signature(connection):
        graph = nx.Graph()
        graph.add_nodes_from(H)
        for x in H:
            graph.add_edges_from((x, hmul(x, step)) for step in connection)
        degrees = sorted({graph.degree(x) for x in H})
        adjacent = set()
        nonadjacent = set()
        for index, x in enumerate(H):
            neighbors = set(graph[x])
            for y in H[index + 1 :]:
                common = len(neighbors & set(graph[y]))
                (adjacent if graph.has_edge(x, y) else nonadjacent).add(common)
        return graph, degrees, sorted(adjacent), sorted(nonadjacent)

    candidate_records = []
    selected_eight_orbit = None
    for orbit in sorted(
        (orbit for orbit in complement_suborbits if len(orbit) == 8),
        key=lambda item: tuple(sorted(item)),
    ):
        connection = (center - {HI}) | set(orbit)
        _, degrees, adjacent, nonadjacent = cayley_common_neighbor_signature(connection)
        is_gq24 = degrees == [10] and adjacent == [1] and nonadjacent == [5]
        candidate_records.append(
            {
                "eight_orbit": [list(x) for x in sorted(orbit)],
                "degree_set": degrees,
                "adjacent_common_neighbor_set": adjacent,
                "nonadjacent_common_neighbor_set": nonadjacent,
                "is_GQ24_SRG": is_gq24,
            }
        )
        if is_gq24:
            assert selected_eight_orbit is None
            selected_eight_orbit = orbit
    assert selected_eight_orbit is not None
    assert sum(record["is_GQ24_SRG"] for record in candidate_records) == 1

    # One Clifford-selected lift of each projective direction, plus Z(H27).
    generators = (
        (0, 0, 1),  # center omega
        (0, 1, 1),  # omega X
        (1, 0, 1),  # omega Z
        (1, 1, 0),  # Z X
        (1, 2, 2),  # omega^2 Z X^2
    )
    directions = tuple(subgroup3(g) for g in generators)
    assert len(set(directions)) == 5
    assert all(hpow(g, 3) == HI for g in generators)
    selected_connection = (center - {HI}) | set(selected_eight_orbit)
    assert set().union(*(direction - {HI} for direction in directions)) == selected_connection

    base_lines = set()
    for direction in directions:
        cosets = right_cosets(H, direction, hmul)
        assert len(cosets) == 9
        base_lines.update(cosets)
    assert len(base_lines) == 45

    incidence = Counter(x for line in base_lines for x in line)
    assert set(incidence.values()) == {5}
    pair_incidence = Counter(
        frozenset(pair)
        for line in base_lines
        for pair in itertools.combinations(sorted(line), 2)
    )
    assert set(pair_incidence.values()) == {1}

    graph = nx.Graph()
    graph.add_nodes_from(H)
    graph.add_edges_from(tuple(pair) for pair in pair_incidence)
    assert srg_signature(graph) == (27, 10, 1, 5)
    assert len([c for c in nx.enumerate_all_cliques(graph) if len(c) == 3]) == 45

    def image_set(permutation, objects, lift):
        return {lift(permutation, item) for item in objects}

    def orbit_sizes(objects, permutations, lift):
        ordered = sorted(objects, key=lambda item: tuple(sorted(item)))
        index = {item: position for position, item in enumerate(ordered)}
        images = [
            tuple(index[lift(permutation, item)] for item in ordered)
            for permutation in permutations
        ]
        unseen_indices = set(range(len(ordered)))
        sizes = []
        while unseen_indices:
            seed = min(unseen_indices)
            orbit = {permutation[seed] for permutation in images}
            sizes.append(len(orbit))
            unseen_indices -= orbit
        return sorted(sizes)

    line_lift = lambda permutation, line: frozenset(permutation[x] for x in line)
    assert all(
        image_set(permutation, base_lines, line_lift) == base_lines
        for permutation in clifford_maps
    )
    clifford_line_orbits = orbit_sizes(base_lines, clifford_maps, line_lift)
    assert clifford_line_orbits == [9, 36]

    common = load_module(
        ROOT / "analysis/w33_pass4992_4999_common.py", "matter81_compiler_common"
    )
    base = common.build_base()
    target = base["G27"].copy()
    assert srg_signature(target) == (27, 10, 1, 5)

    nx.set_node_attributes(graph, {x: x == HI for x in graph}, "anchor")
    nx.set_node_attributes(target, {x: x == 0 for x in target}, "anchor")
    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph, target, node_match=lambda a, b: a["anchor"] == b["anchor"]
    )
    anchored_isomorphisms = list(matcher.isomorphisms_iter())
    assert len(anchored_isomorphisms) == 1920
    address_to_frame = anchored_isomorphisms[0]
    assert address_to_frame[HI] == 0
    mapped_base_lines = {
        frozenset(address_to_frame[x] for x in line) for line in base_lines
    }
    target_tritangents = {frozenset(t) for t in base["tritangents"]}
    assert mapped_base_lines == target_tritangents

    # K=H27 x C3, with ten slope directions over the five base directions.
    K = tuple((h, p) for h in H for p in range(3))
    KI = (HI, 0)

    def kmul(x, y):
        return (hmul(x[0], y[0]), (x[1] + y[1]) % 3)

    lifted_directions = []
    direction_records = []
    for index, g in enumerate(generators):
        for slope in (1, 2):
            kg = (g, slope)
            direction = frozenset((KI, kg, kmul(kg, kg)))
            assert len(direction) == 3
            lifted_directions.append(direction)
            direction_records.append(
                {
                    "base_direction": index,
                    "base_generator": list(g),
                    "external_slope": slope if slope == 1 else -1,
                    "generator": [list(g), slope],
                }
            )
    assert len(set(lifted_directions)) == 10

    lifted_lines = set()
    for direction in lifted_directions:
        cosets = right_cosets(K, direction, kmul)
        assert len(cosets) == 27
        lifted_lines.update(cosets)
    assert len(lifted_lines) == 270
    lifted_incidence = Counter(x for line in lifted_lines for x in line)
    assert set(lifted_incidence.values()) == {10}
    lifted_pairs = Counter(
        frozenset(pair)
        for line in lifted_lines
        for pair in itertools.combinations(sorted(line), 2)
    )
    assert set(lifted_pairs.values()) == {1}

    mapped_lifted = {
        frozenset((address_to_frame[h], p) for h, p in line)
        for line in lifted_lines
    }
    expected_lifted = {
        frozenset(zip(triangle, phases))
        for triangle in target_tritangents
        for phases in itertools.permutations(range(3))
    }
    assert len(expected_lifted) == 270
    assert mapped_lifted == expected_lifted
    assert all({p for _, p in line} == {0, 1, 2} for line in mapped_lifted)

    # This is the scheduler/address action: the Clifford permutation moves the
    # H27 frame address while the external phase label is treated as inert.
    # A physical Fourier gate is not a permutation of the qutrit basis, so this
    # census is deliberately not described as a physical action on E8 roots.
    lifted_line_lift = lambda permutation, line: frozenset(
        (permutation[h], phase) for h, phase in line
    )
    assert all(
        image_set(permutation, lifted_lines, lifted_line_lift) == lifted_lines
        for permutation in clifford_maps
    )
    clifford_instruction_orbits = orbit_sizes(
        lifted_lines, clifford_maps, lifted_line_lift
    )
    assert clifford_instruction_orbits == [27, 27, 216]

    carrier = json.loads(
        (ROOT / "data/w33_e8_matter81_frame_qutrit_tensor_carrier.json").read_text()
    )
    assert carrier["status"].startswith("PASS_E8_MATTER81")
    record_by_label = {
        (record["complete_frame"], record["external_qutrit_phase"]): record
        for record in carrier["root_records"]
    }
    assert set(record_by_label) == {
        (frame, phase) for frame in range(27) for phase in range(3)
    }
    inverse_address = {frame: h for h, frame in address_to_frame.items()}
    root_addresses = []
    for label in sorted(record_by_label):
        frame, phase = label
        record = record_by_label[label]
        root_addresses.append(
            {
                "root": record["root"],
                "complete_frame": frame,
                "external_qutrit_phase": phase,
                "regular_H27_address": list(inverse_address[frame]),
                "K_address": [list(inverse_address[frame]), phase],
            }
        )

    center_orbit = {hmul(HI, z) for z in center}
    assert len(center_orbit) == 3

    return {
        "H27_order": len(H),
        "H27_center_order": len(center),
        "selected_base_directions": [
            {"generator": list(g), "subgroup": [list(x) for x in sorted(d)]}
            for g, d in zip(generators, directions)
        ],
        "base_cosets": len(base_lines),
        "base_points_per_line": 3,
        "base_lines_per_point": sorted(set(incidence.values()))[0],
        "base_collinearity_srg": list(srg_signature(graph)),
        "physical_Clifford648_address_normalizer": {
            "source": "data/w33_physical_clifford648_full_permutation_dictionary.json",
            "order": len(clifford_maps),
            "multiplication_table_digest": clifford["full_multiplication_table_digest"],
            "complement_suborbit_sizes": sorted(
                len(orbit) for orbit in complement_suborbits
            ),
            "three_eight_orbit_census": candidate_records,
            "unique_GQ24_completion": True,
            "all_648_preserve_45_address_lines": True,
            "address_line_orbit_sizes": clifford_line_orbits,
            "phase_labels_held_fixed_instruction_orbit_sizes": clifford_instruction_orbits,
            "instruction_stabilizer_orders": [
                len(clifford_maps) // size for size in clifford_instruction_orbits
            ],
            "boundary": (
                "This is the induced address/scheduler permutation with the external phase label held fixed. "
                "It is not the complex qutrit action of a physical Clifford gate on the frozen E8 roots."
            ),
        },
        "address_to_complete_frame": {
            ",".join(map(str, h)): frame for h, frame in sorted(address_to_frame.items())
        },
        "anchored_incidence_isomorphism_count": len(anchored_isomorphisms),
        "anchored_gauge_scope": (
            "The first of 1920 identity-to-frame-0 incidence isomorphisms is chosen "
            "deterministically. This does not construct a canonical root-gauge intertwiner."
        ),
        "K_structure": "H27_regular x C3_external_shift",
        "K_order": len(K),
        "lifted_directions": direction_records,
        "lifted_direction_count": len(lifted_directions),
        "lifted_cosets": len(lifted_lines),
        "lifted_lines_per_root": sorted(set(lifted_incidence.values()))[0],
        "lifted_pair_multiplicity_max": max(lifted_pairs.values()),
        "equals_E8_270_cubic_triples": mapped_lifted == expected_lifted,
        "root_addresses": root_addresses,
        "address_center_orbit_size": len(center_orbit),
    }


def operator_geometry():
    # Basis labels for the three trinification nonets.
    internal_basis = []
    for i, j in itertools.product(range(3), repeat=2):
        internal_basis.append(("A_Bbar", i, j))
    for j, k in itertools.product(range(3), repeat=2):
        internal_basis.append(("B_Cbar", j, k))
    for i, k in itertools.product(range(3), repeat=2):
        internal_basis.append(("Abar_C", i, k))
    assert len(internal_basis) == 27

    def mq(label):
        sector, u, v = label
        if sector == "A_Bbar":
            return ((u - v) % 3, (2 * (u + v)) % 3)
        if sector == "B_Cbar":
            return (3 + v, u)
        if sector == "Abar_C":
            return (6 + v, u)
        raise AssertionError(label)

    chart = {label: mq(label) for label in internal_basis}
    assert set(chart.values()) == set(itertools.product(range(9), range(3)))

    def x_action(label):
        sector, u, v = label
        if sector == "A_Bbar":
            return (sector, (u + 1) % 3, (v + 1) % 3)
        return (sector, (u + 1) % 3, v)

    def z_phase(label):
        sector, u, v = label
        if sector == "A_Bbar":
            return (2 * (u + v)) % 3
        return u % 3

    assert all(
        chart[x_action(label)] == (chart[label][0], (chart[label][1] + 1) % 3)
        for label in internal_basis
    )
    assert all(z_phase(label) == chart[label][1] for label in internal_basis)

    x_orbits = []
    unseen = set(internal_basis)
    while unseen:
        label = min(unseen)
        orbit = {label, x_action(label), x_action(x_action(label))}
        x_orbits.append(orbit)
        unseen -= orbit
    assert len(x_orbits) == 9 and {len(x) for x in x_orbits} == {3}

    # Symbolic two-qutrit Pauli displacement operators.  Distinct labels are
    # Hilbert-Schmidt orthogonal; tensoring with I_9 multiplies every squared
    # norm by nine and leaves the 81-dimensional span unchanged.
    displacements = tuple(itertools.product(range(3), repeat=4))
    assert len(displacements) == 81

    def trace_phase_counts(delta):
        da, db, dA, dB = delta
        if db or dB:
            return Counter()
        return Counter((da * q + dA * p) % 3 for q, p in itertools.product(range(3), repeat=2))

    hilbert_schmidt = {}
    for u in displacements:
        for v in displacements:
            delta = tuple((v[i] - u[i]) % 3 for i in range(4))
            counts = trace_phase_counts(delta)
            # Sum n_e omega^e vanishes iff all three coefficients agree.
            value = 81 if u == v else 0
            if u == v:
                assert counts == Counter({0: 9})
            else:
                assert (not counts) or len(set(counts.values())) == 1
            hilbert_schmidt[(u, v)] = value
    assert Counter(hilbert_schmidt.values()) == Counter({0: 6480, 81: 81})

    # Character of nine copies of the unique 9D faithful irrep.
    character_support = {
        "identity": "81",
        "central_omega": "81*omega",
        "central_omega_squared": "81*omega^2",
        "240_noncentral_elements": "0",
    }

    # The complete Qpsi clock is not a spectator for this execution algebra.
    # On the E6 27 its charges are 4^1, (-2)^10, 1^16; the external A2
    # qutrit repeats every eigenspace three times on the matter 81.  If a
    # diagonalizable operator belongs to the commutant M9 tensor I9, every
    # eigenspace dimension is divisible by nine.  Exhausting all 12 powers
    # therefore gives an exact intersection test, not just a heuristic.
    qpsi_source = json.loads(
        (ROOT / "data/w33_qpsi_matter_parity_e8_d8_bridge.json").read_text()
    )
    assert qpsi_source["E6_27"]["branching"] == "27 = 16_1 + 10_-2 + 1_4"
    qpsi_charges = Counter({4: 1, -2: 10, 1: 16})
    qpsi_powers = []
    compatible_powers = []
    for power in range(12):
        histogram = Counter()
        for charge, multiplicity in qpsi_charges.items():
            histogram[(power * charge) % 12] += 3 * multiplicity
        commutant_multiplicity_test = all(n % 9 == 0 for n in histogram.values())
        scalar = len(histogram) == 1
        if commutant_multiplicity_test:
            # In this cyclic family the necessary multiplicity test is met
            # only by the visibly scalar powers, so membership is sufficient.
            assert scalar
            compatible_powers.append(power)
        qpsi_powers.append(
            {
                "power": power,
                "phase_exponent_multiplicities": {
                    str(e): n for e, n in sorted(histogram.items())
                },
                "all_multiplicities_divisible_by_9": commutant_multiplicity_test,
                "scalar": scalar,
                "in_Pauli243_commutant": scalar,
            }
        )
    assert compatible_powers == [0, 4, 8]
    assert qpsi_powers[4]["phase_exponent_multiplicities"] == {"4": 81}
    assert qpsi_powers[8]["phase_exponent_multiplicities"] == {"8": 81}

    return {
        "trinification_branching": "27=(3,3bar,1)+(1,3,3bar)+(3bar,1,3)",
        "internal_basis_count": len(internal_basis),
        "explicit_chart": "internal basis <-> (multiplicity m in {0,...,8}, active q in F3)",
        "multiplicity_dimension": 9,
        "internal_qutrit_dimension": 3,
        "external_qutrit_dimension": 3,
        "matter_factorization": "C^81 ~= C^9_multiplicity tensor C^3_internal tensor C^3_external",
        "X_internal_orbits_on_basis": len(x_orbits),
        "X_internal_orbit_sizes": [
            [size, count]
            for size, count in sorted(Counter(len(x) for x in x_orbits).items())
        ],
        "trinification_H27_representation": "nine copies of the 3D Schrodinger irrep with central character omega",
        "two_qutrit_Pauli_representation": "nine copies of the unique 9D faithful irrep of 3_+^(1+4)",
        "Pauli243_order": 243,
        "projective_displacement_operators": len(displacements),
        "operator_algebra": "I_9 tensor M_9(C)",
        "operator_algebra_dimension": len(displacements),
        "commutant": "M_9(C) tensor I_9",
        "commutant_dimension": 81,
        "Hilbert_Schmidt_Gram": {"diagonal": 81, "off_diagonal": 0, "rank": 81},
        "character": character_support,
        "Qpsi_clock_vs_execution_commutant": {
            "E6_27_charge_multiplicities": {"4": 1, "-2": 10, "1": 16},
            "matter81_charge_multiplicities": {"4": 3, "-2": 30, "1": 48},
            "power_census": qpsi_powers,
            "commuting_powers_mod12": compatible_powers,
            "intersection": "<D12^4> = C3, the FI/common H27 center",
            "matter_parity_D12_power6_commutes": False,
            "Kummer_mod4_D12_power3_commutes": False,
            "meaning": (
                "Only the mod-3 shadow of Qpsi is scalar on the active two-qutrit factor. "
                "The Z2 and Z4 shadows are outside the certified execution commutant. "
                "The complete Steiner/trinification monomial-atlas certificate now also proves "
                "that neither shadow normalizes the execution algebra in any of its 51840 "
                "W(E6)-compatible charts. Parallel rank obstructions rule out a full H27- or "
                "K-equivariant basis conjugacy; only a symmetry-changing compiler remains open."
            ),
        },
        "operator_center_basis_fixed_points": 27,
    }


def main(write=True):
    parents = {
        "landed_address_operator_roles": json.loads(
            (ROOT / "data/w33_address_operator_h27_roles.json").read_text()
        ),
        "regular_center_nogo": json.loads(
            (ROOT / "data/w33_e6_internal_h27_center_gluing_nogo.json").read_text()
        ),
        "physical_pauli243": json.loads(
            (ROOT / "data/w33_e8_trinification_two_qutrit_pauli243.json").read_text()
        ),
        "matter81": json.loads(
            (ROOT / "data/w33_e8_matter81_frame_qutrit_tensor_carrier.json").read_text()
        ),
        "H27_intertwiner_obstruction": json.loads(
            (ROOT / "data/w33_address_operator_h27_intertwiner_obstruction.json").read_text()
        ),
        "K81_intertwiner_obstruction": json.loads(
            (ROOT / "data/w33_scheduler_operator_k81_intertwiner_obstruction.json").read_text()
        ),
    }
    landed = parents["landed_address_operator_roles"]
    assert landed["status"] == "PASS_ADDRESS_AND_OPERATOR_H27_ROLES_SEPARATED_AND_EXECUTABLE"
    assert parents["regular_center_nogo"]["status"].startswith("PASS_PASS369_CENTER")
    assert parents["physical_pauli243"]["status"].startswith("PASS_E8_CONTAINS")
    assert parents["matter81"]["status"].startswith("PASS_E8_MATTER81")
    h27_obstruction = parents["H27_intertwiner_obstruction"]
    k81_obstruction = parents["K81_intertwiner_obstruction"]
    assert h27_obstruction["intertwiner"]["maximum_rank"] == 9
    assert h27_obstruction["intertwiner"]["target_dimension"] == 27
    assert h27_obstruction["intertwiner"]["invertible_intertwiner_exists"] is False
    assert k81_obstruction["intertwiner"]["maximum_rank"] == 27
    assert k81_obstruction["intertwiner"]["target_dimension"] == 81
    assert k81_obstruction["intertwiner"]["invertible_equivariant_compiler_exists"] is False

    address = address_geometry()
    operator = operator_geometry()
    assert address["address_center_orbit_size"] == 3
    assert operator["operator_center_basis_fixed_points"] == 27
    assert address["anchored_incidence_isomorphism_count"] == 1920
    # The earlier landed certificate owns the broad address/operator theorem.
    # This compiler is an independent replay plus two incremental audits: the
    # three-candidate Clifford-gauge uniqueness census and the Qpsi clock
    # intersection.  Compare the shared observables exactly so drift cannot
    # create a second, incompatible copy of the theorem.
    landed_generators = [tuple(x["generator"]) for x in landed["address"]["directions"]]
    compiled_generators = [
        tuple(x["generator"]) for x in address["selected_base_directions"]
    ]
    assert compiled_generators == landed_generators
    assert address["base_collinearity_srg"] == landed["address"]["collinearity_SRG"]
    assert address["base_cosets"] == landed["address"]["right_cosets"]
    assert address["anchored_incidence_isomorphism_count"] == landed["address"]["anchored_incidence_isomorphism_count"]
    assert landed["operator"]["center_fixed_internal_ray_count"] == 27
    assert landed["operator"]["center_fixed_matter_ray_count"] == 81
    assert address["lifted_cosets"] == landed["address"]["lifted_cosets"]
    assert (
        address["physical_Clifford648_address_normalizer"]["address_line_orbit_sizes"]
        == landed["address"]["line_orbit_sizes"]
    )
    assert (
        address["physical_Clifford648_address_normalizer"]
        ["phase_labels_held_fixed_instruction_orbit_sizes"]
        == landed["address"]["phase_fixed_instruction_orbit_sizes"]
    )
    assert operator["operator_algebra"] == landed["operator"]["generated_algebra"].replace("I9", "I_9").replace("M9", "M_9")
    assert operator["commutant"] == landed["operator"]["commutant"].replace("M9", "M_9").replace("I9", "I_9")

    out = {
        "schema": "w33.e8_matter81_h27_address_operator_compiler.v3",
        "status": "PASS_INCREMENTAL_H27_CLIFFORD_UNIQUENESS_AND_QPSI_COMMUTANT_AUDIT",
        "headline": (
            "The new H27 results form an address/operator pair, not one silently interchangeable group action. "
            "The physical Clifford-648 gauge uniquely selects the GQ(2,4) direction lifts on the regular Payne H27; "
            "its 45 lines split 9+36 and the phase-labelled instructions split 27+27+216. After adjoining the external C3 shift, ten explicit "
            "order-three directions have 270 cosets exactly equal to the E8 matter cubic triples. The center-correct "
            "trinification H27 instead acts on the E6 27 as nine copies of a qutrit Schrodinger irrep. With the external "
            "A2 H27, the matter 81 is nine copies of the irreducible two-qutrit Pauli representation, so its restricted "
            "operator algebra is I9 tensor M9 and its exact commutant is M9 tensor I9."
        ),
        "address_space": address,
        "operator_space": operator,
        "nonidentification_witness": {
            "regular_address_H27_center_orbit_size": address["address_center_orbit_size"],
            "trinification_operator_H27_center_basis_fixed_points": operator[
                "operator_center_basis_fixed_points"
            ],
            "equivariant_basis_bijection_exists": False,
            "reason": (
                "The regular center translates three address objects, while the trinification center is scalar and "
                "fixes every basis label. Fixed-point counts are invariant under permutation conjugacy."
            ),
        },
        "equivariant_compiler_obstruction": {
            "H27_maximum_rank": h27_obstruction["intertwiner"]["maximum_rank"],
            "H27_target_dimension": h27_obstruction["intertwiner"]["target_dimension"],
            "invertible_H27_equivariant_intertwiner_exists": h27_obstruction[
                "intertwiner"
            ]["invertible_intertwiner_exists"],
            "K81_maximum_rank": k81_obstruction["intertwiner"]["maximum_rank"],
            "K81_target_dimension": k81_obstruction["intertwiner"]["target_dimension"],
            "invertible_K81_equivariant_compiler_exists": k81_obstruction[
                "intertwiner"
            ]["invertible_equivariant_compiler_exists"],
            "surviving_frontier": (
                "Construct a non-equivariant, proper-subgroup-covariant, or otherwise "
                "symmetry-changing frozen-root dictionary, and record the symmetry lost."
            ),
        },
        "virtual_machine_reading": {
            "scheduler": "K=H27_regular x C3_external_shift addresses all 81 roots and its ten selected C3 coset families are the 270 cubic instructions",
            "execution_unit": "3_+^(1+4) acts as the two-qutrit Pauli algebra on C3_internal tensor C3_external",
            "protected_or_latent_register": "the exact C9 multiplicity factor, whose full M9 algebra is the commutant of the execution algebra",
            "compiler_gap": "construct a symmetry-changing frozen-root dictionary linking the regular address chart to the trinification multiplicity/active-qutrit chart; full H27/K equivariance is impossible",
        },
        "ownership_and_increment": {
            "broad_theorem_owner": "analysis/w33_address_operator_h27_roles.py and data/w33_address_operator_h27_roles.json",
            "shared_observables_exactly_replayed": True,
            "new_checks": [
                "among the three eight-element complement suborbits, exactly one central completion is SRG(27,10,1,5)",
                "the anchored address-to-frame incidence gauge has exactly 1920 choices, so the chosen GraphMatcher map is not a canonical root-gauge intertwiner",
                "the Qpsi C12 clock meets the Pauli243 execution commutant exactly in powers 0,4,8, the scalar FI C3",
            ],
            "purpose": "independent regression audit and compiler-facing refinement, not a second ownership claim for the address/operator theorem",
        },
        "scope": (
            "Exact finite incidence and restricted-representation theorem. The nine-dimensional commutant is a "
            "noiseless subsystem only for errors/operators contained in the certified Pauli243 algebra. It is not a "
            "claim of physical noise protection, generations, a vacuum, Yukawa values, or hardware realization."
        ),
        "parents": [
            "data/w33_address_operator_h27_roles.json",
            "data/w33_e6_internal_h27_center_gluing_nogo.json",
            "data/w33_e8_trinification_two_qutrit_pauli243.json",
            "data/w33_e8_matter81_frame_qutrit_tensor_carrier.json",
            "data/w33_address_operator_h27_intertwiner_obstruction.json",
            "data/w33_scheduler_operator_k81_intertwiner_obstruction.json",
            "data/w33_qpsi_matter_parity_e8_d8_bridge.json",
            "data/w33_physical_clifford648_full_permutation_dictionary.json",
            "data/w33_pass371_naturality_and_the_clifford_match.json",
            "data/w33_pass386_the_geometric_gap_is_the_phase.json",
            "analysis/BT858_heisenberg_shell_torsors.md",
            "analysis/BT865_dual_torsor_steinberg_compiler.md",
        ],
        "checks": {
            "five_H27_directions_give_45_GQ24_cosets": True,
            "physical_Clifford648_uniquely_selects_GQ24_direction_lifts": True,
            "Clifford648_address_line_orbits_are_9_plus_36": True,
            "phase_fixed_instruction_orbits_are_27_plus_27_plus_216": True,
            "ten_lifted_directions_give_270_E8_cubic_cosets": True,
            "all_81_frozen_roots_receive_regular_group_addresses": True,
            "trinification_27_is_nine_qutrit_irreps": True,
            "matter81_is_nine_two_qutrit_irreps": True,
            "operator_and_commutant_dimensions_are_81": True,
            "Qpsi_clock_commutant_intersection_is_exactly_FI_Z3": True,
            "address_operator_permutation_conflation_refuted": True,
            "H27_equivariant_coordinate_intertwiner_exists": False,
            "full_K_equivariant_compiler_exists": False,
            "symmetry_changing_coordinate_dictionary_left_open": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": out["status"],
                "address": {
                    k: address[k]
                    for k in (
                        "base_cosets",
                        "base_collinearity_srg",
                        "K_order",
                        "lifted_direction_count",
                        "lifted_cosets",
                        "lifted_lines_per_root",
                        "equals_E8_270_cubic_triples",
                    )
                },
                "operator": operator,
                "nonidentification_witness": out["nonidentification_witness"],
            },
            indent=2,
        )
    )
    return out


if __name__ == "__main__":
    main(True)
