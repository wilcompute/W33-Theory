from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_20260923_corrected_weil_hodge_e6_physics.py"
DATA = ROOT / "data/w33_20260923_corrected_weil_hodge_e6_physics.json"


def load_module():
    spec = importlib.util.spec_from_file_location("w33_corrected_weil", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_corrected_weil_lift_and_phase_firewall():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    a = d["attack1_corrected_Weil6"]
    assert a["single_sector"]["retained_phase_Clifford_order"] == 648
    assert a["full_similitude"]["order"] == 1296
    assert a["trace_field"]["field"] == "Q"
    assert a["trace_field"]["order18_elements_absent"] is True


def test_allq_hodge_and_hamiltonian_normal_form():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    h = d["attack2_Z3_Hamiltonian_classification"]
    assert h["neutral_levels"] == 86
    assert h["forced_matter_doublets"] == 81
    assert h["real_parameter_count_C_and_T"] == 10302
    assert max(h["synthetic"].values()) < 1e-10

    a = d["attack3_allq_weighted_Hodge"]
    q3 = next(x for x in a["instances"] if x["q"] == 3)
    assert q3["b1"] == 81
    assert q3["supertrace"] == -80
    assert all(abs(q3["lambda_n"][str(i)] - v) < 1e-12 for i, v in enumerate((0.0, 4.8, 19.2, 43.2)) if i)


def test_fi_packet_is_fail_closed_and_scaled():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    fi = d["attack4_FI_fail_closed_monte_carlo"]
    assert fi["rates"]["good"] > 0.99
    assert max(v for k, v in fi["rates"].items() if k != "good") < 0.001
    assert fi["supercycles_good"] == 80


def test_outer_e6_and_mckean_singer_certificates():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    extra = d["outside_box"]
    e6 = extra["A_E6_Weil_phase_triality"]["facts"]
    assert e6["WE6_order"] == 51840
    assert e6["WE6_point_stabilizer_order"] == 1296
    assert e6["Out_order"] == 3
    assert e6["WE6_6D_restrictions_in_outer_orbit"] is True
    assert extra["B_allq_McKean_Singer"]["identity"] == "Str exp(-tL)=1-q^4 for every t"


def test_all_declared_checks_pass():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    assert all(d["checks"].values())
