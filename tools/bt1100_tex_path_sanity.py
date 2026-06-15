#!/usr/bin/env python3
"""BT1126 no-network TeX/path sanity check for main W33 paper."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W33_MARKER = r"\end{document}"
HOLONET_MARKER = r"\subsection{The ethos}"

W33_SECTION_INPUTS = [
    r"paper/sections/sec_bt1083_1085_matter_bridge",
    r"paper/sections/sec_bt1086_1088_core_reservoir",
    r"paper/sections/sec_bt1089_1090_natural_core_intertwiner",
    r"paper/sections/sec_bt1092_1093_explicit_quotient_cube",
    r"paper/sections/sec_bt1095_1096_A12_K_matrix",
    r"paper/sections/sec_bt1098_1100_realform_spectrum_ci",
    r"paper/sections/sec_bt1101_1102_whitening_structure",
    r"paper/sections/sec_bt1104_1106_projector_coupling_report",
    r"paper/sections/sec_bt1107_1109_coupling_generation_report",
    r"paper/sections/sec_bt1110_1112_weight_closure_report",
    r"paper/sections/sec_bt1113_1116_weight_coupling_factorization",
    r"paper/sections/sec_bt1117_1119_k3_yukawa_patch_report",
    r"paper/sections/sec_bt1120_1122_k3_yukawa_build_path",
    r"paper/sections/sec_bt1126_1128_mainpaper_fixture_numeric",
]
HOLONET_SECTION_INPUTS = [
    r"paper/sections/sec_bt1083_1085_holonet_bridge",
    r"paper/sections/sec_bt1086_1088_holonet_reservoir_runtime",
    r"paper/sections/sec_bt1089_1090_holonet_core_intertwiner",
    r"paper/sections/sec_bt1092_1093_holonet_quotient_cube",
    r"paper/sections/sec_bt1095_1096_holonet_A12_K_matrix",
    r"paper/sections/sec_bt1098_1100_holonet_realform_spectrum_ci",
    r"paper/sections/sec_bt1101_1102_holonet_whitening_structure",
    r"paper/sections/sec_bt1104_1106_holonet_projector_coupling_report",
    r"paper/sections/sec_bt1107_1109_holonet_coupling_generation_report",
    r"paper/sections/sec_bt1110_1112_holonet_weight_closure_report",
    r"paper/sections/sec_bt1113_1116_holonet_weight_coupling_factorization",
    r"paper/sections/sec_bt1117_1119_holonet_k3_yukawa_patch_report",
    r"paper/sections/sec_bt1120_1122_holonet_k3_yukawa_build_path",
    r"paper/sections/sec_bt1126_1128_holonet_mainpaper_fixture_numeric",
]


def tex_path(input_name: str) -> Path:
    p = ROOT / input_name
    return p if p.suffix == ".tex" else p.with_suffix(".tex")


def simple_brace_balance(text: str) -> int:
    cleaned = text.replace(r"\{", "").replace(r"\}", "")
    return cleaned.count("{") - cleaned.count("}")


def main() -> None:
    errors: list[str] = []
    w33 = ROOT / "w33_paper.tex"
    holonet = ROOT / "photonic_holonet.tex"

    if not w33.exists() or W33_MARKER not in w33.read_text(encoding="utf-8"):
        errors.append("missing main W33 source or end marker")
    if not holonet.exists() or HOLONET_MARKER not in holonet.read_text(encoding="utf-8"):
        errors.append("missing holonet source or ethos marker")

    labels: dict[str, Path] = {}
    section_files = [tex_path(x) for x in W33_SECTION_INPUTS + HOLONET_SECTION_INPUTS]
    for p in section_files:
        if not p.exists():
            errors.append(f"missing input target {p}")
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
        print("BT1126 TeX/path sanity check FAILED")
        for e in errors:
            print(f" - {e}")
        raise SystemExit(1)
    print("BT1126 TeX/path sanity check passed")
    print(f"checked_section_files={len(section_files)}")
    print(f"checked_labels={len(labels)}")


if __name__ == "__main__":
    main()
