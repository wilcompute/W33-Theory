#!/usr/bin/env python3
"""Pass 1197: fail-closed namespace and exact-claim guard for future pass packets."""
from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "w33_pass_namespace_registry_v2.json"
OUT = ROOT / "data" / "w33_pass1197_namespace_claim_guard.json"

REQUIRED_ARTIFACTS = [
    "analysis/w33_pass1193_a5_intersection_bridge.py",
    "data/w33_pass1193_a5_intersection_bridge.json",
    "analysis/w33_pass1194_residual_wedderburn_idempotents.py",
    "data/w33_pass1194_residual_wedderburn_idempotents.json",
    "analysis/w33_pass1195_ihara_primitive_cycle_census.py",
    "data/w33_pass1195_ihara_primitive_cycle_census.json",
    "analysis/w33_pass1196_equivariant_ihara_orbit_boundary.py",
    "data/w33_pass1196_equivariant_ihara_orbit_boundary.json",
    "analysis/w33_pass1197_namespace_claim_guard.py",
    "tests/test_w33_pass1193_1197.py",
    ".github/workflows/pass_namespace_and_claim_guard.yml",
]

FORBIDDEN_PATTERNS = {
    "ihara_coefficient_12": re.compile(r"x\^2\s*-\s*(?:lambda|lam)\s*\*?\s*x\s*\+\s*12", re.I),
    "impossible_S5_central_quotient": re.compile(r"S_?5\s*/\s*\\?\{?\\?pm\s*1", re.I),
    "PSp_order_51840": re.compile(r"PSp\s*\(?4\s*,\s*3\)?[^\n.;]{0,40}order\s*51840", re.I),
    "maschke_absolute_irreducibility": re.compile(r"Maschke[^\n]{0,120}(?:absolute(?:ly)? irreducible|hence over characteristic 0)", re.I),
}


def parse_range(text: str) -> tuple[int, int]:
    if "-" in text:
        a, b = text.split("-", 1)
        return int(a), int(b)
    n = int(text)
    return n, n


def registry_checks(registry: dict[str, object]) -> tuple[list[tuple[int, int, str]], list[str]]:
    errors: list[str] = []
    ranges = []
    for block in registry.get("canonical_blocks", []):
        start, stop = parse_range(str(block["range"]))
        if start > stop:
            errors.append(f"reversed range {start}-{stop}")
        ranges.append((start, stop, str(block.get("owner", ""))))
    ranges.sort()
    for left, right in zip(ranges, ranges[1:]):
        if right[0] <= left[1]:
            errors.append(f"overlap {left} vs {right}")
    block = next((b for b in registry["canonical_blocks"] if str(b["range"]) == "1193-1197"), None)
    if block is None:
        errors.append("missing canonical 1193-1197 block")
    elif block.get("status") != "COMPLETE":
        errors.append("1193-1197 block is not COMPLETE")
    return ranges, errors


def pass_is_registered(number: int, ranges: list[tuple[int, int, str]]) -> bool:
    return any(a <= number <= b for a, b, _ in ranges)


def pass_numbers(path: Path) -> list[int]:
    return [int(m.group(1)) for m in re.finditer(r"(?:pass|PASS)(\d{4})", path.name)]


def scan_future_pass_files(ranges: list[tuple[int, int, str]]) -> list[str]:
    errors = []
    roots = [ROOT / "analysis", ROOT / "data", ROOT / "tests", ROOT]
    seen: set[Path] = set()
    for base in roots:
        if not base.exists():
            continue
        iterator = base.rglob("*") if base != ROOT else base.glob("PASS*RELEASE*.md")
        for path in iterator:
            if not path.is_file() or path in seen:
                continue
            seen.add(path)
            for number in pass_numbers(path):
                if number >= 1193 and not pass_is_registered(number, ranges):
                    errors.append(f"unregistered future pass {number} in {path.relative_to(ROOT)}")
    return errors


def scan_forbidden_claims() -> list[str]:
    """Pass 1192 guards the historical corpus; this guard owns packets 1193 onward."""
    errors = []
    candidates = []
    for pattern in ("analysis/w33_pass*.py", "PASS*_RELEASE*.md", "tests/test_w33_pass*.py"):
        candidates.extend(ROOT.glob(pattern))
    for path in sorted(set(candidates)):
        if path.resolve() == Path(__file__).resolve():
            continue
        numbers = pass_numbers(path)
        if not numbers or max(numbers) < 1193:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, regex in FORBIDDEN_PATTERNS.items():
            if regex.search(text):
                errors.append(f"{label}: {path.relative_to(ROOT)}")
    return errors


def main() -> dict[str, object]:
    errors: list[str] = []
    if not REGISTRY.exists():
        errors.append("missing namespace registry")
        ranges = []
    else:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        ranges, registry_errors = registry_checks(registry)
        errors.extend(registry_errors)

    for rel in REQUIRED_ARTIFACTS:
        if not (ROOT / rel).exists():
            errors.append(f"missing required artifact {rel}")

    errors.extend(scan_future_pass_files(ranges))
    errors.extend(scan_forbidden_claims())

    for n in range(1193, 1197):
        matches = list((ROOT / "data").glob(f"w33_pass{n}_*.json"))
        if len(matches) != 1:
            errors.append(f"pass {n} expected one result JSON, found {len(matches)}")
            continue
        if json.loads(matches[0].read_text(encoding="utf-8")).get("status") != "PASS":
            errors.append(f"pass {n} result status is not PASS")

    workflow_path = ROOT / ".github/workflows/pass_namespace_and_claim_guard.yml"
    workflow_text = workflow_path.read_text(encoding="utf-8") if workflow_path.exists() else ""
    if "pull_request:" not in workflow_text or "w33_pass1197_namespace_claim_guard.py" not in workflow_text:
        errors.append("mandatory pull-request workflow gate is not wired")

    precommit_path = ROOT / ".pre-commit-config.yaml"
    precommit = precommit_path.read_text(encoding="utf-8") if precommit_path.exists() else ""
    if "pass-namespace-claim-guard" not in precommit:
        errors.append("pre-commit namespace/claim hook is not wired")

    result = {
        "schema": "w33.pass1197.namespace_claim_guard.v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "registered_ranges": [{"start": a, "stop": b, "owner": owner} for a, b, owner in ranges],
        "required_artifact_count": len(REQUIRED_ARTIFACTS),
        "forbidden_pattern_count": len(FORBIDDEN_PATTERNS),
        "policy": {
            "historical_corpus_owned_by_pass1192": True,
            "future_pass_files_must_be_registered": True,
            "canonical_ranges_must_not_overlap": True,
            "exact_result_jsons_must_pass": True,
            "pull_request_gate_mandatory": True,
            "precommit_gate_mandatory": True,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if errors:
        for error in errors:
            print("ERROR:", error)
        raise SystemExit(1)
    print(json.dumps({"status": "PASS", "registered_block": "1193-1197", "required_artifacts": len(REQUIRED_ARTIFACTS)}, indent=2))
    return result


if __name__ == "__main__":
    main()
