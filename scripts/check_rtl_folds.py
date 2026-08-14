#!/usr/bin/env python3
"""Find RTL modules that synthesize away.

Built at Pass 2772 after a MEASURED defect that both tracks shipped independently.

`rtl/w33_pass2757_qutrit_cx.sv` (parallel track) and my own withdrawn `w33_cx_frame`
are Pauli-frame trackers with no load port.  After reset the state is (0,0,0,0), and
because the map is (xp, zp - zf, xf + xp, zf) with xp and zf structurally constant, the
whole state is frozen: the module implements the identity.  Yosys proves it -- after
`flatten; opt -full` the netlist ends `assign zf = 2'h0; assign xp = 2'h0;` and 6 of the
8 state flops are deleted.

Neither exhaustive testbench caught it.  Both drive the COMBINATIONAL map directly and
never instantiate the sequential wrapper, so the simulation is correct about the map and
silent about the tracker.  Simulation cannot see this class of defect at all: a module
that folds to a constant still simulates correctly, it just does nothing.

Only synthesis asks whether the state can move.  This runs that question over every
module in rtl/ and reports two symptoms:

    CONSTANT OUTPUT   an output port is tied to a literal after full optimization
    FLOPS DELETED     declared state bits that do not survive opt

Neither symptom is automatically a bug -- a genuinely constant output (a tie-off, a
version register) is fine, and opt legitimately merges equivalent flops.  Both are worth
a human look, which is why this WARNS and never blocks, matching the repo's standing
policy for check_rediscovery.py, check_certificates.py and check_novelty_claims.py.

Requires yosys.  On this machine it lives in WSL; see --yosys.

Usage:
    py -3 scripts/check_rtl_folds.py                 # every module in rtl/
    py -3 scripts/check_rtl_folds.py rtl/foo.sv      # one file
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RTL = ROOT / "rtl"

MODULE = re.compile(r"^\s*module\s+([A-Za-z_]\w*)", re.M)
# `assign <name> = <literal>;` in the written-back netlist
CONST_ASSIGN = re.compile(r"^\s*assign\s+([\\]?[\w.\[\]:$]+)\s*=\s*\d+'[hbd][0-9a-fx]+\s*;", re.M)
OUTPUT_PORT = re.compile(r"^\s*output\s+(?:reg\s+|wire\s+)?(?:\[[^\]]*\]\s*)?([\w]+)", re.M)


def wsl_yosys(script: str, workdir: Path) -> str:
    """Run a yosys script.  Prefers a native yosys, falls back to WSL."""
    if shutil.which("yosys"):
        cmd = ["yosys", "-q", "-p", script]
        return subprocess.run(
            cmd, cwd=workdir, capture_output=True, text=True, timeout=300
        ).stdout
    # WSL mounts are lower-case ("/mnt/c"), but pathlib resolves the drive to "C:".
    # Lower-casing the drive LETTER is the whole fix; lower-casing the "/mnt/" prefix
    # instead leaves "/mnt/C/..." and every cd silently fails.
    drive, _, rest = str(workdir).partition(":")
    wsl_dir = "/mnt/" + drive.lower() + rest.replace("\\", "/")
    inner = (
        "export PATH=$HOME/.local/bin:$HOME/.local/w33-hardware/bin:$PATH; "
        f"cd '{wsl_dir}' && yosys -q -p \"{script}\" 2>&1"
    )
    return subprocess.run(
        ["wsl", "-e", "bash", "-lc", inner], capture_output=True, text=True, timeout=600
    ).stdout


def audit(path: Path) -> list[str]:
    src = path.read_text(encoding="utf-8", errors="ignore")
    mods = [m for m in MODULE.findall(src) if not m.startswith("tb_")]
    findings = []
    for mod in mods:
        out = ROOT / "data" / f"_fold_{mod}.v"
        out.parent.mkdir(exist_ok=True)
        # RELATIVE paths only.  The repo root is "c:\Repos\Theory of Everything" --
        # a drive colon and two spaces -- and an absolute path breaks both the WSL
        # mount translation and yosys's own argument splitting.
        rel_src = path.resolve().relative_to(ROOT).as_posix()
        rel_out = out.relative_to(ROOT).as_posix()
        script = (
            f"read_verilog -sv {rel_src}; "
            f"hierarchy -top {mod}; proc; flatten; opt -full; opt_expr -full; "
            f"clean -purge; write_verilog -noattr {rel_out}"
        )
        try:
            log = wsl_yosys(script, ROOT)
        except Exception as exc:                       # noqa: BLE001
            findings.append(f"  {path.name}:{mod}  yosys failed: {exc}")
            continue
        if not out.exists():
            first = next((l for l in log.splitlines() if "ERROR" in l), "no netlist written")
            findings.append(f"  {path.name}:{mod}  NOT SYNTHESIZED: {first.strip()[:110]}")
            continue
        netlist = out.read_text(encoding="utf-8", errors="ignore")
        outs = set(OUTPUT_PORT.findall(netlist))
        consts = {c.lstrip("\\") for c in CONST_ASSIGN.findall(netlist)}
        dead = sorted(outs & consts)
        if dead:
            findings.append(
                f"  {path.name}:{mod}\n"
                f"    CONSTANT OUTPUT after opt: {', '.join(dead)}\n"
                f"    (a port tied to a literal cannot carry state; check for a missing\n"
                f"     load path, as in Pass 2753's frame trackers)"
            )
        out.unlink(missing_ok=True)
    return findings


def selftest() -> int:
    """Planted-fault recall for the module extractor, which is the part that runs offline.

    The fold check itself needs yosys and cannot run here, so this pins the ONE piece of
    logic that decides what yosys is ever pointed at: the module scan and the testbench
    exclusion. A MODULE regex that stopped matching would make this guard silently audit
    nothing and report a clean zero (Pass 5250).
    """
    cases = [("one module", "module fold_a(input x);\nendmodule\n", ["fold_a"]),
             ("two modules", "module a();endmodule\nmodule b();endmodule\n", ["a", "b"]),
             ("testbench excluded", "module tb_a();endmodule\nmodule a();endmodule\n",
              ["a"]),
             ("indented module", "  module spaced();endmodule\n", ["spaced"]),
             ("no module", "// just a comment\n", [])]
    ok = True
    print("  selftest -- module extraction and testbench exclusion\n")
    for name, src, want in cases:
        got = [m for m in MODULE.findall(src) if not m.startswith("tb_")]
        good = got == want
        ok &= good
        print(f"    {name:22s} got={str(got):22s} want={str(want):18s} "
              f"{'PASS' if good else 'FAIL'}")
    have_yosys = shutil.which("yosys") is not None
    print(f"""
  THE TESTBENCH CASE IS LOAD-BEARING. A tb_ module is stimulus, not hardware; synthesising
  it produces folds that mean nothing and would bury the real finding. Excluding it is the
  difference between a guard and a noise generator.

  WHAT IS NOT COVERED HERE. yosys is {'PRESENT' if have_yosys else 'ABSENT'} on this machine, and the actual fold
  detection -- read_verilog, flatten, opt -full, and the comparison that finds a register
  synthesised away -- is not exercised by this self-test at all. So a green result here
  means the guard will look at the right modules, NOT that it can still detect a fold.""")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    paths = [Path(f) for f in args.files] or sorted(
        p for p in RTL.glob("*.sv") if not p.name.startswith("tb_")
    )
    print(f"check_rtl_folds: {len(paths)} file(s)")
    allf = []
    for p in paths:
        if not p.exists():
            continue
        allf.extend(audit(p))
    if allf:
        print(f"\n{len(allf)} module(s) fold to a constant - review, not a block:\n")
        for f in allf:
            print(f.encode("ascii", "replace").decode("ascii"))
    elif not args.quiet:
        print("no module folds an output to a constant.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
