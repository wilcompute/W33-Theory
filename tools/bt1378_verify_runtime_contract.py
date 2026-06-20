#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1378_runtime_contract_verification.json")
    ns = ap.parse_args()
    q4 = load("data/bt1362_symmetric_q4_gauge_quotient.json")
    packet = load("data/bt1374_q6_tomotope_packet_route_compiler.json")
    operator = load("data/bt1375_steinberg_cycle_operator_scheduler_lift.json")
    contract = load("data/bt1377_physical_universal_computation_contract.json")
    checks = {
        "q4_symmetric_3244": q4["code"] == {"n": 32, "rank_hx": 15, "rank_hz": 13, "k": 4, "dx": 4, "dz": 4},
        "q4_clock_stabilizer_64": q4["symmetry"]["symmetric_active_stabilizer_size"] == 64,
        "q4_clock_structure_c2_4_c4": q4["symmetry"]["stabilizer_structure"] == "C2^4 : C4",
        "packet_compiler_verified": all(packet["checks"].values()),
        "packet_rule_is_4block_plus_mod4": packet["address_rule"]["formula"] == "tomotope_flag = 4 * tomotope_block + (mirror_slot mod 4)",
        "packet_bus_192": "192" in packet["address_rule"]["meaning"],
        "steinberg_operator_verified": operator.get("verified") is True,
        "contract_verified": contract["verified"] is True,
        "deterministic_kernel_not_universal": contract["deterministic_kernel"]["universal_without_port"] is False,
        "non_clifford_port_required": contract["universal_port"]["required"] is True,
        "runtime_order_51840": contract["deterministic_kernel"]["runtime_order"] == 51840,
        "mirror_bus_2160": contract["deterministic_kernel"]["mirror_bus_ticks"] == 2160,
        "word_ticks_8": contract["deterministic_kernel"]["word_ticks"] == 8
    }
    result = {
        "bt": 1378,
        "title": "Physical runtime contract verifier",
        "verified": all(checks.values()),
        "checks": checks,
        "pipeline": [
            "BT1362 symmetric Q4 [[32,4,4]] quotient with C2^4:C4 clock",
            "BT1374 packet route compiler to single-bit Q6/tomotope edges",
            "BT1375 central C3 Steinberg scheduler",
            "BT1377 protected Clifford runtime plus explicit non-Clifford port"
        ],
        "honest_boundary": "The deterministic packet machine is a certified Clifford/symplectic runtime. Universal computation still requires the explicit non-Clifford port."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1378, "verified": result["verified"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
