#!/usr/bin/env python3
"""Idempotently integrate Passes 2962/2965 into blueprint and live atlas.

The two paper wrappers are updated directly in the release branch.  This helper
handles the very large holonet_machine_blueprint.tex and docs/index.html files
without rewriting them through a connector.  It fails closed when the expected
end anchors are absent and supports --root for isolated tests.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

BLUEPRINT_INPUT = r"\input{analysis/BT2962_BT2965_spread_curvature_route_code_blueprint_insert}"
HTML_MARKER = "<!-- BT2962-BT2965-SPREAD-CURVATURE-ROUTE-CODE-V1 -->"
HTML_SECTION = r'''
<!-- BT2962-BT2965-SPREAD-CURVATURE-ROUTE-CODE-V1 -->
<section id="bt2962-bt2965-spread-curvature" style="max-width:1100px;margin:3rem auto;padding:1.5rem;border:1px solid #6f7f91;border-radius:12px;">
  <h2>Latest exact result: spread curvature and route checking</h2>
  <p><strong>Pass 2962.</strong> Every one of the 36 W(3,3) spreads gives the same gauge-invariant parity curvature on its ten router modes. The 60 odd triangle holonomies form the exceptional ten-point two-graph; its switching class contains the Petersen graph and its full automorphism group is PΣL(2,9) ≅ S<sub>6</sub> of order 720. Every four-mode tetrahedron satisfies the exact discrete Bianchi identity.</p>
  <p><strong>Pass 2965.</strong> Comparing observed triangle parity with the certified baseline gives a binary [45,9,9] gauge code. The 120 triangle checks have rank 36, all non-gauge parity faults through weight 8 are detected, and all faults through weight 4 are correctable modulo local slot gauge.</p>
  <p><strong>Boundary.</strong> These are exact finite routing statements, not measured optical Berry phases, crosstalk results, or continuum gauge-field claims.</p>
  <p><code>python analysis/bt2962_oam_holonomy_s6_two_graph.py</code><br>
     <code>python analysis/bt2965_curvature_route_code.py</code></p>
</section>
'''.strip()


def insert_before(text: str, anchor: str, payload: str, marker: str) -> tuple[str, bool]:
    if marker in text:
        return text, False
    if anchor not in text:
        raise RuntimeError(f"required anchor missing: {anchor!r}")
    return text.replace(anchor, payload + "\n" + anchor, 1), True


def integrate(root: Path, check_only: bool = False) -> dict:
    blueprint = root / "holonet_machine_blueprint.tex"
    index = root / "docs" / "index.html"
    if not blueprint.is_file():
        raise FileNotFoundError(blueprint)
    if not index.is_file():
        raise FileNotFoundError(index)

    blueprint_text = blueprint.read_text(encoding="utf-8")
    index_text = index.read_text(encoding="utf-8")

    new_blueprint, changed_blueprint = insert_before(
        blueprint_text,
        r"\end{document}",
        BLUEPRINT_INPUT,
        BLUEPRINT_INPUT,
    )
    new_index, changed_index = insert_before(
        index_text,
        "</body>",
        HTML_SECTION,
        HTML_MARKER,
    )

    if check_only:
        if changed_blueprint or changed_index:
            raise SystemExit("Passes 2962/2965 are not fully integrated")
    else:
        if changed_blueprint:
            blueprint.write_text(new_blueprint, encoding="utf-8", newline="\n")
        if changed_index:
            index.write_text(new_index, encoding="utf-8", newline="\n")

    return {
        "blueprint_changed": changed_blueprint,
        "index_changed": changed_index,
        "blueprint_integrated": BLUEPRINT_INPUT in new_blueprint,
        "index_integrated": HTML_MARKER in new_index,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = integrate(args.root.resolve(), args.check)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
