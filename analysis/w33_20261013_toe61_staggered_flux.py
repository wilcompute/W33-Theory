"""TOE61 outside-box: exact all-temperature determinant flux theorem
SURVIVES arbitrary uniform sublattice-staggered gap m.
"""
from pathlib import Path
from itertools import product
import numpy as np,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep
ed,volts,*_=prep();E=np.asarray(ed,int);V=np.asarray(volts,int)
p=json.loads((R/'data/w33_20261013_toe61_det_poly.json').read_text())
assert p['number_three_pi_dominates']==7
# det(I+t (K+m²I))=(1+m²t)^40 det(I+(t/(1+m²t))K)
# for all real m and t>=0. Hence TOE61 positive polynomial
# inequalities survive a uniform staggered on-site gap.
gamma=[0]*80
adj=[[] for _ in range(80)]
for a,b in E:adj[a].append(b);adj[b].append(a)
seen={0:0};q=[0]
for a in q:
 for b in adj[a]:
  if b not in seen:seen[b]=1-seen[a];q.append(b)
  else:assert seen[b]!=seen[a]
assert sum(x==0 for x in seen.values())==40
for i in range(80):gamma[i]=1 if seen[i]==0 else -1
Gamma=np.diag(gamma)
def H(c,m):
 h=np.zeros((80,80))
 for (a,b),v in zip(E,V):
  h[a,b]=h[b,a]=-(-1)**int(v@np.asarray(c))
 return h+m*Gamma
def F(H,beta):
 e=np.linalg.eigvalsh(H)
 return float(-np.logaddexp(0.,-beta*e).sum()/beta)
corners=list(product((0,1),repeat=3))
rows=[]
for mass in (0.,.15,.8,2.,10.):
 for beta in (.2,1.,4.,15.):
  values=[F(H(c,mass),beta) for c in corners]
  assert values[-1]<min(values[:-1])-1e-10,(mass,beta,values)
  rows.append({'mass':mass,'beta':beta,
               'three_pi_minus_trivial':values[-1]-values[0],
               'three_pi_minus_second_best':values[-1]-min(values[:-1])})
out={'status':'PASS_TOE61_STAGGERED_MASS_ALL_TEMPERATURE_FLUX_THEOREM',
'numeric_test_count':len(rows),'samples':rows,
'conditional_exact_theorem':"H_{c,m}=[[mI,-B_c],[-B_c^T,-mI]] has eigenvalues ±sqrt(σ_j(B_c)^2+m²). For every t>=0, det(I+t(K_c+m² I))=(1+m²t)^40 det(I+t/(1+m²t) K_c). Since TOE61 proves exact nonnegative coefficientwise determinant differences and three-pi dominates every other Z2 corner, the dominance survives ANY real staggered mass m and every beta>0 at chemical potential0 via cosh Weierstrass product.",
'physics_limits':"One uniform sublattice-staggered spinless mass and half-filled fixed finite graph. Not general onsite potentials, chiral Standard Model, physical Dirac mass generation, interacting fermions, continuous U1 minimization, thermal gauge backreaction, or observed CP.",
'prior':"Mass deformation via H²=K+m² and Weierstrass product is elementary standard. The W33-specific coefficient certificates are TOE61."}
(R/'data/w33_20261013_toe61_staggered_flux.json').write_text(json.dumps(out,indent=2)+'\n')
print('TOE61 staggered',len(rows),'last gap',rows[-1]['three_pi_minus_second_best'])
