import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest


def require_edge_rootpair_artifact(repo: Path) -> Path:
    artifact = repo / "artifacts" / "edge_to_rootpair_triple.json"
    if not artifact.exists():
        pytest.skip(
            "edge_to_rootpair_triple.json is an ignored heavy artifact; "
            "run tools/build_edge_to_rootpairs.py to materialize this optional test input"
        )
    return artifact


def test_compute_full_derivations(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    # make zips similar to previous test
    tri_folder = repo / "TOE_E6pair_SRG_triangle_decomp_v01_20260227_bundle"
    tri_zip = tmp_path / "tri.zip"
    with zipfile.ZipFile(tri_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in tri_folder.rglob("*"):
            if p.is_file():
                zf.write(p, p.relative_to(tri_folder))
    edge_zip = tmp_path / "edge.zip"
    with zipfile.ZipFile(edge_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(
            require_edge_rootpair_artifact(repo),
            "TOE_edge_to_oriented_rootpairs_v01_20260227/edge_to_oriented_rootpair_triple.json",
        )
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "compute_full_derivations.py"),
            "--tri_zip",
            str(tri_zip),
            "--edge_zip",
            str(edge_zip),
            "--quick",
        ],
        cwd=repo,
    )
    assert res.returncode == 0
    # check output files
    assert (repo / "full_derivations_report.json").exists()
    assert (repo / "full_derivations_basis.json").exists()
