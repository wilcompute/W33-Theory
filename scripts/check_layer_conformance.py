#!/usr/bin/env python3
"""Enforce the blueprint's own may-claim table, sentence by sentence.  Pass 4690.

WHY THIS EXISTS
---------------
Part 0 of the blueprint ends with a table saying what each layer may and may not claim, and
then says something notable about it:

    "Most of the withdrawn claims recorded in Part Evidence were violations of this table
     --- a measurement made at one layer and reported as though it constrained another.
     Both are visible immediately once the layer is named, and neither was visible without
     it."

If that is true, the table is not commentary -- it is a decision procedure, and a decision
procedure that only runs in a reader's head runs on the pages the reader happens to reach.
Every withdrawn claim in this project was in a document somebody had already read.

THE TABLE, MECHANISED
---------------------
    L0-L2  may claim necessity and exact counts;  may NOT claim speed, area or power
    L3     may claim gate counts and relative cost;  may NOT claim minimality or uniqueness
    L4     may claim energy floors and timing;  may NOT claim a floor has been ACHIEVED
    L5-L6  may claim behaviour and equivalence;  may NOT claim anything about physics

A violation is a sentence carrying one layer's vocabulary together with that layer's
forbidden vocabulary.  That is detectable without understanding the sentence, which is the
point: the check has to survive being run by something that is not reading carefully.

WHAT IT WILL NOT CATCH
----------------------
A claim that crosses layers across two sentences, or one whose layer is implied by
surrounding context rather than named in the sentence.  Sentence-local detection is the
tractable fragment, not the whole rule.

    py -3 scripts/check_layer_conformance.py --selftest
    py -3 scripts/check_layer_conformance.py [files...]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# vocabulary that places a sentence at a layer
LAYER_VOCAB = {
    "L0-L2": re.compile(
        r"\b(?:W\(3,3\)|symplectic polar|40 points|forty points|81 frames|opcode|"
        r"instruction set|Sp\(4,3\)|51,?840|4,?199,?040|frame|carrier point|"
        r"generalis\w+ quadrangle|generaliz\w+ quadrangle)\b", re.I),
    "L3": re.compile(
        r"\b(?:datapath|netlist|gate count|cells?\b|synthesi[sz]\w*|standard cell|"
        r"yosys|LUTs?|flip-?flops?|register file)\b", re.I),
    "L4": re.compile(
        r"\b(?:Landauer|kT\s*\\?ln\s*2|erasure|thermodynamic|joules?|physical "
        r"realization|substrate|photonic|CMOS)\b", re.I),
    "L5-L6": re.compile(
        r"\b(?:kernel|virtual machine|interpreter|routing policy|scheduler|"
        r"fault escalation|relocation|host software)\b", re.I),
}

# vocabulary each layer is forbidden to use
FORBIDDEN = {
    "L0-L2": (re.compile(
        r"\b(?:watts?|milliwatts?|\bW\b(?=\s*(?:of|at|per))|nanoseconds?|\bns\b|"
        r"megahertz|\bMHz\b|\bGHz\b|clock (?:rate|speed)|throughput|latency|"
        r"square millimet\w+|mm\^?2|die area|power (?:draw|budget|consumption))\b", re.I),
        "speed, area or power at a layer with no physical realization"),
    "L3": (re.compile(
        r"\b(?:minimal|minimum possible|optimal|fewest possible|smallest possible|"
        r"cannot be (?:beaten|improved)|provably (?:smallest|fewest)|unique(?:ly)? "
        r"(?:smallest|minimal))\b", re.I),
        "minimality or uniqueness of a gate count that was synthesised, not proved minimal"),
    "L4": (re.compile(
        r"\b(?:achieve[sd]?|attain(?:s|ed)?|reaches the floor|operates at the (?:floor|"
        r"limit)|measured at the (?:floor|limit)|realis\w+ the bound|realiz\w+ the bound)\b",
        re.I),
        "a thermodynamic floor described as achieved rather than as a bound"),
    "L5-L6": (re.compile(
        r"\b(?:joules?|watts?|kT\s*\\?ln|Landauer|temperature|photon|dissipat\w+|"
        r"energy (?:cost|per))\b", re.I),
        "physics from a layer that is policy or host software"),
}

SENT = re.compile(r"(?<=[.!?])\s+|\n\n+")
TEXCMD = re.compile(r"\\[a-zA-Z@]+\s*|[{}$&%~^_]|\\\\")

# Two false-positive families, both found by triaging the first run on the blueprint.
#
#  1. TABLES.  A tabular body has no sentence structure, so the splitter flattens an entire
#     table into one "sentence" in which a geometry row and a MHz column co-occur. Eight of
#     the first fifteen hits were this and none was a claim at all.
#  2. "MINIMAL ENGINE".  Here `minimal` names the minimal GENERATING SET of the group -- an
#     L2 statement that is proved -- not a minimal cell count. Six hits were this, and one
#     of them was the document's own warning box explaining the distinction. Flagging a
#     passage for correctly drawing the line it draws is the checker being wrong twice.
SKIP_ENV = re.compile(r"\\begin\{(tabular|tabularx|array|longtable|spec|verbatim|"
                      r"lstlisting|tikzpicture)\}")
END_ENV = re.compile(r"\\end\{(tabular|tabularx|array|longtable|spec|verbatim|"
                     r"lstlisting|tikzpicture)\}")
PROVED_MINIMAL = re.compile(
    r"minimal\s+(?:engine|generating set|generating sets|instruction set|"
    r"arithmetic core|word|program)", re.I)


def sentences(text: str):
    # strip comments, then split; keep an approximate line number
    out, line, depth = [], 1, 0
    for block in text.split("\n"):
        if SKIP_ENV.search(block):
            depth += 1
        keep = depth == 0 and not block.lstrip().startswith("%")
        if END_ENV.search(block):
            depth = max(0, depth - 1)
        if keep:
            out.append((line, block))
        line += 1
    joined = []
    buf, start = [], None
    for ln, b in out:
        if start is None:
            start = ln
        buf.append(b)
        if b.strip().endswith((".", "!", "?")) or not b.strip():
            joined.append((start, " ".join(buf)))
            buf, start = [], None
    if buf:
        joined.append((start or 1, " ".join(buf)))
    res = []
    for ln, chunk in joined:
        for s in SENT.split(chunk):
            s = TEXCMD.sub(" ", s)
            s = re.sub(r"\s+", " ", s).strip()
            if len(s) > 20:
                res.append((ln, s))
    return res


def scan_text(text: str):
    hits = []
    for ln, s in sentences(text):
        for layer, vocab in LAYER_VOCAB.items():
            if not vocab.search(s):
                continue
            pat, why = FORBIDDEN[layer]
            m = pat.search(s)
            if m and layer == "L3" and PROVED_MINIMAL.search(s):
                continue        # "minimal engine" = minimal generating set, an L2 theorem
            if m:
                hits.append({"line": ln, "layer": layer, "trigger": m.group(0),
                             "why": why, "text": s[:130]})
    return hits


PLANTS = [
    ("planted L0-L2 x power", True,
     r"The instruction set uses eight opcodes and the design runs at 500 MHz."),
    ("planted L3 x minimality", True,
     "Design A synthesises to 103 cells, which is the minimal cell count for this datapath."),
    ("planted L4 x achieved", True,
     "The photonic carrier achieves the Landauer floor of kT ln 2 per erasure."),
    ("planted L5-L6 x physics", True,
     "The virtual machine dissipates 4.859e-21 joules per route on the host."),
    ("clean L0-L2", False,
     "The instruction set has eight opcodes in three bits and generates Sp(4,3)."),
    ("clean L3", False,
     "Design A synthesises to 103 cells against Design D's 240 cells."),
    ("clean L4", False,
     "Erasure costs kT ln 2 = 2.871e-21 J at 300 K, a bound no realization can beat."),
    ("clean L5-L6", False,
     "The virtual machine executes the same eight opcodes and returns identical results."),
    # the two false-positive families, kept as regression cases
    ("clean: minimal generating set", False,
     "The minimal engine of four operations synthesises to 43 logic cells."),
    ("planted L3 minimality survives", True,
     "The datapath uses 103 cells, the fewest possible for any conforming design."),
]


def selftest() -> int:
    ok = True
    print("  selftest -- one planted violation and one clean sentence per rule\n")
    for name, want, s in PLANTS:
        got = bool(scan_text(s + "\n\n"))
        good = got == want
        ok &= good
        print(f"    {name:26s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print("""
  Each clean sentence sits at the SAME layer as its planted twin and uses the same nouns.
  The pairs differ only in the forbidden move -- quoting a clock rate for a mathematical
  object, calling a synthesis result minimal, calling a bound achieved, pricing a software
  route in joules. A checker that flagged both halves of a pair would be detecting the
  topic, not the violation.

  ITS LIMIT: detection is sentence-local. A claim whose layer is set by the previous
  paragraph, or split across a sentence boundary, is invisible here -- and the two examples
  Part 0 gives (a wattage from an assumed cadence, a cell count against a wrong baseline)
  are BOTH of that kind. This catches the easy fragment and does not replace reading.""")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    files = [Path(f) for f in a.files] if a.files else \
        [ROOT / "holonet_machine_blueprint_body.tex"] + \
        sorted((ROOT / "manuscripts" / "tex").glob("part*.tex"))
    total = 0
    per_layer = {}
    for p in files:
        if not p.is_file():
            continue
        hits = scan_text(p.read_text(encoding="utf-8", errors="replace"))
        if hits:
            rel = p.relative_to(ROOT).as_posix() if ROOT in p.parents else p.name
            print(f"\n  {rel}")
        for h in hits:
            total += 1
            per_layer[h["layer"]] = per_layer.get(h["layer"], 0) + 1
            print(f"    line {h['line']:5d}  [{h['layer']}]  trigger={h['trigger']!r}")
            print(f"      {h['why']}")
            print(f"      {h['text']}")
    print(f"\n  {total} sentence-local layer violations"
          + (f"  {per_layer}" if per_layer else ""))
    if total == 0:
        print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
