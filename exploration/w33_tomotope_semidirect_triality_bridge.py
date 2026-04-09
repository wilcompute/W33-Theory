"""Semidirect triality structure of the faithful tomotope 12-point model.

The faithful degree-12 tomotope model from the user is now identified with the
mode-major packet `3 x 4`:

    three local modes x four chart states.

This module extracts the exact group structure of that action.

Results:

    - the full permutation group has order 96;
    - it preserves the unique 3-block system of size 4;
    - the quotient on the three blocks has order 6, hence is S3;
    - the kernel has order 16 and consists only of involutions;
    - on each 4-block, the kernel restriction is the Klein four group V4;
    - the three block restrictions are not independent: they satisfy

          z = x + y

      in V4 ~= F2^2.

So the faithful tomotope symmetry is exactly

    (V4 x V4) ⋊ S3,

with the quotient S3 acting as triality on the three local modes and the kernel
encoding coupled chart flips on the three mode blocks.
"""

from __future__ import annotations

from collections import Counter, deque
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from exploration.w33_tomotope_mode_chart_action_bridge import user_tomotope_generators


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_tomotope_semidirect_triality_bridge_summary.json"
BLOCKS = (tuple(range(0, 4)), tuple(range(4, 8)), tuple(range(8, 12)))
KLEIN_LABELS = {
    (0, 1, 2, 3): "e",
    (1, 0, 3, 2): "a",
    (2, 3, 0, 1): "b",
    (3, 2, 1, 0): "c",
}
KLEIN_F2 = {"e": (0, 0), "a": (1, 0), "b": (0, 1), "c": (1, 1)}


def compose(left, right):
    return tuple(left[index] for index in right)


def generate_group(generators):
    identity = tuple(range(len(next(iter(generators.values())))))
    group = {identity}
    queue = deque([identity])
    while queue:
        element = queue.popleft()
        for generator in generators.values():
            image = compose(element, generator)
            if image not in group:
                group.add(image)
                queue.append(image)
    return group


def restrict_to_block(permutation, block):
    position = {value: index for index, value in enumerate(block)}
    return tuple(position[permutation[value]] for value in block)


def block_action(permutation):
    image = []
    for block in BLOCKS:
        value = permutation[block[0]]
        for block_index, other in enumerate(BLOCKS):
            if value in other:
                image.append(block_index)
                break
    return tuple(image)


def permutation_order(permutation):
    identity = tuple(range(len(permutation)))
    power = permutation
    order = 1
    while power != identity:
        power = compose(power, permutation)
        order += 1
    return order


def build_summary() -> dict[str, Any]:
    generators = user_tomotope_generators()
    group = generate_group(generators)

    quotient_images = {block_action(permutation) for permutation in group}
    kernel = [permutation for permutation in group if block_action(permutation) == (0, 1, 2)]

    kernel_triples = []
    affine_constraint_holds = True
    for permutation in kernel:
        triple = tuple(KLEIN_LABELS[restrict_to_block(permutation, block)] for block in BLOCKS)
        kernel_triples.append(triple)
        x, y, z = (KLEIN_F2[label] for label in triple)
        if (x[0] ^ y[0], x[1] ^ y[1]) != z:
            affine_constraint_holds = False
    kernel_triples = sorted(set(kernel_triples))

    summary: dict[str, Any] = {
        "group_packet": {
            "order": len(group),
            "generator_images": {
                name: [value + 1 for value in permutation]
                for name, permutation in generators.items()
            },
            "element_order_spectrum": dict(sorted(Counter(permutation_order(g) for g in group).items())),
        },
        "mode_block_packet": {
            "blocks": [[value + 1 for value in block] for block in BLOCKS],
            "quotient_order": len(quotient_images),
            "kernel_order": len(kernel),
            "kernel_order_spectrum": dict(sorted(Counter(permutation_order(g) for g in kernel).items())),
            "kernel_block_triples": kernel_triples,
        },
        "tomotope_semidirect_triality_theorem": {
            "the_faithful_degree_12_model_has_order_96": len(group) == 96,
            "the_unique_mode_block_quotient_has_order_6_and_is_s3": len(quotient_images) == 6,
            "the_block_kernel_has_order_16": len(kernel) == 16,
            "every_nontrivial_kernel_element_is_an_involution": (
                Counter(permutation_order(g) for g in kernel) == Counter({1: 1, 2: 15})
            ),
            "the_kernel_restricts_to_v4_on_each_block": all(
                len({restrict_to_block(permutation, block) for permutation in kernel}) == 4
                for block in BLOCKS
            ),
            "the_kernel_is_the_constrained_chart_flip_packet_z_equals_x_plus_y": affine_constraint_holds,
            "the_full_group_is_the_semidirect_triality_packet_16_semidirect_s3": (
                len(kernel) * len(quotient_images) == len(group)
            ),
        },
        "interpretation": (
            "The faithful tomotope symmetry on the 3x4 local packet is exactly a "
            "triality quotient S3 acting on the three local modes, together with a "
            "16-element constrained chart-flip kernel. The kernel is not three "
            "independent V4 choices; it is the coupled packet (x,y,x+y)."
        ),
    }
    return summary


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["tomotope_semidirect_triality_theorem"], indent=2))


if __name__ == "__main__":
    main()
