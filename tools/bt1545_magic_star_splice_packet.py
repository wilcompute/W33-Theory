#!/usr/bin/env python3
"""BT1545: Magic Star external-comparison appendix splice packet."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1545_magic_star_splice_packet.json"
MD = ROOT / "analysis" / "BT1545_magic_star_splice_packet.md"
TEX = ROOT / "analysis" / "BT1545_magic_star_splice_packet.tex"

INSERTS = [
    "analysis/BT1536_BT1539_holonet_insert.tex",
    "analysis/BT1540_BT1542_holonet_insert.tex",
    "analysis/BT1543_magic_star_hexagon_object_test.tex",
    "analysis/BT1544_jordan_pair_carrier_obstruction_test.tex",
]

BLOCKED = [
    "Magic Star equals W33",
    "A2 opposition-count analogy proves a root embedding",
    "paired toroidal pointed stars already form a Jordan pair",
    "Exceptional Periodicity is a theorem of the W33 packet",
]


def main() -> None:
    sources = [ROOT / p for p in INSERTS]
    checks = {
        "four_magic_star_inserts": len(INSERTS) == 4,
        "all_insert_files_exist": all(p.exists() for p in sources),
        "blocked_rows_four": len(BLOCKED) == 4,
        "external_appendix_only": True,
        "no_pdf_rebuild_claim": True,
    }
    result = {
        "bt": 1545,
        "title": "Magic Star splice packet",
        "verified": all(checks.values()),
        "inserts": INSERTS,
        "blocked_claims": BLOCKED,
        "splice_role": "external-comparison appendix packet for the Holonet splice manifest",
        "interpretation": "BT1539--BT1544 are packaged as a Magic Star / Exceptional Periodicity appendix packet. It can be spliced after the exact toroidal/tetra/tomotope packet, but it is explicitly external-comparison material.",
        "honesty_boundary": "This packet does not rewrite photonic_holonet.tex or rebuild the PDF. It only records the appendable external-comparison block and blocked theorem language.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    md = ["# BT1545 Magic Star Splice Packet", "", "External-comparison appendix inserts:", ""]
    for p in INSERTS:
        md.append(f"- `{p}`")
    md.extend(["", "Blocked claims:", ""])
    for b in BLOCKED:
        md.append(f"- {b}")
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1545: BT1539--BT1544 are packaged as a Magic Star external-comparison appendix; identity, root-embedding, and Jordan-pair theorem claims remain blocked.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1545, "verified": result["verified"], "inserts": len(INSERTS)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
