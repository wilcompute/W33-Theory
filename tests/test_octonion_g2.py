import subprocess
from pathlib import Path
import json

def test_octonion_g2(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    # run the tool in quick mode to avoid heavy computation but still produce outputs
    res = subprocess.run([
        ".venv\\Scripts\\python.exe",
        str(repo / "tools" / "octonion_g2.py"),
        "--quick"
    ], cwd=repo)
    assert res.returncode == 0
    # check output files
    stats_file = repo / 'octonion_rep_stats.json'
    deriv_file = repo / 'octonion_derivations.json'
    assert stats_file.exists()
    assert deriv_file.exists()
    stats = json.loads(stats_file.read_text(encoding="utf-8"))
    assert stats.get('orbit_size') == 480
    assert stats.get('null_dim') == 14
    assert stats.get('fix_dim') == 8
    deriv = json.loads(deriv_file.read_text(encoding="utf-8"))
    assert deriv.get('null_dim') == 14
    assert deriv.get('fix_dim') == 8
    # also verify the so7-specific output
    so7_file = repo / 'octonion_g2_so7.json'
    assert so7_file.exists()
    so7 = json.loads(so7_file.read_text(encoding="utf-8"))
    assert so7.get('null_dim') == 14
    assert so7.get('fix_dim') == 8
    assert len(so7.get('basis7', [])) == 14
    # check skew-symmetry of each 7x7 basis matrix
    for M in so7['basis7']:
        for i in range(7):
            for j in range(7):
                assert M[i][j] == -M[j][i]
