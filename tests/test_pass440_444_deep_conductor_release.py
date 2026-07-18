from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass440_galois_ring_conductor_tower as p440
import w33_pass441_formal_kernel_audit as p441
import w33_pass442_blind_photonic_preregistration as p442
import w33_pass443_section_sensitive_smith_classification as p443
import w33_pass444_hjelmslev_conductor_geometry as p444

def test_pass440_conductor_tower():
    p=p440.build_payload();assert p['status']=='PASS';assert len(p['instances'][2]['conductor_strata'])==3

def test_pass441_no_sorry_formal_kernel():
    p=p441.build_payload();assert p['status']=='PASS';assert p['checks']['no_sorry_token'];assert p['checks']['no_axiom_declaration']

def test_pass442_blind_holdout():
    p=p442.build_payload();s=p['holdout']['summary'];assert p['status']=='PASS';assert s['correct']==s['decided']==192;assert s['abstained']==0

def test_pass443_two_orbits_and_two_smith_groups():
    p=p443.build_payload();assert p['status']=='PASS';assert p['checks']['curl_is_complete_orbit_invariant'];assert p['classes']['flat']['critical_group_factors']!=p['classes']['curved']['critical_group_factors']

def test_pass444_hjelmslev_gram_bridge():
    p=p444.build_payload();assert p['status']=='PASS';assert all(x['status']=='PASS' for x in p['explicit_instances'])
