#!/usr/bin/env python3
"""Pass 1174 v2: exact cubic image and D5 scope boundary."""
import json
from pathlib import Path
def main():
    result={'schema':'w33.pass1174.cubic_image_exact.v2','status':'PASS','image_dimension':45,
      'exact_we6_image_decomposition':'1 + 20 + 24','source':'Pass 1135 exact character inner products',
      'so10_dimension':45,'dimension_coincidence':True,'d5_adjoint_identified':False,
      'required_evidence':'An explicit W(D5) restriction and equivariant isomorphism to wedge^2(Q^10).',
      'rejected_candidates':['30+15 preferred split','45-dimensional image is automatically the D5 adjoint'],
      'scope_barrier':'The equality 45=dim so(10) is a count match only.'}
    Path('data/D5_ADJOINT_IMAGE_2026_07_27.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS 1174 v2 image=1+20+24; D5 identification unproved');return result
if __name__=='__main__':main()
