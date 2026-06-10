#!/usr/bin/env python3
"""
BT678 — Fano gauge to D6 stabilizer weld.

This welds the three diagonal Fano/tomotope gauges

    011, 101, 110

from BT666 to the three metric pairs in the secondary K3,3 frame quotient:

    far, middle, active.

The metric-matching stabilizer is S3 on the three channels, times one global
side flip.  Thus it has order 6*2=12 and is D6 ~= W(G2).

Boundary: this is the secondary carrier-label/frame quotient.  It is not a
raw 160-flag Levi action and it is not a real folded-Hashimoto reflection.
"""
from __future__ import annotations

from itertools import permutations, product


CHANNEL_TO_GAUGE = {
    "far": "011",
    "middle": "101",
    "active": "110",
}
GAUGE_TO_CHANNEL = {v: k for k, v in CHANNEL_TO_GAUGE.items()}
CHANNELS = tuple(CHANNEL_TO_GAUGE)


def xor_bits(a: str, b: str) -> str:
    return "".join("1" if x != y else "0" for x, y in zip(a, b))


def build_k33():
    vertices = [(side, ch) for side in ("+", "-") for ch in CHANNELS]
    edges = {frozenset((("+", a), ("-", b))) for a in CHANNELS for b in CHANNELS}
    matching = {frozenset((("+", ch), ("-", ch))) for ch in CHANNELS}
    return vertices, edges, matching


def transform_vertex(v, sigma, flip_side: bool):
    side, ch = v
    if flip_side:
        side = "+" if side == "-" else "-"
    return (side, sigma[ch])


def image_edges(edges, sigma, flip_side):
    return {
        frozenset(transform_vertex(v, sigma, flip_side) for v in e)
        for e in edges
    }


def all_channel_permutations():
    for perm in permutations(CHANNELS):
        yield dict(zip(CHANNELS, perm))


def main() -> None:
    # The three gauges are the nonzero elements of the even Fano plane line/subspace.
    gauges = set(CHANNEL_TO_GAUGE.values())
    assert gauges == {"011", "101", "110"}
    assert xor_bits("011", "101") == "110"
    assert xor_bits("011", "110") == "101"
    assert xor_bits("101", "110") == "011"
    assert xor_bits("011", xor_bits("101", "110")) == "000"

    vertices, edges, matching = build_k33()
    assert len(vertices) == 6
    assert len(edges) == 9
    assert len(matching) == 3

    weld_group = []
    induced_gauge_perms = set()
    side_flips = set()
    for sigma, flip in product(all_channel_permutations(), (False, True)):
        assert image_edges(edges, sigma, flip) == edges
        assert image_edges(matching, sigma, flip) == matching
        gauge_perm = tuple(CHANNEL_TO_GAUGE[sigma[GAUGE_TO_CHANNEL[g]]] for g in sorted(gauges))
        induced_gauge_perms.add(gauge_perm)
        side_flips.add(flip)
        weld_group.append((sigma, flip))

    assert len(weld_group) == 12
    assert len(induced_gauge_perms) == 6
    assert side_flips == {False, True}

    print("BT678 Fano gauge / D6 stabilizer weld: PASS")
    print("diagonal_gauges=011,101,110")
    print("channels=far,middle,active")
    print("metric_matching_pairs=far+/far-, middle+/middle-, active+/active-")
    print("S3_gauge_permutations=6")
    print("global_side_flip=2")
    print("stabilizer_order=12 ~= D6 ~= W(G2)")
    print("boundary=secondary carrier-label quotient only")


if __name__ == "__main__":
    main()
