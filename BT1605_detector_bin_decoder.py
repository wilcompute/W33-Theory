#!/usr/bin/env python3
"""
BT1605 — Detector-Bin Decoder
================================
Builds the inverse map from Fano bin clicks back to:
  - Witting source/target role
  - Rail (H / V / orbital)
  - Hesse residue (Z/3Z)
  - CSS syndrome row

Context in the BT stack:
  BT1602 welded 168 Fano bins to the Witting transaction body.
       80 bins used 9×, 88 bins used 10× → 1600 total frames.
  BT1603 closed the finite universal-computation ABI with Clifford
       transport + contextual fuel + Hesse/T non-Clifford port + CSS.
  BT1605 (this file) is the DECODER: given a raw click pattern on the
       168 bins, recover the original Witting frame identity.

Fano plane geometry (PG(2,2)):
  7 points, 7 lines, each line through 3 points, each point on 3 lines.
  We extend to 168 bins = 24 orbits × 7 bins/orbit.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Fano plane incidence — canonical 7-point, 7-line table
# ---------------------------------------------------------------------------
#
# Points: 0..6 (projective coordinates over GF(2))
# Lines:  each row is a 3-element subset of points
FANO_LINES: List[Tuple[int, int, int]] = [
    (0, 1, 3),
    (1, 2, 4),
    (2, 3, 5),
    (3, 4, 6),
    (4, 5, 0),
    (5, 6, 1),
    (6, 0, 2),
]

# Point → list of lines through that point
FANO_POINT_LINES: Dict[int, List[int]] = {p: [] for p in range(7)}
for line_idx, (a, b, c) in enumerate(FANO_LINES):
    for pt in (a, b, c):
        FANO_POINT_LINES[pt].append(line_idx)

# ---------------------------------------------------------------------------
# Witting frame roles
# ---------------------------------------------------------------------------
#
# The 1600 Witting frames decompose as 7 roles × 24 orbits × (9 or 10 uses).
# Roles follow the Witting polytope vertex classification.

WITTING_ROLES: List[str] = [
    "source",        # frame initiates the photon injection
    "target",        # frame receives the photon
    "relay_H",       # horizontal-rail relay
    "relay_V",       # vertical-rail relay
    "ancilla_css",   # CSS syndrome ancilla
    "ancilla_hesse", # Hesse residue ancilla
    "dark_ref",      # dark-count reference (BT1601 placeholder)
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class BinDecoding:
    """Full decoded identity of a single Fano bin click."""
    bin_id: int              # Raw Fano bin index 0..167
    orbit: int               # Orbit index 0..23
    fano_point: int          # Fano point 0..6 within orbit
    witting_role: str        # One of WITTING_ROLES
    rail: str                # 'H', 'V', or 'ancilla'
    hesse_residue: int       # Element of Z/3Z ∈ {0, 1, 2}
    css_syndrome_row: int    # Row index in CSS parity-check matrix
    fano_lines: List[int]    # Line indices through this Fano point

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ClickPattern:
    """A set of bin IDs that fired in one measurement shot."""
    bins: List[int]
    run_id: str = "shot_0"


@dataclass
class DecodedFrame:
    """Result of decoding a ClickPattern."""
    run_id: str
    click_count: int
    decodings: List[BinDecoding]
    dominant_role: Optional[str]    # most common role in this shot
    hesse_vote: int                 # majority Hesse residue mod 3
    css_syndrome_bits: List[int]    # one bit per CSS row (parity of clicks)
    valid: bool                     # True if click count is consistent


# ---------------------------------------------------------------------------
# Decoder core
# ---------------------------------------------------------------------------

class DetectorBinDecoder:
    """
    Maps each of the 168 Fano bins to its full Witting frame identity,
    then decodes click patterns into frame-level information.
    """

    # Number of Fano orbits that tile the 168 active bins
    N_ORBITS: int = 24
    BINS_PER_ORBIT: int = 7
    N_BINS: int = 168  # = 24 × 7

    # CSS parity-check matrix has one row per Fano line = 7 rows,
    # tiled across 24 orbits → 168 columns total.
    N_CSS_ROWS: int = 7  # one per Fano line

    def __init__(self):
        self._table: Dict[int, BinDecoding] = {}
        self._build_table()

    def _build_table(self) -> None:
        """Construct the 168-entry forward and inverse lookup table."""
        for orbit in range(self.N_ORBITS):
            for fano_pt in range(self.BINS_PER_ORBIT):
                bin_id = orbit * self.BINS_PER_ORBIT + fano_pt

                # Role: rotate through 7 roles per orbit
                role = WITTING_ROLES[fano_pt % len(WITTING_ROLES)]

                # Rail assignment: even fano_pt → H, odd → V, ancilla roles → ancilla
                if "ancilla" in role or "dark" in role:
                    rail = "ancilla"
                elif fano_pt % 2 == 0:
                    rail = "H"
                else:
                    rail = "V"

                # Hesse residue: bin_id mod 3
                hesse_res = bin_id % 3

                # CSS syndrome row: determined by which Fano line(s) pass
                # through this point.  Use primary line (first in list).
                lines_through = FANO_POINT_LINES[fano_pt]
                css_row = lines_through[0] if lines_through else 0

                self._table[bin_id] = BinDecoding(
                    bin_id=bin_id,
                    orbit=orbit,
                    fano_point=fano_pt,
                    witting_role=role,
                    rail=rail,
                    hesse_residue=hesse_res,
                    css_syndrome_row=css_row,
                    fano_lines=list(lines_through),
                )

    def decode_bin(self, bin_id: int) -> BinDecoding:
        if bin_id not in self._table:
            raise KeyError(f"bin_id {bin_id} out of range [0, {self.N_BINS - 1}]")
        return self._table[bin_id]

    def decode_pattern(self, pattern: ClickPattern) -> DecodedFrame:
        """Decode a full click pattern into a DecodedFrame."""
        decodings = [self.decode_bin(b) for b in pattern.bins]

        # Dominant role
        role_counts: Dict[str, int] = {}
        for d in decodings:
            role_counts[d.witting_role] = role_counts.get(d.witting_role, 0) + 1
        dominant = max(role_counts, key=role_counts.get) if role_counts else None

        # Hesse vote: majority mod 3
        residues = [d.hesse_residue for d in decodings]
        vote_counts = [residues.count(r) for r in range(3)]
        hesse_vote = vote_counts.index(max(vote_counts))

        # CSS syndrome bits: parity of clicks per CSS row
        css_bits = [0] * self.N_CSS_ROWS
        for d in decodings:
            css_bits[d.css_syndrome_row] ^= 1

        # Validity: click count should be between 1 and N_BINS
        valid = 1 <= len(pattern.bins) <= self.N_BINS

        return DecodedFrame(
            run_id=pattern.run_id,
            click_count=len(pattern.bins),
            decodings=decodings,
            dominant_role=dominant,
            hesse_vote=hesse_vote,
            css_syndrome_bits=css_bits,
            valid=valid,
        )

    def full_table_json(self, indent: int = 2) -> str:
        """Serialise the complete 168-entry decode table to JSON."""
        return json.dumps(
            {str(k): v.to_dict() for k, v in sorted(self._table.items())},
            indent=indent,
        )

    def inverse_lookup(
        self,
        role: Optional[str] = None,
        rail: Optional[str] = None,
        hesse_residue: Optional[int] = None,
        css_row: Optional[int] = None,
    ) -> List[BinDecoding]:
        """Filter the table by any combination of decoded fields."""
        results = list(self._table.values())
        if role is not None:
            results = [r for r in results if r.witting_role == role]
        if rail is not None:
            results = [r for r in results if r.rail == rail]
        if hesse_residue is not None:
            results = [r for r in results if r.hesse_residue == hesse_residue]
        if css_row is not None:
            results = [r for r in results if r.css_syndrome_row == css_row]
        return results


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("BT1605 — Detector-Bin Decoder")
    print("================================\n")

    decoder = DetectorBinDecoder()

    # Verify all 168 bins decode without error
    assert len(decoder._table) == 168, "Expected 168 entries in decode table"

    # Spot-check bin 0
    b0 = decoder.decode_bin(0)
    print(f"Bin 0: orbit={b0.orbit} fano_pt={b0.fano_point} "
          f"role={b0.witting_role} rail={b0.rail} "
          f"hesse={b0.hesse_residue} css_row={b0.css_syndrome_row}")

    # Inverse lookup: find all H-rail source bins
    h_sources = decoder.inverse_lookup(role="source", rail="H")
    print(f"\nH-rail source bins : {len(h_sources)} (expected 12 = 24 orbits / 2 rails)")

    # Decode a synthetic 3-click pattern
    pattern = ClickPattern(bins=[0, 7, 14], run_id="test_shot")
    frame = decoder.decode_pattern(pattern)
    print(f"\nDecoded frame (bins 0,7,14):")
    print(f"  dominant_role    = {frame.dominant_role}")
    print(f"  hesse_vote       = {frame.hesse_vote}")
    print(f"  css_syndrome     = {frame.css_syndrome_bits}")
    print(f"  valid            = {frame.valid}")

    # Verify Fano-line coverage: each of 7 CSS rows has ≥1 bin
    for row in range(7):
        bins_on_row = decoder.inverse_lookup(css_row=row)
        assert len(bins_on_row) > 0, f"CSS row {row} has no bins"
    print("\nAll 7 CSS syndrome rows covered: OK")
    print("BT1605 decoder: OK")
