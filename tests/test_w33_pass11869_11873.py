import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11869_11873_siegel_level3_two_qutrits.json"


def test_siegel_level3_two_qutrits():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11869_11873_siegel_level3_two_qutrits.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    a = d["11869_siegel_is_clifford"]
    assert a["order_generated_mod3"] == 51840
    assert a["order_on_40_points"] == 25920 and a["order_on_40_points_with_CP"] == 51840
    assert d["11870_genus_one_arrow_is_modular_cp"]["max_rel_err_j_hesse_vs_j_tau"] < 1e-10
    c = d["11871_coble_on_burkhardt"]
    assert c["cubic_group_order"] == 103680
    assert c["theta_null_max_abs_I4_of_coble"] < 1e-12 < c["random_min_abs_I4"]
