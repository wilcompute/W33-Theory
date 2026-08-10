import json
import subprocess
from pathlib import Path

def test_pocket_transport_glue(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    bundle_dir = repo / 'TOE_pocket_transport_glue_orbit480_v01_20260227_bundle'
    assert bundle_dir.exists()
    # run recompute to refresh summaries
    res = subprocess.run([".venv\Scripts\python.exe", str(bundle_dir / 'recompute.py')], cwd=repo)
    assert res.returncode == 0
    glue = json.loads((repo / 'pocket_glue_summary.json').read_text(encoding="utf-8"))
    assert glue['total_pockets'] == 540
    assert glue['components'] == 1
    assert glue['glue_solutions'] == 2
    orbit = json.loads((repo / 'orbit_480_summary.json').read_text(encoding="utf-8"))
    assert orbit['orbit_size'] == 480
    assert orbit['group_order'] == 645120
