import ast
import importlib
import os
import sys
from pathlib import Path

# Optional heavy dependencies we want to skip tests for when missing.
# Key: logical name → list of module names to try importing.
_optional_candidates = {
    "pandas": ["pandas"],
    "sage": ["sage", "sageall", "sagelib", "sagemath"],
    "strawberryfields": ["strawberryfields"],
}

# Map logical name → availability flag
_optional_modules = {k: False for k in _optional_candidates}

# Environment variable allows forcing running optional tests; value 'ALL' or comma-separated names
_FORCE_ENV = os.environ.get("RUN_OPTIONAL_TESTS", "").strip()
_FORCE_ALL = _FORCE_ENV.upper() == "ALL"
_FORCED = set([x.strip().lower() for x in _FORCE_ENV.split(",") if x.strip()])


def _file_imports_modules(path):
    """Return a set of top-level module names imported by the given file (using ast).
    This is safer than regex-based detection and handles several import forms."""
    try:
        txt = Path(str(path)).read_text()
    except Exception:
        return set()
    try:
        tree = ast.parse(txt)
    except Exception:
        # If we can't parse, fall back to an empty set to avoid false skips
        return set()

    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name.split(".")[0]
                mods.add(name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                name = node.module.split(".")[0]
                mods.add(name)
    return mods


# record of skipped test files due to missing optional deps
_SKIPPED_OPTIONAL = []


def pytest_ignore_collect(path, config):
    """Skip collecting tests that import optional heavy modules not present.

    This runs early during collection and prevents ImportError at import time.
    It also supports an environment override: set RUN_OPTIONAL_TESTS=ALL or a
    comma-separated list like "sage,strawberryfields" to force-running those tests
    in local or CI environments where the optional deps are present by other means.

    When we skip a file due to an unavailable optional dependency, we record the
    skip in `_SKIPPED_OPTIONAL` so CI can include an artifact listing skipped
    tests and the missing modules.
    """
    imported = _file_imports_modules(path)
    # Normalize lower-case for comparison
    imported_lc = set(m.lower() for m in imported)

    for logical, candidates in _optional_candidates.items():
        logical_lc = logical.lower()
        # If forced via env var, treat as available
        if _FORCE_ALL or logical_lc in _FORCED:
            _optional_modules[logical] = True
            continue

        # otherwise, if any candidate import is present in file, and we cannot import it, skip
        if any((c.split(".")[0].lower() in imported_lc) for c in candidates):
            # detect actual availability
            avail = False
            for m in candidates:
                try:
                    importlib.import_module(m)
                    avail = True
                    break
                except Exception:
                    continue
            _optional_modules[logical] = avail
            if not avail:
                # record skip for later reporting
                _SKIPPED_OPTIONAL.append({"path": str(path), "requires": logical})
                # avoid noisy stdout in pytest collection, write to stderr
                sys.stderr.write(f"Skipping {path} (requires {logical})\n")
                return True
    return False


def pytest_sessionfinish(session, exitstatus):
    """Write an artifacts/skipped_optional_tests.json file at test session end
    for CI to collect and for humans to inspect. This runs even if all tests are
    skipped or collection fails (as long as pytest reaches session finish)."""
    try:
        import json
        from pathlib import Path

        out_dir = Path("artifacts")
        out_dir.mkdir(exist_ok=True)
        out_path = out_dir / "skipped_optional_tests.json"
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump({"skipped": _SKIPPED_OPTIONAL}, fh, indent=2)
        # also print a short summary to the CI log
        if _SKIPPED_OPTIONAL:
            sys.stderr.write(
                f"Recorded {len(_SKIPPED_OPTIONAL)} skipped optional test files to {out_path}\n"
            )
    except Exception:
        # Be conservative: don't make test runs fail because reporting failed
        pass


# Run a quick probe at import time so callers can inspect _optional_modules if needed
for key in list(_optional_candidates.keys()):
    for candidate in _optional_candidates[key]:
        try:
            importlib.import_module(candidate)
            _optional_modules[key] = True
            break
        except Exception:
            _optional_modules[key] = False


# Optional helper: allow 'python conftest.py' to print detection results
if __name__ == "__main__":
    for k, v in _optional_modules.items():
        print(k, "available" if v else "missing")
