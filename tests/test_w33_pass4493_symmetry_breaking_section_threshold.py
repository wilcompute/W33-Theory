from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'analysis/w33_pass4493_symmetry_breaking_section_threshold.py'
CERT=ROOT/'data/PART_W33_PASS4493_SYMMETRY_BREAKING_SECTION_THRESHOLD.json'


def test_pass4493_corrected_exact_subgroup_census():
    proc=subprocess.run([sys.executable,str(SCRIPT)],cwd=ROOT,text=True,capture_output=True)
    assert proc.returncode==0,proc.stdout+'\n'+proc.stderr
    d=json.loads(CERT.read_text())
    assert d['pass']==4493 and d['status']=='CORRECTED_BY_PASSES_4503_4507'
    full=d['tested_subgroups']['full_PSp']
    line=d['tested_subgroups']['one_line_stabilizer']
    point=d['tested_subgroups']['one_point_stabilizer']
    flag=d['tested_subgroups']['incident_flag_stabilizer']
    apartment=d['tested_subgroups']['apartment_setwise_stabilizer']
    assert (full['section_system']['rank_coefficient'],full['section_system']['rank_augmented'])==(389,390)
    assert (line['order'],line['section_system']['rank_coefficient'],line['section_system']['rank_augmented'])==(648,386,387)
    assert (point['order'],point['section_system']['rank_coefficient'],point['section_system']['rank_augmented'])==(648,387,388)
    assert line['section_system']['consistent'] is False and point['section_system']['consistent'] is False
    assert (flag['order'],flag['section_system']['rank_coefficient'],flag['section_system']['rank_augmented'],flag['section_system']['affine_dimension'])==(162,384,384,6)
    assert (apartment['order'],apartment['section_system']['rank_coefficient'],apartment['section_system']['rank_augmented'])==(16,357,358)
    assert '370/370' in d['erratum']['withdrawn']


def test_pass4493_public_and_manuscript_sources_are_corrected():
    insert=(ROOT/'analysis/PASS4493_symmetry_breaking_section_insert.tex').read_text()
    page=(ROOT/'docs/apartment-symmetry-breaking-section.html').read_text()
    card=(ROOT/'analysis/PASS4493_symmetry_breaking_section_index_insert.html').read_text()
    assert '386/387' in insert and '384/384' in insert
    assert 'false positive' in page.lower() and '386 / 387' in page and '384' in page
    assert 'withdrawn' in card.lower() and '386/387' in card
    assert 'rank(A)=rank([A|b])=370' not in page
    cfg=json.loads((ROOT/'data/w33_public_frontier_extension_pass4461_4464.json').read_text())
    assert 'pass4493-symmetry-breaking-section-threshold' in [x['token'] for x in cfg['public_sections']]
