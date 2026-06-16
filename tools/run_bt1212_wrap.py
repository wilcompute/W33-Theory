#!/usr/bin/env python3
import subprocess
import sys
files = ['tests/test_bt1212_materialized_z2_s3.py']
raise SystemExit(subprocess.call([sys.executable, '-m', 'pytest', '-q'] + files))
