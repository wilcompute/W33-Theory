import re
import subprocess
from pathlib import Path

import pytest

# pattern to detect json.dump(..., indent=2) without default=
PATTERN = re.compile(r"json\.dump\([^\)]*indent\s*=\s*2[^\)]*\)")


def _changed_python_files(repo_root: Path) -> list[Path]:
    """Return Python files changed in the PR/working tree."""
    rel_paths: set[str] = set()
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMRT", "origin/master...HEAD"],
        ["git", "diff", "--name-only", "--diff-filter=ACMRT", "HEAD"],
        ["git", "diff", "--name-only", "--diff-filter=ACMRT", "--cached"],
    ]
    for cmd in commands:
        proc = subprocess.run(
            cmd,
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        if proc.returncode != 0:
            continue
        for line in proc.stdout.splitlines():
            if line.endswith(".py"):
                rel_paths.add(line)
    return sorted(
        path
        for rel in rel_paths
        if (path := repo_root / rel).exists() and path.is_file()
    )


def test_no_plain_json_dump_with_indent():
    """Fail if changed files add json.dump(..., indent=2) without default=."""
    repo_root = Path(".").resolve()
    paths = _changed_python_files(repo_root)
    if not paths:
        pytest.skip("No changed Python files available for JSON serialization guard")

    matches = []
    for p in paths:
        parts = p.relative_to(repo_root).parts
        if any(
            part in (".venv", ".venv_tools", "venv", "env", "artifacts")
            for part in parts
        ):
            continue
        if "site-packages" in str(p) or "venv" in str(p):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for m in PATTERN.finditer(text):
            snippet = m.group(0)
            # if 'default=' not present in the snippet, allow if file uses dump_json helper
            if "default=" not in snippet:
                if "dump_json(" in text or "from utils.json_safe import" in text:
                    continue
                matches.append((str(p), snippet))

    if matches:
        msgs = [f"{fn}: {sn}" for fn, sn in matches]
        raise AssertionError(
            "Found json.dump calls with indent=2 and no default=:\n" + "\n".join(msgs)
        )
    # otherwise pass


def main():
    PATTERN = re.compile(r"json\.dump\([^\)]*indent\s*=\s*2[^\)]*\)")


if __name__ == "__main__":
    main()
