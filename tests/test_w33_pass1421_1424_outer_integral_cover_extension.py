from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1421_1424_outer_integral_cover_extension.py"
DATA = ROOT / "data" / "w33_pass1421_1424_outer_integral_cover_extension.json"


def test_exact_certificate_is_frozen() -> None:
    subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, check=True)
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())
    assert payload["passes"]["1421"]["group_order"] == 51840
    assert payload["passes"]["1423"]["saturation_index"] == 486
    assert payload["passes"]["1424"]["extended_certified_lower_bound"] == 298080
    assert payload["certificate_sha256"] == "27fdcc78da468d8c220fd5f4e7145aa5a50b7cf6789a546b8ae0a046bbedcd30"
