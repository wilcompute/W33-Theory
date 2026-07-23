#!/usr/bin/env python3
"""Claim-governance linter for RH and Hilbert-Polya statements.

The repository contains exact finite graph-RH theorems, exploratory bridges,
and historical overclaims. This tool prevents new text from silently crossing
those tiers. It is report-only by default; use --strict to fail on unqualified
high-risk claims. It can be run on explicit changed files in CI.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
from pathlib import Path
import re
from typing import Iterable, Sequence

TEXT_SUFFIXES = {".md", ".tex", ".py", ".txt", ".html", ".rst"}
DEFAULT_EXCLUDED_PARTS = {
    ".git",
    "archive",
    "legacy",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
}

SAFE_CONTEXT = re.compile(
    r"\b(?:not|does\s+not|cannot|fails?\s+to|finite(?:-graph|\s+graph)?|"
    r"analogue|analog|toy|heuristic|candidate|conjectur|without\s+(?:an?\s+)?"
    r"(?:transfer|determinant)|transfer\s+obstruction|classical\s+RH\s+remains|"
    r"not\s+classical|counterexample|unsupported|false|reclassified|claim\s+audit)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Rule:
    rule_id: str
    severity: str
    pattern: re.Pattern[str]
    guidance: str


RULES: tuple[Rule, ...] = (
    Rule(
        "RH_PROOF",
        "error",
        re.compile(
            r"\b(?:prove[sd]?|proof\s+of|solve[sd]?)\s+(?:the\s+)?(?:classical\s+)?"
            r"Riemann\s+Hypothesis\b",
            re.IGNORECASE,
        ),
        "Qualify as finite graph-RH, heuristic, or supply an explicit classical transfer theorem.",
    ),
    Rule(
        "RH_HOLDS",
        "error",
        re.compile(r"\bRiemann\s+Hypothesis\s+holds\b", re.IGNORECASE),
        "State the exact domain: W(3,3) graph-RH versus the classical completed zeta function.",
    ),
    Rule(
        "HILBERT_POLYA_REALIZED",
        "error",
        re.compile(
            r"\bHilbert[-\s]*P[oó]lya\b.{0,80}\b(?:realized|proved|completed)\b",
            re.IGNORECASE,
        ),
        "Require determinant equality and spectral-set equality, not a map landing on Re(s)=1/2 by definition.",
    ),
    Rule(
        "DELIGNE_TRANSFER",
        "error",
        re.compile(
            r"\bDeligne\b.{0,160}\b(?:implies|proves|therefore|=>)\b.{0,80}"
            r"\b(?:classical\s+)?Riemann\s+Hypothesis\b",
            re.IGNORECASE,
        ),
        "Separate finite-field/automorphic RH results from the classical Riemann zeta problem.",
    ),
    Rule(
        "RH_QED",
        "warning",
        re.compile(
            r"(?:Riemann\s+Hypothesis.{0,200}Q\.?E\.?D\.?|"
            r"Q\.?E\.?D\.?.{0,200}Riemann\s+Hypothesis)",
            re.IGNORECASE | re.DOTALL,
        ),
        "Use Q.E.D. only after the theorem scope is explicitly finite or a classical transfer is proved.",
    ),
    Rule(
        "TOPOLOGICAL_NECESSITY",
        "warning",
        re.compile(
            r"\b(?:topological|phase)\s+(?:torque|collapse|invariance)\b.{0,120}"
            r"\b(?:forces?|mandates?|dictates?|strictly\s+forbids?)\b",
            re.IGNORECASE,
        ),
        "Name the exact functional, domain, and coercive/no-cancellation theorem.",
    ),
)


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule_id: str
    severity: str
    excerpt: str
    guidance: str


def context_window(lines: Sequence[str], index: int, radius: int = 3) -> str:
    lo = max(0, index - radius)
    hi = min(len(lines), index + radius + 1)
    return " ".join(line.strip() for line in lines[lo:hi])


def lint_text(text: str, path: str = "<memory>") -> list[Finding]:
    lines = text.splitlines()
    findings: list[Finding] = []
    for index, line in enumerate(lines):
        window = context_window(lines, index)
        for rule in RULES:
            match = rule.pattern.search(line)
            if not match:
                continue
            if SAFE_CONTEXT.search(window):
                continue
            findings.append(
                Finding(
                    path=path,
                    line=index + 1,
                    rule_id=rule.rule_id,
                    severity=rule.severity,
                    excerpt=line.strip()[:280],
                    guidance=rule.guidance,
                )
            )
    return findings


def iter_text_files(paths: Iterable[Path], include_archive: bool = False) -> Iterable[Path]:
    seen: set[Path] = set()
    for path in paths:
        if path.is_file():
            if path.suffix.lower() in TEXT_SUFFIXES and path not in seen:
                seen.add(path)
                yield path
            continue
        if not path.exists():
            continue
        for candidate in path.rglob("*"):
            if not candidate.is_file() or candidate.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if not include_archive and any(
                part in DEFAULT_EXCLUDED_PARTS for part in candidate.parts
            ):
                continue
            if candidate not in seen:
                seen.add(candidate)
                yield candidate


def lint_paths(paths: Iterable[Path], include_archive: bool = False) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_text_files(paths, include_archive=include_archive):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        findings.extend(lint_text(text, str(path)))
    return findings


def summary(findings: Sequence[Finding]) -> dict[str, object]:
    by_severity = {
        severity: sum(f.severity == severity for f in findings)
        for severity in ("error", "warning")
    }
    return {
        "status": "PASS" if not findings else "FINDINGS",
        "finding_count": len(findings),
        "by_severity": by_severity,
        "findings": [asdict(finding) for finding in findings],
        "policy": {
            "finite_graph_RH_claims": "allowed when scoped explicitly",
            "classical_RH_claims": "require transfer/determinant theorem",
            "default_mode": "report-only",
            "strict_mode": "nonzero exit on unqualified errors",
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", default=["."], help="Files or directories")
    parser.add_argument("--json", dest="json_path", help="Write JSON report")
    parser.add_argument("--strict", action="store_true", help="Fail on error findings")
    parser.add_argument(
        "--include-archive", action="store_true", help="Include archive and legacy trees"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    findings = lint_paths(
        [Path(path) for path in args.paths], include_archive=args.include_archive
    )
    payload = summary(findings)
    rendered = json.dumps(payload, indent=2)
    print(rendered)
    if args.json_path:
        output = Path(args.json_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    if args.strict and any(finding.severity == "error" for finding in findings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
