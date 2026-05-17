#!/usr/bin/env python3
"""Part DCCCXXXVIII: post-audit reconciliation ledger.

The DCCCXIV phenomenology audit was pushed immediately before a GitHub-side
DCCCXIV graviton correction and DCCCXV master update landed.  This verifier
keeps both facts visible:

* DCCCII still contains the historical top-mass sigma/status mismatch.
* DCCCXI records the sharpened top pole-mass tension.
* The later DCCCXIV graviton correction closes that top-sector tension.
* DCCCXV promotes the corrected top mass into the live master scorecard.
* The duplicated DCCCXIV part surface is detected instead of overwritten.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


OUT_PATH = ROOT / "data" / "dcccxxxviii_post_audit_reconciliation_ledger.json"


@dataclass(frozen=True)
class ReconciliationSummary:
    part: str
    decimal: int
    current_result_max_decimal: int
    valid_result_max_decimal: int
    invalid_result_json_count: int
    dcccxiv_markdown_count: int
    duplicate_part_surface_count: int
    dcccxiv_result_count: int
    historical_top_claim_limit_sigma: float
    historical_top_max_sigma: float
    dcccxi_tension_sigma: float
    corrected_top_sigma: float
    master_promoted_top_sigma: float
    audit_flag_count: int
    all_identities_hold: bool


def _json(path: str | Path) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _walk_numbers(obj: Any, path: str = "") -> list[tuple[str, float]]:
    rows: list[tuple[str, float]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            subpath = f"{path}.{key}" if path else key
            rows.extend(_walk_numbers(value, subpath))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            rows.extend(_walk_numbers(value, f"{path}[{index}]"))
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        rows.append((path, float(obj)))
    return rows


def _sigma_values(payload: dict[str, Any]) -> list[tuple[str, float]]:
    return [
        (path, value)
        for path, value in _walk_numbers(payload)
        if "sigma" in path.lower()
    ]


def _claimed_sigma_limits(*texts: str) -> list[float]:
    combined = " ".join(texts).replace("-", " ")
    return sorted(
        {
            float(match.group(1))
            for match in re.finditer(
                r"within\s+([0-9]+(?:\.[0-9]+)?)\s*sigma",
                combined,
                re.I,
            )
        }
    )


def _result_payloads() -> list[tuple[Path, dict[str, Any]]]:
    payloads: list[tuple[Path, dict[str, Any]]] = []
    for path in ROOT.glob("PART_*_results.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(payload.get("decimal"), int):
            payloads.append((path, payload))
    return sorted(payloads, key=lambda row: int(row[1]["decimal"]))


def _roman_to_int(text: str) -> int:
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    previous = 0
    for char in reversed(text):
        value = values[char]
        if value < previous:
            total -= value
        else:
            total += value
            previous = value
    return total


def _part_decimal_from_name(path: Path) -> int | None:
    match = re.match(r"PART_([MDCLXVI]+)_", path.name)
    if not match:
        return None
    return _roman_to_int(match.group(1))


def _part_surface_max_decimal(excluded_decimals: set[int] | None = None) -> int:
    excluded = excluded_decimals or set()
    decimals = [
        decimal
        for path in ROOT.glob("PART_*")
        if (decimal := _part_decimal_from_name(path)) is not None
        and decimal not in excluded
    ]
    return max(decimals)


def _invalid_result_json_files(min_decimal: int, max_decimal: int) -> list[str]:
    invalid: list[str] = []
    for path in sorted(ROOT.glob("PART_*_results.json")):
        decimal = _part_decimal_from_name(path)
        if decimal is None or decimal < min_decimal or decimal > max_decimal:
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            invalid.append(path.name)
            continue
        if not isinstance(payload, dict) or not isinstance(payload.get("decimal"), int):
            invalid.append(path.name)
    return invalid


def _part_markdowns(part: str) -> list[str]:
    return sorted(path.name for path in ROOT.glob(f"PART_{part}_*.md"))


def _load_prior_audit() -> dict[str, Any]:
    audit_path = ROOT / "data" / "dcccxiv_phenomenology_claim_ledger_audit.json"
    if audit_path.exists():
        return json.loads(audit_path.read_text(encoding="utf-8"))

    from verify_dcccxiv_phenomenology_claim_ledger_audit import build_audit

    return build_audit()


def build_reconciliation() -> dict[str, Any]:
    top_802 = _json("PART_DCCCII_top_quark_mass_results.json")
    top_811 = _json("PART_DCCCXI_top_mass_3loop_results.json")
    correction_814 = _json("PART_DCCCXIV_graviton_top_correction_results.json")
    master_815 = _json("PART_DCCCXV_master_verification_update_results.json")
    prior_audit = _load_prior_audit()

    result_payloads = _result_payloads()
    valid_result_max_decimal = max(int(payload["decimal"]) for _, payload in result_payloads)
    current_max_decimal = _part_surface_max_decimal(excluded_decimals={838})
    invalid_result_json_files = _invalid_result_json_files(
        min_decimal=829,
        max_decimal=current_max_decimal,
    )
    dcccxiv_result_count = sum(
        1
        for _, payload in result_payloads
        if payload.get("part") == "DCCCXIV" or payload.get("decimal") == 814
    )
    dcccxiv_markdowns = _part_markdowns("DCCCXIV")

    historical_limits = _claimed_sigma_limits(
        str(top_802.get("status", "")),
        str(top_802.get("theorem", "")),
    )
    historical_top_claim_limit = min(historical_limits)
    historical_top_max_sigma = max(value for _, value in _sigma_values(top_802))
    dcccxi_tension_sigma = float(top_811["comparison"]["residual_sigma"])
    corrected_top_sigma = float(correction_814["result"]["residual_sigma"])
    master_promoted_top_sigma = float(
        master_815["promoted_result"]["residual_sigma"]
    )

    prior_flags = prior_audit.get("audit_flags", [])

    audit_flags = [
        {
            "kind": "duplicate_dcccxiv_part_surface",
            "part": "DCCCXIV",
            "markdown_files": dcccxiv_markdowns,
            "message": (
                "Two theorem notes now occupy the DCCCXIV surface. The older "
                "claim-ledger audit and the newer graviton top correction should "
                "both remain visible until the numbering ledger is cleaned up."
            ),
        },
        {
            "kind": "superseded_top_tension",
            "from_part": "DCCCII/DCCCXI",
            "to_part": "DCCCXIV/DCCCXV",
            "historical_max_sigma": historical_top_max_sigma,
            "dcccxi_tension_sigma": dcccxi_tension_sigma,
            "corrected_sigma": corrected_top_sigma,
            "message": (
                "The DCCCII sigma/status mismatch remains historically true, "
                "but the live top-sector status is superseded by the DCCCXIV "
                "graviton correction and DCCCXV master update."
            ),
        },
        {
            "kind": "audit_range_superseded",
            "prior_audit_range_end": prior_audit["summary"]["range_end"],
            "current_result_max_decimal": current_max_decimal,
            "valid_result_max_decimal": valid_result_max_decimal,
            "message": (
                "The DCCCXIV claim-ledger audit intentionally covered 784..813. "
                f"The live result ledger now reaches {current_max_decimal}, so this "
                "DCCCXXXVIII layer bridges the post-audit updates."
            ),
        },
        {
            "kind": "invalid_result_json_surfaces",
            "files": invalid_result_json_files,
            "message": (
                "Several post-828 files use a *_results.json suffix but contain "
                "Markdown rather than machine-readable JSON. The theorem surface "
                "reaches DCCCXXXII while valid result JSONs currently reach "
                f"{valid_result_max_decimal}."
            ),
        },
    ]

    identities = {
        "old_dcccii_sigma_mismatch_still_present": (
            historical_top_claim_limit <= 1.0 and historical_top_max_sigma > 1.0
        ),
        "dcccxi_top_tension_is_present": (
            top_811.get("part") == "DCCCXI"
            and dcccxi_tension_sigma >= 10.0
            and "TENSION" in str(top_811.get("status", "")).upper()
        ),
        "dcccxiv_graviton_correction_present": (
            correction_814.get("part") == "DCCCXIV"
            and correction_814.get("decimal") == 814
            and "DCCCXI" in correction_814.get("connections", [])
        ),
        "dcccxiv_correction_closes_top_sector": (
            corrected_top_sigma <= 1.0
            and "top mass tension closed"
            in str(correction_814.get("status", "")).lower()
        ),
        "dcccxv_master_promotes_correction": (
            master_815.get("part") == "DCCCXV"
            and master_815.get("decimal") == 815
            and "DCCCXIV" in master_815.get("connections", [])
            and master_promoted_top_sigma == corrected_top_sigma
        ),
        "duplicate_dcccxiv_markdown_detected": len(dcccxiv_markdowns) == 2,
        "single_dcccxiv_result_json_detected": dcccxiv_result_count == 1,
        "prior_audit_remains_historical_guardrail": (
            prior_audit["summary"]["range_end"] == 813
            and any(
                flag.get("kind") == "sigma_status_mismatch"
                and flag.get("part") == "DCCCII"
                for flag in prior_flags
            )
        ),
        "ledger_reaches_closure_burst_after_audit": current_max_decimal >= 837,
        "post_828_result_json_hygiene_gap_detected": (
            valid_result_max_decimal < current_max_decimal
            and len(invalid_result_json_files) >= 4
        ),
    }

    summary = ReconciliationSummary(
        part="DCCCXXXVIII",
        decimal=838,
        current_result_max_decimal=current_max_decimal,
        valid_result_max_decimal=valid_result_max_decimal,
        invalid_result_json_count=len(invalid_result_json_files),
        dcccxiv_markdown_count=len(dcccxiv_markdowns),
        duplicate_part_surface_count=max(0, len(dcccxiv_markdowns) - 1),
        dcccxiv_result_count=dcccxiv_result_count,
        historical_top_claim_limit_sigma=historical_top_claim_limit,
        historical_top_max_sigma=historical_top_max_sigma,
        dcccxi_tension_sigma=dcccxi_tension_sigma,
        corrected_top_sigma=corrected_top_sigma,
        master_promoted_top_sigma=master_promoted_top_sigma,
        audit_flag_count=len(audit_flags),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "identities": identities,
        "audit_flags": audit_flags,
        "chain": {
            "historical_source": "DCCCII",
            "sharpened_tension": "DCCCXI",
            "correction": "DCCCXIV",
            "master_update": "DCCCXV",
            "reconciliation": "DCCCXXXVIII",
        },
        "dcccxiv_surfaces": {
            "markdown_files": dcccxiv_markdowns,
            "result_count": dcccxiv_result_count,
        },
        "invalid_result_json_files": invalid_result_json_files,
        "theorem": (
            "Post-Audit Reconciliation Ledger. The DCCCII top-mass "
            "sigma/status mismatch remains a valid historical audit flag, "
            "DCCCXI records the sharpened top-pole tension, DCCCXIV supplies "
            "the graviton correction to 0.93 sigma, and DCCCXV promotes that "
            "correction into the live master scorecard. The duplicated "
            "DCCCXIV part surface is detected as a numbering-ledger issue, and "
            "post-828 Markdown-in-.json result surfaces are flagged separately."
        ),
        "honesty_boundary": (
            "This verifier reconciles internal repository state. It does not "
            "validate the physical graviton self-energy derivation or replace "
            "external experimental review."
        ),
        "status": (
            "RECONCILED - DCCCII top tension superseded; duplicate DCCCXIV "
            "surface detected"
        ),
    }


def write_reconciliation(path: Path = OUT_PATH) -> Path:
    payload = build_reconciliation()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_reconciliation()
    payload = build_reconciliation()
    print(f"Wrote {out}")
    print(f"Verified: {payload['summary']['all_identities_hold']}")
    print(f"audit_flags = {payload['summary']['audit_flag_count']}")


if __name__ == "__main__":
    main()
