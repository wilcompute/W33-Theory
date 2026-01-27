import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_summary_exists():
    f = ROOT / 'SUMMARY_RESULTS.json'
    assert f.exists()
    d = json.load(open(f))
    assert 'total_part_json_files' in d


def test_desi_present():
    f = ROOT / 'SUMMARY_RESULTS.json'
    d = json.load(open(f))
    summaries = d.get('summaries', {})
    # find any part with desi_dark_energy in key_results
    found = False
    for fname, meta in summaries.items():
        # open original file
        partf = ROOT / fname
        if not partf.exists():
            continue
        pdata = json.load(open(partf))
        kr = pdata.get('key_results') or {}
        if isinstance(kr, dict) and 'desi_dark_energy' in kr:
            found = True
            dd = kr['desi_dark_energy']
            assert 'w0_measured' in dd and 'w0_w33_predicted' in dd
            break
    assert found


def test_summary_and_numeric_comparisons():
    sr = ROOT / 'SUMMARY_RESULTS.json'
    assert sr.exists(), "SUMMARY_RESULTS.json is missing"
    data = json.load(open(sr))
    assert 'total_part_json_files' in data and data['total_part_json_files'] >= 1
    assert isinstance(data.get('summaries', {}), dict)

    nc = ROOT / 'NUMERIC_COMPARISONS.json'
    assert nc.exists(), "NUMERIC_COMPARISONS.json is missing"
    ndata = json.load(open(nc))
    assert isinstance(ndata, list)
    if ndata:
        entry = ndata[0]
        for key in ('file', 'name', 'measured', 'predicted', 'diff'):
            assert key in entry
        assert isinstance(entry['measured'], (int, float))
        assert isinstance(entry['predicted'], (int, float))
        assert isinstance(entry['diff'], (int, float))
