#!/usr/bin/env python3
import subprocess
import sys
files = [
    'tests/test_bt1201_objectwise_labels.py',
    'tests/test_bt1202_parity_candidates.py',
    'tests/test_bt1203_54x40_w33_shells.py',
    'tests/test_bt1204_labelled_2160.py',
]
raise SystemExit(subprocess.call([sys.executable, '-m', 'pytest', '-q'] + files))
