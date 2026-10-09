"""Certified second *ordered* energy upper enclosure from 11-state Wick intervals.

Construct two rational independent vectors (approximated Ritz eigendirections).
Exact interval arithmetic bounds the 2x2 restricted quadratic form above,
and an exact Gram lower bound provides an upper bound on lambda_max.
This does NOT lower-bound the ground energy or certify an excitation gap.
"""
import sys,json
from pathlib import Path
from fractions import Fraction as F
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_certified11_wick import I
def magbound(a):
    return max(abs(a.lo),abs(a.hi))
def bilinear(h,u,v):
    real=I(0);imag=I(0)
    for i,(a,b) in enumerate(u):
        for j,(c,d) in enumerate(v):
            re,im=h[i][j]
            real+=re*(a*c+b*d)-im*(a*d-b*c)
            imag+=re*(a*d-b*c)+im*(a*c+b*d)
    return real,imag
def certificate():
    data=json.loads((ROOT/'data/w33_20261009_certified11_wick.json').read_text())
    h=[[(I(F(re[0]),F(re[1])),I(F(im[0]),F(im[1]))) for re,im in row] for row in data['matrix_intervals']]
    mat=np.array([[complex(float((re.lo+re.hi)/2),float((im.lo+im.hi)/2)) for re,im in row] for row in h])
    ev,evec=np.linalg.eigh(mat)
    vectors=[[(F(f'{z.real:.13f}'),F(f'{z.imag:.13f}')) for z in evec[:,col]] for col in (0,1)]
    a,b=bilinear(h,vectors[0],vectors[0])[0],bilinear(h,vectors[1],vectors[1])[0]
    xy=bilinear(h,vectors[0],vectors[1])
    g0=sum(x*x+y*y for x,y in vectors[0]);g1=sum(x*x+y*y for x,y in vectors[1])
    gr=sum(x*u+y*v for (x,y),(u,v) in zip(*vectors))
    gi=sum(x*v-y*u for (x,y),(u,v) in zip(*vectors))
    gram_lower=min(g0,g1)-abs(gr)-abs(gi)
    numerator=max(a.hi,b.hi)+magbound(xy[0])+magbound(xy[1])
    upper=numerator/gram_lower
    assert gram_lower>F(9999999999,10**10)
    assert upper<F('139.666')
    return dict(status='PASS',upper_bound_on_second_ordered_eigenvalue=str(upper),
      decimal_upper=float(upper),compressed_trial_eigenvalues=list(map(float,ev[:2])),
      columns=[[[str(x),str(y)] for x,y in v] for v in vectors],
      gram_lower=str(gram_lower),Gershgorin_numerator=str(numerator),
      theorem='E1=minmax_lambda2(H) <= maxRayleigh(span(v0,v1)) <= GershgorinUpper(H2)/GershgorinLower(G2), all rationals outward upper bounds.',
      boundary='This is an upper bound for the SECOND ORDERED EIGENVALUE (counting multiplicity), not a lower bound for the ground energy or a bound for the first distinct excitation if the ground is degenerate.')
if __name__=='__main__':
    obj=certificate()
    (ROOT/'data/w33_20261009_second_ordered_upper_certificate.json').write_text(json.dumps(obj,indent=2)+'\n')
    print('CERTIFIED E_1 upper',obj['decimal_upper'])
