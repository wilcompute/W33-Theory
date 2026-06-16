#!/usr/bin/env python3
import subprocess
import sys
files = ['tests/test_bt1194_universal_2160_carrier.py', 'tests/test_bt1195_d4_coset_half_fiber.py', 'tests/test_bt1196_universal2160.py']
raise SystemExit(subprocess.call([sys.executable, '-m', 'pytest', '-q'] + files))
