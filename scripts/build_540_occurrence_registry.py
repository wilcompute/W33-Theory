#!/usr/bin/env python3
"""Canonical entrypoint for the Pass 1145 zero-ambiguity 540 registry builder."""  # {540:mixed}
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.pass1142_1146_bundle_runtime import execute_member
execute_member("scripts/build_540_occurrence_registry.py", globals())
