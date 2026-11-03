#!/usr/bin/env python3
"""Pascal -> Gaussian q-Pascal -> symplectic W(3,q), with explicit counterexamples.

Exact integer arithmetic. No numerical pattern fitting or physical-scale claims.
"""
from pathlib import Path
import itertools, math, json
from functools import lru_cache
from fractions import Fraction
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1]
@lru_cache(None)
def gaussian(n,k,q):
    if k<0 or k>n:return 0
    if k==0 or k==n:return 1
    return gaussian(n-1,k-1,q)+q**k*gaussian(n-1,k,q)
def projective_points(q):
    pts={}
    for v in itertools.product(range(q),repeat=4):
        if not any(v):continue
        pivot=next(a for a in v if a)
        inv=pow(pivot,-1,q)
        normalized=tuple((a*inv)%q for a in v)
        pts[normalized]=1
    return tuple(sorted(pts))
def omega(v,w,q):
    return (v[0]*w[2]-v[2]*w[0]+v[1]*w[3]-v[3]*w[1])%q
def symplectic_counts(q):
    P=projective_points(q)
    N=len(P)
    count_edges=sum(omega(P[i],P[j],q)==0 for i in range(N) for j in range(i+1,N))
    I=2*count_edges//(q*(q+1))
    projected=gaussian(4,1,q)
    all_2d=gaussian(4,2,q)
    expected=(q+1)*(q*q+1)
    assert N==projected==expected
    assert count_edges*2==N*q*(q+1)
    assert I==expected
    assert all_2d==(q*q+1)*(q*q+q+1)
    assert all_2d-I==q*q*(q*q+1)
    return {'q':q,'projective_points':N,'Gaussian_4_1':projected,
            'Gaussian_4_2_all_two_spaces':all_2d,
            'symplectic_isotropic_two_spaces':I,
            'nonsymplectic_two_spaces':all_2d-I,
            'symplectic_point_graph_edges':count_edges,
            'isotropic_fraction':str(Fraction(I,all_2d)),
            'all_2space_isotropic_fraction':I/all_2d}
def fibpoly(n,x):
    if n in (0,1):return n
    a,b=0,1
    for _ in range(2,n+1):a,b=b,b+x*a
    return b
def pascal_fibpoly(n,x):
    return sum(math.comb(n-1-k,k)*x**k for k in range((n-1)//2+1))
def constants():
    qprod=[math.prod(math.comb(n,k) for k in range(n+1)) for n in range(27)]
    e_rows=[]
    for n in (2,4,8,16,24):
        p=Fraction(qprod[n+1]*qprod[n-1],qprod[n]**2)
        assert p==Fraction((n+1)**n,n**n)
        e_rows.append({'n':n,'exact_fraction':str(p),'approx':float(p),
                       'error_to_e':abs(float(p)-math.e)})
    phi_rows=[]
    phi=(1+math.sqrt(5))/2
    for n in (5,10,20,30):
        F=sum(math.comb(n-k,k) for k in range(n//2+1))
        Fp=sum(math.comb(n+1-k,k) for k in range((n+1)//2+1))
        ratio=Fp/F
        phi_rows.append({'n':n,'fibonacci_ratio':ratio,'error_to_phi':abs(ratio-phi)})
    # Exact sum via 1/T_n^2=4/n^2+4/(n+1)^2-8/(n(n+1)).
    # This is 4 pi^2/3 - 12, NOT 4 pi^2/3 - 6.
    mp.mp.dps=50
    total=mp.nsum(lambda k: 4/(k*k*(k+1)*(k+1)),[1,mp.inf])
    pi_expr=4*mp.pi**2/3-12
    assert abs(total-pi_expr)<mp.mpf('1e-42')
    # Triangular reciprocal alternating series from Howard paper:
    # 2 + [+1,+1,-1,-1,...]/T_{n-1}, n>=2.
    signs=[1 if (k//2)%2==0 else -1 for k in range(12)]
    # Its first entries 1,1/3,-1/6,-1/10,+1/15, +1/21 ...
    assert signs[:6]==[1,1,-1,-1,1,1]
    # Existence of a CONTINUUM of positive shallow-diagonal growth constants:
    # characteristic lambda^2-lambda-x=0 for F_{n}=F_{n-1}+xF_{n-2}.
    transfer=[]
    for x in (Fraction(1,4),Fraction(1,2),Fraction(1),Fraction(2),Fraction(3)):
        for n in range(2,12):
            assert fibpoly(n,x)==pascal_fibpoly(n,x)
        rho=(1+math.sqrt(1+4*float(x)))/2
        approx=float(fibpoly(32,x)/fibpoly(31,x))
        transfer.append({'diagonal_weight_x':str(x),
                         'analytic_Perron_root':rho,'ratio_n32_to_n31':approx,
                         'abs_error':abs(rho-approx)})
    return {'Euler_row_product_cross_ratios':e_rows,
            'phi_Fibonacci_diagonal_ratios':phi_rows,
            'triangular_inverse_square_sum':str(total),
            'triangular_inverse_square_exact_formula':'4*pi**2/3 -12',
            'Howard_Toloza_pi_alternating_first_signs':signs,
            'weighted_fibonacci_generalization':transfer}
def main():
    rows=[symplectic_counts(q) for q in (2,3,5,7)]
    assert rows[1]['projective_points']==40
    assert rows[1]['Gaussian_4_2_all_two_spaces']==130
    assert rows[1]['symplectic_isotropic_two_spaces']==40
    c=constants()
    out={'status':'PASS_EXACT_Q_PASCAL_W33_SYMPLECTIC_SELECTOR_AND_CONSTANT_NONUNIQUENESS',
         'projective_and_symplectic_rows':rows,
         'constants':c,
         'q_pascal_rule':'[n k]_q=[n-1 k-1]_q+q^k [n-1 k]_q, and as q->1 this is ordinary Pascal.',
         'mathematical_geometry':'Gaussian [4 1]_q counts projective points of F_q^4; Gaussian [4 2]_q counts 2-subspaces. A supplied nondegenerate alternating 2-form selects exactly (q+1)(q²+1) isotropic 2-spaces, defining the lines of W(3,q). At q=3 the count is 40 of 130 total, with 90 excluded. This does not determine q=3 uniquely.',
         'physical_boundary':'Generalized Pascal constructs combinatorial dimensions and algebraic Perron growth constants, but no unique dimensional conversion. The weighted recurrence F_n(x)=F_(n-1)(x)+x F_(n-2)(x) yields a continuum of Perron roots, phi only for x=1; Pi and Euler e arise under distinct extraction limits. Infinite countable patterns generate many constants, not a physical choice of which are fundamental.',
         'legacy_repo':'PART_DCCL_PASCAL_SYNERGETICS_CLIFFORD_HIERARCHY.md; PART_DCCLI_PASCAL_DIAGONAL_W33_GENERATOR.md; w33_BREAKTHROUGH_435_pascal_trinity_triangular.py. Already known numeric matches are attributed to these files, not new.',
         'sources':['https://pressbooks.howardcc.edu/jrip1/chapter/fee-fi-fo-fum-deriving-e-latex-theta%CE%B8-and-latex-pi%CF%80-from-pascals-triangle/',
                    'https://oeis.org/A022167','https://mathworld.wolfram.com/PascalsTriangle.html']}
    path=ROOT/'data/toe_20261103_q_pascal_symplectic_scale_selector.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print('Q_PASCAL',json.dumps({'q':rows,'e':c['Euler_row_product_cross_ratios'],
           'weighted_growth':c['weighted_fibonacci_generalization'],'pi':c['triangular_inverse_square_sum']})[:9000],flush=True)
if __name__=='__main__':main()
