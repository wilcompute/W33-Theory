"""Find top-level function calls and plt.show() not protected by a
"if __name__ == '__main__'" guard.

Usage: python scripts/find_top_level_calls.py
Exits with code 1 if any suspicious files are found.
"""

from __future__ import annotations

import ast
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {
    ".venv",
    ".venv_tools",
    "venv",
    "env",
    "artifacts",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    "scripts/sage",
}

IGNORED_PATTERNS = ["# requires sage", "#!/usr/bin/env sage"]

suspicious = []

import os

for dirpath, dirnames, filenames in os.walk(REPO_ROOT, onerror=lambda e: None):
    # Skip virtualenv and build dirs
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
            tree = ast.parse(text, filename=str(p))
        except Exception:
            continue

        # Collect top-level calls that are expressions or simple assignments calling functions
        for node in tree.body:
            # skip if this node is an if __name__ guard
            if isinstance(node, ast.If):
                # check for name == '__main__'
                try:
                    if any(
                        isinstance(cmp, ast.Compare)
                        and isinstance(cmp.left, ast.Name)
                        and cmp.left.id == "__name__"
                        for cmp in [node.test]
                    ):
                        continue
                except Exception:
                    pass
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                suspicious.append(
                    (
                        str(p),
                        node.lineno,
                        ast.unparse(node.value) if hasattr(ast, "unparse") else "call",
                    )
                )
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                suspicious.append(
                    (
                        str(p),
                        node.lineno,
                        ast.unparse(node.value) if hasattr(ast, "unparse") else "call",
                    )
                )

# Also look for plt.show occurrences
for p in REPO_ROOT.rglob("*.py"):
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        continue
    if "plt.show(" in text and any(part not in SKIP_DIRS for part in p.parts):
        suspicious.append((str(p), None, "plt.show()"))

if suspicious:
    print("Found top-level function calls or plt.show() in these files:")
    for fn, ln, call in suspicious:
        if ln:
            print(f"  {fn}:{ln}: {call}")
        else:
            print(f"  {fn}: {call}")
    print(
        "\nRecommendation: move runtime code into a main() function and guard with if __name__ == '__main__'."
    )
    sys.exit(1)
else:
    print("No suspicious top-level calls found.")
    sys.exit(0)
