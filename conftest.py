import importlib
from pathlib import Path

# Detect availability of optional heavy dependencies
_optional_modules = {
    "pandas": False,
    "sage": False,
}
for m in list(_optional_modules.keys()):
    try:
        importlib.import_module(m)
        _optional_modules[m] = True
    except Exception:
        _optional_modules[m] = False

import re

_skip_triggers = {
    "pandas": [re.compile(r"^\s*(import|from)\s+pandas\b", re.M)],
    "sage": [
        re.compile(r"^\s*(import|from)\s+sage\b", re.M),
        re.compile(r"from\s+sage\.all", re.M),
    ],
}


def pytest_ignore_collect(path, config):
    """Skip collecting test files that reference optional heavy dependencies
    which are not available in the current environment. This prevents
    the test run from failing with ImportError on machines without
    those optional packages (e.g., CI runners without Sage or user venvs
    without pandas)."""
    try:
        text = Path(str(path)).read_text()
    except Exception:
        return False

    for mod, triggers in _skip_triggers.items():
        if not _optional_modules.get(mod, False):
            for trig in triggers:
                # trig is a compiled regex pattern, use .search to test
                if trig.search(text):
                    # skip collecting this test file
                    print(f"Skipping {path} (requires {mod})")
                    return True
    return False
