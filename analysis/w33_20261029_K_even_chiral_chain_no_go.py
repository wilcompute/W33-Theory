#!/usr/bin/env python3
"""K-even H27 chiral many-body toy chain: finite-volume symmetry and 1D limits.
This does NOT derive a physical vacuum. Inter-cell ferromagnetic J is assumed.
"""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import math,json

def sector_energy(seq,g=F(1,4),J=F(1,10),field=F(0)):
 n=len(seq)
 # The H27 one-body sector minima are -2-3g for central k=+/-,
 # -2 in central k=0; chiral observable O=+/-sqrt(3),0.
 one=-2*n-3*g*sum(x!=0 for x in seq)
 bond=-3*J*sum(seq[i]*seq[(i+1)%n] for i in range(n))
 # Conjugate field of strength field/sqrt3: -field * chirality_sign.
 return one+bond-field*sum(seq)

def verify():
 g=F(1,4);J=F(1,10)
 rows=[]
 for n in range(3,9):
  en=Counter(sector_energy(s,g,J) for s in product((-1,0,1),repeat=n))
  E0=min(en)
  E1=min(e for e in en if e>E0)
  assert E0==n*(-2-3*g-3*J)
  assert en[E0]==2
  assert E1-E0==12*J
  # Each chiral one-site k=+/- sector has three independent
  # lowest-energy states. Thus 2*3**n actual ground eigenstates.
  rows.append(dict(cells=n,sector_patterns=3**n,minimum=str(E0),
    first_sector_gap=str(E1-E0),ground_sector_patterns=2,
    internal_ground_multiplicity=2*3**n))
 # K maps signs + <-> -, and H is exactly even under K.
 assert sector_energy([1]*7,g,J)==sector_energy([-1]*7,g,J)
 # A positive field selects one sign; reversing field selects the other.
 h=F(1,1000)
 assert sector_energy([1]*5,g,J,h)<sector_energy([-1]*5,g,J,h)
 assert sector_energy([1]*5,g,J,-h)>sector_energy([-1]*5,g,J,-h)
 # For the projected 3-state nearest-neighbor transfer matrix with
 # finite beta, every entry is positive. Perron-Frobenius then
 # ensures one simple dominant eigenvalue, i.e. no finite-T
 # phase transition in this finite-range 1D chain.
 for beta in (.1,1.,3.,10.):
  T=[[math.exp(beta*(3*float(J)*a*b+
        .5*(3*float(g)*(a!=0)+3*float(g)*(b!=0)))) for b in (-1,0,1)]
        for a in (-1,0,1)]
  assert all(x>0 and math.isfinite(x) for row in T for x in row)
 return dict(status="PASS",group="H27^N",
  local_H="X+X^-1+Y+Y^-1-g*[i(Z-Z^-1)]^2",
  added_assumption="Commuting nearest-neighbor -J O_i O_j with O=i(Z-Z^-1).",
  g=str(g),J=str(J),central_sign_values=[-1,0,1],
  ground_chiral_vacua="two K-exchanged uniform sign sectors, with 3^N local degeneracy each",
  checked_ring_sizes=rows,field_sign_selects_chirality=True,
  finite_temperature_1d_finite_range="No spontaneous symmetry breaking at T>0; strictly positive finite-temperature transfer matrix.",
  obstruction="Any finite-dimensional real K-even Hamiltonian with unique ground state has zero expectation of every K-odd Hermitian observable.",
  limitations="Inter-site coupling and one-dimensional lattice are externally assumed. Not a derived spacetime, chiral Standard Model, physical mass scale, or unique zero-field ground state.")
if __name__=="__main__":print(json.dumps(verify(),indent=2))
