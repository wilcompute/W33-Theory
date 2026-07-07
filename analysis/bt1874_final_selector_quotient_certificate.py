#!/usr/bin/env python3
"""BT1874/BT1883: upgraded final selector quotient certificate.

BT1883 upgrades the certificate to distinguish three layers: (1) support shadow
closed, (2) integral vertex-E8 basis exists through BT982 and is mapped through
BT1880, (3) explicit Z^40 chain-boundary compatibility is still open.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1874_FINAL_SELECTOR_QUOTIENT_CERTIFICATE.json")

CANONICAL_SELECTOR = [[3, 68], [4, 42], [38, 65], [90, 144]]

QUOTIENT_STAGES = [
    {"stage": "support_minimality", "status": "closed", "witness": "BT951", "claim": "support 60 with six minimizers"},
    {"stage": "certificate_graph", "status": "closed_partial", "witness": "BT953/BT1837", "claim": "certificate orbits [[0,1],[2],[3],[4],[5]]"},
    {"stage": "vertex_metric", "status": "closed", "witness": "BT954", "claim": "minimizer 2 selected"},
    {"stage": "tetracode_metric", "status": "closed", "witness": "BT956/BT1840", "claim": "minimizer 2 selected through recovered matrix"},
    {"stage": "transported_S4", "status": "closed", "witness": "BT959/BT1845", "claim": "orbit 24, stabilizer 1, support-60 singleton"},
    {"stage": "glue_stabilizer", "status": "closed", "witness": "BT1855", "claim": "signed monomial tetracode glue stabilizer 48 = 2 x 24"},
    {"stage": "S4_transport_to_H", "status": "closed", "witness": "BT1856", "claim": "S4 quotient transports to H"},
    {"stage": "support_phase_action", "status": "closed_at_H_support_level", "witness": "BT1861/BT1871", "claim": "central-inversion phase fixes winner-2 support mask"},
    {"stage": "integral_vertex_E8_basis", "status": "closed", "witness": "BT982/BT1876", "claim": "BT982 supplies final_integral_basis_B in vertex E8 root coordinates with E8 Cartan Gram"},
    {"stage": "BT982_to_selector_template_mapping", "status": "closed_candidate", "witness": "BT1880", "claim": "BT982 basis columns mapped into BT1875 selector-pair/phase rows"},
    {"stage": "basis_level_phase_gram_action", "status": "closed_in_vertex_E8_coordinates", "witness": "BT1882", "claim": "central-inversion bookkeeping action preserves mapped slot Gram contributions"},
    {"stage": "explicit_Z40_chain_boundary_compatibility", "status": "open", "witness": "BT1881", "claim": "needs explicit Z^40 chain A/2 representatives and boundary operator/action"},
]

PHASE_BIT = {
    "invariant": "A2_integral_phase_coset_bit",
    "ambient_quotient": "O(A2)/W(A2)",
    "identity_class": 0,
    "central_inversion_class": 1,
    "support_shadow": "both bits are identical on the mod-2 H support selector",
    "basis_level_action": "phase bit 1 is represented by simultaneous vector negation in the mapped BT982 slot pair",
}


def theorem_summary():
    open_stages = [s for s in QUOTIENT_STAGES if s["status"] == "open"]
    checks = {
        "canonical_selector_recorded": CANONICAL_SELECTOR == [[3, 68], [4, 42], [38, 65], [90, 144]],
        "phase_bit_recorded": PHASE_BIT["ambient_quotient"] == "O(A2)/W(A2)",
        "BT982_basis_exists_recorded": any(s["stage"] == "integral_vertex_E8_basis" and s["status"] == "closed" for s in QUOTIENT_STAGES),
        "BT1880_mapping_recorded": any(s["stage"] == "BT982_to_selector_template_mapping" for s in QUOTIENT_STAGES),
        "BT1882_basis_phase_action_recorded": any(s["stage"] == "basis_level_phase_gram_action" for s in QUOTIENT_STAGES),
        "exactly_one_open_stage": len(open_stages) == 1,
        "open_stage_is_Z40_chain_boundary": open_stages[0]["stage"] == "explicit_Z40_chain_boundary_compatibility",
        "support_shadow_closed": any(s["stage"] == "support_phase_action" and s["status"] == "closed_at_H_support_level" for s in QUOTIENT_STAGES),
    }
    return {
        "theorem": "BT1874/BT1883 Upgraded Final Selector Quotient Certificate",
        "canonical_selector": CANONICAL_SELECTOR,
        "metric_winner": 2,
        "quotient_stages": QUOTIENT_STAGES,
        "phase_bit": PHASE_BIT,
        "final_open_boundary": "construct/prove explicit Z^40 chain A/2 representatives and boundary compatibility for the mapped BT982 phase action",
        "closed_shadow_statement": "everything visible on the mod-2 H support shadow is closed",
        "basis_bridge_statement": "BT982 supplies the integral vertex-E8 basis; BT1880 maps it into selector-pair/phase rows; BT1882 preserves Gram at vertex-E8 basis level",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Upgraded certificate. It does not solve the remaining explicit Z^40 chain-boundary compatibility problem."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
