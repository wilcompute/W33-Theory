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
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1382_non_clifford_port_abi.json")
    ns = ap.parse_args()
    contract = load("data/bt1377_physical_universal_computation_contract.json")
    runtime = load("data/bt1378_runtime_contract_verification.json")
    ports = [
        {
            "name": "Hesse-SIC/T measurement port",
            "resource_class": "magic-state or SIC-assisted non-stabilizer measurement",
            "entry_boundary": "measurement/topological boundary after Clifford packet scheduling",
            "packet_interface": "inject one non-Clifford resource token into the protected Clifford runtime",
            "verification_signature": ["not Clifford-generated", "consumed by measurement/injection", "returns to Clifford packet ABI"],
            "status": "recorded ABI; physical resource factory not yet certified"
        },
        {
            "name": "Fibonacci braiding port",
            "resource_class": "topological non-Clifford braid resource",
            "entry_boundary": "braid/measurement boundary coupled to the packet scheduler",
            "packet_interface": "export Clifford-protected logical wire to braid resource and reimport outcome",
            "verification_signature": ["non-Clifford braid generator", "classical feed-forward outcome", "returns to Clifford packet ABI"],
            "status": "recorded ABI; braid hardware not yet certified"
        }
    ]
    checks = {
        "runtime_contract_verified": runtime["verified"] is True,
        "bt1377_requires_port": contract["universal_port"]["required"] is True,
        "deterministic_kernel_not_universal": contract["deterministic_kernel"]["universal_without_port"] is False,
        "two_port_options": len(ports) == 2,
        "all_ports_have_entry_boundary": all("entry_boundary" in p for p in ports),
        "all_ports_return_to_packet_abi": all("packet ABI" in p["packet_interface"] or "packet ABI" in " ".join(p["verification_signature"]) for p in ports),
    }
    result = {
        "bt": 1382,
        "title": "Non-Clifford port ABI certificate",
        "verified": all(checks.values()),
        "checks": checks,
        "deterministic_kernel": {
            "runtime_order": contract["deterministic_kernel"]["runtime_order"],
            "universal_without_port": contract["deterministic_kernel"]["universal_without_port"],
            "word_ticks": contract["deterministic_kernel"]["word_ticks"]
        },
        "ports": ports,
        "honest_boundary": "BT1382 certifies the ABI and verification contract for non-Clifford injection. It does not certify a magic-state factory, Hesse-SIC hardware, or Fibonacci anyon device."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1382, "verified": result["verified"], "ports": len(ports)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
