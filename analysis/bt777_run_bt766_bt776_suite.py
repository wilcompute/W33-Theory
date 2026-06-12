#!/usr/bin/env python3
"""BT777 — import-based theorem-suite runner for BT766--BT785.

Runs the octet/projector/bus/metadata verifier modules in dependency order by
importing each module and calling its main() function directly.
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
OUT = ROOT / "data" / "PART_BT777_THEOREM_SUITE_summary.json"

if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

MODULES = [
    "bt766_intrinsic_k44_octet_quotient",
    "bt767_k44_octet_incidence_projector",
    "bt769_center_quad_octet_identification",
    "bt770_octet_nonedge_packet_abi",
    "bt771_null_15_sector_kernel",
    "bt772_pg32_labeled_15_sector",
    "bt773_octet_packet_selector_bus",
    "bt774_three_projector_architecture",
    "bt775_pg32_equivariance_obstruction",
    "bt776_2160_to_51840_fiber_lift_scaffold",
    "bt778_pg32_label_stabilizer",
    "bt779_51840_metadata_lift",
    "bt781_h15_frame_action",
    "bt782_partial_transport_metadata_compatibility",
    "bt785_generated_partial_blocks_compatibility",
]

EXPECTED_OUTPUTS = [
    "data/PART_BT766_INTRINSIC_K44_OCTET_QUOTIENT_results.json",
    "data/PART_BT767_K44_OCTET_INCIDENCE_PROJECTOR_results.json",
    "data/PART_BT769_CENTER_QUAD_OCTET_IDENTIFICATION_results.json",
    "data/PART_BT770_OCTET_NONEDGE_PACKET_ABI_summary.json",
    "data/PART_BT771_NULL_15_SECTOR_KERNEL_summary.json",
    "data/PART_BT772_PG32_LABELED_15_SECTOR_summary.json",
    "data/PART_BT773_OCTET_PACKET_SELECTOR_BUS_summary.json",
    "data/PART_BT774_THREE_PROJECTOR_ARCHITECTURE_summary.json",
    "data/PART_BT775_PG32_EQUIVARIANCE_OBSTRUCTION_summary.json",
    "data/PART_BT776_2160_TO_51840_FIBER_LIFT_SCAFFOLD_summary.json",
    "data/PART_BT778_PG32_LABEL_STABILIZER_summary.json",
    "data/PART_BT779_51840_METADATA_LIFT_summary.json",
    "data/PART_BT781_H15_FRAME_ACTION_summary.json",
    "data/PART_BT782_PARTIAL_TRANSPORT_METADATA_COMPATIBILITY_summary.json",
    "data/PART_BT785_GENERATED_PARTIAL_BLOCKS_COMPATIBILITY_summary.json",
]


def main():
    module_status = {}
    for name in MODULES:
        module = importlib.import_module(name)
        module.main()
        module_status[name] = "ok"

    output_status = {rel: (ROOT / rel).exists() for rel in EXPECTED_OUTPUTS}
    summary = {
        "theorem": "BT777 BT766--BT785 Import-Based Theorem Suite",
        "module_count": len(MODULES),
        "modules": MODULES,
        "module_status": module_status,
        "outputs_present": output_status,
        "all_outputs_present": all(output_status.values()),
        "all_checks_pass": len(module_status) == len(MODULES) and all(output_status.values()),
        "boundary": "This runner checks the local Python theorem stack only. It does not validate external GAP, LaTeX, or unavailable Q43 target artifacts."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if not summary["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
