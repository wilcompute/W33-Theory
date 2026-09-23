#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'data/w33_e6_cubic_hybrid81_transport.json').read_text())
r=s['root_tensor']; j=s['jacobian']; c=s['checks']
assert r['signed_E6_triads']==45 and r['nonzero_unordered_channels']==810
assert r['firewall_bad_channels']==162 and r['input_degree_each']==20 and r['output_multiplicity_each']==10
assert j['collective_image_span_dimension']==81 and j['collectively_reaches_all_54_retyped_slots']
assert j['single_root_background_rank54'] is False
assert 'does not prove' in s['boundary']
assert all(c[k] for k in ('canonical_45_triads_loaded','e6id_to_current_H27_is_bijective','canonical_triads_equal_current_45_H27_lines','collective_jacobian_span81','hybrid_change_of_basis_invertible'))
out={'schema':'w33.e6.54-slot.audit.v1','status':'PASS_COLLECTIVE_REACHABILITY_ONLY','collective_span':81,'retyped_slots':54,'single_root_rank54':False}
(ROOT/'data/w33_actual_e6_54_slot_audit.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True))
