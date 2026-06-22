#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1455_claim_firewall.json"


def main() -> None:
    claims = [
        {"claim": "Szilassi fixed hexagon [11,9,12,10,8,13] under R(x,y,z)=(-x,-y,z)", "tier": "exact_coordinate", "basis": "BT1444 coordinate parser", "paper_language": "exact finite coordinate fact"},
        {"claim": "12*(13+1)=168 and 12*2=24 active/guard lift", "tier": "exact_finite_arithmetic", "basis": "BT1439 and BT1448 finite bus maps", "paper_language": "exact count lift"},
        {"claim": "closure tick preserves retwined CSS syndrome equivariance", "tier": "verified_finite_decoder", "basis": "BT1449 closure trials", "paper_language": "finite decoder-compatible carrier"},
        {"claim": "tau_4 with D4 shear generates S3 x C3", "tier": "exact_finite_group", "basis": "BT1453 classifier", "paper_language": "exact finite group classifier"},
        {"claim": "quartic coefficient 4-phi^2 bridges 3 opposite pairs and 13 half-turn core", "tier": "numerical_structural_resonance", "basis": "BT1454 coefficient identities", "paper_language": "arithmetic resonance / structural hint"},
        {"claim": "Otto visible rounded g value is close to measured g", "tier": "numerical_resonance", "basis": "BT1438 visible-value residual audit", "paper_language": "rounded numerical proximity only"},
        {"claim": "Otto equations 49,50,64,65,66 give a formula-level derivation", "tier": "blocked_pending_transcription", "basis": "BT1447/BT1450 equation bodies unavailable as text", "paper_language": "do not claim until equations are transcribed and audited"},
        {"claim": "Moebius-ball carrier is established as a real-world model", "tier": "speculative_not_imported", "basis": "requires normalization, spin cover, moment formula, and discriminating tests", "paper_language": "not imported as established real-world physics"},
    ]
    tier_counts = {}
    for row in claims:
        tier_counts[row["tier"]] = tier_counts.get(row["tier"], 0) + 1
    checks = {
        "has_exact_coordinate_claim": any(row["tier"] == "exact_coordinate" for row in claims),
        "has_finite_decoder_claim": any(row["tier"] == "verified_finite_decoder" for row in claims),
        "has_resonance_claim": any("resonance" in row["tier"] for row in claims),
        "has_blocked_formula_claim": any(row["tier"] == "blocked_pending_transcription" for row in claims),
        "has_speculative_not_imported_claim": any(row["tier"] == "speculative_not_imported" for row in claims),
        "no_speculative_claim_promoted_to_exact": not any(row["tier"].startswith("exact") and "real-world" in row["claim"] for row in claims),
    }
    result = {
        "bt": 1455,
        "title": "Claim firewall for Otto/W33 bridge",
        "verified": all(checks.values()),
        "claims": claims,
        "tier_counts": tier_counts,
        "recommended_paper_rule": "Use exact language for coordinate, bus, group, and decoder facts; use resonance language for quartic and rounded-g numerics; keep formula-level and real-world claims blocked until audited.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1455, "verified": result["verified"], "tiers": tier_counts}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
