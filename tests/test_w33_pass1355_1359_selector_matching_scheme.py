from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1355_1359_selector_matching_scheme.py"
DATA = ROOT / "data" / "w33_pass1355_1359_selector_matching_scheme.json"
EXPECTED_SHA256 = "4efac1631cc6991861a927e04297c4a072b9a2d4e49953642b9113c7e22f87f0"


def load_module():
    spec = importlib.util.spec_from_file_location("pass1355_1359", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_scheme_certificate():
    result = load_module().build()
    assert result["status"] == "PASS"
    assert result["construction"] == {
        "field": 3,
        "points": 40,
        "isotropic_lines": 40,
        "perfect_matchings_per_line": 3,
        "selectors": 120,
    }
    assert result["relations"]["valencies"] == [1, 2, 36, 27, 54]
    assert result["primitive_multiplicities"] == [1, 15, 24, 20, 60]
    assert result["quotient"]["quotient_srg"] == [40, 12, 2, 4]
    assert result["holonomy"]["generated_group"] == "S3"
    assert result["holonomy"]["fiber_kernel"] == "trivial"
    assert result["automorphism"]["scheme_group_order"] == 51840
    assert result["p_polynomial"] is False
    assert result["q_polynomial"] is False


def test_frozen_json_is_byte_exact():
    raw = DATA.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
    parsed = json.loads(raw)
    assert parsed["fusion_partitions"] == [
        [[1], [2], [3], [4]],
        [[1], [2], [3, 4]],
        [[1], [2, 3, 4]],
        [[1, 2, 3, 4]],
    ]


def test_cli_check_mode():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--output", str(DATA), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "PASS 1355-1359" in completed.stdout


def test_integrator_is_idempotent(tmp_path):
    for name in ("w33_paper.tex", "photonic_holonet.tex"):
        (tmp_path / name).write_text("\\documentclass{article}\n\\begin{document}\nfixture\n\\end{document}\n", encoding="utf-8")
    integrator = ROOT / "tools" / "integrate_pass1355_1359.py"
    for _ in range(2):
        subprocess.run([sys.executable, str(integrator), "--root", str(tmp_path)], check=True)
    subprocess.run([sys.executable, str(integrator), "--root", str(tmp_path), "--check"], check=True)
    marker = r"\input{analysis/BT1355_BT1359_selector_matching_scheme}"
    for name in ("w33_paper.tex", "photonic_holonet.tex"):
        assert (tmp_path / name).read_text(encoding="utf-8").count(marker) == 1
