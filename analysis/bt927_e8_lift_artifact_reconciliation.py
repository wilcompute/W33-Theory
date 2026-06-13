#!/usr/bin/env python3
"""BT927 - reconcile the E8 lift artifacts.

The repo now has several E8 witnesses.  BT927 classifies their roles and states
what is and is not known about their equivalence.
"""
from __future__ import annotations
import json
from pathlib import Path

OUT = Path("data/bt927_e8_lift_artifact_reconciliation.json")

ARTIFACTS = [
    {
        "name": "BT924_SNF_shadow",
        "kind": "integral invariant-factor location",
        "object": "SNF_Z(A)=diag(1^16,2^8,8^15,24)",
        "rank_8_role": "the eight d_i=2 valuation-1 factors locate the E8 shadow in coker(A)",
        "metric_status": "rank/location only; no positive-definite Gram chosen",
    },
    {
        "name": "BT925_mod2_form",
        "kind": "canonical mod-2 bilinear form",
        "object": "H=ker(A2)/im(A2) with B=(x^T A y)/2 mod 2",
        "rank_8_role": "nondegenerate alternating F2 form of rank 8 = E8/2E8 bilinear form",
        "metric_status": "2-adic consistency only; no definiteness information",
    },
    {
        "name": "BT926_vertex_E8",
        "kind": "positive-definite vertex Cartan witness",
        "object": "G=2I-A_sub for subset [0,1,4,22,27,35,23,34]",
        "rank_8_role": "explicit positive-definite even unimodular rank-8 Cartan form",
        "metric_status": "definite E8 certified, but not canonically linked to chain H",
    },
    {
        "name": "MCCCLXXXVIII_tetracode_E8",
        "kind": "tetracode/A2 glue root-system witness",
        "object": "four A2 planes + W33-derived ternary tetracode glue -> 240 roots",
        "rank_8_role": "full rank-8 E8 root system with reflection closure",
        "metric_status": "metric root coordinates certified; bridge to chain H not yet canonical",
    },
    {
        "name": "MCCCLXXXIX_E8_E6_A2_decomposition",
        "kind": "coordinate branching witness",
        "object": "E8 -> E6 x A2, 240 = 72 + 6 + 81 + 81",
        "rank_8_role": "connects E8 coordinates to W33/Steinberg matter-sector split",
        "metric_status": "branching coordinates useful for map search, not proof of chain lift alone",
    },
]


def main() -> None:
    result = {
        "theorem": "BT927 E8 lift artifact reconciliation",
        "artifact_count": len(ARTIFACTS),
        "artifacts": ARTIFACTS,
        "equivalence_status": "not yet proved: all witnesses are E8-consistent, but no canonical isometry from the BT924/BT925 chain shadow to the BT926 vertex or tetracode metric witnesses has been constructed.",
        "reconciliation": {
            "same_rank": True,
            "same_mod2_bilinear_type": True,
            "positive_definite_witness_exists": True,
            "canonical_chain_to_metric_map_exists": False,
            "next_map_target": "construct an explicit symplectic basis of H and lift it into either the BT926 vertex Gram or MCCCLXXXVIII tetracode coordinates, then certify integral even-unimodular positivity."
        },
        "exact_conclusion": "The current repo has three compatible E8 layers: chain shadow (BT924/925), vertex definite form (BT926), and tetracode root system (MCCCLXXXVIII/MCCCLXXXIX). They should be treated as distinct witnesses until an explicit integral isometry links them.",
        "checks": {
            "T1_chain_shadow_catalogued": True,
            "T2_mod2_form_catalogued": True,
            "T3_vertex_E8_catalogued": True,
            "T4_tetracode_E8_catalogued": True,
            "T5_equivalence_not_overclaimed": True
        }
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT927 wrote", OUT)


if __name__ == "__main__":
    main()
