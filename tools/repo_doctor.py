#!/usr/bin/env python3
"""Environment and workspace health check for the W33 repo.

This is intentionally non-destructive. It answers:

- are the declared Python dependencies present?
- is the usual local virtualenv available?
- how dirty/cluttered is the current worktree?
- which root-level files are presentation-hostile on GitHub?
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration._artifact_paths import candidate_repo_roots, find_repo_data_path

REQUIREMENT_IMPORT_NAMES = {
    "jsonschema": "jsonschema",
    "matplotlib": "matplotlib",
    "mpmath": "mpmath",
    "networkx": "networkx",
    "numba": "numba",
    "numpy": "numpy",
    "pandas": "pandas",
    "pytest": "pytest",
    "requests": "requests",
    "scipy": "scipy",
    "sympy": "sympy",
}

HEAVY_DATA_RELATIVE_PATHS = (
    Path("extracted_v13")
    / "W33-Theory-master"
    / "artifacts"
    / "e8_root_metadata_table.json",
    Path("artifacts") / "e8_structure_constants_w33_discrete.json",
    Path("V24_output_v13_full") / "l3_patch_triples_full.jsonl",
    Path("V24_output_v13_full") / "l4_patch_quads_full.jsonl",
)


def _venv_report() -> dict[str, object]:
    configured = os.environ.get("VENV_DIR")
    venv = Path(configured).expanduser() if configured else ROOT / ".venv"
    return {
        "expected_path": str(venv),
        "configured_via_env": bool(configured),
        "exists": venv.exists(),
        "python": str(venv / "bin" / "python"),
    }


def _module_present(import_name: str, python_bin: Path | None) -> bool:
    if python_bin and python_bin.exists():
        code = (
            "import importlib.util;"
            f"print(1 if importlib.util.find_spec({import_name!r}) else 0)"
        )
        try:
            out = subprocess.check_output([str(python_bin), "-c", code], text=True)
            return out.strip() == "1"
        except subprocess.SubprocessError:
            return False
    return importlib.util.find_spec(import_name) is not None


def _read_requirements(path: Path, seen: set[Path] | None = None) -> list[str]:
    seen = seen or set()
    path = path.resolve()
    if path in seen or not path.exists():
        return []
    seen.add(path)

    packages: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-r "):
            nested = (path.parent / line.split(maxsplit=1)[1]).resolve()
            packages.extend(_read_requirements(nested, seen))
            continue
        name = re.split(r"[<>=!~\[]", line, maxsplit=1)[0].strip()
        if name:
            packages.append(name)
    return packages


def _dependency_report() -> dict[str, object]:
    venv = _venv_report()
    python_bin = Path(str(venv["python"])) if venv["exists"] else None
    declared = sorted(
        {
            pkg
            for pkg in _read_requirements(ROOT / "requirements-dev.txt")
            if pkg in REQUIREMENT_IMPORT_NAMES
        }
    )
    rows = []
    missing = []
    for pkg in declared:
        import_name = REQUIREMENT_IMPORT_NAMES[pkg]
        present = _module_present(import_name, python_bin)
        rows.append({"package": pkg, "import": import_name, "present": present})
        if not present:
            missing.append(pkg)
    return {
        "declared": declared,
        "rows": rows,
        "missing": missing,
        "ok": not missing,
        "inspected_python": str(python_bin) if python_bin else sys.executable,
    }


def _git_status_lines() -> list[str]:
    out = subprocess.check_output(
        ["git", "status", "--porcelain=v1"],
        cwd=ROOT,
        text=True,
    )
    return [line for line in out.splitlines() if line]


def _root_clutter_report() -> dict[str, object]:
    loose_files = []
    heavy_dirs = []
    for child in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
        if child.name.startswith("."):
            continue
        if child.is_dir() and (
            child.name.startswith("TOE_")
            or child.name.startswith("V")
            or child.name in {"bundles", "archive", "artifacts", "ChatGPT Files"}
            or child.name.startswith("_")
        ):
            heavy_dirs.append(child.name)
        if child.is_file() and (
            child.suffix in {".zip", ".pdf"}
            or child.name.startswith("TOE_")
            or child.name.startswith("REPORT")
            or child.name.startswith("SYMBOLIC_")
            or child.name.startswith("MATH_")
        ):
            loose_files.append(child.name)
    return {
        "presentation_hostile_root_files": loose_files[:50],
        "heavy_root_directories": heavy_dirs[:50],
        "counts": {
            "presentation_hostile_root_files": len(loose_files),
            "heavy_root_directories": len(heavy_dirs),
        },
    }


def _data_artifact_report() -> dict[str, object]:
    rows = []
    missing = []
    for rel in HEAVY_DATA_RELATIVE_PATHS:
        resolved = find_repo_data_path(ROOT, rel)
        row = {
            "relative_path": str(rel),
            "present": resolved is not None,
            "resolved_path": str(resolved) if resolved else None,
        }
        rows.append(row)
        if resolved is None:
            missing.append(str(rel))
    return {
        "candidate_roots": [str(root) for root in candidate_repo_roots(ROOT)],
        "rows": rows,
        "missing": missing,
        "ok": not missing,
    }


def build_report() -> dict[str, object]:
    deps = _dependency_report()
    git_lines = _git_status_lines()
    data_artifacts = _data_artifact_report()
    return {
        "repo_root": str(ROOT),
        "python": sys.version.split()[0],
        "venv": _venv_report(),
        "dependencies": deps,
        "data_artifacts": data_artifacts,
        "git_dirty_entries": len(git_lines),
        "root_clutter": _root_clutter_report(),
        "next_steps": [
            "Run ./scripts/bootstrap_repo_env.sh to create a local .venv and install requirements-dev.txt.",
            "If heavyweight theorem artifacts live outside this worktree, set W33_DATA_ROOT=/path/to/repo-with-artifacts.",
            "Run python3 tools/repo_cleanup_audit.py for a category view of dirty worktree entries.",
            "Prefer keeping promoted theorem work under exploration/, tests/, docs/, and tools/qiskit/ rather than adding new root-level drops.",
        ],
        "verdict": (
            "healthy"
            if deps["ok"] and data_artifacts["ok"]
            else "missing_python_dependencies"
            if not deps["ok"]
            else "missing_repo_data_artifacts"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2))
        return

    print(f"Repo root: {report['repo_root']}")
    print(f"Python: {report['python']}")
    print(f"Dirty entries: {report['git_dirty_entries']}")
    venv = report["venv"]
    print(f"Venv: {'present' if venv['exists'] else 'missing'} at {venv['expected_path']}")

    deps = report["dependencies"]
    print("\nDependencies:")
    for row in deps["rows"]:
        status = "ok" if row["present"] else "missing"
        print(f"  [{status}] {row['package']}")

    artifacts = report["data_artifacts"]
    print("\nHeavy data artifacts:")
    for row in artifacts["rows"]:
        status = "ok" if row["present"] else "missing"
        target = row["resolved_path"] or row["relative_path"]
        print(f"  [{status}] {target}")

    clutter = report["root_clutter"]
    print(
        "\nRoot clutter:"
        f" {clutter['counts']['presentation_hostile_root_files']} loose files,"
        f" {clutter['counts']['heavy_root_directories']} heavy directories"
    )
    for item in clutter["presentation_hostile_root_files"][:10]:
        print(f"  file: {item}")
    for item in clutter["heavy_root_directories"][:10]:
        print(f"  dir:  {item}")

    print("\nNext steps:")
    for step in report["next_steps"]:
        print(f"  - {step}")


if __name__ == "__main__":
    main()
