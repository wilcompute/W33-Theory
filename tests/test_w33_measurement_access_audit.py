from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_measurement_access_audit.py"
DATA = ROOT / "analysis/w33_measurement_access_audit.json"


def load_script():
    spec = importlib.util.spec_from_file_location("measurement_access_audit_test", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_checked_inventory_is_scoped_and_synthetic_trace_is_fenced():
    checked = json.loads(DATA.read_text())
    assert checked["schema"] == "w33.measurement_access_audit.v2"
    assert checked["status"] == "AWAITING_IDENTIFIED_INSTRUMENT_AND_CALIBRATION"
    assert checked["selection"] == {
        "identified_instrument": None,
        "measured_trace": None,
        "independent_calibration": None,
    }
    windows = checked["interface_inventory"]["windows_serial"]
    assert windows["returncode"] == 0
    assert all("Bluetooth" in row["name"] for row in windows["ports"])
    assert checked["interface_inventory"]["visa"]["enumerated"] is False
    assert checked["interface_inventory"]["network_instruments"]["enumerated"] is False
    assert checked["synthetic_fixture_firewall"] == {
        "path": "analysis/w33_oscillator_calibration_test.json",
        "data_origin": "synthetic seeded Gaussian fixture, not hardware measurements",
        "may_be_used_as_measurement": False,
        "mass_stiffness_scale_identified": False,
    }


def test_readiness_requires_all_three_inputs(monkeypatch, tmp_path):
    module = load_script()
    fake_windows = {
        "attempted": False,
        "executable": None,
        "command": module.WINDOWS_SERIAL_QUERY,
        "returncode": None,
        "stderr": "test fixture",
        "ports": [],
    }
    monkeypatch.setattr(module, "windows_serial_inventory", lambda: fake_windows)
    monkeypatch.setattr(module, "visible_nodes", lambda pattern: [])
    monkeypatch.setattr(module, "repository_candidates", lambda: [])
    trace = tmp_path / "measured.csv"
    calibration = tmp_path / "calibration.json"
    trace.write_text("t,y\n0,1\n")
    calibration.write_text("{}\n")

    incomplete = module.audit(
        instrument="scope-1",
        measured_trace=str(trace),
        checked_utc="2000-01-01T00:00:00+00:00",
    )
    assert incomplete["status"] == "AWAITING_IDENTIFIED_INSTRUMENT_AND_CALIBRATION"

    ready = module.audit(
        instrument="scope-1",
        measured_trace=str(trace),
        independent_calibration=str(calibration),
        checked_utc="2000-01-01T00:00:00+00:00",
    )
    assert ready["status"] == "READY_FOR_READONLY_TRACE_INGEST"

