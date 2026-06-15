#!/usr/bin/env python3
import subprocess
import sys

cmd = [sys.executable, '-m', 'pytest', '-q', 'tests/test_bt1164_count.py', 'tests/test_bt1165_grade_type_counts.py', 'tests/test_bt1166_count45.py']
raise SystemExit(subprocess.call(cmd))
