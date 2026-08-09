#!/usr/bin/env python3
"""Pass 4529 -- rank-two building obstruction compass.

This pass does not recompute group cohomology.  It takes the exact Pass-4509
restriction barcode and Pass-4519 Borel identification as inputs and chooses a
basis of the two-dimensional radical H^1 in which the two simple parabolic
restriction kernels are coordinate axes.

Over F2 there are three nonzero classes.  Pass 4509 says the point parabolic
kills `fixed_line`, the line parabolic kills `sum`, and their incident Borel
kills all three.  Thus e_P=fixed_line and e_L=sum are independent; the remaining
class `second` is e_P+e_L.  This is the precise rank-two residue/chamber reading
supported by the certificates.

Boundary: this is a conceptual coordinate theorem for the computed
H^1(PSp(4,3),K/J).  It is not a general BN-pair theorem for arbitrary Ext^1
modules or arbitrary groups of Lie type.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4529_RANK2_BUILDING_OBSTRUCTION_COMPASS.json"


def main() -> int:
    c4509 = json.loads((ROOT / "data/PART_W33_PASS4509_COHOMOLOGY_RESTRICTION_BARCODE.json").read_text())
    c4519 = json.loads((ROOT / "data/PART_W33_PASS4519_FLAG_BOREL_SYLOW3_NORMALIZER.json").read_text())
    c4528 = json.loads((ROOT / "data/PART_W33_PASS4528_BOREL_OVERGROUP_SPLITTING.json").read_text())

    assert c4509["H1_dimension"] == 2
    b = c4509["barcode"]
    assert b["point_648"]["killed_nonzero_classes"] == ["fixed_line"]
    assert b["line_648"]["killed_nonzero_classes"] == ["sum"]
    assert set(b["incident_flag_162"]["killed_nonzero_classes"]) == {"fixed_line", "second", "sum"}
    assert c4519["normalizer"]["equals_flag_stabilizer"] is True
    assert c4528["overgroup_orders"] == {"Borel": 162, "G": 25920, "line_parabolic": 648, "point_parabolic": 648}

    # Coordinate labels in F2^2.  The third nonzero vector is forced.
    coords = {
        "fixed_line": [1, 0],
        "sum": [0, 1],
        "second": [1, 1],
    }
    assert len({tuple(v) for v in coords.values()}) == 3

    out = {
        "pass": 4529,
        "cohomology_space": "H^1(PSp(4,3), K/J) ~= F2^2",
        "coordinate_basis": {"e_point": "fixed_line", "e_line": "sum"},
        "class_coordinates": coords,
        "restriction_kernels": {
            "point_parabolic_648": {"dimension": 1, "span": ["e_point"]},
            "line_parabolic_648": {"dimension": 1, "span": ["e_line"]},
            "incident_Borel_162": {"dimension": 2, "span": ["e_point", "e_line"]},
        },
        "overgroup_link": "Pass 4528 proves the Borel is the intersection of the two order-648 parabolics and the unique splitting member of its overgroup interval.",
        "theorem": "The two computed radical obstruction bits can be coordinatized by the two simple parabolic residue directions: point and line parabolics kill distinct axes, while their incident chamber/Borel kills their full F2^2 span.",
        "boundary": "This is an exact re-coordinatization of the computed restriction barcode, not a proof that every rank-two building extension has two obstruction bits or that the full Ext^1_G(H10,K/J) is F2^2."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
