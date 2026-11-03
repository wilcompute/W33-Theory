import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pass12527_to_12533_producer():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12527_to_12533_frames_knots_burkhardt.py")], check=True, cwd=ROOT,
                   capture_output=True)
    res = json.loads((ROOT / "data" / "w33_pass12527_to_12533_frames_knots_burkhardt.json").read_text())
    assert res["all_checks_pass"], res["checks"]
