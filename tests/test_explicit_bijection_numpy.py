import json
from pathlib import Path

from tools.e8_w33_bijection import load_explicit_bijection
from tools.e8_w33_harness import ip_distributions

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "explicit_bijection_decomposition.json"


def ensure_artifact():
    if not ART.exists():
        import runpy
        import subprocess
        import sys

        try:
            runpy.run_path(
                str(ROOT / "tools" / "explicit_bijection_decomposition.py"),
                run_name="__main__",
            )
        except Exception:
            subprocess.check_call(
                [
                    sys.executable,
                    str(ROOT / "tools" / "explicit_bijection_decomposition.py"),
                ]
            )
    assert ART.exists(), "artifact not created"


def test_ip_distribution_snapshot():
    ensure_artifact()
    data = load_explicit_bijection(ART)
    ip_adj, ip_non = ip_distributions(data)

    # Snapshot expectations derived from current canonical bijection
    expected_adj = {-8: 21, -4: 548, 0: 1260, 4: 811}
    expected_non = {-8: 99, -4: 6172, 0: 13860, 4: 5909}

    assert ip_adj == expected_adj
    assert ip_non == expected_non
