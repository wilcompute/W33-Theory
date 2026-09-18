#!/usr/bin/env python3
"""No-go for identifying the W33 outer C2 with the Z6-II even-order C2.

Heterotic side:
  P = <theta | theta^6=1> = C6 = C3 x C2.
  C3=<theta^2>, C2=<theta^3>.  Because P is abelian,
      theta^3 theta^2 theta^-3 = theta^2.
  Thus the order-two factor acts trivially by conjugation on C3.
  The order-two Wilson line is an Abelian gauge-lattice shift/character and
  likewise does not turn the cyclic point group into a semidirect product.

W33 side:
  H=3^(1+12) has center <z>=C3 and the certified multiplier-minus-one outer
  involution s satisfies
      s z s^-1 = z^-1.
  Hence <z,s> = C3:C2 = S3.

Since the conjugation actions C2 -> Aut(C3)=C2 are respectively trivial and
nontrivial, there is no extension-equivariant isomorphism identifying these
two C2 operations.

An actual heterotic counterpart would require a non-Abelian space-group/flavor
extension containing a reflection that inverts an order-three generator
(e.g. an S3/dihedral action), not the present cyclic Z6-II point group.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_z6ii_c2_extension_no_go.json'

def mul6(a,b):return (a+b)%6
def inv6(a):return (-a)%6
def conj6(a,b):return mul6(mul6(a,b),inv6(a))
def main(write=True):
    theta2=2;theta3=3
    assert conj6(theta3,theta2)==theta2
    assert (-theta2)%6==4 and theta2!=4
    out={'schema':'w33.z6ii_c2_extension_no_go.v1','status':'PASS_NO_GO',
      'heterotic':{
        'point_group':'C6=<theta> isomorphic to C3 x C2',
        'C3_generator':'theta^2',
        'C2_generator':'theta^3',
        'conjugation':'theta^3 theta^2 theta^-3 = theta^2',
        'action_on_C3':'trivial',
        'Wilson_line_note':'order-two Wilson line is an Abelian gauge-lattice shift; it does not supply inversion conjugation of the C3 point-group generator'},
      'W33':{
        'C3_generator':'Heisenberg center z',
        'C2_generator':'multiplier-minus-one outer involution s',
        'conjugation':'s z s^-1 = z^-1',
        'action_on_C3':'nontrivial inversion',
        'generated_group':'C3:C2 = S3'},
      'obstruction':'The two homomorphisms C2 -> Aut(C3) are inequivalent (trivial versus the unique nontrivial automorphism). Therefore no extension-equivariant identification exists.',
      'what_would_be_needed':'A non-Abelian heterotic extension with an order-two reflection inverting an order-three element, such as an S3/dihedral space-group or flavor action.',
      'consequence':'The earlier cross-repo parallel should be stated only as both having order-two ingredients. The current Z6-II C2 is not the W33 outer inversion.',
      'checks':{'C6_conjugation_trivial':True,'C3_inverse_distinct':True,'W33_parent_inversion_certified_elsewhere':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
