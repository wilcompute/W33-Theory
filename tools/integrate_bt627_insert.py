#!/usr/bin/env python3
"""BT629: idempotently integrate the BT627 external W(G2) packet insert.

This narrow helper avoids touching the larger all-in-one integrator.  It copies

    analysis/BT627_external_wg2_packet_insert.tex

into paper/sections and inserts

    \input{sections/sec_bt627_external_wg2_packet}

exactly once in paper/w33_preprint.tex, preferentially after the BT624 folded
Hashimoto sector note when that line is present, otherwise after the BT618/BT619
physical propagator block, otherwise before the TOE singularity section.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT627_external_wg2_packet_insert.tex"
DST = ROOT / "paper" / "sections" / "sec_bt627_external_wg2_packet.tex"
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
INPUT_LINE = r"\input{sections/sec_bt627_external_wg2_packet}"
PREFERRED_ANCHORS = [
    r"\input{sections/sec_bt624_folded_hashimoto_sector_note}",
    r"\input{sections/sec_bt619_endpoint_factorial_trace_law}",
    r"\input{sections/sec_bt618_physical_propagator_normal_form}",
    r"\input{sections/sec_bt613_folded_hashimoto_hodge_flow}",
]
FALLBACK_SECTION = r"\section{The TOE Singularity Theorem}"


def insert_once(text: str, line: str) -> tuple[str, bool]:
    if line in text:
        return text, False
    for anchor in PREFERRED_ANCHORS:
        if anchor in text:
            return text.replace(anchor, anchor + "\n" + line, 1), True
    if FALLBACK_SECTION in text:
        return text.replace(FALLBACK_SECTION, line + "\n\n" + FALLBACK_SECTION, 1), True
    raise RuntimeError("No safe insertion anchor found for BT627 insert")


def main() -> int:
    if not SRC.exists():
        raise FileNotFoundError(SRC)
    if not PREPRINT.exists():
        raise FileNotFoundError(PREPRINT)
    DST.parent.mkdir(parents=True, exist_ok=True)
    src_text = SRC.read_text(encoding="utf-8")
    old_dst = DST.read_text(encoding="utf-8") if DST.exists() else None
    dst_changed = old_dst != src_text
    if dst_changed:
        DST.write_text(src_text, encoding="utf-8")

    preprint = PREPRINT.read_text(encoding="utf-8")
    new_preprint, inserted = insert_once(preprint, INPUT_LINE)
    if inserted:
        PREPRINT.write_text(new_preprint, encoding="utf-8")

    print({
        "bt": 629,
        "source": str(SRC.relative_to(ROOT)),
        "section": str(DST.relative_to(ROOT)),
        "preprint": str(PREPRINT.relative_to(ROOT)),
        "input_line": INPUT_LINE,
        "section_changed": dst_changed,
        "input_inserted": inserted,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
