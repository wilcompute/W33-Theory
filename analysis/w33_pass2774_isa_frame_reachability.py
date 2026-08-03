#!/usr/bin/env python3
"""Pass 2774 -- which Pauli frames can the Holonet ISA actually reach?

The Pass 2753 defect was stated as "an output folds to a constant".  That is the
SYMPTOM.  The property underneath it is reachability: starting from the reset frame
(0,0,0,0), which of the 81 frames can the instruction set drive the machine into?  A
module whose reachable set is {0} synthesizes to the identity, which is how yosys found
it -- but reachability is the statement worth checking, because it is exact, it is
independent of any synthesis tool, and it distinguishes the two modules that look alike.

Two modules implement the same CX map and differ entirely on this question:

    rtl/w33_pass2757_qutrit_cx.sv   w33_qutrit_cx_frame     CX only, no load port
    rtl/w33_pass2762_holonet_isa.sv w33_pass2762_holonet_isa six frame opcodes

The first is a pure symplectic action, and every symplectic map fixes the origin, so its
reachable set from reset is exactly {(0,0,0,0)} -- no sequence of CX pulses can ever move
it.  The second includes opcode 101 (sigma^5 = Z), which INCREMENTS a Z component: an
affine translation, not a linear map.  That one non-linear instruction is what makes the
whole frame space reachable.

This computes both, exactly, by breadth-first search over F_3^4.

    py -3 analysis/w33_pass2774_isa_frame_reachability.py
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def neg(v: int) -> int:
    return (-v) % 3


# The six frame-moving opcodes, transcribed from w33_pass2762_frame_step.
# Each maps (xp, zp, xf, zf) -> (xp, zp, xf, zf).
def op_fp(s):                       # 000  F_p
    xp, zp, xf, zf = s
    return (neg(zp), xp, xf, zf)


def op_ff(s):                       # 001  F_f
    xp, zp, xf, zf = s
    return (xp, zp, neg(zf), xf)


def op_sp(s):                       # 010  S_p
    xp, zp, xf, zf = s
    return (xp, (zp + xp) % 3, xf, zf)


def op_sf(s):                       # 011  S_f
    xp, zp, xf, zf = s
    return (xp, zp, xf, (zf + xf) % 3)


def op_cx_pf(s):                    # 100  CX, direction 0
    xp, zp, xf, zf = s
    return (xp, (zp - zf) % 3, (xf + xp) % 3, zf)


def op_cx_fp(s):                    # 100  CX, direction 1
    xp, zp, xf, zf = s
    return ((xp + xf) % 3, zp, xf, (zf - zp) % 3)


def op_z_p(s):                      # 101  sigma^5 = Z, register 0
    xp, zp, xf, zf = s
    return (xp, (zp + 1) % 3, xf, zf)


def op_z_f(s):                      # 101  sigma^5 = Z, register 1
    xp, zp, xf, zf = s
    return (xp, zp, xf, (zf + 1) % 3)


SYMPLECTIC = [op_fp, op_ff, op_sp, op_sf, op_cx_pf, op_cx_fp]
TRANSLATION = [op_z_p, op_z_f]
START = (0, 0, 0, 0)


def reachable(ops) -> set:
    seen = {START}
    q = deque([START])
    while q:
        s = q.popleft()
        for f in ops:
            t = f(s)
            if t not in seen:
                seen.add(t)
                q.append(t)
    return seen


def symplectic_check(f) -> bool:
    """Does f preserve the two-qutrit form <u,v> = (xp*zp' - zp*xp') + (xf*zf' - zf*xf')?"""
    def form(u, v):
        return ((u[0] * v[1] - u[1] * v[0]) + (u[2] * v[3] - u[3] * v[2])) % 3

    for a in range(81):
        u = (a // 27, (a // 9) % 3, (a // 3) % 3, a % 3)
        for b in range(81):
            v = (b // 27, (b // 9) % 3, (b // 3) % 3, b % 3)
            if form(f(u), f(v)) != form(u, v):
                return False
    return True


def main() -> int:
    cx_only = reachable([op_cx_pf])
    all_symp = reachable(SYMPLECTIC)
    full_isa = reachable(SYMPLECTIC + TRANSLATION)

    print("reachable frames from reset (0,0,0,0), out of 81:")
    print(f"  CX alone                    (w33_qutrit_cx_frame) : {len(cx_only)}")
    print(f"  all six symplectic opcodes                        : {len(all_symp)}")
    print(f"  full ISA, symplectic + sigma^5 = Z                : {len(full_isa)}")

    linear_ok = all(symplectic_check(f) for f in SYMPLECTIC)
    z_is_linear = op_z_p(START) == START
    print()
    print(f"  all six symplectic opcodes preserve the form      : {linear_ok}")
    print(f"  sigma^5 = Z fixes the origin (i.e. is linear)     : {z_is_linear}")

    print()
    print("  Every symplectic map is linear and fixes 0, so ANY module built only from")
    print("  the six Clifford opcodes has reachable set {0} and folds away.  Opcode 101")
    print("  is the only instruction that translates, and it is what makes the frame")
    print("  space reachable at all.")

    out = {
        "pass": 2774,
        "reachable_from_reset": {
            "cx_alone": len(cx_only),
            "six_symplectic_opcodes": len(all_symp),
            "full_isa_with_sigma5_Z": len(full_isa),
            "total_frames": 81,
        },
        "symplectic_opcodes_preserve_form": linear_ok,
        "sigma5_Z_fixes_origin": z_is_linear,
        "modules": {
            "rtl/w33_pass2757_qutrit_cx.sv::w33_qutrit_cx_frame": "reachable set {0}",
            "rtl/w33_pass2762_holonet_isa.sv::w33_pass2762_holonet_isa": "reachable set is all 81",
            "rtl/w33_pass2752_cx_loadable_frame.sv::w33_cx_loadable_frame": "all 81 via the load port",
        },
    }
    path = ROOT / "data" / "PART_W33_PASS2774_ISA_FRAME_REACHABILITY.json"
    path.parent.mkdir(exist_ok=True)
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
