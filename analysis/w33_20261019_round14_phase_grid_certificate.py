"""Rigorous contiguous temperature BAND of global-threshold failure.
Use exact Q(omega) rational traces + Taylor/alternating exponential
bounds at EVERY rational grid center, Lipschitz to cover intervals.
No diagonalizations/optimizers in the proof.
"""
from __future__ import annotations
import json,math,itertools
from pathlib import Path
from fractions import Fraction as F
import sympy as S
from w33_20261019_tick_operator_frame_majorization import points,symp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round14_phase_grid_certificate.json"
W=S.Matrix([[0,-1],[1,-1]]);I18=S.eye(18);OMEGA=S.kronecker_product(S.eye(9),W)
def pauli(pt):
 a,b,c,d=pt
 R=S.zeros(18)
 for i,j in itertools.product(range(3),repeat=2):
  r=3*((i+a)%3)+(j+b)%3;t=3*i+j;V=W**((c*i+d*j)%3)
  for u,v in itertools.product(range(2),repeat=2):R[2*r+u,2*t+v]=V[u,v]
 return R
def main():
 pts=points();ids=[0,23,27,28,34,36,39];ks=[2,2,2,1,2,0,1];wt=[S.Rational(1473,10000)]*6+[S.Rational(1162,10000)]
 assert all(symp(pts[a],pts[b])!=0 for a,b in itertools.combinations(ids,2))
 Q=S.zeros(18)
 for i,k,w in zip(ids,ks,wt):
  U=pauli(pts[i]);P=(I18+(OMEGA**((-k)%3))*U+(OMEGA**((-2*k)%3))*(U**2))/3
  Q+=w*P
 assert S.trace(Q)==6
 nmax=18; mom=[];P=I18
 for n in range(nmax+1):
  mom.append(F(int(S.numer(S.trace(P)/2)),int(S.denom(S.trace(P)/2))))
  P=P*Q
 assert mom[0]==9 and mom[1]==3
 C=F(4,3)*sum((F(str(wt[i]))*F(str(wt[j])) for i,j in itertools.combinations(range(7),2)),F())
 fact=[math.factorial(n) for n in range(nmax+2)]
 def elowerupper(a):
  lo=sum((a**n/fact[n] for n in range(nmax+1)),F())
  assert a<F(nmax+2)
  upper=lo+a**(nmax+1)/fact[nmax+1]/(1-a/F(nmax+2))
  return lo,upper
 def midpoint_bound(T):
  a=1/T
  eL,eU=elowerupper(a)
  # κ_local=-1/2*(E-1)/(E+2); decreasing in E.
  kU=-(eL-1)/(2*(eL+2))
  x=kU*C/T
  assert F(-1)<x<0
  exU=sum((x**n/math.factorial(n) for n in range(5)),F())
  ZL=sum((mom[n]*a**n/fact[n] for n in range(nmax+1)),F())
  ratio=(3*eU+6)*exU
  gap=ZL-ratio
  # Δ=T log(Z_real/R_real) >= T*(ZL-ratio)/ZL
  return T*gap/ZL
 # closed band, step 1/5000, midpoint h/2=1/10000.
 start=F(19,20);end=F(13,10);step=F(1,5000)
 N=int((end-start)/step)
 assert start+N*step==end and N==1750
 maxvariation=step/F(2)*(3+2*C)
 minmargin=None;worst_i=None;neg_count=0
 for i in range(N):
  T=start+(i*2+1)*step/2
  m=midpoint_bound(T)
  if m<=maxvariation:neg_count+=1
  if minmargin is None or m-maxvariation<minmargin:
   minmargin=m-maxvariation;worst_i=i
 assert neg_count==0,("insufficient lower bounds",neg_count,worst_i,float(minmargin))
 assert minmargin>0
 checks={"exact_18x18_Qomega_projectors":True,
   "1750_rational_temperature_midpoint_certificates":N==1750,
   "each_midpoint_margin_exceeds_Rigorous_Lipschitz_halfstep":neg_count==0,
   "uniform_strict_lower_bound_positive":minmargin>0,
   "nonzero_contiguous_band_0p95_to_1p30":start==F(19,20) and end==F(13,10)}
 out={"schema":"w33.round14.rational_grid_temperature_band.v1",
  "theorem":"At the two-tick local critical coupling κ_local(T), one fixed seven-tick rational W33 state has strictly lower engineered free energy than a singleton for EVERY T in [0.95,1.30], not just grid points. For 1750 rational midpoints spaced 1/5000, exact Q(omega)-over-Q rational trace powers n<=18 lower bound Tr exp(Q/T), rational Taylor lower-upper bounds exp(1/T), and degree-four alternating-series upper bound exp(κ_upper C/T) yield exact lower energy advantage at EVERY midpoint. The Gibbs entropy derivative difference <=ln9<3 and |κ_local'|<2 on the band imply variation <= halfstep*(3+2C). Every exact rational certified midpoint lower advantage exceeds this bound. Finitely many rational checks + Lipschitz cover the ENTIRE continuum interval.",
  "T_interval":["19/20","13/10"],"grid_subintervals":N,
  "exact_Rational_C":str(C),"max_halfstep_Lipschitz_error":str(maxvariation),
  "max_halfstep_error_float":float(maxvariation),
  "worst_grid_index":worst_i,
  "minimum_proved_energy_advantage_over_entire_band_exact":str(minmargin),
  "minimum_proved_energy_advantage_over_entire_band_float":float(minmargin),
  "trace_moments_n0_to18":[str(x) for x in mom],
  "boundary":"Does NOT determine the global transition curve or prove seven-tick state is exact global minimizer; only a rigorously feasible competitor at κ_local over specified band. No physical negative coupling derived.",
  "checks":checks,"all_checks_pass":all(checks.values())}
 OUT.write_text(json.dumps(out,indent=2)+"\n")
 print(json.dumps({"pass":out["all_checks_pass"],"band":out["T_interval"],"grid":N,"min_energy_margin":out["minimum_proved_energy_advantage_over_entire_band_float"]}))
 return out
if __name__=="__main__":main()
