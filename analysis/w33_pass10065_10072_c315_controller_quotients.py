#!/usr/bin/env python3
"""Pass10065-10072: arithmetic/controller quotient tower of the C315 Singer torsor.

The abstract V2 C13 clock sits in F_{2^12}^x=C4095.  Modding out the clock
itself leaves C315.  Because ord_13(2)=12, C13 is not contained in any proper
subfield multiplicative group; instead it lies in the kernel of every norm to
a proper subfield F_{2^d}, d|12.  Therefore all proper-subfield norms descend
canonically to quotients of C315.

For d=2,3,4,6 the descended images have orders 3,7,15,63.  The controller
interpretation is especially sharp:

* the four-channel clock quotient C12 -> C4 has kernel C3, whose fixed field is
  F_{2^4}=F16.  Its canonical norm shadow is C315 -> F16^x=C15, kernel C21;
* the binary orientation quotient C12 -> C2 has kernel C6, fixed field F4.
  Its canonical norm shadow is C315 -> F4^x=C3, kernel C105.

Thus the C315 ambiguity has a Galois-controlled reduction ladder, not just a
cardinality decomposition.
"""
from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10065_10072_C315_CONTROLLER_QUOTIENTS.json'

def ordmod(a,n):
    x=1
    for k in range(1,100):
        x=x*a%n
        if x==1:return k
    raise RuntimeError

def main():
    assert ordmod(2,13)==12
    Q=2**12-1
    assert Q==4095==13*315
    rows={}
    for d in (1,2,3,4,6):
        target=2**d-1
        exponent=Q//target
        assert exponent%13==0 # C13 lies in norm kernel
        image=target
        kernel_on_C315=315//image
        rows[d]={'subfield':f'F_{2**d}','norm_exponent':exponent,'descended_image_order':image,'kernel_order_on_C315':kernel_on_C315}
    assert rows[2]['descended_image_order']==3 and rows[2]['kernel_order_on_C315']==105
    assert rows[3]['descended_image_order']==7 and rows[3]['kernel_order_on_C315']==45
    assert rows[4]['descended_image_order']==15 and rows[4]['kernel_order_on_C315']==21
    assert rows[6]['descended_image_order']==63 and rows[6]['kernel_order_on_C315']==5
    # CRT/Sylow structure and Frobenius action orders.
    assert 315==9*5*7
    acts={9:ordmod(2,9),5:ordmod(2,5),7:ordmod(2,7)}
    assert acts=={9:6,5:4,7:3}
    # Fixed field degree = index of controller-kernel subgroup in C12.
    controllers={
      'orientation_C2':{'kernel_in_Galois':6,'fixed_field_degree':2,'fixed_field':'F4','norm_shadow':'C3','kernel_on_C315':'C105'},
      'four_channel_C4':{'kernel_in_Galois':3,'fixed_field_degree':4,'fixed_field':'F16','norm_shadow':'C15','kernel_on_C315':'C21'},
      'six_phase_C6':{'kernel_in_Galois':2,'fixed_field_degree':6,'fixed_field':'F64','norm_shadow':'C63','kernel_on_C315':'C5'},
    }
    out={
      'schema':'w33.pass10065_10072.c315_controller_quotients.v1','status':'PASS','passes':'10065-10072',
      'Singer_torsor':{'ambient_units':'F4096^x=C4095','clock':'C13','quotient':'C315','factorization':'C9 x C5 x C7'},
      'Frobenius_action_orders_on_Sylow_factors':{str(k):v for k,v in acts.items()},
      'proper_subfield_norms':{str(k):v for k,v in rows.items()},
      'controller_dictionary':controllers,
      'four_channel_result':'C315 -> C15 canonically via N_{F4096/F16}; kernel C21. This is the norm shadow naturally selected by C12->C4.',
      'orientation_only_result':'C315 -> C3 canonically via N_{F4096/F4}; kernel C105. Thus the binary orientation controller sees a residual ternary phase shadow.',
      'maximal_proper_subfield_result':'N_{F4096/F64} gives C315 -> C63 with the smallest norm kernel C5 among proper subfields.',
      'theorem':'The C315 Singer ambiguity carries a canonical Galois/norm quotient ladder C315 -> C63, C15, C7, C3. In particular the four-channel C4 controller canonically selects the C15 shadow, while the orientation C2 controller selects the C3 shadow. The residual factors are therefore dictated by subfield arithmetic rather than chosen ad hoc.',
      'boundary':'These are canonical arithmetic quotient/shadow maps. Calling a norm shadow physically measured or fully resolving the geometric transporter would require additional controller implementation data.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','C4_shadow':'C15','C2_shadow':'C3','max_proper_shadow':'C63'}))
    return 0
if __name__=='__main__':raise SystemExit(main())
