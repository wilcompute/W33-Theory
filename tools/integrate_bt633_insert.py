#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT633_e2_wg2_phase_packet_insert.tex"
DST = ROOT / "paper" / "sections" / "sec_bt633_e2_wg2_phase_packet.tex"
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
LINE = r"\input{sections/sec_bt633_e2_wg2_phase_packet}"
ANCHORS = [
    r"\input{sections/sec_bt627_external_wg2_packet}",
    r"\input{sections/sec_bt624_folded_hashimoto_sector_note}",
    r"\input{sections/sec_bt619_endpoint_factorial_trace_law}",
    r"\input{sections/sec_bt618_physical_propagator_normal_form}",
    r"\end{document}",
]

def main() -> int:
    DST.parent.mkdir(parents=True, exist_ok=True)
    src = SRC.read_text(encoding="utf-8")
    changed_section = (not DST.exists()) or DST.read_text(encoding="utf-8") != src
    if changed_section:
        DST.write_text(src, encoding="utf-8")

    text = PREPRINT.read_text(encoding="utf-8")
    inserted = False
    anchor_used = "already-present"
    if LINE not in text:
        for anchor in ANCHORS:
            if anchor in text:
                if anchor == r"\end{document}":
                    text = text.replace(anchor, LINE + "\n" + anchor, 1)
                else:
                    text = text.replace(anchor, anchor + "\n" + LINE, 1)
                inserted = True
                anchor_used = anchor
                break
        if not inserted:
            raise RuntimeError("No insertion anchor found")
        PREPRINT.write_text(text, encoding="utf-8")

    print({
        "bt": 636,
        "source": str(SRC.relative_to(ROOT)),
        "section": str(DST.relative_to(ROOT)),
        "line": LINE,
        "section_changed": changed_section,
        "inserted": inserted,
        "anchor": anchor_used,
    })
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
