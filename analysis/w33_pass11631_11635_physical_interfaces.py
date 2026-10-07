"""Five user-requested interfaces; supplied actions are not a complete TOE.

Owners11630: Reye instrument;11625-29: finite CP sectors and shell action;
8909-16: selected D4; Eisenstein weld: Coxeter quotient; BT547/5031:
tree probabilities/count;11316/11323/11386: spin-two and cycle/hub controls.
"""
from pathlib import Path
import itertools as it
import json
import sys
from collections import Counter
import hashlib
import numpy as np
import sympy as s
import networkx as nx
from scipy.linalg import expm,logm
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
OUT=ROOT/'data/w33_pass11631_11635_physical_interfaces.json'
# Advisory combination-token candidates are credited as broader context,
# not as owners of the specific pulse/CP/slant/normal/ensemble maps below.
CONTEXT_OWNERS=[
 'analysis/BT1601_BT1603_physical_fano_universal_closure.md',
 'analysis/BT1602_fano_witting_detector_bin_synthesis.md',
 'analysis/BT1697_holonet_typed_packet_abi.md',
 'analysis/BT1893_BT1895_summary.md',
 'PASS1030_EIGHTY_CARRIER_ORIENTATION_OBSTRUCTION.md',
 'W33_FOR_EVERYONE.tex',
 'analysis/BT1741_BT1744_execution_summary.md',
 'analysis/PASS11070_11075_ORIENTED_CHAMBER_LOCAL_E8_NERVE.md',
 'analysis/BT4049_BT4056_five_front_outside_box.md',
 'analysis/BT1707_BT1709_qubit_contextuality_hesse_bridge.md',
 'analysis/BT1745_BT1748_execution_summary.md',
 'analysis/BT1745_June24_25_commit_audit.md']


def read(name):return json.loads((ROOT/'data'/name).read_text())
def cm(rows):return np.array([[complex(s.sympify(z)) for z in r] for r in rows])
def complex_pack(A):return [[[float(z.real),float(z.imag)] for z in r] for r in A]

def microscopic_instrument():
    d=read('w33_pass11630_reye_witting_instrument.json')['instrument']
    L=cm(d['projective_matrix']);U=cm(d['polar_unitary'])
    I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    S=np.kron(Y,I);pm=(np.eye(4)-S)/2;pp=np.eye(4)-pm
    r=2-np.sqrt(3);theta=np.arccos(np.sqrt(r));p=(3-np.sqrt(3))/2
    # Ancilla first. Only one-body ancilla Y and two-body YaY1 are used.
    Hfilter=theta*np.kron(Y,pm)
    W=expm(-1j*Hfilter)
    D=pp+np.sqrt(r)*pm;E=np.sqrt(1-r)*pm
    assert np.allclose(W,np.block([[D,-E],[E,D]]),atol=2e-14)
    Hpolar=1j*logm(U);assert np.max(abs(Hpolar-Hpolar.conj().T))<1e-12
    Hpolar=(Hpolar+Hpolar.conj().T)/2
    paulis=[I,X,Y,Z];labels='IXYZ';coeff={}
    for i,j in it.product(range(4),repeat=2):
        c=np.trace(np.kron(paulis[i],paulis[j])@Hpolar)/4
        assert abs(c.imag)<1e-12;coeff[labels[i]+labels[j]]=float(c.real)
    H2=sum(coeff[labels[i]+labels[j]]*np.kron(paulis[i],paulis[j]) for i,j in it.product(range(4),repeat=2))
    assert np.max(abs(expm(-1j*H2)-U))<2e-13
    total=np.kron(I,expm(-1j*H2))@W
    assert np.max(abs(total[:4,:4]-L/np.sqrt(1+1/np.sqrt(3))))<2e-13
    # Failure is U E rather than E; same effect, explicitly retained output.
    assert np.allclose(total[4:,:4],U@E)
    initial=np.ones(4)/2;readout=np.kron(np.array([[1,1]])/np.sqrt(2),I)
    q=readout@total[:4,:4]@initial;success=np.vdot(q,q).real
    assert abs(success-5*(3-np.sqrt(3))/12)<1e-13
    noise=[]
    for delta,a in it.product([-.02,0.,.02],[0.,.01,.05]):
        wa=expm(-1j*(theta+delta)*np.kron(Y,pm))
        ww=np.kron(I,U)@wa
        rho=(1-a)*np.diag([1.,0.])+a*np.diag([0.,1.])
        full=ww@np.kron(rho,np.outer(initial,initial))@ww.conj().T
        out=readout@full[:4,:4]@readout.conj().T;pr=np.trace(out).real;out/=pr
        bloch=[float(np.trace(A@out).real) for A in [X,Y,Z]]
        noise.append(dict(angle_offset=delta,ancilla_bit_error=a,success=pr,Bloch=bloch,
                          Hadamard_distillable=abs(bloch[0])+abs(bloch[2])>1))
    # Exact-norm resource margin: contraction+normalization uses no IID noise assumption.
    radius=np.sqrt(success)/(10*np.sqrt(2))
    return dict(status='PASS',filter_angle=theta,filter_Hamiltonian='theta/2 Ya - theta/2 Ya Y1; second system qubit is spectator',
        polar_Pauli_coefficients=coeff,polar_Hamiltonian=complex_pack(H2),
        pulse_schedule=['Prepare ancilla|0>, system|++>','Evolve Hfilter for unit time','Evolve Hpolar on system for unit time','Measure ancilla Z; keep0','Measure first system qubit X; keep+'],
        unitary=complex_pack(total),numerical_pulse_error=float(np.max(abs(expm(-1j*H2)-U))),
        total_success=success,explicit_noise_trials=noise,
        sufficient_coherent_unitary_error=radius,
        error_bound='If total pre-readout unitary operator-norm error is epsilon, the normalized successful pure state has trace-norm error<=4epsilon/sqrt(p_total). Its x/z magic margin is>=2/5-4sqrt2 epsilon/sqrt(p_total); epsilon<sqrt(p_total)/(10sqrt2) suffices with perfect readout. Duhamel bounds epsilon by integrated Hamiltonian norm errors, summed over both pulses.',
        boundary='An explicit spin interaction/pulse specification with supplied controllable local and two-qubit terms; exact filter algebra, numerical principal-log polar coefficients. It does not derive these couplings from W33 or demonstrate a photonic/native device, noisy readout threshold, correlated-error distillation or fault-tolerant rate.')

def clifford_geometry():
    old=read('w33_pass11625_11629_composites_joint_vacua.json')['reye_vacuum_audit']
    w=np.exp(2j*np.pi/3)
    rays=np.array(list(np.eye(3))+[np.array([1,w**r,w**t])/np.sqrt(3) for r,t in it.product(range(3),repeat=2)])
    F=np.array([[w**(i*j) for j in range(3)] for i in range(3)])/np.sqrt(3)
    gens=[F,np.diag([1,1,w]),np.roll(np.eye(3),1,axis=0),np.diag([1,w,w*w])]
    pg=old['Clifford_generators'];ident=tuple(range(12));group={ident:np.eye(3,dtype=complex)};queue=[ident]
    for p in queue:
        for g,G in zip(pg,gens):
            q=tuple(g[p[i]] for i in range(12))
            if q not in group:group[q]=G@group[p];queue.append(q)
    assert len(group)==216
    cp=tuple(map(int,np.argmax(abs(rays.conj()@rays.conj().T)**2,axis=0)))
    def tr(c,p):return tuple(sorted(tuple(sorted(p[i] for i in t)) for t in c))
    configs=set()
    for o in old['unitary_lift_orbits']:
        c=tuple(map(tuple,o['representative']))
        configs.update(tr(c,p) for p in group)
    assert len(configs)==432
    return old,group,gens,pg,cp,tr,configs

def physical_flavor():
    old,group,gens,pg,cp,tr,configs=clifford_geometry()
    counts=Counter();seeds=[]
    for c in sorted(configs):
        for h in range(12):
            little=[p for p in group if p[h]==h and tr(c,p)==c]
            counts[len(little)]+=1
            if len(little)==1:seeds.append((c,h))
    assert seeds
    c,h=seeds[0];partner=(tr(c,cp),cp[h])
    orbit={(tr(c,p),p[h]):G for p,G in group.items()}
    assert len(orbit)==216 and partner not in orbit
    e=s.symbols('epsilon',real=True)
    Yu=s.diag(1,2,4);Yd=s.Matrix([[2,1,s.I*e],[1,3,1],[s.I*e,1,4]])
    Hu=Yu.H*Yu;Hd=Yd.H*Yd;comm=Hu*Hd-Hd*Hu
    invariant=s.factor(s.trace(comm**3)/s.I)
    assert invariant!=0 and s.simplify(invariant.subs(e,0))==0
    u=np.array(Hu,complex);d=np.array(Hd.subs(e,1),complex)
    assert min(np.linalg.eigvalsh(u))>0 and min(np.linalg.eigvalsh(d))>0
    table={};reps=[]
    for key,G in orbit.items():
        a,b=G@u@G.conj().T,G@d@G.conj().T
        table[key]=(a,b)
        ck=(tr(key[0],cp),cp[key[1]])
        assert ck not in orbit
        table[ck]=(a.conj(),b.conj())
        reps.append(dict(config=[list(t) for t in key[0]],h=key[1],representative=complex_pack(G)))
    assert len(table)==432
    residual=0.
    for key,(a,b) in table.items():
        for p,G in zip(pg,gens):
            aa,bb=table[(tr(key[0],p),p[key[1]])]
            residual=max(residual,np.max(abs(aa-G@a@G.conj().T)),np.max(abs(bb-G@b@G.conj().T)))
    assert residual<2e-12
    for key,(a,b) in table.items():
        aa,bb=table[(tr(key[0],cp),cp[key[1]])]
        assert np.max(abs(aa-a.conj()))<1e-12 and np.max(abs(bb-b.conj()))<1e-12
    eu,Vu=np.linalg.eigh(u);ed,Vd=np.linalg.eigh(d);V=Vu.conj().T@Vd
    J=float(np.imag(V[0,0]*V[1,1]*V[0,1].conj()*V[1,0].conj()))
    assert abs(J)>1e-5
    return dict(status='PASS',joint_sector_stabilizer_census={str(k):v for k,v in counts.items()},
        selected_config=[list(t) for t in c],selected_h=h,selected_little_group=1,
        unitary_orbit=216,CP_paired_orbit=432,orbit_representatives=reps,
        symmetric_Yu=Yu.tolist(),symmetric_Yd=[[str(z) for z in row] for row in Yd.tolist()],
        exact_CP_invariant_Tr_commutator_cube_over_i=str(invariant),
        epsilon1_squared_masses={'up':eu.tolist(),'down':ed.tolist()},epsilon1_CKM=complex_pack(V),epsilon1_Jarlskog=J,
        generator_covariance_error=float(residual),
        residual_symmetry_no_go='A nontrivial common residual unitary on three nondegenerate families forces both Hermitian mass matrices into its eigenspace blocks. Distinct or2+1 eigenblocks imply zero3-family Jarlskog; incidence CP breaking alone is insufficient in those sectors.',
        construction='On the chosen free joint incidence/Higgs orbit set Hq(g.s)=G Hq(seed)Gdag; on its disjoint CP orbit use complex conjugates. Projective phases cancel. Symmetric seed Yukawas have Takagi factors and can be transported as conjugate(G)Y Gdag up to the Higgs overall phase.',
        boundary='An explicit sigma/Higgs-dependent positive mass-squared map and physical quark CP witness on one CP-paired orbit. The seed coefficients, epsilon, Higgs fields and scales are supplied; not an observed flavor fit, continuous UV operator, parent potential selecting this orbit or full5184-sector Yukawa Lagrangian. Other sectors remain unassigned, rather than given invented coefficients.')

def coxeter_data():
    from w33_e8_eisenstein_witting_weld import e8_roots_doubled
    R=np.array(e8_roots_doubled(),dtype=int)
    a=[(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0)]
    for i in range(1,7):
        z=[0]*8;z[i]=2;z[i-1]=-2;a.append(z)
    reflections=[s.eye(8)-s.Matrix(z)*s.Matrix(z).T/4 for z in a]
    C=s.eye(8)
    for T in reflections:C=T*C
    return R,C,C**10,reflections

def phase_quotient():
    from w33_pass11630_reye_witting_instrument import exact_vectors,proportional
    R,C,omega,refs=coxeter_data();E=s.eye(8)[:,4:]
    D4=[tuple(r) for r in R if not any(r[:4])];assert len(D4)==24
    original=s.simplify(E.T*(2*omega+s.eye(8))*E)
    assert original.rank()==2
    rng=np.random.default_rng(11633);W=s.eye(8);word=[];good=None
    for trial in range(1000):
        N=E.T*(2*W*omega*W.T+s.eye(8))*E
        if N*N==-s.eye(4):good=W*omega*W.T;break
        j=int(rng.integers(8));W=refs[j]*W;word.append(j)
    assert good is not None
    N=E.T*(2*good+s.eye(8))*E
    # Match the pullback Hermitian form to the supplied L, with a signed
    # coordinate permutation. This creates a named full8-real-to4-complex map.
    source=read('w33_pass11630_reye_witting_instrument.json')['instrument']
    Js=s.Matrix(source['J']);O=None
    for p in it.permutations(range(4)):
        for signs in it.product([-1,1],repeat=4):
            o=s.zeros(4)
            for i,j in enumerate(p):o[j,i]=signs[i]
            if o.T*Js*o==N:O=o;break
        if O is not None:break
    assert O is not None
    J=(2*good+s.eye(8))/s.sqrt(3)
    realframe=E.row_join(J*E);assert realframe.det()!=0
    L0=s.Matrix([[s.sympify(z) for z in row] for row in source['projective_matrix']])
    # The selected D4 roots are the (ei+-ej) cell, so use its inverse-adjoint
    # map, not the primary cell's L. This is the11630 contragredient distinction.
    L=s.simplify(s.sqrt(s.Rational(2,3))*L0.H.inv())
    P=L*O*(s.eye(4).row_join(s.I*s.eye(4)))*realframe.inv()
    assert all(s.simplify(s.expand(z))==0 for z in P*J-s.I*P)
    V=exact_vectors();mapping=[]
    # Numerical overlap only proposes a label; every proposed match is then
    # certified by exact minors. Pairwise exact distinctness ensures uniqueness.
    assert all(not proportional(V[i],V[j]) for i in range(40) for j in range(i))
    numeric=np.column_stack([np.array(v.evalf(),complex).ravel() for v in V])
    numeric/=np.linalg.norm(numeric,axis=0)
    Pnumeric=np.array(P.evalf(),complex)
    for r in R:
        vn=Pnumeric@r;vn/=np.linalg.norm(vn)
        label=int(np.argmax(abs(numeric.conj().T@vn)**2))
        v=P*s.Matrix(r);assert proportional(v,V[label]);mapping.append(label)
    assert Counter(mapping)=={i:6 for i in range(40)}
    rootindex={tuple(r):i for i,r in enumerate(R)}
    g5=W*(C**5)*W.T
    perm=[rootindex[tuple(g5*s.Matrix(r))] for r in R]
    assert all(mapping[i]==mapping[perm[i]] for i in range(240))
    selected=sorted(set(mapping[rootindex[r]] for r in D4));assert len(selected)==12
    # Original quotient's slant collapse is computed directly via real complex planes.
    Jold=(2*omega+s.eye(8))/s.sqrt(3);classes=[]
    for r in D4:
        r=s.Matrix(r);same=None
        for i,t in enumerate(classes):
            if s.Matrix.hstack(t,Jold*t,r).rank()==2:same=i;break
        if same is None:classes.append(r)
    return dict(status='PASS',original_restricted_N=original.tolist(),original_complex_distinct_D4_rays=len(classes),
        original_slant_cosines=[0,1],compatible_Weyl_word=word,compatible_restricted_N=N.tolist(),
        repaired_slant_cosines=['1/sqrt(3)','1/sqrt(3)'],signed_real_permutation=O.tolist(),
        complex_projection=[[str(s.simplify(z)) for z in row] for row in P.tolist()],
        all240_root_to_Witting_ray=mapping,selected_D4_Witting_rays=selected,
        repaired_omega=[[str(z) for z in row] for row in good.tolist()],
        full_map_checks='P J=iP; all240 roots match exactly one canonical Witting ray; every ray has6roots; conjugated C^5 acts within fibers; selected D4 has12distinct rays',
        boundary='The old D4 and old Coxeter quotient are individually valid but their direct combination is unsuitable for the supplied invertible slant map. The explicit Weyl conjugation changes the chosen complex structure. This is a finite exact dictionary, not a canonical physical choice or transport of all real Peres orthogonal contexts.')

def full_quantum_normals():
    p=ROOT/'data/w33_pass11634_full_quantum_normals.json'
    d=json.loads(p.read_text());producer=ROOT/'analysis/w33_pass11634_full_quantum_normals.py'
    digest=hashlib.sha256(producer.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    assert d['producer_sha256']==digest and d['all_normal_positive']
    assert d['gauge_rank']==33 and d['normal_dimension']==264 and d['gauge_Ward_HG_norm']<1e-8
    return {k:d[k] for k in ['status','quadrature_order','full_gradient_norm','gauge_rank','gauge_Ward_HG_norm','normal_dimension','minimum_normal_curvature','minimum_scalar_denominator','scheme','boundary','producer_sha256']}|{'certificate_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def native_tree_gravity():
    from w33_levi_kirchhoff_cycle_projector import build_w33,build_levi
    g,points=build_w33();levi,_=build_levi(g,points)
    edges=sorted(tuple(sorted(e)) for e in levi.edges());B=np.zeros((80,160),dtype=np.int64)
    for j,(a,b) in enumerate(edges):B[a,j]=-1;B[b,j]=1
    Lap=B@B.T;Knum=np.rint(160*B.T@np.linalg.pinv(Lap.astype(float))@B).astype(np.int64)
    # Integer identities certify the exact unique orthogonal cut projector.
    assert np.array_equal(Knum,Knum.T) and np.array_equal(Knum@Knum,160*Knum)
    assert np.array_equal(B@Knum,160*B) and np.trace(Knum)==79*160
    assert set(np.diag(Knum))=={79}
    e,f=next((i,j) for i in range(160) for j in range(i+1,160) if set(edges[i])&set(edges[j]))
    assert abs(Knum[e,f])==27
    p=s.Rational(79,160);cov=-s.Rational(int(Knum[e,f])**2,160**2)
    degreevar=s.factor(4*p*(1-p)+12*cov);assert degreevar==s.Rational(1053,1600)
    # Independent weighted Matrix-Tree cofactor control for the two-edge law.
    trials=[]
    joint=p*p+cov
    for a,b in [(2.,3.),(.7,1.4),(1.01,.99)]:
        weights=np.ones(160);weights[e]=a;weights[f]=b
        logdet=np.linalg.slogdet(((B*weights)@B.T)[:-1,:-1])[1]
        base=np.linalg.slogdet(Lap[:-1,:-1])[1]
        expected=1+float(p)*(a-1+b-1)+float(joint)*(a-1)*(b-1)
        assert abs(np.exp(logdet-base)-expected)<3e-13
        trials.append(dict(weights=[a,b],cofactor_ratio=float(np.exp(logdet-base)),exact_polynomial_value=expected))
    tree=nx.bfs_tree(levi,0).to_undirected();ti=[edges.index(tuple(sorted(edge))) for edge in tree.edges()]
    assert len(ti)==79 and nx.is_tree(tree)
    ev=np.linalg.eigvalsh(B[:,ti]@B[:,ti].T);assert ev[1]>0 and abs(ev[0])<1e-12
    # DPP covariance: fixed79-edge size gives row sums zero, but variance of
    # nonconstant edge observables is nonzero and induces a quartic cumulant.
    Cov=-Knum*Knum
    np.fill_diagonal(Cov,79*(160-79))
    assert not np.any(Cov.sum(axis=1))
    assert np.linalg.eigvalsh(Cov.astype(float)).min()>-1e-8
    m=np.arange(-8,9);rho=s.Rational(-7,10);charge=s.Rational(1,5)
    energy=np.array([float(rho+charge**2*int(n)**2/2) for n in m]);beta=3.
    rates=np.zeros((17,17))
    for i in range(16):
        rates[i,i+1]=np.exp(-beta*(energy[i+1]-energy[i])/2)
        rates[i+1,i]=np.exp(-beta*(energy[i]-energy[i+1])/2)
    rates[np.diag_indices(17)]=-rates.sum(axis=1)
    stationary=np.exp(-beta*energy);stationary/=sum(stationary)
    assert max(abs(stationary@rates))<2e-15 and stationary[8]>stationary[14]
    # A common vacuum energy changes the odds between two four-volumes.
    C,V1,V2=s.symbols('C V1 V2',real=True)
    odds=s.exp(-C*(V1-V2))
    return dict(status='PASS',native_graph={'vertices':80,'edges':160,'cycles':81},
        prior_tree_count='2^83*5^23 (BT547/5031)',prior_edge_probability=str(p),
        exact_cut_projector_numerator=Knum.tolist(),projector_denominator=160,edges=[list(e) for e in edges],
        representative_tree_edges=ti,representative_tree_first_positive_Laplacian_eigenvalue=float(ev[1]),
        branch_action='S_T=sum_i M_i^2/2 integral sqrt(-g_i)R_i - sum_(ij in T) m_ij^2 M_ij^2 integral sqrt(-g_i) sum_n beta_ij,n e_n(sqrt(g_i^-1 g_j)) + individually coupled matter. All continuum metrics and coefficients are supplied.',
        ensemble='A conserved superselection register T ranges over native spanning trees with uniform measure. Graph automorphisms permute T, restoring graph symmetry at ensemble level. Each branch is an80-metric pairwise tree on a regular principal-square-root/Lorentz-constraint branch; imported ghost-free tree theorems apply conditionally. No branch-changing dynamics has been specified.',
        conditional_branch_spin2_polarizations=397,
        exact_adjacent_edge_covariance=str(cov),exact_vertex_tree_degree_variance=str(degreevar),
        two_edge_inclusion=str(joint),two_edge_weighted_partition='1+(79/160)(a-1+b-1)+(5512/25600)(a-1)(b-1)',weighted_cofactor_controls=trials,
        effective_action='-log E_T exp(-sum_e I_e O_e)=p sum_e O_e - (1/2) sum_ef Cov(I_e,I_f) O_e O_f + higher cumulants. If O_e starts quadratic in metric fluctuations, the covariance term starts quartic. Averaging branch actions discards this term and has no inherited ghost-free theorem.',
        vacuum_shift_relative_volume_odds=str(odds),
        flux_control={'rho':str(rho),'charge':str(charge),'beta':beta,'m':m.tolist(),'energies':energy.tolist(),'stationary_distribution':stationary.tolist(),'generator':rates.tolist(),'smallest_positive_energy':str(rho+charge**2*6**2/2),'next_downhill_energy':str(rho+charge**2*5**2/2)},
        vacuum_boundary='The tree register cannot sequester a common cosmological source: a shift C multiplies the odds of unequal-volume sectors by exp[-C(V1-V2)]. Supplied membrane/flux transitions obeying detailed balance select their supplied Gibbs distribution, not a smallest positive vacuum: the next downhill flux state is AdS. An absorbing boundary, measure or dynamical sequestering law is additional physics.',
        boundary='A native-edge80-metric superselection architecture and exact ensemble-cumulant controls, not a native derivation of propagating spacetime, an averaged ghost-free action, a proof beyond regular tree branches, Newton constant or observed cosmological constant. The earlier160-edge cyclic metric failure and prior extra-hub construction remain valid.',
        prior_owners=['analysis/w33_levi_kirchhoff_cycle_projector.py','analysis/w33_pass11323_native_cycle_lapse_hessian.py','analysis/w33_pass11384_11388_native_dynamics.py'],
        primary_sources=['https://arxiv.org/abs/1109.3515','https://arxiv.org/abs/1410.7774','https://arxiv.org/html/2604.07625v1','https://arxiv.org/abs/1903.02829'])

def produce():
    out=dict(status='PASS',passes=list(range(11631,11636)),reservation='420ab9140',context_owners=CONTEXT_OWNERS)
    for key,fn in [('microscopic_instrument',microscopic_instrument),('physical_flavor',physical_flavor),('phase_quotient',phase_quotient),('full_quantum_normals',full_quantum_normals),('native_tree_gravity',native_tree_gravity)]:
        out[key]=fn();print(key,'PASS',flush=True)
    out['producer_sha256']=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    OUT.write_text(json.dumps(out,indent=2,default=str)+'\n')
    return out

if __name__=='__main__':produce()
