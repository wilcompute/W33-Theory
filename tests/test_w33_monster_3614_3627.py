from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_monster_structural_program():
    subprocess.run([sys.executable,str(ROOT/'analysis/w33_monster_structural_program.py')],cwd=ROOT,check=True)
    d=json.loads((ROOT/'data/PART_3614_3627_MONSTER_STRUCTURAL_PROGRAM_results.json').read_text(encoding="utf-8"))
    assert d['verified'] is True
    assert d['w33']['vertices']==40 and d['w33']['degree']==12
    assert d['w33']['eigenvalue_2_projector']['rank']==24
    assert d['w33']['eigenvalue_2_projector']['numerator_scale']==60
    assert d['bonkers_falsifiers']['leech_seed']['status'].startswith('NO_GO')
    assert d['bonkers_falsifiers']['raw_moonshine_moments']['residuals']==[10933957100,105149879960,355102291024]
    assert d['monster_u42']['steinberg_3_local_register']['degree']==81
