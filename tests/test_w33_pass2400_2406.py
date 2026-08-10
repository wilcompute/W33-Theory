import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load(n,s):
    d=json.loads((ROOT/f'data/w33_pass{n}_{s}.json').read_text(encoding="utf-8"));assert d['sha256_without_hash_field']==digest(d);return d
def test_six_frontier_certificates():
    a=load(2400,'syndrome_first_external_merge');b=load(2401,'five_orbit_shell_algebra');c=load(2402,'duad_first_coloring_base')
    d=load(2403,'sl3_shell_parabolic_bridge');e=load(2404,'e8_coexact_hom_obstruction');f=load(2405,'tomotope_192_curved_duad_atlas')
    assert a['exact_runs']['16']['cross_shard_collision_edges']==43_428_489
    assert b['ordered_pair_orbitals']['rank']==527 and b['S6_Wedderburn']['center_dimension']==11
    assert c['exact_cover_model']['binary_variables']==4860 and c['bounded_9color_run']['status'].endswith('UNKNOWN')
    assert d['shell_bridge']['shared_finite_packet']=='S4 of order 24'
    assert e['Hom_obstruction']['Hom_PSp_8_to_90_dimension']==0
    assert len(f['max_intersection_profiles'])==3 and all(z['duad_degree']==96 for z in f['max_intersection_profiles'].values())
def test_boundaries_and_hooks():
    assert 'global U6 coefficient' in load(2400,'syndrome_first_external_merge')['boundary']
    assert 'neither proves nor disproves' in load(2402,'duad_first_coloring_base')['boundary']
    assert 'No equivariant bijection' in load(2405,'tomotope_192_curved_duad_atlas')['boundary']
    assert all('BT2406_six_frontiers_insert' in (ROOT/p).read_text(encoding="utf-8") for p in ('w33_paper.tex','photonic_holonet.tex'))
