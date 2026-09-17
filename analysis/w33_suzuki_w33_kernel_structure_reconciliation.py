#!/usr/bin/env python3
"""Reconcile the new W33 stabilizer kernels with the older Suzuki subgroup shape.

The refactorization compiler records the projective Suzuki W33 stabilizer as
    2_-^(1+6) : U4(2),
of order 3317760.  The exhaustive stabilizer quotient certificate proves that
the induced 27-decomposition action is PSp(4,3), order 25920, while the faithful
2.Suz lift has linear image Sp(4,3), order 51840.

Using the established alias U4(2) ~= PSp(4,3), the order-128 projective kernel
is therefore exactly the normal extraspecial 2_-^(1+6).  In the faithful
12-dimensional F3 representation the central involution of 2.Suz acts as
-I_12 (the only nontrivial scalar involution).  It restricts to -I_4, so it is
not in the linear kernel, but it vanishes after projectivization.  Consequently

    K_linear ~= 2_-^(1+6),                         order 128,
    K_projective ~= 2_-^(1+6) x C2,               order 256.

This is a structural reconciliation of two independently certified layers; it
adds no physical interpretation.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_suzuki_w33_kernel_structure_reconciliation.json'


def main(write=True):
    old=json.loads((ROOT/'data'/'w33_suzuki_refactorization_compiler.json').read_text())
    new=json.loads((ROOT/'data'/'w33_suzuki_w33_stabilizer_projective_quotient.json').read_text())
    assert old['status']=='PASS' and new['status']=='PASS'
    proj_old=old['stabilizers']['W33_stabilizer_order']
    assert proj_old==3317760
    assert old['stabilizers']['W33_stabilizer_shape']=='2_-^(1+6):U4(2)'
    psp=new['projective_27_action']['order']; sp=new['linear_restriction']['order']
    assert psp==25920 and sp==51840
    e=proj_old//psp
    assert e==128
    lift=new['block_stabilizer']['order']; assert lift==2*proj_old==6635520
    klin=new['linear_restriction']['kernel_order']; kproj=new['projective_27_action']['kernel_order']
    assert klin==128 and kproj==256
    out={
      'schema':'w33.suzuki_w33_kernel_structure_reconciliation.v1','status':'PASS',
      'headline':'The order-128 kernel of the Suzuki W33 local quotient is the normal extraspecial group 2_-^(1+6) from the previously certified projective stabilizer shape 2_-^(1+6):U4(2), with U4(2) ~= PSp(4,3). In the faithful 2.Suz symplectic lift the central involution acts as -I12, lies outside the linear kernel but inside the projective kernel, so K_linear ~= 2_-^(1+6) and K_projective ~= 2_-^(1+6) x C2.',
      'projective_Suzuki_stabilizer':{'order':proj_old,'shape':'2_-^(1+6):U4(2)'},
      'quotient_alias':{'U4(2)_order':psp,'PSp4_3_order':psp,'identified_in_repo':True},
      'linear_kernel':{'order':klin,'shape':'2_-^(1+6)'},
      'projective_kernel_in_2Suz':{'order':kproj,'shape':'2_-^(1+6) x C2','extra_C2':'central involution -I12 of the faithful 2.Suz lift'},
      'order_checks':{'extraspecial_order':e,'2Suz_stabilizer_is_double_projective':lift==2*proj_old,
                      'linear_kernel_128':klin==e,'projective_kernel_256':kproj==2*e},
      'boundary':'This identifies exact finite subgroup structure by reconciling two certified repository computations. It does not assign a physical meaning to the extraspecial kernel or central involution.'
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); return out

if __name__=='__main__': main(True)
