#!/usr/bin/env python3
"""Pass10685-10692 outside-box: the 3-5-7 clock factors recover exact W33 cyclotomic residue arithmetic.

The local rank-3 schemes from Pass10677 have exact spectral fields:

  C3 thin factor:     x^2+x+1       -> Q(sqrt(-3));
  C5 pentagon factor: x^2+x-1       -> Q(sqrt(5));
  C7 Singer factor:   x^2+x+2       -> Q(sqrt(-7)).

The C7 relation D={1,2,4} has Gauss-period eigenvalues (-1 +/- sqrt(-7))/2.
The C5 cycle relation has eigenvalues 2, (sqrt5-1)/2, -(sqrt5+1)/2.
Thus the rank-27 Bose-Mesner eigenmatrix lives in the multiquadratic compositum
Q(sqrt(-3),sqrt5,sqrt(-7)), of degree 8.

At the project's W33 parameter q=3,
  Phi3=13, Phi4=10, Phi6=7.
The binary-Leech clock tower has exact cardinalities
  |F4^6|-1 = 4095 = 3^2*5*7*13,
  PG(5,4)  = 1365 = 3*5*7*13,
  C13 quotient selector = 105 = 3*5*7.
Hence, specifically at q=3,
  105 = q * (Phi4(q)/2) * Phi6(q),
while the removed C13 clock is Phi3(q).  The first removed C3 is precisely the
internal F4^x scalar projectivization.

This is an arithmetic decomposition at q=3, not asserted as a polynomial
identity for arbitrary q.
"""
from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10685_10692_CYCLOTOMIC_357_W33_ARITHMETIC.json'

def phi3(q): return q*q+q+1
def phi4(q): return q*q+1
def phi6(q): return q*q-q+1

def main():
    q=3
    assert (phi3(q),phi4(q),phi6(q))==(13,10,7)
    nonzero=4**6-1; projective=nonzero//3; selector=projective//13
    assert (nonzero,projective,selector)==(4095,1365,105)
    assert nonzero==3*3*5*7*13
    assert projective==3*5*7*13
    assert selector==3*5*7
    assert selector==q*(phi4(q)//2)*phi6(q)
    assert projective==phi3(q)*selector
    assert nonzero==3*projective

    # Local minimal polynomials and discriminants.
    localspec={
      'C3':{'polynomial':'x^2+x+1','discriminant':-3,'field':'Q(sqrt(-3))'},
      'C5':{'polynomial':'x^2+x-1','discriminant':5,'field':'Q(sqrt(5))'},
      'C7':{'polynomial':'x^2+x+2','discriminant':-7,'field':'Q(sqrt(-7))'},
    }
    # Distinct independent squareclasses -3,5,-7 give degree 2^3.
    squareclasses={-3,5,-7,(-3)*5,(-3)*(-7),5*(-7),(-3)*5*(-7)}
    assert len(squareclasses)==7
    # None is a rational square (sign or squarefree absolute part > 1).
    def is_square_abs(n):
      if n<0:return False
      r=math.isqrt(n);return r*r==n
    assert all(not is_square_abs(n) for n in squareclasses)

    q5=json.loads((ROOT/'data/w33_pass543_547_icosahedral_fourier_recurrence.json').read_text())
    p543=q5['parts']['pass543']['association_scheme']
    assert p543['adjacency_charpoly']=='(x - 5)*(x + 1)**5*(x**2 - 5)**3'

    out={
      'schema':'w33.pass10685_10692.cyclotomic_357_w33_arithmetic.v1','status':'PASS','passes':'10685-10692','outside_box':True,
      'local_spectral_fields':localspec,
      'compositum':{'field':'Q(sqrt(-3),sqrt(5),sqrt(-7))','degree':8,'reason':'three independent quadratic squareclasses'},
      'W33_q3':{'q':3,'Phi3':13,'Phi4':10,'Phi6':7},
      'Leech_clock_factorization':{
        'F4^6_nonzero':'4095 = 3^2 * 5 * 7 * 13',
        'projectivize_by_F4_units':'4095 / 3 = 1365 = 3 * 5 * 7 * 13',
        'quotient_by_C13_clock':'1365 / 13 = 105 = 3 * 5 * 7',
        'W33_reading_at_q3':'105 = q * (Phi4(q)/2) * Phi6(q); removed C13 = Phi3(q)',
        'first_removed_C3':'F4^x scalar projectivization'},
      'golden_field_crosscheck':{
        'current_C5_factor':'pentagon relation has nontrivial eigenvalue polynomial x^2+x-1 and field Q(sqrt5)',
        'prior_q5_pass543':'icosahedral association image has factor (x^2-5)^3',
        'claim':'same quadratic spectral field Q(sqrt5), not an objectwise identification of the two schemes'},
      'Fano_field_reading':'The C7 Singer relation has Gauss periods (-1 +/- sqrt(-7))/2 and is simultaneously the Fano (7,3,1) difference-set factor from Pass10677.',
      'theorem':'After the intrinsic F4 scalar and C13 clock are removed from F4^6, the 105-state harmonic residue factors at W33 q=3 as q*(Phi4/2)*Phi6 = 3*5*7. Its three rank-3 harmonic factors carry the exact quadratic fields Q(sqrt(-3)), Q(sqrt5), and Q(sqrt(-7)), with the C5 factor supplying the golden field and the C7 factor supplying the Fano/Singer field.',
      'boundary':'The factor identity is a special arithmetic identity at q=3, not a universal polynomial identity. The Q(sqrt5) match to the repo q=5 icosahedral lane is a shared spectral field only.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','selector':105,'W33_factors':[13,10,7],'harmonic_fields':['sqrt(-3)','sqrt5','sqrt(-7)']}))
if __name__=='__main__': main()
