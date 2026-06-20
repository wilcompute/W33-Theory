#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1402_photonic_manuscript_runtime_frontier.json"


def load_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def row_named(rows: list[dict[str, Any]], name: str) -> dict[str, Any]:
    return next(row for row in rows if row["name"] == name)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()

    runtime = load_json("data/bt1378_runtime_contract_verification.json")
    port_abi = load_json("data/bt1385_hesse_sic_t_port_abi.json")
    queue = load_json("data/bt1391_hesse_sic_t_queue_model.json")
    demonstrator = load_json("data/bt1394_reduced_qutrit_demonstrator.json")
    maxsat = load_json("data/bt1395_s3_maxsat_bound_pathway.json")
    eraser = load_json("data/bt1396_qutrit_quantum_erasure_readout.json")
    example = load_json("data/bt1397_example_optimality_certificate_verification.json")
    noise = load_json("data/bt1400_qutrit_erasure_noise_sensitivity.json")

    holonet = read("photonic_holonet.tex")
    single_photon = read("single_photon_universal_computation.tex")
    claim_master = read("paper/w33_q4_claim_stratified_master.tex")
    docs_index = read("docs/index.html")
    holonet_norm = " ".join(holonet.split())
    single_photon_norm = " ".join(single_photon.split())

    baseline = row_named(noise["rows"], "baseline")
    conservative = row_named(noise["rows"], "conservative")
    baseline_heavy = row_named(queue["rows"], "baseline_heavy")
    conservative_medium = row_named(queue["rows"], "conservative_medium")

    checks = {
        "runtime_contract_verified": runtime["verified"] is True
        and runtime["checks"]["runtime_order_51840"] is True,
        "demonstrator_visibility_tuple": demonstrator["verified"] is True
        and abs(demonstrator["visibility_results"]["I_tensor_I"] - 1.0) < 1e-12
        and abs(demonstrator["visibility_results"]["F_tensor_I"] - (1.0 / 3.0)) < 1e-12
        and abs(demonstrator["visibility_results"]["F_tensor_F_conj_invariant"] - 1.0)
        < 1e-12
        and demonstrator["visibility_results"]["X_tensor_I"] < 1e-12
        and demonstrator["visibility_results"]["Z_tensor_I"] < 1e-12,
        "eraser_restores_route_coherence": eraser["verified"] is True
        and abs(eraser["readout"]["eraser_success_probability"] - (1.0 / 3.0)) < 1e-12
        and eraser["readout"]["conditional_route_l1_coherence"] == 2.0,
        "noise_model_has_strong_and_conservative_passes": noise["verified"] is True
        and baseline["coherence_gamma"] > 0.9
        and conservative["coherence_gamma"] > 0.75,
        "hesse_sic_t_abi_is_concrete": port_abi["verified"] is True
        and port_abi["resource_token"]["sic_outcomes"] == 9
        and port_abi["timing_contract"]["clifford_window_ticks"] == 51840,
        "queue_has_positive_slack_in_live_cases": queue["verified"] is True
        and baseline_heavy["expected_slack_tokens_per_window"] > 0
        and conservative_medium["expected_slack_tokens_per_window"] > 0,
        "maxsat_boundary_is_witness_not_global_proof": maxsat["verified"] is True
        and maxsat["computed_score"] == 210
        and maxsat["optimality_status"] == "witness_only"
        and example["project_optimality_status"] == "not_solver_certified",
        "holonet_exposes_bt1402_runtime_frontier": "BT1402 runtime-frontier handoff"
        in holonet_norm
        and "Hesse-SIC/T token has nine outcomes" in holonet_norm
        and "MaxSAT frontier remains witness-only" in holonet_norm,
        "single_photon_exposes_bt1402_runtime_frontier": "BT1402 Runtime-Frontier Handoff"
        in single_photon_norm
        and "route register is maximally mixed before the eraser" in single_photon_norm
        and "Hesse-SIC/T port consumes one nine-outcome SIC token"
        in single_photon_norm,
        "claim_master_already_exposes_runtime_frontier": "BT1394 verifies the reduced Bell-qutrit signatures"
        in claim_master
        and "BT1385 makes the Hesse-SIC/T option concrete" in claim_master,
        "docs_index_exposes_bt1402_card": "BT1402: manuscript runtime-frontier handoff"
        in docs_index
        and "baseline gamma" in docs_index,
    }

    result = {
        "bt": 1402,
        "title": "Photonic holonet manuscript runtime-frontier handoff",
        "verified": all(checks.values()),
        "checks": checks,
        "frontier_contract": {
            "clifford_runtime": {
                "runtime_order": 51840,
                "word_ticks": 8,
                "clifford_window_ticks": 51840,
            },
            "single_photon_demonstrator": {
                "V(I)": demonstrator["visibility_results"]["I_tensor_I"],
                "V(F3)": demonstrator["visibility_results"]["F_tensor_I"],
                "V(F3_tensor_conj_invariant)": demonstrator["visibility_results"][
                    "F_tensor_F_conj_invariant"
                ],
                "V(X)": demonstrator["visibility_results"]["X_tensor_I"],
                "V(Z)": demonstrator["visibility_results"]["Z_tensor_I"],
                "route_reduced_purity": demonstrator["route_control"]["route_purity"],
            },
            "quantum_eraser_readout": {
                "success_probability": eraser["readout"]["eraser_success_probability"],
                "conditional_l1_coherence": eraser["readout"][
                    "conditional_route_l1_coherence"
                ],
                "baseline_gamma": baseline["coherence_gamma"],
                "conservative_gamma": conservative["coherence_gamma"],
            },
            "hesse_sic_t_port": {
                "sic_outcomes": 9,
                "queue_window_microframes": queue["window"]["microframes"],
                "baseline_heavy_slack_tokens": baseline_heavy[
                    "expected_slack_tokens_per_window"
                ],
                "conservative_medium_slack_tokens": conservative_medium[
                    "expected_slack_tokens_per_window"
                ],
            },
            "s3_maxsat_boundary": {
                "computed_score": maxsat["computed_score"],
                "project_status": example["project_optimality_status"],
            },
        },
        "boundary": (
            "BT1402 is a manuscript/frontier consistency packet. It does not "
            "certify physical Hesse-SIC optics, a magic-state factory, detector "
            "dark-count budgets, or a solver-generated global S3 optimum."
        ),
    }

    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "baseline_gamma": baseline["coherence_gamma"],
                "maxsat_status": maxsat["optimality_status"],
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
