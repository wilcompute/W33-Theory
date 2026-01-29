import json
from pathlib import Path

def test_tomotope_followup_exists():
    repo = Path(__file__).resolve().parents[1]
    f = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'tomotope_tda_followup_modes8_structured.json'
    assert f.exists(), f"Missing {f}"
    data = json.load(open(f))
    assert 'js' in data and 0.0 <= data['js'] <= 1.0
    assert 'h1_count' in data and isinstance(data['h1_count'], int)
