#!/usr/bin/env python3
"""Transparent compatibility validator for the Pass 1142 exact results."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.pass1147_transparent_runtime import obtain_certificate


REQUIRED = ("directed_schlaefli", "a2_color_torsor")


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
        REQUIRED,
    )
    print(
        json.dumps(
            {
                "schema": "w33.pass1142.exact_compatibility.v1",
                "status": "PASS",
                "canonical_schema": certificate["schema"],
                "validated_sections": list(REQUIRED),
                "gap_source_executed": source_executed,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
