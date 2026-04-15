#!/usr/bin/env python3
"""
Audit "prediction" scripts for external-data / fitted-parameter usage.

This repo contains two kinds of computations:
  1) Internal mathematical certificates (purely derived from repo artifacts).
  2) Phenomenology / mapping scripts that compare to experimental numbers or
     include ad-hoc correction factors.

This script does NOT judge correctness. It only flags:
  - hard-coded experimental constants,
  - explicit "Experimental:" comparisons,
  - obvious ad-hoc correction factors,
  - whether a script reads from repo `data/` or `artifacts/`.

Outputs:
  - artifacts/prediction_script_audit.json
  - artifacts/prediction_script_audit.md
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
SRC = ROOT / "src"
OUT_JSON = ROOT / "artifacts" / "prediction_script_audit.json"
OUT_MD = ROOT / "artifacts" / "prediction_script_audit.md"


EXTERNAL_CONSTANT_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "planck_mass_GeV",
        re.compile(r"\b1\.22e19\b|\b1\.220e19\b|\b1\.22\s*\*\s*10\*\*19\b"),
    ),
    ("higgs_vev_246", re.compile(r"\b246(\.0+)?\b")),
    ("alpha_inv_137", re.compile(r"\b137\.0\d*\b")),
    ("alpha_s_MZ", re.compile(r"\b0\.1179\b|\b0\.118\b")),
    ("cabibbo_0p225", re.compile(r"\b0\.2253\b|\b0\.2252\b|\b0\.2250\b")),
    ("higgs_mass_125", re.compile(r"\b125\.1\b|\b125\.25\b|\b125\.3\b")),
    ("top_mass_173", re.compile(r"\b173(\.0+)?\b|\b172\.6\b|\b172\.7\b")),
    ("weinberg_0p231", re.compile(r"\b0\.2312\b|\b0\.23121\b")),
]


ADHOC_FACTOR_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "explicit_correction_factor",
        re.compile(r"\bcorrection\s*factor\b", re.IGNORECASE),
    ),
    ("magic_factor_0p6", re.compile(r"\b0\.6\b")),
    (
        "fudge_factor_words",
        re.compile(r"\b(fudge|tune|fit|calibrat)\w*\b", re.IGNORECASE),
    ),
    ("parameter_free_claim", re.compile(r"\bparameter[- ]free\b", re.IGNORECASE)),
]


@dataclass(frozen=True)
class ScriptAudit:
    path: str
    reads_repo_data: bool
    reads_repo_artifacts: bool
    mentions_experimental: bool
    external_constant_hits: list[str]
    adhoc_factor_hits: list[str]


def _iter_python_files(paths: Iterable[Path]) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        if not p.exists():
            continue
        if p.is_file() and p.suffix == ".py":
            out.append(p)
        elif p.is_dir():
            out.extend(sorted(p.glob("*.py")))
    return sorted(set(out))


def _audit_one(path: Path) -> ScriptAudit:
    text = path.read_text(encoding="utf-8", errors="replace")
    reads_repo_data = (
        ("data/" in text)
        or ("W33_ROOT" in text)
        or ("_toe/" in text)
        or ("_v23/" in text)
    )
    reads_repo_artifacts = ("artifacts/" in text) or ('ROOT / "artifacts"' in text)
    mentions_experimental = bool(re.search(r"\bExperimental\b|\bexperiment\b", text))

    external_hits = [
        name for name, pat in EXTERNAL_CONSTANT_PATTERNS if pat.search(text)
    ]
    adhoc_hits = [name for name, pat in ADHOC_FACTOR_PATTERNS if pat.search(text)]

    return ScriptAudit(
        path=path.relative_to(ROOT).as_posix(),
        reads_repo_data=reads_repo_data,
        reads_repo_artifacts=reads_repo_artifacts,
        mentions_experimental=mentions_experimental,
        external_constant_hits=external_hits,
        adhoc_factor_hits=adhoc_hits,
    )


def _to_md(audits: list[ScriptAudit]) -> str:
    lines: list[str] = []
    lines.append("# Prediction Script Audit")
    lines.append("")
    lines.append(
        "This is a mechanical scan. It flags likely external-data usage and ad-hoc factors."
    )
    lines.append("")

    def yn(b: bool) -> str:
        return "yes" if b else "no"

    lines.append(
        "| script | reads `data/` | reads `artifacts/` | mentions experimental | external-constant hits | ad-hoc hits |"
    )
    lines.append("|---|---:|---:|---:|---|---|")
    for a in audits:
        ext = ", ".join(a.external_constant_hits) if a.external_constant_hits else "—"
        adh = ", ".join(a.adhoc_factor_hits) if a.adhoc_factor_hits else "—"
        lines.append(
            f"| `{a.path}` | {yn(a.reads_repo_data)} | {yn(a.reads_repo_artifacts)} | {yn(a.mentions_experimental)} | {ext} | {adh} |"
        )
    lines.append("")
    lines.append("## Notes")
    lines.append(
        "- A hit does not mean the script is wrong; it means it is not purely internal/axiomatic."
    )
    lines.append(
        "- For publish-grade claims, prefer scripts that read only `artifacts/` (and not hard-coded experimental constants)."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    py_files = _iter_python_files([TOOLS, SRC])
    audits = [_audit_one(p) for p in py_files]

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps([asdict(a) for a in audits], indent=2), encoding="utf-8"
    )
    OUT_MD.write_text(_to_md(audits), encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
