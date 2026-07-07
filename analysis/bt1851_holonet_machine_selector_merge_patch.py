#!/usr/bin/env python3
"""BT1851: direct holonet_machine.tex merge patch for the E8 selector upgrade.

Applies the BT1849 tetracode selector upgrade insert directly after the compiled
defect runtime stack result. Kept as a patcher so the paper can be merged
reproducibly without hand-editing the full TeX file in a connector pass.
"""
from __future__ import annotations

import json
from pathlib import Path

TEX = Path("holonet_machine.tex")
OUT = Path("data/PART_BT1851_HOLONET_MACHINE_SELECTOR_MERGE_PATCH_results.json")

INSERT = r"""

\begin{result}[Metric-canonical E8 selector]
The E8-side selector attached to the runtime aperture stack is now canonical at the strongest transported quotient currently available.  Exact support recursion lowers the old support-76 candidate to support 60 with six minimizers; the vertex metric selects minimizer 2; the recovered chain-to-tetracode matrix independently selects the same minimizer in the tetracode metric gauge; and the transported tetracode block-permutation quotient $S_4$ gives a 24-element orbit with trivial stabilizer whose intersection with the six support-60 minimizers is only the selected minimizer.  The canonical selector is
\[
  (3,68),\quad (4,42),\quad (38,65),\quad (90,144).
\]
These four pairs label the four runtime striations used by the aperture table, compiled trace schema, and shot protocol.

\emph{Boundary.} This closes the metric selector and transported $S_4$ quotient.  It does not yet close the full local $A_2$/Weyl/glue stabilizer refinement, which requires intersecting the four-plane $W(A_2)^4$ action with the tetracode code-glue stabilizer and transporting the survivor to the chain model.

Witnesses: \path{bt954_metric_selector_among_support60}, \path{bt956_tetracode_metric_selector_matrix}, \path{bt959_selected_minimizer_stabilizer_orbit}, \path{bt1845_tetracode_stabilizer_action_audit}, and \path{bt1846_winner2_canonical_basis_export}.
\end{result}
"""

ANCHOR = "\\path{bt1824_executable_packet_replay}, \\path{bt1825_aperture_shot_table_exporter}.\n\\end{result}"


def apply_patch(text: str) -> tuple[str, bool]:
    if "Metric-canonical E8 selector" in text:
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
        "theorem": "BT1851 Holonet Machine Selector Merge Patch",
        "target": str(TEX),
        "anchor_found": ANCHOR in text,
        "already_merged": not changed,
        "would_insert_metric_canonical_selector": changed,
        "apply_mode": apply,
        "checks": {
            "anchor_found": ANCHOR in text,
            "insert_has_canonical_selector": "(3,68)" in INSERT and "(90,144)" in INSERT,
            "local_A2_boundary_present": "A_2" in INSERT,
            "witnesses_present": "bt959_selected_minimizer_stabilizer_orbit" in INSERT
        },
        "honest_scope": "Patch witness. Run with apply=True or adapt as a script to modify holonet_machine.tex in a local repo checkout."
    }


def main() -> int:
    summary = theorem_summary(apply=False)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if all(summary["checks"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
