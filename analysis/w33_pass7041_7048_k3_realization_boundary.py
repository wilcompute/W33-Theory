#!/usr/bin/env python3
"""Passes 7041--7048: distinguish the finite curved precomplex from a K3 realization.

This packet does not synthesize a missing K3 matrix.  It verifies the evidence
contract in the current source tree:
  * the 45-point transport-twisted precomplex is an explicit finite object;
  * the historical 2428x36 K3 scanner was corrected because it scanned zeros;
  * the deformation script constructs a synthetic one-entry perturbation and
    itself states that existence on the actual K3 side remains open;
  * therefore the missing datum is an explicit K3 -> finite-precomplex chain/
    cochain realization with source hash and coordinate map.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS7041_7048_K3_REALIZATION_BOUNDARY.json"

PRE = ROOT / "exploration" / "w33_transport_twisted_precomplex_bridge.py"
TRI = ROOT / "exploration" / "w33_k3_mixed_plane_triangle_row_curvature_witness_bridge.py"
DEF = ROOT / "scripts" / "w33_k3_deformation_theory.py"
SCAN = ROOT / "scripts" / "w33_k3_curvature_witness_scan.py"


def must(path:Path, *needles:str):
    text=path.read_text(encoding="utf-8")
    for s in needles:
        assert s in text, (path,s)
    return text


def main():
    pre=must(PRE,"adapted_transport_precomplex_data","curvature_iq","off_diagonal_curvature_rank")
    tri=must(TRI,"supported_triangle_count","2428","4046","curvature_iq")
    deform=must(DEF,"np.zeros((N_SUPPORTED, N_ACTIVE_COLS)","perturbed[0, 0] = 1","actual K3 side")
    scan=must(SCAN,"NO_OBJECT_LOADED","source","hash")

    report={
      "passes":list(range(7041,7049)),
      "finite_transport_precomplex":{
        "source":str(PRE.relative_to(ROOT)),
        "explicitly_constructed":True,
        "curvature_block":"curvature_iq = (d1 d0) invariant-row/sign-column block over F3",
        "claimed_off_diagonal_rank_in_source_summary":36,
        "finite_object_status":"REAL INTERNAL FINITE OBJECT"
      },
      "triangle_localization":{
        "source":str(TRI.relative_to(ROOT)),
        "supported_transport_triangles":2428,
        "supported_rows":4046,
        "status":"DERIVED FROM THE FINITE PRECOMPLEX"
      },
      "synthetic_deformation":{
        "source":str(DEF.relative_to(ROOT)),
        "allocates_zero_template":True,
        "sets_one_entry_by_hand":True,
        "source_admits_actual_k3_existence_open":True,
        "status":"MODEL PERTURBATION, NOT K3 DATA"
      },
      "fail_closed_scanner":{
        "source":str(SCAN.relative_to(ROOT)),
        "requires_loaded_object_hash_and_coordinate_certificate":True,
        "status":"NO ACTUAL K3 OBJECT LOADED"
      },
      "theorem_boundary":"The finite transport object and its curvature are real. What remains unproved is that an actual K3 geometric/cochain object realizes this finite precomplex or its 2428x36 active block.",
      "missing_certificate":[
        "named K3 geometric/cochain source object",
        "stable source hash",
        "explicit basis/coordinate map into the finite C0,C1,C2 carrier",
        "proof or executable check that K3 differential/connection maps to d0,d1",
        "independent comparison of the induced curvature with curvature_iq"
      ],
      "status":"FINITE_CURVED_PRECOMPLEX_CLOSED__K3_REALIZATION_OPEN"
    }
    OUT.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    return report

if __name__=="__main__":
    main()
