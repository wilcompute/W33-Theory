#!/usr/bin/env python3
"""
holonet -- the universal VM as a command-line tool. One executable that exposes the whole architecture
as subcommands you can run: route a packet, teleport a state, correct an error, reproduce a node, verify
the whole stack, or print the datasheet. It is a thin command-line front end over holonet_node.py (the
runnable node): the network, processor, memory, and self-reproduction the papers describe, packaged as
a tool anyone can install and run on any computer. The point is the same as the node's -- the
architecture is classically emulable, so this CLI runs the entire machine (everything but the priced
9^t quantum-advantage dial) on ordinary hardware.

Usage:
    py -3 analysis/holonet_cli.py route 0001 0010      # route a packet (address is the route)
    py -3 analysis/holonet_cli.py teleport             # teleport a random qutrit A->B
    py -3 analysis/holonet_cli.py correct              # run a [[5,1,3]]_3 error-correction cycle
    py -3 analysis/holonet_cli.py reproduce            # splice a W(3,3) child (self-reproduction)
    py -3 analysis/holonet_cli.py verify               # self-test the whole stack -> PASS/FAIL
    py -3 analysis/holonet_cli.py info                 # print the datasheet

Honest scope: a CLI wrapper over the holonet_node VM; the routing and Clifford layer are exact and
classical, the QEC and teleportation are exact small state-vector simulations, the quantum advantage is
not run (the priced 9^t dial). So: the universal VM, as a tool.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import holonet_node as hn  # noqa: E402


def parse_addr(s):
    """Parse an address like '0001' or '0,0,0,1' into a normalized W(3,3) point."""
    digits = s.split(",") if "," in s else list(s)
    v = tuple(int(d) % 3 for d in digits)
    if len(v) != 4 or not any(v):
        raise SystemExit(f"bad address {s!r}: need 4 base-3 digits, not all zero")
    p = hn._norm(v)
    if p not in hn.POINTS:
        raise SystemExit(f"address {s!r} is not a valid W(3,3) point")
    return p


def cmd_route(args):
    a, b = parse_addr(args.src), parse_addr(args.dst)
    path = hn.route(a, b)
    hops = len(path) - 1
    print(f"route {a} -> {b}:  {' -> '.join(str(p) for p in path)}")
    print(
        f"  {hops} hop{'s' if hops != 1 else ''} (address is the route; symplectic test, no table)"
    )
    if hops == 2:
        mp = hn.multipath(a, b)
        print(
            f"  mu = {len(mp)} internally-disjoint relays available (four-way multipath)"
        )


def cmd_teleport(args):
    r = hn.teleport_state(seed=args.seed)
    print(
        f"teleport A -> B:  outcome (k,l)={r['outcome']}, correction X^{r['outcome'][0]}Z^{r['outcome'][1]}"
    )
    print(
        f"  recovered fidelity = {r['fidelity']:.6f}  (message destroyed at A by no-cloning)"
    )


def cmd_correct(args):
    r = hn.qec_cycle(seed=args.seed)
    print(
        f"correct [[5,1,3]]_3:  injected error {r['injected']}, decoded {r['decoded']}"
    )
    print(
        f"  recovery fidelity = {r['fidelity']:.6f}  (one logical qutrit, distance-3 single-error correction)"
    )


def cmd_reproduce(args):
    node = hn.HolonetNode(hn.POINTS[0])
    child = node.reproduce()
    print(f"reproduce:  node {node.address} (level {node.level}) spliced a child")
    print(
        f"  -> {child.address} (level {child.level}, diameter {8 * child.level}); von Neumann self-reproduction"
    )


def cmd_info(args):
    print("HOLONET datasheet (the substrate as a computer):")
    rows = [
        (
            "processor",
            "balanced ternary; word 27=3^3; ISA Sp(4,3)=51840=|W(E6)| + 1 cubic magic",
        ),
        (
            "interconnect",
            f"GQ(3,3): {len(hn.POINTS)} nodes, radix 12, diameter 2, bisection 100, 11-fault",
        ),
        (
            "memory",
            "[[66,8,3]]_3 qutrit surface code, distance 3 (corrects 1 fault/cycle)",
        ),
        ("clock", "golden-ratio quasicrystal, three-gap bounded jitter, beat 30"),
        ("consensus", "leaderless, 1/3-per-round, 5-Byzantine / 11-crash"),
        ("magic", "robustness 3, mana ln(5/3); classical emulation cost 9^t"),
        (
            "contextuality",
            "fraction 1/10 (state-independent KS; classical S<=36 vs quantum 40)",
        ),
    ]
    for k, v in rows:
        print(f"  {k:14s}: {v}")


def cmd_audit(args):
    """Re-verify every architectural layer from q=3 in one pass/fail ledger."""
    import w33_master_audit  # noqa: E402

    checks, all_ok = w33_master_audit.run_audit()
    print("holonet audit -- re-deriving the whole datasheet from q=3:")
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")
    print(
        f"\n{'ALL PASS -- the whole datasheet re-derives from q=3.' if all_ok else 'FAILURES present.'}"
    )
    sys.exit(0 if all_ok else 1)


def cmd_bench(args):
    """Time the classical machine: deterministic op counts + host-relative throughput."""
    import holonet_bench  # noqa: E402

    if getattr(args, "compare", False) and getattr(args, "scale", False):
        ledger, ok = holonet_bench.run_compare_scale()
        holonet_bench._print_compare_scale(ledger)
        if getattr(args, "plot", False):
            try:
                p = holonet_bench.plot_compare_scale(ledger)
                print(f"\nwrote {p}")
            except Exception as e:
                print(f"\n(plot skipped: {e})")
        print(
            f"\n{'OK -- baseline routing state diverges with q; Holonet stays 0 bytes / 2 hops.' if ok else 'FAILURES present.'}"
        )
        sys.exit(0 if ok else 1)
    if getattr(args, "compare", False):
        ledger, ok = holonet_bench.run_compare()
        holonet_bench._print_compare(ledger)
        print(
            f"\n{'OK -- table-free routing verified equivalent; 0 bytes of routing state.' if ok else 'FAILURES present.'}"
        )
        sys.exit(0 if ok else 1)

    ledger, ok = holonet_bench.run_bench()
    print("holonet bench -- deterministic op counts (same on any machine):")
    for k, v in ledger["deterministic_op_counts"].items():
        print(f"  {k:32s}: {v}")
    print("host-relative throughput (THIS machine):")
    for k, v in ledger["host_relative_throughput"].items():
        if v:
            print(f"  {k:32s}: {v:12.0f} /s")
    print(
        f"\n{'OK -- op counts forced by geometry; times host-relative.' if ok else 'FAILURES present.'}"
    )
    sys.exit(0 if ok else 1)


def cmd_uor(args):
    """Run the Holonet-UOR bridge demo path."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    py = sys.executable
    venv_py_bin = os.path.join(root, ".venv", "bin", "python")
    venv_py_scripts = os.path.join(root, ".venv", "Scripts", "python.exe")

    def is_valid_venv(path):
        if not os.path.exists(path):
            return False
        # On Windows, check if pyvenv.cfg points to a Linux path (WSL venv)
        cfg = os.path.join(os.path.dirname(os.path.dirname(path)), "pyvenv.cfg")
        if os.path.exists(cfg):
            try:
                with open(cfg, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "home = /usr/bin" in content or "home = /bin" in content:
                        return False
            except Exception:
                pass
        return True

    if sys.platform == "win32":
        compiler_py = venv_py_scripts if is_valid_venv(venv_py_scripts) else py
    else:
        compiler_py = venv_py_bin if is_valid_venv(venv_py_bin) else py

    commands = [
        [
            py,
            "analysis/holonet_uor_certificate.py",
            "--input",
            "data/holonet_wrap_demo_factorial.json",
            "--out",
            "data/holonet_uor_certificate.json",
        ],
        [
            py,
            "analysis/holonet_uor_certificate.py",
            "--input",
            "data/holonet_wrap_rule110_demo.json",
            "--out",
            "data/holonet_uor_rule110_certificate.json",
        ],
        [
            py,
            "analysis/holonet_uor_live_adapter.py",
            "--out",
            "data/holonet_uor_live_adapter_plan.json",
        ],
        [
            py,
            "analysis/holonet_uor_submitter.py",
            "--out",
            "data/holonet_uor_submitter_report.json",
        ],
        [
            py,
            "analysis/holonet_uor_mock_runtime.py",
            "--out",
            "data/holonet_uor_mock_runtime_report.json",
        ],
        [py, "analysis/w33_uor_runtime_model.py"],
        [
            py,
            "analysis/w33_uor_spread_scheduler.py",
            "--out",
            "data/w33_uor_spread_scheduler.json",
        ],
        [
            py,
            "analysis/holonet_os_scheduler.py",
            "--out",
            "data/holonet_os_scheduler_trace.json",
        ],
        [
            py,
            "analysis/w33_spread_contextual_microkernel_bridge.py",
            "--out",
            "data/w33_spread_contextual_microkernel_bridge.json",
        ],
        [
            compiler_py,
            "analysis/w33_line_context_compiler.py",
            "--exact-backend",
            "auto",
            "--exact-time-limit",
            "120",
            "--out",
            "data/w33_line_context_compiler.json",
        ],
        [
            py,
            "analysis/w33_defect_spread_tensor.py",
            "--out",
            "data/w33_defect_spread_tensor.json",
        ],
        [
            py,
            "analysis/w33_spread_clock_graph.py",
            "--out",
            "data/w33_spread_clock_graph.json",
        ],
        [
            py,
            "analysis/w33_clock_policy_stress.py",
            "--out",
            "data/w33_clock_policy_stress.json",
        ],
        [
            py,
            "analysis/w33_packet_latency_benchmark.py",
            "--out",
            "data/w33_packet_latency_benchmark.json",
        ],
        [py, "analysis/w33_uor_holonomy_shadow_api_bridge.py"],
        [
            py,
            "analysis/w33_uor_holonomy_live_probe.py",
            "--out",
            "data/w33_uor_holonomy_live_probe.json",
        ],
        [
            py,
            "analysis/holonet_uor_shacl_shape_check.py",
            "--out",
            "data/holonet_uor_shacl_shape_report.json",
        ],
        [py, "analysis/holonet_uor_shacl_export.py"],
        [py, "analysis/holonet_uor_browser_demo.py"],
    ]

    def insert_before_output(script_name, flag):
        for command in commands:
            if len(command) > 1 and command[1].endswith(script_name):
                command.insert(-2, flag)
                return
        raise RuntimeError(f"could not find {script_name} in UOR command list")

    if args.live:
        insert_before_output("holonet_uor_live_adapter.py", "--probe-live")
        insert_before_output("holonet_uor_submitter.py", "--live")
        insert_before_output("w33_uor_holonomy_live_probe.py", "--live")
        insert_before_output("holonet_uor_shacl_shape_check.py", "--live")

    print("holonet uor -- content-addressed VM certificate and OS replay", flush=True)
    for index, command in enumerate(commands, start=1):
        label = " ".join(command[1:])
        print(f"\n[{index:02d}/{len(commands):02d}] {label}", flush=True)
        proc = subprocess.run(command, cwd=root, check=False)
        if proc.returncode != 0:
            print(f"\nFAIL: command exited {proc.returncode}")
            sys.exit(proc.returncode)
    print("\nALL PASS -- Holonet-UOR bridge demo artifacts regenerated.")
    print("  browser replay: docs/holonet_uor_os_replay.html")
    print("  SHACL export:   docs/holonet_uor_certificate_shapes.ttl")
    print("  line compiler:  data/w33_line_context_compiler.json")
    print("  defect tensor:  data/w33_defect_spread_tensor.json")
    print("  clock graph:    data/w33_spread_clock_graph.json")
    print("  clock stress:   data/w33_clock_policy_stress.json")
    print("  packet latency: data/w33_packet_latency_benchmark.json")


def cmd_verify(args):
    checks = []
    # realization / minimal substrate
    import w33_realization_dimension

    checks.append(
        (
            "minimal substrate: q=2 impossible",
            w33_realization_dimension.verify_q2_obstruction(),
        )
    )
    checks.append(
        (
            "minimal substrate: q=3 Witting exists",
            w33_realization_dimension.verify_witting_existence(),
        )
    )
    # network
    a = hn.POINTS[0]
    dst = next(p for p in hn.POINTS if hn.symplectic(a, p) != 0)
    checks.append(
        (
            "network: 40 nodes, radix 12",
            len(hn.POINTS) == 40 and len(hn.neighbors(a)) == 12,
        )
    )
    checks.append(("network: diameter-2 route", len(hn.route(a, dst)) == 3))
    checks.append(("network: mu=4 multipath", len(hn.multipath(a, dst)) == 4))
    # processor
    reg = hn.CliffordRegister(2)
    reg.fourier(0)
    reg.sum(0, 1)
    checks.append(("processor: valid Clifford state", reg.is_valid_state()))
    # memory / correct
    qc = hn.qec_cycle(seed=0)
    checks.append(("memory: [[5,1,3]]_3 corrects error", qc["fidelity"] > 0.999999))
    # teleport
    tp = hn.teleport_state(seed=0)
    checks.append(("teleport: fidelity 1", tp["fidelity"] > 0.999999))
    # reproduce
    child = hn.HolonetNode(a).reproduce()
    checks.append(("reproduce: child spliced", child.level == 2))
    print("holonet verify -- self-testing the whole stack:")
    allok = True
    for name, ok in checks:
        allok = allok and ok
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")
    print(
        f"\n{'ALL PASS -- this machine is a working holonet node.' if allok else 'FAILURES present.'}"
    )
    sys.exit(0 if allok else 1)


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="holonet", description="The universal VM as a command-line tool."
    )
    sub = p.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("route", help="route a packet between two addresses")
    pr.add_argument("src")
    pr.add_argument("dst")
    pr.set_defaults(func=cmd_route)
    pt = sub.add_parser("teleport", help="teleport a random qutrit A->B")
    pt.add_argument("--seed", type=int, default=0)
    pt.set_defaults(func=cmd_teleport)
    pc = sub.add_parser("correct", help="run a [[5,1,3]]_3 error-correction cycle")
    pc.add_argument("--seed", type=int, default=0)
    pc.set_defaults(func=cmd_correct)
    prp = sub.add_parser("reproduce", help="splice a W(3,3) child (self-reproduction)")
    prp.set_defaults(func=cmd_reproduce)
    sub.add_parser("info", help="print the datasheet").set_defaults(func=cmd_info)
    sub.add_parser(
        "verify", help="self-test the whole stack -> PASS/FAIL"
    ).set_defaults(func=cmd_verify)
    sub.add_parser(
        "audit", help="re-derive every layer's headline constant from q=3 -> PASS/FAIL"
    ).set_defaults(func=cmd_audit)
    pb = sub.add_parser(
        "bench",
        help="time the classical machine -> op counts + host-relative throughput",
    )
    pb.add_argument(
        "--compare",
        action="store_true",
        help="compare table-free address routing against a classical table-routed baseline",
    )
    pb.add_argument(
        "--scale",
        action="store_true",
        help="with --compare: tabulate how the routing-state win grows with fabric order q",
    )
    pb.add_argument(
        "--plot",
        action="store_true",
        help="with --compare --scale: also write the divergence figure docs/holonet_scale.png",
    )
    pb.set_defaults(func=cmd_bench)
    pu = sub.add_parser(
        "uor",
        help="run the Holonet-UOR bridge demo, mock runtime, OS replay, and shapes",
    )
    pu.add_argument(
        "--live",
        action="store_true",
        help="also run bounded live UOR probes for accepted public endpoints",
    )
    pu.set_defaults(func=cmd_uor)
    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
