#!/usr/bin/env python3
import subprocess
import sys
cmd = [sys.executable, '-m', 'pytest', '-q', 'tests/test_bt1176_intrinsic_sp42_s6_dictionary.py', 'tests/test_bt1177_schlafli_27_triangle_bridge.py', 'tests/test_bt1178_z2_audit.py', 'tests/test_bt1179_z2_obstruction.py']
raise SystemExit(subprocess.call(cmd))
