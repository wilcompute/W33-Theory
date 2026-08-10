from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load():
 p=ROOT/'analysis/bt3320_3329_global_cover_quantum_hypercube.py'
 s=importlib.util.spec_from_file_location('bt',p);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m

def test_regenerate_exact_packet(tmp_path):
 m=load();d=m.certificate()
 assert d['status'].startswith('PASS_EXACT_EIGHT_FRONT')
 c=d['pass3320_3321_global_cover_reconciliation']
 assert c['global_exact_census']['covers']==3547800
 assert c['closed_hamming_component']['covers']==1574640
 assert c['exterior_complement']['covers']==1973160
 assert c['exterior_complement']['orbits']==192
 assert c['exterior_complement']['stabilizer_histogram']=={'2':120,'4':57,'8':15}
 assert d['pass3322_rational_dual_orbit_compression']['orbit_compressed_rational_coordinates']==98191335
 assert d['pass3323_decoder_contract']['cases']==8192
 assert d['pass3324_unknown_refinement']['depth4_grandchildren']==100
 assert d['pass3327_tau_fourier']['tau_invariant_multiplicities']==[1,6,22,44,42,20]
 h=d['pass3328_3329_hypercube']['q15_host']
 assert h['codewords']==243 and h['binary_length']==15 and h['distance_histogram']['2']==1215
 assert d['live_chromatic_boundary']=='10 <= chi(H) <= 11'

def test_frozen_result_matches_regeneration():
 m=load();d=m.certificate();f=json.loads((ROOT/'data/PART_BT3320_BT3329_GLOBAL_COVER_QUANTUM_HYPERCUBE_results.json').read_text(encoding="utf-8"))
 assert d==f
