#!/usr/bin/env python3
"""Pass 3193: machine-readable month-wide theorem genealogy and stale-claim audit."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3193_MONTH_CLAIM_GENEALOGY_results.json"
FRONT_DOORS = ("w33_paper.tex", "photonic_holonet.tex", "holonet_machine_blueprint.tex", "docs/index.html")

CLAIMS = [
    {
        "id": "m36_fixed_gauge_no_go",
        "early": "fixed logical-Pauli gauge found no improving two-copy branch",
        "correction": "full 11,520 logical-Clifford decoder census finds 48 improving deep-grade branches",
        "status": "superseded_scope",
        "anchors": ["fixed-gauge", "48 improving", "11,520"],
    },
    {
        "id": "witting_three_representatives",
        "early": "three resource representatives",
        "correction": "four Clifford classes with sizes 4,8,12,12; the two middle classes are inequivalent",
        "status": "corrected",
        "anchors": ["4+8+12+12", "[4, 8, 12, 12]", "two middle"],
    },
    {
        "id": "rank_two_subspace_is_code",
        "early": "rank-two six-qubit witnesses treated as stabilizer codes",
        "correction": "common same-sign Pauli rank is three, not the rank five required for a rank-two six-qubit stabilizer code",
        "status": "refuted",
        "anchors": ["rank five", "not stabilizer codes", "common same-sign Pauli rank"],
    },
    {
        "id": "chirality_helstrom_label",
        "early": "0.788675 labelled as the one-copy Helstrom success",
        "correction": "0.788675 is the selected local-Pauli receiver; unrestricted one-copy Helstrom success is 0.908248",
        "status": "corrected",
        "anchors": ["0.908248", "selected Pauli receiver", "not the Helstrom"],
    },
    {
        "id": "instruction_graph_irregularity_structural",
        "early": "degree collapse interpreted as structural for every generator choice",
        "correction": "one regular four-generator graph exists, but it is the translation-only noncomputing set",
        "status": "corrected",
        "anchors": ["translation-only", "ONE gives a regular", "cannot perform a single Clifford"],
    },
    {
        "id": "collision18_universal_compute",
        "early": "18-collision frame-connected set called a computing minimum",
        "correction": "that set generates affine order 243; exact universal minimum is 36 collisions",
        "status": "withdrawn",
        "anchors": ["order 243", "minimum universal collision", "36-collision"],
    },
    {
        "id": "ihara_bass_first_two_attempts",
        "early": "regular-graph formula and misoriented linearisation produced incompatible pole claims",
        "correction": "K4 reference validation fixed the Bass routine before the nonregular 81-frame graph was measured",
        "status": "withdrawn_and_recomputed",
        "anchors": ["K_4", "linearisation orientation", "validated before"],
    },
    {
        "id": "support_is_execution_congruence",
        "early": "15-state support quotient read as a deterministic execution state",
        "correction": "micro-ISA refinement is 16 to 40 to 78 to 81; support is for readout and ternary phase for execution",
        "status": "refuted",
        "anchors": ["16 -> 40 -> 78 -> 81", "support for readout", "phase for execution"],
    },
    {
        "id": "route_time_product_is_joint_code",
        "early": "route and clock product described as a joint error-correcting code",
        "correction": "all noiseless states are injective but route minimum distance is one; it is synchronization plus localization",
        "status": "refuted",
        "anchors": ["route minimum distance", "synchronization plus localization", "not a joint"],
    },
    {
        "id": "blind_insdel_acquisition",
        "early": "bounded edit tracking implicitly treated as blind acquisition",
        "correction": "adjacent phase-word edit balls intersect without an epoch; phase-coded delimiters are required",
        "status": "corrected",
        "anchors": ["trusted epoch", "edit balls intersect", "phase-coded"],
    },
    {
        "id": "missing_m36_inputs_are_no_go",
        "early": "absence of candidate files risked being read as exhaustive failure",
        "correction": "NO_INPUTS_DISCOVERED and partial zero-hit states are non-results until every shard and independent certifier complete",
        "status": "governance_hardened",
        "anchors": ["NO_INPUTS_DISCOVERED", "not a no-go", "partial zero-hit"],
    },
    {
        "id": "source_complete_equals_observed",
        "early": "source completion, queued CI, placement and PDF publication were occasionally conflated",
        "correction": "proved, modelled, simulated, synthesized, placed, compiled and measured claims are separately typed",
        "status": "governance_hardened",
        "anchors": ["source-complete", "evidence gate", "not claimed until observed"],
    },
]


def git_log() -> str:
    command = ["git", "log", "--all", "--since=2026-07-04", "--pretty=format:%H%x09%s%x09%b"]
    try:
        return subprocess.run(command, cwd=ROOT, check=True, text=True, capture_output=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def front_door_text() -> dict[str, str]:
    result = {}
    for relative in FRONT_DOORS:
        path = ROOT / relative
        if path.exists():
            result[relative] = path.read_text(encoding="utf-8", errors="surrogateescape")
    return result


def main() -> None:
    log = git_log()
    doors = front_door_text()
    rows = []
    for claim in CLAIMS:
        commit_hits = sorted({anchor for anchor in claim["anchors"] if anchor.lower() in log.lower()})
        door_hits = {
            path: sorted({anchor for anchor in claim["anchors"] if anchor.lower() in text.lower()})
            for path, text in doors.items()
        }
        rows.append(dict(claim, commit_anchor_hits=commit_hits, front_door_anchor_hits=door_hits))

    high_risk_literals = {
        "unqualified_18_collision_minimum": re.compile(r"minimum(?:-collision| collision).*18", re.I),
        "unqualified_0788675_helstrom": re.compile(r"Helstrom[^\n]{0,80}0\.788675|0\.788675[^\n]{0,80}Helstrom", re.I),
        "support_execution_isomorphism": re.compile(r"support(?: quotient)? is (?:the )?execution", re.I),
        "missing_input_no_go": re.compile(r"NO_INPUTS_DISCOVERED[^\n]{0,80}(?:no-go|impossible)", re.I),
    }
    review_findings = []
    for path, text in doors.items():
        for label, pattern in high_risk_literals.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                context = text[max(0, match.start() - 120):match.end() + 120].replace("\n", " ")
                review_findings.append({"path": path, "line": line, "rule": label, "context": context})

    result = {
        "schema": "w33.pass3193.month_claim_genealogy.v1",
        "audit_window": {"start": "2026-07-04", "end": "2026-08-04"},
        "claim_families": len(rows),
        "relations": rows,
        "front_doors_scanned": sorted(doors),
        "high_risk_literal_findings_for_manual_review": review_findings,
        "policy": "A later exact correction supersedes only the scope it actually recomputes. Historical passages may remain, but canonical claims must link to the correcting node and preserve evidence type.",
        "boundary": "This is a repository claim-lineage compiler and stale-literal review surface. Regex hits are review prompts, not automatic mathematical verdicts; absence of a phrase is not proof of consistency."
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"claim_families": len(rows), "review_findings": len(review_findings)}, sort_keys=True))


if __name__ == "__main__":
    main()
