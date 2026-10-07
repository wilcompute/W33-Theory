"""Five physical follow-ups, with finite maps and explicit remaining boundaries.
Prior11271 owns d times family6bar;11632 owns free-sector lookup.
Prior7240 owns4480 E8 structures;11633 owns the compatible slant witness.
Prior11323 owns nonlinear cycle elimination;11546 owns affine fixed-flux Ward.
"""
from pathlib import Path
from collections import Counter
import sys,json,itertools as it,hashlib
import numpy as np
import sympy as s
import networkx as nx
from scipy.optimize import root
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11631_11635_physical_interfaces as old
from w33_pass11289_cycle_gram_gluing_flux import cycle_basis
import w33_pass11302_sequestered_membrane_junction as caps
OUT=ROOT/'data/w33_pass11636_11640_operator_selector_transitions.json'

def digest(p):return hashlib.sha256(Path(p).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def packed(a):return [[[float(z.real),float(z.imag)] for z in row] for row in np.asarray(a)]
def family_rays(exact=False):
    w=(-1+s.I*s.sqrt(3))/2 if exact else np.exp(2j*np.pi/3)
    if exact:return [s.eye(3)[:,i] for i in range(3)]+[s.Matrix([1,w**r,w**t])/s.sqrt(3) for r,t in it.product(range(3),repeat=2)]
    return np.array(list(np.eye(3))+[np.array([1,w**r,w**t])/np.sqrt(3) for r,t in it.product(range(3),repeat=2)])

def incidence_yukawas(config,h,exact=False):
    rays=family_rays(exact)
    if exact:
        Ps=[v*v.H for v in rays];ys=[]
        for power in [1,2]:
            Y=s.zeros(3)
            for t in config:
                Q=sum([Ps[i] for i in t],s.zeros(3));v=(Q**power*h).applyfunc(s.simplify).conjugate();Y+=v*v.T
            ys.append(Y.applyfunc(s.simplify))
        return ys
    Ps=np.einsum('ai,aj->aij',rays,rays.conj());Q=np.array([sum(Ps[i] for i in t) for t in config]);v=Q@h;w=np.einsum('aij,aj->ai',Q,v)
    return [np.einsum('ai,aj->ij',z.conj(),z.conj()) for z in [v,w]]

def flavor():
    _,group,gens,pg,cp,tr,configs=old.clifford_geometry();rays=family_rays();prior=old.read('w33_pass11631_11635_physical_interfaces.json')['physical_flavor'];c=prior['selected_config'];h=prior['selected_h']
    y1,y2=incidence_yukawas(c,family_rays(True)[h],True);e=s.symbols('epsilon',real=True);yd=y1+e*y2
    hu=(y1.H*y1).applyfunc(s.expand);hd=(yd.H*yd).applyfunc(s.expand);comm=(hu*hd-hd*hu).applyfunc(s.expand);invariant=s.factor(s.expand(s.trace(comm**3)/s.I));assert invariant!=0 and invariant.subs(e,0)==0
    archive=ROOT/'data/w33_pass11636_e6_cubic_inputs.npz';src=np.load(archive);d,B=src['d'],src['B'];assert d.shape==(27,27,27) and np.count_nonzero(d)==270
    for b in B:
        assert not np.any(np.einsum('ai,ajk->ijk',b,d)+np.einsum('aj,iak->ijk',b,d)+np.einsum('ak,ija->ijk',b,d))
    # Each E6 leg is checked, and the combined Weyl mass is symmetric.
    for y in [y1,y2]:
        M=np.kron(d[:,:,0],np.array(y,complex));assert np.max(abs(M-M.T))<1e-12
    counts=Counter();min_nonzero=1.;cov=0.;ranks=Counter()
    # Full5184-sector sweep; no arbitrary values for the other sectors.
    for config in sorted(configs):
        for hi in range(12):
            a,b=incidence_yukawas(config,rays[hi]);aa=a.conj().T@a;bb=(a+b).conj().T@(a+b);aa/=np.trace(aa).real;bb/=np.trace(bb).real;z=aa@bb-bb@aa;v=float(np.trace(z@z@z).imag)
            counts['CP_zero' if abs(v)<1e-12 else 'CP_nonzero']+=1
            if abs(v)>=1e-12:min_nonzero=min(min_nonzero,abs(v))
            ranks[str((int(np.linalg.matrix_rank(a,tol=1e-9)),int(np.linalg.matrix_rank(a+b,tol=1e-9))))]+=1
            for p,G in zip(pg,gens):
                # Test the actual field transformation, including central phases.
                a1,b1=incidence_yukawas(tr(config,p),G@rays[hi]);cov=max(cov,float(np.max(abs(a1-G.conj()@a@G.conj().T))),float(np.max(abs(b1-G.conj()@b@G.conj().T))))
    assert cov<1e-11
    # Upgrade the floating full sweep to an exact orbit-wise certificate.
    # A phase of the normalized Higgs ray multiplies both Ys equally and
    # cancels from their Hermitian Grams.
    erays=family_rays(True);ew=(-1+s.I*s.sqrt(3))/2
    egens=[s.Matrix([[ew**(i*j) for j in range(3)] for i in range(3)])/s.sqrt(3),s.diag(1,1,ew),s.Matrix(np.roll(np.eye(3,dtype=int),1,axis=0)),s.diag(1,ew,ew**2)]
    for perm,G in zip(pg,egens):
        for i in range(12):
            z=G*(erays[i]*erays[i].H)*G.H-erays[perm[i]]*erays[perm[i]].H
            assert all(s.simplify(s.expand(v))==0 for v in z)
    remaining={(c,h) for c in configs for h in range(12)};orbit_rows=[];exact_counts=Counter();exact_ranks=Counter();operator_pairs=[]
    while remaining:
        config,hi=min(remaining);orb={(tr(config,p),p[hi]) for p in group};assert orb<=remaining;remaining-=orb
        a,b=incidence_yukawas(config,erays[hi],True);operator_pairs.append((a,b));moment=s.factor(s.expand(s.trace((a+e*b).H*(a+e*b))));b=a+b;aa=(a.H*a).applyfunc(s.expand);bb=(b.H*b).applyfunc(s.expand);cc=(aa*bb-bb*aa).applyfunc(s.expand);cpval=s.factor(s.expand(s.trace(cc**3)/s.I))
        label='CP_zero' if cpval==0 else 'CP_nonzero';exact_counts[label]+=len(orb);rkey=str((a.rank(),b.rank()));exact_ranks[rkey]+=len(orb)
        orbit_rows.append(dict(config=[list(x) for x in config],h=hi,orbit_size=len(orb),CP_epsilon1=str(cpval),rank_pair=[a.rank(),b.rank()],squared_mass_trace_polynomial=str(moment)))
    assert len(orbit_rows)==28 and exact_counts==counts and exact_ranks==ranks
    assert all((s.sympify(r['CP_epsilon1'])!=0)==(r['orbit_size']==216) for r in orbit_rows)
    # A new branch: let an actual81-Weyl E6 determinant lift the pinned
    # finite-sector degeneracy. Do not assume an arbitrary CP seed is selected.
    d0=s.Matrix(d[:,:,0]);assert d0**3==d0 and s.trace(d0*d0)==10
    selection=[]
    for eps in [s.Rational(1,100),s.Integer(1)]:
        scores=[s.sympify(r['squared_mass_trace_polynomial'],locals={'epsilon':e}).subs(e,eps) for r in orbit_rows];best=max(scores);winners=[i for i,q in enumerate(scores) if q==best];gap=best-max(q for q in scores if q!=best)
        a,b=operator_pairs[winners[0]];y=a+eps*b;mf=(y.H*y).applyfunc(s.expand);u4=s.factor(s.expand(s.trace(mf*mf)));bound=s.factor(3*gap/(25*u4));coupling=s.Rational(1,10000);assert coupling**2<bound
        hu=(a.H*a).applyfunc(s.expand);comm=(hu*mf-mf*hu).applyfunc(s.expand);cpval=s.factor(s.expand(s.trace(comm**3)/s.I));a_rank,y_rank=a.rank(),y.rank()
        energies=[];z,w=np.polynomial.legendre.leggauss(64);mom=.13+.12*z
        for aa,bb in operator_pairs:
            yy=np.array(aa+eps*bb,complex);lam=np.linalg.eigvalsh(yy.conj().T@yy);energies.append(float(-20*np.sum(w*.12*mom/(64*np.pi**2)*np.log1p(float(coupling**2)*lam[:,None]/mom))))
        assert max(energies[i] for i in winners)<min(v for i,v in enumerate(energies) if i not in winners)
        partner=(tr(tuple(map(tuple,orbit_rows[winners[0]]['config'])),cp),cp[orbit_rows[winners[0]]['h']]);other=orbit_rows[winners[1]];other_orbit={(tr(tuple(map(tuple,other['config'])),p),p[other['h']]) for p in group};assert partner in other_orbit
        selection.append(dict(epsilon=str(eps),winning_orbits=winners,total_selected_sectors=sum(orbit_rows[i]['orbit_size'] for i in winners),exact_maximum_family_trace=str(best),exact_trace_gap=str(gap),winner_fourth_mass_moment=str(u4),sufficient_y_squared_bound=str(bound),tested_y=str(coupling),full81_fermion_shell_energies=energies,selected_family_ranks=[a_rank,y_rank],selected_CP_invariant=str(cpval)))
    assert selection[0]['selected_family_ranks']==[3,3] and s.sympify(selection[0]['selected_CP_invariant'])!=0
    assert selection[1]['selected_family_ranks']==[1,1] and s.sympify(selection[1]['selected_CP_invariant'])==0
    a,b=map(lambda z:np.array(z,complex),[y1,y1+y2]);u,U=np.linalg.eigh(a.conj().T@a);v,V=np.linalg.eigh(b.conj().T@b);mix=U.conj().T@V;J=float((mix[0,0]*mix[1,1]*mix[0,1].conjugate()*mix[1,0].conjugate()).imag);assert abs(J)>1e-6
    partner=tr(tuple(map(tuple,c)),cp);ac,bc=incidence_yukawas(partner,rays[h].conj());assert np.max(abs(ac-a.conj()))<1e-12
    return dict(status='PASS',selected_config=c,selected_h=h,Y1=[[str(z) for z in row] for row in y1.tolist()],Y2=[[str(z) for z in row] for row in y2.tolist()],CP_polynomial=str(invariant),epsilon1_J=J,epsilon1_squared_singular_masses=[u.tolist(),v.tolist()],generator_covariance_error=cov,
      fermion_loop_sector_selection=selection,sector_selection_proof='Pinned5184-sector model: one Weyl81 with M=y d[:,:,0] tensor (Y1+epsilon Y2), exactly10 repeated family spectra. Fermion shell favors maximum mass trace at sufficiently weak y. Bounds0<=u-log(1+u)<=u²/2 and log25<4 give strict selection if y²<3*trace_gap/(25*fourth_moment). The two winning orbits are CP conjugates. This is a calculated finite-sector one-loop selection, not full continuous-field vacuum stability or a selected epsilon.',all5184_CP_census_numeric=dict(counts),all5184_CP_census_exact=dict(exact_counts),exact_joint_orbit_representatives=orbit_rows,all5184_rank_census=dict(ranks),minimum_nonzero_normalized_CP=min_nonzero,
      defining_map='Q_t=sum_{i in t} P_i; Y_a(sigma,h)=sum_t sigma_t conjugate(Q_t^a h) conjugate(Q_t^a h).T, a=1,2. Yu=Y1,Yd=Y1+epsilon Y2. P_i are the fixed12 Hesse-ray projectors; sigma is the220-component real triple-incidence field. At each of the432 Reye configurations, exactly16 sigma_t=1. This is a continuous polynomial in sigma,h, defined beyond the minima.',
      invariance='Clifford generators permute P_i and sigma labels while h,psi transform by G. Y_a transforms as conjugate(G) Y_a Gdag, so d_ABC psi_i^A psi_j^B H^C Y_a,ij is invariant and Pauli-allowed. E6 invariance checked on all78 exact generators of the committed signed cubic. Family symmetry is the finite Clifford extension, not an untested continuous family SU3 gauge symmetry.',
      EFT_operator='With dimensionless incidence order parameter sigma and canonical scalar h, psi psi H hbar hbar has dimension6 and coefficient y_a/LambdaF². If sigma is a canonical dimension1 field, its coefficient is instead y_a/LambdaF³, dimension7. Distinct supplied27 Higgs channels define up/down spurions; SM branching and vev selection are not derived here.',
      E6_input_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),E6_original_sources={'artifacts/canonical_su3_gauge_and_cubic.json':'13ea38ed37a8c1c9723db7168e1e056a2827ebf060bc096e227f8d9047d78cb1','artifacts/e6_27rep_basis_export/E6_basis_78.npy':'865029db0ae45f2e321a1e987fff74dab151e6138509cd46bcb9ff363d509909'},
      boundary='Exact selected CP polynomial, symmetric E6 operator and full finite covariance replay; exact28-orbit/full5184-sector CP and rank census. This removes the11632 unbuilt continuous operator, but coefficients, cutoff, incidence/Higgs potential, chirality and observed masses/mixing remain supplied or open.',prior_owners=['analysis/w33_pass11361_11368_physical_frontier.py','analysis/w33_pass11625_11629_composites_joint_vacua.py','analysis/w33_pass11271_chiral_symmetric_yukawa_completion.py','analysis/w33_pass11631_11635_physical_interfaces.py','analysis/w33_20261001_global_e6_cartan_covariants.py'])

def complex_selector():
    R,C,omega,refs=old.coxeter_data();A=np.array(4*omega,np.int64);Ts=[np.array(4*r,np.int64) for r in refs];lookup={A.tobytes():0};orbit=[A];parents=[[-1,-1]]
    for i,x in enumerate(orbit):
        for g,t in enumerate(Ts):
            raw=t@x@t;assert not np.any(raw%16);y=raw//16;key=y.tobytes()
            if key not in lookup:lookup[key]=len(orbit);orbit.append(y);parents.append([i,g])
    assert len(orbit)==4480
    perm=np.array([[lookup[(t@x@t//16).tobytes()] for x in orbit] for t in Ts]);energy=[]
    for x in orbit:
        assert np.array_equal(x@x+4*x+16*np.eye(8,dtype=np.int64),np.zeros((8,8),np.int64))
        N=x[4:,4:]+2*np.eye(4,dtype=np.int64);raw=int(np.sum((N@N+4*np.eye(4,dtype=np.int64))**2));assert raw%16==0;energy.append(raw//16)
    energy=np.array(energy);assert Counter(energy)=={0:2304,10:2048,16:128}
    # Exact projector is polynomial in the quartic compatibility energy.
    projector=(energy-10)*(energy-16)//160;assert np.array_equal(projector,energy==0)
    G=nx.Graph();G.add_nodes_from(np.flatnonzero(projector))
    for i in G:
        for p in perm:
            if projector[p[i]]:G.add_edge(i,int(p[i]))
    G.remove_edges_from(nx.selfloop_edges(G));assert nx.is_connected(G)
    outside=np.zeros(4480,int)
    for i in np.flatnonzero(projector):
        for p in perm:
            if not projector[p[i]]:outside[p[i]]+=1
    leakage=s.Rational(int(outside@outside),2304);assert leakage>0
    archive=ROOT/'data/w33_pass11638_complex_selector.npz';np.savez_compressed(archive,orbit=np.array(orbit),permutations=perm,parents=np.array(parents),energy=energy)
    return dict(status='PASS',orbit_size=4480,exact_energy_census={str(k):int(v) for k,v in Counter(energy).items()},compatible_vertices=2304,compatible_edges=G.number_of_edges(),connected_compatible_graph=True,projector_polynomial='P0(E)=(E-10)(E-16)/160',ungated_uniform_good_leakage_norm_squared=str(leakage),
      selector='On the already-owned finite Weyl orbit omega, E=||N²+I4||F² with N=(2omega+I8)|D4. Hamiltonian H=kappa diag(E)+t sum_reflection_edges P0(E_i)P0(E_j)(|i>-|j>)(<i|-<j|). Positive kappa,t select an exact unique uniform coherent ground state on all2304 compatible structures, since its induced reflection graph is connected.',
      exact_gap_lower_bound='min(10*kappa, 2*t/2303²). Connected-graph path/Cauchy bound; multiple generator edges only improve the bound.',
      boundary='A constructed finite quantum selector with input kappa,t and an explicitly gated kinetic term. It selects compatibility, not one classical complex structure, spacetime or a physical law forcing these coefficients. Unrestricted Weyl hopping leaks outside the compatible set; the gating cannot be dropped.',
      archive=str(archive.relative_to(ROOT)),archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),prior_owners=['analysis/w33_pass7237_7244_the_ninety_and_the_witting_rays.py','analysis/w33_pass11631_11635_physical_interfaces.py'])

def tree_transitions():
    B,C=cycle_basis()
    G=nx.Graph();G.add_nodes_from(range(80));edges=[]
    for e in range(160):
        a,b=np.flatnonzero(B[:,e]);edges.append((int(a),int(b)));G.add_edge(int(a),int(b),edge=e)
    parent={0:None};queue=[0];tree=[]
    for a in queue:
        for b in G[a]:
            if b not in parent:parent[b]=a;queue.append(b);tree.append(G[a][b]['edge'])
    chord=next(e for e in range(160) if e not in tree);cycle=C[:,list(e for e in range(160) if e not in set(tree)).index(chord)];support=np.flatnonzero(cycle);remove=int(next(e for e in support if e!=chord));cols=sorted(tree+[chord]);Bs=B[:,cols];cs=cycle[cols];w=s.ones(len(cols),1);w[cols.index(chord)]=s.Rational(1,2);w[cols.index(remove)]=s.Rational(1,2)
    j=s.zeros(len(cols),1)
    j[cols.index(chord)]=cs[cols.index(chord)]*w[cols.index(chord)]*s.Rational(3,4)
    j[cols.index(remove)]=-cs[cols.index(remove)]*w[cols.index(remove)]*s.Rational(3,4)
    L=s.ones(len(cols),1)*2;v=s.Matrix([j[i]/s.sqrt(w[i]**2+j[i]**2) for i in range(len(cols))]);assert sum(cs[i]*L[i]*v[i] for i in range(len(cols)))==0
    A=sum(cs[i]**2*L[i]*w[i]**2/(w[i]**2+j[i]**2)**s.Rational(3,2) for i in range(len(cols)));g=s.Matrix(abs(Bs))*s.Matrix([v[i]*cs[i] for i in range(len(cols))]);H=-g*g.T/A;assert H.rank()==1
    p=np.array(s.Matrix(Bs)*j,dtype=float).ravel();N=np.ones(80);rows=[];cc=cs.astype(float);U=abs(Bs)
    for t in [.01,.1,.5,.9,.99]:
        ww=np.ones(len(cols));ww[cols.index(chord)]=t;ww[cols.index(remove)]=1-t;j0=Bs.T@np.linalg.pinv(Bs@Bs.T)@p
        fun=lambda x:float(cc@((U.T@N)*(j0+cc*x[0])/np.sqrt(ww**2+(j0+cc*x[0])**2)))
        sol=root(fun,[0.],tol=1e-11);assert abs(fun(sol.x))<1e-10;curr=j0+cc*sol.x[0]
        gg=U@(cc*curr/np.sqrt(ww**2+curr**2));aa=float(np.sum(cc**2*(U.T@N)*ww**2/(ww**2+curr**2)**1.5));hh=-np.outer(gg,gg)/aa;rows.append(dict(t=t,rank=int(np.linalg.matrix_rank(hh,tol=1e-9)),negative_eigenvalue=float(np.linalg.eigvalsh(hh)[0])))
    assert all(x['rank']==1 for x in rows)
    path=[]
    for t in [0.,.25,.5,.75,1.]:
        ww=np.ones(160);ww[[e for e in range(160) if e not in tree]]=0;ww[remove]=max(1-2*t,0);ww[chord]=max(2*t-1,0);gg=nx.Graph();gg.add_nodes_from(range(80));gg.add_edges_from(edges[e] for e in np.flatnonzero(ww));assert nx.is_forest(gg)
        n=nx.number_connected_components(gg);path.append(dict(t=t,edges=gg.number_of_edges(),components=n,conditional_static_spin2_count=2*n+5*(80-n)))
    return dict(status='PASS',tree=tree,chord=chord,removed_edge=remove,cycle_edges=support.tolist(),cycle_length=len(support),weighted_overlap_sweep=rows,exact_midpoint_A=str(A),exact_midpoint_g=[str(x) for x in g],exact_midpoint_nonzero_lapse_eigenvalue=str(-g.dot(g)/A),exact_midpoint_source=p.tolist(),forest_exchange_path=path,
      weighted_shift_formula='Ured=min_c sum_e (N_i+N_j)sqrt(w_e²+j_e²), j=j0+C c. H_N=-g g.T/a for one cycle, g=|B|diag(j/sqrt(w²+j²))C, a=C.T diag((N_i+N_j)w²/(w²+j²)^(3/2))C. The midpoint has exact rational currents and nonzero rank1 Hessian.',
      support_theorem='A continuous acyclic nonnegative-weight path between distinct spanning trees must pass through a disconnected support: a79-edge connected acyclic support has one locally fixed edge basis; changing it requires a weight to vanish before another edge is present. Overlap creates a cycle. The explicit break-before-make path stays a forest but its midpoint has two components and an additional massless sector.',
      boundary='Actual native tree exchange and nonlinear shift-elimination necessary test, with constructive forest alternative. Held-parameter tree/forest counts import static HR theory; they are not a full time-dependent Dirac proof. Promoting the switching parameter to a field or hopping register requires its constraint-preserving operator and an audit of the rank-changing point. No averaged graph ghost freedom or emergent gravity claim.',prior_owners=['analysis/w33_pass11361_11368_physical_frontier.py','analysis/w33_pass11323_native_cycle_lapse_hessian.py','analysis/w33_pass11631_11635_physical_interfaces.py'],primary_sources=['https://arxiv.org/abs/1410.7774','https://arxiv.org/abs/1109.3515'])

def vacuum_response():
    ref=np.array(caps.inputs()[:3]);vol,ravg,israel=caps.caps(*ref);assert abs(israel)<1e-10
    cases=[]
    for alpha in [0.,1.]:
        sig=lambda L:1+3*alpha*L*L;Q=float(sum(vol)/sig(ref[1]));Qhat=-Q*sig(ref[1])*ravg/2
        def residual(z,C,delta=0.):
            R,L,K=z
            rho=L+C+np.array([1.2,.8])**2/2+np.array([delta,0.]);H2=rho/(3*K)
            if K<=0 or R<=0 or np.any(1-H2*R*R<=0):return np.ones(3)*1e6
            cc=np.array([-1.,1.])*np.sqrt(1-H2*R*R);vv=2*np.pi**2/(H2**2)*(2/3-cc+cc**3/3);a=2*np.pi**2*R**3;rr=(4*(rho@vv)+3*.4*a)/(K*sum(vv))
            return np.array([sum(cc)/R-.4/(2*K),(sum(vv)-Q*sig(L))/sum(vol),rr+2*Qhat/(Q*sig(L))])
        base=residual(ref,0);assert np.linalg.norm(base)<1e-8
        eps=1e-5;J=np.column_stack([(residual(ref+eps*np.eye(3)[i],0)-residual(ref-eps*np.eye(3)[i],0))/(2*eps) for i in range(3)])
        dc=(residual(ref,eps)-residual(ref,-eps))/(2*eps);sus=-np.linalg.solve(J,dc);shift=root(lambda z:residual(z,.03),ref+sus*.03,tol=1e-11);assert np.linalg.norm(residual(shift.x,.03))<1e-9
        unequal=root(lambda z:residual(z,0,.01),ref,tol=1e-11);assert np.linalg.norm(residual(unequal.x,0,.01))<1e-9
        if alpha==0:assert np.max(abs(shift.x-(ref+np.array([0.,-.03,0.]))))<1e-8
        else:assert np.linalg.norm(sus-np.array([0.,-1.,0.]))>1e-4
        cases.append(dict(alpha=alpha,fixed_Q=Q,fixed_Qhat=Qhat,reference=ref.tolist(),reference_cap_volumes=vol.tolist(),implicit_Jacobian=J.tolist(),d_R_Lambda_K_d_common_C=sus.tolist(),common_C03_solution=shift.x.tolist(),unequal_threshold01_solution=unequal.x.tolist(),shift_residual=float(np.linalg.norm(residual(shift.x,.03)))))
    # Constant cancellation cannot cancel the local field-dependent part.
    x1,x2,C,a,b,v1,v2=s.symbols('x1 x2 C a b v1 v2',real=True);rho=[C+a*x1**4,C+b*x2**4];avg=(v1*rho[0]+v2*rho[1])/(v1+v2);grav=[s.factor(r-avg) for r in rho];assert all(s.diff(q,C)==0 for q in grav)
    force=[s.diff(v1*rho[0]+v2*rho[1],x1),s.diff(v1*rho[0]+v2*rho[1],x2)];assert force==[4*a*v1*x1**3,4*b*v2*x2**3]
    return dict(status='PASS',sigma='sigma(Lambda)=Lambda+alpha Lambda³; hatsigma(K)=K; fixed chosen sequestering fluxes. Three simultaneous equations: Israel, total volume=Q sigma_prime, averageR=-2 Qhat/(Q sigma_prime). Maxwell membrane form distinct from both sequestering forms.',cases=cases,exact_unequal_volume_radiative_source=list(map(str,grav)),retained_matter_forces=list(map(str,force)),
      result='The old affine fixed-flux Ward identity survives unequal cap volumes and a common constant threshold. Nonlinear sigma gives a calculated geometry/Newton response at fixed flux; an unequal cap threshold also changes the saddle in the affine case. Constant subtraction cannot remove field-dependent radiative forces.',
      boundary='Response and implicit saddle equations of the supplied11302 Euclidean two-cap model. Fluxes, functions, membrane inputs and geometry are supplied, not a quantized W33-selected CC. No saddle determinant, nucleation rate, all-loop/graviton protection or stable Lorentzian universe. This quantifies11546 fixed-data obstruction with geometry allowed to relax; it does not refute nonlinear sequestering radiative stability.',prior_owners=['analysis/w33_pass11302_sequestered_membrane_junction.py','analysis/w33_pass11542_11546_five_dynamical_targets.py','analysis/w33_pass11620_11624_covariant_pair_vacuum.py'],primary_sources=['https://arxiv.org/abs/1505.01492','https://arxiv.org/abs/1604.04000','https://arxiv.org/abs/1606.04958'])

def produce():
    d=dict(status='PASS',passes=list(range(11636,11641)),reservation='5bf052b08')
    for name,fn in [('flavor',flavor),('complex_selector',complex_selector),('tree_transitions',tree_transitions),('vacuum_response',vacuum_response)]:d[name]=fn();print(name,'PASS',flush=True)
    p=ROOT/'data/w33_pass11637_fermion_ir_normals.json';q=json.loads(p.read_text());assert q['status']=='PASS';d['fermion_IR']=dict(status='PASS',certificate=str(p.relative_to(ROOT)),certificate_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),normal_gaps=[x['minimum_normal_curvature'] for x in q['cases']],boundary=q['boundary'])
    d['producer_sha256']=digest(__file__);OUT.write_text(json.dumps(d,indent=2)+'\n');print('allfive PASS',flush=True)
if __name__=='__main__':produce()
