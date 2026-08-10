#!/usr/bin/env python3
"""Wrapper to run dd_shrink_conflict and log exceptions to a file"""
from __future__ import annotations

import sys
import traceback
from pathlib import Path

try:
    from dd_shrink_conflict import main as dd_main
except Exception as e:
    Path("checks/PART_CVII_dd_shrink_run_error.txt").write_text("Import error: " + str(e, encoding="utf-8") + "\n" + traceback.format_exc()
    )
    raise

if __name__ == "__main__":
    try:
        dd_main()
    except SystemExit as e:
        # argparse may call SystemExit for --help etc; rethrow
        raise
    except Exception as e:
        Path("checks/PART_CVII_dd_shrink_run_error.txt").write_text("Runtime error: " + str(e, encoding="utf-8") + "\n" + traceback.format_exc()
        )
        raise
