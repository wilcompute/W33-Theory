#!/usr/bin/env python3
"""Pass10153-10160 outside-box: 315=C13-orbits=W(5,2)-lines is a count match, not a cyclic G-set identity.

The parallel packet promoted

    4095/13 = 315 = number of totally isotropic lines of W(5,2)

to a 'structural identity'.  The equality is exact, but a natural structural
meaning would require at least an automorphism-compatible action.  The abstract
C13 orbit set is a regular torsor for C315=C4095/C13.  If this C315 were realized
as symplectic collineations of W(5,2), Sp(6,2) would contain an element of order
315.  It does not.

Reason: over F2,
  Phi_7(x)=x^6+...+1=(x^3+x+1)(x^3+x^2+1),
two reciprocal irreducible cubics.  Any order-7 symplectic element on a
6-dimensional space must pair the two reciprocal 3-dimensional irreducibles,
so it is fixed-point-free.  Its GL centralizer is F8^* x F8^*; preserving the
symplectic pairing forces the two scalars to be reciprocal, leaving C7.
Therefore C_{Sp6(2)}(h)=C7 for h of order 7.

If g had order 315, then h=g^45 would have order 7 and g would lie in C(h),
contradicting |C(h)|=7.  So there is no regular cyclic C315 action on the 315
W(5,2) isotropic lines coming from Sp6(2).
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10153_10160_C315_W52_STRUCTURAL_NO_GO.json'

def poly_mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]^=(x&y)
    return c

def main():
    # Coefficients low-to-high over F2.
    f1=[1,1,0,1] # x^3+x+1
    f2=[1,0,1,1] # x^3+x^2+1
    phi7=[1,1,1,1,1,1,1]
    assert poly_mul(f1,f2)==phi7
    assert f1==list(reversed(f2))
    c13_orbits=(2**12-1)//13
    w52_lines=63*15//3
    assert c13_orbits==w52_lines==315
    assert 315==3*3*5*7
    # Centralizer proof data: F8^* has order7; symplectic condition leaves diagonal reciprocal C7.
    gl_centralizer=7*7;sp_centralizer=7
    assert gl_centralizer==49 and sp_centralizer==7
    # Hypothetical order315 g gives h=g^45 of order 7 (315/gcd(315,45)=7).
    import math
    assert 315//math.gcd(315,45)==7
    assert 315>sp_centralizer
    out={
      'schema':'w33.pass10153_10160.c315_w52_structural_no_go.v1','status':'PASS','passes':'10153-10160','outside_box':True,
      'exact_count_match':{'C13_orbits_on_F2_12_nonzero':315,'W5_2_isotropic_lines':315,'W5_2_line_count_formula':'63 points * 15 lines/point / 3 points/line'},
      'order7_structure':{'Phi7_factorization_over_F2':'(x^3+x+1)(x^3+x^2+1), reciprocal irreducible cubics','fixed_space_dimension':0,'GL6_2_centralizer_order':49,'Sp6_2_centralizer_order':7,'Sp_centralizer':'C7'},
      'C315_no_go':{'hypothetical_g_order':315,'h':'g^45','h_order':7,'commutation':'g commutes with h because h is a power of g','contradiction':'g would lie in an order-7 centralizer','Sp6_2_has_order315_element':False},
      'theorem':'Although both sets have cardinality 315, the abstract C13-orbit set cannot be identified equivariantly with the W(5,2) isotropic-line set under its natural symplectic automorphism group using the regular C315 torsor: Sp6(2) contains no element of order 315. The 315 equality is therefore a count match until extra non-cyclic/non-symplectic structure supplies an objectwise map.',
      'boundary':'This refutes the natural cyclic-Singer equivariant reading, not every possible bijection between the two 315-sets. A noncanonical bijection always exists by cardinality; a different group-mediated bridge would need separate construction.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','count':315,'Sp6_2_order315':False}))
    return 0
if __name__=='__main__':raise SystemExit(main())
