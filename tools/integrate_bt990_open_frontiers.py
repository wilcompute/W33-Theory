#!/usr/bin/env python3
"""Idempotently update OPEN_FRONTIERS with BT984--BT990 R3 fat-tower status."""
from __future__ import annotations

from pathlib import Path

TARGET = Path("OPEN_FRONTIERS.md")
MARKER = "BT990_R3_FAT_TOWER_STATUS"
BLOCK = f"""
  {MARKER}: BT984--BT990 now make the corrected R3 route executable. BT984/BT985
  verify eigenvalue and heat-trace convergence on an edgewise/fat square tower;
  BT986 verifies the Regge curvature side on a projected edgewise sphere; BT988
  loads the explicit CP2_9/K3_16 facets already present in
  `exploration/w33_explicit_curved_4d_complexes.py`; BT989 retires the old
  barycentric `120/19` and `860/19` constants for R3 and replaces the justified
  top-channel constants by multiplier 16 and mesh scale 2^-r. Remaining = derive
  or load the local 4-simplex edgewise facet template, then recompute the full
  lower-incidence/heat-density constants on CP2_9/K3_16.
"""


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    if MARKER in text:
        print("BT990 OPEN_FRONTIERS status already present")
        return
    anchor = "  NEXT: redo that program on the edgewise (not barycentric) tower."
    if anchor not in text:
        raise SystemExit("Could not find R3 NEXT anchor")
    text = text.replace(anchor, anchor + "\n" + BLOCK.rstrip(), 1)
    TARGET.write_text(text, encoding="utf-8")
    print("Inserted BT990 R3 fat-tower status into OPEN_FRONTIERS.md")


if __name__ == "__main__":
    main()
