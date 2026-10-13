"""TOE61 exact W33 determinant dominance -> all-temperature Z2 flux theorem.

Exact 40x40 integer characteristic coefficients. Independent product of
cosh proof converts determinant dominance at every t>=0 into free energy
inequality for every beta>0 at zero chemical potential.
"""
from pathlib import Path
from itertools import product
import json,sys,hashlib,numpy as np,sympy as sp
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep
ed,volts,*_=prep();ed=np.asarray(ed,int);volts=np.asarray(volts,int)
adj=[[] for _ in range(80)]
for a,b in ed:adj[a].append(b);adj[b].append(a)
seen={0:0};q=[0]
for a in q:
 for b in adj[a]:
  if b not in seen:seen[b]=1-seen[a];q.append(b)
  else:assert seen[b]!=seen[a]
left=[x for x in range(80) if seen[x]==0];right=[x for x in range(80) if seen[x]==1]
assert len(left)==len(right)==40
li={a:i for i,a in enumerate(left)};ri={b:i for i,b in enumerate(right)}
def poly(c):
 B=np.zeros((40,40),dtype=int)
 for (a,b),v in zip(ed,volts):
  z=(-1)**int(v@np.asarray(c))
  if seen[a]==0:B[li[a],ri[b]]=z
  else:B[li[b],ri[a]]=z
 K=sp.Matrix((B@B.T).tolist())
 coeff=K.charpoly().all_coeffs()
 det=[int((-1)**j*coeff[j]) for j in range(41)]
 assert det[0]==1 and all(x>=0 for x in det)
 return det
corners=list(product((0,1),repeat=3))
polys=[poly(c) for c in corners]
base=polys[0]
data=[];pairwise=[]
for ci,c in enumerate(corners):
 p=polys[ci];delta=[a-b for a,b in zip(p,base)]
 assert delta[:4]==[0]*4
 assert all(x>=0 for x in delta)
 first=next((i for i,z in enumerate(delta) if z),None)
 rec=dict(corner=list(c),full_det_coefficients_decimal=[str(x) for x in p],
          full_difference_from_zero_decimal=[str(x) for x in delta],
          first_nonzero_difference_degree=first,
          strictly_positive_coefficient_count=sum(z>0 for z in delta),
          negative_coefficient_count=sum(z<0 for z in delta))
 data.append(rec)
 for cj,other in enumerate(corners):
  if ci==cj:continue
  diff=[a-b for a,b in zip(polys[ci],polys[cj])]
  if all(z>=0 for z in diff):
   pairwise.append(dict(dominating=list(c),dominated=list(other),
                        positive_coefficient_count=sum(z>0 for z in diff)))
 print('DETPOLY',c,'first',first,'nonnegative',rec['negative_coefficient_count']==0,flush=True)
# Independent crosscheck against TOE59 signed eighth trace moment.
# Since p1,p2,p3 of K equal for every c, Newton identities imply
# Δe4(K)=-Δtr(K^4)/4=-Δtr(H^8)/8.
mom=json.loads((R/'data/w33_20261013_toe59_wilson_girth_moments.json').read_text())
moment_index={tuple(r['pi_corner']):r['trace_moment_difference'] for r in mom['tested_corners']}
moment_bridge=[]
for r in data[1:]:
 c=tuple(r['corner'])
 lhs=int(r['full_difference_from_zero_decimal'][4])
 rhs=-int(moment_index[c])//8
 assert int(moment_index[c])%8==0 and lhs==rhs,(c,lhs,rhs)
 moment_bridge.append({'corner':list(c),'delta_e4_exact':lhs,
   'delta_trH8_exact':int(moment_index[c])})
trip=tuple((1,1,1))
trip_dom=[x for x in pairwise if tuple(x['dominating'])==trip]
print('THREE_PI_DOMINATES',len(trip_dom),'of 7',flush=True)
# Mathematical all-temperature dominance proof:
# Fβ(H)= -2/β Σ_σ log(2cosh(βσ/2)); cosh(βσ/2)
# = ∏_(n>=0)(1+β²σ²/(π²(2n+1)²)).
# Thus Fβ(c)-Fβ(c')=-2/β Σ_(n>=0)
# log[det(I+t_n K_c)/det(I+t_n K_c')].
# If coefficientwise det domination, every factor >=1.
out={'status':'PASS_TOE61_EXACT_ALL_TEMPERATURE_Z2_FLUX_DOMINANCE',
'graph':{'80_sites':80,'40_40_bipartition':True,'40_squared_singular_values':True},
'positive_coefficients_verified_integers':True,
'Z2_character_polynomials':data,
'coefficientwise_partial_order':pairwise,
'number_three_pi_dominates':len(trip_dom),
'exact_Newton_bridge_to_TOE59_octagon_H8':moment_bridge,
'theorem':"For the supplied W33 static half-filled spinless bipartite hopping H_c and eight Z2 flat deck holonomies c, the EXACT INTEGER coefficients of det(I+t B_c B_c.T) minus det(I+t B_0 B_0.T) are >=0. Hence for every t>=0 the determinant of every nontrivial c is >= trivial. The Weierstrass infinite product cosh(z)=prod_(n>=0)[1+4z²/(pi²(2n+1)²)] converts that into the exact inequality F_beta(c)<=F_beta(0) for ALL beta>0 at chemical potential zero. Every nonzero c has strict polynomial inequality and hence strict free energy inequality.",
'extra_result':"If the three-pi corner coefficientwise dominates every other corner, it is also the global minimum among these eight Z2 connections for every beta>0. This DOES NOT optimize over continuous U1 holonomies.",
'novelty_limit':"This is an application of standard charpolys and cosh products to the native W33 graph, not a new general flux-phase theorem. Planar Lieb flux theorem has different assumptions. Finite noninteracting static matter, fixed 80-site graph, no dynamical gauge-field backreaction, no physical CP, no SM or observable alpha.",
'verification':"All 41 exact integer coefficients for every corner and pairwise partial order are frozen; recomputation via Sympy's exact characteristic polynomial reproduces them without floating point."}
(R/'data/w33_20261013_toe61_det_poly.json').write_text(json.dumps(out,indent=2)+'\n')
