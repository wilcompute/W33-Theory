#!/usr/bin/env python3
"""Pass 1197: fail-closed namespace and parallel-release collision guard."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1197_parallel_collision_guard.json"
REGISTRY = ROOT / "data" / "w33_pass_namespace_registry_v2.json"
CURRENT_RANGE = range(1193, 1198)
CURRENT_RESULTS = [ROOT / "data" / f"w33_pass{number}_" for number in CURRENT_RANGE]
FORBIDDEN_TRANSPORT = [
    ROOT / ".correction",
    ROOT / "PASS1192_MATERIALIZE.trigger",
    ROOT / ".github" / "workflows" / "pass1192_materialize_pr.yml",
]


def parse_range(value: str) -> set[int]:
    if "-" not in value:
        return {int(value)}
    start, end = map(int, value.split("-", 1))
    assert start <= end
    return set(range(start, end + 1))


def load_result_for_pass(number: int) -> tuple[Path, dict]:
    candidates = sorted((ROOT / "data").glob(f"w33_pass{number}_*.json"))
    if len(candidates) != 1:
        raise AssertionError(f"Pass {number} must have exactly one canonical data certificate; found {candidates}")
    return candidates[0], json.loads(candidates[0].read_text(encoding="utf-8"))


def main() -> dict:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    seen: dict[int, dict] = {}
    collisions = []
    for block in registry["canonical_blocks"]:
        for number in parse_range(block["range"]):
            if number in seen:
                collisions.append({"pass": number, "owners": [seen[number]["owner"], block["owner"]]})
            seen[number] = block
    assert not collisions, collisions

    current_block = next(block for block in registry["canonical_blocks"] if parse_range(block["range"]) == set(CURRENT_RANGE))
    assert current_block["status"] == "COMPLETE"
    assert set(map(int, current_block["artifacts"])) == set(CURRENT_RANGE)

    unregistered = []
    pattern = re.compile(r"(?:^|[_-])pass(\d{4})(?:[_-]|\.|$)", re.IGNORECASE)
    for directory in (ROOT / "analysis", ROOT / "tests", ROOT / "data", ROOT / ".github" / "workflows"):
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            match = pattern.search(path.name)
            if match:
                number = int(match.group(1))
                if number >= 1120 and number not in seen:
                    unregistered.append(str(path.relative_to(ROOT)))
    assert not unregistered, unregistered

    certificates = []
    for number in CURRENT_RANGE:
        path, data = load_result_for_pass(number)
        checks = data.get("checks", {})
        assert data.get("status") == "PASS", (number, data.get("status"))
        assert checks and all(checks.values()), (number, checks)
        certificates.append({
            "pass": number,
            "path": str(path.relative_to(ROOT)),
            "schema": data.get("schema"),
            "checks": len(checks),
        })

    precommit = (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    workflow_path = ROOT / ".github" / "workflows" / "pass1193_1197_exact_release.yml"
    workflow = workflow_path.read_text(encoding="utf-8")
    gate_checks = {
        "precommit_namespace_guard_installed": "pass-namespace-collision-guard" in precommit,
        "workflow_runs_pass1197_guard": "w33_pass1197_parallel_collision_guard.py --check-only" in workflow,
        "workflow_runs_pass1192_guard": "w33_pass1192_parallel_synthesis_guard.py" in workflow,
        "transport_scaffold_absent": all(not path.exists() for path in FORBIDDEN_TRANSPORT),
        "current_block_complete": current_block["status"] == "COMPLETE",
        "current_artifacts_complete": set(map(int, current_block["artifacts"])) == set(CURRENT_RANGE),
    }
    assert all(gate_checks.values()), gate_checks

    result = {
        "schema": "w33.pass1197.parallel_collision_guard.v1",
        "status": "PASS",
        "headline": "Pass-number ownership, exact certificates, legacy synthesis, and transport cleanup are enforced as mandatory parallel-development gates.",
        "registry": {
            "schema": registry["schema"],
            "registered_pass_count": len(seen),
            "minimum_registered": min(seen),
            "maximum_registered": max(seen),
            "collisions": collisions,
            "unregistered_modern_files": unregistered,
        },
        "current_block": current_block,
        "certificates": certificates,
        "gate_checks": gate_checks,
        "checks": {
            "registry_has_no_overlap": not collisions,
            "registered_pass_count_74": len(seen) == 74,
            "no_unregistered_modern_files": not unregistered,
            "passes_1193_1197_all_pass": len(certificates) == 5,
            "mandatory_gates_installed": all(gate_checks.values()),
        },
        "policy": "Parallel agents must reserve a disjoint range before publication; the range, artifacts, exact certificates, synthesis guard, and cleanup gate must all agree before merge.",
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1197 namespace/certificate/synthesis gates clean")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="Retained for pre-commit/CI compatibility; the guard is always fail closed.")
    parser.parse_args()
    main()
