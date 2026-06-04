"""W(3,3) BREAKTHROUGH 157: Cayley compiler macro-depth correction.

BT156 fixed the ISA class-count layer.  The next architecture claim to
stress-test is the compiler-depth layer:

    "8 generator lanes should reach every symmetry in <= q! steps."

For the concrete eight transvection centers used throughout the repo, the
all-group Cayley BFS says something sharper and more useful:

    8 forward elementary lanes      diameter 9 = q^2
    16 inverse-complete directions  diameter 7 = q! + 1
    + one macro/inverse pair        diameter 6 = q!

So the raw generator story was too optimistic, but the architecture can be
made exact: keep the 8 hardware lanes, expose the inverse directions as
directed pulses, and add one receipt-bearing order-9 macro pair from the
distance-7 tail.  That collapses the full 51,840-element compiler table to
the master-equation depth q! = 6.
"""

from __future__ import annotations

from collections import Counter, deque
import json
from pathlib import Path


Q = 3
LAMBDA = 2
MU = 4
QFACT = 6
V = 40
GROUP_ORDER = 51_840

CENTERS = [
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
    (1, 1, 0, 0),
    (1, 0, 1, 0),
    (0, 1, 0, 1),
    (1, 0, 0, 1),
]


def mat_id() -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))


def mat_mul(
    a: tuple[tuple[int, ...], ...],
    b: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4))
        for i in range(4)
    )


def mat_inv(m: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    n = 4
    aug = [
        [m[i][j] for j in range(n)] + [1 if i == j else 0 for j in range(n)]
        for i in range(n)
    ]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col] % 3)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = pow(aug[col][col] % 3, -1, 3)
        aug[col] = [(x * scale) % 3 for x in aug[col]]
        for row in range(n):
            if row != col and aug[row][col] % 3:
                factor = aug[row][col] % 3
                aug[row] = [(aug[row][j] - factor * aug[col][j]) % 3 for j in range(2 * n)]
    return tuple(tuple(aug[i][n:]) for i in range(n))


def mat_order(m: tuple[tuple[int, ...], ...], max_order: int = 200) -> int:
    ident = mat_id()
    cur = ident
    for order in range(1, max_order + 1):
        cur = mat_mul(cur, m)
        if cur == ident:
            return order
    raise ValueError("matrix order exceeds bound")


def transvection(center: tuple[int, int, int, int], scale: int = 1) -> tuple[tuple[int, ...], ...]:
    c = list(center)
    jc = [c[1], (3 - c[0]) % 3, c[3], (3 - c[2]) % 3]
    return tuple(
        tuple(((1 if i == j else 0) + scale * c[i] * jc[j]) % 3 for j in range(4))
        for i in range(4)
    )


def generator_set(include_inverses: bool) -> tuple[list[tuple[tuple[int, ...], ...]], list[str]]:
    gens = []
    labels = []
    scales = (1, 2) if include_inverses else (1,)
    for center_index, center in enumerate(CENTERS, start=1):
        for scale in scales:
            gens.append(transvection(center, scale))
            labels.append(f"T{center_index}^{scale}")
    return gens, labels


def build_group(
    gens: list[tuple[tuple[int, ...], ...]],
) -> tuple[
    list[tuple[tuple[int, ...], ...]],
    dict[tuple[tuple[int, ...], ...], int],
    list[int],
    list[int],
]:
    ident = mat_id()
    elems = [ident]
    index = {ident: 0}
    parent = [-1]
    parent_gen = [-1]
    queue = deque([0])

    while queue:
        elem_index = queue.popleft()
        elem = elems[elem_index]
        for gen_index, gen in enumerate(gens):
            nxt = mat_mul(elem, gen)
            if nxt not in index:
                index[nxt] = len(elems)
                elems.append(nxt)
                parent.append(elem_index)
                parent_gen.append(gen_index)
                queue.append(index[nxt])
    return elems, index, parent, parent_gen


def right_maps(
    elems: list[tuple[tuple[int, ...], ...]],
    index: dict[tuple[tuple[int, ...], ...], int],
    gens: list[tuple[tuple[int, ...], ...]],
) -> list[list[int]]:
    return [[index[mat_mul(elem, gen)] for elem in elems] for gen in gens]


def bfs_from_maps(maps: list[list[int]], size: int) -> list[int]:
    dist = [-1] * size
    dist[0] = 0
    queue = deque([0])
    while queue:
        elem_index = queue.popleft()
        next_dist = dist[elem_index] + 1
        for action in maps:
            nxt = action[elem_index]
            if dist[nxt] < 0:
                dist[nxt] = next_dist
                queue.append(nxt)
    return dist


def distribution(dist: list[int]) -> dict[int, int]:
    return dict(sorted(Counter(dist).items()))


def reconstruct_word(elem_index: int, parent: list[int], parent_gen: list[int], labels: list[str]) -> list[str]:
    word = []
    cursor = elem_index
    while cursor != 0:
        word.append(labels[parent_gen[cursor]])
        cursor = parent[cursor]
    return list(reversed(word))


def cayley_compiler_macro_packet() -> dict:
    forward_gens, forward_labels = generator_set(include_inverses=False)
    symmetric_gens, symmetric_labels = generator_set(include_inverses=True)

    elems, index, parent, parent_gen = build_group(symmetric_gens)
    forward_dist = bfs_from_maps(right_maps(elems, index, forward_gens), len(elems))
    symmetric_maps = right_maps(elems, index, symmetric_gens)
    symmetric_dist = bfs_from_maps(symmetric_maps, len(elems))

    tail = [i for i, dist in enumerate(symmetric_dist) if dist == QFACT + 1]
    macro_index = tail[0]
    macro = elems[macro_index]
    macro_inverse = mat_inv(macro)
    macro_maps = right_maps(elems, index, [macro, macro_inverse])
    macro_dist = bfs_from_maps(symmetric_maps + macro_maps, len(elems))

    forward_distribution = distribution(forward_dist)
    symmetric_distribution = distribution(symmetric_dist)
    macro_distribution = distribution(macro_dist)

    checks = {
        "group_size_is_aut_w33": len(elems) == GROUP_ORDER,
        "forward_diameter_is_q_squared": max(forward_dist) == Q**2 == 9,
        "symmetric_diameter_is_q_factorial_plus_one": max(symmetric_dist) == QFACT + 1 == 7,
        "raw_q_factorial_claim_is_false": max(symmetric_dist) > QFACT,
        "macro_diameter_is_q_factorial": max(macro_dist) == QFACT == 6,
        "macro_order_is_q_squared": mat_order(macro) == Q**2 == 9,
        "macro_word_has_length_q_factorial_plus_one": len(reconstruct_word(macro_index, parent, parent_gen, symmetric_labels)) == QFACT + 1,
        "symmetric_tail_size_is_4v_minus_q_squared": len(tail) == 4 * V - Q**2 == 151,
        "macro_tail_removed": macro_distribution.get(QFACT + 1, 0) == 0,
        "macro_depth_six_shell_is_1217": macro_distribution[QFACT] == 1217,
        "forward_tail_size_is_310": forward_distribution[Q**2] == 310,
        "macro_generator_count_is_18_directed_pulses": len(symmetric_gens) + 2 == 18,
    }

    return {
        "breakthrough": 157,
        "title": "Cayley compiler macro-depth correction",
        "generator_centers": CENTERS,
        "forward_generator_labels": forward_labels,
        "symmetric_generator_labels": symmetric_labels,
        "group_order": len(elems),
        "forward_distribution": forward_distribution,
        "symmetric_distribution": symmetric_distribution,
        "macro_distribution": macro_distribution,
        "diameters": {
            "8_forward_lanes": max(forward_dist),
            "16_inverse_complete_pulses": max(symmetric_dist),
            "18_with_macro_pair": max(macro_dist),
        },
        "macro": {
            "selection_rule": "first element in the inverse-complete distance-7 BFS tail",
            "index": macro_index,
            "order": mat_order(macro),
            "word": reconstruct_word(macro_index, parent, parent_gen, symmetric_labels),
            "matrix": [list(row) for row in macro],
        },
        "architectural_correction": (
            "The concrete 8-lane transvection compiler does not have raw q! depth. "
            "Forward-only lanes have diameter q^2=9; inverse-complete directed pulses "
            "have diameter q!+1=7. A single order-9 macro/inverse pair from the "
            "distance-7 tail restores exact q!=6 global dispatch."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = cayley_compiler_macro_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 157: CAYLEY COMPILER MACRO-DEPTH")
    print("=" * 78)
    print()
    print("DIAMETERS:")
    for key, value in packet["diameters"].items():
        print(f"  {key:<32s} = {value}")
    print()
    print("DISTANCE DISTRIBUTIONS:")
    print(f"  8 forward lanes:             {packet['forward_distribution']}")
    print(f"  16 inverse-complete pulses:  {packet['symmetric_distribution']}")
    print(f"  18 with macro pair:          {packet['macro_distribution']}")
    print()
    print("MACRO:")
    print(f"  order = {packet['macro']['order']}")
    print(f"  word  = {' '.join(packet['macro']['word'])}")
    print(f"  matrix = {packet['macro']['matrix']}")
    print()
    print("ARCHITECTURAL CORRECTION:")
    print(f"  {packet['architectural_correction']}")

    out = Path("data") / "w33_BREAKTHROUGH_157_cayley_compiler_macro_depth.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")
    print(f"verified {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
