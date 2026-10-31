#!/usr/bin/env python3
"""Five followthroughs + three independent physics falsifiers.

Explicit supplied mathematical models. No emergent GR, physical photon, or TOE.
Rebuild W33 from F3^4 and leverage the existing exact symplectic incidence.
"""
from __future__ import annotations
import itertools, json, math, sys, hashlib
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.linalg import null_space, expm
from scipy.sparse.linalg import LinearOperator, eigsh
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261031_server_five_fronts as base
OUT=ROOT/'data'/'w33_20261031_eight_front_server_campaign.json'


def incidence():
    lines=set()
    for i,a in enumerate(base.PTS):
        for j in range(i+1,40):
            b=base.PTS[j]
            if base.pairing(a,b):continue
            L=frozenset(base.IDX[base.canonical(tuple((t*a[k]+u*b[k])%3 for k in range(4)))]
                        for t in range(3) for u in range(3) if t or u)
            assert len(L)==4
            lines.add(L)
    lines=sorted(tuple(sorted(L)) for L in lines)
    assert len(lines)==40
    flags=[(p,j) for j,L in enumerate(lines) for p in L]
    assert len(flags)==160
    D=np.zeros((80,160),dtype=np.int64)
    for e,(p,j) in enumerate(flags):D[p,e]=-1;D[40+j,e]=1
    return D,lines,flags


def projector_exact():
    D,lines,flags=incidence()
    B=D.T@D
    I=np.eye(160,dtype=np.int64)
    C=(8*I-B)@(4*I-B)@((4*I-B)@(4*I-B)-6*I)
    # Exact rational P = C/320, no floating point in this proof.
    assert np.array_equal(C,C.T)
    assert np.array_equal(C@C,320*C)
    assert np.array_equal(D@C,np.zeros((80,160),dtype=np.int64))
    assert np.trace(C)==81*320
    assert np.all(C.diagonal()==162)  # 81/160 of every 160 rails
    assert sorted(set(np.diag(C).tolist()))==[162]
    assert np.linalg.matrix_rank(D)==79
    return D,C


def local_spectral_projection_and_phase_noise():
    D,C=projector_exact()
    P=C.astype(float)/320
    Q=null_space(D.astype(float))
    assert Q.shape==(160,81) and np.linalg.norm(P-Q@Q.T)<1e-10
    rng=np.random.default_rng(511031)
    state=Q@rng.normal(size=81);state/=np.linalg.norm(state)
    assert abs(state@P@state-1)<1e-12
    results=[]
    for sigma in (0.,.15,.35,.7,1.5):
        expected=math.exp(-sigma*sigma)+(1-math.exp(-sigma*sigma))*81/160
        trials=1400
        ph=rng.normal(scale=sigma,size=(trials,160))
        rotated=np.exp(1j*ph)*state[None,:]
        survivals=np.real(np.einsum('bi,ij,bj->b',rotated.conj(),P,rotated,optimize=True))
        empirical=float(survivals.mean())
        se=float(survivals.std()/math.sqrt(trials))
        assert abs(empirical-expected)<max(.012,6*se)
        results.append({'sigma_radians':sigma,'exact_ensemble_code_survival':expected,
                        'MC_code_survival':empirical,'MC_standard_error':se})
    return {'status':'PASS_INTEGER_4HOP_W33_CODE_PROJECTOR_AND_PHASE_NOISE_LAW',
       'exact_polynomial':'P=((8I-B)(4I-B)((4I-B)^2-6I))/320, B=D.T D',
       'integer_idempotence_verified':True,'rank':81,'physical_incidence_modes':160,
       'uniform_diagonal':'81/160','Gaussian_independent_rail_phase_law':
       'E[||P exp(i theta) psi||^2]=exp(-sigma^2)+(1-exp(-sigma^2))*81/160 for any unit norm code state',
       'phase_samples':results,
       'boundary':'A degree4 polynomial in sparse incidence B is not itself a deterministic passive-optical physical projector; LCU/postselection or other hardware is required.'}


def compile_encoder_givens():
    D,_C=projector_exact()
    Q=null_space(D.astype(float))
    A=Q.copy()
    gates=[]
    # Eliminate rows bottom-up via adjacent real Givens rotations.
    for col in range(81):
        for row in range(159,col,-1):
            a,b=A[row-1,col],A[row,col]
            r=math.hypot(a,b)
            if abs(b)<1e-13:continue
            assert r>1e-14
            c,s=a/r,b/r
            u=A[row-1,col:].copy();v=A[row,col:].copy()
            A[row-1,col:]=c*u+s*v
            A[row,col:]=-s*u+c*v
            gates.append((row-1,row,c,s))
    diag=np.diag(A[:81,:81]);assert np.max(abs(abs(diag)-1))<1e-10
    assert np.linalg.norm(A[:81,:81]-np.diag(diag))<1e-10
    assert np.linalg.norm(A[81:])<1e-10
    # Reverse the optical circuit to transform 81 input rails to the code.
    reconstructed=np.zeros((160,81))
    reconstructed[:81]=np.diag(np.sign(diag))
    for i,j,c,s in reversed(gates):
        u=reconstructed[i].copy();v=reconstructed[j].copy()
        reconstructed[i]=c*u-s*v
        reconstructed[j]=s*u+c*v
    residue=float(np.linalg.norm(Q-reconstructed))
    assert residue<1e-9
    payload=np.array(gates,dtype=np.float64)
    return {'status':'PASS_160_PORT_ADJACENT_GIVENS_Q_ENCODER_COMPILED',
       'logical_input_ports':81,'physical_output_ports':160,
       'real_adjacent_two_mode_interferometers':len(gates),
       'worstcase_rectangular_elimination_bound':81*159-81*80//2,
       'reconstruction_Frobenius_error':residue,
       'gate_list_sha256':hashlib.sha256(payload.tobytes()).hexdigest(),
       'sample_gates':[{'modes':[int(i),int(j)],'cos':float(c),'sin':float(s)}for i,j,c,s in gates[:6]],
       'last_diagonal_signs':[int(x)for x in np.sign(diag[:10])],
       'boundary':'Deterministic mathematical real orthogonal network, not fabricated/calibrated; no loss/dephasing model in this ideal compilation. Dense mesh, not an optimal sparse encoder.'}


def qnd_asymmetric_resource_accounting():
    S=np.array([0,1,-1],complex)/math.sqrt(2)
    E=np.array([0,1,1],complex)/math.sqrt(2)
    ss=np.outer(S,S.conj());ee=np.outer(E,E.conj())
    rows=[]
    for fn,fp,transmission in ((0,0,1),(.01,.01,.95),(.05,.1,.8),(.15,.2,.6),(.3,.6,.8),(.2,.85,.6)):
        true_accept=.5*(1-fn);false_accept=.5*fp
        reported_accept=true_accept+false_accept
        rho=(true_accept*ss+false_accept*ee)/reported_accept
        purity=float(np.real(np.trace(rho@rho)))
        fidelity=float(np.real(np.trace(rho@ss)))
        w=base.wigner(rho)
        assert abs(fidelity-(1-fn)/(1-fn+fp))<1e-12
        assert abs(reported_accept-.5*(1-fn+fp))<1e-12
        # Wigner negativity vanishes only at balanced parity mixture;
        # even the opposite-parity E state has nonstabilizer negativity.
        negative=abs((1-fn)-fp)>1e-12
        assert (w['min']< -1e-12)==negative
        rows.append({'false_negative_probability':fn,'false_positive_probability':fp,
          'output_transmission':transmission,'reported_herald_probability':reported_accept,
          'delivered_herald_per_attempt':transmission*reported_accept,
          'delivered_true_strange_per_attempt':transmission*true_accept,
          'false_herald_from_input_0':fp,
          'posterior_strange_fidelity':fidelity,'conditional_purity':purity,
          'Wigner_min':w['min'],'mana':math.log(w['L1']),
          'Wigner_negative':negative})
    return {'status':'PASS_ASYMMETRIC_ANCILLA_QND_AND_TRANSMISSION_RESOURCE_BUDGET',
      'model':'S vs E parity of supplied qutrit input |1>, symmetric ideal probability half each, asymmetric classical outcome errors, independent photon transmission',
      'negative_Wigner_iff':'false_negative + false_positive != 1; the opposite-parity E state is also Wigner-negative, even when Strange fidelity is poor',
      'rows':rows,
      'boundary':'Controlled-R is imported non-Clifford-capable interaction; detector and loss values are hypothetical, no hardware feasibility claim.'}


def small_7color_chain():
    # Exact real quantum spectral check with 7 mutually noncommuting W33 directions.
    import networkx as nx
    G=nx.complement(nx.from_numpy_array(base.ADJ))
    clique=next(c for c in nx.find_cliques(G)if len(c)==7)
    assert all(not base.ADJ[a,b] for a,b in itertools.combinations(clique,2))
    # Restrict one fixed outcome to each of 7 noncommuting directions.
    # For periodic N sites, diagonal energy epsilon times disagreeing neighbors.
    eps=-2/3
    data=[]
    for N in (2,3,4,5):
        d=7**N
        ids=np.arange(d,dtype=np.int64)
        digits=np.stack([(ids//(7**k))%7 for k in range(N)],axis=1)
        bonds=sum((digits[:,i]!=digits[:,(i+1)%N])for i in range(N))
        diagonal=eps*bonds.astype(float)
        for h in (.12,.5):
            def mv(v):
                X=v.reshape((7,)*N)
                Y=(diagonal*v).reshape((7,)*N)
                for axis in range(N):
                    Y=Y-h/7*np.sum(X,axis=axis,keepdims=True)
                return Y.ravel()
            A=LinearOperator((d,d),matvec=mv,dtype=float)
            eigs=np.sort(eigsh(A,k=2,which='SA',tol=1e-8,maxiter=2500,return_eigenvectors=False))
            assert eigs[1]>eigs[0]
            data.append({'N':N,'h':h,'Hilbert_dimension':d,'ground_energy':float(eigs[0]),
                         'finite_gap':float(eigs[1]-eigs[0]),'energy_per_site':float(eigs[0]/N)})
    return {'status':'PASS_TRUNCATED_7_TICK_QUANTUM_CHAIN_LENGTH_SCALING',
      'subspace':'7 selected pairwise noncommuting W33 directions, one outcome per direction; NOT all 120 on each site',
      'coupling_epsilon':eps,'periodic_chain_results':data,
      'boundary':'N<=5 finite lattices and restricted 7-state local space; no 120-local-site thermodynamic quantum phase proven.'}


def qutrit_mds_erasure_code():
    # [[3,1,2]]_3 perfect erasure code, polynomial evaluation over F3.
    # Local qutrits indexed 0,1,2; source logical s=0,1,2.
    V=np.zeros((27,3),dtype=complex)
    for s in range(3):
        for t in range(3):
            x,y,z=t,(s+t)%3,(s+2*t)%3
            V[x*9+y*3+z,s]+=1/math.sqrt(3)
    assert np.linalg.norm(V.conj().T@V-np.eye(3))<1e-12
    rng=np.random.default_rng(310105)
    a=rng.normal(size=3)+1j*rng.normal(size=3);a/=np.linalg.norm(a)
    rho=np.outer(a,a.conj());psi=V@a
    conditions=[]
    for erased in (0,1,2):
        K=np.zeros((3,9,3),dtype=complex)
        for t in range(3):
            for s in range(3):
                for xyz in itertools.product(range(3),repeat=3):
                    if xyz[erased]!=t:continue
                    kept=[xyz[j]for j in range(3)if j!=erased]
                    K[t,kept[0]*3+kept[1],s]=V[xyz[0]*9+xyz[1]*3+xyz[2],s]
        dec=np.column_stack([math.sqrt(3)*K[t,:,s] for t in range(3) for s in range(3)])
        assert np.linalg.norm(dec.conj().T@dec-np.eye(9))<1e-12
        for t,u in itertools.product(range(3),repeat=2):
            assert np.linalg.norm(K[t].conj().T@K[u]-(np.eye(3)/3 if t==u else np.zeros((3,3))))<1e-12
        remaining=sum(K[t]@rho@K[t].conj().T for t in range(3))
        decoded=dec.conj().T@remaining@dec
        expected=np.kron(np.eye(3)/3,rho)
        residual=float(np.linalg.norm(decoded-expected))
        assert residual<1e-12
        conditions.append({'erased_site':erased,'decode_state_error':residual})
    erasures=[]
    for p in (.001,.005,.01,.02,.05,.1,.25,.4,.6):
        success=(1-p)**3+3*p*(1-p)**2
        erasures.append({'per_carrier_erasure':p,'one_qutrit_unencoded_success':1-p,
              'three_qutrit_encoded_recovery_probability':success,'gain':success-(1-p)})
    assert all(row['gain']>0 for row in erasures if row['per_carrier_erasure']<.5)
    return {'status':'PASS_EXPLICIT_QUTRIT_3_1_2_ERASURE_CODE_DECODER',
       'logical_to_physical_isometry':'|s_L>=sum_{t in GF3}|t,s+t,s+2t>/sqrt3',
       'erased_site_exact_recovery':conditions,'erasure_curve':erasures,
       'recoverable_one_erasure_probability':'1-3p^2+2p^3',
       'boundary':'Three physical qutrits with entangling preparation, erasure location known, ideal decoding. NOT a one-photon 160-rail code, and not independent unknown Pauli error correction.'}



def erasure_encoded_floquet_edge():
    """Tie the exact [[3,1,2]]_3 qutrit code to native SWAP exposure."""
    rows=[]
    for L in (4,6,8):
        at={(x,y):(x,y)for x in range(L)for y in range(L)}
        exposure=Counter({p:0 for p in at})
        for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)):
            for x in range(L):
                for y in range(L):
                    if (x+y)%2:continue
                    q=(x+dx,y+dy)
                    if q not in at:continue
                    p=(x,y)
                    exposure[at[p]]+=1;exposure[at[q]]+=1
                    at[p],at[q]=at[q],at[p]
        where={source:dst for dst,source in at.items()}
        active=sorted(p for p in where if where[p]!=p)
        assert len(active)==2*L-1
        cur=active[0];cycle=[]
        while cur not in cycle:
            cycle.append(cur);cur=where[cur]
        assert len(cycle)==2*L-1 and cur==active[0]
        carriers=cycle[:3]
        counts=[exposure[p]for p in carriers]
        for e_gate in (.0005,.001,.003,.005,.01,.02):
            independent_e=[1-(1-e_gate)**(13*t)for t in counts]
            no_loss=math.prod(1-e for e in independent_e)
            one_loss=sum(e*math.prod(1-independent_e[j] for j in range(3)if j!=i)
                         for i,e in enumerate(independent_e))
            encoded_success=no_loss+one_loss
            bare_success=sum(1-e for e in independent_e)/3
            assert 0<=encoded_success<=1 and 0<=bare_success<=1
            rows.append({'L':L,'native_tick_error':e_gate,'three_consecutive_moving_edge_sources':
              [list(x)for x in carriers],'carrier_swap_stage_counts':counts,
              'per_carrier_erasure_probability':independent_e,
              'encoded_known_erasure_recovery_probability':encoded_success,
              'mean_unencoded_single_carrier_survival':bare_success,
              'encoded_minus_mean_unencoded':encoded_success-bare_success})
    return {'status':'PASS_FLOQUET_CHIRAL_ROUTING_WITH_EXPLICIT_THREE_QUTRIT_ERASURE_CODE',
      'rows':rows,
      'encoding':'[[3,1,2]]_3 quantum erasure code on three separate edge carriers; each sees 13 native ticks per actual SWAP stage',
      'boundary':'Independent detectable erasure only. Includes neither the extra entangling encoder/decoder fault cost nor unflagged depolarizing noise. Code positions migrate and edge geometry supplied.'}

def lorentz_noncompact_no_unitary_rep():
    eta=np.diag([-1.,1.,1.,1.])
    K=np.zeros((4,4));K[0,1]=K[1,0]=1
    boost=expm(.7*K)
    spec=np.sort(np.linalg.eigvals(boost).real)
    assert abs(spec[0]-math.exp(-.7))<1e-12 and abs(spec[-1]-math.exp(.7))<1e-12
    assert np.linalg.norm(boost.T@eta@boost-eta)<1e-12
    # If positive definite G exists with K.T G+G K=0, then K is similar to
    # a real antisymmetric generator and hence has purely imaginary spectrum.
    # Here eig(K)={-1,0,0,+1}; impossible. A finite-dimensional faithful
    # 4-vector Lorentz representation cannot be unitary under positive norm.
    assert np.allclose(sorted(np.linalg.eigvalsh(K)),[-1,0,0,1])
    # Show runaway of the previous proposed ultralocal energy:
    v=np.zeros(4);v[0]=1
    h=-.5*(v@eta@v)
    energy=[float(.5*((t*v)@eta@(t*v)))for t in (1,2,4,8)]
    assert energy==[-.5,-2.,-8.,-32.]
    return {'status':'PASS_LORENTZ_POSITIVE_METRIC_REPRESENTATION_OBSTRUCTION',
      'boost_eigenvalues':spec.tolist(),'noncompact_Lorentz_metric_preserved':True,
      'positive_definite_unitarity_possible':False,'indefinite_oscillator_negative_energy_sequence':energy,
      'explanation':'The real 4-vector SO(1,3) boost has eigenvalues exp(+/-t), not unit modulus. No positive invariant inner product on this nontrivial representation; the previously supplied scalar has unbounded negative timelike quadratic energy.',
      'boundary':'No-go only for naive finite-dimensional positive norm on internal 4-vector representation; constrained gauge theories may remove ghosts and retain physical positive Hilbert space.'}


def spin2_plaquette_gauge_control():
    # SO(2) compact subgroup of Lorentz: exact lattice-gauge curvature and
    # supplied matter/angle/electric canonical variables; not gravity.
    rng=np.random.default_rng(310132)
    dims=(3,3,3)
    J=np.array([[0.,-1.],[1.,0.]])
    x=rng.normal(size=dims+(2,));p=rng.normal(size=dims+(2,))
    a=rng.normal(scale=.2,size=dims+(3,));E=rng.normal(size=dims+(3,))
    theta=rng.normal(scale=.2,size=dims)
    def forward(v,mu):
        z=list(v);z[mu]=(z[mu]+1)%dims[mu];return tuple(z)
    def plaquette(v,mu,nu,links):
        return links[v+(mu,)] + links[forward(v,mu)+(nu,)] - links[forward(v,nu)+(mu,)] - links[v+(nu,)]
    def act(x,p,a,E):
        kinetic=.5*(np.sum(p*p)+np.sum(E*E));link=0.;curv=0.
        for v in np.ndindex(dims):
            for mu in range(3):
                dest=forward(v,mu)
                ang=a[v+(mu,)];c,s=math.cos(ang),math.sin(ang)
                R=np.array([[c,-s],[s,c]])
                d=x[dest]-R@x[v];link+=.5*float(d@d)
            for mu,nu in itertools.combinations(range(3),2):
                curv+=1-math.cos(plaquette(v,mu,nu,a))
        return kinetic+link+.7*curv
    a_new=a.copy();x_new=x.copy();p_new=p.copy()
    for v in np.ndindex(dims):
        ang=theta[v];c,s=math.cos(ang),math.sin(ang)
        R=np.array([[c,-s],[s,c]])
        x_new[v]=R@x[v];p_new[v]=R@p[v]
        for mu in range(3):a_new[v+(mu,)]+=theta[forward(v,mu)]-theta[v]
    err=abs(act(x,p,a,E)-act(x_new,p_new,a_new,E))
    assert err<1e-9
    # The Gauss generator is G_v=p_v . J x_v + incoming E - outgoing E.
    # Finite gauge variations of action are canonical Ward zero, when E is dynamic.
    site=(1,1,1)
    def local_delta(scale):
        t=np.zeros(dims);t[site]=scale
        xn=x.copy();pn=p.copy();an=a.copy()
        for v in np.ndindex(dims):
            th=t[v];c,s=math.cos(th),math.sin(th)
            R=np.array([[c,-s],[s,c]])
            xn[v]=R@x[v];pn[v]=R@p[v]
            for mu in range(3):an[v+(mu,)]+=t[forward(v,mu)]-th
        return act(xn,pn,an,E)
    derivative=(local_delta(1e-5)-local_delta(-1e-5))/(2e-5)
    assert abs(derivative)<1e-7
    return {'status':'PASS_SPATIAL_LINK_CURVATURE_U1_GAUSS_CONTROL_WITH_ELECTRIC_MOMENTA',
      'spatial_lattice':[3,3,3],'action_gauge_invariance_error':err,
      'canonical_local_Gauss_Ward_derivative':abs(derivative),
      'scope':'SO2/U1 compact submodel of a Lorentz rotation; actual dynamical link and electric momenta restore Abelian gauge symmetry. No Palatini/Hamiltonian ADM constraints or full SO(1,3) gravity derived.'}


def build():
    tasks={
     '01_exact_optical_projector_phase_control':local_spectral_projection_and_phase_noise,
     '02_160_mode_adjacent_Givens_encoder':compile_encoder_givens,
     '03_QND_asymmetric_readout_and_loss':qnd_asymmetric_resource_accounting,
     '04_quantum_7clock_truncation_finite_scaling':small_7color_chain,
     '05_three_qutrit_erasure_edge_code':qutrit_mds_erasure_code,
     '06_encoded_Floquet_edge_erasure_transport':erasure_encoded_floquet_edge,
     '07_lattice_gauge_curvature_Gauss':spin2_plaquette_gauge_control,
     '08_outsidebox_Lorentz_ghost_no_positive_norm':lorentz_noncompact_no_unitary_rep,
    }
    results={}
    for label,func in tasks.items():
        results[label]=func();print(label,results[label]['status'],flush=True)
    return {'schema':'w33.20261031.server.continuation.eight.fronts.v1',
      'results':results,
      'scope':'Five requested physics fronts (optics, QND, quantum clock, noisy edge decoding, curvature/Gauss) plus three independent novel ideas: 4hop polynomial projector, explicit qutrit quantum erasure, Lorentz positive-metric obstruction. Eight computational modules with optical and edge fronts split into two each.',
      'reference_head':'15b3e3288fed8ba560a3c37ededafb3e4ad86749'}

if __name__=='__main__':
    output=build();OUT.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print('FROZEN',OUT)
