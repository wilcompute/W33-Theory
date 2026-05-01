import json
import subprocess
from pathlib import Path

import pytest


def test_a2_darkstate_v14_dark_state_and_a2_roots():
    script = (
        Path("toe_session_20260316_v14")
        / "toe_session_20260316_v14"
        / "w33_a2_darkstate_v14.py"
    )
    if not script.exists():
        pytest.skip(
            "toe_session_20260316_v14 is an optional session export; "
            "materialize it to run the v14 A2 dark-state regression"
        )

    subprocess.run(["py", "-3", str(script)], check=True)

    results_path = (
        Path("toe_session_20260316_v14")
        / "toe_session_20260316_v14"
        / "w33_a2_darkstate_results_v14.json"
    )
    data = json.loads(results_path.read_text(encoding="utf-8"))

    # check the dark-state claim (v0 is eigenvector with eigenvalue a1)
    assert data["minimal_breaker_theorem"]["dark_state"].startswith(
        "v0 is an exact eigenvector"
    )

    # check that P1(t)=P2(t) is asserted
    probs = data["minimal_breaker_theorem"]["probabilities_from_generation_0"]
    assert "P1(t)" in probs and "P2(t)" in probs
    assert "P1(t)=P2(t)" in probs["identity"]

    # check A2 Cartan matrix is exactly [[2,-1],[-1,2]]
    cartan = data["a2_root_bridge"]["scaled_trace_Cartan"]
    assert cartan == [["2", "-1"], ["-1", "2"]]
