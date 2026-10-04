#!/usr/bin/env python3
"""Fail-closed, idempotent integration for Passes 2974-2983."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED = r"    \input{analysis/BT2974_BT2983_nonabelian_golden_information_insert}%"
WRAPPER_ANCHOR = "  }%\n}\n\\input{"

BLUEPRINT_BLOCK = r'''
% BEGIN BT2974-BT2983 NONABELIAN GOLDEN INFORMATION
\input{analysis/BT2974_BT2983_nonabelian_golden_information_blueprint_insert}
% END BT2974-BT2983 NONABELIAN GOLDEN INFORMATION
'''.strip()

HTML_BLOCK = r'''
<!-- BEGIN BT2974-BT2983 NONABELIAN GOLDEN INFORMATION -->
<section id="bt2974-bt2983-nonabelian-golden-information">
  <h2>Passes 2974–2983: nonabelian route memory and golden control</h2>
  <p>The complete ten-mode route connection is thirty-six <code>D4</code> chord holonomies modulo one simultaneous conjugation. Its binary curvature is only an outer syndrome. The same curvature is constructively the exceptional ten-point <code>S6</code> two-graph.</p>
  <p>The shortest expanding <code>R4/U6</code> word with a rational quotient is <code>R4^2 U6</code>, whose quotient is Fibonacci. It yields a balanced golden scheduler and an <code>A4</code> parity shell, but cannot lift to the protected <code>D4</code> core.</p>
  <p>The general-isotropic three-copy M36 search is partitioned into 495 duplicate-free shards. A 649,940-subspace non-CSS pilot found six collinearity projectors, all stabilizer false leads; the complete 213,648,435-subspace sweep remains open.</p>
</section>
<!-- END BT2974-BT2983 NONABELIAN GOLDEN INFORMATION -->
'''.strip()


def insert_wrapper(path: Path) -> bool:
    text = path.read_text()
    if SHARED in text:
        return False
    if WRAPPER_ANCHOR not in text:
        raise RuntimeError(f"wrapper anchor drifted in {path}")
    path.write_text(text.replace(WRAPPER_ANCHOR, SHARED + "\n" + WRAPPER_ANCHOR, 1))
    return True


def insert_before(path: Path, block: str, sentinel: str, closing: str) -> bool:
    text = path.read_text()
    if sentinel in text:
        return False
    if closing not in text:
        raise RuntimeError(f"closing anchor {closing!r} missing from {path}")
    path.write_text(text.replace(closing, block + "\n" + closing, 1))
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    changed: list[str] = []
    for name in ("w33_paper.tex", "photonic_holonet.tex"):
        path = ROOT / name
        if insert_wrapper(path):
            changed.append(name)
    if insert_before(
        ROOT / "holonet_machine_blueprint.tex",
        BLUEPRINT_BLOCK,
        "BEGIN BT2974-BT2983 NONABELIAN GOLDEN INFORMATION",
        "\\end{document}",
    ):
        changed.append("holonet_machine_blueprint.tex")
    if insert_before(
        ROOT / "docs" / "index.html",
        HTML_BLOCK,
        "BEGIN BT2974-BT2983 NONABELIAN GOLDEN INFORMATION",
        "</body>",
    ):
        changed.append("docs/index.html")

    if args.check and changed:
        raise SystemExit(f"integration was not idempotent; changed {changed}")
    print({"changed": changed, "idempotent": not changed})


if __name__ == "__main__":
    main()
