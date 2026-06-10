#!/usr/bin/env python3
"""BT643 character-tower insert integrator.

This uses a unique helper name because an earlier BT643 endpoint helper already
exists.  The helper is conservative and idempotent.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT643_character_tower_paper_insert.tex"
DST = ROOT / "paper" / "sections" / "sec_bt643_character_tower.tex"
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
INPUT = r"\input{sections/sec_bt643_character_tower}"
ANCHORS = [
    r"\input{sections/sec_bt633_e2_wg2_phase_packet}",
    r"\input{sections/sec627_external_wg2_packet}",
    r"\input{sections/sec_bt618_physical_propagator_normal_form}",
    r"\section{The TOE Singularity Theorem}",
]


def insert_once(text: str, line: str) -> str:
    if line in text:
        return text
    for anchor in ANCHORS:
        idx = text.find(anchor)
        if idx != -1:
            if anchor.startswith(r"\input"):
                end = text.find("\n", idx)
                if end == -1:
                    return text + "\n" + line + "\n"
                return text[: end + 1] + line + "\n" + text[end + 1 :]
            return text[:idx] + line + "\n" + text[idx:]
    return text.rstrip() + "\n" + line + "\n"


def main() -> int:
    if not SRC.exists():
        raise FileNotFoundError(SRC)
    if not PREPRINT.exists():
        raise FileNotFoundError(PREPRINT)
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(SRC.read_text(encoding="utf-8"), encoding="utf-8")
    text = PREPRINT.read_text(encoding="utf-8")
    PREPRINT.write_text(insert_once(text, INPUT), encoding="utf-8")
    print(f"copied {SRC.relative_to(ROOT)} -> {DST.relative_to(ROOT)}")
    print(f"ensured {INPUT} in {PREPRINT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
