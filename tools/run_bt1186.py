#!/usr/bin/env python3
import subprocess
import sys
files = ['tests/test_bt1184_correlation_audit.py', 'tests/test_bt1185_raw_voltage_2cover_invariants.py', 'tests/test_bt1186_voltage_note.py']
raise SystemExit(subprocess.call([sys.executable, '-m', 'pytest', '-q'] + files))
