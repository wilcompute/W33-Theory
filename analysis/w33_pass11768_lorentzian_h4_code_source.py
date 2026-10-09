"""Lorentzian metric on the new native H4 slab; a declared ADM/code-source model.

Prior Oct8 native_H4_4D_spacetime_slab owns all2400 staircase simplices;
native_H4_Regge_S3 owns spatial curvature;20apt_exact_thermal_spectrum
owns the CSS energies. Product Lorentzian metrics, Regge action and ADM
minisuperspace are standard imported frameworks, not W33-derived laws.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from functools import lru_cache
import hashlib,itertools as it,json,math,sys
from pathlib import Path
import networkx as nx
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'analysis'))
from PART_MCCCCXVII_MCCCCXXXII_clifford_fibration_selector_verifier import build_600cell,build_adjacency
OUT=ROOT/'data/w33_pass11768_lorentzian_h4_code_source.json'


@lru_cache(None)
def native_slab():
    V=build_600cell();A=build_adjacency(np.array(V),120)
    g=nx.Graph();g.add_nodes_from(range(120))
    g.add_edges_from((i,j) for i in range(120) for j in range(i+1,120) if A[i][j])
    tetrahedra=sorted(tuple(sorted(c)) for c in nx.enumerate_all_cliques(g) if len(c)==4)
    assert len(tetrahedra)==600 and g.number_of_edges()==720
    simplices=[tuple([v for v in tet[:cut+1]]+[v+120 for v in tet[cut:]]) for tet in tetrahedra for cut in range(4)]
    return g,tetrahedra,simplices


def squared_length_quarters(i,j):
    if i==j:return 0
    if i%120==j%120:return -1
    return 4 if i//120==j//120 else 3


def simplex_gram(simplex):
    q=lambda i,j:squared_length_quarters(simplex[i],simplex[j])
    return s.Matrix(4,4,lambda i,j:s.Rational(q(0,i+1)+q(0,j+1)-q(i+1,j+1),8))


def product_basis(cut):
    vertices=[(r,0) for r in range(cut+1)]+[(r,1) for r in range(cut,4)]
    coords=[s.Matrix([time,*([0,0,0] if r==0 else list(s.eye(3)[:,r-1]))]) for r,time in vertices]
    return s.Matrix.hstack(*[v-coords[0] for v in coords[1:]])


@lru_cache(None)
def lorentzian_certificate():
    graph,tets,simplices=native_slab();edges=set();triangles=set();timelike_angles=defaultdict(float);types=[]
    spatial=(s.eye(3)+s.ones(3))/2
    product=s.diag(-s.Rational(1,4),1,1,1);product[1:4,1:4]=spatial
    normal_transform=s.Matrix.vstack(-s.ones(1,4),s.eye(4))
    for cut in range(4):
        template=[*range(cut+1),*[r+120 for r in range(cut,4)]]
        G=simplex_gram(template);B=product_basis(cut)
        assert abs(B.det())==1 and G==B.T*product*B and G.det()==-s.Rational(1,8)
        dt=s.Matrix([s.Rational(template[i]//120-template[0]//120,2) for i in range(1,5)])
        assert (dt.T*G.inv()*dt)[0]==-1
        N=normal_transform*G.inv()*normal_transform.T
        assert all(N[i,i]!=0 for i in range(5))
        angle={}
        for ids in it.combinations(range(5),3):
            tri=[template[i] for i in ids]
            x,y,z=[s.Rational(squared_length_quarters(i,j),4) for i,j in ((tri[0],tri[1]),(tri[0],tri[2]),(tri[1],tri[2]))]
            det=x*y-(x+y-z)**2/4
            if det<0:
                i,j=[k for k in range(5) if k not in ids]
                assert N[i,i]>0 and N[j,j]>0
                cosine=-N[i,j]/s.sqrt(N[i,i]*N[j,j]);angle[ids]=float(s.acos(cosine))
        types.append(dict(cut=cut,Gram=[[str(x) for x in row] for row in G.tolist()],
                          determinant='-1/8',product_basis=[list(map(int,row)) for row in B.tolist()],dt_squared_norm=-1))
        for simplex in simplices[cut::4]:
            edges.update(it.combinations(sorted(simplex),2));triangles.update(it.combinations(sorted(simplex),3))
            for ids,value in angle.items():timelike_angles[tuple(sorted(simplex[i] for i in ids))]+=value
    assert len(edges)==2280 and len(triangles)==6240
    assert all(i%120==j%120 or graph.has_edge(i%120,j%120) for i,j in edges)
    edge_types=Counter(squared_length_quarters(*e) for e in edges)
    assert edge_types=={4:1440,3:720,-1:120}
    triangle_types=Counter()
    for tri in triangles:
        q=[squared_length_quarters(i,j) for i,j in it.combinations(tri,2)]
        if any(x<0 for x in q):triangle_types['timelike_product_edge']+=1
        elif len({i//120 for i in tri})==1:triangle_types['spatial_boundary']+=1
        else:triangle_types['spacelike_mixed']+=1
    assert triangle_types=={'timelike_product_edge':1440,'spatial_boundary':2400,'spacelike_mixed':2400}
    delta=2*math.pi-5*math.acos(1/3)
    deficits=[2*math.pi-a for a in timelike_angles.values()]
    assert len(deficits)==1440 and max(abs(x-delta) for x in deficits)<1e-12
    return dict(status='PASS',f_vector=[240,2280,6240,6600,2400],
        edge_squared_lengths_at_a1_tau_half={'spatial':1,'cross_diagonal':'3/4','vertical':'-1/4'},
        edge_type_counts={str(k):v for k,v in edge_types.items()},triangle_type_counts=dict(triangle_types),
        exact_Gram_types=types,all_2400_simplex_signatures='one negative, three positive, by exact product congruence',
        symbolic_all_simplex_determinant='-a^6*tau^2/2',each_simplex_volume='sqrt(2)*a^3*tau/48',
        total_spacetime_volume='50*sqrt(2)*a^3*tau',time_covector_squared_norm=-1,
        time_function='t=0 on bottom,t=tau on top, affine on simplices; dt is timelike. This global time function excludes causal closed curves in the product slab.',
        timelike_hinges=1440,each_timelike_hinge_area='a*tau/2',
        timelike_deficit_max_error=max(abs(x-delta) for x in deficits),
        spatial_edge_deficit=delta,
        product_curvature='Only the spatial-edge x interval surfaces have curvature; their two timelike triangular subdivisions carry the same Euclidean-normal-plane deficit. Other mixed hinges are flat subdivision or unfolded spatial-face interiors. Constant-time boundaries have K=0.',
        static_reduced_Regge_action='tau*(720*a*delta-50*sqrt(2)*Lambda*a^3), omitting common1/(8piG)',
        static_lapse_constraint='Lambda*a^2=72*delta/(5*sqrt(2))',
        static_scale_stationarity='Lambda*a^2=24*delta/(5*sqrt(2))',
        no_simultaneous_static_scale_and_lapse_stationarity=True,
        boundary_variation_scope='The two-parameter static ansatz lets a and tau vary. Its failure is not a claim about all independent Regge variations with fixed boundary spatial edges. A continuous-time homogeneous ADM extension below independently tests static bulk equations.',
        geometric_scope='An explicit supplied piecewise-flat Lorentzian metric on the prior native S3xI triangulation. Not a spacetime metric derived from W33, a Regge vacuum, constraint closure or continuum limit.')


@lru_cache(None)
def conditional_code_source_certificate():
    a,N,adot,Lambda,delta,mu,E=s.symbols('a N adot Lambda delta mu E',positive=True)
    C=720*delta;D=50*s.sqrt(2);B=3*D
    # In8piG=1 units. This is an imported ADM minisuperspace law on the
    # scaled PL spatial metric, not an exact time-discrete frustum action.
    lag=-B*a*adot**2/N+N*(C*a-D*Lambda*a**3-mu*E)
    constraint=s.diff(lag,N)
    assert constraint==B*a*adot**2/N**2+C*a-D*Lambda*a**3-mu*E
    astar=3*mu*E/(2*C);lstar=C/(3*D*astar**2)
    assert s.simplify(constraint.subs(adot,0).subs({a:astar,Lambda:lstar},simultaneous=True))==0
    assert s.simplify(s.diff(lag,a).subs(adot,0).subs({a:astar,Lambda:lstar},simultaneous=True))==0
    # Proper-time acceleration from the ADM scale equation + constraint.
    acceleration=Lambda*a/3-mu*E/(2*B*a**2)
    growth=s.simplify(s.diff(acceleration,a).subs({a:astar,Lambda:lstar},simultaneous=True))
    assert s.simplify(growth-lstar)==0
    # More generally a supplied spectral scale mu*a^(-p) has pressure w=p/3.
    # Ordinary dust/radiation/stiff spectral scalings all retain the instability.
    p=s.symbols('p',real=True);q=mu*E*a**(-p)
    power_lag=-B*a*adot**2/N+N*(C*a-D*Lambda*a**3-q)
    power_acceleration=Lambda*a/3-(p+1)*q/(2*B*a**2)
    # At a static point q=2*C*a/(p+3) and Lambda*a^2=(p+1)*C/((p+3)*D).
    static_lambda=(p+1)*C/((p+3)*D*a**2)
    static_q=2*C*a/(p+3)
    assert s.simplify(s.diff(power_lag,N).subs({N:1,adot:0,Lambda:static_lambda,mu:static_q*a**p/E},simultaneous=True))==0
    power_growth=s.diff(power_acceleration,a).subs({Lambda:static_lambda,mu:static_q*a**p/E},simultaneous=True)
    assert s.simplify(power_growth-(p+1)*C/(B*a**2))==0
    return dict(status='PASS',ADM_assumption='Import the GR ADM action in8piG=1units and restrict g_ij=a(t)^2 g0_ij,N=N(t),shift0. Regge integrates the spatial curvature; KijKij-K^2=-6(adot/(Na))^2.',
        gravity_Lagrangian='-150*sqrt(2)*a*adot^2/N+N*(720*delta*a-50*sqrt(2)*Lambda*a^3)',
        code_source='H_exc=H_CSS+60I=sum_v(I-A_v)+sum_f(I-B_f), with the prior60qubit star/octagon stabilizers. Use i<psi|dot psi>-N*mu<psi|H_exc|psi>,norm psi=1.',
        code_lowest_excitation_energy=4,code_ground_energy=0,code_ground_degeneracy=4,
        matter_assumptions='Supplied positive energy scale mu; all code energy is smeared uniformly over native S3 and is independent of a (dust pressure0). This is a named homogeneous coupling, not a native H4check-face embedding or a derived local stress tensor.',
        full_homogeneous_constraint=str(constraint),
        Friedmann_equation='(adot/(N*a))^2=Lambda/3-k_eff/a^2+mu*E/(150*sqrt(2)*a^3)',
        effective_curvature='k_eff=24*delta/(5*sqrt(2))',
        matter_density='rho=mu*E/(50*sqrt(2)*a^3), pressure=0',
        proper_time_acceleration='addot=Lambda*a/3-mu*E/(300*sqrt(2)*a^2)',
        static_excited_solution={'a_star':str(astar),'Lambda_star':str(lstar)},
        static_excited_solution_exists_for_positive_E=True,static_excited_solution_stable=False,
        exact_linear_instability='delta_addot=Lambda_star*delta_a; positive Lambda_star gives exponential growth.',
        code_ground_has_no_positive_radius_static_solution=True,
        power_law_extension={'supplied_energy':'mu*E*a^(-p)',
            'equation_of_state':'w=p/3',
            'static_radius_equation':'a^(p+1)=(p+3)*mu*E/(2*C), C=720*delta',
            'static_curvature_relation':'Lambda*a^2=(p+1)*C/((p+3)*D), D=50*sqrt(2)',
            'linear_growth_squared':'(p+1)*C/(B*a_star^2), B=150*sqrt(2)',
            'all_p_greater_than_minus_one_unstable':True,
            'scope':'An exact no-go inside the supplied homogeneous ADM/power-law spectral-source family. Dust p=0,radiation p=1 and stiff p=3 cannot stabilize the static branch. This is not a theorem excluding nonstatic universes, other matter actions, extra moduli or inhomogeneous dynamics.'},
        normalization_boundary='The choice H_exc=H_CSS+60I and mu is supplied. A different vacuum-energy reference changes gravitational sources; no vacuum-energy cancellation or prediction of Newton or cosmological constants follows.',
        dynamics_scope='A fully specified conditional homogeneous gravity/code-source action and its constraint, beyond two uncoupled carriers. ADM gravity, smearing and energy scale are independent assumptions. No local matter constraints, continuum recovery or stable physical vacuum is derived.')


def payload():
    sources=['analysis/w33_20261008_native_H4_4D_spacetime_slab.py',
             'analysis/w33_20261008_native_H4_Regge_S3.py',
             'analysis/w33_20261008_20apt_exact_thermal_spectrum.py']
    return dict(status='PASS',schema='w33.pass11768.lorentzian_h4_code_source.v1',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        inputs={name:hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for name in sources},
        Lorentzian_slab=lorentzian_certificate(),conditional_ADM_code_source=conditional_code_source_certificate(),
        literature=['https://arxiv.org/abs/2312.11639','https://arxiv.org/abs/1908.10022'],
        boundary='The exact metric and conditional action do not complete gravity, derive physical constants or solve the TOE.')


if __name__=='__main__':
    result=payload();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print('11768 PASS2400Lorentzian simplices,1440timelike deficits; conditional ADM/code source unstable static branch')
