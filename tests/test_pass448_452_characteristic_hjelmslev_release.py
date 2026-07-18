from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass448_z9_characteristic_smith as p448
import w33_pass449_q5_cubic_section_taxonomy as p449
import w33_pass450_formal_fourier_audit as p450
import w33_pass451_device_ready_blind_packet as p451
import w33_pass452_length3_hjelmslev_filtration as p452

def test_pass448_exact_z9_smith():
    p=p448.build_payload();assert p['status']=='PASS';assert p['z9_3_primary']['critical_group_component']['6561']==7

def test_pass449_five_cubic_classes():
    p=p449.build_payload();assert p['status']=='PASS';assert len(p['classes'])==5;assert p['census']['zero_or_triple_root']==25

def test_pass450_formal_audit():
    p=p450.build_payload();assert p['status']=='PASS';assert p['checks']['no_sorry_token'];assert p['checks']['no_axiom_declaration']

def test_pass451_blind_packet():
    p=p451.build_payload();assert p['status']=='PASS';assert p['verification']['correct']==96;assert p['verification']['abstained']==0

def test_pass452_length3_hjelmslev():
    p=p452.build_payload();assert p['status']=='PASS';assert p['gram_spectrum']=={'972':1,'243':8,'81':72,'27':648}
