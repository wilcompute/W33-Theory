import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11874_11878_siegel_fixed_points_cp_magic.json"


def test_siegel_fixed_points_cp_magic():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11874_11878_siegel_fixed_points_cp_magic.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    orders = sorted(r["stabiliser_order"] for r in d["11874_fixed_points"])
    assert orders == [10, 24, 24, 32, 48, 72]
    assert d["11875_weil_5_plus_4"]["commutant_dims"] == {"even": 1, "odd": 1}
    assert d["11876_hierarchy"]["R_spread"] > 10
