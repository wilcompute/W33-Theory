from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'analysis/w33_pass4493_symmetry_breaking_section_threshold.py'
CERT=ROOT/'data/PART_W33_PASS4493_SYMMETRY_BREAKING_SECTION_THRESHOLD.json'


def test_pass4493_exact_subgroup_threshold():
    proc=subprocess.run([sys.executable,str(SCRIPT)],cwd=ROOT,text=True,capture_output=True)
    assert proc.returncode==0,proc.stdout+'\n'+proc.stderr
    d=json.loads(CERT.read_text())
    assert d['pass']==4493
    assert d['checks']=={'passed':12,'total':12}
    full=d['tested_subgroups']['full_PSp']
    line=d['tested_subgroups']['one_line_stabilizer']
    point=d['tested_subgroups']['one_point_stabilizer']
    flag=d['tested_subgroups']['incident_flag_stabilizer']
    apartment=d['tested_subgroups']['apartment_setwise_stabilizer']
    assert full['order']==25920 and full['section_system']['consistent'] is False
    assert (full['section_system']['rank_coefficient'],full['section_system']['rank_augmented'])==(389,390)
    assert line['order']==648 and line['index_in_PSp']==40
    assert point['order']==648 and point['index_in_PSp']==40
    assert (line['section_system']['rank_coefficient'],line['section_system']['rank_augmented'],line['section_system']['affine_dimension'])==(370,370,20)
    assert (point['section_system']['rank_coefficient'],point['section_system']['rank_augmented'],point['section_system']['affine_dimension'])==(370,370,20)
    assert flag['order']==162 and flag['section_system']['affine_dimension']==52
    assert apartment['order']==16 and apartment['section_system']['affine_dimension']==82
    assert 'not a classification of every subgroup' in d['boundary']


def test_pass4493_public_and_manuscript_sources_exist():
    assert (ROOT/'analysis/PASS4493_symmetry_breaking_section_insert.tex').exists()
    page=(ROOT/'docs/apartment-symmetry-breaking-section.html').read_text()
    assert 'rank(A)=rank([A|b])=370' in page
    assert 'fix one point/line' in page.lower()
    cfg=json.loads((ROOT/'data/w33_public_frontier_extension_pass4461_4464.json').read_text())
    assert 'pass4493-symmetry-breaking-section-threshold' in [x['token'] for x in cfg['public_sections']]
