#!/usr/bin/env python3
import subprocess
import sys
files = ['tests/test_bt1191_support_pair_bt748.py', 'tests/test_bt1192_s3_vs_z2.py', 'tests/test_bt1193_s3_shadow_obstruction.py']
cmd = [sys.executable, '-m', 'pytest', '-q'] + files
raise SystemExit(subprocess.call(cmd))
