#!/usr/bin/env python3
"""Pass5071: exact rational matrix bridge behind the shared sqrt(17)."""
from sympy import Matrix, Rational, symbols, factor
x=symbols('x')
A=Matrix([[1,4],[1,0]])
T6=2*A
B2=Matrix([[4,2],[2,5]])
S=Matrix([[1,Rational(1,2)],[0,Rational(1,2)]])
assert A*S == S*(B2-4*Matrix.eye(2))
assert factor(A.charpoly(x).as_expr())==x**2-x-4
assert factor(T6.charpoly(x).as_expr())==x**2-2*x-16
B3model=4*A+10*Matrix.eye(2)
assert factor(B3model.charpoly(x).as_expr())==x**2-24*x+76
print({'A10':A.tolist(),'B2':B2.tolist(),'similarity':S.tolist(),
       'A10_charpoly':str(factor(A.charpoly(x).as_expr())),
       'B3_model_charpoly':str(factor(B3model.charpoly(x).as_expr()))})
