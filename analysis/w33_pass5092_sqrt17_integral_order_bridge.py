#!/usr/bin/env python3
"""Pass5092: integral quadratic-order bridge for the sqrt(17) Hecke/transfer sector."""
from __future__ import annotations
import json
from pathlib import Path
from sympy import Matrix,symbols,factor
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS5092_SQRT17_INTEGRAL_ORDER_BRIDGE.json'
x=symbols('x');I=Matrix.eye(2)
A=Matrix([[1,4],[1,0]])
B2=Matrix([[4,2],[2,5]])
C=B2-4*I
P=Matrix([[2,-1],[-1,1]])
assert P.det()==1 and A*P==P*C
assert factor(A.charpoly(x).as_expr())==x**2-x-4
M3=4*A+10*I
assert factor(M3.charpoly(x).as_expr())==x**2-24*x+76
# lambda=(1+sqrt17)/2 has maximal-order polynomial x^2-x-4, discriminant 17.
# mu=10+4 lambda generates Z+4 O_K, hence conductor/index 4 and discriminant 4^2*17=272.
result={
 'pass':5092,'status':'PASS','A':A.tolist(),'historical_B2':B2.tolist(),'shifted_B2':C.tolist(),
 'integral_similarity_P':P.tolist(),'det_P':int(P.det()),'identity':'A P = P (B2-4I)',
 'A_charpoly':'x^2-x-4','quadratic_field':'Q(sqrt(17))','maximal_order_discriminant':17,
 'q3_affine_block':M3.tolist(),'q3_charpoly':'x^2-24x+76','q3_suborder_index':4,'q3_suborder_discriminant':272,
 'theorem':'The twisted-Hecke quadratic block and the shifted historical B2 block are GL(2,Z)-conjugate, not merely Q-similar. The q3 affine block lies in the conductor-4 suborder of the same quadratic field.',
 'boundary':'This is an integral operator/order bridge. It does not by itself identify the historical transfer carrier geometrically with the apartment-Hecke carrier.'}
OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
