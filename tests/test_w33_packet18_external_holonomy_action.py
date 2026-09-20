import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run_script(name: str, out: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / "analysis" / name)], cwd=ROOT, check=True)
    return json.loads((ROOT / "data" / out).read_text(encoding="utf-8"))

def test_packet18_external_holonomy_action_closes():
    d = run_script(
        "w33_packet18_external_regular_holonomy_action.py",
        "w33_packet18_external_regular_holonomy_action.json",
    )
    assert d["status"] == "PASS_EXTERNAL_REGULAR_HOLONOMY_ACTION"
    assert d["runtime"]["Aut_G_X"] == "N_G(H)/H ~= C2"
    assert d["deck"]["commutes_with_full_left_G_action"] is True
    assert d["holonomy_action"]["regular_on_packet18"] is True
    assert d["holonomy_action"]["physical_C6_profile"] == {"6_cycles": 3}
    assert all(d["checks"].values())

def test_packet72_physical_c6_compiler_closes():
    d = run_script(
        "w33_packet72_physical_c6_address_compiler.py",
        "w33_packet72_physical_c6_address_compiler.json",
    )
    assert d["status"] == "PASS_LOOKUP_FREE_CONTROL_PLANE_COMPILER"
    assert d["cycle_profiles"]["packet18"] == {"6_cycles": 3}
    assert d["cycle_profiles"]["packet72"] == {"6_cycles": 12}
    assert d["power_laws"]["g3"] == "a fixed, b->1-b (pure deck parity)"
    assert d["hardware_read"].startswith("no lookup table")
    assert all(d["checks"].values())
