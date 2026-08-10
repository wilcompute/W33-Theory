import json
from pathlib import Path
DATA=Path(__file__).resolve().parents[1]/'data'
NAMES={1939:'u6_supershard',1940:'split_macwilliams',1941:'gaussian_solver_transport',1942:'integral_phase_order',1943:'hodge_eisenstein_carrier_separator'}
def load(n):return json.loads((DATA/f'w33_pass{n}_{NAMES[n]}.json').read_text(encoding="utf-8"))
def test_five_frontiers():
 a,b,c,d,e=[load(n) for n in range(1939,1944)]
 assert a['combined_supershard']['records']==58282126
 assert b['full_transform']['words']==2**195 and b['full_transform']['nonzero_bins']==39081
 assert c['oriented_lift']['odd_subspace_dimension']==135
 assert d['associative_order']['integral_order']=='M3(Z)'
 assert e['energy_invariant']['A24']==10 and e['energy_invariant']['A90']==4
def test_boundaries():
 a,c,e=load(1939),load(1941),load(1943)
 assert 'no global U6 coefficient' in a['boundary']
 assert 'does not fabricate' in c['boundary']
 assert 'does not derive electromagnetism' in e['boundary']
