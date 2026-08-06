import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis"/"w33_pass3937_3956_rho200_poset_monster_octonion_universal_photon.py"
RESULT=ROOT/"data"/"PART_3937_3956_RHO200_POSET_MONSTER_OCTONION_UNIVERSAL_PHOTON_results.json"

def test_exact_certificate():
    cp=subprocess.run([sys.executable,str(SCRIPT),"--input",str(RESULT),"--print"],
                      check=True,capture_output=True,text=True)
    observed=json.loads(cp.stdout)
    assert observed["semantic_sha256"]=="14cc255a662b55b8a86ba020ae00392faaad50be04ebbb5027a52d470ad3ef54"
    assert all(observed["checks"].values())

def test_manifest_firewalls():
    manifest=json.loads(RESULT.read_text())
    assert manifest["status"].endswith("PENDING")
    assert "Monster" in " ".join(manifest["pending"])
    assert "node count alone cannot alter vacuum c" in manifest["headline_results"]["photon_null_processor"]
