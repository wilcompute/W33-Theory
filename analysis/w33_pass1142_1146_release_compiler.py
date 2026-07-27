#!/usr/bin/env python3
"""Canonical entrypoint that compiles the compact Pass 1142-1146 certificate."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.pass1142_1146_bundle_runtime import execute_member
execute_member("analysis/w33_pass1142_1146_release_compiler.py", globals())
