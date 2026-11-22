#!/usr/bin/env python3
"""Explicit H27-invariant, renormalizable mediator lift of four singlet moduli.

Scope: SO(10)-singlet u_i,v_i and a single E6-adjoint Cartan a, plus eight
E6-singlet H27-character mediators. Does not audit all 27+27bar fields or
establish a realistic nonabelian vacuum.
"""
from itertools import product
import json
from pathlib import Path
import sympy as s
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_round7_h27_mediator_vacuum.json'

def verify():
  w=s.Rational(-1,2)+s.sqrt(3)*s.I/2
  X=s.zeros(3)
  for k in range(3):X[(k+1)%3,k]=1
  Z=s.diag(1,w,w**2)
  u=s.Matrix(s.symbols('u0:3'));v=s.Matrix(s.symbols('v0:3'));a=s.symbols('a')
  modes=tuple((i,j) for i,j in product(range(3),repeat=2) if (i,j)!=(0,0))
  ss={ij:s.Symbol('s'+str(ij[0])+str(ij[1])) for ij in modes}
  B={(i,j):s.expand((v.T*(X**i)*(Z**j)*u)[0]) for i,j in product(range(3),repeat=2)}
  # For the E6 charge-4 bilinear: (m+4lambda a) B00 +36 M a^2.
  # H27-equivariant neutral mediator: s_ab transforms inverse to B_ab;
  # s_ab*s_-a,-b is invariant. All terms are degree <=3.
  m=s.Rational(20,9)
  mass=sum(ss[ij]*ss[(-ij[0])%3,(-ij[1])%3] for ij in modes)
  W=(m+4*a)*B[0,0]+36*a*a+sum(ss[ij]*B[ij] for ij in modes)+mass/2
  var=list(u)+list(v)+[a]+[ss[t] for t in modes]
  root={u[0]:1,u[1]:0,u[2]:0,v[0]:1,v[1]:0,v[2]:0,a:-s.Rational(1,18)}
  root.update({ss[t]:(-1 if t in ((0,1),(0,2)) else 0) for t in modes})
  g=[s.expand(s.diff(W,x)) for x in var]
  grad=[s.simplify(f.subs(root)) for f in g]
  assert grad==[0]*len(var),grad
  # Integrate out the massive s mediators: W_eff = W0 - (1/2) sum B_ab B_-ab.
  weff=(m+4*a)*B[0,0]+36*a*a-s.Rational(1,2)*sum(B[t]*B[(-t[0])%3,(-t[1])%3] for t in modes)
  qvar=list(u)+list(v)+[a]
  Hred=s.Matrix([[s.simplify(s.diff(weff,x,y).subs(root)) for y in qvar] for x in qvar]);rankred=int(Hred.rank());assert rankred==6
  gauge=s.Matrix([1,0,0,-1,0,0,0]);assert Hred*gauge==s.zeros(7,1)
  # In full 15x15 F Hessian, SS block is a permutation matrix with rank8.
  Hss=s.Matrix([[s.diff(W,x,y) for y in var[7:]] for x in var[7:]]);
  assert Hss.det()!=0 and Hss.rank()==8
  # Schur-complement theorem implies full Hessian rank = 8 + rank(Hred) = 14.
  fullrank=8+rankred
  # Verify Hred is the exact Schur complement of the mediator Hessian.
  A=s.Matrix([[s.simplify(s.diff(W,x,y).subs(root)) for y in qvar] for x in qvar])
  Bmix=s.Matrix([[s.simplify(s.diff(W,x,y).subs(root)) for y in var[7:]] for x in qvar])
  schur=s.simplify(A-Bmix*Hss.inv()*Bmix.T)
  assert schur==Hred
  assert len(var)==15 and fullrank==14
  # The bilinears obey exact conjugation-character rules under H27 X and Z.
  # X^-1 W_ab X = omega^b W_ab; Z^-1 W_ab Z = omega^-a W_ab.
  characters={}
  for i,j in modes:
    P=X**i*Z**j
    assert s.simplify(X.T*P*X-w**j*P)==s.zeros(3)
    assert s.simplify(Z.inv()*P*Z-w**(-i)*P)==s.zeros(3)
    characters[f'{i}{j}']={'under_X':int(j),'under_Z':int((-i)%3)}
  return dict(status='PASS_H27_MEDIATOR_LIFTS_FOUR_TRUNCATED_E6_SINGLET_MODULI',
    degree_of_superpotential=3,
    variables={'charged_singlet_u':3,'conjugate_charged_singlet_v':3,'adjoint_cartan_a':1,'E6_neutral_H27_character_mediators':8,'total':15},
    symmetry='External family H27: u transforms as 3D Schrodinger, v as contragredient. B_ab=v^T X^aZ^b u transforms by characters; s_ab carries inverse characters.',
    mediator_modes=[list(t) for t in modes],bilinear_characters=characters,
    superpotential='W=(20/9+4a)sum_i(v_i u_i)+36a^2+sum_(ab!=00)s_ab(v^T X^a Z^b u)+(1/2)sum_(ab!=00)s_ab s_(-a,-b)',
    analytic_root={'u':'(1,0,0)','v':'(1,0,0)','a':'-1/18','s_01':'-1','s_02':'-1','all_other_s':'0'},
    root_F_terms_zero=True,
    root_D_terms_zero='Because v=u* along one E6 U1 weight and adjoint Cartan a is real; all s_ab are E6 singlets. Other E6 D generators vanish on this SO10-singlet ansatz.',
    mediator_Hessian_rank=8,effective_7x7_Hessian_rank=rankred,
    full_15x15_Hessian_rank=fullrank,
    full_15x15_Hessian_nullity=1,
    gauge_complex_zero_mode=[int(v) for v in gauge],
    residual_singlet_moduli_after_gauge_quotient=0,
    exact_reduced_Hessian=[[str(e) for e in Hred.row(i)] for i in range(7)],
    caveat='An isolated *local singlet-sector orbit* of the reduced model. It does not lift the charged SO10 spinor/ten-plet sector, establish a stable full E6 Higgs vacuum, supply three chiral SM families, check radiative corrections or predict mass scales. H27 is an external family group distinct from the subgroup in E6.' )

if __name__=='__main__':
 d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print({k:v for k,v in d.items() if k not in ['bilinear_characters','exact_reduced_Hessian']})
