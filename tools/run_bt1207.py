#!/usr/bin/env python3
import subprocess
import sys
files = [
    'tests/test_bt1205_bt748_half_fiber_lookup.py',
    'tests/test_bt1206_raw_z2_vs_packet_s3.py',
    'tests/test_bt1207_holonet_pocket_shell_bus.py',
]
raise SystemExit(subprocess.call([sys.executable, '-m', 'pytest', '-q'] + files))
