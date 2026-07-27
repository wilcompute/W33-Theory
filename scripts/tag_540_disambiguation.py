#!/usr/bin/env python3
"""Canonical Pass 1145 occurrence classifier with content-hashed registry support."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.pass1142_1146_bundle_runtime import execute_member
execute_member("scripts/tag_540_disambiguation.py", globals())
