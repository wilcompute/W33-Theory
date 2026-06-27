#!/usr/bin/env python3
"""BT1883 — local Holonet TeX splice script.

Applies both patch sections into papers/BT1347_photonic_holonet_journal.tex:
1. papers/BT1857_holonet_k12_compiler_patch.tex
2. papers/BT1880_holonet_finite_css_theorem_patch.tex

The combined block is inserted immediately before \section{Discussion and Open Questions}.

The script is conservative:
- it refuses to run if the insertion marker is missing;
- it refuses to double-insert either patch label;
- it writes a new integrated file instead of overwriting the source;
- it performs simple syntax sanity checks on balanced \begin/\end counts;
- it rejects enumitem-only enumerate options.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "papers" / "BT1347_photonic_holonet_journal.tex"
PATCHES = [
    ROOT / "papers" / "BT1857_holonet_k12_compiler_patch.tex",
    ROOT / "papers" / "BT1880_holonet_finite_css_theorem_patch.tex",
]
OUT = ROOT / "papers" / "BT1347_photonic_holonet_journal_with_BT1857_BT1880.tex"
MARKER = r"\section{Discussion and Open Questions}"
LABELS = [
    r"\label{sec:k12-f12-compiler}",
    r"\label{sec:k12-f12-css-code}",
]


def count_token(text: str, token: str) -> int:
    return text.count(token)


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")

    if MARKER not in source:
        raise SystemExit(f"missing insertion marker: {MARKER}")

    patches = []
    for patch_path, label in zip(PATCHES, LABELS):
        patch = patch_path.read_text(encoding="utf-8")
        if label in source:
            raise SystemExit(f"patch label already appears in source; refusing double insertion: {label}")
        if label not in patch:
            raise SystemExit(f"patch label missing from patch file {patch_path}: {label}")
        patches.append(patch.rstrip())

    combined_patch = "\n\n".join(patches)
    integrated = source.replace(MARKER, combined_patch + "\n\n" + MARKER, 1)

    for env in ["definition", "theorem", "proof", "corollary", "remark", "table", "ruledtabular", "tabular", "enumerate"]:
        b = count_token(integrated, rf"\begin{{{env}}}")
        e = count_token(integrated, rf"\end{{{env}}}")
        if b != e:
            raise SystemExit(f"unbalanced environment {env}: begin={b}, end={e}")

    if r"\begin{enumerate}[nosep]" in integrated:
        raise SystemExit("enumitem-only [nosep] option found")

    if LABELS[0] not in integrated or LABELS[1] not in integrated:
        raise SystemExit("one or more expected patch labels missing after splice")

    OUT.write_text(integrated, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print("BT1883 sanity checks passed")


if __name__ == "__main__":
    main()
