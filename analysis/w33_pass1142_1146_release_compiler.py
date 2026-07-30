#!/usr/bin/env python3
"""Read-only compatibility summary for the transparent Pass 1147 release."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.pass1147_transparent_runtime import (
    REQUIRED_SECTIONS,
    obtain_certificate,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        help="validate an existing Pass 1147 certificate instead of running GAP",
    )
    args = parser.parse_args()
    certificate, source_executed, _ = obtain_certificate(
        args.certificate,
        REQUIRED_SECTIONS,
    )
    print(
        json.dumps(
            {
                "schema": "w33.pass1142_1146.release_compatibility.v1",
                "status": "PASS",
                "canonical_schema": certificate["schema"],
                "validated_sections": list(REQUIRED_SECTIONS),
                "gap_source_executed": source_executed,
                "writes_tracked_artifacts": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
