#!/usr/bin/env python3
"""BT1491: idempotently splice the exact finite insert stack into the paper."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1491_paper_splice_v2_idempotent.json"
MD = ROOT / "analysis" / "BT1489_BT1491_row_square_splice.md"
INSERT = ROOT / "analysis" / "BT1489_BT1491_holonet_insert.tex"
MAIN = ROOT / "photonic_holonet.tex"

MARKER_START = "% BT1491 exact finite insert stack start"
MARKER_END = "% BT1491 exact finite insert stack end"
ANCHOR = "%======================================================================\n\\section{The software: braids, teleported gates, universality}"
REQUIRED_INSERTS = [
    "analysis/BT1480_BT1482_holonet_insert.tex",
    "analysis/BT1483_BT1485_holonet_insert.tex",
    "analysis/BT1486_BT1488_holonet_insert.tex",
    "analysis/BT1489_BT1491_holonet_insert.tex",
]


def load_json(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def write_insert() -> None:
    insert = r"""\subsection{BT1489--BT1491 row symmetry and Fano--E6 square}
\label{sec:bt1489-bt1491-row-fano-e6-square}

BT1489 lifts the \(S_4\), \(D_4\), and \(V_4\) branch actions from triangle
labels to the actual ABI v2 row layer.  All \(24\) elements of \(S_4\), all
\(8\) elements of the square \(D_4\) subgroup, and all \(4\) \(V_4\)
translations act as honest permutations of the \(72\) active/guard value rows.
The lift preserves the \(C_3\) channel, row kind, qutrit value, guard slot, and
column formula, so the branch symmetry is now a decoder-row symmetry.

BT1490 is the new finite-geometry lock:
\[
24 = 4\cdot6 = 3\cdot8,\qquad
72 = 3\cdot24,\qquad
168 = 7\cdot24 = 21\cdot8,\qquad
81 = 72+9.
\]
The shared \(24\)-state fiber is \(V_4\) branch times six row-value slots on the
ABI side, and three local Fano arms times the \(D_4\) flag stabilizer on the
Fano side.  Thus the same finite fiber feeds the E6/CSS \(72\)-sector, the
\(81\)-closure after adjoining the \(q^2=9\) firewall gap, and the Fano-native
\(168\) active-bin bus.

BT1491 makes the paper splice idempotent.  The main holonet paper now imports
the BT1480--BT1491 exact finite packet through one controlled block; rerunning
the splicer replaces that block rather than duplicating it.  The claim firewall
remains intact: this is an exact finite ABI and incidence statement, not a
detector calibration, optical-layout claim, or imported Golden Quartic/Mobius
particle interpretation.
"""
    INSERT.write_text(insert, encoding="utf-8")


def write_markdown() -> None:
    md = """# BT1489-BT1491: Row Actions, Fano-E6 Square, and Idempotent Paper Splice

## BT1489

BT1489 lifts the branch symmetry into the actual ABI v2 row machine.

```text
S4 branch actions: 24 unique row permutations
D4 square subgroup: 8 unique row permutations
V4 translations: 4 unique row permutations
Rows: 72 = 24 active/guard packets over 3 C3 channels
```

Every lifted action preserves channel, row kind, qutrit value, guard slot, and
the active/guard column formula.  Tau4 now has a concrete row permutation, while
the shear-induced branch identity fixes all 72 rows at this layer.

## BT1490

The new square is the shared 24-state fiber:

```text
24 = 4 V4 branches * 6 ABI row-value slots
24 = 3 local Fano arms * 8 D4 flag states
72 = 3 C3 channels * 24
81 = 72 + q^2 firewall gap
168 = 7 Fano points * 24 = 21 Fano flags * 8
```

This is the clean bridge between the E6/CSS ABI and the Fano detector-bin count.
It keeps the physical firewall explicit: no waveguide calibration or particle
interpretation is imported.

## BT1491

BT1491 makes the paper update mechanical and rerunnable.  If the BT1480-BT1491
insert chain exists, the splicer writes exactly one controlled input block into
`photonic_holonet.tex` before the software section.  A second run is a no-op.

## Current synthesis

```text
S4/D4/V4 branch actions
  -> 72 concrete ABI row permutations
  -> shared 24-state fiber
  -> E6/CSS 72 and 81
  -> Fano 168 by point and flag factorizations
  -> idempotent main-paper splice.
```
"""
    MD.write_text(md, encoding="utf-8")


def input_block() -> str:
    lines = [
        MARKER_START,
        *[f"\\input{{{relpath[:-4]}}}" for relpath in REQUIRED_INSERTS],
        MARKER_END,
        "",
    ]
    return "\n".join(lines)


def splice_main() -> dict:
    text = MAIN.read_text(encoding="utf-8")
    block = input_block()
    start_count = text.count(MARKER_START)
    end_count = text.count(MARKER_END)
    action = "unchanged"

    if start_count or end_count:
        if start_count != 1 or end_count != 1:
            return {
                "ok": False,
                "action": "blocked_multiple_markers",
                "before_marker_count": start_count,
                "after_marker_count": start_count,
            }
        start = text.index(MARKER_START)
        end = text.index(MARKER_END) + len(MARKER_END)
        while end < len(text) and text[end] in "\r\n":
            end += 1
        new_text = text[:start] + block + text[end:]
        action = "replaced" if new_text != text else "unchanged"
    else:
        if ANCHOR not in text:
            return {
                "ok": False,
                "action": "blocked_missing_anchor",
                "before_marker_count": 0,
                "after_marker_count": 0,
            }
        new_text = text.replace(ANCHOR, block + ANCHOR, 1)
        action = "inserted"

    if new_text != text:
        MAIN.write_text(new_text, encoding="utf-8")
    after_text = MAIN.read_text(encoding="utf-8")
    return {
        "ok": True,
        "action": action,
        "before_marker_count": start_count,
        "after_marker_count": after_text.count(MARKER_START),
        "input_counts": {
            relpath: after_text.count(f"\\input{{{relpath[:-4]}}}")
            for relpath in REQUIRED_INSERTS
        },
    }


def main() -> None:
    bt1488 = load_json("data/bt1488_paper_splice_v2_manifest.json")
    bt1489 = load_json("data/bt1489_s4_d4_v4_row_action_lift.json")
    bt1490 = load_json("data/bt1490_fano_e6_commuting_square.json")

    write_insert()
    write_markdown()

    required_exists = {
        relpath: (ROOT / relpath).exists() for relpath in REQUIRED_INSERTS
    }
    splice = (
        splice_main()
        if all(required_exists.values())
        else {
            "ok": False,
            "action": "blocked_missing_required_insert",
            "before_marker_count": MAIN.read_text(encoding="utf-8").count(MARKER_START),
            "after_marker_count": MAIN.read_text(encoding="utf-8").count(MARKER_START),
            "input_counts": {},
        }
    )
    after_text = MAIN.read_text(encoding="utf-8")

    checks = {
        "bt1488_manifest_loaded": bt1488["verified"] is True,
        "bt1489_row_lift_loaded": bt1489["verified"] is True,
        "bt1490_square_loaded": bt1490["verified"] is True,
        "required_insert_chain_present": all(required_exists.values()),
        "insert_written": INSERT.exists()
        and "BT1490 is the new finite-geometry lock"
        in INSERT.read_text(encoding="utf-8"),
        "markdown_written": MD.exists()
        and "shared 24-state fiber" in MD.read_text(encoding="utf-8"),
        "splice_ok": splice["ok"] is True,
        "single_marker_block": after_text.count(MARKER_START) == 1
        and after_text.count(MARKER_END) == 1,
        "each_required_input_once": all(
            after_text.count(f"\\input{{{relpath[:-4]}}}") == 1
            for relpath in REQUIRED_INSERTS
        ),
        "block_before_software_section": after_text.index(MARKER_START)
        < after_text.index(
            "\\section{The software: braids, teleported gates, universality}"
        ),
    }
    result = {
        "bt": 1491,
        "title": "Idempotent paper splice v2",
        "verified": all(checks.values()),
        "main_tex": "photonic_holonet.tex",
        "insert": "analysis/BT1489_BT1491_holonet_insert.tex",
        "markdown": "analysis/BT1489_BT1491_row_square_splice.md",
        "required_inserts": REQUIRED_INSERTS,
        "splice": splice,
        "interpretation": (
            "The main photonic holonet paper now owns the BT1480-BT1491 exact "
            "finite insert chain through one idempotent input block.  Re-running "
            "the tool proves the paper stays single-copy."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": 1491,
                "verified": result["verified"],
                "action": splice["action"],
                "inputs": len(REQUIRED_INSERTS),
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
