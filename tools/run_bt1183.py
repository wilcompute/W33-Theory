#!/usr/bin/env python3
import subprocess
import sys
cmd = [sys.executable, '-m', 'pytest', '-q', 'tests/test_bt1180_boolean_transport_2cover.py', 'tests/test_bt1181_pairdict.py', 'tests/test_bt1182_z2_cover_centralizer96.py', 'tests/test_bt1183_z2_cover_centralizer.py']
raise SystemExit(subprocess.call(cmd))
