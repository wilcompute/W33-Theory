#!/usr/bin/env python3
"""Install the BT777 GitHub Actions workflow locally.

The ChatGPT GitHub connector may block direct writes to .github/workflows.
Run this script from a normal checkout to create the workflow file locally.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "bt766_bt777_suite.yml"

WORKFLOW = """name: BT766 BT777 Suite

on:
  push:
    branches:
      - master
  pull_request:
    branches:
      - master
  workflow_dispatch:

jobs:
  suite:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install numpy networkx
      - name: Run theorem suite
        run: python analysis/bt777_run_bt766_bt776_suite.py
"""


def main() -> None:
    WORKFLOW_PATH.parent.mkdir(parents=True, exist_ok=True)
    WORKFLOW_PATH.write_text(WORKFLOW)
    print(f"Wrote {WORKFLOW_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
