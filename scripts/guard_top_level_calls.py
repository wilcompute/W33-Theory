"""Guard simple top-level side-effects by moving them into a main() function.

Usage:
  python scripts/guard_top_level_calls.py [--apply]

- Dry-run (default): lists candidate files and proposed actions.
- --apply: edits files in place (creates a .bak copy first).

Heuristics (conservative):
- Only consider files without an existing "if __name__ == '__main__'" guard
- Only move top-level nodes of types: Expr (where value is Call), Assign (value is Call), With, Expr(Call to print or json.dump), or simple For/While that do not contain function/class defs
- Skip files that contain 'requires sage' or shebang for sage
- Only apply to files where the number of moved nodes <= 20 and the file is < 4000 lines

This is an automated helper — please review repo changes before merging.
"""

from __future__ import annotations

import argparse
import ast
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {
    ".venv",
    ".venv_tools",
    ".venv_wsl",
    "venv",
    "env",
    "artifacts",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    "scripts/sage",
    "extracted",
    "bundles",
    "data",
    "archive",
}
IGNORED_PATTERNS = ["# requires sage", "#!/usr/bin/env sage"]


def find_candidates():
    candidates = []
    for dirpath, dirnames, filenames in __import__("os").walk(ROOT):
        if any(part in SKIP_DIRS for part in Path(dirpath).parts):
            continue
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            p = Path(dirpath) / fn
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                continue
            if any(pat in text for pat in IGNORED_PATTERNS):
                continue
            try:
                tree = ast.parse(text)
            except Exception:
                continue
            # skip files already guarded
            if any(
                isinstance(node, ast.If)
                and isinstance(node.test, ast.Compare)
                and getattr(node.test.left, "id", None) == "__name__"
                for node in tree.body
            ):
                continue
            movable = []
            for node in list(tree.body):
                # skip imports, defs, class defs
                if isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                        ast.ClassDef,
                        ast.Import,
                        ast.ImportFrom,
                    ),
                ):
                    continue
                # Allow simple expressions or assigns with Call, With blocks, prints
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    movable.append(node)
                elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                    movable.append(node)
                elif isinstance(node, ast.With):
                    movable.append(node)
                elif isinstance(node, (ast.For, ast.While)):
                    # conservative: only allow loops without defs in body
                    has_def = any(
                        isinstance(n, (ast.FunctionDef, ast.ClassDef))
                        for n in ast.walk(node)
                    )
                    if not has_def:
                        movable.append(node)
                else:
                    # anything else (docstring) ignored
                    pass
            if movable and len(movable) <= 20 and len(text.splitlines()) < 4000:
                candidates.append((p, movable))
    return candidates


def make_backup(path: Path):
    bak = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, bak)
    return bak


def apply_guard(path: Path, movable_nodes: list[ast.AST]):
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    # Build new module: keep imports and defs at top, move movable nodes into main
    new_body = []
    main_body_src_lines = []

    # Determine line ranges for nodes to move
    to_move = set()
    for node in movable_nodes:
        to_move.add((node.lineno, getattr(node, "end_lineno", node.lineno)))

    lines = src.splitlines()
    # Compose main_body_src
    for s, e in sorted(to_move):
        # convert to 0-index
        main_body_src_lines.extend(lines[s - 1 : e])

    # Remove moved lines from original, but keep leading/trailing whitespace
    new_lines = []
    skip_ranges = sorted(to_move)
    curr = 1
    for s, e in skip_ranges:
        # add lines before s
        new_lines.extend(lines[curr - 1 : s - 1])
        curr = e + 1
    new_lines.extend(lines[curr - 1 :])

    # Build patched content
    main_def = ["def main():"]
    for l in main_body_src_lines:
        main_def.append("    " + l if l.strip() else "    pass")
    guard = ["\n", "if __name__ == '__main__':", "    main()", "\n"]

    patched = (
        "\n".join(new_lines).rstrip()
        + "\n\n"
        + "\n".join(main_def)
        + "\n"
        + "\n".join(guard)
    )
    # Tidy: avoid duplicate module docstring placement issues
    return patched


def main(apply: bool = False):
    candidates = find_candidates()
    if not candidates:
        print("No conservative candidates found.")
        return
    print(f"Found {len(candidates)} candidate files (conservative).")
    for p, movable in candidates:
        print(f"Candidate: {p} -> move {len(movable)} top-level nodes")
        if apply:
            bak = make_backup(p)
            patched = apply_guard(p, movable)
            p.write_text(patched, encoding="utf-8")
            print(f"  Applied. Backup at {bak}")
        else:
            print("  Dry-run: no changes applied. Run with --apply to edit files.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    main(apply=args.apply)
