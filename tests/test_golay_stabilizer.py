import subprocess
from pathlib import Path

def test_golay_stabilizer(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    res = subprocess.run([".venv\\Scripts\\python.exe", str(repo / "tools" / "golay_stabilizer.py")], cwd=repo)
    assert res.returncode == 0
    outfile = repo / "artifacts" / "golay_stabilizer_generators.txt"
    assert outfile.exists()
    lines = outfile.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 12
    for line in lines:
        xs, zs = line.split()
        assert len(xs)==12 and len(zs)==12
