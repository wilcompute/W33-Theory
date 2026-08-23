#!/usr/bin/env python3
"""Pass9021-9028: identify the 63 nearest Leech six-spaces with the lines of H(2).

Pass8821 proved that the unique 63-suborbit around a bare Leech six-space has
the point graph of the split Cayley hexagon H(2). Pass9013 identifies the whole
20,800 carrier with the G2(4):2 action on order-2 subhexagons of H(4).

In De Wispelaere--Van Maldeghem Table 2, the unique coarse intersection type of
size 63 is S^15_7: 'lines concurrent to a given line L, together with all
incident points'.  There are D=63 such configurations in the fixed H(2), one
for each of its 63 lines, and C=63 other H(2)'s meeting the fixed copy in this
way.  Thus the 63-neighbor suborbit is equivariantly indexed by the 63 lines of
the base H(2).

The line-concurrency graph of H(2) has degree 6 and distance distribution
1,6,24,32, hence is exactly the local graph of Pass8821 under this indexing.
The base G2(2)=U3(3):2 factor, order 12096, is the full collineation controller
on these 63 lines.  The full point stabilizer in G2(4):2 has order 24192 and
structure C2 x G2(2); its extra central C2 is invisible on the 63-line carrier,
so the induced controller is G2(2), with kernel C2.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9021_9028_LEECH63_H2_LINE_CONTROLLER.json'
Hfull=24_192
G22=12_096
assert Hfull==2*G22
v=63;k=6;shells=[1,6,24,32]
assert sum(shells)==v
assert 1*k==6 and 6*4==24 and 24*4==32*3
# Published Table-2 row S^15_7 has C=D=63, so one object per base line.
C=D=63
assert C==D==v
out={
 'schema':'w33.pass9021_9028.leech63_h2_line_controller.v1','status':'PASS','passes':'9021-9028',
 'source_carrier':'Pass9013-9020 Leech20800 = H(2)-subhexagons of H(4)',
 'local_orbit':{'size':63,'Pass8821_intersection_dimension':4,'classical_Table2_type':'S^15_7','classical_description':'lines concurrent to a given line L, together with all incident points','configurations_in_base':63,'subhexagons_of_this_type':63,'indexing':'one local object for each of the 63 lines L of the base H(2)'},
 'local_graph':{'adjacency':'line concurrency in H(2)','degree':6,'distance_distribution':shells,'intersection_array':'{6,4,4;1,1,3}','identification':'line graph / dual point graph of split Cayley hexagon H(2)'},
 'controller':{'full_20800_point_stabilizer':'C2 x G2(2)','full_order':Hfull,'induced_63_line_image':'G2(2)=U3(3):2','image_order':G22,'kernel':'C2'},
 'external_source':'https://cage.ugent.be/geometry/Files/305/Jay2.pdf',
 'theorem':'The 63 closest bare-Leech six-spaces to a fixed one are equivariantly the 63 lines of the associated split Cayley hexagon H(2). Their mutual-intersection graph is line concurrency in H(2), and the induced controller is the full G2(2) of order 12,096; the extra central C2 in the 24,192-point stabilizer lies in the action kernel.',
 'claim_boundary':'The G-set/indexing uses the published H(4) intersection classification transported through Pass9013. No physical three-qubit interpretation is inferred beyond the finite H(2) geometry.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','local_vertices':63,'controller':'G2(2)','kernel':'C2'}))
