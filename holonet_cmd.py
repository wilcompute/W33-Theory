#!/usr/bin/env python3
"""
holonet_cmd -- console-script entry point for the holonet CLI.

This thin shim makes `holonet` a real installed command. After `pip install -e .` from the repo root,
the `holonet` command is available system-wide; it forwards to the universal-VM CLI in
analysis/holonet_cli.py (route / teleport / correct / reproduce / verify / info). The shim only adds the
analysis directory to the import path and calls the CLI's main, so the installed command and
`py -3 analysis/holonet_cli.py` behave identically.

Usage after install:
    pip install -e .
    holonet verify
    holonet route 0001 0010
"""
from __future__ import annotations

import os
import sys


def main(argv=None):
    sys.path.insert(
        0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis")
    )
    import holonet_cli  # noqa: E402

    holonet_cli.main(argv)


if __name__ == "__main__":
    main()
