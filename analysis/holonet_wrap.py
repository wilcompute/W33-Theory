#!/usr/bin/env python3
"""Run any classical command inside a Holonet VM control envelope.

This wrapper is the practical bridge:

    arbitrary classical program
        -> command genome
        -> W(3,3) packet routing envelope
        -> side-channel snapshot
        -> substrate checksum / audit artifact

It does not pretend to replace the child process CPU arithmetic. Today it wraps the program's IO and
control plane in the Holonet architecture. That is still useful: every command becomes addressable,
route-scheduled, auditable, and ready to drive the physical-substrate stub. The next layer is binary
translation, where instruction/memory ops are lifted into the same packet ABI.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import holonet_node as hn  # noqa: E402
import holonet_sidechannel_suite as side  # noqa: E402
from w33_line_context_compiler import build_compilation  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def b3(n: int, width: int = 4) -> tuple[int, ...]:
    digs = []
    for _ in range(width):
        digs.append(n % 3)
        n //= 3
    return tuple(reversed(digs))


def point_from_digest(digest: bytes, offset: int) -> tuple[int, ...]:
    val = int.from_bytes(digest[offset : offset + 4], "big", signed=False)
    target = b3(val % 81)
    # Normalize through the same projective representative set by nearest deterministic scan.
    if any(target):
        normed = hn._norm(
            target
        )  # intentionally using module-local finite-field normalizer.
        if normed in hn.POINTS:
            return normed
    return hn.POINTS[val % len(hn.POINTS)]


def packetize(blob: bytes, label: str, max_packets: int) -> list[dict]:
    packets = []
    if not blob:
        blob = b"\x00"
    for i in range(0, min(len(blob), max_packets * 16), 16):
        chunk = blob[i : i + 16]
        digest = hashlib.sha256(label.encode() + i.to_bytes(4, "big") + chunk).digest()
        src = point_from_digest(digest, 0)
        dst = point_from_digest(digest, 8)
        path = hn.route(src, dst)
        packets.append(
            {
                "label": label,
                "index": i // 16,
                "bytes": len(chunk),
                "sha256_16": hashlib.sha256(chunk).hexdigest()[:16],
                "src": "".join(map(str, src)),
                "dst": "".join(map(str, dst)),
                "symplectic": int(hn.symplectic(src, dst)),
                "hops": len(path) - 1,
                "relays": len(hn.multipath(src, dst)) if len(path) == 3 else 0,
                "path": ["".join(map(str, p)) for p in path],
            }
        )
    return packets


def substrate_checksum(packets: list[dict]) -> str:
    acc = 0
    for p in packets:
        for ch in p["src"] + p["dst"]:
            acc = (3 * acc + int(ch)) % (3**20)
        acc = (acc + p["hops"] + 2 * p["relays"] + p["symplectic"]) % (3**20)
    return format(acc, "x")


def run_command(cmd: list[str], stdin_bytes: bytes | None, timeout: float | None):
    before = side.snapshot()
    t0 = time.perf_counter()
    proc = subprocess.run(
        cmd,
        input=stdin_bytes,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )
    elapsed = time.perf_counter() - t0
    after = side.snapshot()
    return proc, elapsed, side.delta(before, after)


def build_report(args, cmd, proc, elapsed, deltas, stdin_bytes):
    command_line = " ".join(shlex.quote(x) for x in cmd)
    genome = hashlib.sha256(
        json.dumps(
            {
                "cmd": cmd,
                "cwd": str(ROOT),
                "stdin_sha256": hashlib.sha256(stdin_bytes or b"").hexdigest(),
            },
            sort_keys=True,
        ).encode()
    ).hexdigest()
    packets = []
    packets.extend(packetize(command_line.encode(), "cmd", args.max_packets))
    packets.extend(packetize(stdin_bytes or b"", "stdin", args.max_packets))
    packets.extend(packetize(proc.stdout, "stdout", args.max_packets))
    packets.extend(packetize(proc.stderr, "stderr", args.max_packets))
    checksum = substrate_checksum(packets)
    route_bytes_saved = max(0, len(packets)) * 6
    report = {
        "command": cmd,
        "command_line": command_line,
        "returncode": proc.returncode,
        "elapsed_s": elapsed,
        "stdout_preview": proc.stdout[: args.preview_bytes].decode("utf-8", "replace"),
        "stderr_preview": proc.stderr[: args.preview_bytes].decode("utf-8", "replace"),
        "stdout_bytes": len(proc.stdout),
        "stderr_bytes": len(proc.stderr),
        "stdin_bytes": len(stdin_bytes or b""),
        "genome_sha256": genome,
        "packets": packets,
        "packet_count": len(packets),
        "max_hops": max((p["hops"] for p in packets), default=0),
        "substrate_checksum": checksum,
        "control_plane": {
            "routing_table_entries": 0,
            "routing_state_bytes": 0,
            "classical_next_hop_bits_avoided_for_packet_destinations": route_bytes_saved,
            "address_is_route": True,
        },
        "sidechannel_delta": deltas,
        "boundary": (
            "This wraps arbitrary classical execution in the Holonet control plane. It does not yet "
            "binary-translate the child process arithmetic into Holonet-native gates."
        ),
    }
    if args.optimize != "none":
        compilation = build_compilation(
            [report],
            exact_backend=args.compile_exact_backend,
            exact_time_limit_s=args.compile_time_limit,
            optimize_policy=args.optimize,
        )
        active = compilation["active_schedule"]
        native = compilation["clock_native_schedule"]
        report["holonet_compilation"] = {
            "status": compilation["status"],
            "optimizer_policy": args.optimize,
            "exact_backend": compilation["optimizer"]["exact_backend"]["status"],
            "optimality_status": compilation["optimizer"]["optimality_status"],
            "job_count": compilation["lowering"]["job_count"],
            "active_policy": {
                "ticks": active["tick_count"],
                "clock_slots": active["clock_embedding"]["clock_slot_count"],
                "connectors": active["clock_embedding"]["connector_slot_count"],
                "schedule_hash": active["schedule_hash"],
            },
            "clock_native_policy": {
                "ticks": native["tick_count"],
                "clock_slots": native["clock_slot_count"],
                "connectors": native["connector_slot_count"],
                "schedule_hash": native["schedule_hash"],
            },
            "selected_policy_schedule": compilation["optimizer"][
                "selected_policy_schedule"
            ],
            "boundary": (
                "Compilation is over the wrapper control packet DAG, not over child-process arithmetic. "
                "Use --compile-exact-backend scipy/auto only when a solver is available and the packet DAG is small."
            ),
        }
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Wrap any command in a Holonet VM control envelope."
    )
    parser.add_argument("--stdin-file", help="optional file to pass to child stdin")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--max-packets", type=int, default=64)
    parser.add_argument("--preview-bytes", type=int, default=1000)
    parser.add_argument(
        "--optimize",
        choices=["active-ticks", "clock-slots", "none"],
        default="active-ticks",
        help="compile the wrapper packet envelope under this Holonet scheduler policy",
    )
    parser.add_argument(
        "--compile-exact-backend",
        choices=["off", "auto", "scipy"],
        default="off",
        help="optional exact backend for the wrapper packet compiler",
    )
    parser.add_argument("--compile-time-limit", type=float, default=5.0)
    parser.add_argument("--out", default="data/holonet_wrap_last.json")
    parser.add_argument("cmd", nargs=argparse.REMAINDER, help="command after --")
    args = parser.parse_args(argv)
    cmd = args.cmd[1:] if args.cmd and args.cmd[0] == "--" else args.cmd
    if not cmd:
        parser.error(
            "expected a command, e.g. analysis/holonet_wrap.py -- python3 -c 'print(123)'"
        )
    stdin_bytes = None
    if args.stdin_file:
        stdin_bytes = Path(args.stdin_file).read_bytes()
    proc, elapsed, deltas = run_command(cmd, stdin_bytes, args.timeout)
    report = build_report(args, cmd, proc, elapsed, deltas, stdin_bytes)
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("HOLONET WRAP")
    print("------------")
    print(f"cmd: {report['command_line']}")
    print(f"returncode: {report['returncode']} elapsed: {report['elapsed_s']:.6f}s")
    print(f"genome: {report['genome_sha256'][:24]}...")
    print(
        f"packets: {report['packet_count']} max_hops: {report['max_hops']} checksum: {report['substrate_checksum']}"
    )
    print("control plane: address-is-route, routing table bytes = 0")
    if "holonet_compilation" in report:
        selected = report["holonet_compilation"]["selected_policy_schedule"]
        active = report["holonet_compilation"]["active_policy"]
        native = report["holonet_compilation"]["clock_native_policy"]
        print(
            "compile: "
            f"selected {selected['policy']} -> {selected['tick_count']} ticks / "
            f"{selected['clock_slot_count']} clock slots; "
            f"active {active['ticks']}/{active['clock_slots']}, "
            f"native {native['ticks']}/{native['clock_slots']}"
        )
    if report["stdout_preview"]:
        print("\nstdout preview:")
        print(report["stdout_preview"].rstrip())
    if report["stderr_preview"]:
        print("\nstderr preview:")
        print(report["stderr_preview"].rstrip())
    print(f"\nwrote {args.out}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
