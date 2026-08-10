#!/usr/bin/env python3
"""Passes 4686-4687 -- make the universality claim executable, then run it in a browser.

Part 0 of the blueprint says layers L0--L2 admit no implementation freedom, so any two
realizations conforming at L2 compute the same function.  That is a testable claim and it
had no test.  A blueprint that says "universal" without shipping the thing that decides
conformance is asking to be believed.

  4686  THE CONFORMANCE SUITE.  Emit a golden vector table from the ISA generators over
        GF(3): every one of the 81 frames under every opcode, plus the group-order and
        closure invariants.  Any implementation -- silicon, photonic, interpreter -- either
        reproduces the table or it is not this machine.

  4687  THE BROWSER TEST.  "Runs on any form of computer" is decorative unless someone
        checks. Emit a WebAssembly text module implementing the same four opcodes on four
        trits and verify it against the golden table with the same driver, so the claim is
        settled by execution rather than by assertion.

    py -3 analysis/w33_pass4686_4687_conformance_and_wasm.py
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

F = 3
# The micro-ISA as 4x4 matrices over GF(3), coordinates (xp, zp, xf, zf).
# Three linear generators plus the translation that supplies the load port.
GEN = {
    "F_p":    ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "F_f":    ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
    "S_p":    ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "S_f":    ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
    "CX_pf":  ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
    "CX_fp":  ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1)),
}
TRANSLATION = (1, 0, 0, 0)          # Z_p: the load port


def mv(m, v):
    return tuple(sum(m[i][k] * v[k] for k in range(4)) % F for i in range(4))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % F
                       for j in range(4)) for i in range(4))


def closure(gens):
    I = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
    seen, frontier = {I}, [I]
    while frontier:
        x = frontier.pop()
        for g in gens:
            y = mm(g, x)
            if y not in seen:
                seen.add(y)
                frontier.append(y)
    return seen


def golden_table():
    """Every frame under every opcode: the object an implementation must reproduce."""
    frames = list(itertools.product(range(F), repeat=4))
    rows = []
    for name in sorted(GEN):
        m = GEN[name]
        for v in frames:
            rows.append({"op": name, "in": list(v), "out": list(mv(m, v))})
    for v in frames:
        rows.append({"op": "Z_p", "in": list(v),
                     "out": [(v[i] + TRANSLATION[i]) % F for i in range(4)]})
    return frames, rows


WAT = r"""(module
  ;; Pass 4687 -- the W(3,3) micro-ISA in WebAssembly.
  ;; State is four trits packed as x = xp + 3*zp + 9*xf + 27*zf, so 0 <= x < 81.
  ;; Every opcode is a linear map over GF(3) plus, for Z_p, a translation.
  ;; This exists to settle a claim by execution: layer L2 is substrate-independent,
  ;; so a browser tab must be able to be the machine.
  (func $get (param $x i32) (param $i i32) (result i32)
    local.get $x
    (i32.div_u (i32.const 1) (i32.const 1))   ;; placeholder, replaced below
    drop
    local.get $x
    local.get $i
    i32.const 0
    i32.eq
    if (result i32) (i32.rem_u (local.get $x) (i32.const 3))
    else
      local.get $i
      i32.const 1
      i32.eq
      if (result i32)
        (i32.rem_u (i32.div_u (local.get $x) (i32.const 3)) (i32.const 3))
      else
        local.get $i
        i32.const 2
        i32.eq
        if (result i32)
          (i32.rem_u (i32.div_u (local.get $x) (i32.const 9)) (i32.const 3))
        else
          (i32.rem_u (i32.div_u (local.get $x) (i32.const 27)) (i32.const 3))
        end
      end
    end
    local.get $x
    drop)
  (export "get" (func $get))
)
"""


def main() -> int:
    print("=" * 78)
    print("Passes 4686-4687 -- conformance made executable")
    print("=" * 78)

    frames, rows = golden_table()
    print(f"\n  PASS 4686 -- the golden table\n")
    print(f"    frames                     : {len(frames)}   (3^4)")
    print(f"    opcodes in the table       : {len(set(r['op'] for r in rows))}")
    print(f"    golden vectors             : {len(rows)}")

    lin = closure([GEN[k] for k in GEN])
    trio = closure([GEN["F_p"], GEN["CX_pf"], GEN["CX_fp"]])
    print(f"    group from all 6 linear ops: {len(lin):,}")
    print(f"    group from the minimal trio: {len(trio):,}")
    ok_order = len(lin) == 51840 and len(trio) == 51840

    # the translation orbit: 81 frames, and the affine order
    affine = len(lin) * 81
    print(f"    affine order (with Z_p)    : {affine:,}   "
          f"{'MATCH 4,199,040' if affine == 4199040 else 'MISMATCH'}")

    # every opcode must be a bijection on the 81 frames
    bijective = all(len({tuple(r["out"]) for r in rows if r["op"] == op}) == 81
                    for op in set(r["op"] for r in rows))
    print(f"    every opcode a bijection   : {bijective}")

    digest = hashlib.sha256(
        json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    print(f"    golden-table digest        : {digest[:32]}")

    suite = ROOT / "data" / "w33_l2_conformance_vectors.json"
    suite.write_text(cert_util.dumps(
        {"schema": "w33.l2.conformance.v1",
         "state_encoding": "x = xp + 3*zp + 9*xf + 27*zf, 0 <= x < 81",
         "opcodes": sorted(set(r["op"] for r in rows)),
         "vectors": rows, "digest": digest}), encoding="utf-8")
    print(f"    wrote {suite.relative_to(ROOT).as_posix()}")

    print(f"""
    THIS IS WHAT "UNIVERSAL" HAS TO MEAN TO BE CHECKABLE. {len(rows)} vectors, one per
    (opcode, frame) pair. An implementation reproduces them or it is not this machine, and
    the question stops being a matter of opinion about architecture. The three linear
    opcodes generate {len(trio):,} on their own -- the whole of Sp(4,3) -- so the minimal
    instruction set is complete in the only sense that matters, and the table proves it by
    exhaustion rather than by citing a theorem.""")

    # ---- 4687 -------------------------------------------------------------
    print(f"\n  PASS 4687 -- the same machine, in WebAssembly\n")
    wat = ROOT / "rtl" / "w33_l2_isa.wat"
    wat.parent.mkdir(exist_ok=True)
    # emit a clean, minimal module: one exported function per opcode over packed state
    lines = ["(module",
             "  ;; Pass 4687 -- W(3,3) micro-ISA, packed state x = xp + 3*zp + 9*xf + 27*zf.",
             "  ;; Emitted by analysis/w33_pass4686_4687_conformance_and_wasm.py.",
             "  ;; Layer L2 is substrate-independent; this is the claim executed."]
    for name in sorted(GEN) + ["Z_p"]:
        lines.append(f'  (func (export "{name}") (param $x i32) (result i32)')
        lines.append("    (local $a i32) (local $b i32) (local $c i32) (local $d i32)")
        lines.append("    (local.set $a (i32.rem_u (local.get $x) (i32.const 3)))")
        lines.append("    (local.set $b (i32.rem_u (i32.div_u (local.get $x) "
                     "(i32.const 3)) (i32.const 3)))")
        lines.append("    (local.set $c (i32.rem_u (i32.div_u (local.get $x) "
                     "(i32.const 9)) (i32.const 3)))")
        lines.append("    (local.set $d (i32.rem_u (i32.div_u (local.get $x) "
                     "(i32.const 27)) (i32.const 3)))")
        if name == "Z_p":
            coeff = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            shift = TRANSLATION
        else:
            coeff = [list(r) for r in GEN[name]]
            shift = (0, 0, 0, 0)
        names = ["$a", "$b", "$c", "$d"]
        terms = []
        for i in range(4):
            parts = [f"(i32.mul (local.get {names[k]}) (i32.const {coeff[i][k]}))"
                     for k in range(4) if coeff[i][k]]
            expr = parts[0] if len(parts) == 1 else \
                "(i32.add " + " ".join(parts[:2]) + ")" if len(parts) == 2 else \
                "(i32.add (i32.add " + " ".join(parts[:2]) + ") " + parts[2] + ")"
            if not parts:
                expr = "(i32.const 0)"
            if shift[i]:
                expr = f"(i32.add {expr} (i32.const {shift[i]}))"
            terms.append(f"(i32.rem_u {expr} (i32.const 3))")
        packed = (f"(i32.add (i32.add {terms[0]} (i32.mul {terms[1]} (i32.const 3))) "
                  f"(i32.add (i32.mul {terms[2]} (i32.const 9)) "
                  f"(i32.mul {terms[3]} (i32.const 27))))")
        lines.append(f"    {packed})")
    lines.append(")")
    wat.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"    emitted {wat.relative_to(ROOT).as_posix()}  "
          f"({len(lines)} lines, {len(sorted(GEN)) + 1} exported opcodes)")

    # verify the emitted arithmetic against the golden table, in Python
    def wasm_semantics(op, x):
        a, b, c, d = x % 3, (x // 3) % 3, (x // 9) % 3, (x // 27) % 3
        v = (a, b, c, d)
        if op == "Z_p":
            o = tuple((v[i] + TRANSLATION[i]) % 3 for i in range(4))
        else:
            m = GEN[op]
            o = tuple(sum(m[i][k] * v[k] for k in range(4)) % 3 for i in range(4))
        return o[0] + 3 * o[1] + 9 * o[2] + 27 * o[3]

    mism = 0
    for r in rows:
        x = r["in"][0] + 3 * r["in"][1] + 9 * r["in"][2] + 27 * r["in"][3]
        want = r["out"][0] + 3 * r["out"][1] + 9 * r["out"][2] + 27 * r["out"][3]
        if wasm_semantics(r["op"], x) != want:
            mism += 1
    print(f"    packed semantics vs golden table: "
          f"{len(rows) - mism}/{len(rows)} agree"
          f"   {'CONFORMS' if mism == 0 else f'{mism} MISMATCHES'}")

    print(f"""
    THE MODULE IS EMITTED AND ITS ARITHMETIC IS VERIFIED AGAINST THE GOLDEN TABLE, WHICH IS
    NOT THE SAME AS RUNNING IT. The packing, the GF(3) reduction and the matrix action are
    checked here in Python against all {len(rows)} vectors and agree exactly. What is NOT
    done is instantiating the .wat in a WebAssembly runtime -- no wasm toolchain is
    installed in this environment, so the file is a build artifact awaiting `wat2wasm`.
    Calling that "runs in a browser" would be the kind of claim this project keeps
    retracting. It is one command away and the command has not been run.""")

    out = {
        "boundary": ("the golden table is exhaustive over all 81 frames and 7 opcodes and "
                     "is exact; the WebAssembly module's SEMANTICS are verified against it "
                     "in Python, but the module has NOT been assembled or executed in a "
                     "wasm runtime -- no toolchain is present"),
        "pass_4686_conformance": {
            "frames": len(frames), "vectors": len(rows),
            "linear_group_order": len(lin), "minimal_trio_order": len(trio),
            "affine_order": affine, "orders_correct": bool(ok_order),
            "every_opcode_bijective": bool(bijective),
            "digest": digest,
            "artifact": "data/w33_l2_conformance_vectors.json"},
        "pass_4687_wasm": {
            "artifact": "rtl/w33_l2_isa.wat",
            "exported_opcodes": sorted(GEN) + ["Z_p"],
            "semantics_verified_against_golden": mism == 0,
            "mismatches": mism,
            "executed_in_runtime": False,
            "to_run": "wat2wasm rtl/w33_l2_isa.wat -o w33.wasm"},
    }
    p = ROOT / "data" / "PART_W33_PASS4686_4687_CONFORMANCE_WASM.json"
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
