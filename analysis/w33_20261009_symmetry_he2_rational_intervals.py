"""Independent outward-rounded exact Wick certificate of PSp He2
24- and 15-dimensional W33 quantum current trial sectors.
The interval arithmetic and sign convention are imported from audited
Pass11786; this producer does NOT assume trial values are exact levels.
"""
from pathlib import Path
import json
from fractions import Fraction as F
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_certified11_wick import I,block,parameters
import w33_20261008_5state_ritz as P
def certify():
  edges,n,A,B,wp,wl=P.geometry()
  m,t,f,e=parameters()
  base={}
  for side,adj,W in [('p',A,wp),('l',B,wl)]:
    idx=[0,int(np.flatnonzero(adj[0])[0]),int(np.flatnonzero((adj[0]==0)&(np.arange(40)!=0))[0])]
    base[side]=[block(edges,W[0],W[j],side,side,m,t,f,left=(2,),right=(2,))[0][0] for j in idx]
  inc=int(np.flatnonzero(n[0])[0])
  non=int(np.flatnonzero(n[0]==0)[0])
  cross=[block(edges,wp[0],wl[j],'p','l',m,t,f,left=(2,),right=(2,))[0][0] for j in (inc,non)]
  def orbital(v,lam):
    return v[0][0]+lam*v[1][0]-(lam+1)*v[2][0]
  n24=I(F(32,27));n15=I(F(16,27))
  p24=orbital(base['p'],2)/n24
  l24=orbital(base['l'],2)/n24
  c24=I(6).sqrt()*(cross[0][0]-cross[1][0])/n24
  ci24=I(6).sqrt()*(cross[0][1]-cross[1][1])/n24
  avg=(p24+l24)/2
  discr=(((p24-l24)/2)**2+c24*c24+ci24*ci24).sqrt()
  p15=orbital(base['p'],-4)/n15
  l15=orbital(base['l'],-4)/n15
  value={'24_lower_ritz_interval':(avg-discr).data(),
         '24_upper_ritz_interval':(avg+discr).data(),
         '15_point_ritz_interval':p15.data(),
         '15_line_ritz_interval':l15.data(),
         'sector24_gram_norm':str(F(32,27)),
         'sector15_gram_norm':str(F(16,27))}
  # Round outward to fixed publicly useful figures
  assert 142.7193<float(F(value['24_lower_ritz_interval'][0]))<142.7194
  assert 145.1724<float(F(value['24_upper_ritz_interval'][0]))<145.1725
  assert all(143.6110<float(F(value[z][0]))<143.6112 for z in ('15_point_ritz_interval','15_line_ritz_interval'))
  return dict(status='PASS',schema='w33.20261009.symmetry_ritz_rational_intervals.v1',**value,
     theorem='Point/line He2 trial spaces each decompose into 1+24+15. Exact Wick 2x2 block and 1x1 blocks enclose Ritz energy levels, giving upper bounds by min-max within invariant sectors.',
     certification='Outward rational Wick intervals with 10^-36 grid at every operation; not based on convergence of Gaussian quadrature.',
     boundary='No lower spectral enclosure in full Hamiltonian; true ground irrep and spectral gap are not proved. Multiplicities are trial-representation dimensions, not exact spectral degeneracies.')
if __name__=='__main__':
  d=certify()
  (ROOT/'data/w33_20261009_symmetry_he2_rational_intervals.json').write_text(json.dumps(d,indent=2)+'\n')
  print('Certified He2 intervals',{k:v for k,v in d.items() if 'interval' in k and k!='certification'})
