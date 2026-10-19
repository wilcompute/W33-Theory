import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12084_the_corpus_orbifold_uses_the_split_form.json"


def test_the_corpus_orbifold_uses_the_split_form():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12084_the_corpus_orbifold_uses_the_split_form.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
