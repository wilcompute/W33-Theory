from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 ROOT/'analysis/w33_pass4485_apartment_core_self_gluing.py',
 ROOT/'analysis/w33_pass4486_repeated_core_form_resurrection.py',
 ROOT/'analysis/w33_pass4487_parallel_pauli_core_coordinate_weld.py',
 ROOT/'analysis/w33_pass4488_apartment_extension_nonsplitting.py',
]
CERTS=[
 ROOT/'data/PART_W33_PASS4485_APARTMENT_CORE_SELF_GLUING.json',
 ROOT/'data/PART_W33_PASS4486_REPEATED_CORE_FORM_RESURRECTION.json',
 ROOT/'data/PART_W33_PASS4487_PARALLEL_PAULI_CORE_COORDINATE_WELD.json',
 ROOT/'data/PART_W33_PASS4488_APARTMENT_EXTENSION_NONSPLITTING.json',
]

def test_witnesses_regenerate_frozen_certificates():
    before=[json.loads(p.read_text(encoding="utf-8")) for p in CERTS]
    for s in SCRIPTS:
        p=subprocess.run([sys.executable,str(s)],cwd=ROOT,text=True,capture_output=True)
        assert p.returncode==0,p.stdout+'\n'+p.stderr
    after=[json.loads(p.read_text(encoding="utf-8")) for p in CERTS]
    assert after==before

def test_4485_literal_repeated_core():
    d=json.loads(CERTS[0].read_text(encoding="utf-8")); assert d['pass']==4485
    assert d['checks']=={'passed':15,'total':15}
    assert d['core']['literal_space']=='U/J' and d['core']['dimension']==8
    assert d['diagram']['repeated_core']=='U/J (8) is both radical submodule and protected middle factor'

def test_4486_forms_are_not_conflated():
    d=json.loads(CERTS[1].read_text(encoding="utf-8")); assert d['pass']==4486
    assert d['checks']=={'passed':11,'total':11}
    assert d['radical_occurrence']['polar_rank']==0
    assert d['protected_occurrence']['polar_rank']==8
    assert (d['protected_occurrence']['singular_nonzero'],d['protected_occurrence']['anisotropic'])==(135,120)
    assert 'Same module does not mean same form' in d['boundary']

def test_4487_parallel_core_is_literal_coordinate_match():
    d=json.loads(CERTS[2].read_text(encoding="utf-8")); assert d['pass']==4487
    assert d['checks']=={'passed':9,'total':9}
    assert d['core']['literal_space']=='U/J'
    assert 'parallel F8 = lift-defined protected F8' in d['identities']
    assert 'parallel q8 = wt(Nb)/2 on all 256 classes' in d['identities']

def test_4488_extension_is_nonsplit():
    d=json.loads(CERTS[3].read_text(encoding="utf-8")); assert d['pass']==4488
    assert d['checks']=={'passed':16,'total':16}
    assert d['splits_PSp_equivariantly'] is False
    assert d['section_system']=={'equations':1660,'rank_augmented':390,'rank_coefficient':389,'unknowns':390}
    assert d['Hom_PSp_H10_to_Cap']['dimension']==1
    assert d['Hom_PSp_H10_to_Cap']['unique_nonzero_rank']==9
    assert d['Hom_PSp_H10_to_Cap']['projection_to_H10']=='zero'

def test_three_manuscripts_and_public_sources_include_self_gluing_once():
    needle=r'\input{analysis/PASS4485_4488_apartment_core_self_gluing_insert}%'
    for name in ['w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex']:
        assert (ROOT/name).read_text(encoding="utf-8").count(needle)==1
    cfg=json.loads((ROOT/'data/w33_public_frontier_extension_pass4461_4464.json').read_text(encoding="utf-8"))
    tokens=[x['token'] for x in cfg['public_sections']]
    assert 'pass4472-4479-apartment-module-thermo-ihara-pauli' in tokens
    assert 'pass4485-4488-apartment-core-self-gluing' in tokens
    page=(ROOT/'docs/apartment-core-self-gluing.html').read_text(encoding="utf-8")
    assert 'rank(A)=389' in page and 'rank([A|b])=390' in page
