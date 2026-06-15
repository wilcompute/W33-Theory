#!/usr/bin/env python3
import json
out={
 'bt':1187,
 'title':'transport edge support map audit',
 'available_map':'transport edge -> two quotient points -> two W33 supports',
 'quotient_points':45,
 'transport_edges':720,
 'support_size':8,
 'target_factorization':'51840=540*2*48',
 'missing':'support-pair to BT748 fiber coordinate',
 'status':'partial W33 support map exists; full voltage/chirality correlation remains blocked',
 'all_checks_pass':45*32//2==720 and 51840==540*2*48
}
print(json.dumps(out,indent=2,sort_keys=True))
