"""W(3,3) BREAKTHROUGH 159: forbidden pocket F4 normalizer.

BT158 found an eight-element forbidden macro pocket inside the inverse-complete
distance-7 Cayley tail.  Those eight elements do not restore q! compiler
diameter when used as the single macro pair.

BT159 shows why they are not disposable:

    <forbidden pocket> has order 1152 = |W(F4)|
    = 576 block-diagonal polarization-preserving maps
    + 576 anti-diagonal polarization-swapping maps.

So the "bad" macro pocket is exactly the seed of the 24-cell/F4 control
normalizer.  It fails as a global diameter-collapse macro because it remains
inside the polarization normalizer, but as a generated group it recovers the
same F4/tomotope/24-cell symmetry that the geometry kept pointing toward.
"""

from __future__ import annotations

from collections import Counter, deque
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_157_cayley_compiler_macro_depth import (  # noqa: E402
    mat_id,
    mat_mul,
    mat_order,
)
from analysis.w33_BREAKTHROUGH_158_macro_tail_sieve import macro_tail_sieve_packet  # noqa: E402


Q = 3
LAMBDA = 2
MU = 4
F4_WEYL_ORDER = 1152
HALF_F4 = 576


def to_matrix_tuple(matrix: list[list[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(row) for row in matrix)


def mat_neg(matrix: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple((3 - entry) % 3 for entry in row) for row in matrix)


def zero_block(
    matrix: tuple[tuple[int, ...], ...],
    rows: range,
    cols: range,
) -> bool:
    return all(matrix[row][col] == 0 for row in rows for col in cols)


def is_block_diagonal(matrix: tuple[tuple[int, ...], ...]) -> bool:
    return zero_block(matrix, range(2), range(2, 4)) and zero_block(matrix, range(2, 4), range(2))


def is_anti_diagonal(matrix: tuple[tuple[int, ...], ...]) -> bool:
    return zero_block(matrix, range(2), range(2)) and zero_block(matrix, range(2, 4), range(2, 4))


def closure_generated_by(
    generators: list[tuple[tuple[int, ...], ...]],
) -> set[tuple[tuple[int, ...], ...]]:
    ident = mat_id()
    group = {ident, *generators}
    queue = deque(generators)

    while queue:
        current = queue.popleft()
        for generator in generators:
            for product in (mat_mul(current, generator), mat_mul(generator, current)):
                if product not in group:
                    group.add(product)
                    queue.append(product)
    return group


def inverse_by_power(matrix: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    ident = mat_id()
    current = ident
    for _ in range(mat_order(matrix) - 1):
        current = mat_mul(current, matrix)
    return current


def forbidden_pocket_f4_packet() -> dict:
    tail_packet = macro_tail_sieve_packet()
    forbidden = [to_matrix_tuple(row["matrix"]) for row in tail_packet["forbidden_macros"]]
    forbidden_set = set(forbidden)
    generated = closure_generated_by(forbidden)
    ident = mat_id()
    neg_ident = mat_neg(ident)

    order_distribution = dict(sorted(Counter(mat_order(matrix) for matrix in generated).items()))
    forbidden_order_distribution = dict(sorted(Counter(mat_order(matrix) for matrix in forbidden).items()))
    block_count = sum(is_block_diagonal(matrix) for matrix in generated)
    anti_count = sum(is_anti_diagonal(matrix) for matrix in generated)
    pair_products = Counter()
    for left in forbidden:
        for right in forbidden:
            product = mat_mul(left, right)
            if product == ident:
                pair_products["identity"] += 1
            elif product in forbidden_set:
                pair_products["forbidden"] += 1
            else:
                pair_products["normalizer_other"] += 1

    checks = {
        "forbidden_pocket_size_is_2_to_q": len(forbidden) == 2**Q == 8,
        "forbidden_generates_f4_order": len(generated) == F4_WEYL_ORDER,
        "f4_order_is_24cell_weyl": F4_WEYL_ORDER == 2**7 * Q**2,
        "generated_split_is_576_plus_576": block_count == anti_count == HALF_F4,
        "generated_has_only_block_or_anti": block_count + anti_count == len(generated),
        "forbidden_are_all_anti_diagonal": all(is_anti_diagonal(matrix) for matrix in forbidden),
        "forbidden_order_distribution_is_binary_twelve": forbidden_order_distribution == {2: 4, 12: 4},
        "forbidden_inverse_closed": all(inverse_by_power(matrix) in forbidden_set for matrix in forbidden),
        "forbidden_pair_products_are_identity_or_normalizer": dict(pair_products)
        == {"identity": 8, "normalizer_other": 56},
        "negative_identity_in_generated_group": neg_ident in generated,
        "order_distribution_sums_to_1152": sum(order_distribution.values()) == F4_WEYL_ORDER,
        "order_distribution_matches_closure": order_distribution
        == {1: 1, 2: 27, 3: 80, 4: 84, 6: 432, 8: 144, 12: 384},
    }

    return {
        "breakthrough": 159,
        "title": "Forbidden pocket F4 normalizer",
        "forbidden_pocket_size": len(forbidden),
        "generated_order": len(generated),
        "generated_order_reading": "1152 = |W(F4)| = full 24-cell Weyl group order",
        "polarization_split": {
            "block_diagonal_preserving": block_count,
            "anti_diagonal_swapping": anti_count,
        },
        "forbidden_order_distribution": forbidden_order_distribution,
        "generated_order_distribution": order_distribution,
        "forbidden_pair_products": dict(pair_products),
        "architectural_reading": (
            "The eight BT158 forbidden macros are not failed design noise. They "
            "generate the F4-sized polarization normalizer: 576 maps preserving "
            "the 2+2 Lagrangian split and 576 maps swapping it. They fail as "
            "single q!-restoring macros because they stay inside this normalizer, "
            "but they are exactly the 24-cell/tomotope control pocket."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = forbidden_pocket_f4_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 159: FORBIDDEN POCKET F4 NORMALIZER")
    print("=" * 78)
    print()
    print("FORBIDDEN POCKET:")
    print(f"  size            = {packet['forbidden_pocket_size']} = 2^q")
    print(f"  generated order = {packet['generated_order']} = |W(F4)|")
    print()
    print("POLARIZATION SPLIT:")
    for key, value in packet["polarization_split"].items():
        print(f"  {key:<28s} = {value}")
    print()
    print("ORDER DISTRIBUTIONS:")
    print(f"  forbidden = {packet['forbidden_order_distribution']}")
    print(f"  generated = {packet['generated_order_distribution']}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_159_forbidden_pocket_f4_normalizer.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")
    print(f"verified {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
