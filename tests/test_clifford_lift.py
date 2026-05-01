import json
import subprocess
import sys
from pathlib import Path


def test_clifford_lift_verifies(tmp_path):
    # Run the Clifford-lift builder on the W33 bundle and assert both generators verify.
    sys.path.insert(0, str(Path("tools").resolve()))
    from tools import build_qutrit_clifford_lift as clf

    bundle_dir = tmp_path / "bundle"
    export_run = subprocess.run(
        [
            sys.executable,
            "tools/export_w33_heisenberg_bundle.py",
            "--out-dir",
            str(bundle_dir),
            "--v0",
            "0",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    assert export_run.returncode == 0, export_run.stderr

    argv_backup = sys.argv.copy()
    try:
        outdir = tmp_path / "analysis"
        sys.argv = [
            "clf",
            "--bundle-dir",
            str(bundle_dir),
            "--out-dir",
            str(outdir),
        ]
        clf.main()
        outp = outdir / "clifford_lift_on_H27_and_N12.json"
        assert outp.exists()
        j = json.loads(outp.read_text(encoding="utf-8"))
        gens = j.get("generators", [])
        names = {g["name"]: g for g in gens}
        assert names["S"]["verified"] is True
        assert names["T"]["verified"] is True
    finally:
        sys.argv = argv_backup
