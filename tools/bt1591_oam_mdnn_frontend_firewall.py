#!/usr/bin/env python3
"""BT1591: OAM-MDNN front-end proposal with the exact ABI firewall intact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1591_oam_mdnn_frontend_firewall.json"
MD = ROOT / "analysis" / "BT1591_oam_mdnn_frontend_firewall.md"
TEX = ROOT / "analysis" / "BT1591_oam_mdnn_frontend_firewall.tex"


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    literature = load_json("data/bt1588_oam_literature_claim_firewall.json")
    radial = load_json("data/bt1589_lg_oam_radial_covariance_simulator.json")
    lanes = load_json("data/bt1590_full_witness_lane_sheet_compiler.json")

    source_keys = {source["key"] for source in literature["sources"]}
    exact_numbers = {
        "recenter_sectors": 9,
        "centered_transaction_words": 24,
        "finite_action_addresses": 216,
        "witness_segments": lanes["counts"]["segments"],
        "witness_ticks": lanes["counts"]["total_ticks"],
        "radial_worst_eta": radial["worst_case"]["effective_eta"],
        "radial_recentered_threshold": radial["model"]["recentered_threshold"],
    }
    frontend_layers = [
        {
            "layer": "LG mode cleaner and radial monitor",
            "physical_role": "prepare/monitor p=0,1,2 radial shells before any recenter decision",
            "repo_interface": "BT1589 radial channel family L(eta)",
            "acceptance_test": "row-stochastic shell tomography and worst eta below recentered threshold",
            "claim_tier": "calibration requirement",
        },
        {
            "layer": "OAM sector sorter",
            "physical_role": "classify the affine shift sector (x,z) in F3^2",
            "repo_interface": "9 recenter sectors feeding BT1587",
            "acceptance_test": "9x9 sector confusion matrix with dark-reference controls",
            "claim_tier": "hardware proposal",
        },
        {
            "layer": "diffractive multiplex/demultiplex front-end",
            "physical_role": "passively fan mode families into the recenter-sector channels",
            "repo_interface": "OAM-MDNN source motivates multiplexed mode processing only",
            "acceptance_test": "inter-sector crosstalk matrix measured before ABI claims",
            "claim_tier": "literature motivation",
        },
        {
            "layer": "24-word transaction selector",
            "physical_role": "select the centered S4 fiber transaction word after recentering",
            "repo_interface": "BT1495 24 centered 72-tick words",
            "acceptance_test": "each word reused 45 times in BT1590 lane sheet",
            "claim_tier": "exact finite ABI",
        },
        {
            "layer": "native D4 fast lane plus S4 relabel lane",
            "physical_role": "send eight square-subgroup words through native D4 routing and sixteen through analyzer relabels",
            "repo_interface": "BT1590 native 25920 ticks / relabel 51840 ticks",
            "acceptance_test": "D4 and S4 tick counts match the full witness replay",
            "claim_tier": "exact finite ABI schedule",
        },
        {
            "layer": "five-gate witness replay",
            "physical_role": "run I,X,Z,F3,S across all recenter sectors and transaction words",
            "repo_interface": "BT1590 77760-tick lane sheet",
            "acceptance_test": "lane balance, detector balance, radial covariance, and external-reference comparison",
            "claim_tier": "protocol witness",
        },
    ]
    claim_firewall = [
        {
            "claim": "OAM-MDNN supports multiplexed OAM mode processing as an optical front-end idea",
            "allowed": True,
            "basis": "external literature motivation plus BT1591 layer mapping",
        },
        {
            "claim": "OAM-MDNN proves the holonet 216-action ABI",
            "allowed": False,
            "basis": "ABI proof remains BT1587/BT1590 exact finite certificates",
        },
        {
            "claim": "BT1589 proves measured LG radial leakage",
            "allowed": False,
            "basis": "BT1589 is symbolic shell covariance only",
        },
        {
            "claim": "BT1590 is a calibrated optical-loss budget",
            "allowed": False,
            "basis": "BT1590 is a deterministic lane/timing compiler",
        },
        {
            "claim": "The front-end can be accepted after tomography, crosstalk, and 77760-tick replay pass",
            "allowed": True,
            "basis": "explicit protocol acceptance tests, not assumed from papers",
        },
    ]
    acceptance_matrix = {
        "radial_covariance": radial["verified"] is True
        and radial["worst_case"]["effective_eta"]
        < radial["model"]["recentered_threshold"],
        "full_lane_replay": lanes["verified"] is True
        and lanes["counts"]["total_ticks"] == 77760,
        "literature_firewall": literature["verified"] is True
        and "oam_multiplexing_natphot_2026" in source_keys,
        "exact_numbers_align": exact_numbers["recenter_sectors"]
        * exact_numbers["centered_transaction_words"]
        == exact_numbers["finite_action_addresses"],
        "native_plus_relabel_exhausts_ticks": lanes["action_level_tick_counts"][
            "native_d4_square_pulse"
        ]
        + lanes["action_level_tick_counts"]["s4_analyzer_relabel"]
        == lanes["counts"]["total_ticks"],
        "blocked_claims_present": sum(not row["allowed"] for row in claim_firewall)
        == 3,
    }
    result = {
        "bt": 1591,
        "title": "OAM-MDNN front-end firewall",
        "verified": all(acceptance_matrix.values()),
        "source_packets": {
            "literature_firewall": "data/bt1588_oam_literature_claim_firewall.json",
            "radial_covariance": "data/bt1589_lg_oam_radial_covariance_simulator.json",
            "lane_sheet": "data/bt1590_full_witness_lane_sheet_compiler.json",
        },
        "external_source_used": "oam_multiplexing_natphot_2026",
        "exact_numbers": exact_numbers,
        "frontend_layers": frontend_layers,
        "claim_firewall": claim_firewall,
        "acceptance_matrix": acceptance_matrix,
        "interpretation": (
            "The cool architecture move is to use OAM-multiplexed diffractive optics as a "
            "front-end sectorizer, not as the quantum computer. It passively classifies and "
            "routes mode families into the nine recenter sectors; the exact holonet work is "
            "still the local 9*24 ABI and the 77760-tick witness replay."
        ),
        "honesty_boundary": (
            "BT1591 is a hardware-front-end proposal and claim firewall. It does not assert "
            "that an OAM-MDNN implements a quantum gate, preserves coherence, or meets loss "
            "budgets without the listed measurements."
        ),
        "checks": acceptance_matrix,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1591 OAM-MDNN Front-End Firewall\n\n"
        "BT1591 uses the 2026 OAM-multiplexed diffractive-neural-network result as a "
        "front-end design hint only. The proposed physical role is passive sector sorting "
        "into the nine affine recenter channels; the exact computation remains the local "
        "`9*24=216` ABI and the BT1590 `77760`-tick witness replay.\n",
        encoding="utf-8",
    )
    TEX.write_text(
        "\\begin{center}\\small\n"
        "BT1591: OAM-multiplexed diffractive optics are a proposed sectorizing front end; "
        "the exact claim remains the local $9\\cdot24=216$ ABI and the $77760$-tick witness replay.\n"
        "\\end{center}\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1591,
                "verified": result["verified"],
                "ticks": exact_numbers["witness_ticks"],
                "front_end_layers": len(frontend_layers),
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
