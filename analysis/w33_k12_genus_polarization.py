"""Exact K12 lattice polarization bridge to the genus-oscillator corpus.
Prior: Holotrade a0ed473/b63daac; W33 BT802, BT1844, DCCXXIII.
No equality of graph K_12 and Coxeter-Todd lattice K_12 is assumed.
"""
from pathlib import Path
from math import isqrt, comb
import json
import sympy as s
from sympy.matrices.normalforms import hermite_normal_form, smith_normal_form
from sympy.polys.domains import ZZ
from w33_coxeter_todd_oriented_observer import mul

GAUSSIAN = [[-1, 0, 0, 1, 0, 0, -1, 1, 0, 0, 0, 0], [-1, 1, 1, 0, 0, 0, 0, 1, 0, 1, -1, 1], [-1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [-2, 1, 0, 0, 0, 0, -1, 1, -1, 1, -1, 0], [-2, 1, 0, 1, 0, 1, -1, 2, 0, 1, 0, 1], [-1, 1, 0, 1, -1, 1, -1, 2, 0, 1, 0, 0], [1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, -1, -1, 1, 0, 0, 0, 0, 1, -1, 1, 0], [0, 0, 1, -1, 1, 0, 1, -1, 0, 1, 0, 1], [0, 0, 0, -1, 1, -1, 0, -1, -1, 0, 0, 0], [1, 0, 0, 0, 0, -1, 1, -1, 0, -1, 0, 0], [1, -1, 0, 0, -1, 0, 0, -1, 0, -1, 0, -1]]

def integral(M):
    assert all(x.q == 1 for x in M)
    return [[int(x) for x in row] for row in M.tolist()]

def minimal_surface(g):
    n = (7 + isqrt(1 + 48*g)) // 2
    while (2*n-7)**2 < 1+48*g:
        n += 1
    if g == 2:
        n = 10
    return [n, 3*n+6*g-6, 2*n+4*g-4]

def darboux(E):
    cols = [s.eye(E.rows)[:,i] for i in range(E.rows)]
    pairs = []
    while cols:
        i,j = next((i,j) for i in range(len(cols)) for j in range(i+1,len(cols))
                   if abs((cols[i].T*E*cols[j])[0]) == 1)
        a = cols[i]; b = cols[j]*(a.T*E*cols[j])[0]
        rest = [c for k,c in enumerate(cols) if k not in (i,j)]
        cols = [c+(b.T*E*c)[0]*a-(a.T*E*c)[0]*b for c in rest]
        pairs.extend([a,b])
    return s.Matrix.hstack(*pairs)

def audit():
    prior = json.loads(Path(__file__).with_name('w33_coxeter_todd_oriented_observer.json').read_text())
    columns = [[a for z in v for a in mul(u,z)]
               for v in prior['reflection_lines_eisenstein'] for u in [(1,0),(0,1)]]
    B = hermite_normal_form(s.Matrix(columns).T)
    Q = s.diag(*([s.Matrix([[1,s.Rational(-1,2)],[s.Rational(-1,2),1]])]*6))
    O = s.diag(*([s.Matrix([[0,1],[-1,0]])]*6))
    W0 = s.diag(*([s.Matrix([[0,-1],[1,-1]])]*6))
    G = B.T*Q*B
    E = B.T*O*B/2
    W = B.inv()*W0*B
    integral(G); integral(E); integral(W)
    assert B.det() == 64 and G.det() == 729 and E.det() == 1
    assert E.T == -E and W**2+W+s.eye(12) == s.zeros(12)
    assert W.T*G*W == G and W.T*E*W == E
    Jnum = 2*W+s.eye(12)  # J = Jnum/sqrt(3)
    assert Jnum**2 == -3*s.eye(12)
    assert G*Jnum == -3*E and E*Jnum == G
    assert G.is_positive_definite  # E J = G/sqrt(3), the Riemann positivity condition
    T = darboux(E)
    assert T.det() == 1 and T.T*E*T == O
    # Recovered independently; Holotrade b63daac owns the antilinear Gaussian structure.
    I = s.Matrix(GAUSSIAN)
    assert I**2 == -s.eye(12) and I.T*G*I == G and abs(I.det()) == 1
    assert I*W == W**2*I and I.T*E*I == -E
    D = -G*I  # D I = G > 0, an integral Gaussian Riemann form
    assert D.T == -D and I.T*D*I == D and D*I == G
    smith = [abs(int(x)) for x in smith_normal_form(D,domain=ZZ).diagonal()]
    assert smith == [1]*6+[3]*6
    # Genus ladders: exact arithmetic with the genus-two JR exception.
    rows = []
    for g in range(13):
        linear = [4+3*g,6+15*g,4+10*g]
        minimum = minimal_surface(g)
        assert linear[0]-linear[1]+linear[2] == 2-2*g
        assert comb(linear[0],2)-linear[1] == 9*g*(g-1)//2
        rows.append({'genus':g,'JR_minimum':minimum,'linear_oscillator':linear,
                     'linear_is_minimal':linear==minimum})
    assert [r['genus'] for r in rows if r['linear_is_minimal']] == [0,1,2]
    assert minimal_surface(6) == [12,66,44]
    # Incidence owns the spectrum; a mechanical oscillator uses square-root frequencies.
    Fano = [(0,1,3),(0,2,5),(0,4,6),(1,2,4),(1,5,6),(2,3,6),(3,4,5)]
    F = s.zeros(7)
    for j,L in enumerate(Fano):
        for i in L: F[i,j] = 1
    A = s.BlockMatrix([[s.zeros(7),F],[F.T,s.zeros(7)]]).as_explicit()
    P = (9*s.eye(14)-A*A)/7
    assert F*F.T == 2*s.eye(7)+s.ones(7)
    assert P*P == P and s.trace(P) == 12 and (P*A)**2 == 2*P
    return {'status':'PASS','schema':'w33.k12-genus-polarization.v1',
            'lattice_basis':integral(B),'real_gram':integral(G),
            'eisenstein_alternating_form':integral(E),'eisenstein_unit':integral(W),
            'darboux_basis':integral(T),'lattice_index':64,'real_gram_determinant':729,
            'principal_polarization_determinant':1,
            'complex_structure':'J=(2W+I)/sqrt(3); E*J=G/sqrt(3)',
            'gaussian_complex_structure':integral(I),'gaussian_alternating_form':integral(D),
            'gaussian_polarization_type':[1,1,1,3,3,3],
            'gaussian_is_antisymplectic_for_eisenstein_form':True,
            'genus_ladders':rows,
            'neighborly_surface_rungs':[[n,(n-3)*(n-4)//12] for n in range(4,41) if (n-3)*(n-4)%12==0],
            'JR_handle_subtraction_delta':[0,-6,-4],
            'heawood_centered_middle_square':'(P*A)^2=2P, rank P=12',
            'mechanical_middle_frequencies':'sqrt(3-sqrt(2)), sqrt(3+sqrt(2)), for unit masses and stiffness L',
            'jacobian_obstruction':{'status':'theorem using strong Torelli and the canonical map',
                'scope':'natural Eisenstein complex structure with the specified principal polarization',
                'reason':'scalar order-three action on holomorphic differentials cannot come from a smooth curve of genus at least two'},
            'boundary':'Integral symplectic module bridge, not a triangulation map or physical oscillator realization. Other complex structures and polarizations require separate tests.'}

if __name__ == '__main__':
    import sys
    result = audit()
    if '--write' in sys.argv:
        Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','real_gram_determinant','principal_polarization_determinant','gaussian_polarization_type','jacobian_obstruction']},indent=2))
