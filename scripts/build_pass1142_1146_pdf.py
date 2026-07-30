#!/usr/bin/env python3
"""Fail-closed notice for the unrecovered Pass 1142-1146 PDF builder.

The release Markdown and exact certificates remain the reviewable publication
surfaces.  PDF packaging is deliberately disabled until a deterministic,
checked-in renderer replaces the source lost in the corrupted bundle.
"""
from __future__ import annotations

import argparse


MESSAGE = (
    "Pass 1142-1146 PDF generation is quarantined: its source was not "
    "recoverable from the corrupted bundle. Use PASS1142_1146_EXACT_RELEASE.md "
    "and the checked-in JSON certificates."
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    raise SystemExit(MESSAGE)


if __name__ == "__main__":
    main()
