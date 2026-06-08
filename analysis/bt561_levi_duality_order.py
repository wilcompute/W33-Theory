#!/usr/bin/env python3
import json
from pathlib import Path
q=3
psp43=25920
we6=51840
# Classical fact: W(3,q) is self-dual exactly for even q; q=3 is odd.
self_dual=(q%2==0)
full=psp43 if not self_dual else 2*psp43
r={
 'bt':561,
 'title':'Levi duality order',
 'q':q,
 'self_dual':self_dual,
 'group':'PSp(4,3)',
 'full_flag_frame_automorphism_order':full,
 'we6_relation':'2*25920=51840',
 'result':'no point-line duality for W(3,3); full incidence/flag-frame group is 25920',
 'all_identities_hold': (not self_dual and full==psp43 and 2*full==we6)
}
Path('data/PART_BT561_LEVI_DUALITY_ORDER_results.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print(json.dumps(r,indent=2))
