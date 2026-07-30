#!/usr/bin/env python3
"""Read-only compatibility audit for the completed Pass 1144 migration.

The semantic migration has already been materialized and recorded in the
version-3 retraction ledger.  This historical command name now delegates to
the checked-in descendant guard; it cannot modify corpus files.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_shifted_adjacency_descendants import audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="accepted for compatibility; this command is always read-only",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="retired: Pass 1144 has already been materialized",
    )
    args = parser.parse_args()

    if args.apply:
        raise SystemExit(
            "Pass 1144 migration is retired; --apply is disabled. "
            "Run the read-only descendant audit instead."
        )

    result = audit(args.root)
    print(
        json.dumps(
            {
                "schema": "w33.pass1144.migration_compatibility_audit.v1",
                "status": result["status"],
                "read_only": True,
                "summary": result["summary"],
                "violations": result["violations"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
