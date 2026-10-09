"""Formal rational interval certificate: all 80 W33 classical zero star
directions have global coherent-displacement minimum at zero when covariance
and Gaussian phase are fixed to Pass11769's EXACT optimized complex trial.
Essential cubic terms retained. This is NOT a ground-energy lower bound.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as H

def box(lo,hi=None):return (F(lo),F(lo if hi is None else hi))
def plus(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return (-x[1],-x[0])
def sub(x,y):return plus(x,neg(y))
def mul(x,y):
 v=[a*b for a in x for b in y]
 return min(v),max(v)
def div(x,y):
 assert y[0]>0 or y[1]<0
 return mul(x,(1/y[1],1/y[0]))
def sq(x):return (F(0) if x[0]<=0<=x[1] else min(x[0]**2,x[1]**2),max(x[0]**2,x[1]**2))
def times(x,y):return mul(x,y)
def checked(star,U,V,m,t,f):
 q=np.zeros(80,dtype=np.int64)
 if star<40:q[:40]=-1;q[star]=39
 else:q[40:]=1;q[star]=-39
 active=np.flatnonzero(V@q+40)
 assert len(active)==4
 p=-40*U[active].sum(axis=0)
 assert np.all((V@q+40)*(U@p+40*7680)==0)
 X=[F(int(x),40) for x in V@q]
 Y=[F(int(y),40*7680) for y in U@p]
 Sxx=sum(x*x for x in X)/20
 Syy=sum(y*y for y in Y)/20
 Sxy=sum(x*y for x,y in zip(X,Y))/20
 W=F(1,200)*sum(x*x*y for x,y in zip(X,Y))
 Z=F(1,200)*sum(x*y*y for x,y in zip(X,Y))
 R=F(1,400)*sum(x*x*y*y for x,y in zip(X,Y))
 sx=mul(m,t)
 sy=plus(div(m,t),mul(sq(f),sx))
 cross=mul(f,sx)
 A=mul(plus(box(F(1,20)),sy),box(Sxx))
 B=mul(plus(box(F(1,20)),sx),box(Syy))
 T=mul(box(4*Sxy),plus(box(F(1,20)),cross))
 w,z,r=box(W),box(Z),box(R)
 D0=sub(mul(box(4),mul(A,B)),sq(T))
 D1=sub(mul(box(4),mul(A,z)),mul(box(2),mul(T,w)))
 D2=sub(mul(box(4),mul(A,r)),sq(w))
 Ddisc=sub(sq(D1),mul(box(4),mul(D0,D2)))
 alpha_disc=sub(sq(z),mul(box(4),mul(B,r)))
 assert min(A[0],B[0],R)>0
 assert D0[0]>0 and D2[0]>0
 assert Ddisc[1]<0 and alpha_disc[1]<0, (star,Ddisc,alpha_disc)
 return dict(star=star,
  H0_discriminant_lower=str(D0[0]),theta_discriminant_upper=str(Ddisc[1]),
  alpha_discriminant_upper=str(alpha_disc[1]),
  D2_lower=str(D2[0]),
  # Conservatively rounded displayed extrema; full rationals retained in calculations.
  numeric=dict(A=[float(v) for v in A],B=[float(v) for v in B],
    discriminant_upper=float(Ddisc[1]),alpha_disc_upper=float(alpha_disc[1]),
    D0_lower=float(D0[0]),D2_lower=float(D2[0])))

def main():
 trial=H.exact_trial(); br=H.root_bracket(trial)
 sqrtlo,sqrthi=map(F,br['sqrt10_interval'])
 tlo,thi=map(F,br['t_interval'])
 assert sqrtlo**2<10<sqrthi**2
 mlo=(6*sqrtlo+15)/40;mhi=(6*sqrthi+15)/40
 m=box(mlo,mhi);t=box(tlo,thi)
 b=F(1,20)
 f=div(box(-2*b),plus(mul(box(3),mul(m,t)),box(b)))
 g=H.geometry()
 U=np.rint(40*g['u']).astype(np.int64);V=np.rint(40*g['v']).astype(np.int64)
 rows=[checked(i,U,V,m,t,f) for i in range(80)]
 assert len(rows)==80
 Dmin=min(r['numeric']['D0_lower'] for r in rows)
 D2min=min(r['numeric']['D2_lower'] for r in rows)
 discmax=max(r['numeric']['discriminant_upper'] for r in rows)
 admax=max(r['numeric']['alpha_disc_upper'] for r in rows)
 out=dict(status='EXACT_RATIONAL_INTERVAL_CERTIFIED',all80=True,
  root_bracket=br,interval_m=[str(z) for z in m],
  interval_t=[str(z) for z in t],interval_f=[str(z) for z in f],
  numerical_summary=dict(D0_lower_min=Dmin,D2_lower_min=D2min,D_discriminant_upper_max=discmax,alpha_discriminant_upper_max=admax),
  star_rows=rows,
  theorem='At every one of 80 native classical-zero star coherent directions, holding the Pass11769 centered complex Gaussian covariance and phase fixed, E(s,r)-E0=A s²+B r²+T sr+W s²r+Z sr²+R s²r². Exact rational outward interval checks prove A,B,R>0, alpha(s)=B+Zs+Rs²>0 for all real s, and D(s)=4A alpha(s)-(T+Ws)²>0 for all real s. Thus the centered Gaussian is the UNIQUE minimizer over both real coherent amplitudes s,r for each star. This is not a lower bound on infinite-dimensional H or unrestricted covariances.',
  proof_scope='Fractions with exact sqrt10 and stationarity-root rational isolating intervals; finite exact incidence sums, all 80. Generalized star coherent directions only, NOT arbitrary displacement vectors or arbitrary Gaussian covariance.')
 (ROOT/'data/w33_20261009_round20_exact_star_interval.json').write_text(json.dumps(out,indent=2)+'\n')
 print('EXACT INTERVAL all80 star coherent minima',out['numerical_summary'],flush=True)
if __name__=='__main__':main()
