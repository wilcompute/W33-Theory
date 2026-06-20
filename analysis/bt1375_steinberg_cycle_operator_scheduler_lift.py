#!/usr/bin/env python3
"""BT1375: Steinberg scheduler as a concrete cycle-vector operator.

BT1372 assigned the 2160 scheduler slots to Steinberg basis labels.  BT1375
checks the missing linear layer: the generation advance is the actual order-3
central operator on the concrete BT865 cycle-vector witnesses.

The construction rebuilds the W(3,3) triangle chain complex over F3, reloads
BT865's first Heisenberg free-module witnesses, generates their 3 x 27 orbit
basis vectors, and acts on those vectors by the unique center of the
Heisenberg O3.  The operator is a permutation of the concrete cycle witnesses;
over F3 its nilpotent part has ranks 54, 27, 0, exactly the BT865 triality
filtration and exactly the BT1372 three-epoch scheduler clock.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

P = 3
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1375_steinberg_cycle_operator_scheduler_lift.json"


def canon(v: Iterable[int]) -> tuple[int, ...]:
    vv = tuple(int(x) % P for x in v)
    for x in vv:
        if x % P:
            scale = 1 if x % P == 1 else 2
            return tuple((scale * y) % P for y in vv)
    raise ValueError("zero vector")


def rref_mod3(matrix: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    a = [[int(x) % P for x in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    pivots: list[int] = []
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        if a[r][c] == 2:
            a[r] = [(2 * x) % P for x in a[r]]
        for i in range(rows):
            if i == r or not a[i][c]:
                continue
            factor = a[i][c]
            a[i] = [(a[i][j] - factor * a[r][j]) % P for j in range(cols)]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return a, pivots


def nullspace_mod3(matrix: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    rref, pivots = rref_mod3(matrix)
    cols = len(matrix[0])
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for f in free:
        v = [0] * cols
        v[f] = 1
        for row, p in enumerate(pivots):
            v[p] = (-rref[row][f]) % P
        basis.append(v)
    return basis, pivots


class GF3Span:
    def __init__(self, vectors: Iterable[list[int]] = ()) -> None:
        self.pivots: dict[int, list[int]] = {}
        for v in vectors:
            self.add(v)

    @property
    def rank(self) -> int:
        return len(self.pivots)

    def copy(self) -> "GF3Span":
        out = GF3Span()
        out.pivots = {p: v[:] for p, v in self.pivots.items()}
        return out

    def reduce(self, vector: list[int]) -> list[int]:
        v = [int(x) % P for x in vector]
        while True:
            pivot = next((i for i, x in enumerate(v) if x), None)
            if pivot is None or pivot not in self.pivots:
                return v
            factor = v[pivot]
            row = self.pivots[pivot]
            v = [(v[i] - factor * row[i]) % P for i in range(len(v))]

    def add(self, vector: list[int]) -> bool:
        v = self.reduce(vector)
        pivot = next((i for i, x in enumerate(v) if x), None)
        if pivot is None:
            return False
        if v[pivot] == 2:
            v = [(2 * x) % P for x in v]
        self.pivots[pivot] = v
        return True


def build_w33_chain() -> dict[str, object]:
    pts = sorted({canon(v) for v in product(range(P), repeat=4) if any(v)})
    pt_index = {p: i for i, p in enumerate(pts)}

    def symp(x: tuple[int, ...], y: tuple[int, ...]) -> int:
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % P

    adj = [[False] * len(pts) for _ in pts]
    for i, j in combinations(range(len(pts)), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True

    lines = [
        frozenset(q)
        for q in combinations(range(len(pts)), 4)
        if all(adj[i][j] for i, j in combinations(q, 2))
    ]
    edges = sorted((i, j) for i, j in combinations(range(len(pts)), 2) if adj[i][j])
    edge_index = {edge: i for i, edge in enumerate(edges)}
    triangles = sorted(
        {tuple(sorted(t)) for line in lines for t in combinations(sorted(line), 3)}
    )

    d0 = [[0] * len(edges) for _ in range(len(pts))]
    for ei, (a, b) in enumerate(edges):
        d0[a][ei] = 2
        d0[b][ei] = 1
    d1_columns = []
    for x, y, z in triangles:
        col = [0] * len(edges)
        col[edge_index[(y, z)]] = 1
        col[edge_index[(x, z)]] = 2
        col[edge_index[(x, y)]] = 1
        d1_columns.append(col)

    cycle_basis, d0_pivots = nullspace_mod3(d0)
    boundary_span = GF3Span(d1_columns)
    if not (
        len(pts) == 40
        and len(lines) == 40
        and len(edges) == 240
        and len(triangles) == 160
        and len(d0_pivots) == 39
        and len(cycle_basis) == 201
        and boundary_span.rank == 120
    ):
        raise AssertionError("W33 chain complex drift")

    identity = tuple(range(len(pts)))

    def transvection_perm(v: tuple[int, ...]) -> tuple[int, ...]:
        out = []
        for x in pts:
            w = symp(x, v)
            out.append(pt_index[canon((x[t] + w * v[t]) % P for t in range(4))])
        return tuple(out)

    generators = [transvection_perm(v) for v in pts]

    def compose(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(a[b[i]] for i in range(len(a)))

    psp = {identity}
    frontier = [identity]
    while frontier:
        nxt = []
        for g in frontier:
            for h in generators:
                hg = compose(h, g)
                if hg not in psp:
                    psp.add(hg)
                    nxt.append(hg)
        frontier = nxt
    if len(psp) != 25920:
        raise AssertionError("PSp(4,3) generation drift")

    return {
        "pts": pts,
        "adj": adj,
        "edges": edges,
        "edge_index": edge_index,
        "cycle_basis": cycle_basis,
        "boundary_span": boundary_span,
        "identity": identity,
        "psp": sorted(psp),
        "compose": compose,
    }


def order(g: tuple[int, ...], identity: tuple[int, ...], compose) -> int:
    value = 1
    current = g
    while current != identity:
        current = compose(g, current)
        value += 1
    return value


def inverse(g: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(g)
    for i, x in enumerate(g):
        out[x] = i
    return tuple(out)


def subgroup_generated(
    gens: list[tuple[int, ...]],
    identity: tuple[int, ...],
    compose,
    limit: int = 1000,
) -> set[tuple[int, ...]]:
    group = {identity}
    frontier = [identity]
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                y = compose(g, x)
                if y not in group:
                    group.add(y)
                    if len(group) > limit:
                        return group
                    nxt.append(y)
        frontier = nxt
    return group


def find_point_o3(
    chain: dict[str, object]
) -> tuple[set[tuple[int, ...]], tuple[int, ...]]:
    psp: list[tuple[int, ...]] = chain["psp"]  # type: ignore[assignment]
    identity: tuple[int, ...] = chain["identity"]  # type: ignore[assignment]
    compose = chain["compose"]
    stabilizer = [g for g in psp if g[0] == 0]
    threes = [g for g in stabilizer if order(g, identity, compose) == 3]
    rng = random.Random(86501)
    for _attempt in range(1, 12001):
        chosen = [rng.choice(threes) for _ in range(3)]
        subgroup = subgroup_generated(chosen, identity, compose, limit=27)
        if len(subgroup) != 27:
            continue
        normal = True
        for c in stabilizer:
            ci = inverse(c)
            if any(compose(compose(c, x), ci) not in subgroup for x in subgroup):
                normal = False
                break
        if normal:
            center = {
                g
                for g in subgroup
                if all(compose(g, h) == compose(h, g) for h in subgroup)
            }
            if len(center) != 3:
                raise AssertionError("Heisenberg center drift")
            z = next(g for g in sorted(center) if g != identity)
            return subgroup, z
    raise RuntimeError("normal point O3 search failed")


def act_on_edges(
    g: tuple[int, ...],
    vector: list[int],
    edges: list[tuple[int, int]],
    edge_index: dict[tuple[int, int], int],
) -> list[int]:
    out = [0] * len(edges)
    for ei, coefficient in enumerate(vector):
        if not coefficient:
            continue
        a, b = edges[ei]
        ga, gb = g[a], g[b]
        if ga < gb:
            gi, sign = edge_index[(ga, gb)], 1
        else:
            gi, sign = edge_index[(gb, ga)], 2
        out[gi] = (out[gi] + sign * coefficient) % P
    return out


def add_vectors(a: list[int], b: list[int], scale: int = 1) -> list[int]:
    return [(a[i] + scale * b[i]) % P for i in range(len(a))]


def load_witness_vector(witness: dict[str, object], edge_count: int) -> list[int]:
    vector = [0] * edge_count
    support = witness["support"]
    coefficients = witness["coefficients"]
    for edge, coefficient in zip(support, coefficients):
        vector[int(edge)] = int(coefficient) % P
    return vector


def matrix_rank_mod3(rows: list[list[int]]) -> int:
    return len(rref_mod3(rows)[1]) if rows else 0


def build_result() -> dict[str, object]:
    bt865 = json.loads(
        (ROOT / "data" / "bt865_dual_torsor_steinberg_compiler.json").read_text(
            encoding="utf-8"
        )
    )
    bt1372 = json.loads(
        (
            ROOT / "data" / "bt1372_three_epoch_steinberg_basis_scheduler_lift.json"
        ).read_text(encoding="utf-8")
    )
    chain = build_w33_chain()
    point_o3, central_z = find_point_o3(chain)
    group_ordered = sorted(point_o3)
    edges: list[tuple[int, int]] = chain["edges"]  # type: ignore[assignment]
    edge_index: dict[tuple[int, int], int] = chain["edge_index"]  # type: ignore[assignment]
    boundary_span: GF3Span = chain["boundary_span"]  # type: ignore[assignment]

    witnesses = bt865["point_state_torsor"]["orbit_basis_witnesses"]
    basis_vectors: list[list[int]] = []
    basis_labels = []
    for copy_index, witness in enumerate(witnesses):
        seed = load_witness_vector(witness, len(edges))
        for group_index, g in enumerate(group_ordered):
            basis_vectors.append(act_on_edges(g, seed, edges, edge_index))
            basis_labels.append({"copy": copy_index, "group_index": group_index})

    span = boundary_span.copy()
    rank_gains = []
    for copy_index in range(3):
        before = span.rank
        for vector in basis_vectors[copy_index * 27 : (copy_index + 1) * 27]:
            span.add(vector)
        rank_gains.append(span.rank - before)

    vector_index = {tuple(vector): index for index, vector in enumerate(basis_vectors)}
    image = []
    image_failures = []
    for index, vector in enumerate(basis_vectors):
        z_vector = act_on_edges(central_z, vector, edges, edge_index)
        target = vector_index.get(tuple(z_vector))
        if target is None:
            image_failures.append(index)
            target = -1
        image.append(target)

    generation_cycles: dict[tuple[int, int], list[int]] = {}
    visited = set()
    for index, target in enumerate(image):
        if index in visited:
            continue
        cycle = []
        cur = index
        while cur not in cycle:
            cycle.append(cur)
            visited.add(cur)
            cur = image[cur]
        if len(cycle) != 3:
            raise AssertionError(("central cycle length drift", cycle))
        base_label = basis_labels[cycle[0]]
        # The 27 scheduler matter states are exactly:
        #   3 BT865 free copies x 9 central cosets per copy.
        matter_state = base_label["copy"] * 9 + len(
            [key for key in generation_cycles if key[0] == base_label["copy"]]
        )
        generation_cycles[(base_label["copy"], matter_state % 9)] = cycle

    scheduler_basis_map = []
    for matter_state in range(27):
        copy_index = matter_state // 9
        coset_index = matter_state % 9
        cycle = generation_cycles[(copy_index, coset_index)]
        for generation, basis_vector_index in enumerate(cycle):
            scheduler_basis_map.append(
                {
                    "steinberg_basis_index": generation * 27 + matter_state,
                    "generation": generation,
                    "matter_state": matter_state,
                    "bt865_copy": copy_index,
                    "central_coset": coset_index,
                    "cycle_vector_index": basis_vector_index,
                }
            )

    # Build the matrix of N = Z - I on the concrete basis permutation.
    n_rows = []
    n2_rows = []
    n3_rows = []
    for source, target in enumerate(image):
        row = [0] * 81
        row[target] = (row[target] + 1) % P
        row[source] = (row[source] - 1) % P
        n_rows.append(row)
    for row in n_rows:
        n2 = [0] * 81
        for source, coeff in enumerate(row):
            if coeff:
                n2 = add_vectors(n2, n_rows[source], coeff)
        n2_rows.append(n2)
    for row in n2_rows:
        n3 = [0] * 81
        for source, coeff in enumerate(row):
            if coeff:
                n3 = add_vectors(n3, n_rows[source], coeff)
        n3_rows.append(n3)

    cycle_lengths = Counter()
    for cycle in generation_cycles.values():
        cycle_lengths[len(cycle)] += 1

    bt1372_counts = Counter()
    for epoch in range(3):
        for orbit in range(135):
            lane = orbit // 27
            matter_state = orbit % 27
            for face_slot in range(16):
                local_slot = lane * 16 + face_slot
                generation = (local_slot + matter_state + epoch) % 3
                bt1372_counts[generation * 27 + matter_state] += 1

    checks = {
        "bt865_h1_dimension_loaded": bt865["chain_complex"]["dim_H1_mod3"] == 81,
        "bt1372_three_epoch_scheduler_loaded": bt1372["verified"] is True,
        "point_o3_order_27": len(point_o3) == 27,
        "three_orbit_copies_gain_27_each_mod_boundaries": rank_gains == [27, 27, 27],
        "orbit_basis_completes_cycle_space_mod_boundaries": span.rank == 201,
        "central_operator_maps_basis_vectors_to_basis_vectors": not image_failures,
        "central_operator_has_27_three_cycles": cycle_lengths == Counter({3: 27}),
        "scheduler_basis_map_has_81_rows": len(scheduler_basis_map) == 81,
        "nilpotent_rank_profile_matches_bt865": [
            matrix_rank_mod3(n_rows),
            matrix_rank_mod3(n2_rows),
            matrix_rank_mod3(n3_rows),
        ]
        == [54, 27, 0],
        "three_epoch_scheduler_uniform_on_operator_basis": set(bt1372_counts.values())
        == {80}
        and len(bt1372_counts) == 81,
    }

    return {
        "bt": 1375,
        "title": "Steinberg cycle-vector operator scheduler lift",
        "verified": all(checks.values()),
        "chain_complex": {
            "C1_edges": len(edges),
            "boundary_rank": boundary_span.rank,
            "basis_vectors": len(basis_vectors),
            "rank_gains_mod_boundaries": rank_gains,
            "final_rank_with_boundaries": span.rank,
        },
        "central_operator": {
            "source": "unique center C3 of the BT865 Heisenberg O3",
            "basis_image_sample": image[:18],
            "cycle_length_profile": {
                str(k): v for k, v in sorted(cycle_lengths.items())
            },
            "nilpotent_rank_profile": [
                matrix_rank_mod3(n_rows),
                matrix_rank_mod3(n2_rows),
                matrix_rank_mod3(n3_rows),
            ],
            "kernel_dimensions": [27, 54, 81],
        },
        "scheduler_alignment": {
            "matter_state_factorization": "27 = 3 BT865 free copies * 9 central cosets",
            "generation_factor": "position in the central C3 cycle",
            "three_epoch_uniform_count_per_basis": 80,
            "basis_map_sample": scheduler_basis_map[:18],
        },
        "interpretation": (
            "The BT1372 generation-time rule is not just a label schedule.  It "
            "is realized by the concrete central order-3 operator on BT865's "
            "Steinberg cycle-vector witnesses.  Matter states are the 3 free "
            "BT865 copies times 9 central cosets; generations are the three "
            "positions inside each central orbit."
        ),
        "boundary": (
            "This uses BT865's deterministic witness basis.  A different free "
            "basis conjugates the 81x81 operator, but the 27 three-cycles and "
            "nilpotent rank profile are invariant for the central C3 action."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "nilpotent_rank_profile": result["central_operator"][
                    "nilpotent_rank_profile"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
