"""Exact W(3,q) normalized Levi heat kernel and asymptotic no-go for
continuous 4-dimensional diffusion from the *unmodified* graph Laplacian.
This does not rule out other refinement graphs/actions."""
from pathlib import Path
import json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def eigens(q):
 n=(q+1)*(q*q+1)
 f=q*(q+1)**2//2
 g=q*(q*q+1)//2
 k=q+1
 return [(0,1),(2*k,1),(k-math.sqrt(2*q),f),(k+math.sqrt(2*q),f),(k,2*g)],2*n
def heat(q,t):
 spec,v=eigens(q);k=q+1
 probs=[mult*math.exp(-t*l/k) for l,mult in spec]
 Z=sum(probs);P=Z/v
 haz=sum(l*weight/k for (l,_),weight in zip(spec,probs))/Z
 return P,2*t*haz
def analyze():
 rows={}
 for q in (2,3,5,11,31,101,1001,1000001):
  vals=[]
  for t in (.25,.5,1,2,4):
   p,d=heat(q,t)
   vals.append(dict(t=t,heat_trace=p,running_dimension=d,limit_dimension=2*t,
                    distance_to_limit=abs(d-2*t)))
  rows[str(q)]=dict(n_points=(q+1)*(q*q+1),spectral_data=eigens(q)[0],samples=vals,
      normalized_nonzero_gap=(q+1-math.sqrt(2*q))/(q+1))
 for t in (.25,.5,1,2,4):
  assert abs(heat(1000001,t)[0]-math.exp(-t))<.003
  assert abs(heat(1000001,t)[1]-2*t)<.01
 result=dict(status='PASS',family='native symplectic generalized quadrangle W(3,q), unmodified degree-normalized Levi Laplacian L/(q+1)',
  spectra_formula='Levi graph: 0^1,(2k)^1,(k-sqrt(2q))^f,(k+sqrt(2q))^f,k^(2g), k=q+1, f=q(k+1)^2/2, g=q(q²+1)/2; total 2(k)(q²+1).',
  exact_asymptotic='At fixed normalized heat time t and q -> infinity, empirical Laplacian eigenvalue distribution tends to delta_1: P_q(t)=Tr(exp(-t L/k))/|V| -> exp(-t). Therefore running spectral dimension d_s(q,t)=-2 d ln P_q/d ln t -> 2t, NOT the constant 4 (or other constant) on any finite open interval.',
  spectral_gap_normalized_limit=1,
  finite_q_asymptotic='At fixed q, long-time return -> 1/|V| and running dimension -> 0.',
  prior_art='analysis/w33_20261009_w33_cartesian_power_spectral.py already covers the distinct n-fold Cartesian W33 replication no-go. Here we vary q in single symplectic generalized quadrangles instead.',
  rows=rows,
  limitation='This refutes only the naive unmodified normalized graph-Laplacian scaling. Other evolving graph sequences with local refinement, weighted graph Laplacians, interaction-generated metrics or Lorentzian actions are not ruled out. Positive heat evolution alone cannot give Lorentzian causality or Einstein equations.')
 (ROOT/'data/w33_20261009_toe21_qfamily_heat_nogo.json').write_text(json.dumps(result,indent=2)+'\n')
 print('SPACETIME',[(q,round(heat(q,1)[1],5)) for q in (2,3,5,11,31,101,1001)],flush=True)
 return result
if __name__=='__main__':analyze()
