#!/usr/bin/env python3
"""BT768 — partial root-torsor/Q43 transport consistency tester.

BT764 is intentionally fail-closed for the full 51,840-row transport table.
BT768 is the companion partial checker: it lets local chunks be tested without
pretending the global Pluecker/duo transport is complete.

Accepted partial rows may be unresolved on the Q(4,3) side, but any resolved
claim is checked immediately:
  * row IDs unique
  * r^6 partner references are well-formed
  * if both partners appear, the partner map is an involution
  * r^6 keeps root triple, chirality, branch, and phase, and flips duo
  * if Q(4,3) frames are resolved on both partners, they must be mirror frames
  * claim flags cannot assert evidence missing from the row

This checker never promotes the Pluecker-duo claim.  It only reports whether a
partial table is internally consistent.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IN = ROOT / "data" / "bt760_root_torsor_to_q43_transport.partial.json"
DEFAULT_OUT = ROOT / "data" / "bt768_partial_transport_consistency_summary.json"

REQUIRED = {"row_id", "root_triple_id", "chirality", "inner_coordinate", "phase", "duo", "r6_partner_row_id"}


def load_rows(path: Path) -> list[dict[str, Any]]:
    obj = json.loads(path.read_text())
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict) and "rows" in obj:
        return obj["rows"]
    raise SystemExit(f"{path} must contain a row list or an object with rows")


def frame(row: dict[str, Any], key: str):
    if key in row:
        return row.get(key)
    q = row.get("q43_target") or {}
    return q.get(key)


def claims(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("claims") or row.get("transport_claims") or {}


def mirror_of(f):
    if f is None:
        return None
    return list(reversed(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=DEFAULT_IN)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    if not args.input.exists():
        summary = {
            "theorem": "BT768 partial transport consistency tester",
            "input": str(args.input.relative_to(ROOT)),
            "status": "pending_missing_input",
            "all_tests_pass": False,
            "accepted_plucker_duo_claim": False,
            "boundary": "No partial table exists yet; this is not evidence for Pluecker-duo transport."
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 2

    rows = load_rows(args.input)
    errors: list[str] = []
    warnings: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}

    for i, r in enumerate(rows):
        missing = sorted(REQUIRED - set(r))
        if missing:
            errors.append(f"row {i} missing required fields {missing}")
            continue
        rid = r["row_id"]
        if rid in by_id:
            errors.append(f"duplicate row_id {rid}")
        by_id[rid] = r
        if r["duo"] not in (0, 1):
            errors.append(f"{rid}: duo must be 0 or 1")
        if not (0 <= int(r["phase"]) < 6):
            errors.append(f"{rid}: phase must be in 0..5")

    checked_pairs = 0
    unresolved_partners = 0
    resolved_q43_pairs = 0
    for rid, r in by_id.items():
        pid = r["r6_partner_row_id"]
        p = by_id.get(pid)
        if p is None:
            unresolved_partners += 1
            continue
        checked_pairs += 1
        if p.get("r6_partner_row_id") != rid:
            errors.append(f"{rid}: partner map not involutive")
        for key in ("root_triple_id", "chirality", "phase"):
            if r.get(key) != p.get(key):
                errors.append(f"{rid}: partner changes {key}")
        if "branch" in r and "branch" in p and r["branch"] != p["branch"]:
            errors.append(f"{rid}: partner changes branch")
        if r.get("duo") == p.get("duo"):
            errors.append(f"{rid}: partner does not flip duo")

        ar = frame(r, "q43_apartment_id")
        apid = frame(p, "q43_apartment_id")
        of = frame(r, "q43_oriented_frame")
        mf = frame(r, "q43_mirror_frame")
        pof = frame(p, "q43_oriented_frame")
        pmf = frame(p, "q43_mirror_frame")
        if ar is not None and apid is not None and ar != apid:
            errors.append(f"{rid}: partner resolved to different Q43 apartment")
        if of is not None and pof is not None:
            resolved_q43_pairs += 1
            if mirror_of(of) != pof and mf != pof:
                errors.append(f"{rid}: partner frame is not mirror/reversal")
        cr = claims(r)
        if cr.get("same_q43_apartment") and (ar is None or apid is None):
            errors.append(f"{rid}: claims same_q43_apartment without resolved apartments")
        if cr.get("mirror_match") and (of is None or pof is None):
            errors.append(f"{rid}: claims mirror_match without resolved frames")
        if cr.get("fixed_point_free") and pid == rid:
            errors.append(f"{rid}: claims fixed_point_free but partner is self")

    all_tests_pass = not errors
    summary = {
        "theorem": "BT768 partial transport consistency tester",
        "input": str(args.input.relative_to(ROOT)),
        "rows_seen": len(rows),
        "unique_row_ids": len(by_id),
        "checked_partner_directions": checked_pairs,
        "unresolved_partner_references": unresolved_partners,
        "resolved_q43_partner_directions": resolved_q43_pairs,
        "all_tests_pass": all_tests_pass,
        "accepted_plucker_duo_claim": False,
        "errors": errors[:50],
        "warnings": warnings[:50],
        "boundary": "Partial consistency is not global transport evidence. Full promotion still requires BT764 T6a--T6d on the complete table."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if all_tests_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
