#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
a=json.loads((R/'data/PART_W33_PASS5014_40_TRITANGENT_COVERS_ARE_W33_POINTS.json').read_text())
b=json.loads((R/'data/PART_W33_PASS5015_160_COVERS_W33_INCIDENCES.json').read_text())
c=json.loads((R/'data/PART_BT545_W33_LEVI_MINIMAL_LOGICAL_CYCLE_results.json').read_text())
assert a['nine_tritangent_exact_covers']==200 and a['line_cover_incidences']==320
assert a['multiplicity_census']=={'one_line':160,'four_lines':40}
assert b['covers']==160 and b['incident_point_line_pairs']==160 and b['bijection']
assert c['levi_graph']['vertices']==80 and c['levi_graph']['flag_edges']==160
assert c['levi_graph']['cycle_rank_beta1']==81
assert c['minimal_logical_interpretation']['simple_8_cycles']==1620
assert 320-240+1==81
print('PASS Pass5024-5027 regression')
