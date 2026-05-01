import importlib
import os
import sys
from pathlib import Path

# Add pillars/ and exploration/ to import path so test files
# can import from THEORY_PART_* modules after repo reorganization.
_root = Path(__file__).resolve().parent
for _subdir in ("pillars", "exploration"):
    _p = str(_root / _subdir)
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Detect availability of optional heavy dependencies
_optional_modules = {
    "pandas": False,
    "sage": False,
}

import re

_skip_triggers = {
    "pandas": [re.compile(r"^\s*(import|from)\s+pandas\b", re.M)],
    "sage": [
        re.compile(r"^\s*(import|from)\s+sage\b", re.M),
        re.compile(r"from\s+sage\.all", re.M),
    ],
}

_W33_GP_TIMEOUT_NODEIDS: list[str] = []


def pytest_ignore_collect(path, config):
    """Skip collecting test files that reference optional heavy dependencies
    which are not available in the current environment. This prevents
    the test run from failing with ImportError on machines without
    those optional packages (e.g., CI runners without Sage or user venvs
    without pandas)."""
    p = Path(str(path))

    # Only apply this heuristic to Python test files. Scanning the entire repo can be
    # very noisy and slow, and can trigger surprising capture/log issues.
    if not (p.suffix == ".py" and p.name.startswith("test_")):
        return None

    # Local exploratory tests (kept untracked) should not affect canonical runs.
    if p.name in {"test_yukawa_mass_ratios.py"}:
        return True

    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    for mod, triggers in _skip_triggers.items():
        if not _optional_modules.get(mod, False):
            for trig in triggers:
                # trig is a compiled regex pattern, use .search to test
                if trig.search(text):
                    # skip collecting this test file
                    if getattr(config.option, "verbose", 0) > 0:
                        print(f"Skipping {path} (requires {mod})")
                    return True
    return None


def pytest_configure(config):
    """Register custom markers so -m fast and -m gp_required work cleanly."""
    config.addinivalue_line(
        "markers",
        "fast: marks tests as fast-lane (no GP, no heavy SymPy); should run in <5 s",
    )
    config.addinivalue_line(
        "markers",
        "gp_required: marks tests that invoke PARI/GP and may time out in constrained environments",
    )


def main():
    for m in list(_optional_modules.keys()):
        try:
            importlib.import_module(m)
            _optional_modules[m] = True
        except Exception:
            _optional_modules[m] = False

# ---------------------------------------------------------------------------
# GP-timeout diagnostics
# ---------------------------------------------------------------------------

def _report_gp_environment(config) -> None:
    """Report GP availability and timeout settings at session start."""
    import shutil
    gp_available = shutil.which("gp") is not None
    timeout_env = os.environ.get("W33_GP_TIMEOUT_SECONDS", "180 (default)")
    precomputed_env = os.environ.get("W33_USE_PRECOMPUTED_ON_GP_TIMEOUT", "1 (default)")
    if config.option.verbose > 0:
        print(
            f"\n[W33] PARI/GP available: {gp_available} | "
            f"W33_GP_TIMEOUT_SECONDS={timeout_env} | "
            f"W33_USE_PRECOMPUTED_ON_GP_TIMEOUT={precomputed_env}"
        )


def pytest_sessionstart(session) -> None:
    """Report GP environment once at session start."""
    _W33_GP_TIMEOUT_NODEIDS.clear()
    try:
        _report_gp_environment(session.config)
    except Exception:
        pass


def pytest_runtest_logreport(report):
    """Track runtime GP timeout failures for end-of-session diagnostics."""
    if report.when != "call" or report.outcome != "failed":
        return

    longrepr_text = str(report.longrepr)
    if "PARI/GP timed out" not in longrepr_text:
        return

    if report.nodeid not in _W33_GP_TIMEOUT_NODEIDS:
        _W33_GP_TIMEOUT_NODEIDS.append(report.nodeid)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Emit W33 GP-timeout diagnostics and fallback notice in summary."""
    gp_timeouts = list(_W33_GP_TIMEOUT_NODEIDS)
    if gp_timeouts:
        terminalreporter.section("W33 GP Timeout Diagnostics")
        terminalreporter.write_line(
            f"Detected {len(gp_timeouts)} PARI/GP timeout failure(s)."
        )
        terminalreporter.write_line(
            "Classification: runtime environment blocker (not theorem contradiction)."
        )
        terminalreporter.write_line(
            "Mitigation: set W33_GP_TIMEOUT_SECONDS to a larger value or install GP locally."
        )
        for nodeid in gp_timeouts:
            terminalreporter.write_line(f" - {nodeid}")

    # Report whether deterministic precomputed fallback was used.
    try:
        from exploration import w33_k3_integral_h2_lattice_bridge as k3_bridge
        if getattr(k3_bridge, "_FALLBACK_USED", False):
            terminalreporter.section("W33 GP Fallback")
            terminalreporter.write_line(
                "Deterministic precomputed K3 H^2 lattice fallback was used "
                "after GP timeout during this session."
            )
    except Exception:
        pass


# Initialize optional dependency detection at import time so collection behaves as intended.
main()
