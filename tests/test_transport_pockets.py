import subprocess
from pathlib import Path

def test_transport_pockets(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    geom = repo / 'pocket_geometry.json'
    assert geom.exists()
    res = subprocess.run([".venv\Scripts\python.exe", str(repo / "tools" / "transport_pockets.py"), "--pocket_json", str(geom)], cwd=repo, capture_output=True, text=True)
    assert res.returncode == 0
    out = res.stdout
    assert 'built 540 pockets' in out
    assert '270 twin pairs' in out
    assert 'success count 480' in out
    # also ensure report file created
    report = repo / 'out' / 'transport_report.json'
    assert report.exists()
    data = report.read_text(encoding="utf-8")
    assert '"successful_extensions": 480' in data
