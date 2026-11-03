#!/usr/bin/env python3
"""Hyperbolic sigma-model isometry vs fading dark-matter mass: exact Ward test.

Units Mpl=1. Physical canonical chi mass is sqrt(U_yy/g_yy).
Our result is restricted to a two-field quadratic chi potential and one Killing
translation/rescaling; does not exclude noncompact modulus or spurion UV models.
"""
from pathlib import Path
import sympy as S,json
ROOT=Path(__file__).resolve().parents[1]
def main():
 x,y,b,g,l,m,V0,a=S.symbols('x y beta gamma lam m V0 a',real=True)
 E=S.exp(-2*b*x)
 metric=S.diag(1,E)
 fields=(x,y);K=S.Matrix([1,b*y])
 # Direct Lie-derivative Killing equation.
 Lie=S.Matrix(2,2,lambda i,j:S.simplify(sum(K[k]*S.diff(metric[i,j],fields[k])+
 metric[k,j]*S.diff(K[k],fields[i])+metric[i,k]*S.diff(K[k],fields[j]) for k in range(2))))
 assert Lie==S.zeros(2)
 # 2D Gaussian curvature for ds²=dx²+f(x)² dy² has R=-2 f''/f.
 f=S.exp(-b*x)
 R=S.simplify(-2*S.diff(f,x,2)/f)
 assert R==-2*b*b
 mass2=m*m*S.exp(-2*g*x)
 potential_chi=S.Rational(1,2)*E*mass2*y*y
 V=V0*S.exp(-l*x)
 def directional(U):return S.simplify(S.diff(U,x)*K[0]+S.diff(U,y)*K[1])
 dk_chi=S.simplify(directional(potential_chi))
 dk_V=S.simplify(directional(V))
 assert S.simplify(dk_chi+2*g*potential_chi)==0
 assert S.simplify(dk_V+l*V)==0
 # Pullback under finite isometry x->x+a, y->e^(beta*a)y.
 g_pull=S.simplify(E.subs(x,x+a)*S.exp(2*b*a)/E)
 U_pull=S.simplify((potential_chi.subs({x:x+a,y:y*S.exp(b*a)}))/potential_chi)
 V_pull=S.simplify(V.subs(x,x+a)/V)
 assert g_pull==1
 assert U_pull==S.exp(-2*g*a)
 assert V_pull==S.exp(-l*a)
 # Worldline homogeneous orbit: shift symmetry can't set a non-zero gamma.
 canonical_mass=S.simplify(S.sqrt(S.diff(potential_chi,y,2)/E))
 assert S.simplify(S.diff(S.log(canonical_mass),x)+g)==0
 # kinetic-only isometry and potential breaking both are exact.
 out={'status':'PASS_EXACT_HYPERBOLIC_ISOMETRY_FADING_MASS_WARD_NO_GO',
  'model':'Metric ds^2=dx^2+exp(-2 beta x)dy^2, K=(1,beta*y), Uchi=(m0^2/2) exp[-2(beta+gamma)x] y^2, V(x)=V0 exp(-lam x). x=phi/Mpl and y=chi/Mpl; metric factors are dimensionless.',
  'symbolic_Lie_K_metric':[[str(Lie[i,j]) for j in range(2)] for i in range(2)],
  'exact_scalar_curvature_over_1_over_Mpl_squared':str(R),
  'finite_isometry_pulledback_metric_ratio':str(g_pull),
  'finite_isometry_dark_mass_potential_ratio':str(U_pull),
  'finite_isometry_rolling_potential_ratio':str(V_pull),
  'canonically_normalized_dark_mass_squared':str(mass2),
  'K_derivative_of_dark_potential':str(dk_chi),
  'K_derivative_of_rolling_potential':str(dk_V),
  'theorem':'Within the declared exact two-field hyperbolic sigma model, K is Killing. Global shift+rescaling invariance of BOTH Uchi and V for arbitrary a and generic nonzero fields requires gamma=0 and lambda=0 (or absent corresponding terms). Exact isometry protects constant canonical DM mass, not fading canonical DM mass or a rolling exponential potential. Realizing both with nonzero slopes requires explicitly broken/spurionic isometry, additional fields, an unconventional realization, or noncompact modulus with no such exact protection.',
  'non_claims':'Not a proof that all shift-symmetric or SUSY/monodromy models fail. The metric has constant negative field-space curvature, known in sigma models and alpha-attractors. No gravity quantization, UV completion or coupling to SM fermions constructed.',
  'physical_hypothesis_bridge':'If the TOE invokes one field-space isometry as a universal protection mechanism, the same symmetry imposes Ward identities on dark mass and rolling potential. This supplies a precise falsification criterion without matching arbitrary graph counts.',
  'background_prior':'Earlier repository compact axion exact exponential obstruction and local SUSY portal; this separate hyperbolic isometry Ward identity is not asserted to supersede or prove prior speculative unification.'}
 p=ROOT/'data/toe_20261103_hyperbolic_isometry_ward.json'
 p.write_text(json.dumps(out,indent=2)+'\n')
 print('HYPERBOLIC_WARD',json.dumps({'R':str(R),'dark_shift':str(U_pull),'V_shift':str(V_pull)}))
if __name__=='__main__':main()
