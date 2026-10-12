import json
from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis"/"w33_20261011_h27_hesse_cubic_f_flat_lock.py"
SPEC=importlib.util.spec_from_file_location("h27_hesse_lock",SCRIPT)
M=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)

def test_certificate_replays():
    got=M.payload()
    frozen=json.loads((ROOT/"data/w33_20261011_h27_hesse_cubic_f_flat_lock.json").read_text())
    assert got==frozen

def test_hesse_cubic_f_flat_lock():
    p=M.payload()
    assert p["degree3"]["H27_invariant_dimension"]==2
    assert p["singular_pencil"]["projective_members"]==4
    assert p["singular_pencil"]["union_critical_rays"]==12
    assert p["singular_pencil"]["equals_qutrit_stabilizer_set"]
    assert all(p["checks"].values())
