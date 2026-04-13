from __future__ import annotations

import subprocess
import sys
from pathlib import Path

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
