"""Exact minimal polynomial range for common quadratic cone in Levi model."""
import sympy as sp
z=sp.Symbol("z")
q=sp.Rational(1,4)-z/sp.Integer(10)+z*z/sp.Integer(40)
assert sp.rem(sp.expand((4+z)*q-1),z**3-6*z,z)==0
a,b=sp.symbols("a b")
assert sp.solve([a+4*b,b],[a,b])=={a:0,b:0}
r=sp.sqrt((4+sp.sqrt(6))/(4-sp.sqrt(6)))
def certificate():
    return dict(status="PASS",degree_one_nonzero_solutions=0,
                minimal_degree=2,
                inverse_polynomial="I/4-A/10+A^2/40",
                naive_speed_ratio=float(r),
                scope="Only polynomial-in-Levi-adjacency quadratic spring class")
if __name__=="__main__":
    print(certificate())
