from __future__ import annotations
import importlib.util,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'analysis/bt3687_3693_realized_octad_borel_psd_proof_tomography_architecture.py'
FROZEN=ROOT/'data/PART_BT3687_BT3693_REALIZED_OCTAD_BOREL_PSD_PROOF_TOMOGRAPHY_ARCHITECTURE_results.json'

def load():
 spec=importlib.util.spec_from_file_location('p3649',SRC);m=importlib.util.module_from_spec(spec);assert spec.loader;spec.loader.exec_module(m);return m
@pytest.fixture(scope='session')
def packet():return load().build_result()

def test_frozen_semantic_certificate(packet):
 assert json.loads(json.dumps(packet))==json.loads(FROZEN.read_text(encoding="utf-8"))
 assert packet['semantic_sha256']=='3ff49c19511ebcf3c9159c1d69f123ae66dd275498c94f501230710634982828'

def test_realized_octad_deck(packet):
 p=packet['passes']['3687_realized_octad_deck'];assert (p['abstract_patterns'],p['realized_patterns'])==(69,59)
 assert p['exceptional_frontier_ids']==[1,3,4,5,7,8,10,12,13,21]
 assert p['witness_digest']=='1cd53497824bcec7da92bd283d0856f51ad61f90d17e97c0d583efa3cca6ab21'

def test_borel_bridge_collapses(packet):
 p=packet['passes']['3688_exact_Borel_bridge_screen'];assert p['valid_subsets']==55 and p['maximum_weight']==2
 assert p['weight_histogram']=={0:1,1:18,2:36};assert sorted(map(len,p['compatibility_components']))==[6,6,6]

def test_psd_cone_classification(packet):
 p=packet['passes']['3689_observable_PSD_cone'];assert p['cone_isomorphism']=='R_+ x Herm_3^+(C) x R_+'
 assert p['rank_strata_count']==16 and p['Caratheodory_number']==5 and p['algebraic_boundary_degree']==5
 assert p['invariant_form_determinant']=='7/19'

def test_content_addressed_proofs(packet):
 p=packet['passes']['3690_content_addressed_proof_archive'];assert p['instances']==32
 assert p['merkle_root']=='d75cdc80648d7ddf913555f164140bc864087689e4c37e8ba77b0c3f763d9529'
 assert p['maximum_clique_histogram']=={6:1,7:2,8:4,9:4,10:2,11:6,12:6,13:3,16:4}

def test_marked_atlas_and_architecture_firewalls(packet):
 p=packet['passes']['3691_marked_resolvent_atlas'];assert [p['sizes'][str(n)]['W_exclusive_resolvent_signatures'] for n in range(1,6)]==[0,0,1,3,10]
 assert all(p['sizes'][str(n)]['G_exclusive_resolvent_signatures']==0 for n in range(1,6))
 loss=packet['passes']['3692_bonkers_one_photon_scalability_loss_firewall'];assert loss['minimum_orthogonal_modes']==3**81
 assert loss['per_hop_loss_upper_bound']<0.001
 ctl=packet['passes']['3693_bonkers_generic_controllability_specificity_firewall'];assert ctl['dynamical_Lie_algebra_dimension']==1600 and ctl['direct_pair_interference_tomography_settings']==1561
