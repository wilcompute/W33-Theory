"""Audit qutrit scripts against the corrected CCT trit-savings rule.

The repo has many qutrit-adjacent scripts.  CCT trit savings, however, is not
just q=3 compression: in Klee's quasicrystal game-of-life layer it is the
least-change/maximum-empire-overlap path through allowed same-type neighbor
moves.  This scanner inventories qutrit and quasicrystal scripts against that
corrected criterion.
"""

from __future__ import annotations

import json
import re
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
SCAN_ROOTS = ("scripts", "exploration", "tools")
SCRIPT_SUFFIXES = {".py", ".sage"}

CRITERIA_PATTERNS = {
    "qutrit_core_language": (
        r"\bqutrits?\b",
        r"\btwo[- ]qutrit",
        r"\btrits?\b",
        r"\bq\s*=\s*3\b",
        r"\bF_?3\b",
    ),
    "two_qutrit_w33_bridge": (
        r"W\(3,3\)",
        r"GQ\(3,3\)",
        r"\bW33\b",
        r"\bPauli\b",
        r"\bcommut",
        r"\bSRG\(40,\s*12,\s*2,\s*4\)",
        r"\b240\b",
    ),
    "quasicrystal_carrier": (
        r"\bquasicrystal",
        r"\bPenrose\b",
        r"\bFIG\b",
        r"Fibonacci IcosaGrid",
        r"cut[- ]and[- ]project",
        r"perpendicular space",
        r"mother lattice",
    ),
    "empire_possibility_windows": (
        r"\bempire\b",
        r"empire[- ]window",
        r"possibility[- ]space",
        r"possibility[- ]space[- ]window",
        r"cut[- ]window",
    ),
    "least_change_trit_savings_rule": (
        r"least change",
        r"trits?[- ]saving",
        r"maximum trits?[- ]saving",
        r"changed tiles",
        r"cut[- ]window shifts",
        r"argmax_i",
        r"E0\s+intersect\s+Ei",
    ),
    "neighbor_clock_packet": (
        r"\beight\b.*\bneighbors?\b",
        r"\b8\b.*\bneighbors?\b",
        r"K[- ]neighbors?",
        r"\bclockwise\b",
        r"\bcounterclockwise\b",
        r"\b4\+4\b",
        r"K\s*[-=]\s*MU",
        r"K\s*-\s*mu",
    ),
}

COMPILED_CRITERIA_PATTERNS = {
    name: tuple(re.compile(pattern, re.IGNORECASE) for pattern in patterns)
    for name, patterns in CRITERIA_PATTERNS.items()
}

RELEVANCE_REGEXES = (
    r"\bqutrits?\b",
    r"\btwo[- ]qutrit",
    r"\btrits?\b",
    r"trits?[- ]saving",
    r"least change",
    r"\bquasicrystal",
    r"\bPenrose\b",
    r"\bFIG\b",
    r"Fibonacci IcosaGrid",
    r"possibility[- ]space",
    r"empire[- ]window",
)

RELEVANCE_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE) for pattern in RELEVANCE_REGEXES
)


def _script_files() -> Iterable[Path]:
    for root_name in SCAN_ROOTS:
        root = ROOT / root_name
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if any(part in {"__pycache__", ".venv"} for part in path.parts):
                continue
            if path.suffix in SCRIPT_SUFFIXES:
                yield path


def _rg_relevant_script_files() -> set[Path] | None:
    cmd = [
        "rg",
        "-l",
        "-i",
        "--glob",
        "*.py",
        "--glob",
        "*.sage",
        "--glob",
        "!**/__pycache__/**",
        "--glob",
        "!**/.venv/**",
    ]
    for pattern in RELEVANCE_REGEXES:
        cmd.extend(["-e", pattern])
    cmd.extend(SCAN_ROOTS)

    try:
        result = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    except (FileNotFoundError, OSError):
        return None

    if result.returncode not in {0, 1}:
        return None

    return {ROOT / line.strip() for line in result.stdout.splitlines() if line.strip()}


def _relevant_script_files() -> Iterable[Path]:
    rg_paths = _rg_relevant_script_files()
    if rg_paths is None:
        yield from _script_files()
        return

    for path in sorted(rg_paths):
        if path.is_file() and path.suffix in SCRIPT_SUFFIXES:
            yield path


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _is_relevant_script(path: Path, text: str) -> bool:
    haystack = f"{path.name}\n{text}"
    return any(pattern.search(haystack) for pattern in RELEVANCE_PATTERNS)


def classify_qutrit_script(path: Path, text: str) -> Dict[str, object]:
    rel = path.relative_to(ROOT).as_posix()
    haystack = f"{rel}\n{text}"
    criteria = {
        name: any(pattern.search(haystack) for pattern in compiled)
        for name, compiled in COMPILED_CRITERIA_PATTERNS.items()
    }

    quasicrystal_savings_ready = (
        criteria["quasicrystal_carrier"]
        and criteria["empire_possibility_windows"]
        and criteria["least_change_trit_savings_rule"]
    )
    w33_qutrit_ready = (
        criteria["qutrit_core_language"] and criteria["two_qutrit_w33_bridge"]
    )

    if (
        quasicrystal_savings_ready
        and w33_qutrit_ready
        and criteria["neighbor_clock_packet"]
    ):
        alignment = "complete_cct_quasicrystal_trit_savings_spine"
    elif quasicrystal_savings_ready:
        alignment = "direct_quasicrystal_trit_savings_missing_w33_qutrit_bridge"
    elif w33_qutrit_ready:
        alignment = "qutrit_w33_core_missing_quasicrystal_trit_savings_layer"
    elif criteria["quasicrystal_carrier"]:
        alignment = "quasicrystal_context_missing_explicit_trit_savings_rule"
    else:
        alignment = "partial_qutrit_context"

    return {
        "path": rel,
        "criteria": criteria,
        "matched_criteria_count": sum(1 for value in criteria.values() if value),
        "alignment": alignment,
    }


@lru_cache(maxsize=1)
def build_qutrit_script_savings_audit() -> Dict[str, object]:
    """Scan relevant scripts and classify their corrected CCT trit-savings alignment."""
    records: List[Dict[str, object]] = []
    for path in _relevant_script_files():
        text = _read_text(path)
        if _is_relevant_script(path, text):
            records.append(classify_qutrit_script(path, text))

    records.sort(key=lambda item: (str(item["alignment"]), str(item["path"])))
    alignment_counts: Dict[str, int] = {}
    for record in records:
        alignment = str(record["alignment"])
        alignment_counts[alignment] = alignment_counts.get(alignment, 0) + 1

    missing_quasicrystal_layer = [
        str(record["path"])
        for record in records
        if record["alignment"]
        == "qutrit_w33_core_missing_quasicrystal_trit_savings_layer"
    ]
    missing_w33_bridge = [
        str(record["path"])
        for record in records
        if record["alignment"]
        == "direct_quasicrystal_trit_savings_missing_w33_qutrit_bridge"
    ]
    partial = [
        str(record["path"])
        for record in records
        if record["alignment"]
        in {
            "quasicrystal_context_missing_explicit_trit_savings_rule",
            "partial_qutrit_context",
        }
    ]

    allowed_alignments = {
        "complete_cct_quasicrystal_trit_savings_spine",
        "direct_quasicrystal_trit_savings_missing_w33_qutrit_bridge",
        "qutrit_w33_core_missing_quasicrystal_trit_savings_layer",
        "quasicrystal_context_missing_explicit_trit_savings_rule",
        "partial_qutrit_context",
    }

    return {
        "inventory": {
            "scan_roots": SCAN_ROOTS,
            "audited_script_count": len(records),
            "qutrit_or_quasicrystal_script_count": len(records),
            "alignment_counts": alignment_counts,
        },
        "criteria": tuple(CRITERIA_PATTERNS.keys()),
        "records": tuple(records),
        "priority_gaps": {
            "qutrit_w33_core_scripts_missing_quasicrystal_trit_savings_layer": tuple(
                missing_quasicrystal_layer
            ),
            "quasicrystal_savings_scripts_missing_w33_qutrit_bridge": tuple(
                missing_w33_bridge
            ),
            "partial_context_scripts_needing_manual_review": tuple(partial),
        },
        "theorem": {
            "relevant_scripts_were_scanned": len(records) > 0,
            "quasicrystal_trit_savings_bridge_is_complete": any(
                record["path"] == "scripts/w33_cct_quasicrystal_trit_savings_audit.py"
                and record["alignment"]
                == "complete_cct_quasicrystal_trit_savings_spine"
                for record in records
            ),
            "qutrit_core_bridge_is_detected_as_owner_not_full_savings_rule": any(
                record["path"] == "scripts/w33_cct_qutrit_core_bridge_audit.py"
                and record["alignment"]
                == "qutrit_w33_core_missing_quasicrystal_trit_savings_layer"
                for record in records
            ),
            "two_qutrit_pauli_script_is_detected": any(
                record["path"] == "scripts/w33_two_qutrit_pauli.py"
                for record in records
            ),
            "scripts_have_actionable_quasicrystal_trit_savings_classification": all(
                record["alignment"] in allowed_alignments for record in records
            ),
        },
    }


if __name__ == "__main__":
    print(json.dumps(build_qutrit_script_savings_audit(), indent=2))
