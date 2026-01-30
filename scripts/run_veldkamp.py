import json
import sys
import traceback
from pathlib import Path

try:
    from src.finite_geometry.veldmap import summarize_veldkamp

    p = Path("bundles/v23_toe_finish/v23/Q_triangles_with_centers_Z2_S3_fiber6.csv")
    print("CSV exists:", p.exists())
    s = summarize_veldkamp(p)
    print(json.dumps(s, indent=2))
except Exception:
    traceback.print_exc()
    sys.exit(1)
