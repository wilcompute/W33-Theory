#!/usr/bin/env python3
"""BT782 — compatibility of BT779 metadata with the first partial chunk.

The existing partial artifact contains one 48-row block:
root_triple_id = 0, chirality = 0, inner_coordinate = 0..47.

BT779 provides a deterministic 540*2*48 metadata shape.  This verifier checks
that the old 48-row partial block embeds exactly as:

    id540 = 0, bit2 = 0, id48 = inner_coordinate.

The Q(4,3) target fields remain unresolved, so this is a source/local metadata
compatibility check only.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import bt771_first_partial_transport_chunk as partial

ROOT = Path(__file__).resolve().parents[1]
PARTIAL = ROOT / "data" / "bt760_root_torsor_to_q43_transport.partial.json"
OUT = ROOT / "data" / "PART_BT782_PARTIAL_TRANSPORT_METADATA_COMPATIBILITY_summary.json"


def partner_inner(inner: int) -> int:
    branch, residue = divmod(inner, 12)
    duo, phase = divmod(residue, 6)
    return branch * 12 + (1 - duo) * 6 + phase


def main():
    # Materialize the partial file if needed and refresh its consistency summary.
    partial.main()
    payload = json.loads(PARTIAL.read_text())
    rows = payload.get("rows", [])
    by_id = {r["row_id"]: r for r in rows}

    embedded = []
    errors = []
    for r in rows:
        inner = r["inner_coordinate"]
        candidate = {
            "id540": r["root_triple_id"],
            "bit2": r["chirality"],
            "id48": inner,
        }
        embedded.append((candidate["id540"], candidate["bit2"], candidate["id48"]))
        if candidate["id540"] != 0 or candidate["bit2"] != 0 or not (0 <= candidate["id48"] < 48):
            errors.append(f"bad metadata candidate for {r['row_id']}")
        pid = r["r6_partner_row_id"]
        partner = by_id.get(pid)
        if partner is None:
            errors.append(f"missing partner {pid}")
        elif partner["inner_coordinate"] != partner_inner(inner):
            errors.append(f"partner mismatch at {r['row_id']}")
        if r.get("q43_target", {}).get("status") != "unresolved":
            errors.append(f"unexpected resolved target at {r['row_id']}")

    checks = {
        "partial_rows_48": len(rows) == 48,
        "unique_row_ids_48": len(by_id) == 48,
        "embeds_as_id540_0_bit2_0_all_48_id48": set(embedded) == {(0, 0, i) for i in range(48)},
        "partner_rule_matches_inner_coordinate_involution": not errors,
        "q43_targets_remain_unresolved": all(r.get("q43_target", {}).get("status") == "unresolved" for r in rows),
        "accepted_full_transport_claim_false": payload.get("status") == "first_source_local_partial_chunk_unresolved_target",
    }

    result = {
        "theorem": "BT782 Partial Transport / BT779 Metadata Compatibility",
        "partial_file": str(PARTIAL.relative_to(ROOT)),
        "embedding_rule": "root_triple_id -> id540, chirality -> bit2, inner_coordinate -> id48",
        "summary": {
            "rows": len(rows),
            "root_ids": sorted(Counter(r["root_triple_id"] for r in rows).items()),
            "chirality_ids": sorted(Counter(r["chirality"] for r in rows).items()),
            "inner_coordinates": [min(r["inner_coordinate"] for r in rows), max(r["inner_coordinate"] for r in rows)],
            "unresolved_q43_targets": sum(r.get("q43_target", {}).get("status") == "unresolved" for r in rows),
        },
        "checks": checks,
        "errors": errors[:20],
        "all_checks_pass": all(checks.values()),
        "boundary": "This embeds the first 48-row partial block into the BT779 540*2*48 metadata shape. It does not resolve Q(4,3) target apartments or promote the full table."
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
