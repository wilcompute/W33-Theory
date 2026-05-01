"""Helpers for locating heavyweight repo data artifacts across worktrees.

Some promoted theorem modules depend on large generated datasets that may live
either in the current worktree, another worktree of the same repo, or a sibling
checkout. The goal here is portability, not silent magic: resolve the first
available path in the expected search order and raise a clear error when
nothing matches.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from functools import lru_cache
from pathlib import Path


def _dedupe_paths(paths: list[Path]) -> tuple[Path, ...]:
    deduped: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve(strict=False)
        if resolved not in seen:
            deduped.append(resolved)
            seen.add(resolved)
    return tuple(deduped)


def _git_worktree_roots(repo_root: Path) -> tuple[Path, ...]:
    try:
        out = subprocess.check_output(
            ["git", "worktree", "list", "--porcelain"],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError):
        return ()

    roots: list[Path] = []
    for line in out.splitlines():
        if line.startswith("worktree "):
            candidate = Path(line.split(" ", 1)[1])
            if candidate.exists():
                roots.append(candidate)
    return _dedupe_paths(roots)


@lru_cache(maxsize=1)
def candidate_repo_roots(repo_root: Path) -> tuple[Path, ...]:
    """Return candidate repo roots that may host heavyweight data artifacts."""
    roots: list[Path] = []

    configured = os.environ.get("W33_DATA_ROOT")
    if configured:
        roots.append(Path(configured).expanduser())

    roots.append(repo_root)
    roots.extend(_git_worktree_roots(repo_root))

    parent = repo_root.parent
    for name in ("Theory of Everything", "Theory_of_Everything_clean"):
        candidate = parent / name
        if candidate.exists():
            roots.append(candidate)

    return _dedupe_paths(roots)


def find_repo_data_path(repo_root: Path, relative_path: str | Path) -> Path | None:
    """Return the first existing repo data path, or ``None`` if unresolved."""
    rel = Path(relative_path)
    for root in candidate_repo_roots(repo_root):
        candidate = root / rel
        if candidate.exists():
            return candidate
    return None


def resolve_repo_data_path(repo_root: Path, relative_path: str | Path) -> Path:
    """Resolve a required repo data path or raise a clear actionable error."""
    rel = Path(relative_path)
    resolved = find_repo_data_path(repo_root, rel)
    if resolved is not None:
        return resolved

    attempted = "\n".join(
        f"  - {root / rel}" for root in candidate_repo_roots(repo_root)
    )
    message = (
        f"Missing required repo data path '{rel}'. Checked:\n{attempted}\n"
        "Set W33_DATA_ROOT=/path/to/repo-with-artifacts if the heavy data lives "
        "outside the current worktree."
    )
    if "pytest" in sys.modules:
        import pytest

        pytest.skip(message, allow_module_level=True)
    raise FileNotFoundError(message)


def load_json_from_repo_data(repo_root: Path, relative_path: str | Path):
    """Load JSON from the first matching repo data path."""
    path = resolve_repo_data_path(repo_root, relative_path)
    return json.loads(path.read_text(encoding="utf-8"))
