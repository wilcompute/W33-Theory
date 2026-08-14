#!/usr/bin/env python3
from sympy import Matrix,symbols,factor
x=symbols('x');I=Matrix.eye(2)
A=Matrix([[1,4],[1,0]]);B2=Matrix([[4,2],[2,5]]);P=Matrix([[2,-1],[-1,1]])
assert P.det()==1 and A*P==P*(B2-4*I)
assert factor(A.charpoly(x).as_expr())==x**2-x-4
M3=4*A+10*I
assert factor(M3.charpoly(x).as_expr())==x**2-24*x+76
print({'detP':1,'disc_OK':17,'q3_conductor':4,'q3_disc':272})
