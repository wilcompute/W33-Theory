#!/usr/bin/env python3
"""Canonical entrypoint for the Pass 1144 semantic descendant migration."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.pass1142_1146_bundle_runtime import execute_member
execute_member("scripts/migrate_shifted_adjacency_descendants.py", globals())
