#!/usr/bin/env python3
"""
BT771 — First partial root-torsor/Q(4,3) transport chunk.

This materializes the first real partial transport candidate for the BT763/BT764
pipeline: one root triple, one chirality, all 48 inner-centralizer coordinates.
It verifies the source-side BT766 r^6 involution and deliberately leaves the
Q(4,3) target apartment/frame fields unresolved.

Boundary: this is not a Pluecker-duo transport proof.  It is a partial chunk
that BT768 can test for source-local consistency while BT764 remains blocked by
missing complete Q(4,3) transport data.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT_PARTIAL = Path("data/bt760_root_torsor_to_q43_transport.partial.json")
OUT_SUMMARY = Path("data/bt768_partial_transport_consistency_summary.json")


def partner_inner(inner: int) -> int:
    branch, residue = divmod(inner, 12)
    duo, phase = divmod(residue, 6)
    return branch * 12 + (1 - duo) * 6 + phase


def make_row(inner: int) -> dict:
    branch, residue = divmod(inner, 12)
    duo, phase = divmod(residue, 6)
    partner = partner_inner(inner)
    return {
        "row_id": f"tau_000_0_{inner:02d}",
        "root_triple_id": 0,
        "chirality": 0,
        "inner_coordinate": inner,
        "phase": phase,
        "duo": duo,
        "branch": branch,
        "r6_partner_row_id": f"tau_000_0_{partner:02d}",
        "q43_target": {
            "status": "unresolved",
            "q43_apartment_id": None,
            "q43_oriented_frame": None,
            "q43_mirror_frame": None,
        },
        "claims": {
            "same_q43_apartment": False,
            "order_two": True,
            "mirror_match": False,
            "fixed_point_free": True,
            "plucker_duo_transport": False,
        },
    }


def validate(rows: list[dict]) -> dict:
    by_id = {r["row_id"]: r for r in rows}
    errors: list[str] = []
    checked = 0
    for row in rows:
        partner_id = row["r6_partner_row_id"]
        partner = by_id.get(partner_id)
        if partner is None:
            errors.append(f"missing partner for {row['row_id']}: {partner_id}")
            continue
        checked += 1
        if partner.get("r6_partner_row_id") != row["row_id"]:
            errors.append(f"partner involution fails at {row['row_id']}")
        for key in ("root_triple_id", "chirality", "phase", "branch"):
            if partner[key] != row[key]:
                errors.append(f"partner does not preserve {key} at {row['row_id']}")
        if partner["duo"] == row["duo"]:
            errors.append(f"partner does not flip duo at {row['row_id']}")
    return {
        "theorem": "BT771 first partial transport chunk",
        "status": "partial_source_consistency_pass_target_unresolved" if not errors else "failed",
        "partial_input": str(OUT_PARTIAL),
        "rows_seen": len(rows),
        "unique_row_ids": len(by_id),
        "checked_partner_directions": checked,
        "unresolved_partner_references": max(0, len(rows) - checked),
        "resolved_q43_partner_directions": 0,
        "all_tests_pass_for_partial_contract": not errors,
        "accepted_plucker_duo_claim": False,
        "errors": errors,
        "boundary": (
            "BT771 is not a BT763/BT764 transport proof: all Q(4,3) "
            "apartment/frame targets remain unresolved.  It confirms only the "
            "first root-triple/chirality block obeys the BT766 r6 source "
            "involution and the BT768 partial-contract shape."
        ),
    }


def main() -> None:
    rows = [make_row(i) for i in range(48)]
    payload = {
        "bt771_partial_version": "1.0",
        "status": "first_source_local_partial_chunk_unresolved_target",
        "boundary": (
            "This 48-row chunk covers tau_000, chirality 0 only. It verifies "
            "source-side r6 duo-pair consistency but leaves Q(4,3) target "
            "frames unresolved, so BT764 full transport promotion remains blocked."
        ),
        "rows": rows,
    }
    summary = validate(rows)
    OUT_PARTIAL.parent.mkdir(parents=True, exist_ok=True)
    OUT_PARTIAL.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
