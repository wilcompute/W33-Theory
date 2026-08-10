import importlib
import json
import subprocess
import sys
from pathlib import Path


def test_verify_and_register_pairs_happy_path(tmp_path, monkeypatch):
    # prepare temporary repo layout
    project_root = tmp_path
    checks = project_root / "checks"
    checks.mkdir()
    # create a fake local_hotspot result with one INFEASIBLE pair
    local = project_root / "local_res.json"
    local.write_text(
        json.dumps(
            {
                "edges": [37, 38],
                "k": 40,
                "radius": 1,
                "time_limit": 5,
                "tests": [{"pair": [37, 28, 38, 22], "status": "INFEASIBLE"}],
            }
        )
    )

    # monkeypatch subprocess.run to simulate solver writing PART_CVII_e8_embedding_cpsat.json
    def fake_run(cmd, check=False, stdout=None, stderr=None, text=True, timeout=None):
        outp = checks / "PART_CVII_e8_embedding_cpsat.json"
        outp.write_text(json.dumps({"status": "INFEASIBLE"}, encoding="utf-8"))

        class Dummy:
            returncode = 0
            stdout = ""
            stderr = ""

        return Dummy()

    monkeypatch.setattr(subprocess, "run", fake_run)

    # set argv and run the module main()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "scripts/verify_and_register_pairs.py",
            "--input",
            str(local),
            "--checks-dir",
            str(checks),
            "--forbid-json",
            str(checks / "forbids.json"),
        ],
    )

    # import and run script
    mod = importlib.import_module("scripts.verify_and_register_pairs")
    mod.main()

    # verify forbid file exists and contains the pair
    forb = json.loads((checks / "forbids.json").read_text(encoding="utf-8"))
    assert "obstruction_sets" in forb
    assert any(
        [
            entry.get("set") == [37, 38] and entry.get("roots") == [28, 22]
            for entry in forb["obstruction_sets"]
        ]
    )
