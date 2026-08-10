import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_frozen_release():
    subprocess.run([sys.executable,str(ROOT/'analysis'/'w33_pass1826_1830_verify_frozen.py')],check=True)
def test_boundaries_are_explicit():
    a=json.loads((ROOT/'data'/'w33_pass1826_1830_five_frontiers.json').read_text(encoding="utf-8"))
    assert 'full 2^45 weight enumerator remains open' in a['boundaries'][0]
    assert 'not every possible nine-cover' in a['boundaries'][1]
