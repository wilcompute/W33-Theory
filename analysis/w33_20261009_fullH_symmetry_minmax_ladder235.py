"""Certified full-H min-max spectral *counting ladder* from the
already exact-Wick 24/15 He2/4/6 trial blocks.

For each of 6 /3 columns, rationalize numpy eigenspace vectors;
form EXACT fraction Gram and the midpoint projected Ritz form, and
certify B*Gram-H is strictly diagonally dominant with a
conservative <=1e-20 enclosure for interval uncertainty.
This avoids trusting raw numpy eigenvalues as certified.
"""
from pathlib import Path
import sys,json,math
from fractions import Fraction as F
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def gaussian_critical(block,cutoff,r):
 d=len(block)
 mid=np.array([[complex(float((F(z[0][0])+F(z[0][1]))/2),float((F(z[1][0])+F(z[1][1]))/2)) for z in row] for row in block])
 assert np.max(abs(mid-mid.conj().T))<1e-12
 ew,U=np.linalg.eigh(mid)
 V=[[complex(F(f'{U[a,j].real:.11f}'),F(f'{U[a,j].imag:.11f}')) for j in range(r)] for a in range(d)]
 # Exact rational complex: entries=(F,F); use ordinary python complex
 # for display only, rational real/im required for certificate.
 v=[[(F(f'{U[a,j].real:.11f}'),F(f'{U[a,j].imag:.11f}')) for j in range(r)] for a in range(d)]
 R=[[F((F(b[0][0])+F(b[0][1]))/2) for b in row] for row in block]
 I=[[F((F(b[1][0])+F(b[1][1]))/2) for b in row] for row in block]
 halfwidth=max(max(F(z[k][1])-F(z[k][0]) for k in (0,1)) for row in block for z in row)
 assert halfwidth<F(1,10**23),halfwidth
 def times(z,w):
  a,b=z;c,e=w
  return (a*c-b*e,a*e+b*c)
 def plus(z,w):return (z[0]+w[0],z[1]+w[1])
 def conj(z):return (z[0],-z[1])
 zeros=(F(0),F(0))
 G=[[zeros for j in range(r)] for i in range(r)]
 K=[[zeros for j in range(r)] for i in range(r)]
 for i in range(r):
  for j in range(r):
   for a in range(d):
    G[i][j]=plus(G[i][j],times(conj(v[a][i]),v[a][j]))
    for b in range(d):
     K[i][j]=plus(K[i][j],times(conj(v[a][i]),times((R[a][b],I[a][b]),v[b][j])))
 B=F(math.ceil(ew[r-1]*10**6)+10,10**6)
 # Worst absolute perturbation per entry of reduced K: at most
 # 4*d²*max halfwidth (safe given real and imag component bounds <=1).
 error=F(4*d*d)*halfwidth
 margins=[]
 for i in range(r):
  diag=B*G[i][i][0]-K[i][i][0]
  radius=sum(abs(B*G[i][j][0]-K[i][j][0])+abs(B*G[i][j][1]-K[i][j][1]) for j in range(r) if j!=i)
  bound=diag-radius-r*error
  assert bound>0,(r,i,float(bound),float(diag),float(radius))
  margins.append(float(bound))
 assert all(G[i][i][0]>F(999,1000) for i in range(r))
 return dict(rank=r,upper=str(B),matrix_dimension=d,gershgorin_min_margin=min(margins),
   bound_on_each_projected_entry_error=str(error),floating_reference_eigenvalue=float(ew[r-1]),
   certificate='B*Gram-V*H*V is strictly diagonally dominant with exact rational componentwise offdiagonal 1-norm; interval uncertainty budget <=r*4*d^2*max(original interval width). Implies positive definite for ALL exact Wick block matrices.')
def certificate():
 raw=json.load(open(ROOT/'data/w33_20261009_he246_symmetry_exact_wick.json'))
 sectors={}
 for key,data in raw['sectors'].items():
  mat=data['matrix_intervals'];sectors[key]=[gaussian_critical(mat,0,r) for r in range(1,len(mat)+1)]
 # First trivial state certificate from corrected full Hamiltonian interval
 triv=F('127.595507')
 events=[]
 for k,records in sectors.items():
  mult=24 if k=='24' else 15
  for rec in records:events.append((F(rec['upper']),k,rec['rank'],mult))
 events.sort()
 maxima={k:0 for k in sectors}
 ladder=[dict(fullH_ordered_eigenvalue_index=1,certified_upper=str(triv),active_trial_multiplicity={'trivial':1})]
 for B,k,rank,mult in events:
  maxima[k]=max(maxima[k],rank)
  idx=1+sum((24 if key=='24' else 15)*r for key,r in maxima.items())
  ladder.append(dict(fullH_ordered_eigenvalue_index=idx,certified_upper=str(B),
       active_trial_multiplicity={key:r for key,r in maxima.items()}))
 assert ladder[-1]['fullH_ordered_eigenvalue_index']==235
 assert float(F(ladder[-1]['certified_upper']))<182.169
 return dict(status='PASS',independent_symmetry_trial_dimensions={'trivial':1,'24':24*6,'15_p':15*3,'15_l':15*3},
  exact_Gershgorin_certificates=sectors,fullH_minmax_ladder=ladder,
  fullH_E235_upper=ladder[-1]['certified_upper'],
  theorem='Each rationalized projected Ritz subspace V of size r has a certified exact positive-definite B*V*V-V*H*V by rational strict diagonal dominance and explicit original Wick enclosure error. PSp covariance supplies 24 or 15 isotypic orthonormal copies. Min-max gives real full infinite-H eigenvalue-count UPPER bounds up to E235. All certificates are from above and do not decide true ground symmetry, lower energies or first distinct physical gap.',
  limitation='Orthogonality of 24 vs 15 vs trivial follows from PSp representation; point/line 15 cross Gram and Hamiltonian blocks vanish by 0 singular-value line-point incidence association scheme, already proved in earlier He24 pass.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_fullH_symmetry_minmax_ladder235.json').write_text(json.dumps(d,indent=2)+'\n')
 print('235 MINMAX',[(x['fullH_ordered_eigenvalue_index'],float(F(x['certified_upper']))) for x in d['fullH_minmax_ladder']])
