from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_20260923_next5_plus3_physics.py"
FROZEN = ROOT / "data/w33_20260923_next5_plus3_physics_frozen.json"


def load_module():
    spec = importlib.util.spec_from_file_location("w33_next5_plus3_physics", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_next5_plus3_physics_replays_core_certificates():
    m = load_module()
    out = m.main(write=False)
    frozen = json.loads(FROZEN.read_text())

    assert out["status"] == frozen["status"]
    assert all(out["checks"].values())

    # Attack 1: the completion is self-dual and has the exact adjoint identity.
    assert out["attack1"]["doubled_cells"] == [80, 400, 400, 80]
    assert out["attack1"]["doubled_betti"] == [1, 81, 81, 1]
    assert all(out["attack1"]["codifferential_checks"].values())

    # Attack 2: preserve the negative result.
    assert "not the canonical free energy" in out["attack2"]["title"]
    assert out["attack2"]["partition_function"] == "Z_q(beta)=2+(q-3) exp(-2 beta)"

    # Attack 3: exact global Floquet data and FI fourth power.
    assert out["attack3"]["order"] == 12
    assert out["attack3"]["trace_U_power_t_for_t0_to11"] == [
        248, 51, 105, 132, 5, 51, 24, 51, 5, 132, 105, 51
    ]
    assert out["attack3"]["fourth_power_grading"]["equals_physical_FI_grading"] is True

    # Attack 4: conservative design still clears 5 sigma at 128 detected events.
    assert out["attack4"]["shot_noise"]["5sigma_detected_events_minimum_worst_binomial_variance_proxy"] <= 128
    assert out["attack4"]["shot_noise"]["recommended_sigma_proxy"] > 5

    # Attack 5: log-index obstruction vanishes only at q=3.
    assert out["attack5"]["cases"]["3"]["zero_obstruction"] is True
    assert out["attack5"]["cases"]["9"]["coset_entropy_bits"] == 2.0
    assert all(
        not row["zero_obstruction"]
        for q, row in out["attack5"]["cases"].items()
        if q != "3"
    )

    # Outside-box probes.
    assert out["outside1"]["cases"]["3"]["charge_conjugate_pair_is_complete"] is True
    assert out["outside1"]["cases"]["5"]["charge_conjugate_pair_is_complete"] is False
    assert out["outside2"]["matrix_checks"]["S_squared_minus_identity"] is True
    assert out["outside3"]["identity_on_E8_grading"] is True
