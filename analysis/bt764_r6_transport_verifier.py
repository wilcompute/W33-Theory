#!/usr/bin/env python3
"""BT764 — r^6 transport verifier for the BT763 table.

This verifier consumes the transport table required by BT762/BT763:

    data/bt760_root_torsor_to_q43_transport.json

It is deliberately fail-closed.  If the table is absent, malformed, incomplete,
or if any T6a--T6d condition fails, the final Pluecker-duo claim is rejected.

The verifier is intentionally schema-light and dependency-free so it can run in
CI without the jsonschema package.  It checks the structural constraints that
matter for the mathematical claim.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "data" / "bt760_root_torsor_to_q43_transport.json"
OUT = ROOT / "data" / "bt764_r6_transport_verifier_results.json"

EXPECTED_ROWS = 540 * 2 * 48


def canonical_unoriented(frame):
    t = tuple(frame)
    rots = [t[i:] + t[:i] for i in range(len(t))]
    r = tuple(reversed(t))
    rots += [r[i:] + r[:i] for i in range(len(r))]
    return min(rots)


def canonical_oriented(frame):
    t = tuple(frame)
    rots = [t[i:] + t[:i] for i in range(len(t))]
    return min(rots)


def fail(reason, extra=None):
    result = {
        "theorem": "BT764 r6 transport verifier",
        "source": str(TABLE.relative_to(ROOT)),
        "status": reason,
        "accepted_plucker_duo_claim": False,
        "all_tests_pass": False,
        "checks": {},
        "boundary": "Fail-closed: duo bit is not promoted to Pluecker mirror unless the explicit BT763 transport table passes T6a--T6d."
    }
    if extra:
        result.update(extra)
    return result


def main():
    if not TABLE.exists():
        result = fail("missing_transport_table")
    else:
        try:
            payload = json.loads(TABLE.read_text())
        except Exception as exc:
            result = fail("invalid_json", {"error": repr(exc)})
        else:
            rows = payload.get("rows", []) if isinstance(payload, dict) else []
            by_id = {r.get("row_id"): r for r in rows if isinstance(r, dict)}
            partner_defined = True
            same_apartment = True
            mirror_orientation = True
            order_two = True
            fixed = []
            malformed = []
            for r in rows:
                rid = r.get("row_id")
                pid = r.get("r6_partner_row_id")
                partner = by_id.get(pid)
                if not rid or not pid or partner is None:
                    partner_defined = False
                    malformed.append(rid or "<missing-row-id>")
                    continue
                if partner.get("r6_partner_row_id") != rid:
                    order_two = False
                frame = r.get("q43_oriented_frame", [])
                mirror = r.get("q43_mirror_frame", [])
                pframe = partner.get("q43_oriented_frame", [])
                if canonical_unoriented(frame) != canonical_unoriented(pframe):
                    same_apartment = False
                if canonical_oriented(pframe) != canonical_oriented(mirror):
                    mirror_orientation = False
                if canonical_oriented(frame) == canonical_oriented(pframe):
                    fixed.append(rid)
                claims = r.get("claims", {})
                if claims.get("same_apartment") is not True:
                    same_apartment = False
                if claims.get("r6_matches_mirror") is not True:
                    mirror_orientation = False
                if claims.get("mirror_is_order_two") is not True:
                    order_two = False
                if claims.get("no_fixed_oriented_frame") is not True:
                    fixed.append(rid)
            checks = {
                "schema_version_1_0": payload.get("bt763_schema_version") == "1.0",
                "source_stack_BT748_BT750": payload.get("source_stack", {}).get("torsor_source") == "BT748" and payload.get("source_stack", {}).get("duo_source") == "BT750",
                "target_stack_BT758_BT760": payload.get("target_stack", {}).get("q43_source") == "BT758" and payload.get("target_stack", {}).get("mirror_source") == "BT760",
                "row_count_expected_51840": len(rows) == EXPECTED_ROWS,
                "unique_row_ids": len(by_id) == len(rows),
                "T6a_partner_defined_for_every_row": partner_defined,
                "T6b_same_underlying_q43_apartment": same_apartment,
                "T6c_r6_matches_declared_mirror_frame": mirror_orientation,
                "T6d_order_two": order_two,
                "T6d_no_fixed_oriented_frame": len(fixed) == 0,
            }
            all_pass = all(checks.values())
            result = {
                "theorem": "BT764 r6 transport verifier",
                "source": str(TABLE.relative_to(ROOT)),
                "row_count": len(rows),
                "expected_rows": EXPECTED_ROWS,
                "malformed_rows_sample": malformed[:20],
                "fixed_rows_sample": fixed[:20],
                "checks": checks,
                "all_tests_pass": all_pass,
                "accepted_plucker_duo_claim": all_pass,
                "status": "verified_transport" if all_pass else "failed_transport",
                "boundary": "Only all_tests_pass=true promotes duo bit = Pluecker mirror. Otherwise BT760 remains target-side only."
            }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result.get("all_tests_pass") is False and TABLE.exists():
        # In CI this should fail if a candidate table exists but is wrong.
        raise SystemExit(1)


if __name__ == "__main__":
    main()
