#!/usr/bin/env python3
import subprocess
import sys
files = [
    'tests/test_bt1208_table_writer_status.py',
    'tests/test_bt1209_iso_sampler_status.py',
    'tests/test_bt1210_half_fiber_table_status.py',
    'tests/test_bt1211_execution_pipeline_status.py',
]
raise SystemExit(subprocess.call([sys.executable, '-m', 'pytest', '-q'] + files))
