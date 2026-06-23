#!/usr/bin/env python3
"""BT1586: full operator/OAM appendix splicer for the main Holonet paper."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "photonic_holonet.tex"
OUT = ROOT / "data" / "bt1586_operator_oam_full_appendix_splicer.json"
MD = ROOT / "analysis" / "BT1586_operator_oam_full_appendix_splicer.md"

BEGIN = "% BT1586 OPERATOR_OAM_FULL_APPENDIX BEGIN"
END = "% BT1586 OPERATOR_OAM_FULL_APPENDIX END"
INSERTION_MARKER = r"\begin{thebibliography}"
INSERTS = [
    "analysis/BT1564_BT1566_holonet_insert.tex",
    "analysis/BT1567_BT1569_holonet_insert.tex",
    "analysis/BT1570_BT1572_holonet_insert.tex",
    "analysis/BT1573_BT1576_holonet_insert.tex",
    "analysis/BT1580_BT1582_holonet_insert.tex",
    "analysis/BT1583_BT1585_holonet_insert.tex",
    "analysis/BT1586_BT1588_holonet_insert.tex",
    "analysis/BT1589_BT1591_holonet_insert.tex",
    "analysis/BT1592_BT1594_holonet_insert.tex",
]


def block() -> str:
    lines = [BEGIN]
    lines.extend(rf"\input{{{insert}}}" for insert in INSERTS)
    lines.append(END)
    return "\n".join(lines) + "\n"


def remove_existing_block(text: str) -> str:
    if BEGIN not in text or END not in text:
        return text
    before = text.split(BEGIN, 1)[0]
    after = text.split(END, 1)[1]
    return before.rstrip() + "\n\n" + after.lstrip("\n")


def splice_text(text: str) -> tuple[str, str]:
    insert_block = block()
    if BEGIN in text and END in text:
        stripped = remove_existing_block(text)
        if INSERTION_MARKER in stripped:
            return (
                stripped.replace(
                    INSERTION_MARKER, insert_block + "\n" + INSERTION_MARKER, 1
                ),
                "relocate_existing_block",
            )
        return stripped.rstrip() + "\n\n" + insert_block, "replace_existing_block"
    if INSERTION_MARKER in text:
        return (
            text.replace(INSERTION_MARKER, insert_block + "\n" + INSERTION_MARKER, 1),
            "insert_before_bibliography",
        )
    return text.rstrip() + "\n\n" + insert_block, "append_to_end"


def build_result(applied: bool) -> dict:
    target_text = TARGET.read_text(encoding="utf-8") if TARGET.exists() else ""
    spliced, mode = splice_text(target_text)
    second, second_mode = splice_text(spliced)
    missing = [insert for insert in INSERTS if not (ROOT / insert).exists()]
    if applied and spliced != target_text:
        TARGET.write_text(spliced, encoding="utf-8")
        target_text = spliced

    target_has_block = BEGIN in target_text and END in target_text
    checks = {
        "target_exists": TARGET.exists(),
        "bibliography_marker_present": INSERTION_MARKER in target_text,
        "nine_insert_paths": len(INSERTS) == 9,
        "insert_paths_unique": len(INSERTS) == len(set(INSERTS)),
        "all_insert_paths_exist": not missing,
        "bounded_block_has_begin_end": BEGIN in block() and END in block(),
        "includes_latest_claim_ledger": "analysis/BT1583_BT1585_holonet_insert.tex"
        in INSERTS,
        "includes_new_synthesis": "analysis/BT1586_BT1588_holonet_insert.tex"
        in INSERTS,
        "includes_radial_lane_frontend": "analysis/BT1589_BT1591_holonet_insert.tex"
        in INSERTS,
        "includes_lab_mode_hesse_loop": "analysis/BT1592_BT1594_holonet_insert.tex"
        in INSERTS,
        "idempotent_second_pass": second == splice_text(second)[0]
        and second_mode in {"replace_existing_block", "relocate_existing_block"},
        "applied_block_present_or_dry_run": (not applied) or target_has_block,
        "block_before_end_document": (BEGIN not in target_text)
        or (r"\end{document}" not in target_text.split(BEGIN, 1)[0]),
        "block_before_bibliography": (BEGIN not in target_text)
        or (BEGIN in target_text.split(INSERTION_MARKER, 1)[0]),
    }
    return {
        "bt": 1586,
        "title": "Operator/OAM full appendix splicer",
        "verified": all(checks.values()),
        "target": "photonic_holonet.tex",
        "applied": applied,
        "mode": mode,
        "second_mode": second_mode,
        "insert_count": len(INSERTS),
        "inserts": INSERTS,
        "missing_inserts": missing,
        "interpretation": (
            "The full operator/OAM appendix is now a bounded, idempotent paper splice. "
            "It includes the operator-on-photon, internal Clifford, recentering/protocol, "
            "validation/ledger, BT1586-BT1588 synthesis, and BT1589-BT1591 "
            "radial/lane/front-end inserts, plus the BT1592-BT1594 lab/mode/Hesse "
            "witness-loop insert."
        ),
        "honesty_boundary": (
            "This splices exact finite and claim-ledger text into the paper. It does not "
            "assert calibrated OAM hardware, measured leakage, or an optical loss model."
        ),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    result = build_result(args.apply)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text(
        "# BT1586 Operator/OAM Full Appendix Splicer\n\n"
        "BT1586 upgrades the earlier dry-run splice into a full bounded appendix splice "
        "for the main `photonic_holonet.tex` paper. The block includes the BT1564-BT1585 "
        "operator/OAM inserts, the BT1586-BT1588 synthesis insert, and the "
        "BT1589-BT1591 radial/lane/front-end insert, plus the BT1592-BT1594 "
        "lab/mode/Hesse witness-loop insert. It remains idempotent on repeated application.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1586,
                "verified": result["verified"],
                "applied": result["applied"],
                "mode": result["mode"],
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
