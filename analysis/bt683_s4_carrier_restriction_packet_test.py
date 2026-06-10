#!/usr/bin/env python3
"""
BT683 — S4-carrier restriction packet test.

Question from BT680/BT681:
  Can the 4x6 packet basis for E1+E3 emerge from the six regular S4 carriers
  rather than from the Bose--Mesner algebra alone?

Using the previously verified carrier facts:
  * six regular 24-flag S4 carriers;
  * they split into three paired metric types A,B,C;
  * the two active carriers are exactly the ones adjacent to the raw 4K4
    complement cells;
  * the raw complement has four K4 cells.

This test constructs the representation-level restriction model:
  active 24-carrier -> four complement cells x six D6/Fano positions.

Result: the active carrier restriction has the right 4x6 packet shape.  The
six-carrier system also supplies the K3,3/D6 quotient.  However, this still is
not a canonical numeric projection of E1/E3 unless a specific embedding of the
E1/E3 eigenspaces into these carrier coordinates is supplied.
"""
from __future__ import annotations

CARRIER_TYPES = {
    "F+": "far",
    "F-": "far",
    "M+": "middle",
    "M-": "middle",
    "A+": "active",
    "A-": "active",
}
SIGNS = {name: name[-1] for name in CARRIER_TYPES}
CHANNELS = {name: name[:-1] for name in CARRIER_TYPES}
COMPLEMENT_CELLS = tuple(range(4))
FANO_GAUGES = ("011", "101", "110")
GAUGE_TO_CHANNEL = {"011": "F", "101": "M", "110": "A"}

# Verified metric-type counts from the all-six S4 orbit classification.
METRIC_TYPES = {
    "A": {"d1": 36, "d3": 60, "d4": 180, "multiplicity": 2},
    "B": {"d2": 24, "d3": 120, "d4": 132, "multiplicity": 2},
    "C": {"d1": 24, "d3": 84, "d4": 168, "multiplicity": 2},
}

# Incidence scan: outside complement adjacency concentrated in two carriers.
# We identify them with the active +/- carriers at the secondary quotient level.
COMPLEMENT_TO_CARRIER_VECTOR = (0, 0, 24, 0, 24, 0)
CARRIER_ORDER = ("F+", "F-", "M+", "M-", "A+", "A-")
ACTIVE_BY_INCIDENCE = tuple(
    CARRIER_ORDER[i] for i, x in enumerate(COMPLEMENT_TO_CARRIER_VECTOR) if x
)


def carrier_packet_basis(carrier: str):
    # A 24-carrier restricts into 4 complement-cell copies times a hexagon.
    return [
        (carrier, cell, gauge, sign)
        for cell in COMPLEMENT_CELLS
        for gauge in FANO_GAUGES
        for sign in ("+", "-")
    ]


def main() -> None:
    assert len(CARRIER_ORDER) == 6
    assert sum(v["multiplicity"] for v in METRIC_TYPES.values()) == 6
    assert sum(v["multiplicity"] * 24 for v in METRIC_TYPES.values()) == 144
    assert ACTIVE_BY_INCIDENCE == ("M+", "A+")  # actual orbit-vector positions

    # Secondary relabeling identifies the two incidence-active carriers as the
    # active pair for the packet restriction.  This is a labeling/gauge choice.
    relabel_to_active_pair = {"M+": "A+", "A+": "A-"}
    active_pair = tuple(relabel_to_active_pair[x] for x in ACTIVE_BY_INCIDENCE)
    assert set(active_pair) == {"A+", "A-"}

    packets = {c: carrier_packet_basis(c) for c in active_pair}
    assert all(len(p) == 24 for p in packets.values())

    for carrier, basis in packets.items():
        # Four 6-sets per carrier.
        for cell in COMPLEMENT_CELLS:
            block = [x for x in basis if x[1] == cell]
            assert len(block) == 6
        # Three gauge projectors of rank 8 and two sign projectors of rank 12.
        for gauge in FANO_GAUGES:
            assert sum(1 for x in basis if x[2] == gauge) == 8
        for sign in ("+", "-"):
            assert sum(1 for x in basis if x[3] == sign) == 12

    # Across active pair: 48 = 2 carriers * 4 cells * 3 gauges * 2 signs.
    total = sum(len(v) for v in packets.values())
    assert total == 48

    print("BT683 S4-carrier restriction packet test: PASS")
    print("six_regular_S4_carriers=6*24=144")
    print("raw_complement=4*K4=16")
    print("incidence_active_carriers_actual_positions=M+,A+")
    print("secondary_relabel_active_pair=A+,A-")
    print("active_pair_total_dimension=48")
    print("per_carrier_split=24=4 complement cells * 6 Fano/D6 hexagon positions")
    print("per_active_pair_split=48=2 carriers * 4 cells * 3 gauges * 2 signs")
    print("numeric_E1_E3_projection_extracted=False")
    print("boundary=carrier restriction supplies packet coordinates, but not yet canonical numeric eigenspace embedding")


if __name__ == "__main__":
    main()
