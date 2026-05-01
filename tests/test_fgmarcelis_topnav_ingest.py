import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _pg32_lines_artifact(tmp_path):
    p = ROOT / "artifacts" / "pg32_lines_from_remaining15.json"
    if p.exists():
        return p

    import contextlib
    import io

    import tools.verify_pg32_remaining15 as verify_pg32

    verify_pg32.ROOT = tmp_path
    with contextlib.redirect_stdout(io.StringIO()):
        verify_pg32.main()
    return tmp_path / "artifacts" / "pg32_lines_from_remaining15.json"


def test_pg32_artifact_exists_and_valid(tmp_path):
    p = _pg32_lines_artifact(tmp_path)
    data = json.loads(p.read_text(encoding="utf-8"))
    summary = data.get("summary", {})
    assert summary.get("n_lines") == 35
    assert summary.get("line_size") == 3
    # each listed line must have exactly 3 point indices
    for L in data.get("lines", []):
        pts = L.get("points", [])
        assert len(pts) == 3


def test_ckm_27_lines_summary():
    p = next(
        (
            path
            for path in [
                ROOT / "CKM_27_LINES.json",
                ROOT / "archive" / "json" / "CKM_27_LINES.json",
            ]
            if path.exists()
        ),
        None,
    )
    assert p is not None and p.exists(), "CKM 27-lines summary missing"
    d = json.loads(p.read_text(encoding="utf-8"))
    isec = d.get("intersection_structure", {})
    assert isec.get("lines") == 27
    # repo summary uses 11 intersections per line and 156 total (Schläfli meet counts)
    assert isec.get("intersections_per_line") == 11
    assert isec.get("total_intersections") == 156


def test_mog_map_builds():
    # THE_EXACT_MAP provides build_mog_map()
    import importlib.util

    path = ROOT / "exploration" / "THE_EXACT_MAP.py"
    spec = importlib.util.spec_from_file_location(
        "THE_EXACT_MAP",
        path,
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mog = mod.build_mog_map()
    assert isinstance(mog, dict)
    assert len(mog) == 12
