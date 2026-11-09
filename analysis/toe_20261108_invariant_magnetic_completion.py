"""Native all-short-face homogenization and a supplied invariant completion.

Prior geometry/loops/cone engineering: October27 Bloch face module.
No selected time, interacting gauge continuum or TOE is derived here.
"""
from functools import lru_cache
from itertools import combinations,product
import hashlib,json
from pathlib import Path
import sys
import numpy as np
import sympy as sp
from scipy.linalg import eigh,orth
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261027_native_bloch_face_module as prior
from w33_pass12188_native_period_symplectic_repair import mul
PAIRS=list(combinations(range(4),2))

def compound(A):
    return sp.Matrix([[A[i,k]*A[j,l]-A[i,l]*A[j,k] for k,l in PAIRS] for i,j in PAIRS])

def wedge(n):
    return np.array([[n[i]*(a==j)-n[j]*(a==i) for a in range(4)] for i,j in PAIRS],float)

@lru_cache(None)
def model():
    d=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text())
    B,V,edges,lookup,nbr=prior.geometry();faces,census=prior.enumerate_faces(V,lookup,nbr)
    h=sp.Matrix([[sp.Rational(x) for x in row] for row in d['harmonic_voltages_Q']])
    hf=np.array(h,float);M=h.T*h
    F=np.zeros((len(faces),135),int)
    for r,face in enumerate(faces):
        for e,sign in face:F[r,e]+=sign
    selected=json.loads((ROOT/'data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json').read_text())['independent_face_basis']
    Fb=np.zeros((105,135),int)
    for i,row in enumerate(selected):
        for e,s in row['boundary']:Fb[i,e]+=s
    C=orth(Fb.T);A=F@C
    den=int(sp.ilcm(*[x.q for x in h]));hn=np.array((h*den).tolist(),dtype=int)
    raw_numerator=np.zeros((len(faces),4,4),dtype=int)
    for r,face in enumerate(faces):
        pos=np.zeros(4,int)
        for e,s in face:
            if s<0:pos-=V[e]
            raw_numerator[r]+=s*np.outer(pos,hn[e])
            if s>0:pos+=V[e]
    raw_numerator=raw_numerator.reshape(len(faces),16);raw=raw_numerator/den
    X=np.linalg.solve(A.T@A,A.T@raw)
    residual=(raw-A@X).reshape(len(faces),4,4)
    area=np.column_stack([residual[:,i,j] for i,j in PAIRS])
    chi=area.T@area
    target=compound(M)/27
    eigen=eigh(chi,np.array(target,float),eigvals_only=True)
    return dict(B=B,V=V,edges=edges,lookup=lookup,faces=faces,F=F,C=C,A=A,h=h,hf=hf,M=M,
                raw=raw,residual=residual,area=area,chi=chi,target=target,census=census,Fb=Fb,
                relative_eigen=eigen,raw_numerator=raw_numerator,raw_denominator=den)

def exact_short_tensor(m):
    """Rational candidates are accepted only after exact normal-equation checks."""
    from fractions import Fraction
    F=sp.Matrix(m['F'].tolist());C=sp.Matrix(m['Fb'].T.tolist());A=F*C
    den=m['raw_denominator'];raw=sp.Matrix(m['raw_numerator'].tolist())/den
    af=np.array(A,float)
    xn=np.linalg.solve(af.T@af,af.T@np.array(raw,float))
    X=sp.Matrix([[sp.Rational(Fraction(float(x)).limit_denominator(1000000)) for x in row] for row in xn])
    R=raw-A*X
    assert A.T*R==sp.zeros(105,16),'Rational reconstruction failed exact normal equations'
    assert all(R[:,4*i+j]+R[:,4*j+i]==sp.zeros(len(m['faces']),1) for i in range(4) for j in range(4))
    area=R[:,[4*i+j for i,j in PAIRS]];chi=area.T*area
    assert chi.rank()==1
    assert np.max(abs(np.array(chi,float)-m['chi']))<1e-12
    proof=dict(method='Exact rational rawderivative and optical normal equations. Numerical candidates accepted only after exact A.T(raw-A X)=0 and antisymmetry checks.',raw_common_denominator=int(den),rational_optical_solution_max_denominator=int(sp.ilcm(*[x.q for x in X])),normal_equations_exact=True,antisymmetry_exact=True,rank_exact=1)
    return chi,proof,area,A

def cup_certificate(m,area,A):
    """Check lifted polygon cup representatives independently of harmonic h."""
    from fractions import Fraction
    polygon=np.zeros((len(m['faces']),6),int)
    for r,face in enumerate(m['faces']):
        pos=np.zeros(4,int)
        for e,s in face:
            step=s*m['V'][e]
            polygon[r]+=[pos[i]*step[j]-pos[j]*step[i] for i,j in PAIRS]
            pos+=step
        assert not pos.any()
    delta=sp.Matrix(polygon.tolist())-2*area
    af=np.array(A,float)
    yn=np.linalg.solve(af.T@af,af.T@np.array(delta,float))
    Y=sp.Matrix([[sp.Rational(Fraction(float(y)).limit_denominator(1000000)) for y in row] for row in yn])
    assert A*Y==delta,'Independent polygon area has not been matched modulo optical coboundaries'
    assert area.rank()==1
    # An explicitly nonuniform positive length weighting as a numerical control.
    w=np.array([{3:1.3,4:.7,5:2.1}[len(f)] for f in m['faces']])
    C=m['A'];raw=m['raw'];X=np.linalg.solve(C.T@(w[:,None]*C),C.T@(w[:,None]*raw))
    R=(raw-C@X).reshape(len(w),4,4)
    U=np.column_stack([R[:,i,j] for i,j in PAIRS]);weighted=U.T@(w[:,None]*U)
    assert abs(weighted[0,0]-float(m['chi'][0,0]))>.01
    assert np.max(abs(weighted[1:,:]))<1e-12 and np.max(abs(weighted[:,1:]))<1e-12
    return dict(period_cup_image_rank=1,face_cohomology_dimension=len(m['faces'])-105,
        polygon_twice_area_mod_optical_exact=True,weighted_face_lengths=[1.3,.7,2.1],
        weighted_area_coefficient=float(weighted[0,0]),weighted_other_components_max=float(max(np.max(abs(weighted[1:,:])),np.max(abs(weighted[:,1:])))),
        proof='Integer lifted polygon twice-areas equal twice the projected harmonic derivative plus an exact optical coboundary. Hence the period map pullback on degree-two cohomology has rank1. A positive definite change of face metric selects different representatives of the same quotient, so no such weighting of these short faces can produce more than one leading magnetic polarization. This is not an all-k rank bound.')

def first_area(faces,V,h):
    rows=[]
    for face in faces:
        pos=sp.zeros(1,4);a=sp.zeros(4)
        for e,sign in face:
            v=sp.Matrix([V[e].tolist()])
            if sign<0:pos-=v
            a+=sign*pos.T*h[e,:]
            if sign>0:pos+=v
        assert pos==sp.zeros(1,4) and a+a.T==sp.zeros(4)
        rows.append([a[i,j] for i,j in PAIRS])
    return sp.Matrix(rows)

@lru_cache(None)
def completion():
    m=model();chi,proof,area,A=exact_short_tensor(m);alpha=sp.Rational(1,16)
    topology=cup_certificate(m,area,A)
    relative=sp.factor((m['target'].inv()*chi).trace())
    assert chi==sp.diag(sp.Rational(29857,5775),0,0,0,0,0)
    assert relative==sp.Rational(29857,5775)
    complement=m['target']-alpha*chi
    assert all(complement[:i,:i].det()>0 for i in range(1,7))
    ni=m['M'].inv()[:,0];xi=m['M'].inv()[:,1]
    simple=sp.Matrix([ni[i]*xi[j]-ni[j]*xi[i] for i,j in PAIRS])
    ratio=sp.factor((simple.T*chi*simple)[0]/(simple.T*m['target']*simple)[0])
    assert ratio==relative and ratio>1
    _,periods,comm=prior.deck_loops(m['edges'],m['V'])
    S=first_area(comm,m['V'],m['h']);assert abs(S.det())==1
    H=S.T.inv()*complement*S.inv()
    group=list(product(range(3),repeat=3));idx={g:i for i,g in enumerate(group)}
    controllers=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text())['exact_deck_actions']
    blocks=[];lifts=[]
    for g,action in zip(group,controllers):
        assert list(g)==action['h'];R=sp.Matrix(action['matrix']);P=np.zeros((135,135),int)
        vp=[idx[mul(g,x)] for x in group]
        ep=[]
        for e,(a,b) in enumerate(m['edges']):
            a,b=vp[a],vp[b];e2=m['lookup'][min(a,b),max(a,b)];sgn=1 if a<b else -1
            ep.append((e2,sgn));P[e2,e]=sgn
        mapped=[[(ep[e][0],sgn*ep[e][1]) for e,sgn in face] for face in comm]
        Sg=first_area(mapped,m['V'],m['h'])
        assert Sg.T*H*Sg==complement
        Cr=compound(R);assert Cr.T*chi*Cr==chi and R.T*m['M']*R==m['M']
        delta=sp.Matrix((P.T@m['V']).tolist())-sp.Matrix(m['V'].tolist())*R.inv()
        # Integrate the exact coboundary, fixing the old vertex0 offset to0.
        shifts={0:sp.zeros(1,4)};todo=[0]
        for a in todo:
            for e,(u,v) in enumerate(m['edges']):
                if u==a and v not in shifts:shifts[v]=shifts[a]+delta[e,:];todo.append(v)
                if v==a and u not in shifts:shifts[u]=shifts[a]-delta[e,:];todo.append(u)
        offsets=sp.Matrix.vstack(*[shifts[a] for a in range(27)])
        assert sp.Matrix(m['B'].tolist())*offsets==delta and all(x.q==1 for x in offsets)
        blocks.append(mapped)
        lifts.append(dict(R=np.array(R,float),inverse=np.array(R.inv(),float),offsets=np.array(offsets,float),vertex=vp,edge=ep))
    m.update(chi_exact=chi,exact_proof=proof,alpha=alpha,relative=relative,complement=complement,
             H=H,S=S,blocks=blocks,lifts=lifts,
             overshoot_n=ni,overshoot_x=xi,overshoot_simple=simple,topology=topology)
    return m

def full_curl(k,completed=True):
    m=completion();F=np.sqrt(float(m['alpha']))*prior.curl(m['faces'],m['V'],k)
    if not completed:return F
    factor=np.linalg.cholesky(np.array(m['H'],float)).T/np.sqrt(27)
    return np.vstack([F]+[factor@prior.curl(block,m['V'],k) for block in m['blocks']])

def spectrum(k,completed=True):
    m=completion();F=full_curl(k,completed);D=prior.gradient(m['V'],m['edges'],k)
    _,ev=prior.transverse(F,D)
    return dict(lowest_squared_frequencies=ev[:7].tolist(),Ward_max=float(np.max(abs(F@D))))

def covariance(k,controller):
    m=completion();g=m['lifts'][controller];kp=g['R']@k;U=np.zeros((135,135),complex)
    for e,((a,b),(e2,sign)) in enumerate(zip(m['edges'],g['edge'])):
        shift=g['offsets'][a] if sign>0 else m['V'][e]@g['inverse']+g['offsets'][b]
        U[e2,e]=sign*np.exp(-1j*shift@kp)
    F=full_curl(k);Fp=full_curl(kp);K=F.conj().T@F;Kp=Fp.conj().T@Fp
    D=prior.gradient(m['V'],m['edges'],k)
    Dp=prior.gradient(m['V'],m['edges'],kp)
    W=np.zeros((27,27),complex)
    for a,b in enumerate(g['vertex']):W[b,a]=np.exp(-1j*g['offsets'][a]@kp)
    return dict(controller=controller,gradient_covariance_max=float(np.max(abs(U@D-Dp@W))),
                magnetic_covariance_max=float(np.max(abs(K-U.conj().T@Kp@U))))

def produce():
    m=completion();rays=[]
    for n in ([1,0,0,0],[0,0,1,0],[1,2,-1,1]):
        n=np.array(n,float);target=float(n@np.array(m['M'],float)@n/27);samples=[]
        for t in (.02,.01,.005):
            r=spectrum(t*n);r.update(t=t,scaled_lowest_three=(np.array(r['lowest_squared_frequencies'][:3])/t**2).tolist());samples.append(r)
        rays.append(dict(direction=n.tolist(),scalar_target_squared_speed=target,samples=samples))
    k=np.array([.17,-.23,.31,.11]);cov=[covariance(k,g) for g in (1,3,9,17,26)]
    assert all(z['magnetic_covariance_max']<2e-10 and z['gradient_covariance_max']<1e-12 for z in cov)
    paths=[str(Path(__file__).relative_to(ROOT)),'analysis/w33_20261027_native_bloch_face_module.py','data/w33_20261027_native_bloch_face_module.json','data/w33_pass11991_native_four_period_cover.json','data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json']
    rational=lambda A:[[str(x) for x in row] for row in A.tolist()]
    return dict(status='EXACT_NATIVE_SHORT_FACE_AREA_TENSOR_AND_SUPPLIED_INVARIANT_COMMON_CONE_COMPLETION_NOT_TOE',
        area_pair_order=PAIRS,exact_short_area_tensor=rational(m['chi_exact']),short_tensor_proof=m['exact_proof'],
        period_cup_product_obstruction=m['topology'],
        short_face_weight=str(m['alpha']),short_weight_PSD_compensation_threshold=str(1/m['relative']),
        unit_weight_overshoot_witness=dict(n=list(map(str,m['overshoot_n'])),x=list(map(str,m['overshoot_x'])),
            simple_area=list(map(str,m['overshoot_simple'])),short_to_target_energy_ratio=str(m['relative']),
            conclusion='Unit shortface weights already exceed the desired scalar magnetic energy on this decomposable area. Adding positive commutator-flux energy cannot restore the target. For positive semidefinite compensation alpha<=5775/29857 is necessary and sufficient; strict inequality gives positive definite6flux coupling.'),
        target_area_tensor=rational(m['target']),complement_area_tensor=rational(m['complement']),
        commutator_area_matrix=rational(m['S']),supplied_six_flux_coupling=rational(m['H']),
        leading_identity='alpha chi_short + (1/27)sum_g S_g.T H S_g = compound(M)/27. Exact on all27 controllers. Wedge(n).T target Wedge(n)=((n.T M n)M-(Mn)(Mn).T)/27.',
        exact_controller_count=27,exact_integral_vertex_lifts=True,commutator_blocks=m['blocks'],
        finite_momentum_covariance=cov,generic_completed_spectrum=spectrum(k),generic_short_only_spectrum=spectrum(k,False),rays=rays,
        scope='Bare noncompact harmonicU1 gauge model with unit electric edge metric and4spatial deck directions plus supplied external time. Positive short weights and162mapped16step commutator rows, with6flux crosscouplings per controller. Engineered leading cone; no unique action selection, exact finite-k cone, scalar-loop inhomogeneous response, 3+1gravity or TOE.',
        prior_owners='October27 exact ranks/flatmode obstruction, native commutators and engineered metric cone. Pass11991 integer deckactions/harmonic metric. New application computes allshortface homogenized tensor and constructs controller-averaged positive compensation.',
        input_raw_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})

if __name__=='__main__':
    d=produce();(ROOT/'data/toe_20261108_invariant_magnetic_completion.json').write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps(dict(status=d['status'],short_tensor=d['exact_short_area_tensor'],covariance=d['finite_momentum_covariance'],rays=d['rays'])))
