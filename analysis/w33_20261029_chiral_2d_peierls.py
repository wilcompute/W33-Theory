#!/usr/bin/env python3
"""A genuine 2D thermodynamic chiral SSB *conditional model*, not a TOE.
Project H27 k=+/- local threefold ground sectors, assume a square lattice
and interaction -J O_i O_j where O eigenvalues are +/-sqrt(3).
Then K=3J is exactly the ordinary zero-field nearest-neighbor 2D Ising
coupling. At low temperature, + and - infinite-volume Gibbs phases coexist
and a Peierls bound proves nonzero magnetization. Nothing selects one sign.
"""
import math,json
from collections import Counter
from fractions import Fraction as F

def verify():
 J=F(1,10);K=3*J
 torus=[]
 for n in (2,3,4):
  edges=[]
  for i in range(n):
   for j in range(n):
    v=i*n+j
    edges.append((v,i*n+(j+1)%n))
    edges.append((v,((i+1)%n)*n+j))
  hist=Counter()
  for bits in range(1<<(n*n)):
   anti=sum(((bits>>u)^(bits>>v))&1 for u,v in edges)
   bonds=-len(edges)+2*anti
   hist[bonds]+=1
  assert sum(hist.values())==2**(n*n)
  assert min(hist)==-2*n*n and hist[-2*n*n]==2
  torus.append(dict(n=n,sector_configurations=2**(n*n),
      ground_sign_patterns=2,ground_bond_energy=str(-2*n*n*K),
      first_three_bond_energies=[(str(K*e),v) for e,v in sorted(hist.items())[:3]]))
 # Peierls: plus-boundary phase, minus site entails an enclosing interface
 # gamma of >=4 dual edges; probability <= exp(-2*beta*K*|gamma|).
 # Count at most l*3^l self-avoiding dual contours of length l enclosing site,
 # using a marked ray crossing (<=l possible) and non-backtracking continuations.
 # At beta*K=log(12)/2, t=3*exp(-2*beta*K)=1/4.
 # Sum_l>=4 l*t^l = t^4*(4-3*t)/(1-t)^2 =13/576.
 # Consequently <s>_+ >= 1-2*(13/576)=275/288 >0.
 t=F(1,4)
 bound=t**4*(4-3*t)/(1-t)**2
 assert bound==F(13,576)
 m_lower=1-2*bound
 assert m_lower==F(275,288)
 betaK=math.log(12)/2
 beta_critical=math.asinh(1)/(2*float(K)) # exact square Ising critical line
 assert betaK/float(K)>beta_critical
 return dict(status="PASS_CONDITIONAL_2D_INTERACTION",local_H27_central_signs=[-1,1],
   project_nonzero_chiral_ground_sector=True,
   internal_local_ground_multiplicity_per_sign=3,
   explicitly_assumed_geometry="2D infinite square lattice with nearest-neighbor chiral sign interactions",
   assumed_J=str(J),Ising_K_equals_3J=str(K),
   numerical_tori=torus,
   beta_times_K_illustration="log(12)/2",inverse_temperature=float(betaK/float(K)),
   peierls_P_minus_upper=str(bound),plus_phase_magnetization_lower=str(m_lower),
   K_conjugate_negative_phase_exists=True,
   exact_2D_Ising_beta_critical=beta_critical,
   references=["Griffiths, Phys Rev 136 A437 (1964), DOI 10.1103/PhysRev.136.A437"],
   boundary="Assumes 2D lattice and J; projects away k=0 and excited sectors. Establishes spontaneous K-breaking in this assumed 2D projected Ising theory, NOT a selected physical vacuum, actual spacetime, masses or observed chirality.")
if __name__=="__main__":print(json.dumps(verify(),indent=2))
