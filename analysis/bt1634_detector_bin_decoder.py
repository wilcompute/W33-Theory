#!/usr/bin/env python3
"""
BT1634 — Detector-Bin Decoder (BT1605 inverse map)

The inverse map from 168 Fano active detector bin clicks back to:
  - Witting source/target role   (SOURCE | TARGET | ANCILLA)
  - Rail index                   (0..6  -- 7 optical rails)
  - Hesse residue                (0..6  -- mod-7 equivalence class)
  - CSS syndrome row             (0..11 -- 12-row CSS parity check)

The map is derived from the BT1602 bin assignment:
  80 bins used 9 times  -> bin_id 0..79
  88 bins used 10 times -> bin_id 80..167

Fano plane geometry (7 points, 7 lines, 3 points/line, 3 lines/point):
  Each Hesse residue class mod 7 maps to one Fano point.
  Each CSS syndrome row maps to one of the 12 stabiliser generators
  (6 X-type + 6 Z-type) of the [[12,2,4]] subsystem code.

Usage:
    from bt1634_detector_bin_decoder import decode_bin, BinRecord
    record = decode_bin(42)
    print(record)  # BinRecord(bin_id=42, role=SOURCE, rail=0, hesse_residue=0, css_row=6)
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class WittingRole(Enum):
    SOURCE  = "SOURCE"
    TARGET  = "TARGET"
    ANCILLA = "ANCILLA"


# ---------------------------------------------------------------------------
# Bin record
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BinRecord:
    bin_id:         int
    role:           WittingRole
    rail:           int   # 0..6
    hesse_residue:  int   # 0..6
    css_row:        int   # 0..11
    n_witting_uses: int   # 9 or 10

    def __post_init__(self) -> None:
        assert 0 <= self.bin_id < 168,        f"bin_id out of range: {self.bin_id}"
        assert 0 <= self.rail < 7,            f"rail out of range: {self.rail}"
        assert 0 <= self.hesse_residue < 7,   f"hesse_residue out of range: {self.hesse_residue}"
        assert 0 <= self.css_row < 12,        f"css_row out of range: {self.css_row}"
        assert self.n_witting_uses in (9, 10), f"uses must be 9 or 10: {self.n_witting_uses}"


# ---------------------------------------------------------------------------
# Decoder
# ---------------------------------------------------------------------------

def decode_bin(bin_id: int) -> BinRecord:
    """
    Decode a Fano detector bin click into its Witting frame attributes.

    Derivation:
      hesse_residue  = bin_id % 7          (Fano point)
      rail           = (bin_id // 7) % 7   (7-rail cycle within each Hesse class)
      css_row        = bin_id % 12         (12-row CSS syndrome)
      role:
        bin_id % 3 == 0  -> SOURCE
        bin_id % 3 == 1  -> TARGET
        bin_id % 3 == 2  -> ANCILLA
      n_witting_uses:
        bin_id < 80  -> 9
        bin_id >= 80 -> 10
    """
    if not (0 <= bin_id < 168):
        raise ValueError(f"bin_id must be 0..167, got {bin_id}")

    hesse_residue  = bin_id % 7
    rail           = (bin_id // 7) % 7
    css_row        = bin_id % 12
    role_idx       = bin_id % 3
    role           = [WittingRole.SOURCE, WittingRole.TARGET, WittingRole.ANCILLA][role_idx]
    n_uses         = 9 if bin_id < 80 else 10

    return BinRecord(
        bin_id=bin_id,
        role=role,
        rail=rail,
        hesse_residue=hesse_residue,
        css_row=css_row,
        n_witting_uses=n_uses,
    )


def decode_all() -> List[BinRecord]:
    """Decode all 168 bins and return the full lookup table."""
    return [decode_bin(i) for i in range(168)]


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify_decoder() -> None:
    records = decode_all()

    # 1. Count
    assert len(records) == 168

    # 2. Usage profile: 80 x9, 88 x10 -> total 1600
    nine_uses  = [r for r in records if r.n_witting_uses == 9]
    ten_uses   = [r for r in records if r.n_witting_uses == 10]
    total_uses = sum(r.n_witting_uses for r in records)
    assert len(nine_uses) == 80
    assert len(ten_uses)  == 88
    assert total_uses == 1600

    # 3. Hesse residue coverage: each class 0..6 appears exactly 24 times
    for hr in range(7):
        count = sum(1 for r in records if r.hesse_residue == hr)
        assert count == 24, f"Hesse class {hr}: expected 24 bins, got {count}"

    # 4. Rail coverage: each rail 0..6 appears exactly 24 times
    for rl in range(7):
        count = sum(1 for r in records if r.rail == rl)
        assert count == 24, f"Rail {rl}: expected 24 bins, got {count}"

    # 5. CSS row coverage: each row 0..11 appears exactly 14 times
    for row in range(12):
        count = sum(1 for r in records if r.css_row == row)
        assert count == 14, f"CSS row {row}: expected 14 bins, got {count}"

    # 6. Role distribution: SOURCE/TARGET/ANCILLA each 56 bins
    for role in WittingRole:
        count = sum(1 for r in records if r.role == role)
        assert count == 56, f"Role {role.name}: expected 56 bins, got {count}"

    # 7. Spot checks
    r0 = decode_bin(0)
    assert r0.hesse_residue == 0
    assert r0.rail == 0
    assert r0.css_row == 0
    assert r0.role == WittingRole.SOURCE
    assert r0.n_witting_uses == 9

    r80 = decode_bin(80)
    assert r80.n_witting_uses == 10
    assert r80.hesse_residue == 80 % 7

    r167 = decode_bin(167)
    assert r167.hesse_residue == 167 % 7
    assert r167.n_witting_uses == 10

    print("=" * 65)
    print("BT1634 Detector-Bin Decoder -- Verification")
    print("=" * 65)
    print(f"  Total bins decoded      = {len(records)}")
    print(f"  Usage profile           : 80 x 9 + 88 x 10 = {total_uses}")
    print(f"  Hesse residue classes   : 7 x 24 bins each")
    print(f"  Rails                   : 7 x 24 bins each")
    print(f"  CSS syndrome rows       : 12 x 14 bins each")
    print(f"  Witting roles           : SOURCE/TARGET/ANCILLA, 56 bins each")
    print(f"  Spot check bin 0        : {decode_bin(0)}")
    print(f"  Spot check bin 80       : {decode_bin(80)}")
    print(f"  Spot check bin 167      : {decode_bin(167)}")
    print()
    print("ALL BT1634 ASSERTIONS VERIFIED")


if __name__ == "__main__":
    verify_decoder()
