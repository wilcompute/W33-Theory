#!/usr/bin/env python3
"""BT1317 - Consolidated raw-data to tomotope/Markov pipeline verifier.

This script ties together the artifacts that had previously lived in separate
packets:

  raw toroidal TXT -> CCCCXXI Fano bridge -> 168/192 tomotope packet bridge
  -> 42-step transport -> 7+1 Markov stationary split -> 21/16 Fourier source.

The point is not a new count. It is a single executable chain showing that all
published toroidal/tomotope layers agree on the same heptad carrier.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "bt1317_toroidal_tomotope_pipeline_consolidator.json"


def _load_module(name: str, relpath: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relpath)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module at {relpath}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _raw_heptad() -> dict[str, Any]:
    bt803 = _load_module("bt803", "analysis/bt803_seven_realizations_census.py")
    rows = bt803.parse_dataset(ROOT / "data" / "Toroidal-Polyhedra-Realizations.txt")
    family_counts = {
        "Csaszar": sum(1 for row in rows if row["kind"] == "Csaszar"),
        "Szilassi": sum(1 for row in rows if row["kind"] == "Szilassi"),
    }
    edge_counts = sorted({len(bt803.edges_of(row["faces"])) for row in rows})
    euler_values = sorted(
        {
            len(row["vertices"]) - len(bt803.edges_of(row["faces"])) + len(row["faces"])
            for row in rows
        }
    )
    return {
        "total": len(rows),
        "family_counts": family_counts,
        "edge_counts": edge_counts,
        "euler_values": euler_values,
    }


def build_pipeline() -> dict[str, Any]:
    ccccxxi = _load_module(
        "ccccxxi", "exploration/PART_CCCCXXI_TOROIDAL_FANO_BRIDGE.py"
    )
    dual_packet = _load_module(
        "dual_packet", "scripts/tomotope_toroidal_dual_packet_bridge.py"
    )
    step_transport = _load_module(
        "step_transport", "scripts/tomotope_toroidal_step_transport_bridge.py"
    )
    markov_ground = _load_module(
        "markov_ground", "scripts/tomotope_toroidal_markov_ground_bridge.py"
    )
    markov_fourier = _load_module(
        "markov_fourier", "scripts/tomotope_toroidal_markov_fourier_bridge.py"
    )

    raw = _raw_heptad()
    fano = ccccxxi.build_results()
    packet = dual_packet.build_bridge()
    step = step_transport.build_bridge()
    ground = markov_ground.build_bridge()
    fourier = markov_fourier.build_bridge()

    nontrivial_second_moment = Fraction(
        int(fourier["summary"]["nontrivial_square_sum_num"]),
        int(fourier["summary"]["nontrivial_square_sum_den"]),
    )
    unoriented_from_moment = nontrivial_second_moment * 16
    oriented_from_moment = unoriented_from_moment * 2
    weighted_from_moment = oriented_from_moment * int(
        step["summary"]["slot_stabilizer_size"]
    )

    chain = {
        "raw_heptad": raw["total"],
        "fano_realization_count": fano["realization_counting"]["total_realizations"],
        "active_packet_weight": packet["summary"]["active_packet_weight"],
        "tomotope_weight": packet["summary"]["tomotope_weight"],
        "oriented_transports": step["summary"]["oriented_transport_count"],
        "weighted_active_transport": step["summary"]["weighted_active_transport"],
        "stationary_active_weight": ground["summary"]["stationary_active_weight"],
        "stationary_ground_weight": ground["summary"]["stationary_ground_weight"],
        "nontrivial_second_moment": str(nontrivial_second_moment),
        "moment_ladder": {
            "times_16": int(unoriented_from_moment),
            "times_2": int(oriented_from_moment),
            "times_stabilizer_4": int(weighted_from_moment),
        },
    }

    checks = {
        "raw_is_five_plus_two_heptad": raw["total"] == 7
        and raw["family_counts"] == {"Csaszar": 5, "Szilassi": 2},
        "raw_all_genus_one_with_21_edges": raw["edge_counts"] == [21]
        and raw["euler_values"] == [0],
        "fano_bridge_verified": fano["verified"]
        and fano["checks_passed"] == fano["checks_total"] == 48,
        "packet_bridge_verified": packet["summary"]["all_identities_hold"],
        "active_packet_matches_dual_flags": packet["summary"]["active_packet_weight"]
        == packet["summary"]["dual_toroidal_flag_weight"]
        == 168,
        "tomotope_is_active_plus_ground": packet["summary"]["tomotope_weight"] == 192
        and packet["summary"]["ground_packet_weight"] == 24,
        "step_transport_bridge_verified": step["summary"]["all_identities_hold"],
        "transport_weight_matches_packet_weight": step["summary"][
            "weighted_active_transport"
        ]
        == packet["summary"]["active_packet_weight"]
        == 168,
        "markov_ground_bridge_verified": ground["summary"]["all_identities_hold"],
        "stationary_weights_match_packet_split": (
            ground["summary"]["stationary_active_weight"],
            ground["summary"]["stationary_ground_weight"],
        )
        == (168, 24),
        "fourier_bridge_verified": fourier["summary"]["all_identities_hold"],
        "moment_ladder_recovers_21_42_168": (
            unoriented_from_moment,
            oriented_from_moment,
            weighted_from_moment,
        )
        == (Fraction(21, 1), Fraction(42, 1), Fraction(168, 1)),
    }

    return {
        "theorem": "BT1317 toroidal tomotope pipeline consolidator",
        "verified": all(checks.values()),
        "pipeline_chain": chain,
        "raw": raw,
        "upstream": {
            "ccccxxi_checks": f"{fano['checks_passed']}/{fano['checks_total']}",
            "dual_packet_summary": packet["summary"],
            "step_transport_summary": step["summary"],
            "markov_ground_summary": ground["summary"],
            "markov_fourier_summary": fourier["summary"],
        },
        "checks": checks,
        "boundary": (
            "This consolidates existing verified carriers. It does not assert "
            "that metric realization labels are canonical Fano labels; BT1318 "
            "tests the C2-axis issue separately."
        ),
    }


def write_results(path: Path = OUT_PATH) -> Path:
    payload = build_pipeline()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    payload = build_pipeline()
    out = write_results()
    print(f"BT1317 verified={payload['verified']} wrote {out}")
    if not payload["verified"]:
        failed = [name for name, ok in payload["checks"].items() if not ok]
        raise SystemExit(f"BT1317 failed checks: {failed}")


if __name__ == "__main__":
    main()
