#!/usr/bin/env python3
"""Canonical executable entrypoint for the explicit rank-81 Steinberg bridge."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.pass1142_1146_bundle_runtime import execute_member
execute_member("analysis/w33_pass1142_1146_intertwiner.py", globals())
