#!/usr/bin/env python3
"""Canonical entrypoint for the Pass 1142-1146 release-PDF builder."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.pass1142_1146_bundle_runtime import execute_member
execute_member("scripts/build_pass1142_1146_pdf.py", globals())
