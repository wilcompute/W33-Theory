#!/usr/bin/env python3
"""Part DCCCXIV: phenomenology claim-ledger audit.

The May 17 GitHub burst added Parts DCCLXXXIV-DCCCXIII as broad
phenomenology claims. This verifier does not adjudicate the physics. It adds
an executable claim-hygiene layer:

* every result JSON in the 784..813 range is present,
* every result JSON has a matching theorem note,
* statuses are classified instead of read as uniformly proven,
* stale master-verification coverage is detected, and
* internal numerical/status mismatches are surfaced.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


OUT_PATH = ROOT / "data" / "dcccxiv_phenomenology_claim_ledger_audit.json"
RANGE_START = 784
RANGE_END = 813


@dataclass(frozen=True)
class AuditSummary:
    range_start: int
    range_end: int
    expected_result_count: int
    result_file_count: int
    markdown_file_count: int
    claimed_proven_count: int
    prediction_count: int
    partial_count: int
    tension_count: int
    mixed_count: int
    audit_flag_count: int
    master_verification_stale_by: int
    all_identities_hold: bool


def _result_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.glob("PART_*_results.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        decimal = payload.get("decimal")
        if isinstance(decimal, int) and RANGE_START <= decimal <= RANGE_END:
            files.append(path)
    return sorted(files, key=lambda p: json.loads(p.read_text(encoding="utf-8"))["decimal"])


def _matching_markdown(part: str) -> list[str]:
    return sorted(path.name for path in ROOT.glob(f"PART_{part}_*.md"))


def _status_class(status: str) -> str:
    upper = status.upper()
    has_proven = any(word in upper for word in ("PROVEN", "VERIFIED", "COMPLETE"))
    has_prediction = "PREDICTION" in upper
    has_partial = "PARTIAL" in upper
    has_tension = "TENSION" in upper
    has_open = "OPEN" in upper

    if has_proven and (has_prediction or has_partial or has_tension or has_open):
        return "mixed"
    if has_tension:
        return "tension"
    if has_partial:
        return "partial"
    if has_prediction:
        return "prediction"
    if has_proven:
        return "claimed_proven"
    if "CONCLUDED" in upper:
        return "concluded"
    return "unclassified"


def _walk_numbers(obj: Any, path: str = "") -> list[tuple[str, float]]:
    rows: list[tuple[str, float]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            subpath = f"{path}.{key}" if path else key
            rows.extend(_walk_numbers(value, subpath))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            rows.extend(_walk_numbers(value, f"{path}[{i}]"))
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        rows.append((path, float(obj)))
    return rows


def _sigma_values(payload: dict[str, Any]) -> list[tuple[str, float]]:
    return [
        (path, value)
        for path, value in _walk_numbers(payload)
        if "sigma" in path.lower()
    ]


def _claimed_sigma_limits(text: str) -> list[float]:
    normalized = text.replace("-", " ")
    return sorted({
        float(match.group(1))
        for match in re.finditer(r"within\s+([0-9]+(?:\.[0-9]+)?)\s*sigma", normalized, re.I)
    })


def _master_through_decimal(payload: dict[str, Any]) -> int | None:
    text = str(payload.get("through_part", ""))
    match = re.search(r"\((\d+)\)", text)
    if match:
        return int(match.group(1))
    return None


def build_audit() -> dict[str, Any]:
    files = _result_files()
    expected_decimals = list(range(RANGE_START, RANGE_END + 1))
    entries: list[dict[str, Any]] = []
    flags: list[dict[str, Any]] = []

    seen_decimals: list[int] = []
    markdown_count = 0
    status_counter: Counter[str] = Counter()

    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        part = str(payload["part"])
        decimal = int(payload["decimal"])
        status = str(payload.get("status", ""))
        theorem = str(payload.get("theorem", ""))
        markdown = _matching_markdown(part)
        markdown_count += int(bool(markdown))
        status_kind = _status_class(status)
        status_counter[status_kind] += 1
        seen_decimals.append(decimal)

        sigma_values = _sigma_values(payload)
        sigma_limits = _claimed_sigma_limits(f"{status} {theorem}")
        max_sigma = max((value for _, value in sigma_values), default=None)

        entry = {
            "part": part,
            "decimal": decimal,
            "title": payload.get("title"),
            "result_file": path.name,
            "markdown_files": markdown,
            "status": status,
            "status_class": status_kind,
            "sigma_values": [{"path": p, "value": v} for p, v in sigma_values],
            "claimed_sigma_limits": sigma_limits,
        }
        entries.append(entry)

        if not markdown:
            flags.append(
                {
                    "kind": "missing_markdown",
                    "part": part,
                    "message": f"{path.name} has no matching PART_{part}_*.md theorem note.",
                }
            )

        for limit in sigma_limits:
            if max_sigma is not None and max_sigma > limit:
                flags.append(
                    {
                        "kind": "sigma_status_mismatch",
                        "part": part,
                        "claimed_limit_sigma": limit,
                        "max_sigma_in_payload": max_sigma,
                        "message": (
                            f"{part} claims within {limit:g} sigma but its result JSON "
                            f"contains a sigma value {max_sigma:g}."
                        ),
                    }
                )

    missing_decimals = sorted(set(expected_decimals) - set(seen_decimals))
    duplicate_decimals = sorted(
        decimal for decimal, count in Counter(seen_decimals).items() if count > 1
    )
    if missing_decimals:
        flags.append(
            {
                "kind": "missing_result_decimals",
                "decimals": missing_decimals,
                "message": "The phenomenology burst is not a contiguous 784..813 ledger.",
            }
        )
    if duplicate_decimals:
        flags.append(
            {
                "kind": "duplicate_result_decimals",
                "decimals": duplicate_decimals,
                "message": "Multiple result JSONs share the same decimal part number.",
            }
        )

    master = next((entry for entry in entries if entry["part"] == "DCCXCVIII"), None)
    master_stale_by = 0
    if master is not None:
        master_payload = json.loads((ROOT / master["result_file"]).read_text(encoding="utf-8"))
        through_decimal = _master_through_decimal(master_payload)
        if through_decimal is not None:
            master_stale_by = RANGE_END - through_decimal
            if master_stale_by > 0:
                flags.append(
                    {
                        "kind": "stale_master_verification",
                        "part": "DCCXCVIII",
                        "through_decimal": through_decimal,
                        "current_max_decimal": RANGE_END,
                        "stale_by": master_stale_by,
                        "message": (
                            "DCCXCVIII master verification is older than the live "
                            "phenomenology burst."
                        ),
                    }
                )

    identities = {
        "result_ledger_has_expected_count": len(files) == len(expected_decimals),
        "result_ledger_is_contiguous_784_to_813": sorted(seen_decimals) == expected_decimals,
        "all_result_decimals_are_unique": not duplicate_decimals,
        "all_results_have_markdown_notes": markdown_count == len(files),
        "top_mass_sigma_mismatch_is_detected": any(
            flag["kind"] == "sigma_status_mismatch" and flag.get("part") == "DCCCII"
            for flag in flags
        ),
        "master_verification_staleness_is_detected": any(
            flag["kind"] == "stale_master_verification" for flag in flags
        ),
        "ledger_contains_mixed_or_non_proven_claims": any(
            entry["status_class"] in {"mixed", "partial", "prediction", "tension"}
            for entry in entries
        ),
    }

    summary = AuditSummary(
        range_start=RANGE_START,
        range_end=RANGE_END,
        expected_result_count=len(expected_decimals),
        result_file_count=len(files),
        markdown_file_count=markdown_count,
        claimed_proven_count=status_counter["claimed_proven"],
        prediction_count=status_counter["prediction"],
        partial_count=status_counter["partial"],
        tension_count=status_counter["tension"],
        mixed_count=status_counter["mixed"],
        audit_flag_count=len(flags),
        master_verification_stale_by=master_stale_by,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "status_counts": dict(status_counter),
        "entries": entries,
        "audit_flags": flags,
        "identities": identities,
        "theorem": (
            "Phenomenology Claim-Ledger Audit. The DCCLXXXIV-DCCCXIII burst is "
            "a contiguous 30-part ledger, but it is not uniformly verified: it "
            "contains predictions, partial theorems, mixed proof/prediction "
            "claims, explicit tensions, stale master-verification coverage, and "
            "at least one internal sigma-status mismatch."
        ),
        "honesty_boundary": (
            "This audit checks claim hygiene and internal result-JSON consistency. "
            "It does not validate the underlying phenomenological derivations, "
            "external experimental inputs, or physical correctness of the model."
        ),
    }


def write_audit(path: Path = OUT_PATH) -> Path:
    payload = build_audit()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_audit()
    payload = build_audit()
    print(f"Wrote {out}")
    print(f"Verified: {payload['summary']['all_identities_hold']}")
    print(f"audit_flags = {payload['summary']['audit_flag_count']}")


if __name__ == "__main__":
    main()
