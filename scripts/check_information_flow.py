#!/usr/bin/env python3
"""Prove, at the gate level, that information flows only one way.

Pass 2834.  The architectural law "support for readout, phase for execution" (parallel
track, Pass 2822) is a theorem about the mathematics: the support mask is not a
congruence for the instruction set, so a machine that stored only support could not
predict its own next state.

Nothing about that theorem constrains a netlist.  An engineer can wire the cheap 4-bit
mask back into the datapath, and the resulting machine passes simulation almost always,
because support IS preserved by most operations -- it drifts the first time a translation
fires on a register holding a 2.  That is the same failure shape as Pass 2753's folded
frame registers: correct in simulation, wrong in silicon, invisible to the testbench.

So this checks the law where it can actually be violated.  It flattens the design to
gates, builds the driver graph, and computes reachability:

    frame flops  ---->  support mask       MUST be reachable  (the readout works)
    support mask ---->  frame flops        MUST be unreachable (the diode holds)

The second direction is the point, and it is a proof rather than a convention: no naming
scheme, comment or code review establishes it, and a single accidental wire breaks it.

WARNS on the forward direction, FAILS on the reverse -- an information-flow violation is
not a candidate for review, it is a defect.  That is the one place this repo's
"warn, never block" policy does not apply, because unlike a rediscovery collision there
is no benign reading of a backward edge.

Usage:
    py -3 scripts/check_information_flow.py rtl/w33_pass2834_support_readout_diode.sv \\
        --top w33_support_readout_diode --source support_mask --sink xp,zp,xf,zf
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_yosys(script: str) -> str:
    """Run a yosys script from the repo root.  Prefers native, falls back to WSL."""
    if shutil.which("yosys"):
        return subprocess.run(["yosys", "-q", "-p", script], cwd=ROOT,
                              capture_output=True, text=True, timeout=600).stdout
    # WSL mounts are lower-case ("/mnt/c") but pathlib resolves the drive as "C:".
    # Lower-casing the drive LETTER is the whole fix -- see check_rtl_folds.py.
    drive, _, rest = str(ROOT).partition(":")
    wsl_dir = "/mnt/" + drive.lower() + rest.replace("\\", "/")
    inner = ("export PATH=$HOME/.local/bin:$HOME/.local/w33-hardware/bin:$PATH; "
             f"cd '{wsl_dir}' && yosys -q -p \"{script}\" 2>&1")
    return subprocess.run(["wsl", "-e", "bash", "-lc", inner],
                          capture_output=True, text=True, timeout=900).stdout


def build_graph(netlist: dict, top: str):
    """Directed graph on net BITS: an edge u -> v means u can influence v."""
    mod = netlist["modules"][top]
    edges = defaultdict(set)
    for cell in mod["cells"].values():
        ins, outs = [], []
        dirs = cell.get("port_directions", {})
        for port, bits in cell["connections"].items():
            d = dirs.get(port, "input")
            (outs if d == "output" else ins).extend(b for b in bits if isinstance(b, int))
        for a in ins:
            for b in outs:
                edges[a].add(b)
    return mod, edges


def bits_of(mod: dict, name: str) -> list[int]:
    for kind in ("ports", "netnames"):
        entry = mod.get(kind, {}).get(name)
        if entry:
            return [b for b in entry["bits"] if isinstance(b, int)]
    return []


def reachable(edges, seeds: list[int]) -> set[int]:
    seen, q = set(seeds), deque(seeds)
    while q:
        u = q.popleft()
        for v in edges.get(u, ()):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return seen


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source_file")
    ap.add_argument("--top", required=True)
    ap.add_argument("--source", required=True,
                    help="net that must NOT reach the sinks (comma separated)")
    ap.add_argument("--sink", required=True, help="comma-separated sink nets")
    ap.add_argument("--extra", default="", help="extra .sv files, comma separated")
    args = ap.parse_args(argv)

    files = " ".join([args.source_file] + [f for f in args.extra.split(",") if f])
    out = ROOT / "data" / f"_flow_{args.top}.json"
    out.parent.mkdir(exist_ok=True)
    rel = out.relative_to(ROOT).as_posix()
    script = (f"read_verilog -sv {files}; hierarchy -top {args.top}; proc; flatten; "
              f"opt -full; clean -purge; write_json {rel}")
    log = run_yosys(script)
    if not out.exists():
        err = next((l for l in log.splitlines() if "ERROR" in l), "no netlist written")
        print(f"check_information_flow: SYNTHESIS FAILED -- {err.strip()[:120]}")
        return 1

    netlist = json.loads(out.read_text(encoding="utf-8"))
    if args.top not in netlist["modules"]:
        print(f"check_information_flow: top {args.top!r} not in the netlist")
        return 1
    mod, edges = build_graph(netlist, args.top)

    srcs = [b for n in args.source.split(",") for b in bits_of(mod, n.strip())]
    sinks = {n.strip(): bits_of(mod, n.strip()) for n in args.sink.split(",")}
    if not srcs:
        print(f"check_information_flow: source {args.source!r} has no bits; "
              f"cannot prove anything")
        return 1

    print(f"top {args.top}: {len(mod['cells'])} cells after flatten+opt")
    print(f"source {args.source!r}: {len(srcs)} bit(s)")

    fwd = reachable(edges, srcs)
    bad = {n: sorted(set(b) & fwd) for n, b in sinks.items() if set(b) & fwd}

    # the intended direction, checked so the guard cannot pass vacuously
    back_ok = {}
    for n, b in sinks.items():
        if not b:
            continue
        back_ok[n] = bool(set(srcs) & reachable(edges, b))

    print("\nreverse direction (must be EMPTY):")
    if bad:
        for n, bits in bad.items():
            print(f"  VIOLATION: {args.source} reaches {n} at bits {bits}")
    else:
        print(f"  clean -- {args.source} reaches none of {', '.join(sinks)}")

    print("\nforward direction (must be non-empty, else the readout is dead):")
    for n, ok in back_ok.items():
        mark = "ok" if ok else "DEAD"
        print(f"  {n} -> {args.source}: {mark}")

    dead = [n for n, ok in back_ok.items() if not ok]
    if bad:
        print("\nFAIL: information flows backward.  This is a defect, not a review item.")
        return 1
    if dead:
        print(f"\nWARNING: the readout never sees {', '.join(dead)} -- a diode that "
              f"conducts nowhere passes the reverse test vacuously.")
    else:
        print("\nPASS: the readout is a diode -- state reaches the mask, the mask "
              "reaches no state.")
    out.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
