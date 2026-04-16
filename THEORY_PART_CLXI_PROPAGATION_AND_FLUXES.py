#!/usr/bin/env python3
"""
Wrapper to run pillars/THEORY_PART_CLXI_PROPAGATION_AND_FLUXES.py
"""

import runpy
import pathlib
import sys

script = pathlib.Path(__file__).parent / "pillars" / "THEORY_PART_CLXI_PROPAGATION_AND_FLUXES.py"
if not script.exists():
    print(f"Missing script: {script}", file=sys.stderr)
    sys.exit(1)
runpy.run_path(str(script), run_name="__main__")
