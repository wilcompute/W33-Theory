#!/usr/bin/env python3
import subprocess
import sys

cmd = [sys.executable, '-m', 'pytest', '-q', 'tests/test_bt1161_orbit_closed_boolean_module.py', 'tests/test_bt1162_quotient_equivariance.py', 'tests/test_bt1163_projected_boolean_quotient_module.py']
raise SystemExit(subprocess.call(cmd))
