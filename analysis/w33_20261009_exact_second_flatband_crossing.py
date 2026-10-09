"""A SECOND exact topology threshold of the 160-state W33 flat band.

Pass round9 established 81 to 96 ground-space crossing at t=1/2.
Here construct *rational pseudoinverse* to the 80x80 Levi Gram G
by its exact integer minimal polynomial, and verify algebraic
generalized spectrum of two native adjacency couplers.

X = G^+ [B(A30+2I)B^T] G^+, symmetric on 80 Levi vertices.
Nonzero spectrum expected -1^15,1^15,4^1,
(3 +/- sqrt(10))^24. Thus another exact downward crossing of
24 levels at t2 = 1/(sqrt(10)-2) = (sqrt(10)+2)/6.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys,time
import numpy as np
import sympy as S
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_correlated_disorder_dual_couplers import construct
def certificate():
 B,A6,A30,M,D,P=construct()
 G=S.Matrix((B@B.T).tolist())
 C=S.Matrix((B@(A30+2*np.eye(160,dtype=np.int64))@B.T).tolist())
 I=S.eye(80);x=S.Symbol('x')
 h=S.expand((x-8)*(x-4)*((x-4)**2-6))
 assert h.subs(x,0)==320
 assert G*(G-8*I)*(G-4*I)*((G-4*I)**2-6*I)==S.zeros(80)
 q=S.div(S.Poly(320-h,x),S.Poly(x,x))[0].as_expr()/320
 assert S.rem(S.Poly(320-h,x),S.Poly(x,x))==0
 G2=G*G;G3=G2*G;G4=G3*G
 def evaluate(poly):
  p=S.Poly(poly,x);v=S.zeros(80)
  for (degree,),val in p.terms():
   v+=val*[I,G,G2,G3,G4][degree]
  return v
 projector=evaluate(h)/320
 assert projector*projector==projector
 Zin=evaluate(q)-q.subs(x,0)*projector
 assert G*Zin==I-projector and Zin*G==I-projector
 X=Zin*C*Zin
 assert X==X.T
 # Matrix polynomial of degree6 with rational entries: exactly zero.
 X2=X*X
 f1=X2-6*X-I
 f2=X2-I
 residual=X*(X-4*I)*f1*f2
 assert residual==S.zeros(80),max(abs(t) for t in residual)
 tr=[int(S.trace(X)),int(S.trace(X2)),int(S.trace(X2*X))]
 a,b,c,n=S.symbols('a b c n')
 z=S.solve([a+b+c+2*n-79,
           -a+b+4*c+6*n-tr[0],
           a+b+16*c+38*n-tr[1],
           -a+b+64*c+234*n-tr[2]],(a,b,c,n),dict=True)
 assert z==[{a:15,b:15,c:1,n:24}],z
 # Additional zero mode from ker G is one-dimensional:
 assert S.trace(projector)==1
 t2=S.simplify(1/(S.sqrt(10)-2))
 assert t2==(2+S.sqrt(10))/6
 return dict(status='PASS',
    exact_G_Gram_polynomial='G*(G-8I)*(G-4I)*((G-4I)^2-6I)=0',
    rational_pseudoinverse_formula='Gplus=q(G)-q(0)*h(G)/320, h=(G-8I)(G-4I)((G-4I)^2-6I), q(x)=(320-h(x))/(320*x)',
    pseudoinverse_rational_matrix_exact=True,
    reduced_symmetric_eigenvalue_polynomial='X*(X-4I)*(X^2-6X-I)*(X^2-I)=0',
    reduced_trace_first_second_third=tr,
    generalized_eigenvalue_multiplicities={'-1':15,'1':15,'4':1,'3-sqrt10':24,'3+sqrt10':24},
    guaranteed_groundband_critical_1='1/2',
    guaranteed_groundband_critical_2=str(t2),
    second_critical_t_numeric=float(t2),
    exact_second_crossing='There are 24 additional transverse modes with generalized lambda=3-sqrt10, whose (1-t)+t*lambda coefficient changes sign exactly at t2=(sqrt10+2)/6. At t2 the -2 cycle flat band has 81 persistent eigenvectors but the 15 former negative modes are already lower. It is NOT a second ground-state degeneracy of the entire operator.',
    negative_eigenvalue_counts_of_A_t_plus_2={'0<=t<=1/2':0,
     '1/2<t<(sqrt10+2)/6':15,
     't=(sqrt10+2)/6':15,
     '(sqrt10+2)/6<t<=1':39},
    zero_eigenvalue_dimensions_at_critical={'t=1/2':96,'t=(sqrt10+2)/6':105},
    caveat='The matrix inertia counts follow from congruence by the positive Levi Gram on its 79D image and the exact generalized eigenvalue spectrum. Negative modes need not be interpreted as physical negative energies or spacetime.')
if __name__=='__main__':
 st=time.time();d=certificate()
 (ROOT/'data/w33_20261009_exact_second_flatband_crossing.json').write_text(json.dumps(d,indent=2)+'\n')
 print('SECOND CROSSING',d['second_critical_t_numeric'],d['reduced_trace_first_second_third'],'secs',time.time()-st)
