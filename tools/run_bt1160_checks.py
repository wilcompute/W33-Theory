#!/usr/bin/env python3
import subprocess
import sys

cmd = [sys.executable, '-m', 'pytest', '-q', 'tests/test_bt1158_obstruction.py', 'tests/test_bt1159_deterministic_boolean_search.py', 'tests/test_bt1160_boolean_bridge_obstruction.py']
raise SystemExit(subprocess.call(cmd))
