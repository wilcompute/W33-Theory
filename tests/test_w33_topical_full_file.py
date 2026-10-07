"""Keep corpus retrieval independent of a result's position in a long file."""
import importlib.util
from pathlib import Path


def test_topical_scan_reads_results_beyond_old_limit(tmp_path, monkeypatch):
    path = Path(__file__).resolve().parents[1] / 'scripts/build_topical_aliases.py'
    spec = importlib.util.spec_from_file_location('topical_scan_regression', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    folder = tmp_path / 'docs'
    folder.mkdir()
    (folder / 'index.html').write_text(' ' * 400_001 + '\nSp(4,3) and [[40,12,4]]\n')
    monkeypatch.setattr(module, 'ROOT', str(tmp_path))
    monkeypatch.setattr(module, 'DIRS', ['docs'])
    index, count = module.scan()
    assert count == 1
    assert index['group:Sp(4,3)'] == {'docs/index.html'}
    assert index['code:[[40,12,4]]'] == {'docs/index.html'}
