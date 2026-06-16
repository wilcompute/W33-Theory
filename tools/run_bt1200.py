#!/usr/bin/env python3
import subprocess
import sys
files = [
    'tests/test_bt1197_universal_2160_projection_codec.py',
    'tests/test_bt1198_z2_projection.py',
    'tests/test_bt1199_s3_projection.py',
    'tests/test_bt1200_2160_projection_codec.py',
]
raise SystemExit(subprocess.call([sys.executable, '-m', 'pytest', '-q'] + files))
