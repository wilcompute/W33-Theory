from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass558_q5_triality_partition as p558
import w33_pass559_z9_radial_quadratic_automaton as p559
import w33_pass560_cyclotomic_uniformizer_formal as p560
import w33_pass561_noise_aware_orientation_latch as p561
import w33_pass562_q5_tensor_type_derivation as p562
import w33_pass558_562_release as release

def test_triality_group():
    p=p558.payload();assert p['status']=='PASS';assert p['partition_stabilizer']['order']==60;assert p['partition_stabilizer']['block_action']=='S3';assert p['partition_stabilizer']['block_action_kernel']=='D10'

def test_extended_automaton_cached():
    import pickle
    base=pickle.loads(p559.BASE_CACHE.read_bytes());ext=pickle.loads(p559.EXT_CACHE.read_bytes());p=p559.payload(base+ext)
    assert p['status']=='PASS';assert p['layers'][-1]['sections']==59049;assert p['layers'][-1]['distinct_charpolys']==9266;assert p['minimal_future_automaton']['layers'][4]['minimal_markov_states']==3281

def test_cyclotomic_formal_support():
    p=p560.payload();assert p['status']=='PASS';assert p['checks']['actual_cyclotomic_identity_formalized'];assert p['checks']['no_unproved_placeholders']

def test_noise_selector():
    p=p561.payload();assert p['status']=='PASS';assert p['orientation_profiles']['conservative']['selected_architecture']=='repeated_channel_parity';assert p['orientation_profiles']['nominal']['selected_architecture']=='direct_twelvefold_parity'

def test_tensor_derivation():
    p=p562.payload();assert p['status']=='PASS';assert p['checks']['five_type_census_exact'];assert p['checks']['walsh_translation_theorem_matches_geometry']

def test_release_lock():
    p=release.payload();assert p['status']=='PASS';assert p['owner_check_total']==55;assert all(p['release_checks'].values())
