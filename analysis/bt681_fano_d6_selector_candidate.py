#!/usr/bin/env python3
"""
BT681 — Flag-level Fano/D6 selector candidate.

This is the candidate algebra needed after BT680.

Input structure from the corrected codec stack:
  * four raw 4K4 complement cells supply a 4-copy label;
  * the three diagonal Fano gauges 011,101,110 supply far/middle/active;
  * the +/- carrier side supplies the two sheets.

Thus each 24-dimensional sector has the representation-level packet form

    24 = 4 copies * 3 Fano gauges * 2 signs = 4 hexagons.

The D6 ~= W(G2) stabilizer acts on the hexagon coordinates by S3 gauge
permutations and the global sign flip.  The four-copy label is not selected by
Bose--Mesner data; it is imported from the raw 4K4 complement-cell boundary.

Boundary: this is a concrete selector-candidate algebra, not yet a numerical
intertwiner from the computed 160-flag E1/E3 eigenspaces.
"""
from __future__ import annotations

from itertools import permutations, product
from collections import defaultdict

GAUGES = ("011", "101", "110")
GAUGE_TO_CHANNEL = {"011": "far", "101": "middle", "110": "active"}
CHANNEL_TO_GAUGE = {v: k for k, v in GAUGE_TO_CHANNEL.items()}
SIGNS = ("+", "-")
COPIES = tuple(range(4))
SECTORS = ("E1_short", "E3_long")


def sector_basis(sector: str):
    return [(sector, c, g, s) for c in COPIES for g in GAUGES for s in SIGNS]


def hexagon_for_copy(sector: str, copy: int):
    return [(sector, copy, g, s) for g in GAUGES for s in SIGNS]


def d6_actions():
    for perm in permutations(GAUGES):
        sigma = dict(zip(GAUGES, perm))
        for flip in (False, True):
            yield sigma, flip


def apply_d6(state, action):
    sector, copy, gauge, sign = state
    sigma, flip = action
    new_sign = sign
    if flip:
        new_sign = "+" if sign == "-" else "-"
    return (sector, copy, sigma[gauge], new_sign)


def main() -> None:
    # Build two 24-dimensional sectors.
    basis_by_sector = {sec: sector_basis(sec) for sec in SECTORS}
    assert all(len(b) == 24 for b in basis_by_sector.values())
    total_basis = [x for sec in SECTORS for x in basis_by_sector[sec]]
    assert len(total_basis) == 48

    # Four hexagons per sector.
    hexagons = {(sec, c): hexagon_for_copy(sec, c) for sec in SECTORS for c in COPIES}
    assert all(len(h) == 6 for h in hexagons.values())
    assert sum(len(h) for h in hexagons.values() if h[0][0] == "E1_short") == 24
    assert sum(len(h) for h in hexagons.values() if h[0][0] == "E3_long") == 24

    # D6 action preserves copies and sectors, acts transitively on the six hexagon vertices.
    actions = list(d6_actions())
    assert len(actions) == 12
    seed = ("E1_short", 0, "011", "+")
    orbit = {apply_d6(seed, a) for a in actions}
    assert orbit == set(hexagons[("E1_short", 0)])

    # Projector ranks in one sector.
    ranks = {}
    for sec in SECTORS:
        ranks[(sec, "sector")] = len(basis_by_sector[sec])
        for c in COPIES:
            ranks[(sec, f"copy_{c}")] = len(hexagons[(sec, c)])
        for g in GAUGES:
            ranks[(sec, f"gauge_{g}")] = sum(1 for x in basis_by_sector[sec] if x[2] == g)
        for s in SIGNS:
            ranks[(sec, f"sign_{s}")] = sum(1 for x in basis_by_sector[sec] if x[3] == s)
    assert all(ranks[(sec, f"copy_{c}")] == 6 for sec in SECTORS for c in COPIES)
    assert all(ranks[(sec, f"gauge_{g}")] == 8 for sec in SECTORS for g in GAUGES)
    assert all(ranks[(sec, f"sign_{s}")] == 12 for sec in SECTORS for s in SIGNS)

    # The selector algebra partitions each sector into 4 canonical hexagon blocks.
    partition_check = {}
    for sec in SECTORS:
        covered = set()
        disjoint = True
        for c in COPIES:
            h = set(hexagons[(sec, c)])
            disjoint = disjoint and covered.isdisjoint(h)
            covered |= h
        partition_check[sec] = (disjoint and covered == set(basis_by_sector[sec]))
    assert all(partition_check.values())

    print("BT681 Fano/D6 selector candidate: PASS")
    print("sector_dimension=24")
    print("sector_split=4 copies x 6 hexagon vertices")
    print("E1_plus_E3=48=4*(6_short+6_long)")
    print("D6_order=12")
    print("copy_projector_rank=6")
    print("gauge_projector_rank=8")
    print("sign_projector_rank=12")
    print("selector_candidate_passes_representation_tests=True")
    print("numeric_eigenspace_intertwiner_extracted=False")
    print("boundary=copy labels imported from raw 4K4 cells; not selected by Bose-Mesner data alone")


if __name__ == "__main__":
    main()
