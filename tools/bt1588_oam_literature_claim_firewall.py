#!/usr/bin/env python3
"""BT1588: external OAM literature guardrail for the operator/OAM appendix."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1588_oam_literature_claim_firewall.json"
MD = ROOT / "analysis" / "BT1588_oam_literature_claim_firewall.md"

SOURCES = [
    {
        "key": "oam_toffoli_prl_2024",
        "title": "Polarization and Orbital Angular Momentum Encoded Quantum Toffoli Gate Enabled by Diffractive Neural Networks",
        "venue": "Physical Review Letters 133, 140601 (2024)",
        "url": "https://doi.org/10.1103/PhysRevLett.133.140601",
        "repo_use": "same-photon polarization/OAM controlled-gate motivation",
        "blocked_use": "does not prove the holonet internal operator-leg semantics",
    },
    {
        "key": "timebin_qudit_prl_2025",
        "title": "Robust approach for time-bin encoded photonic quantum states",
        "venue": "Physical Review Letters 134, 180802 (2025)",
        "url": "https://doi.org/10.1103/PhysRevLett.134.180802",
        "repo_use": "high-dimensional time-bin preparation/readout motivation",
        "blocked_use": "does not calibrate the holonet 72-tick transaction loss model",
    },
    {
        "key": "oam_topology_natcomm_2025",
        "title": "Revealing the topological nature of entangled orbital angular momentum states of light",
        "venue": "Nature Communications 16, 11095 (2025)",
        "url": "https://www.nature.com/articles/s41467-025-66066-3",
        "repo_use": "OAM topology and high-dimensional mode guardrail",
        "blocked_use": "does not identify the W(3,3) finite substrate or remove leakage tests",
    },
    {
        "key": "oam_multiplexing_natphot_2026",
        "title": "Orbital angular momentum multiplexing diffractive neural networks for high-capacity optical inference",
        "venue": "Nature Photonics (2026)",
        "url": "https://doi.org/10.1038/s41566-026-01930-2",
        "repo_use": "OAM multiplexing and diffractive mode-processing motivation",
        "blocked_use": "does not provide a quantum gate certificate or holonet transaction ABI",
    },
]


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    abi = load_json("data/bt1587_oam_recenter_transaction_abi.json")
    claim_ledger = load_json("data/bt1585_operator_oam_appendix_claim_ledger.json")
    leakage = load_json("data/bt1577_radial_leakage_bound_from_oam_phase_ops.json")
    checks = {
        "four_external_sources": len(SOURCES) == 4,
        "all_sources_have_urls": all(
            source["url"].startswith("https://") for source in SOURCES
        ),
        "all_sources_have_blocked_use": all(
            source["blocked_use"] for source in SOURCES
        ),
        "abi_verified": abi["verified"] is True,
        "claim_ledger_verified": claim_ledger["verified"] is True,
        "leakage_verified": leakage["verified"] is True,
        "claim_ledger_has_three_blocked": claim_ledger["tier_counts"][
            "blocked physical overclaim"
        ]
        == 3,
        "firewall_keeps_external_as_literature": all(
            "motivation" in source["repo_use"] or "guardrail" in source["repo_use"]
            for source in SOURCES
        ),
    }
    result = {
        "bt": 1588,
        "title": "OAM literature claim firewall",
        "verified": all(checks.values()),
        "sources": SOURCES,
        "source_packets": {
            "abi": "data/bt1587_oam_recenter_transaction_abi.json",
            "claim_ledger": "data/bt1585_operator_oam_appendix_claim_ledger.json",
            "leakage": "data/bt1577_radial_leakage_bound_from_oam_phase_ops.json",
        },
        "interpretation": (
            "Recent OAM and time-bin photonics support the physical direction: same-photon "
            "mode registers, high-dimensional time-bin control, OAM topology, and OAM "
            "multiplexed diffractive processing are real laboratory themes. The holonet imports "
            "them only as motivation and guardrails; "
            "the exact claim remains the finite 216-action recenter transaction ABI."
        ),
        "honesty_boundary": (
            "No external paper is used as a proof of W(3,3), calibrated loss, measured leakage, "
            "or internal operator-leg semantics. Those remain local repo certificates or blocked claims."
        ),
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text(
        "# BT1588 OAM Literature Claim Firewall\n\n"
        "BT1588 records four external OAM/time-bin guardrails and keeps them in the "
        "literature-motivation tier. The executable architecture claim is still the local "
        "BT1587 certificate: 216 internal Clifford/OAM actions are nine recentering shifts "
        "over 24 centered 72-tick transaction words.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"bt": 1588, "verified": result["verified"], "sources": len(SOURCES)},
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
