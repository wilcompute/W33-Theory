#!/usr/bin/env python3
"""Compare conventional control tables with generated W(3,3) control on real wrapped programs.

The Holonet wrapper already turns arbitrary commands into W(3,3) packet
envelopes.  This witness runs small deterministic programs through that wrapper
and records what the architecture avoids:

* no persistent next-hop table;
* packet destinations generated from projective addresses;
* line/spread schedule produced by the existing compiler;
* packet-specific next-hop fields replaced by incidence generation.

It keeps the boundary explicit: the child commands still execute on the host
CPU.  The comparison is over the control plane that surrounds those commands.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "data" / "w33_wrapped_program_control_comparison.json"
DEFAULT_MD = ROOT / "docs" / "w33_wrapped_program_control_comparison.md"


PROGRAMS = [
    {
        "name": "sum_of_squares_40",
        "code": "print(sum(i*i for i in range(40)))",
        "expected_stdout": "20540\n",
    },
    {
        "name": "rule110_16",
        "code": (
            "s='0001000000000000'\n"
            "rule=110\n"
            "for _ in range(16):\n"
            "    nxt=[]\n"
            "    for i in range(len(s)):\n"
            "        tri=s[(i-1)%len(s)]+s[i]+s[(i+1)%len(s)]\n"
            "        nxt.append(str((rule >> int(tri,2)) & 1))\n"
            "    s=''.join(nxt)\n"
            "print(s)\n"
        ),
        "expected_stdout": None,
    },
]


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def run_wrapper(program: dict[str, Any]) -> dict[str, Any]:
    out = ROOT / "data" / f"w33_wrap_compare_{program['name']}.json"
    cmd = [
        sys.executable,
        str(ROOT / "analysis" / "holonet_wrap.py"),
        "--max-packets",
        "12",
        "--optimize",
        "clock-slots",
        "--compile-exact-backend",
        "off",
        "--out",
        str(out.relative_to(ROOT)),
        "--",
        sys.executable,
        "-c",
        program["code"],
    ]
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"wrapper failed for {program['name']}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    report = json.loads(out.read_text(encoding="utf-8"))
    report["_wrapper_stdout"] = proc.stdout
    report["_wrapper_json"] = str(out.relative_to(ROOT))
    return report


def command_row(
    program: dict[str, Any],
    report: dict[str, Any],
    per_instance_route_bytes: int,
    per_instance_control_bytes: int,
) -> dict[str, Any]:
    compilation = report.get("holonet_compilation", {})
    active = compilation.get("active_policy", {})
    clock_native = compilation.get("clock_native_policy", {})
    stdout_ok = (
        True
        if program["expected_stdout"] is None
        else report["stdout_preview"] == program["expected_stdout"]
    )
    return {
        "name": program["name"],
        "returncode": report["returncode"],
        "stdout_preview": report["stdout_preview"],
        "stdout_ok": stdout_ok,
        "packet_count": report["packet_count"],
        "max_hops": report["max_hops"],
        "generated_routing_state_bytes": report["control_plane"]["routing_state_bytes"],
        "conventional_persistent_routing_table_bytes": per_instance_route_bytes,
        "conventional_listed_control_table_bytes": per_instance_control_bytes,
        "packet_specific_next_hop_bits_avoided": report["control_plane"][
            "classical_next_hop_bits_avoided_for_packet_destinations"
        ],
        "active_ticks": active.get("ticks"),
        "active_clock_slots": active.get("clock_slots"),
        "clock_native_ticks": clock_native.get("ticks"),
        "clock_native_clock_slots": clock_native.get("clock_slots"),
        "selected_policy": compilation.get("selected_policy_schedule"),
        "wrapper_json": report["_wrapper_json"],
        "boundary": report["boundary"],
    }


def build_payload() -> dict[str, Any]:
    instance = load_json("data/w33_instance_architecture_map.json")
    recursive = load_json("data/w33_recursive_instance_compression.json")
    route_bytes = next(
        item["naive_bytes"]
        for item in instance["compression_ledger"]
        if item["name"] == "next-hop routing table"
    )
    control_bytes = sum(item["naive_bytes"] for item in instance["compression_ledger"])
    reports = [run_wrapper(program) for program in PROGRAMS]
    rows = [
        command_row(program, report, route_bytes, control_bytes)
        for program, report in zip(PROGRAMS, reports)
    ]
    aggregate = {
        "programs": len(rows),
        "total_packets": sum(row["packet_count"] for row in rows),
        "max_hops": max(row["max_hops"] for row in rows),
        "persistent_routing_table_bytes_if_stored_per_instance": route_bytes,
        "listed_control_table_bytes_if_stored_per_instance": control_bytes,
        "generated_persistent_routing_state_bytes": 0,
        "packet_specific_next_hop_bits_avoided": sum(
            row["packet_specific_next_hop_bits_avoided"] for row in rows
        ),
    }
    checks = {
        "instance_map_passes": instance["status"] == "PASS",
        "recursive_compression_passes": recursive["status"] == "PASS",
        "all_wrapped_programs_return_zero": all(row["returncode"] == 0 for row in rows),
        "all_expected_stdout_matches": all(row["stdout_ok"] for row in rows),
        "all_routes_have_diameter_two": all(row["max_hops"] <= 2 for row in rows),
        "all_generated_route_state_zero": all(
            row["generated_routing_state_bytes"] == 0 for row in rows
        ),
        "route_table_bytes_match_instance_witness": route_bytes == 1170,
        "control_table_bytes_match_instance_witness": control_bytes == 1816,
        "compilers_emit_clock_native_policy": all(
            row["clock_native_clock_slots"] is not None for row in rows
        ),
    }
    payload = {
        "schema": "w33.wrapped_program_control_comparison.v1",
        "theorem": "W(3,3) wrapped-program control comparison",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "commands": rows,
        "aggregate": aggregate,
        "checks": checks,
        "interpretation": (
            "The wrapper makes ordinary programs into Holonet control packets. "
            "The host still executes the child arithmetic, but the surrounding "
            "routing/scheduling/audit envelope uses generated W33 incidence "
            "instead of persistent next-hop, bus, spread, or transition tables."
        ),
        "honesty_boundary": (
            "This is a control-plane comparison for real wrapped commands. It "
            "does not binary-translate the child program arithmetic into native "
            "qutrit gates or prove physical speedup."
        ),
    }
    return payload


def markdown(payload: dict[str, Any]) -> str:
    rows = []
    for row in payload["commands"]:
        rows.append(
            "| {name} | {packet_count} | {max_hops} | {active_clock_slots} | "
            "{clock_native_clock_slots} | {packet_specific_next_hop_bits_avoided} |".format(
                **row
            )
        )
    agg = payload["aggregate"]
    return f"""# W(3,3) Wrapped Program Control Comparison

This witness runs real commands through `analysis/holonet_wrap.py` and compares
the conventional control-plane payload with generated W(3,3) control.

| Program | Packets | Max hops | Active slots | Clock-native slots | Packet next-hop bits avoided |
|---|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

## Aggregate

- Programs wrapped: `{agg['programs']}`
- Total packets: `{agg['total_packets']}`
- Max route hops: `{agg['max_hops']}`
- Persistent routing table bytes if stored per instance: `{agg['persistent_routing_table_bytes_if_stored_per_instance']}`
- Listed control-table bytes if stored per instance: `{agg['listed_control_table_bytes_if_stored_per_instance']}`
- Generated persistent routing state bytes: `{agg['generated_persistent_routing_state_bytes']}`
- Packet-specific next-hop bits avoided: `{agg['packet_specific_next_hop_bits_avoided']}`

Boundary: the child programs still run on the host CPU. The comparison is over
the packet envelope: address generation, routing, scheduling, and audit state.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)

    payload = build_payload()
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    md_out = Path(args.md_out)
    if not md_out.is_absolute():
        md_out = ROOT / md_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_out.write_text(markdown(payload), encoding="utf-8")

    print(f"status: {payload['status']}")
    for row in payload["commands"]:
        print(
            f"{row['name']}: packets={row['packet_count']}, max_hops={row['max_hops']}, "
            f"clock_slots={row['clock_native_clock_slots']}"
        )
    print(
        "avoided: "
        f"{payload['aggregate']['persistent_routing_table_bytes_if_stored_per_instance']} routing bytes per instance, "
        f"{payload['aggregate']['packet_specific_next_hop_bits_avoided']} packet next-hop bits"
    )
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
