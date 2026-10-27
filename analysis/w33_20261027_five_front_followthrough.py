"""Five-front continuation of the native finite-loop gauge construction.

Native maps and explicit tests; supplied couplings and dimensional projections
are named. Prior owners: October27 face module; October23 code; Pass12188;
Pass10950 Qpsi; TOE38 and TOE58--62 compact gauge methods.
"""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from math import gcd, lcm
from pathlib import Path
import hashlib
import json
import sys

import numpy as np
import sympy as s
from scipy.sparse import coo_matrix, diags, bmat, eye
from scipy.sparse.linalg import eigsh
from scipy.optimize import linprog, minimize
from scipy.special import expit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import w33_20261027_native_bloch_face_module as prior
import w33_pass12188_native_period_symplectic_repair as native

ROOT = Path(__file__).resolve().parents[1]
PAIRS = list(combinations(range(4), 2))


def exact_list(M):
    return [[str(x) for x in row] for row in M.tolist()]


@lru_cache(None)
def inputs():
    B, V, edges, lookup, nbr = prior.geometry()
    loops, periods, comm = prior.deck_loops(edges, V)
    H, _ = prior.matched_loop_metric(B, V, periods)
    d = json.loads((ROOT/'data/w33_20261027_native_bloch_face_module.json').read_text())
    M = s.Matrix(d['effective_symbol']['harmonic_link_gram_M'])
    return B, V, edges, loops, periods, comm, H, M


def metric_classification():
    *_, periods, comm, H, M = inputs()
    W = s.Matrix(periods)
    # Unknown symmetric six-loop metric: test a spanning set of quadratic n.
    z = s.symbols('h:21')
    pairs6 = [(i,j) for i in range(6) for j in range(i,6)]
    S = s.zeros(6)
    for x,(i,j) in zip(z,pairs6): S[i,j]=S[j,i]=x
    equations=[]
    directions=[s.eye(4)[:,i] for i in range(4)]
    directions += [s.eye(4)[:,i]+s.eye(4)[:,j] for i,j in PAIRS]
    for n in directions:
        u=W*n
        C=s.Matrix([[u[i]*W[j,a]-u[j]*W[i,a] for a in range(4)] for i,j in PAIRS])
        equations.extend(list(C.T*S*C))
    A,_=s.linear_eq_to_matrix(equations,z)
    ns=A.nullspace()
    assert A.rank()==20 and len(ns)==1
    J=s.zeros(6)
    J[0,5]=J[5,0]=1
    J[1,4]=J[4,1]=-1
    J[2,3]=J[3,2]=1
    assert A*s.Matrix([J[i,j] for i,j in pairs6])==s.zeros(A.rows,1)
    assert (J*H)**2==4*s.eye(6) and s.trace(J*H)==0
    theta=s.Symbol('theta')
    determinant=s.factor((H+theta*J).det())
    assert s.expand(determinant-(4-theta**2)**3)==0
    # Integer orientation reversal is not a symmetry selected by the graph.
    # At constitutive level it flips the four-form and can fix theta=0 if imposed.
    return {'unknown_symmetric_metric_parameters':21,'constraint_rank':20,
            'all_metrics_for_fixed_target_symbol':'H(theta)=H0+theta*J',
            'J':exact_list(J),'positive_interval':'-2 < theta < 2',
            'determinant':str(determinant),
            'interpretation':'One four-form ambiguity is invisible to the leading plane-wave symbol. It is an analogue of an axion constitutive term, not a derived QCD axion or full spacetime theta term.',
            'microscopic_selection':'Common-cone requirement plus an imposed orientation reversal fixes theta=0 in this class. Neither requirement is a microscopic derivation of the couplings.'}


def finite_k_four_form():
    B,V,edges,loops,periods,comm,H,M=inputs()
    payload=json.loads((ROOT/'data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json').read_text())
    faces=[f['boundary'] for f in payload['independent_face_basis']]
    J=np.zeros((6,6));J[0,5]=J[5,0]=1;J[1,4]=J[4,1]=-1;J[2,3]=J[3,2]=1
    rows=[]
    for t in (.04,.02,.01,.005):
        k=t*np.array([1,2,-1,1]);D=prior.gradient(V,edges,k)
        Fs=prior.curl(faces,V,k);Fc=prior.curl(comm,V,k)
        term=Fc.conj().T@J@Fc
        rec={'t':t,'four_form_operator_norm_over_t3':float(np.linalg.norm(term,2)/t**3),'spectra':[]}
        for theta in (-1,0,1):
            coupling=np.array(H,dtype=float)+theta*J
            F=np.vstack((Fs,np.linalg.cholesky(coupling).T@Fc))
            _,ev=prior.transverse(F,D)
            rec['spectra'].append({'theta':theta,'lambda_over_t2':(ev[:3]/t**2).tolist()})
        rows.append(rec)
    return {'samples':rows,
            'scope':'The leading four-form ambiguity is generally visible at finite lattice momentum. The supplied loop discretization is not proved to realize an exact topological F wedge F action; no physical axion inferred.'}


def dimensional_reduction():
    *_,H,M=inputs()
    # Work on the momentum module T=R^-T, not the contragredient period R.
    _,R=native.native()
    T=[x.inv().T for x in R.values()]
    assert all(x.T*M*x==M for x in T)
    z=s.symbols('p:16');P=s.Matrix(4,4,z)
    eq=[e for x in T for e in P*x-x*P]
    A,_=s.linear_eq_to_matrix(eq,z)
    commutant=A.nullspace()
    assert len(commutant)==4
    # Exhibit the two inequivalent rational C3 planes and their full commutant.
    Q=s.Matrix([[-1,0,-1,1],[-1,1,-1,0],[0,0,1,-2],[0,0,1,1]])
    Qmom=Q.inv().T
    blocks=[Qmom.inv()*x*Qmom for x in T]
    assert all(x[:2,2:]==s.zeros(2) and x[2:,:2]==s.zeros(2) for x in blocks)
    # Each irreducible order3 plane has centralizer Q(sqrt(-3)); idempotents
    # of that field are only0,1. Two inequivalent planes give ranks0,2,4.
    for part in (slice(0,2),slice(2,4)):
        rep=next(x[part,part] for x in blocks if x[part,part]!=s.eye(2))
        assert rep**2+rep+s.eye(2)==s.zeros(2)
    # Search an actual integral metric reflection; report scope precisely.
    found=None
    for raw in product(range(-2,3),repeat=4):
        if not any(raw) or gcd(*raw)!=1: continue
        v=s.Matrix(raw);F=s.eye(4)-2*v*(v.T*M)/(v.dot(M*v))
        if all(x.q==1 for x in F):
            assert F*F==s.eye(4) and F.T*M*F==M
            found=(v,F);break
    out={'native_momentum_commutant_dimension':4,
         'native_symmetry_invariant_rational_projector_ranks':[0,2,4],
         'native_rank3_projector_exists':False,
         'circle_zero_mode_count':{'three_dimensional_photon':2,'extra_massless_scalar':1},
         'circle_obstruction':'Setting compact momentum to zero leaves the compact component of A as a massless scalar. It cannot be removed by zero-mode gauge transformations.',
         'orbifold_zero_mode_count':{'three_dimensional_photon':2,'extra_massless_scalar':0},
         'orbifold_assumption':'Supply a reflection, A along its odd line odd and the three tangent components even. This is a continuum boundary condition, not a verified automorphism of the selected105-face microscopic action.',
         'scope':'No native-H27-invariant rational3D truncation. A chosen compactification/projection breaks that symmetry; no radius is dynamically selected.'}
    if found:
        v,F=found
        out['integral_metric_reflection']={'odd_vector':list(map(int,v)),
             'matrix':exact_list(F),'even_projector':exact_list((s.eye(4)+F)/2),
             'ranks_even_odd':[3,1],
             'commutes_with_native_group':all(F*x==x*F for x in T)}
    return out


def compact_metric_completion():
    *_,H,M=inputs()
    # Include unit harmonics to remove extra compact minima. Find bounded integer
    # harmonics by LP, then certify their weights by EXACT rational elimination.
    eps=s.Rational(1,100)
    B=H-eps*s.eye(6)
    assert all(B[:i,:i].det()>0 for i in range(1,7))
    qs=[q for q in product((-1,0,1),repeat=6) if any(q) and next(x for x in q if x)>0]
    ij=[(i,j) for i in range(6) for j in range(i,6)]
    A=s.Matrix([[q[i]*q[j] for q in qs] for i,j in ij])
    rhs=s.Matrix([B[i,j] for i,j in ij])
    result=linprog(np.ones(len(qs)),A_eq=np.array(A,dtype=float),
                   b_eq=np.array(rhs,dtype=float).ravel(),bounds=(0,None),method='highs')
    assert result.success
    active=np.flatnonzero(result.x>1e-8).tolist()
    weights,free=A[:,active].gauss_jordan_solve(rhs)
    assert free.rows==0 and all(x>0 for x in weights)
    harmonics=[{'q':[int(i==j) for i in range(6)],'weight':str(eps)} for j in range(6)]
    total=eps*s.eye(6)
    for col,weight in zip(active,weights):
        q=s.Matrix(qs[col])
        total+=weight*q*q.T
        harmonics.append({'q':list(map(int,q)),'weight':str(weight)})
    assert total==H
    return {'potential':'sum_q w_q*(1-cos(q dot f))',
            'harmonics':harmonics,'all_weights_positive':True,
            'Hessian_at_zero_equals_prior_H0':True,
            'unique_global_minimum_on_flux_6_torus':'f=0 mod2pi, because all six positive unit harmonics are included',
            'max_integer_harmonic_charge':max(abs(q) for h in harmonics for q in h['q']),
            'scope':'A supplied finite-loop periodic interaction exists with exactly the desired harmonic Hessian, all q entries0,+1,-1. LP only locates a candidate; exact rational reconstruction proves feasibility, not optimality. Higher interactions and couplings remain modeling choices.'}


def microscopic_induction_probe():
    """Static free charged-matter determinant on the actual19-site patch.

    A concrete microscopic candidate is tested, not asserted to explain H0.
    These are spinless thermal hopping copies with the Qpsi multiplicities,
    not a chiral relativistic E6 determinant or a temporal polarization tensor.
    """
    C,B,keys,endpoints=lifted_patch()
    dual=C.T@np.linalg.inv(C@C.T)
    links=[(int(np.flatnonzero(row<0)[0]),int(np.flatnonzero(row>0)[0])) for row in B]
    def response(phi,T):
        A=dual@np.array(phi);total=0.;grad=np.zeros(2);hess=np.zeros((2,2))
        for charge,mult in ((1,16),(-2,10),(4,1)):
            K=np.zeros((B.shape[1],B.shape[1]),complex)
            first=np.zeros((2,*K.shape),complex)
            second=np.zeros((2,2,*K.shape),complex)
            for e,(a,b) in enumerate(links):
                K[b,a]=-np.exp(1j*charge*A[e]);K[a,b]=K[b,a].conjugate()
                for i in range(2):
                    first[i,b,a]=1j*charge*dual[e,i]*K[b,a]
                    first[i,a,b]=first[i,b,a].conjugate()
                    for j in range(2):
                        second[i,j,b,a]=-charge**2*dual[e,i]*dual[e,j]*K[b,a]
                        second[i,j,a,b]=second[i,j,b,a].conjugate()
            ev,U=np.linalg.eigh(K)
            total-=mult*T*np.logaddexp(0,-ev/T).sum()
            occ=expit(-ev/T)
            gap=ev[:,None]-ev[None,:]
            divided=np.zeros_like(gap);distinct=abs(gap)>1e-9
            np.divide(occ[:,None]-occ[None,:],gap,out=divided,where=distinct)
            limit=-occ*(1-occ)/T
            divided[~distinct]=np.broadcast_to(limit[:,None],gap.shape)[~distinct]
            deriv=[U.conj().T@X@U for X in first]
            for i in range(2):
                grad[i]+=mult*np.dot(occ,np.diag(deriv[i])).real
                for j in range(2):
                    direct=np.dot(occ,np.diag(U.conj().T@second[i,j]@U))
                    mixing=np.sum(divided*deriv[i]*deriv[j].T)
                    hess[i,j]+=mult*(direct+mixing).real
        return float(total),grad,hess
    *_,H,M=inputs();target=np.array(H[:2,:2],dtype=float)
    rows=[]
    grid=list(product(np.linspace(0,2*np.pi,13,endpoint=False),repeat=2))
    for T in (.25,1.,2.):
        starts=sorted(grid,key=lambda x:response(x,T)[0])[:5]
        fits=[minimize(lambda x:response(x,T)[:2],x,jac=True,method='BFGS',options={'gtol':1e-10}) for x in starts]
        fit=min(fits,key=lambda x:x.fun);phi=fit.x%(2*np.pi)
        F0,gradient0,K=response([2*np.pi/3,4*np.pi/3],T)
        assert np.max(abs(gradient0))<1e-11
        assert abs(K[0,0]-K[1,1])<1e-11
        scale=float(np.vdot(K,target)/np.vdot(target,target))
        residual=float(np.linalg.norm(K-scale*target)/max(np.linalg.norm(K),1e-14))
        rows.append({'temperature':T,'minimum_flux_angles':phi.tolist(),
                     'free_energy':float(fit.fun),'hessian':K.tolist(),
                     'hessian_eigenvalues':np.linalg.eigvalsh(K).tolist(),
                     'zero_flux_hessian_eigenvalues':np.linalg.eigvalsh(response([0,0],T)[2]).tolist(),
                     'central_flux_angles':[2*np.pi/3,4*np.pi/3],
                     'central_flux_gradient_max':float(max(abs(gradient0))),
                     'central_flux_free_energy':F0,
                     'best_target_scale':scale,'relative_shape_residual':residual,
                     'scan_scope':'13x13 angle grid followed by5 local optimizations; global minimality not certified'})
    return {'native_patch_vertices':B.shape[1],'internal_charge_multiplicities':{'1':16,'-2':10,'4':1},
            'model':'Static grand-canonical spinless hopping free energy, mu=0,t=1',
            'samples':rows,
            'central_stationarity':'All27 Qpsi charges are1 mod3, so at Z3 central flux all species hopping matrices are gauge-equivalent, with the same spectrum. The first derivative is proportional to Tr Q=0, and the Hessian to Tr Q^2=72. Third derivatives are proportional to Tr Q^3=0.',
            'target_shape_obstruction':'The native theta patch has two equal8-edge paths and a4-edge path. Exchange plus flux conjugation fixes the central flux, forcing K11=K22 at every T. The target H0 principal block has diagonals25/9 and11/3; it cannot be proportional to this induced central Hessian.',
            'scope':'Concrete induced spatial stiffness candidate. Analytic spectral derivatives avoid finite-difference cancellation. It neither computes a relativistic electric response nor selects the full six-loop metric; global minima are not certified.'}


def central_link_gauge_equivalence():
    C,B,keys,endpoints=lifted_patch()
    phi=np.array([2*np.pi/3,4*np.pi/3])
    A=C.T@np.linalg.solve(C@C.T,phi)
    links=[(int(np.flatnonzero(row<0)[0]),int(np.flatnonzero(row>0)[0])) for row in B]
    records=[]
    for charge in (-2,4):
        ratios=np.exp(1j*(charge-1)*A)
        phases={0:1+0j};todo=[0]
        for a in todo:
            for e,(tail,head) in enumerate(links):
                if a==tail:b=head;factor=ratios[e]
                elif a==head:b=tail;factor=ratios[e].conjugate()
                else:continue
                if b not in phases:phases[b]=phases[a]*factor;todo.append(b)
        assert len(phases)==B.shape[1]
        error=max(abs(phases[b]/phases[a]-ratios[e])for e,(a,b) in enumerate(links))
        assert error<1e-12
        records.append({'charge':charge,'edge_phase_coboundary_max':float(error)})
    return {'controls':records,'scope':'Explicit vertex-phase intertwiners. The link matrices are gauge-equivalent, not literally equal in the chosen harmonic gauge.'}


def lifted_patch(N=3):
    B,V,edges,loops,periods,comm,H,M=inputs()
    dictionaries=[]
    for face in comm[:2]:
        position=np.zeros(4,dtype=int);vertex=0;row=Counter()
        for e,sign in face:
            a,b=edges[e] if sign==1 else edges[e][::-1]
            assert vertex==a
            if sign<0:position-=V[e]
            key=(tuple(map(int,position%N)),e)
            row[key]+=sign
            if sign>0:position+=V[e]
            vertex=b
        assert vertex==0 and not position.any()
        dictionaries.append({k:v for k,v in row.items() if v})
    keys=sorted(set().union(*dictionaries));C=np.zeros((2,len(keys)),dtype=int)
    vertices=set();endpoints=[]
    for cell,e in keys:
        a,b=edges[e]
        tail=(cell,a);head=(tuple(map(int,(np.array(cell)+V[e])%N)),b)
        endpoints.append((tail,head));vertices.update((tail,head))
    vid={v:i for i,v in enumerate(sorted(vertices))}
    incidence=np.zeros((len(keys),len(vid)),dtype=int)
    for j,(a,b) in enumerate(endpoints):incidence[j,vid[a]]=-1;incidence[j,vid[b]]=1
    for r,row in enumerate(dictionaries):
        C[r]=[row.get(key,0) for key in keys]
    assert not (C@incidence).any() and np.linalg.matrix_rank(C)==2
    return C,incidence,keys,endpoints


def rotor_matrix(cutoff,g,charge=0,matter=False,hopping=.3,mass=.2):
    C,B,keys,endpoints=lifted_patch()
    states=np.array(list(product(range(-cutoff,cutoff+1),repeat=2)),dtype=int)
    idx={tuple(x):i for i,x in enumerate(states)};size=len(states)
    *_,H,M=inputs()
    a=float(H[0,0]+H[0,1]);b=float(H[1,1]+H[0,1]);c=float(-H[0,1])
    assert np.allclose([a,b,c],[10/9,2,5/3])
    harmonics=[((1,0),a),((0,1),b),((1,-1),c)]
    magnetic_rows=[];magnetic_cols=[];magnetic_vals=[]
    shifts=[]
    for step,w in harmonics:
        pairs=[]
        for i,x in enumerate(states):
            j=idx.get(tuple(x+step))
            if j is not None:
                pairs.append((i,j))
                magnetic_rows.extend((i,j));magnetic_cols.extend((j,i))
                magnetic_vals.extend((-w/(2*g*g),)*2)
        shifts.append(pairs)
    magnetic=coo_matrix((magnetic_vals,(magnetic_rows,magnetic_cols)),shape=(size,size)).tocsr()
    E0=np.zeros(len(keys),dtype=int);E0[0]=charge
    blocks=[]
    for sector in ((0,1) if matter else (1,)):
        E=states@C+sector*E0
        # G=div E-n+background; in the transferred state n-background=div E0.
        assert np.array_equal(E@B,np.tile(sector*E0@B,(size,1)))
        electric=.5*g*g*np.sum(E*E,axis=1)
        diagonal=electric+(a+b+c)/(g*g)
        if matter: diagonal=diagonal+mass*(2*sector-1)
        blocks.append(diags(diagonal)+magnetic)
    Hamil=(bmat([[blocks[0],-hopping*eye(size)],[-hopping*eye(size),blocks[1]]],format='csr')
           if matter else blocks[0])
    eigen,vec=eigsh(Hamil,k=2,which='SA',tol=2e-11,v0=np.ones(Hamil.shape[0]))
    order=np.argsort(eigen);eigen=eigen[order];psi=vec[:,order[0]]
    copies=psi.reshape(2,size) if matter else psi.reshape(1,size)
    wilson=[float(sum(np.sum(part[[i for i,j in pairs]]*part[[j for i,j in pairs]]) for part in copies))
            for pairs in shifts]
    boundary=np.any(np.abs(states)==cutoff,axis=1)
    edge_probability=float(np.sum(copies[:,boundary]**2))
    return {'cutoff':cutoff,'dimension':Hamil.shape[0],'g':g,'charge':charge,
            'dynamical_two_site_matter':matter,'ground_energy':float(eigen[0]),
            'gap':float(eigen[1]-eigen[0]),'Wilson_cosines':wilson,
            'boundary_probability':edge_probability,
            'Gauss_exact_for_every_basis_state':True}


def compact_dynamics():
    C,B,keys,endpoints=lifted_patch()
    rows=[]
    for g in (.5,1.,2.):
        seq=[rotor_matrix(L,g) for L in (2,4,6,8,10)]
        assert all(seq[i+1]['ground_energy']<=seq[i]['ground_energy']+1e-9 for i in range(4))
        rows.append({'g':g,'samples':seq,
                     'last_energy_difference':abs(seq[-1]['ground_energy']-seq[-2]['ground_energy'])})
    matter=[rotor_matrix(8,1.,charge=q,matter=True) for q in (1,-2,4)]
    static=[rotor_matrix(8,1.,charge=q) for q in (0,1,-2,4)]
    return {'native_finite_cover_periods':[3]*4,'patch_vertices':B.shape[1],
            'patch_links':len(keys),'loop_Gram':(C@C.T).tolist(),
            'loops':'first two actual lifted16-traversal commutators from prior certificate',
            'magnetic_potential_weights':['10/9','2','5/3'],
            'magnetic_harmonics':[[1,0],[0,1],[1,-1]],
            'neutral_cutoff_sequences':rows,'static_endpoint_charge_controls':static,
            'dynamical_matter_controls':matter,
            'scope':'Two native magnetic flux coordinates only. Other native gauge modes are held out; charged/dynamical sectors use one actual patch edge. This is finite-patch compact U1 ED with unitary infinite-cutoff shifts approximated by hard-wall Galerkin projections, not a full phase diagram, confinement proof, or continuum photon.'}


def matter_interface():
    path=ROOT/'artifacts/canonical_su3_gauge_and_cubic.json'
    raw=path.read_bytes();triads=json.loads(raw)['solution']['d_triples']
    tri=[tuple(t['triple']) for t in triads]
    # Exact dictionary from Pass10950, anchored at internal index0.
    q=[4 if j==0 else (-2 if any(0 in t and j in t for t in tri) else 1) for j in range(27)]
    assert Counter(q)==Counter({1:16,-2:10,4:1})
    assert all(sum(q[j] for j in t)==0 for t in tri)
    patterns=Counter(tuple(sorted(q[j] for j in t)) for t in tri)
    assert patterns==Counter({(-2,1,1):40,(-2,-2,4):5})
    assert sum(q)==sum(x**3 for x in q)==0
    # Symbolic exponent Ward law for charged link hopping, all27 components.
    chi_a,chi_b=s.symbols('chi_a chi_b')
    assert all(s.expand(-x*chi_b+x*(chi_b-chi_a)+x*chi_a)==0 for x in q)
    return {'canonical_cubic_sha256':hashlib.sha256(raw).hexdigest(),
            'internal_Qpsi':q,'branching':'27=16_1+10_-2+1_4',
            'cubic_charge_patterns':{str(k):v for k,v in patterns.items()},
            'all45_signed_cubic_terms_U1_invariant':True,
            'trace_Q':sum(q),'trace_Q_cubed':sum(x**3 for x in q),
            'hopping':'sum_(edge v->w,A) -t_A psi_(w,A)^dag U_edge^(q_A) psi_(v,A)+h.c.',
            'Gauss':'div E - sum_A q_A n_(v,A) + background_v = 0',
            'matter_site_carrier':'native spatial vertex v tensor independent internal E6 index A; the two27-element sets are not identified',
            'prior_owner':'analysis/w33_pass10950_clock_albert_lorentz_spinor.py and data/w33_qpsi_matter_parity_e8_d8_bridge.json',
            'scope':'An explicit gauged U1 subgroup charge map and signed-cubic compatibility, with one-particle two-site ED controls. No nonabelian E6 link, chiral lattice regulator, full Fock vacuum, common fermion speed, or Standard Model derived.'}


def run():
    return {'status':'FIVE_FRONT_CONTINUATION_WITH_EXPLICIT_SCOPE',
            'metric_classification':metric_classification(),
            'finite_k_four_form':finite_k_four_form(),
            'microscopic_induction_probe':microscopic_induction_probe(),
            'central_link_gauge_equivalence':central_link_gauge_equivalence(),
            'dimensional_reduction':dimensional_reduction(),
            'compact_metric_completion':compact_metric_completion(),
            'compact_dynamics':compact_dynamics(),
            'matter_interface':matter_interface(),
            'intake':'Tracked separately in analysis/2026-10-27_research_intake_coverage.json; extraction/archival is not labeled human/model reading.'}


if __name__=='__main__':
    d=run();out=ROOT/'data/w33_20261027_five_front_followthrough.json'
    out.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(d,indent=2))
