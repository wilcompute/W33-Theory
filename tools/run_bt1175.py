#!/usr/bin/env python3
import subprocess
import sys
cmd = [sys.executable, '-m', 'pytest', '-q', 'tests/test_bt1173_s6_sp42_naturality.py', 'tests/test_bt1174_center_quad_incidence45.py', 'tests/test_bt1175_triple45_bridge.py']
raise SystemExit(subprocess.call(cmd))
