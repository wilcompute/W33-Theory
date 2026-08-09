from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 ROOT/'analysis/w33_pass4490_fixed_point_nonsplitting_obstruction.py',
 ROOT/'analysis/w33_pass4491_fixed_line_extension_cocycle.py',
 ROOT/'analysis/w33_pass4492_cocycle_support_route_sentinel_extension.py',
]
CERTS=[
 ROOT/'data/PART_W33_PASS4490_FIXED_POINT_NONSPLITTING_OBSTRUCTION.json',
 ROOT/'data/PART_W33_PASS4491_FIXED_LINE_EXTENSION_COCYCLE.json',
 ROOT/'data/PART_W33_PASS4492_COCYCLE_SUPPORT_ROUTE_SENTINEL_EXTENSION.json',
]

def test_witnesses_regenerate_frozen_certificates():
    before=[json.loads(p.read_text()) for p in CERTS]
    for s in SCRIPTS:
        proc=subprocess.run([sys.executable,str(s)],cwd=ROOT,text=True,capture_output=True)
        assert proc.returncode==0,proc.stdout+'\n'+proc.stderr
    after=[json.loads(p.read_text()) for p in CERTS]
    assert after==before

def test_4490_fixed_point_obstruction():
    d=json.loads(CERTS[0].read_text())
    assert d['checks']=={'passed':6,'total':6}
    assert d['fixed_dimensions']=={'E=M/J':0,'K/J':0,'M':1,'V=H10':1}
    assert 'fixed H10 class' in d['obstruction']
    assert 'rank(A)=389' in d['relation_to_4488']

def test_4491_cocycle_support_23():
    d=json.loads(CERTS[1].read_text())
    assert d['checks']=={'passed':10,'total':10}
    assert d['support']['dimension']==23
    assert d['support']['module']=='(K intersect R^perp)/J'
    assert d['support']['profile']=='8 | 1 | 14'
    assert d['gauge_tests']['I/J']['possible'] is False
    assert d['gauge_tests']['KcapRperp/J']['possible'] is True

def test_4492_support_is_route_hull_by_sentinel_extension():
    d=json.loads(CERTS[2].read_text())
    assert d['checks']=={'passed':8,'total':8}
    assert d['quotient_exact_sequence']=='0 -> U/J (8) -> W/J (23) -> C (15) -> 0'
    assert d['support_profile']=='8 | (1 | 14)'
    assert d['owners']['U/J']=='Pass 176'
    assert d['owners']['sentinel_C']=='Pass 201'

def test_manuscripts_and_public_registry_include_fixed_point_packet():
    needle=r'\input{analysis/PASS4490_4492_fixed_point_cocycle_insert}%'
    for name in ['w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex']:
        assert (ROOT/name).read_text().count(needle)==1
    cfg=json.loads((ROOT/'data/w33_public_frontier_extension_pass4461_4464.json').read_text())
    assert 'pass4490-4492-fixed-point-cocycle' in [x['token'] for x in cfg['public_sections']]
    page=(ROOT/'docs/apartment-extension-cocycle.html').read_text()
    assert 'E^PSp = 0' in page
    assert '0 → U/J (8) → (K∩R⊥)/J (23) → C (15) → 0' in page
