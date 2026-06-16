from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSERT = ROOT / 'analysis' / 'BT1207_photonic_holonet_pocket_shell_bus_insert.tex'


def test_bt1207_holonet_pocket_shell_bus_insert():
    text = INSERT.read_text(encoding='utf-8')
    assert r'\label{thm:nonabelian-pocket-shell-bus}' in text
    assert '2160 = 54\\cdot 40' in text
    assert 'SRG}(40,12,2,4)' in text
    assert '720\\cdot3' in text
