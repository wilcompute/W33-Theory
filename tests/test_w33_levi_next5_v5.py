from __future__ import annotations
import json
import py_compile
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name):
    return json.loads((DATA / f"PART_2026_07_11_LEVI_NEXT5_V5_{name}.json").read_text())


def fresh(name):
    p = subprocess.run([sys.executable, str(ROOT / "analysis" / f"w33_levi_next5_v5_{name}.py")], cwd=ROOT, capture_output=True, text=True, check=True, timeout=240)
    return json.loads(p.stdout)


def test_fourier_geometry():
    d=load("fourier"); assert d["status"]=="PASS"
    assert (d["heisenberg_q3"]["point_block_rank"], d["heisenberg_q3"]["incidence_column_span_dimension"], d["heisenberg_q3"]["line_gram_diagonal_rank"]) == (3,6,3)
    assert d["full_w33"]["jordan_blocks"] == {"J1":6,"J2":0,"J3":22,"J4":2}


def test_h2_transgression_and_gauge():
    d=load("extension"); assert d["status"]=="PASS"
    assert d["periodic_cohomology"]["H1_dimension"]==3
    assert d["periodic_cohomology"]["H2_dimension"]==3
    assert len(d["H2_extensions"])==8
    assert d["transgression"]["delta_class"]=="0x0"
    assert d["checks"]["gauged_order8_generator_fixed"]


def test_e8_runtime_lanes():
    d=load("lanes"); assert d["status"]=="PASS"
    assert d["decomposition"]["orbit_sizes"] == [1]*6+[27]*6+[72]
    assert d["routing"]["payload_addresses"]==162
    assert d["routing"]["control_fanout_per_payload"]=={"minus":16,"orthogonal":40,"plus":16}
    assert d["falsifier"]["passed"] and d["falsifier"]["steps"]==50000


def test_hybrid_hardware_budget():
    d=load("hybrid"); assert d["status"]=="PASS"
    assert d["power_budget"]["total_mw"] < 100
    assert d["foundry_corners"]["p05"] > .999
    assert d["drift"]["tracked_min"] > .999
    assert len((ROOT/"hardware/holonet_v5_hybrid.gds.b64").read_text()) > 30000


def test_vendor_fpga_runtime():
    d=load("hardware"); assert d["status"]=="PASS"
    assert d["fpga"]["input_events"] > 1_000_000
    assert d["fpga"]["frames"]==256
    assert all(d["checks"].values())


def test_all_fresh_witnesses():
    for name in ("fourier","extension","lanes","hybrid","hardware"):
        assert fresh(name)["status"]=="PASS"


def test_sources_compile_and_formal_imported():
    for p in (ROOT/"analysis").glob("w33_levi_next5_v5*.py"):
        py_compile.compile(str(p), doraise=True)
    assert "import W33.HeisenbergQ3" in (ROOT/"formal/W33.lean").read_text()


def test_cli_routes_and_aggregate():
    source=(ROOT/"holonet_cmd.py").read_text()
    for cmd in ("fourier-geometry-v5","extension-cohomology-v5","e8-lanes-v5","hybrid-compiler-v5","hardware-runtime-v5","levi-next5-v5"):
        assert cmd in source
    d=load("results"); assert d["status"]=="PASS" and all(d["checks"].values())
