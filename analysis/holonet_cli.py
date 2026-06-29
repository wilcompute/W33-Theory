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


def cmd_verify(args):
    checks = []
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
    pb.set_defaults(func=cmd_bench)
    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
