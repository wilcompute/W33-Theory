#!/usr/bin/env python3
"""PART CCCCXV -- Dressed Q4 Packet Logical Verifier.

CCCCXIV builds the integrated Q4/Bacon-Shor packet matrix and records a
line-star replacement target of weight 12: three W33 line-star edges mapped to
three weight-4 packet columns.

This file checks the dressed subsystem question left open there.  In a 4x4
Bacon-Shor packet, the X-center contains even column parities.  Therefore a
three-column attachment is nontrivial, but it is center-equivalent to a
one-column logical representative.  Its dressed packet weight is 4, not 12.

Consequence: the current Q4 packet layer is a correct [[1296,81,4]] subsystem
packet layer and an exact attachment matrix, but it does not by itself prove the
integrated [[1296,81,>=12]] replacement distance.  A later architecture must add
column locks, use separate packets per base edge, or keep the Steane/Phi6 lift as
the distance-81 protection layer.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
Q4_PACKET_PATH = ROOT / "exploration" / "PART_CCCCXIV_INTEGRATED_Q4_PACKET_SUBSYSTEM_MATRIX.py"
Q4_PACKET_RESULTS = ROOT / "PART_CCCCXIV_integrated_q4_packet_subsystem_matrix_results.json"

ROWS = 4
COLS = 4
PACKETS = 81
BASE_LINE_STAR_WEIGHT = 3
PACKET_COLUMN_WEIGHT = 4
RAW_REPLACEMENT_WEIGHT = BASE_LINE_STAR_WEIGHT * PACKET_COLUMN_WEIGHT


def ok(name: str, cond: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(cond), "value": value}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_q4_packet_module():
    spec = importlib.util.spec_from_file_location("integrated_q4_packet_ccccxiv_for_ccccxv", Q4_PACKET_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def bit(cols: Iterable[int]) -> int:
    out = 0
    for col in cols:
        out ^= 1 << col
    return out


def span(generators: List[int]) -> List[int]:
    out: List[int] = []
    for mask in range(1 << len(generators)):
        value = 0
        for idx, generator in enumerate(generators):
            if (mask >> idx) & 1:
                value ^= generator
        out.append(value)
    return sorted(set(out))


def column_center_generators() -> List[int]:
    return [bit([0, 1]), bit([1, 2]), bit([2, 3])]


def min_dressed_column_count(raw_columns: Iterable[int]) -> Dict[str, Any]:
    raw = bit(raw_columns)
    center = span(column_center_generators())
    dressed = sorted((raw ^ row for row in center), key=lambda value: (value.bit_count(), value))
    best = dressed[0]
    return {
        "raw_column_mask": raw,
        "raw_column_count": raw.bit_count(),
        "center_span_size": len(center),
        "center_span": center,
        "best_dressed_mask": best,
        "best_dressed_column_count": best.bit_count(),
        "best_dressed_physical_weight": best.bit_count() * ROWS,
        "is_nontrivial": raw not in center,
    }


def attachment_columns(attachment: Dict[str, Any]) -> List[int]:
    return [edge["packet_column"] for edge in attachment["edge_columns"]]


def build_results() -> Dict[str, Any]:
    q4_results = load_json(Q4_PACKET_RESULTS)
    q4_module = load_q4_packet_module()
    full_q4 = q4_module.build_results()
    attachments = q4_module.attachment_map()
    packet = q4_results["global_packet_subsystem"]
    summary = q4_results["attachment_summary"]

    first_columns = attachment_columns(attachments[0])
    first_dressed = min_dressed_column_count(first_columns)
    all_dressed = [min_dressed_column_count(attachment_columns(attachment)) for attachment in attachments]
    center_span = span(column_center_generators())

    checks: List[Dict[str, Any]] = []
    checks.append(ok("Q4 packet artifact verified", q4_results["verified"] is True, q4_results["checks_passed"]))
    checks.append(ok("full Q4 module still verifies", full_q4["verified"] is True, full_q4["checks_passed"]))
    checks.append(ok("global packet layer is [[1296,81,4]]", (packet["n"], packet["k"], packet["d_packet_layer"]) == (1296, 81, 4), packet))
    checks.append(ok("81 W33 line-star attachments exist", len(attachments) == PACKETS == summary["attachments"], summary))
    checks.append(ok("each raw attachment uses three packet columns", all(len(attachment["edge_columns"]) == BASE_LINE_STAR_WEIGHT for attachment in attachments), attachments[0]))
    checks.append(ok("each raw attachment has replacement weight 12", all(sum(edge["support_weight"] for edge in attachment["edge_columns"]) == RAW_REPLACEMENT_WEIGHT for attachment in attachments), attachments[0]))
    checks.append(ok("column center span has even parity size 8", len(center_span) == 8 and all(mask.bit_count() % 2 == 0 for mask in center_span), center_span))
    checks.append(ok("three-column attachment is nontrivial modulo center", first_dressed["is_nontrivial"] is True, first_dressed))
    checks.append(ok("three-column attachment dresses to one column", first_dressed["best_dressed_column_count"] == 1, first_dressed))
    checks.append(ok("dressed physical weight is 4", first_dressed["best_dressed_physical_weight"] == PACKET_COLUMN_WEIGHT, first_dressed))
    checks.append(ok("all attachments have dressed physical weight 4", all(item["best_dressed_physical_weight"] == PACKET_COLUMN_WEIGHT for item in all_dressed), all_dressed[0]))
    checks.append(ok("raw 12 target is not the dressed subsystem distance", RAW_REPLACEMENT_WEIGHT > first_dressed["best_dressed_physical_weight"], {"raw": RAW_REPLACEMENT_WEIGHT, "dressed": first_dressed["best_dressed_physical_weight"]}))

    verified = all(check["passed"] for check in checks)
    return {
        "part": "CCCCXV",
        "title": "Dressed Q4 Packet Logical Verifier",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(check["passed"] for check in checks),
        "packet_layer": {
            "n": packet["n"],
            "k": packet["k"],
            "d_packet_layer": packet["d_packet_layer"],
            "notation": packet["notation"],
        },
        "attachment_audit": {
            "attachments": len(attachments),
            "raw_replacement_weight": RAW_REPLACEMENT_WEIGHT,
            "raw_columns_per_attachment": BASE_LINE_STAR_WEIGHT,
            "packet_column_weight": PACKET_COLUMN_WEIGHT,
            "sample_columns": first_columns,
            "sample_dressed": first_dressed,
        },
        "dressed_distance_conclusion": {
            "current_subsystem_packet_distance": PACKET_COLUMN_WEIGHT,
            "raw_replacement_target": RAW_REPLACEMENT_WEIGHT,
            "integrated_12_claim_status": "not_proved_by_current_subsystem_dressing",
            "reason": "three packet columns are center-equivalent to one column in the 4x4 Bacon-Shor packet",
        },
        "repair_options": [
            "add column-lock checks that forbid even-column center dressing for replacement attachments",
            "route the three base line-star edges into three independent packets before repetition/majority decoding",
            "keep the Steane/Phi6 concatenated lift as the distance-81 protection layer while Q4 packets serve as local gauge/routing hardware",
        ],
        "architecture_upgrade": (
            "Closes the CCCCXIV honesty boundary for the current Q4/Bacon-Shor "
            "packet attachment: the raw replacement weight is 12, but subsystem "
            "dressing reduces each three-column representative to weight 4."
        ),
        "theorem": (
            "In the current 4x4 Q4/Bacon-Shor packet, X-center rows span the even "
            "column parities. A three-column line-star attachment has odd parity, "
            "so it is a valid nontrivial logical representative, but adding center "
            "rows dresses it to a one-column representative of physical weight 4. "
            "Therefore the integrated packet layer proves [[1296,81,4]], not yet "
            "[[1296,81,>=12]]."
        ),
        "honesty_boundary": (
            "This is an obstruction/verification result for the current subsystem "
            "packet model. It does not rule out a column-locked, multi-packet, or "
            "Steane-concatenated architecture that achieves higher distance."
        ),
        "checks": checks,
    }


def main() -> int:
    results = build_results()
    out = ROOT / "PART_CCCCXV_dressed_q4_packet_logical_verifier_results.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "part": results["part"],
                "verified": results["verified"],
                "checks_passed": results["checks_passed"],
                "checks_total": results["checks_total"],
                "dressed_distance": results["dressed_distance_conclusion"]["current_subsystem_packet_distance"],
                "out_path": str(out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
