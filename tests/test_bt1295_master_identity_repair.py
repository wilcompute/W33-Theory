import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "BT1295_q3_master_identity.py"
RESULT = ROOT / "BT1295_q3_master_identity_results.json"
REPORT = ROOT / "BT1295_BT1296_BT1297_breakthrough_report.md"


def load_bt1295():
    spec = importlib.util.spec_from_file_location("bt1295", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bt1295_all_faces_pass_with_repaired_formulas():
    bt1295 = load_bt1295()
    faces, all_pass = bt1295.verify_all_faces()

    assert all_pass is True
    assert faces["C_SRG_vertex_count"]["v"] == 40
    assert faces["C_SRG_vertex_count"]["formula"] == "(q+1)*(q^2+1)"

    cayley = faces["J_Cayley_diameter"]
    assert cayley["formula_4q_plus_2"] == 14
    assert "formula_q2_plus_q_plus_2" not in cayley
    assert "4q+2" in cayley["proof_note"]

    branching = faces["K_branching_number"]
    assert branching["polar_half_shell"] == 20
    assert branching["two_half_shells"] == 40
    assert branching["pass"] is True


def test_bt1295_script_regenerates_pass_json():
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    data = json.loads(RESULT.read_text(encoding="utf-8"))

    assert data["status"] == "PASS"
    assert data["all_faces_pass"] is True
    assert data["faces"]["C_SRG_vertex_count"]["v"] == 40
    master = data["unified_identity"]["master_identity"]
    assert "(q+1)(q^2+1)=40" in master
    assert "4q+2" in master


def test_breakthrough_report_records_bt1298_repair_boundary():
    text = REPORT.read_text(encoding="utf-8")
    assert "(q+1)(q^2+1)" in text
    assert "4q+2" in text
    assert "BT1298 repaired the executable witness" in text


if __name__ == "__main__":
    test_bt1295_all_faces_pass_with_repaired_formulas()
    test_bt1295_script_regenerates_pass_json()
    test_breakthrough_report_records_bt1298_repair_boundary()
    print("BT1295 master identity repair regression PASS")
