#!/usr/bin/env python3
import subprocess
import sys
files = ['tests/test_bt1187_edge_support_map.py', 'tests/test_bt1188_correlation_table_status.py', 'tests/test_bt1189_s3_port_refinement.py']
raise SystemExit(subprocess.call([sys.executable, '-m', 'pytest', '-q'] + files))
