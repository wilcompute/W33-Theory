"""Five independently reproducible TOE/photonic falsification gates (2026-11-19).

1. Native 3-time qutrit memory: exact depolarizing-noise threshold, all
   pairwise-classical decompositions retained as CPTP Kraus instruments.
2. Qutrit SIC SU(3) baryons: exhaustive *exact* cyclotomic Jacobian ranks for
   4096 translation-orbit subsets, with minimal full-rank cardinality 27.
3. Color-dependent SU(3) readout: finite 9-Weyl/3-shift twirls undo bias.
4. Albert/G2: 27=6*1+3*7, with centralizer / degeneracy restriction.
5. Causal orientations: a cubic arrow statistic detects 23/24 dual pairs of
   5-event posets; one exact blind pair remains.

These are mathematical/experimental-model controls, not a Theory of Everything.
"""
from __future__ import annotations
from itertools import combinations, permutations, product
from collections import Counter, defaultdict
from pathlib import Path
import json
import math
import numpy as np
from scipy.optimize import brentq
import sympy as sp
from sympy.polys.matrices import DomainMatrix

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'toe_20261119_five_physics_gates_v3.json'
I3=np.eye(3,dtype=complex)
w=np.exp(2j*np.pi/3)
X=np.roll(I3,1,axis=0)
Z=np.diag([1,w,w*w])
F=np.array([[w**(i*j) for j in range(3)] for i in range(3)],complex)/np.sqrt(3)


def app(Ks,rho):
    return sum((K@rho@K.conj().T for K in Ks),np.zeros((3,3),complex))
def tp(Ks):
    return float(np.linalg.norm(sum((K.conj().T@K for K in Ks),np.zeros((3,3),complex))-I3))
def choi(Ks):
    return np.block([[app(Ks,np.outer(I3[:,i],I3[:,j].conj()))
                      for j in range(3)] for i in range(3)])
def depol_ops(e):
    return ([np.sqrt(1-e)*I3] if e<1 else [])+[np.sqrt(e/9)*np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b) for a,b in product(range(3),repeat=2)]
def after(Ks,Ls):
    return [L@K for K in Ks for L in Ls]
def prep(v):
    return [np.outer(v,I3[:,k].conj()) for k in range(3)]
def native_channels(g,e):
    E1=[np.sqrt(1-g)*I3]+[np.sqrt(g)*np.outer(I3[:,0],I3[:,j].conj()) for j in range(3)]
    EB=[np.outer(I3[:,j],I3[:,j].conj()) for j in range(3)]
    EC=[np.outer(F[:,j],F[:,j].conj()) for j in range(3)]
    return E1,after(EB,depol_ops(e)),after(EC,depol_ops(e))

def memory_noise_gate():
    cases=[]
    for g in (.05,.36,.75,1.0):
        def W(e):
            a=1-2*e/3; b=e/3
            return 6*(2*math.sqrt(a*b)+b)-2*g
        critical=brentq(W,1e-15,.5)
        cases.append({'gamma':g,'critical_output_depolarizing_fraction':critical,
          'witness_at_zero_noise':W(0.),'witness_at_one_pct':W(.01),
          'negative_at_one_pct':bool(W(.01)<0)})
    errmax=0.; tpmax=0.; checked=[]
    for g,e in ((.36,0.),(.36,.005),(.36,.01),(.36,.02),(.75,.03)):
        E1,E2,E3=native_channels(g,e);D=depol_ops(e)
        for channel in (E1,E2,E3):tpmax=max(tpmax,tp(channel))
        # For each first channel, a different Kraus instrument encodes the
        # subsequent dephasing basis; its sum is the SAME replacement E1.
        for basis,target in ((I3,E2),(F,E3)):
            K=[np.sqrt(1-g)*I3]+[np.sqrt(g)*np.outer(I3[:,0],basis[:,j].conj()) for j in range(3)]
            DB=[np.outer(basis[:,j],basis[:,j].conj()) for j in range(3)]
            feedback=[after(DB,D)]+[after(prep(basis[:,j]),D) for j in range(3)]
            comp=[A@k for k,L in zip(K,feedback) for A in L]
            errmax=max(errmax,float(np.linalg.norm(choi(comp)-choi(target))),
                       float(np.linalg.norm(choi(K)-choi(E1))))
            for fs in feedback:tpmax=max(tpmax,tp(fs))
        # Dephased + depolarized E2 is mixed unitary. Each branch can be
        # inverted on the system, so the E2 -> E3' pair is classically feasible.
        mix=[]
        for a,b in product(range(3),repeat=2):
            U=np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b)
            p=(1-e)/3*(a==0)+e/9
            mix.append((math.sqrt(p)*U,U))
        K=[entry[0] for entry in mix]
        fb=[[A@U.conj().T for A in E3] for _,U in mix]
        comp=[A@k for k,L in zip(K,fb) for A in L]
        errmax=max(errmax,float(np.linalg.norm(choi(K)-choi(E2))),
                   float(np.linalg.norm(choi(comp)-choi(E3))))
        for fs in fb:tpmax=max(tpmax,tp(fs))
        # Faithful quantum fidelity for each pair of noisy orthogonal outputs.
        a=1-2*e/3;b=e/3
        root_f=2*math.sqrt(a*b)+b
        measured=[]
        for ch,basis in ((E2,I3),(E3,F)):
            for i,j in combinations(range(3),2):
                R=app(ch,np.outer(basis[:,i],basis[:,i].conj()))
                S=app(ch,np.outer(basis[:,j],basis[:,j].conj()))
                va,Ua=np.linalg.eigh(R)
                sq=Ua@np.diag(np.sqrt(np.maximum(va,0)))@Ua.conj().T
                ev=np.linalg.eigvalsh(sq@S@sq)
                measured.append(float(sum(np.sqrt(np.maximum(ev,0)))))
        assert max(abs(x-root_f) for x in measured)<2e-7
        checked.append({'gamma':g,'epsilon':e,'pairwise_fidelity_sum':sum(measured),
                        'analytical_witness':6*root_f-2*g})
    assert errmax<1e-12 and tpmax<1e-12
    return {'theorem_source':'Beyer et al 2026 arXiv:2611.17268 supplement VI Eq S38',
       'noise_model':'E2,E3 each postprocessed by Lambda_e(rho)=(1-e)rho+e Tr(rho) I/3; E1 unchanged',
       'formula':'W=6*(2 sqrt[(1-2e/3)*(e/3)] + e/3)-2 gamma',
       'all_three_pairs_remain_classically_decomposable':True,
       'pairwise_kraus_choi_error_max':errmax,'kraus_tp_error_max':tpmax,
       'exact_pairwise_decomposition':'E1 instrument in Z or Fourier basis then output depol; E2 random Weyl branch followed by inverse and E3',
       'noise_critical_table':cases,'reproduced_tests':checked,
       'interpretation':'For gamma=.36 witness ceases to certify after just over 1% output depolarization. W>=0 does not mean memory becomes classical. Common quantum realization persists after postprocessing.'}


def dimension_scaling_gate():
    # Constructive general-d extension of the native qutrit pattern.
    # E1=(1-gamma)Id + gamma|0><0|Tr, E2/E3=MUB dephasings
    # followed by identical depolarizing channels. The published
    # general-d MUB witness yields W=(d-1)[d F_pair - gamma].
    g=.36;rows=[]
    for d in (2,3,4,5,6,9,12):
        f=lambda e:2*math.sqrt((1-e+e/d)*(e/d))+(d-2)*e/d
        W=lambda e:(d-1)*(d*f(e)-g)
        root=brentq(W,1.e-16,.5)
        rows.append({'dimension':d,'critical_depolarizing_fraction':root,
                     'small_gamma_approx_gamma_sq_over_4d':g*g/(4*d),
                     'witness_at_eps_0':W(0),
                     'witness_at_eps_0p01':W(.01)})
    assert all(rows[i]['critical_depolarizing_fraction']>rows[i+1]['critical_depolarizing_fraction']
               for i in range(len(rows)-1))
    assert abs(rows[1]['critical_depolarizing_fraction']-.010263207615968257)<1e-10
    return {'dimension_independent_construction':'E1=(1-g)Id+g|0><0|Tr; E2/E3 two MUB complete dephasings, optionally both followed by depolarizing noise',
      'published_witness_plus_our_explicit_channels':'W_d=(d-1)[d*(2 sqrt((1-e+e/d)*(e/d))+(d-2)*e/d)-gamma]',
      'pairwise_classical_constructions_exist_for_any_d':True,
      'proof':'First E1 Kraus instrument resolved in either MUB and basis-conditional reprepare; E2 mixed Weyl-Z random phases and a uniform d^2-Weyl depolarizing mixture, with branchwise inverse and E3 feedback',
      'noise_strength_gamma':g,'critical_noise_table':rows,
      'noise_fragility_asymptotic_small_gamma':'epsilon_critical~gamma^2/(4d), fixed dimension d, gamma->0',
      'scope':'New family/robustness deduction from Beyer et al dimension-d witness, not a novel quantum-memory theorem or an experimental implementation.'}

def baryon_orbit_gate():
    # Rational cyclotomic field Q(omega) exact ranks: omega^2+omega+1=0.
    s=sp.sqrt(-3); omega=(-1+s)/2
    XS=sp.Matrix([[0,0,1],[1,0,0],[0,1,0]])
    ZS=sp.diag(1,omega,omega**2)
    v=sp.Matrix([1,-1,0])
    P=sp.Matrix.hstack(*[XS**b*ZS**a*v for b in range(3) for a in range(3)])
    trips=list(combinations(range(9),3));index={t:i for i,t in enumerate(trips)}
    rows=[]
    for triple in trips:
        row=[sp.S.Zero]*27
        for j,k in enumerate(triple):
            for coord in range(3):
                C=P[:,list(triple)].copy();C[:,j]=sp.eye(3)[:,coord]
                row[3*k+coord]=sp.simplify(sp.expand(C.det()))
        rows.append(row)
    field=sp.QQ.algebraic_field(s)
    DM=DomainMatrix.from_Matrix(sp.Matrix(rows)).convert_to(field)
    assert DM.rank()==19
    def shift(k,da,db):return 3*((k//3+db)%3)+(k%3+da)%3
    unseen=set(trips);orbits=[]
    while unseen:
        t=min(unseen)
        orb=tuple(sorted({tuple(sorted(shift(i,a,b) for i in t)) for a,b in product(range(3),repeat=2)}))
        unseen.difference_update(orb);orbits.append(orb)
    orbits.sort(key=lambda o:(len(o),o))
    assert len(orbits)==12 and sorted(map(len,orbits))==[3]*4+[9]*8
    stats=defaultdict(Counter);winning=None
    for mask in range(1<<12):
        picks=[index[t] for i,o in enumerate(orbits) if (mask>>i)&1 for t in o]
        if len(picks)>27:continue
        rank=DM.extract(picks,list(range(27))).rank() if picks else 0
        stats[len(picks)][rank]+=1
        if rank==19 and (winning is None or len(picks)<winning[0]):
            winning=(len(picks),mask,rank,picks)
    assert winning[0]==27
    assert all(max(stats[n])<19 for n in stats if n<27)
    assert sum(v for key,v in stats[27].items() if key==19)==72
    orbit_count=sum(len(orbits[i]) for i in range(12) if winning[1]>>i&1)
    assert orbit_count==27
    return {'field':'Q(omega), omega^2+omega+1=0, exact rational algebraic rank',
        'SIC_fiducial':'(1,-1,0); X^b Z^a orbit labelled (a,b) in F3^2',
        'baryon_coordinate_count':84,'full_jacobian_rank':19,
        'translation_group':'F3^2 acts on nine species indices by (a,b)->(a+u,b+v)',
        'translation_triple_orbit_sizes':[3]*4+[9]*8,
        'translation_closed_subsets_examined':4096,
        'full_rank_minimum_closed_baryon_count':27,
        'minimum_closed_subset_winning_orbit_indices':[i for i in range(12) if winning[1]>>i&1],
        'minimum_closed_subset_winning_baryon_index_list':winning[3],
        'minimum_27_subset_full_rank_count':72,
        'rank_census_through_27':{str(size):{str(r):num for r,num in sorted(count.items())}
             for size,count in sorted(stats.items())},
        'raw_19_constraints_not_translation_closed':True,
        'unpaired_linear_multiplier_count_if_27_massless_singlets':27-19,
        'caveat':'A 19-dimensional invariant SPACE of linear COMBINATIONS might exist; obstruction only applies to subsets of coordinate baryons. Chosen b_ijk constants may still explicitly break translation symmetry. Additional multiplier mass terms may lift eight zero modes but must be gauge/symmetry legal.'}


def random_su3(rng):
    M=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    Q,R=np.linalg.qr(M);Q=Q@np.diag(np.diag(R)/abs(np.diag(R)))
    return Q/np.linalg.det(Q)**(1/3)

def twirl_gate():
    rng=np.random.default_rng(26111933)
    etas=[np.diag([.4,1.,1.6]).astype(complex)]
    U=random_su3(rng);etas.append(U@etas[0]@U.conj().T)
    ws=[np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b) for a,b in product(range(3),repeat=2)]
    max9=max3=0.;individual=[]
    for eta in etas:
        normalized=eta/np.trace(eta)
        nine=sum((U.conj().T@eta@U for U in ws),np.zeros((3,3),complex))/9
        assert np.linalg.norm(nine-np.trace(eta)/3*I3)<1e-12
        if np.linalg.norm(eta-np.diag(np.diag(eta)))<1e-12:
            three=sum((np.linalg.matrix_power(X,a).conj().T@eta@np.linalg.matrix_power(X,a)
                 for a in range(3)),np.zeros((3,3),complex))/3
            assert np.linalg.norm(three-np.trace(eta)/3*I3)<1e-12
        for j in range(24):
            A,B=random_su3(rng),random_su3(rng)
            K=A@B@A.conj().T@B.conj().T
            target=np.trace(K)
            obs=lambda V: 3*np.trace(eta@V@K@V.conj().T)/np.trace(eta)
            a0=abs(obs(I3)-target)
            nine_avg=sum(obs(U) for U in ws)/9
            three_avg=sum(obs(np.linalg.matrix_power(X,a)) for a in range(3))/3
            max9=max(max9,abs(nine_avg-target))
            max3=max(max3,abs(three_avg-target))
            if j==0:individual.append({'eta_type':'diagonal' if eta is etas[0] else 'rotated',
                'uncompensated_error':float(a0),
                'three_shift_error':float(abs(three_avg-target)),
                'nine_Weyl_error':float(abs(nine_avg-target))})
    assert max9<1e-12
    v=.8;eps=.2;delta=.01
    N=math.ceil(36/(v*v*eps*eps)*math.log(4/delta))
    return {'readout_model':'m(V)=3 Tr[eta V K V†]/Tr eta, eta positive fixed lab detector',
      'exact_nine_Weyl_identity':'(1/9) sum_(a,b) (X^a Z^b)† eta (X^a Z^b)=(Tr eta/3) I',
      'exact_three_shift_identity_for_diagonal_eta':'(1/3) sum_a (X^a)† eta X^a=(Tr eta/3) I',
      'max_complex_trace_error_9_setting_48_trials':float(max9),
      'max_complex_trace_error_3_setting_48_trials':float(max3),
      'example_errors':individual,
      'accepted_detections_per_phase_sufficient_Hoeffding':N,
      'assumptions':'9 or 3 exact coherent conjugation settings; same visibility/phase at each setting; independent balanced Bernoulli detections; uniform setting allocation; no nonlinear detector effects. Twirling transforms actual controlled circuit, not a passive change of gauge.',
      'prior_theorem':'Qutrit Weyl operators are a unitary 1-design; application to nonuniform Holonet readout is this certificate.'}


def g2_gate():
    # Compute skew real 7x7 infinitesimal stabilizer of standard positive Fano form.
    triples=[(0,1,2,1),(0,3,4,1),(0,5,6,1),(1,3,5,1),
             (1,4,6,-1),(2,3,6,-1),(2,4,5,-1)]
    tensor=np.zeros((7,7,7),dtype=int)
    for a,b,c,sgn in triples:
        for perm in permutations((a,b,c)):
            parity=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
            tensor[perm]=sgn*(-1 if parity%2 else 1)
    pairs=list(combinations(range(7),2))
    basis=[]
    for i,j in pairs:
        E=np.zeros((7,7),dtype=int);E[i,j]=1;E[j,i]=-1;basis.append(E)
    rows=[]
    for a,b,c in combinations(range(7),3):
        rows.append([sum(E[a,k]*tensor[k,b,c]+E[b,k]*tensor[a,k,c]+E[c,k]*tensor[a,b,k]
                        for k in range(7)) for E in basis])
    M=sp.Matrix(rows)
    assert M.rank()==7 and len(M.nullspace())==14
    generators=[]
    for coords in M.nullspace():
        E=sp.zeros(7)
        for coeff,B in zip(coords,basis):
            if coeff:E+=coeff*sp.Matrix(B)
        generators.append(E)
    # Schur commutant on the real fundamental: matrices commuting with all
    # 14 positive compact g2 generators are scalar multiples of I7.
    commrows=[]
    for E in generators:
        for i in range(7):
            for j in range(7):
                coeff=[]
                for a in range(7):
                    for b in range(7):
                        coeff.append((1 if i==a else 0)*E[b,j]-E[i,a]*(1 if b==j else 0))
                commrows.append(coeff)
    rank=sp.Matrix(commrows).rank()
    assert rank==48
    # Albert real 27 = diagonal R^3 + 3 offdiagonal octonions O:
    # O=R + Im(O)=1+7 under compact G2, so 27=6*1+3*7.
    rng=np.random.default_rng(160627)
    A=rng.normal(size=(6,6));S=(A+A.T)/2
    B=rng.normal(size=(3,3));T=(B+B.T)/2
    mass=np.zeros((27,27));mass[:6,:6]=S;mass[6:,6:]=np.kron(T,np.eye(7))
    maxcomm=0.
    for E in generators:
        G=np.zeros((27,27));G[6:,6:]=np.kron(np.eye(3),np.array(E).astype(float))
        maxcomm=max(maxcomm,float(np.linalg.norm(G@mass-mass@G)))
    expected=np.sort(np.repeat(np.linalg.eigvalsh(T),7))
    actual=np.sort(np.linalg.eigvalsh(mass[6:,6:]))
    assert maxcomm<1e-11 and np.max(abs(expected-actual))<1e-11
    return {'real_Albert_G2_branching':'H3(O) 27 = R^3 diagonal + 3 O = 6 trivial singlets + 3 real irreducible sevens',
     'fano_form_3_index_equations':35,'skew_generator_variables':21,
     'exact_skew_stabilizer_constraint_rank':int(M.rank()),
     'G2_generator_count':len(generators),
     'exact_real_7d_G2_commutant_rank':int(rank),
     'real_7d_commutant_dimension':49-rank,
     'real_symmetric_G2_equivariant_mass_parameter_count':21+6,
     'example_27d_mass_commutator_residual':maxcomm,
     'example_7fold_mass_multiplicity_exact':True,
     'meaning':'Real G2-invariant quadratic masses on 6*1+3*7 contain arbitrary symmetric 6x6 singlet block and symmetric 3x3 multiplicity block times I7. Any G2 charged seven has sevenfold degeneracy; neither family chirality nor observed mass spectrum is thereby derived.'}


def causal_gate():
    n=5;pairs=list(combinations(range(n),2));perms=list(permutations(range(n)))
    def closure(edges):
        A=np.zeros((n,n),dtype=np.int8)
        for a,b in edges:A[a,b]=1
        for k in range(n):
            for i in range(n):
                for j in range(n):A[i,j]|=A[i,k]&A[k,j]
        return A
    def key(A):
        return min(''.join(str(int(A[i,j])) for i in pi for j in pi) for pi in perms)
    representatives={}
    for mask in range(1<<len(pairs)):
        A=closure([t for b,t in enumerate(pairs) if mask>>b&1])
        representatives.setdefault(key(A),A)
    assert len(representatives)==63
    nonself=[];self_count=0;seen=set()
    def arrow(A):
        past=A.sum(axis=0).astype(int);future=A.sum(axis=1).astype(int)
        return int(sum(past**3-future**3))
    for key0,A in representatives.items():
        if key0 in seen:continue
        dual=key(A.T);seen.update((key0,dual))
        if dual==key0:self_count+=1;continue
        nonself.append((key0,dual,arrow(A)))
        assert arrow(A.T)==-arrow(A)
        H=np.zeros((n,n),dtype=float)
        for i,j in pairs:
            if A[i,j] and not any(A[i,k] and A[k,j] for k in range(n)):H[i,j]=1
        G=np.linalg.inv(1.3*np.eye(n)-.6*H)
        Gdual=np.linalg.inv(1.3*np.eye(n)-.6*H.T)
        assert abs(np.linalg.norm(G,'fro')-np.linalg.norm(Gdual,'fro'))<1e-12
        assert np.linalg.norm((G-G.T)+(Gdual-Gdual.T))<1e-12
    blind=[{'poset_key':k,'dual_key':d} for k,d,s in nonself if s==0]
    assert self_count==15 and len(nonself)==24 and len(blind)==1
    assert sum(s!=0 for _,_,s in nonself)==23
    return {'five_event_isomorphism_classes':63,
      'self_dual_order_classes':self_count,'distinct_nonselfdual_pairs':len(nonself),
      'odd_arrow_statistic':'A3(P)=sum_i [number_of_predecessors(i)^3-number_of_successors(i)^3]',
      'duality_rule':'A3(P^op)=-A3(P)',
      'nonself_dual_pairs_detected':sum(s!=0 for _,_,s in nonself),
      'nonself_dual_pairs_blind':len(blind),'blind_poset_keys':blind,
      'unoriented_inverse_response_invariant':'|| (mI-alpha H)^-1 ||_F^2 unchanged by H->H.T',
      'boundary_sensitive_response':'G-G.T reverses sign under duality. Its signed matrix elements require oriented preparation/readout labels.',
      'caution':'A signed cubic count is not a physical time arrow or gravity action and fails to distinguish one nonselfdual pair; a true T-symmetric theory need not prefer P to P^op.'}


def run():
    results={'date':'2026-11-19','baseline_commit':'366aefd1189eed06ed9f5c34b6420d7d457fa475',
      'falsifier_status':'Five independent math/quantum toy controls; NOT a validated TOE.'}
    results['native_qutrit_noise']=memory_noise_gate()
    results['all_dimension_MUB_noise_scaling']=dimension_scaling_gate()
    results['SIC_H27_baryon_coordinate_orbits']=baryon_orbit_gate()
    results['SU3_detector_Weyl_twirl']=twirl_gate()
    results['real_G2_Albert_multiplets']=g2_gate()
    results['causal_oriented_invariant']=causal_gate()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(results,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('ALL FIVE PHYSICS GATES PASSED')
    print('QUTRIT noise epsilon_critical gamma=.36',results['native_qutrit_noise']['noise_critical_table'][1]['critical_output_depolarizing_fraction'])
    print('BARYON min exact H27 translation-closed full-rank set',results['SIC_H27_baryon_coordinate_orbits']['full_rank_minimum_closed_baryon_count'])
    print('SU3 9-Weyl twirl error',results['SU3_detector_Weyl_twirl']['max_complex_trace_error_9_setting_48_trials'])
    print('G2 real Albert sector',results['real_G2_Albert_multiplets']['real_Albert_G2_branching'])
    print('CAUSAL arrow 5-poset nonselfdual pairs',results['causal_oriented_invariant']['nonself_dual_pairs_detected'],'of',results['causal_oriented_invariant']['distinct_nonselfdual_pairs'])
    print('JSON',OUT)
    return results
if __name__=='__main__':run()
