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
REGISTRY_SUPPLEMENTS = ROOT / "data" / "w33_pass_namespace_registry_v2.d"
CURRENT_RANGE = range(1193, 1198)
MINIMUM_BASELINE_REGISTERED = 74
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


def selftest() -> int:
    """Planted-fault recall for the range parser this guard reserves numbers with.

    parse_range is the whole namespace-collision mechanism: every reservation block is
    expanded through it, so an off-by-one here silently mis-reserves a pass number, which
    is the exact fault the guard exists to prevent (Pass 5250).
    """
    cases = [("single number", "4801", {4801}),
             ("inclusive range", "10-13", {10, 11, 12, 13}),
             ("degenerate range", "7-7", {7}),
             ("wide block", "5246-5253", set(range(5246, 5254)))]
    ok = True
    print("  selftest -- reservation range expansion\n")
    for name, arg, want in cases:
        got = parse_range(arg)
        good = got == want
        ok &= good
        print(f"    {name:20s} {arg:>12s} -> {len(got):3d} number(s)  "
              f"{'PASS' if good else 'FAIL (got %s)' % sorted(got)}")
    for name, arg in (("reversed range rejected", "13-10"),):
        try:
            parse_range(arg)
            print(f"    {name:20s} {arg:>12s} -> accepted           FAIL")
            ok = False
        except AssertionError:
            print(f"    {name:20s} {arg:>12s} -> rejected           PASS")
    print("""
  THE INCLUSIVE-RANGE CASE IS THE ONE THAT MATTERS. "5246-5253" must expand to EIGHT
  numbers, not seven: a half-open reading leaves the last number of every block unclaimed,
  and an unclaimed number at a block boundary is precisely where two lanes collide. The
  reversed-range case checks the guard refuses input it cannot mean rather than silently
  reserving nothing.""")
    return 0 if ok else 1


def load_result_for_pass(number: int) -> tuple[Path, dict]:
    candidates = sorted((ROOT / "data").glob(f"w33_pass{number}_*.json"))
    if len(candidates) != 1:
        raise AssertionError(f"Pass {number} must have exactly one canonical data certificate; found {candidates}")
    return candidates[0], json.loads(candidates[0].read_text(encoding="utf-8"))


def load_registry_blocks() -> tuple[dict, list[dict], list[str]]:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    blocks = list(registry["canonical_blocks"])
    supplements = []
    if REGISTRY_SUPPLEMENTS.exists():
        for path in sorted(REGISTRY_SUPPLEMENTS.glob("*.json")):
            supplement = json.loads(path.read_text(encoding="utf-8"))
            assert supplement.get("schema") == "w33.pass_namespace_registry.v2.supplement", path
            assert supplement.get("status") == "ACTIVE", path
            assert supplement.get("canonical_blocks"), path
            blocks.extend(supplement["canonical_blocks"])
            supplements.append(str(path.relative_to(ROOT)))
    return registry, blocks, supplements


def main() -> dict:
    registry, registry_blocks, supplements = load_registry_blocks()
    seen: dict[int, dict] = {}
    collisions = []
    for block in registry_blocks:
        for number in parse_range(block["range"]):
            if number in seen:
                collisions.append({"pass": number, "owners": [seen[number]["owner"], block["owner"]]})
            seen[number] = block
    assert not collisions, collisions

    current_block = next(
        block for block in registry_blocks
        if parse_range(block["range"]) == set(CURRENT_RANGE)
    )
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
        "registry_monotonic_from_original_baseline": len(seen) >= MINIMUM_BASELINE_REGISTERED,
        "registry_supplements_typed": all(path.endswith(".json") for path in supplements),
    }
    assert all(gate_checks.values()), gate_checks

    result = {
        "schema": "w33.pass1197.parallel_collision_guard.v3",
        "status": "PASS",
        "headline": "Pass-number ownership, exact certificates, legacy synthesis, transport cleanup, and typed registry supplements are enforced as mandatory parallel-development gates.",
        "registry": {
            "schema": registry["schema"],
            "supplements": supplements,
            "registered_pass_count": len(seen),
            "minimum_registered": min(seen),
            "maximum_registered": max(seen),
            "minimum_baseline_registered": MINIMUM_BASELINE_REGISTERED,
            "collisions": collisions,
            "unregistered_modern_files": unregistered,
        },
        "current_block": current_block,
        "certificates": certificates,
        "gate_checks": gate_checks,
        "checks": {
            "registry_has_no_overlap": not collisions,
            "registered_pass_count_at_least_original_74": len(seen) >= MINIMUM_BASELINE_REGISTERED,
            "no_unregistered_modern_files": not unregistered,
            "passes_1193_1197_all_pass": len(certificates) == 5,
            "mandatory_gates_installed": all(gate_checks.values()),
        },
        "policy": "Parallel agents must reserve a disjoint range before publication. Canonical blocks may live in the base v2 registry or typed v2 supplements; all blocks are merged before overlap and unregistered-artifact checks. The registry count is monotonic rather than frozen at its original 74-pass baseline.",
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"PASS 1197 namespace/certificate/synthesis gates clean ({len(seen)} registered passes)")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="Retained for pre-commit/CI compatibility; the guard is always fail closed.")
    parser.add_argument("--selftest", action="store_true", help="Planted-fault recall for the reservation range parser.")
    args = parser.parse_args()
    if args.selftest:
        raise SystemExit(selftest())
    main()
