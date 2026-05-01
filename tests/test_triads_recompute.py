import csv
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def load_recorded(path: Path):
    d = {}
    with path.open("r", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            if r.get("triad"):
                parts = [int(x) for x in r["triad"].split()]
                tri = tuple(sorted(parts))
            else:
                tri = tuple(sorted((int(r["a"]), int(r["b"]), int(r["c"]))))
            if r.get("hol_mod12"):
                hol = int(r["hol_mod12"])
            elif r.get("holonomy_z12"):
                hol = int(r["holonomy_z12"])
            else:
                hol = None
            d[tri] = hol
    return d


def test_recomputed_triads_match_recorded(tmp_path: Path):
    recorded = load_recorded(
        ROOT
        / (
            "bundles/phase_aware_v3/W33_N12_58_phase_aware_loop_v3/w33_four_center_triads_with_ray_holonomy.csv"
        )
    )
    w33_csv = ROOT / "data/_workbench/02_geometry/W33_line_phase_map.csv"
    rays_csv = (
        ROOT
        / "data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
    )
    if not w33_csv.exists() or not rays_csv.exists():
        pytest.skip("raw phase-aware recomputation inputs are optional and absent")

    outdir = tmp_path / "triad_recompute"
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(ROOT / "bundles/phase_aware_v1/scripts_recompute_w33_ray_holonomy.py"),
        "--w33_csv",
        str(w33_csv),
        "--rays_csv",
        str(rays_csv),
        "--outdir",
        str(outdir),
    ]
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert run.returncode == 0, run.stderr

    recomputed = load_recorded(outdir / "w33_four_center_triads_with_ray_holonomy.csv")
    # ensure counts match
    assert len(recorded) == len(recomputed)
    # ensure exact match of triad -> hol value
    assert recorded == recomputed
