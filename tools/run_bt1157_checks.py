#!/usr/bin/env python3
import subprocess
import sys

cmd = [sys.executable, '-m', 'pytest', '-q', 'tests/test_bt1155_boolean_intertwiner.py', 'tests/test_bt1156_negative_sector_grade_decomposition.py', 'tests/test_bt1157_signature_clifford_refinement.py']
raise SystemExit(subprocess.call(cmd))
