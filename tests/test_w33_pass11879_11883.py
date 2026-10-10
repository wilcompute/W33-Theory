import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11879_11883_e8_higgs_siegel_modulus.json"


def test_e8_higgs_siegel_modulus():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11879_11883_e8_higgs_siegel_modulus.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["11880_breaking"]["witting_stabiliser_dims"] == [24]
    assert d["11881_potential"]["independent_quartic_invariants"] == 2
    assert d["11882_invariants"]["invariant_counts_by_degree"]["12"] == 1
