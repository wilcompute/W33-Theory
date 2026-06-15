#!/usr/bin/env python3
import subprocess
import sys
cmd = [sys.executable, '-m', 'pytest', '-q', 'tests/test_bt1170_incidence45.py', 'tests/test_bt1171_pairmap.py', 'tests/test_bt1172_incidence45.py']
raise SystemExit(subprocess.call(cmd))
