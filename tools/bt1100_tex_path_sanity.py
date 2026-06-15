#!/usr/bin/env python3
"""BT1100 no-network TeX/path sanity check.

This is not a TeX compiler.  It checks the deterministic hazards we can validate
without installing TeX: integration markers, expected input files, duplicate
labels among staged sections, and simple brace balance in the section files.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

W33_MARKER = r"\section{The TOE Singularity Theorem}"
HOLONET_MARKER = r"\subsection{The ethos}"

W33_SECTION_INPUTS = [
    r"sections/sec_bt1083_1085_matter_bridge",
    r"sections/sec_bt1086_1088_core_reservoir",
    r"sections/sec_bt1089_1090_natural_core_intertwiner",
    r"sections/sec_bt1092_1093_explicit_quotient_cube",
    r"sections/sec_bt1095_1096_A12_K_matrix",
]

HOLONET_SECTION_INPUTS = [
    r"paper/sections/sec_bt1083_1085_holonet_bridge",
    r"paper/sections/sec_bt1086_1088_holonet_reservoir_runtime",
    r"paper/sections/sec_bt1089_1090_holonet_core_intertwiner",
    r"paper/sections/sec_bt1092_1093_holonet_quotient_cube",
    r"paper/sections/sec_bt1095_1096_holonet_A12_K_matrix",
]


def tex_path(input_name: str, base: Path) -> Path:
    p = base / input_name
    if p.suffix != ".tex":
        p = p.with_suffix(".tex")
    return p


def simple_brace_balance(text: str) -> int:
    # Ignore escaped braces.
    cleaned = text.replace(r"\{", "").replace(r"\}", "")
    return cleaned.count("{") - cleaned.count("}")


def main() -> None:
    errors: list[str] = []

    w33 = ROOT / "paper" / "w33_preprint.tex"
    holonet = ROOT / "photonic_holonet.tex"
    helper = ROOT / "tools" / "bt1100_integrate_all_latest_sections.py"

    if not w33.exists():
        errors.append(f"missing {w33}")
    elif W33_MARKER not in w33.read_text(encoding="utf-8"):
        errors.append(f"missing W33 marker {W33_MARKER}")

    if not holonet.exists():
        errors.append(f"missing {holonet}")
    elif HOLONET_MARKER not in holonet.read_text(encoding="utf-8"):
        errors.append(f"missing holonet marker {HOLONET_MARKER}")

    if not helper.exists():
        errors.append(f"missing latest integration helper {helper}")

    section_files: list[Path] = []
    for inp in W33_SECTION_INPUTS:
        p = tex_path(inp, ROOT / "paper")
        section_files.append(p)
        if not p.exists():
            errors.append(f"missing W33 input target {p}")
    for inp in HOLONET_SECTION_INPUTS:
        p = tex_path(inp, ROOT)
        section_files.append(p)
        if not p.exists():
            errors.append(f"missing holonet input target {p}")

    labels: dict[str, Path] = {}
    for p in section_files:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        bal = simple_brace_balance(text)
        if bal != 0:
            errors.append(f"brace imbalance {bal:+d} in {p}")
        for label in re.findall(r"\\label\{([^}]+)\}", text):
            if label in labels:
                errors.append(f"duplicate label {label}: {labels[label]} and {p}")
            labels[label] = p

    if errors:
        print("BT1100 TeX/path sanity check FAILED")
        for e in errors:
            print(f" - {e}")
        raise SystemExit(1)

    print("BT1100 TeX/path sanity check passed")
    print(f"checked_section_files={len(section_files)}")
    print(f"checked_labels={len(labels)}")


if __name__ == "__main__":
    main()
