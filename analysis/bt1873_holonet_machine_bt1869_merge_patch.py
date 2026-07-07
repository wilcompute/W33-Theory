#!/usr/bin/env python3
"""BT1873: holonet_machine.tex merge patch for BT1869.

Builds a reproducible patch path for inserting the merged selector/glue subsection
into holonet_machine.tex after the compiled defect runtime stack result.
"""
from __future__ import annotations

import json
from pathlib import Path

TEX = Path("holonet_machine.tex")
OUT = Path("data/PART_BT1873_HOLONET_MACHINE_BT1869_MERGE_PATCH_results.json")

ANCHOR = "\\path{bt1824_executable_packet_replay}, \\path{bt1825_aperture_shot_table_exporter}.\n\\end{result}"

INSERT = r"""

\subsection{Metric-canonical selector and the remaining sign-kernel lift}
The E8-side selector used by the runtime aperture stack is canonical at every quotient level visible on
the mod-$2$ support shadow.  Exact support recursion lowers the old support-$76$ candidate to the true
support minimum $60$, with six minimizers.  The vertex metric selects minimizer $2$, and the recovered
chain-to-tetracode matrix independently selects the same minimizer in the tetracode metric gauge.  The
selected basis is
\[
  (3,68),\quad (4,42),\quad (38,65),\quad (90,144).
\]
The transported block-permutation quotient is $S_4$ of order $24$; acting on the selected support-$60$
minimizer it has orbit size $24$, trivial stabilizer, and intersection with the six support-$60$
minimizers only at the selected minimizer.  The tetracode-coordinate glue stabilizer has the exact split
\[
  |G_{\mathrm{glue}}|=48=2\cdot24.
\]
The $24$-part is the transported $S_4$ quotient.  The remaining size-$2$ sign kernel is represented, at
lattice-bookkeeping level, by the central inversion $-I$ in $O(A_2)/W(A_2)$ on each of the four $A_2$
planes.  It preserves the $A_2$ Gram form and fixes the winner-$2$ support mask because it reduces to the
identity mod $2$.  The remaining open layer is the concrete integral E8 chain representative for that
central-inversion phase action.
"""


def apply_patch(text: str) -> tuple[str, bool]:
    if "Metric-canonical selector and the remaining sign-kernel lift" in text:
        return text, False
    if ANCHOR not in text:
        raise ValueError("compiled runtime stack anchor not found")
    return text.replace(ANCHOR, ANCHOR + INSERT, 1), True


def theorem_summary(apply: bool = False):
    text = TEX.read_text(encoding="utf-8")
    new_text, changed = apply_patch(text)
    if apply and changed:
        TEX.write_text(new_text, encoding="utf-8")
    return {
        "theorem": "BT1873 Holonet Machine BT1869 Merge Patch",
        "target": str(TEX),
        "anchor_found": ANCHOR in text,
        "already_merged": not changed,
        "would_insert_BT1869_subsection": changed,
        "apply_mode": apply,
        "insert_contains": {
            "canonical_selector": "(3,68)" in INSERT and "(90,144)" in INSERT,
            "glue_split_48": "48=2\\cdot24" in INSERT,
            "central_inversion_OA2": "O(A_2)/W(A_2)" in INSERT,
            "final_boundary": "integral E8 chain representative" in INSERT
        },
        "checks": {
            "anchor_found": ANCHOR in text,
            "insert_has_selector": "(3,68)" in INSERT and "(90,144)" in INSERT,
            "insert_has_glue_split": "48=2\\cdot24" in INSERT,
            "insert_has_central_inversion_wording": "central inversion" in INSERT and "O(A_2)/W(A_2)" in INSERT
        },
        "honest_scope": "Patch witness. It does not rewrite holonet_machine.tex unless run with apply=True in a repo checkout."
    }


def main() -> int:
    summary = theorem_summary(apply=False)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if all(summary["checks"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
