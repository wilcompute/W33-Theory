from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.prepare_legacy_test_fixtures import ensure_legacy_test_fixtures

WINDOWS_VENV_PYTHON = ".venv\\Scripts\\python.exe"
_ORIG_SUBPROCESS_RUN = subprocess.run


def _rewrite_python_argv(args):
    if isinstance(args, (list, tuple)) and args:
        head = str(args[0])
        # If the exact venv python path is used, replace with the current
        # sys.executable so subprocesses run in the same interpreter pytest
        # is using (the activated venv during tests).
        if head == WINDOWS_VENV_PYTHON:
            rewritten = list(args)
            rewritten[0] = sys.executable
            return rewritten

        # Many legacy scripts invoke the Windows launcher via `py -3 script`.
        # Rewrite that to use the current test interpreter so required
        # dependencies installed in the venv are available to the subprocess.
        if head.lower() == "py" and len(args) >= 3 and str(args[1]).startswith("-3"):
            rewritten = [sys.executable] + list(args[2:])
            return rewritten
    return args


def _patched_subprocess_run(*popenargs, **kwargs):
    if popenargs:
        args = _rewrite_python_argv(popenargs[0])
        popenargs = (args, *popenargs[1:])
    elif "args" in kwargs:
        kwargs["args"] = _rewrite_python_argv(kwargs["args"])
    return _ORIG_SUBPROCESS_RUN(*popenargs, **kwargs)


def pytest_sessionstart(session) -> None:
    ensure_legacy_test_fixtures()
    subprocess.run = _patched_subprocess_run


def pytest_collection_modifyitems(config, items) -> None:
    missing_by_path: dict[Path, list[str]] = {}
    for item in items:
        test_path = Path(str(item.fspath))
        if test_path not in missing_by_path:
            try:
                source = test_path.read_text(encoding="utf-8")
            except OSError:
                missing_by_path[test_path] = []
                continue
            optional_roots = set(re.findall(r"toe_session_\d{8}_v\d+", source))
            optional_roots.update(
                re.findall(r"bundles/v\d+(?:[A-Za-z0-9_+-]*)?", source)
            )
            missing_by_path[test_path] = sorted(
                name for name in optional_roots if not (ROOT / name).exists()
            )
        missing = missing_by_path[test_path]
        if missing:
            item.add_marker(
                pytest.mark.skip(
                    reason=(
                        "optional export missing: "
                        + ", ".join(missing[:3])
                        + ("..." if len(missing) > 3 else "")
                    )
                )
            )
