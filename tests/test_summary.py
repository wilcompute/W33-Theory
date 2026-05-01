import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_JSON = ROOT / "archive" / "json"


def _first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError(", ".join(str(path) for path in paths))


def _summary_results_path() -> Path:
    return _first_existing(
        ROOT / "SUMMARY_RESULTS.json", ARCHIVE_JSON / "SUMMARY_RESULTS.json"
    )


def _numeric_comparisons_path() -> Path:
    return _first_existing(
        ROOT / "NUMERIC_COMPARISONS.json", ARCHIVE_JSON / "NUMERIC_COMPARISONS.json"
    )


def _part_json_path(fname: str) -> Path | None:
    for path in (ROOT / fname, ARCHIVE_JSON / fname):
        if path.exists():
            return path
    return None


def test_summary_exists():
    d = json.loads(_summary_results_path().read_text(encoding="utf-8"))
    assert "total_part_json_files" in d


def test_desi_present():
    d = json.loads(_summary_results_path().read_text(encoding="utf-8"))
    summaries = d.get("summaries", {})
    # find any part with desi_dark_energy in key_results
    found = False
    for fname, meta in summaries.items():
        if isinstance(meta, dict) and isinstance(meta.get("key_results"), dict):
            pdata = meta
        else:
            partf = _part_json_path(fname)
            if partf is None:
                continue
            pdata = json.loads(partf.read_text(encoding="utf-8"))
        kr = pdata.get("key_results") or {}
        if isinstance(kr, dict) and "desi_dark_energy" in kr:
            found = True
            dd = kr["desi_dark_energy"]
            assert "w0_measured" in dd and "w0_w33_predicted" in dd
            break
    assert found


def test_summary_and_numeric_comparisons():
    data = json.loads(_summary_results_path().read_text(encoding="utf-8"))
    assert "total_part_json_files" in data and data["total_part_json_files"] >= 1
    assert isinstance(data.get("summaries", {}), dict)

    ndata = json.loads(_numeric_comparisons_path().read_text(encoding="utf-8"))
    assert isinstance(ndata, list)
    if ndata:
        entry = ndata[0]
        for key in ("file", "name", "measured", "predicted", "diff"):
            assert key in entry
        assert isinstance(entry["measured"], (int, float))
        assert isinstance(entry["predicted"], (int, float))
        assert isinstance(entry["diff"], (int, float))
