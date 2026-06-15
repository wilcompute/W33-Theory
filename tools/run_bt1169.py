#!/usr/bin/env python3
import subprocess
import sys
cmd = [sys.executable, '-m', 'pytest', '-q', 'tests/test_bt1167_layer45_model.py', 'tests/test_bt1168_factor3_interpretation.py', 'tests/test_bt1169_layer45.py']
raise SystemExit(subprocess.call(cmd))
