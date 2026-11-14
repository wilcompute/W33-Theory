from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def run(script: str, output: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / "analysis" / script)], cwd=ROOT, check=True)
    return json.loads((DATA / output).read_text(encoding="utf-8"))


def test_twisted_port_local_system() -> None:
    result = run("bt3274_3275_twisted_port_local_system.py", "PART_BT3274_BT3275_TWISTED_PORT_LOCAL_SYSTEM_results.json")
    controls = {row["name"]: row for row in result["controls"]}
    assert controls["trivial_rank_two"]["dim_H1"] == 872
    assert controls["d4_quarter_turn"]["dim_H0"] == 0
    assert controls["d4_quarter_turn"]["dim_H1"] == 870
    assert controls["d4_quarter_turn"]["twisted_euler_characteristic"] == -870


def test_independent_curvature_quotient() -> None:
    result = run("bt3276_3277_independent_curvature_quotient.py", "PART_BT3276_BT3277_INDEPENDENT_CURVATURE_QUOTIENT_results.json")
    assert result["hypotheses"] == 48_826
    assert result["base_signatures"] == 46_284
    assert result["collision_classes"] == 1_436
    assert result["quotient_states"] == 876
    assert result["initial_quotient_states"] == 770
    assert result["traversal_independent_partition"] is True


def test_runtime_universe_firewall() -> None:
    result = run("bt3278_3279_runtime_universe_firewall.py", "PART_BT3278_BT3279_RUNTIME_UNIVERSE_FIREWALL_results.json")
    assert result["universes"]["baseline4"]["observed_size"] == 2
    assert result["universes"]["census56"]["observed_size"] in {1, 194}
    assert len(result["cross_universe_refusals"]) == 2
    assert result["malformed_universe_control_refused"] is True
    assert result["census_pending_records"] in {193, 0}


def test_constrained_reset_rank_floor() -> None:
    result = run("bt3280_3281_constrained_reset_semigroup.py", "PART_BT3280_BT3281_CONSTRAINED_RESET_SEMIGROUP_results.json")
    assert result["quotient_states"] == 876
    assert set(result["terminal_witnesses"]) == {"none", "flat", "curved"}
    assert len(set(result["terminal_witnesses"].values())) == 3
    assert result["global_unauthorized_rank_floor"] == 3
    assert result["authorized_reset"]["rank"] == 1
    assert result["authorized_reset"]["shortest_word_length"] == 1
