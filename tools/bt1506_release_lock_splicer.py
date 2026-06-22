#!/usr/bin/env python3
"""BT1506: idempotent release-lock splicer for BT1495--BT1503 inserts.

This edits photonic_holonet.tex in a checkout.  The GitHub connector commit only
adds the splicer and manifest; it does not rewrite the large paper source here.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "photonic_holonet.tex"
OUT = ROOT / "data" / "bt1506_release_lock_splicer.json"
MARKER = "% BT1506 transaction/scheduler release-lock splice"
INSERTS = [
    r"\input{analysis/BT1495_BT1497_holonet_insert}",
    r"\input{analysis/BT1498_BT1500_holonet_insert}",
    r"\input{analysis/BT1501_BT1503_holonet_insert}",
]
ANCHOR = r"\section[The fuel: matter equals magic]{The fuel: matter $=$ magic}"


def splice_text(text: str) -> tuple[str, dict]:
    before_counts = {ins: text.count(ins) for ins in INSERTS}
    if all(count == 1 for count in before_counts.values()):
        return text, {"already_spliced": True, "before_counts": before_counts, "after_counts": before_counts}
    if any(count > 1 for count in before_counts.values()):
        raise RuntimeError(f"duplicate insert before splice: {before_counts}")
    if text.count(ANCHOR) != 1:
        raise RuntimeError("fuel anchor must occur exactly once")
    block = MARKER + "\n" + "\n".join(INSERTS) + "\n\n"
    new_text = text.replace(ANCHOR, block + ANCHOR, 1)
    after_counts = {ins: new_text.count(ins) for ins in INSERTS}
    return new_text, {"already_spliced": False, "before_counts": before_counts, "after_counts": after_counts}


def main() -> None:
    text = MAIN.read_text(encoding="utf-8")
    new_text, counts = splice_text(text)
    if new_text != text:
        MAIN.write_text(new_text, encoding="utf-8")
    final = MAIN.read_text(encoding="utf-8")
    checks = {
        "main_exists": MAIN.exists(),
        "fuel_anchor_unique": final.count(ANCHOR) == 1,
        "all_inserts_once": all(final.count(ins) == 1 for ins in INSERTS),
        "marker_present": MARKER in final,
        "idempotent_counts": all(v == 1 for v in counts["after_counts"].values()),
    }
    result = {
        "bt": 1506,
        "title": "Release-lock splicer",
        "verified": all(checks.values()),
        "target": "photonic_holonet.tex",
        "anchor": ANCHOR,
        "marker": MARKER,
        "inserts": INSERTS,
        "counts": counts,
        "interpretation": "This splicer inserts the BT1495--BT1503 transaction/scheduler packet before the fuel section and is safe to rerun.",
        "honesty_boundary": "The connector commit adds the splicer; run it in checkout before rebuilding the PDF.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1506, "verified": result["verified"], "already_spliced": counts["already_spliced"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
