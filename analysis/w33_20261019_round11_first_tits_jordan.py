"""Exact first Tits construction of the split Albert algebra in 27=3*M3 coordinates.

This is a nontrivial constructive bridge to the E6 cubic, NOT an
explicit 27x27 map to a selected Cayley-Dickson octonion basis.
Reference: general first Tits construction for M3(F), mu=1.
"""
from __future__ import annotations
import json, random
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round11_first_tits_jordan.json"
def N(x):
    A,B,C=x
    return A.det()+B.det()+C.det()-sp.trace(A*B*C)
def sharp(x):
    A,B,C=x
    return (A.adjugate()-B*C,C.adjugate()-A*B,B.adjugate()-C*A)
def pairing(x,y):
    A,B,C=x;D,E,F=y
    return sp.trace(A*D+B*F+C*E)
def polarization(x,y):
    # exact degree-three coefficient of N(x+t*y)
    t=sp.symbols("t")
    z=tuple(A+t*B for A,B in zip(x,y))
    return sp.Poly(sp.expand(N(z)),t).coeff_monomial(t)
def sample(rng):
    return tuple(sp.Matrix(3,3,[rng.randint(-2,2) for _ in range(9)]) for _ in range(3))
def run():
    rng=random.Random(110319)
    checksums=[]
    maxdigits=0
    for _ in range(40):
        x=sample(rng);y=sample(rng)
        q=sharp(x)
        qq=sharp(q)
        assert all(qqi==N(x)*xi for qqi,xi in zip(qq,x))
        assert pairing(q,y)==polarization(x,y)
        maxdigits=max(maxdigits,len(str(abs(int(N(x))))))
        checksums.append(int(N(x)))
    e=(sp.eye(3),sp.zeros(3),sp.zeros(3))
    assert N(e)==1
    assert all(a==b for a,b in zip(sharp(e),e))
    # A determinant×3 term and the 27 mixed ABC monomials survive.
    a=sp.symbols("a0:9");b=sp.symbols("b0:9");c=sp.symbols("c0:9")
    A=sp.Matrix(3,3,a);B=sp.Matrix(3,3,b);C=sp.Matrix(3,3,c)
    poly=sp.Poly(sp.expand(N((A,B,C))),*(a+b+c))
    assert len(poly.terms())==45
    # The standard Tits cubic's group of norm-preserving linear
    # transformations is the split simply connected E6 (up to center);
    # a known classical theorem, not proved by 40 random evaluations.
    checks={"first_tits_cubic_45_monomials":len(poly.terms())==45,
        "adjoint_of_adjoint_identity_exact_40_instances":len(checksums)==40,
        "adjoint_is_trace_pairing_gradient_exact_40_instances":True,
        "unit_norm_and_selfadjoint":N(e)==1}
    out={"schema":"w33.round11.first_tits_split_albert_exact.v1",
        "theorem":"The 27 complex components of three 3x3 matrices (A,B,C) carry the FIRST TITS construction J(M3(C),mu=1) cubic N=det A+det B+det C-Tr(ABC), with unit (I3,0,0), trace pairing T((A,B,C),(D,E,F))=Tr(AD+BF+CE), quadratic adjoint #(A,B,C)=(adj A-BC,adj C-AB,adj B-CA), and defining cubic Jordan identity (x#)#=N(x)x. Exact integer matrix arithmetic verifies the adjoint identity and polarized-gradient formula on 40 reproducible random samples, and exact symbolic coefficient expansion finds 45 cubic monomials.",
        "N_unit":str(N(e)),"monomial_count":len(poly.terms()),
        "samples_exact_integer":len(checksums),
        "sample_norms_first_12":checksums[:12],
        "max_norm_decimal_digits":maxdigits,
        "critical_scope":"This provides an EXACT constructive 27D cubic Jordan model in the SAME SU3^3 coordinates as the E6 trinification. It is not a dense 27x27 coordinate intertwiner to the specific 3+8+8+8 Cayley-Dickson chart; deriving such a matrix and matching clock action is still OPEN. The fact the first Tits construction gives an Albert algebra is established prior art (not new).",
        "source":"https://www.mdpi.com/2075-1680/13/5/299 section 2.4 first Tits construction, cubic N and quadratic sharp.",
        "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"monomials":len(poly.terms()),"sample_N":checksums[:4]},indent=2))
    return out
if __name__=="__main__":run()
