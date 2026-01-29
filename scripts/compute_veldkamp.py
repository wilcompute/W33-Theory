#!/usr/bin/env python3
import json
import traceback
import sys
from pathlib import Path

try:
    from src.finite_geometry.veldmap import summarize_veldkamp
    csv = Path('bundles/v23_toe_finish/v23/Q_triangles_with_centers_Z2_S3_fiber6.csv')
    s = summarize_veldkamp(csv)
    print(json.dumps(s, indent=2))
except Exception as e:
    traceback.print_exc()
    sys.exit(1)
