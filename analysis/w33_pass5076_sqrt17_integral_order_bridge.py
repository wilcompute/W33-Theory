#!/usr/bin/env python3
"""Pass5076: integral quadratic-order bridge for the sqrt(17) sector."""
from sympy import Matrix,symbols,factor
x=symbols('x');I=Matrix.eye(2)
A=Matrix([[1,4],[1,0]])
B2=Matrix([[4,2],[2,5]])
C=B2-4*I
P=Matrix([[2,-1],[-1,1]])
assert P.det()==1 and A*P==P*C
assert factor(A.charpoly(x).as_expr())==x**2-x-4
M3=4*A+10*I
assert factor(M3.charpoly(x).as_expr())==x**2-24*x+76
# lambda=(1+sqrt(17))/2 generates the maximal quadratic order because 17 is fundamental.
# mu=10+4 lambda generates Z+4 O_K, index/conductor 4, hence discriminant 4^2*17=272.
print({'A':A.tolist(),'B2':B2.tolist(),'P':P.tolist(),'detP':int(P.det()),
       'A_charpoly':str(factor(A.charpoly(x).as_expr())),
       'M3_charpoly':str(factor(M3.charpoly(x).as_expr())),
       'maximal_order_discriminant':17,'q3_suborder_index':4,'q3_suborder_discriminant':272})
