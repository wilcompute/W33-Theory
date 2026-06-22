#!/usr/bin/env python3
"""BT1503: release/splice manifest v3 for the transaction/scheduler packet."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1503_paper_release_splice_lock_v3.json"
MD = ROOT / "analysis" / "BT1503_paper_release_splice_lock_v3.md"

PREFERRED_PACKET = [
    "analysis/BT1495_BT1497_transaction_frontier_scheduler.md",
    "analysis/BT1498_BT1500_wcnf_css_unification.md",
    "analysis/BT1495_BT1497_holonet_insert.tex",
    "analysis/BT1498_BT1500_holonet_insert.tex",
    "analysis/BT1500_scheduler_pulse_unification_table.tex",
    "analysis/BT1502_native_d4_pulse_calibration_ledger.tex",
]

REQUIRED_DATA = [
    "data/bt1495_72_tick_transaction_word_compiler.json",
    "data/bt1498_full_fano_quotient_wcnf.json",
    "data/bt1499_transaction_word_css_replay.json",
    "data/bt1500_scheduler_pulse_unification_table.json",
    "data/bt1501_quotient_compatibility_wcnf.json",
    "data/bt1502_native_d4_pulse_calibration_ledger.json",
]

REQUIRED_TOOLS = [
    "tools/bt1495_72_tick_transaction_word_compiler.py",
    "tools/bt1498_full_fano_quotient_wcnf.py",
    "tools/bt1499_transaction_word_css_replay.py",
    "tools/bt1500_scheduler_pulse_unification_table.py",
    "tools/bt1501_quotient_compatibility_wcnf.py",
    "tools/bt1502_native_d4_pulse_calibration_ledger.py",
]

SPLICE_ORDER = [
    {"order": 1, "insert": "analysis/BT1495_BT1497_holonet_insert.tex", "anchor": "after BT1492-BT1494 section", "claim_tier": "exact finite transaction/scheduler"},
    {"order": 2, "insert": "analysis/BT1498_BT1500_holonet_insert.tex", "anchor": "after BT1495-BT1497 section", "claim_tier": "exact finite plus quotient-scaffold boundary"},
    {"order": 3, "insert": "analysis/BT1500_scheduler_pulse_unification_table.tex", "anchor": "inside transaction/scheduler section", "claim_tier": "exact finite count table"},
    {"order": 4, "insert": "analysis/BT1502_native_d4_pulse_calibration_ledger.tex", "anchor": "inside native D4 calibration paragraph", "claim_tier": "finite calibration ledger, not noise model"},
]


def main() -> None:
    existing_packet = [p for p in PREFERRED_PACKET if (ROOT / p).exists()]
    existing_data = [p for p in REQUIRED_DATA if (ROOT / p).exists()]
    existing_tools = [p for p in REQUIRED_TOOLS if (ROOT / p).exists()]
    live_json_verified = []
    for p in existing_data:
        try:
            obj = json.loads((ROOT / p).read_text(encoding="utf-8"))
            live_json_verified.append(obj.get("verified") is True)
        except Exception:
            live_json_verified.append(False)
    checks = {
        "all_preferred_packet_files_exist": len(existing_packet) == len(PREFERRED_PACKET),
        "all_required_data_exist": len(existing_data) == len(REQUIRED_DATA),
        "all_required_tools_exist": len(existing_tools) == len(REQUIRED_TOOLS),
        "all_live_json_verified": all(live_json_verified) and len(live_json_verified) == len(REQUIRED_DATA),
        "splice_order_is_1_to_4": [row["order"] for row in SPLICE_ORDER] == [1, 2, 3, 4],
        "quotient_scaffold_boundary_present": any("quotient-scaffold" in row["claim_tier"] for row in SPLICE_ORDER),
        "calibration_not_noise_model_boundary_present": any("not noise model" in row["claim_tier"] for row in SPLICE_ORDER),
    }
    md = [
        "# BT1503 Paper Release / Splice Lock v3",
        "",
        "Preferred exact finite transaction/scheduler packet before next PDF rebuild:",
        "",
    ]
    for row in SPLICE_ORDER:
        md.append(f"{row['order']}. Insert `{row['insert']}` at `{row['anchor']}`; tier: {row['claim_tier']}.")
    md.extend([
        "",
        "Honesty boundaries:",
        "- BT1501 is a quotient compatibility scaffold, not a solved 330-optimum certificate.",
        "- BT1502 is a finite calibration-priority ledger, not a measured optical-noise model.",
        "- Rebuild the PDF only after these inserts are spliced into `photonic_holonet.tex` in checkout.",
    ])
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    result = {
        "bt": 1503,
        "title": "Paper release splice lock v3",
        "verified": all(checks.values()),
        "preferred_packet": PREFERRED_PACKET,
        "required_data": REQUIRED_DATA,
        "required_tools": REQUIRED_TOOLS,
        "splice_order": SPLICE_ORDER,
        "markdown": "analysis/BT1503_paper_release_splice_lock_v3.md",
        "interpretation": "BT1495-BT1502 are promoted to the preferred exact finite transaction/scheduler packet for the next Holonet release splice, with quotient and calibration honesty boundaries explicit.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1503, "verified": result["verified"], "splices": len(SPLICE_ORDER)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
