import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_bridge() -> dict:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "analysis" / "w33_selector_e6_e8_runtime_bridge.py"),
        ],
        cwd=ROOT,
        check=True,
    )
    return json.loads(
        (ROOT / "data" / "w33_selector_e6_e8_runtime_bridge.json").read_text(
            encoding="utf-8"
        )
    )


def test_selector_e6_e8_runtime_bridge_closes_support_clock():
    data = run_bridge()

    assert data["verified"] is True
    assert all(data["checks"].values())
    selector = data["selector_e6_surface"]
    runtime = data["runtime_surface"]

    assert selector["sheet_count"] == 120
    assert selector["sheet_self_support"] == 108
    assert selector["we6_irrep_dimensions"] == [1, 15, 20, 24, 60]
    assert selector["twisted_conflict_count"] == 760

    assert runtime["frequency_probe_rows_per_supercycle"] == 12960
    assert runtime["runtime_slots_per_probe"] == 4
    assert runtime["we6_order"] == 51840
    assert 120 * 108 == 12960
    assert 12960 * 4 == 51840


def test_selector_e6_e8_runtime_bridge_exposes_e8_signed_sheet_budget():
    data = run_bridge()
    e8 = data["e8_surface"]
    runtime = data["runtime_surface"]

    assert e8["signed_sheet_count"] == 240
    assert e8["cartan_match"] is True
    assert abs(e8["basis_det"]) == 1
    assert runtime["runtime_slots_per_signed_sheet_accounting"] == 216
    assert 240 * 216 == 51840
    assert data["checks"]["C11_signed_sheet_budget_is_e8_root_budget"] is True


def test_selector_e6_e8_runtime_bridge_keeps_boundary_honest():
    data = run_bridge()
    boundary = " ".join(data["claim_boundary"])

    assert "not a proof of a canonical sheet-to-root bijection" in boundary
    assert "bench data" in boundary
    assert "exact quotient budgets" in boundary
    assert "canonical" in boundary
    assert "source_certificates" in data
    assert "data/bt982_explicit_integral_e8_basis.json" in data["source_certificates"]
    assert "data/w33_frequency_bin_lab_packet.json" in data["source_certificates"]


def test_selector_e6_e8_runtime_bridge_publication_anchor():
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert 'id="selector-e6-e8-runtime-bridge"' in docs
    assert "w33_selector_e6_e8_runtime_bridge.py" in docs
    assert "w33_selector_e6_e8_runtime_bridge.json" in docs
    assert "120 sheets &times; 108 support = 12960 probes" in docs
    assert "240&times;216 = 51840" in docs
