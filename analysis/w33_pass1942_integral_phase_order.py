#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/w33_pass1942_integral_phase_order.json'
I=sp.eye(3);R4=sp.Matrix([[0,-1,0],[1,0,0],[0,0,1]]);U6=sp.Matrix([[1,0,0],[0,0,1],[0,-1,1]])
words={'':I};front={'':I}
for _ in range(4):
 new={}
 for name,M in front.items():
  for ch,G in [('r',R4),('u',U6)]:
   N=M*G;key=tuple(N)
   if all(tuple(X)!=key for X in words.values()):words[name+ch]=N;new[name+ch]=N
 front=new
vec=lambda M:sp.Matrix(9,1,list(M));V=sp.Matrix.hstack(*[vec(M) for M in words.values()]);H=hermite_normal_form(V);P=R4*U6
x=sp.symbols('x0:9');X=sp.Matrix(3,3,x);sol=sp.linsolve([z for M in (X*R4-R4*X,X*U6-U6*X) for z in M],x)
E=[]
for i in range(3):
 for j in range(3):
  M=sp.zeros(3);M[i,j]=1;E.append(M)
T=sp.Matrix([[sp.trace(a*b) for b in E] for a in E]);l=sp.Symbol('lambda')
checks={'R4_order4':R4**4==I and R4**2!=I,'U6_order6':U6**6==I and U6**3!=I,'R4_charpoly':sp.factor(R4.charpoly().as_expr())==(l-1)*(l**2+1),'U6_charpoly':sp.factor(U6.charpoly().as_expr())==(l-1)*(l**2-l+1),'word_lattice_rank9':V.rank()==9,'hermite_identity':H==sp.eye(9),'trace_discriminant_unit':abs(int(T.det()))==1,'product_infinite_order':sp.factor(P.charpoly().as_expr())==l**3-l**2-1,'centralizer_scalar':str(sol)=='{(x8, 0, 0, 0, x8, 0, 0, 0, x8)}'}
out={'schema':'w33.pass1942.integral_phase_order.v1','status':'PASS','checks':checks,'multiplicity_basis':['A=natural V9 in 24','B=natural V9 in 90','C=sign-twisted V9 in 90'],'generators':{'R4_AB':[[int(z) for z in row] for row in R4.tolist()],'description_R4':'The exceptional-S6 paired Gaussian quarter-turn on A+B, identity on C.','U6_BC':[[int(z) for z in row] for row in U6.tolist()],'description_U6':'The Eisenstein unit -omega on B+C, identity on A; its BC characteristic polynomial is t^2-t+1.'},'associative_order':{'rational_algebra':'M3(Q)','integral_order':'M3(Z)','rank':9,'index_in_M3Z':1,'trace_discriminant_abs':1,'center':'Z','commutant':'Z'},'word_certificate':{'distinct_words_through_length4':len(words),'hermite_normal_form':'I9','word_labels':list(words)},'unit_group_behavior':{'generated_group':'infinite','witness':'R4*U6 has characteristic polynomial t^3-t^2-1','spectral_radius_gt_1':True},'no_quaternionic_enhancement':'The two adjacent integral phase units do not generate a quaternion order or a finite SU(2) image. Their unital associative order saturates M3(Z), and their common commutant is only the scalars.','relation_to_real_so3':'The infinitesimal adjacent-plane rotations generate so(3) over R, but the integral C4 and C6 units generate a much larger noncommutative arithmetic object: the full matrix order M3(Z).','phase_interpretation':'The sixfold Eisenstein phase lives on B+C, whereas the paired carrier quarter-turn lives on A+B. Their overlap at B is exactly what forces full matrix saturation.','theorem':'On the saturated A6 multiplicity lattice of the three V9 copies, the Gaussian C4 unit on A+B and Eisenstein C6 unit on B+C generate the full integral order M3(Z). The generated unit group is infinite and the commutant is scalar, ruling out a quaternionic or finite SU(2) enhancement.','boundary':'This is the integral multiplicity-order theorem. It does not identify the infinite arithmetic unit group with a physical gauge group.'}
assert all(checks.values()),{k:v for k,v in checks.items() if not v};x0=dict(out);out['sha256_without_hash_field']=hashlib.sha256(json.dumps(x0,sort_keys=True,separators=(',',':')).encode()).hexdigest();OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'status':out['status'],'sha':out['sha256_without_hash_field'],'checks':checks,'order':out['associative_order']},indent=2))
