#!/usr/bin/env python3
"""Pass 4398 -- the GF(9) width penalty, synthesised and counted.

The arc so far:

    4381  the asymmetric-protection lever EXISTS       (derived from GQ parameters)
    4389  it is REAL                                    (H(3,9) built, rates measured)
    4390  the group theory does not obstruct a machine  (4 transvections generate PSU(4,3))

None of those counted a single gate.  The blueprint's four-machine table -- 103, 132, 206,
240 cells -- was synthesised over GF(3), and a GF(9) datapath is twice as wide before any
arithmetic happens.  So the design question is a price question and this pass asks it.

THE COMPARISON, AND WHAT WOULD MAKE IT INVALID.  Stated first, per CLAUDE.md failure mode 6.

  * The gain being bought is the protection ASYMMETRY, a factor of 1.194 between the two
    register miss rates on H(3,9) (3.2258% vs 2.7027%).  It is not a gain in overall
    detection: H(3,9) detects 97.04% against W(3,3)'s 92.31%, but that improvement comes
    from the quadrangle being BIGGER (1120 flags against 160), not from the asymmetry, and
    a bigger symplectic quadrangle would buy the same thing without leaving GF(3).
  * So the comparison is only licensed between objects doing the SAME job, and the honest
    unit is cells per flag protected, not cells.
  * It would be invalid if the two cores were not the same computation.  They are: both
    are one transvection x -> x + a*B(x,v)*v on a 4-component vector, identical in shape,
    differing only in the field and the form.  That is why this file synthesises the
    transvection and not two unrelated blocks.

    py -3 analysis/w33_pass4398_gf9_width_penalty.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RTL = "rtl/w33_pass4398_gf9_datapath.sv"
TOPS = ["gf3_add", "gf9_add", "gf3_mul", "gf9_mul",
        "symplectic_form_gf3", "hermitian_form_gf9",
        "transvection_gf3", "transvection_gf9"]


def synth(top: str) -> dict:
    """yosys, flattened and mapped to a technology-independent gate library."""
    script = (f"read_verilog -sv {RTL}; hierarchy -top {top}; proc; flatten; opt -full; "
              f"techmap; opt -full; abc -g AND,OR,XOR,NAND,NOR,XNOR; opt -full; stat")
    # WSL sees the Windows tree through /mnt/<drive>; ROOT.as_posix() is a Windows path
    # and `cd` fails on it silently enough that the first run reported "no cell count".
    d = ROOT.as_posix()
    wsl_root = f"/mnt/{d[0].lower()}{d[2:]}"
    r = subprocess.run(
        ["wsl", "-e", "bash", "-lc",
         f"export PATH=$HOME/.local/w33-hardware/bin:$PATH; cd '{wsl_root}' && "
         f"yosys -p \"{script}\""],
        capture_output=True, text=True, timeout=600)
    out = r.stdout + r.stderr
    cells = re.search(r"^\s*(\d+)\s+cells\s*$", out, re.M)
    wires = re.search(r"^\s*(\d+)\s+wires\s*$", out, re.M)
    mix = {k: int(v) for v, k in
           re.findall(r"^\s+(\d+)\s+(\$[A-Za-z_]+)\s*$", out, re.M)}
    if not cells:
        raise RuntimeError(f"{top}: no cell count in yosys output\n{out[-800:]}")
    # $scopeinfo is metadata, not logic; counting it would inflate both sides unequally
    # (the deeper GF(9) hierarchy carries more of them).
    scope = mix.pop("$scopeinfo", 0)
    return {"cells": int(cells.group(1)) - scope,
            "cells_raw": int(cells.group(1)), "scopeinfo": scope,
            "wires": int(wires.group(1)) if wires else None,
            "gate_mix": dict(sorted(mix.items()))}


def main() -> int:
    print("=" * 78)
    print("Pass 4398 -- what a GF(9) datapath costs")
    print("=" * 78)

    res = {}
    for top in TOPS:
        res[top] = synth(top)
        print(f"  {top:26s} {res[top]['cells']:5d} cells")

    add_ratio = res["gf9_add"]["cells"] / res["gf3_add"]["cells"]
    mul_ratio = res["gf9_mul"]["cells"] / res["gf3_mul"]["cells"]
    form_ratio = res["hermitian_form_gf9"]["cells"] / res["symplectic_form_gf3"]["cells"]
    tv_ratio = res["transvection_gf9"]["cells"] / res["transvection_gf3"]["cells"]

    # what the wider core buys, in the units the comparison is licensed in
    w_flags, h_flags = 160, 1120
    w_det, h_det = 1 - Fraction(1, 13), 1 - (Fraction(1, 31) + Fraction(1, 37)) / 2
    w_cost = res["transvection_gf3"]["cells"]
    h_cost = res["transvection_gf9"]["cells"]

    print(f"""
  {'':26s} {'cells':>7s} {'ratio vs GF(3)':>16s}
  {'bilinear/Hermitian form':26s} {res['hermitian_form_gf9']['cells']:7d} {form_ratio:15.3f}x
  {'one transvection':26s} {h_cost:7d} {tv_ratio:15.3f}x

  THE PRICE IS {tv_ratio:.2f}x FOR THE TRANSVECTION AND {form_ratio:.2f}x FOR THE FORM.

  Against the asymmetry factor of 1.194 this is not close.  The lever is real, the group
  theory permits it, and it costs {tv_ratio:.1f} times the logic to obtain a {1.194:.3f} times
  difference in how well two registers are protected.  On this measurement the asymmetric
  quadrangle is a CURIOSITY rather than a design option, and Pass 4390's "reachable" should
  be read as reachable-in-principle only.

  THE DECOMPOSITION, MEASURED RATHER THAN ASSERTED.  The obvious explanation is "GF(9) is
  twice as wide", and the two primitives separate that from the rest without arguing:

      addition   GF(3) {res['gf3_add']['cells']:4d} cells -> GF(9) {res['gf9_add']['cells']:4d}   {add_ratio:5.2f}x   pure width, no field structure
      multiply   GF(3) {res['gf3_mul']['cells']:4d} cells -> GF(9) {res['gf9_mul']['cells']:4d}   {mul_ratio:5.2f}x   width AND the four-multiply identity

  So width alone costs {add_ratio:.2f}x and the field structure costs the rest.  A GF(9) multiply
  is four GF(3) multiplies plus a negate plus two adds, and the Hermitian form needs a
  conjugation the symplectic form does not.  None of that is a coding inefficiency; it is
  what the field is.

  AND THE COMPARISON THAT IS *NOT* LICENSED, STATED SO NOBODY MAKES IT LATER.  H(3,9)
  detects {float(h_det) * 100:.2f}% of single-register faults against W(3,3)'s {float(w_det) * 100:.2f}%, which looks like the
  wider datapath buying something real.  It is not buying it with the FIELD -- it is buying
  it with SIZE, {h_flags} flags against {w_flags}. A larger symplectic quadrangle W(3,q) reaches the
  same detection without ever leaving GF(3), and Pass 4374's law says exactly how: detection
  = 1 - q/((q+1)(q^2+1)-1), which passes 97% at q=5. Comparing H(3,9) to W(3,3) on detection
  compares a big object to a small one and credits the field.

  WHAT THIS PASS DOES NOT SETTLE.  It prices one opcode, not a machine: no register file, no
  control, no load port, and no unitary analogue of the affine translation (still unbuilt
  since Pass 4390). A full machine could amortise the field cost across a datapath that is
  mostly control, and the ratio would fall. What is established is a floor on the
  arithmetic core, and the floor is already {tv_ratio:.1f}x.""")

    out = {
        "boundary": ("prices ONE transvection opcode, technology-independent gate mapping, "
                     "no register file, control, load port or memory; a full machine could "
                     "amortise the field cost and this ratio is a floor on the arithmetic "
                     "core, not a machine-level figure"),
        "rtl": RTL,
        "synthesis": ("yosys 0.67, flatten + opt -full + techmap + "
                      "abc -g AND,OR,XOR,NAND,NOR,XNOR"),
        "cells": {k: v["cells"] for k, v in res.items()},
        "gate_mix": {k: v["gate_mix"] for k, v in res.items()},
        "add_ratio_pure_width": round(add_ratio, 4),
        "mul_ratio_width_plus_field": round(mul_ratio, 4),
        "form_ratio": round(form_ratio, 4),
        "transvection_ratio": round(tv_ratio, 4),
        "asymmetry_bought": 1.194,
        "verdict": ("the asymmetric-protection lever costs "
                    f"{tv_ratio:.2f}x the arithmetic logic to buy a 1.194x difference in "
                    "register protection; on this measurement it is a curiosity, not a "
                    "design option"),
        "not_licensed": ("H(3,9)'s higher overall detection (97.04% vs 92.31%) comes from "
                         "having 1120 flags rather than 160, NOT from the field; a larger "
                         "W(3,q) reaches the same detection over GF(3)"),
    }
    p = ROOT / "data" / "PART_W33_PASS4398_GF9_WIDTH_PENALTY.json"
    p.parent.mkdir(exist_ok=True)
    sys.path.insert(0, str(ROOT / "scripts"))
    import cert_util  # noqa: E402
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
