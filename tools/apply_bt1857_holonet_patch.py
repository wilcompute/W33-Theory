#!/usr/bin/env python3
"""BT1863 — local Holonet TeX splice script.

Applies papers/BT1857_holonet_k12_compiler_patch.tex into
papers/BT1347_photonic_holonet_journal.tex immediately before
\section{Discussion and Open Questions}.

The script is intentionally conservative:
- it refuses to run if the insertion marker is missing;
- it refuses to double-insert the patch;
- it writes a new integrated file instead of overwriting the source;
- it performs simple syntax sanity checks on balanced \begin/\end counts.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "papers" / "BT1347_photonic_holonet_journal.tex"
PATCH = ROOT / "papers" / "BT1857_holonet_k12_compiler_patch.tex"
OUT = ROOT / "papers" / "BT1347_photonic_holonet_journal_with_BT1857.tex"
MARKER = r"\section{Discussion and Open Questions}"
LABEL = r"\label{sec:k12-f12-compiler}"


def count_token(text: str, token: str) -> int:
    return text.count(token)


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    patch = PATCH.read_text(encoding="utf-8")

    if MARKER not in source:
        raise SystemExit(f"missing insertion marker: {MARKER}")
    if LABEL in source:
        raise SystemExit("patch label already appears in source; refusing double insertion")
    if LABEL not in patch:
        raise SystemExit("patch label missing from patch file")

    integrated = source.replace(MARKER, patch.rstrip() + "\n\n" + MARKER, 1)

    for env in ["definition", "theorem", "remark", "table", "ruledtabular", "tabular", "enumerate"]:
        b = count_token(integrated, rf"\begin{{{env}}}")
        e = count_token(integrated, rf"\end{{{env}}}")
        if b != e:
            raise SystemExit(f"unbalanced environment {env}: begin={b}, end={e}")

    if r"\begin{enumerate}[nosep]" in integrated:
        raise SystemExit("enumitem-only [nosep] option found")

    OUT.write_text(integrated, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print("BT1863 sanity checks passed")


if __name__ == "__main__":
    main()
