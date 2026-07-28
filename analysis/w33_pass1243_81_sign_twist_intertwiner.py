#!/usr/bin/env python3
"""Executable entrypoint for Pass 1243 from the reviewed exact source bundle."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.pass1243_1247_bundle_runtime import execute_member
execute_member("analysis/w33_pass1243_81_sign_twist_intertwiner.py", globals())
