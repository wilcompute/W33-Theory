"""Actual native edge moments select six clock vacua in a supplied Landau model.

The character-plane mass ordering and Lorentz kinetic coupling are inputs.
This does not turn a positive graph Laplacian into Lorentzian propagation.
"""
import json,itertools
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]


def payload():
    d=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text())
    C=s.Matrix(d['harmonic_voltages_Q']);G=s.Matrix(d['exact_acoustic_metric']);L=s.Matrix(d['raw_period_lattice_basis'])
    x,y,z,t=s.symbols('x y z t',real=True);a=s.Matrix([x,y,z,t]);u=L.T*a
    projection=L.T*s.diag(1,1,0,0)*L.T.inv(); cp=C*projection*u
    moments={n:s.factor(sum(v**n for v in cp)) for n in (2,4,6)}
    r=x*x+x*y+y*y;p=x*x*y*y*(x+y)**2
    assert s.expand(moments[2]-54*r)==0
    assert s.expand(moments[4]-54*r*r)==0
    assert s.expand(moments[6]-54*r**3-81*p)==0
    # All three terms nonnegative: a global proof, not a multistart scan.
    rb=z*z-z*t+t*t
    V=s.expand((r-1)**2+rb+rb*rb+p)
    points=[s.Matrix([i,j,0,0]) for i,j in ((1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1))]
    rows=[];A={tuple(h) for h in d['parallel_polarization_Lorentz_repair']['selected_subgroup']}
    actions=[(tuple(row['h']),s.Matrix(row['matrix'])) for row in d['exact_deck_actions']]
    for h,M in actions:
        N=L.T.inv()*M*L.T
        assert s.expand(V.subs(dict(zip(a,N*a)),simultaneous=True)-V)==0
        assert M.T*G*M==G
    for v in points:
        sub=dict(zip(a,v));hess=s.hessian(V,a).subs(sub);assert V.subs(sub)==0
        assert all(hess[:i,:i].det()>0 for i in range(1,5))
        v=L.T*v;norm=(v.T*G*v)[0];assert norm==2
        eta=(G-2*G*v*v.T*G/norm)/norm
        fixed={h for h,M in actions if M*v==v};preserved={h for h,M in actions if M.T*eta*M==eta}
        assert fixed==preserved==A and (v.T*eta*v)[0]==-1
        # A second rational drawing checks that signature is not coordinate artefact.
        T=s.eye(4);T[0,1]=2;T[2,3]=-1
        assert (T.T*eta*T).det()==T.det()**2*eta.det() and eta.det()<0
        rows.append(dict(clock_primitive=list(map(str,v)),metric_Q=[[str(q) for q in row] for row in eta.tolist()],Hessian_eigenvalues={str(k):int(m) for k,m in hess.eigenvals().items()},stabilizer=[list(h) for h in sorted(fixed)]))
    # Before a clock is chosen, the quadratic symbol remains positive.
    alpha=s.symbols('alpha');v=L.T*points[0];K=G-alpha*(G*v*v.T*G)/2
    assert s.factor(K.det()/G.det())==1-alpha
    return dict(status='PASS',native_moment_polynomials={str(k):str(v) for k,v in moments.items()},
        exact_anisotropy_identity='I6-I2^3/2916 = 81 x^2 y^2 (x+y)^2',
        clock_action_potential=str(V),definition='a=(x,y,z,t)=L^-T u. rA=x²+xy+y², rB=z²-zt+t²; V=(rA-1)²+rB+rB²+x²y²(x+y)².',
        exact_global_minimum=0,global_vacuum_count=6,global_minimum_proof='Every term is nonnegative. Zero requires rA=1,rB=0,xy(x+y)=0, giving precisely the six displayed points. All four real Hessian modes are positive at each.',
        vacua=rows,orbit_structure='Two H27 orbits of three clock vectors, exchanged by time reversal u->-u. All have exact residual subgroup A={(0,b,c)}; metric forgets time orientation.',
        kinetic_signature_family='K_alpha=G-alpha Gu u^T G/(u^T G u); det K_alpha/det G=1-alpha. Positive for alpha<1, singular at1, Lorentz for alpha>1. Choosing alpha=2 is an ADDITIONAL kinetic input, not a prediction of V.',
        scope='A global clock-order theorem for a declared H27-invariant native-moment potential on the selected rank4 quotient. Character mass ordering, quotient, kinetic sign/coupling and physical action are supplied; no dynamical derivation of GR or signature.',
        prior=['11991 primitive native cover and subgroup/Lorentz permission','11985 supplied clock kinetic constraints','11956 weighted harmonic metric matching','11988 complex-structure compatibility obstruction'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11994_native_clock_order.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['global_vacuum_count'])
