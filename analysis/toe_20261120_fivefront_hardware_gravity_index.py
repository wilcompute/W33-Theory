#!/usr/bin/env python3
"""Five independent model-scoped research falsifiers for W33/TOE (2026-11-20).

No physical quantum processor, G2 compactification, gauge-invariant SU3 experiment,
causal-set Einstein limit, or observed multi-time memory is claimed here.
"""
from __future__ import annotations
from itertools import combinations, product
from pathlib import Path
import json, math
import numpy as np
import networkx as nx
from scipy.sparse import csr_matrix, eye, kron, hstack
from scipy.integrate import quad
from scipy.optimize import brentq, linprog

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'data/toe_20261120_fivefront_hardware_gravity_index.json'


def w33_graph():
    """Independently reconstruct W(3,3) as totally isotropic PG(3,3) lines."""
    def norm(v):
        v=tuple(int(x)%3 for x in v)
        z=next(t for t in v if t)
        return tuple((x*(1 if z==1 else 2))%3 for x in v)
    def sym(u,v):
        return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3
    pts=sorted({norm(v) for v in product(range(3),repeat=4) if any(v)})
    pid={p:i for i,p in enumerate(pts)}
    lines=set()
    for i,u in enumerate(pts):
        for v in pts[i+1:]:
            if sym(u,v): continue
            lines.add(frozenset(pid[norm(tuple(a*u[k]+b*v[k] for k in range(4)))] for a,b in product(range(3),repeat=2) if a or b))
    ordered=sorted(lines,key=lambda s:tuple(sorted(s)))
    G=nx.Graph()
    G.add_nodes_from(range(80))
    for j,points in enumerate(ordered):
        for p in points:G.add_edge(p,40+j)
    assert G.number_of_nodes()==80 and G.number_of_edges()==160
    return G


def css_matrices(L=8):
    G=w33_graph(); edges=sorted((min(u,v),max(u,v)) for u,v in G.edges())
    A0=np.zeros((79,160),dtype=np.int16)
    for k,(u,v) in enumerate(edges):
        if u<79:A0[u,k]=1
        if v<79:A0[v,k]=-1
    A=csr_matrix(A0)
    B=csr_matrix(np.eye(L-1,L,dtype=np.int16)-np.eye(L-1,L,k=1,dtype=np.int16))
    I=lambda n:eye(n,dtype=np.int16,format='csr')
    HX=hstack([kron(A,I(L)),kron(I(79),B.T)],format='csr')
    HZ=hstack([kron(I(160),B),-kron(A.T,I(L-1))],format='csr')
    HX.eliminate_zeros();HZ.eliminate_zeros()
    assert not np.any((HX@HZ.T).data%3)
    assert HX.shape==(79*L,239*L-79) and HZ.shape==(160*(L-1),239*L-79)
    return HX,HZ


def tanner_schedule(H):
    """Conflict-free sequential check-to-qudit layers; not a compiled fault-tolerant circuit."""
    coo=H.tocoo()
    pairs=sorted(zip(coo.row.tolist(),coo.col.tolist()),key=lambda rc:(-int(np.diff(H.indptr)[rc[0]]),rc))
    # Deterministic bipartite edge greedy coloring: no qudit/check twice in a layer.
    row_busy={};col_busy={};layers=[]
    for r,c in pairs:
        forbidden=row_busy.get(r,set())|col_busy.get(c,set())
        layer=0
        while layer in forbidden:layer+=1
        if layer==len(layers):layers.append([])
        layers[layer].append((int(r),int(c)))
        row_busy.setdefault(r,set()).add(layer)
        col_busy.setdefault(c,set()).add(layer)
    assert sum(map(len,layers))==H.nnz
    for layer in layers:
        assert len({r for r,c in layer})==len(layer)
        assert len({c for r,c in layer})==len(layer)
    return layers


def detector_dictionary(H,rounds=3):
    """First-fault lookup with ideal final syndrome boundary.
    Data error of amplitude a at time t contributes a*H[:,j] at t.
    One measurement error contributes +a on detector t, -a on t+1.
    """
    C=H.tocsc()
    seen={};collision=[];counts={'data':0,'measurement':0}
    def add(key,label):
        if key in seen:collision.append((seen[key],label))
        else:seen[key]=label
    for t in range(1,rounds+1):
        for j in range(H.shape[1]):
            start,end=C.indptr[j:j+2]
            vals=[(int(i),int(v)%3) for i,v in zip(C.indices[start:end],C.data[start:end])]
            for a in (1,2):
                sign=tuple(sorted((t,i,(v*a)%3) for i,v in vals))
                add(sign,('data',t,j,a));counts['data']+=1
        for i in range(H.shape[0]):
            for a in (1,2):
                sign=((t,i,a),(t+1,i,(-a)%3))
                add(sign,('measurement',t,i,a));counts['measurement']+=1
    assert not collision,collision[:5]
    return {'rounds':rounds,'check_rows':H.shape[0],'physical':H.shape[1],
            'counts':counts,'unique_single_fault_signatures':len(seen),
            'collision_count':len(collision)},seen


def missing_terminal_boundary(H,rounds=3):
    """Exactly count single-fault ambiguity when the perfect final readout is absent.

    A final-round measurement error has only the +a detector in the observed
    time window; a final-round data error on a degree-one H column produces
    that same detector. No physical perfect terminal readout is assumed.
    """
    C=H.tocsc()
    one=np.flatnonzero(np.diff(C.indptr)==1)
    for j in one:
        start,end=C.indptr[j:j+2]
        assert end-start==1
        row=int(C.indices[start]);coeff=int(C.data[start])%3
        for amp in (1,2):
            observed_data=((rounds,row,coeff*amp%3),)
            observed_measurement=((rounds,row,coeff*amp%3),)
            assert observed_data==observed_measurement
    return {'last_round_weight_one_data_columns':len(one),
            'distinct_data_vs_measurement_fault_labels_that_cannot_be_distinguished':2*len(one),
            'first_example_data_column':int(one[0]) if len(one) else None,
            'first_example_detector_row':int(C.indices[C.indptr[one[0]]]) if len(one) else None,
            'interpretation':'Without a perfect endpoint syndrome, last-round data and readout faults are observationally identical whenever the data-check column has one nonzero entry. This is a finite-window no-go, not a proof decoding cannot use temporal priors.'}


def qutrit_syndrome_gate():
    HX,HZ=css_matrices(8)
    DX,dictX=detector_dictionary(HZ)
    DZ,dictZ=detector_dictionary(HX)
    schedX=tanner_schedule(HX);schedZ=tanner_schedule(HZ)
    def hook_guard(H):
        support_lens=np.diff(H.indptr)
        checks=[]
        for i,w in enumerate(support_lens):
            # All suffix faults are assumed to generate the corresponding
            # stabilizer's data-site coefficients, up to an overall multiplier.
            equivalent=[min(k,int(w)-k) for k in range(int(w)+1)]
            checks.append(max(equivalent))
        return {'max_check_weight':int(max(support_lens)),
                'max_reduced_hook_weight':max(checks)}
    guardX=hook_guard(HX);guardZ=hook_guard(HZ)
    missing={'X':missing_terminal_boundary(HZ),'Z':missing_terminal_boundary(HX)}
    assert missing['X']['last_round_weight_one_data_columns']==320
    assert missing['Z']['last_round_weight_one_data_columns']==32
    assert guardX['max_reduced_hook_weight']<=3 and guardZ['max_reduced_hook_weight']<=2
    # Logical splitting: an X logical of weight 8 can be split into 4 vs 4
    # errors with the same ideal H_Z syndrome. It is NOT a proof of a bad
    # decoder at any specified physical noise rate.
    e1=np.zeros(HZ.shape[1],dtype=np.int16);e2=e1.copy()
    e1[:4]=1;e2[4:8]=2
    assert np.array_equal((HZ@e1)%3,(HZ@e2)%3)
    assert np.count_nonzero(e1)==np.count_nonzero(e2)==4
    single_fault_guaranteed_probability={}
    for label,H in [('X',HZ),('Z',HX)]:
        M=3*(H.shape[0]+H.shape[1])
        single_fault_guaranteed_probability[label]={str(p):float((1-p)**M+M*p*(1-p)**(M-1)) for p in (1e-6,1e-5,1e-4)}
    return {'code':'[[1833,81,8]]_3','physical_sites':1833,
            'one_fault_only_guaranteed_event_probability':single_fault_guaranteed_probability,
            'X_check_rows':HX.shape[0],
            'Z_check_rows':HZ.shape[0],
            'X_syndrome_rounds':DX,'Z_syndrome_rounds':DZ,
            'X_measurement_layers':len(schedX),'Z_measurement_layers':len(schedZ),
            'without_perfect_final_boundary':missing,
            'X_check_hook_guard_support_only':guardX,
            'Z_check_hook_guard_support_only':guardZ,
            'weight_four_logical_splitting_ambiguity':True,
            'scope':'Unique single-data or single-measurement phenomenological fault ONLY with perfect final boundary; removing it gives explicit indistinguishable final-round faults; gate schedule conflict-free but no qutrit SUM fault propagation, ancilla leakage, measurement SPAM, decoder threshold or fault-tolerant circuit.'}


def domain_wall_index():
    """Exact index of a 1D supercharge is a toy chirality gate, not 7D G2."""
    # D=d/dx+tanh(x); exact normalized L2 null state sech(x)/sqrt(2).
    x=np.linspace(-12,12,24001)
    u=1/(np.sqrt(2)*np.cosh(x));m=np.tanh(x)
    residual=np.gradient(u,x,edge_order=2)+m*u
    residual_max=float(np.max(np.abs(residual[50:-50])))
    norm=float(np.trapezoid(u*u,x))
    assert residual_max<1e-6 and abs(norm-1)<1e-8,(residual_max,norm)
    # Adjoint D†=-d/dx+m has formal zero mode cosh(x), not L2(R).
    assert np.cosh(12)>80000
    # On periodic S1, ODE Du=0 and D†v=0 each has periodic nonzero
    # solution iff the integral of m(x) over a period is zero.
    periodic=[{'mass':'sin(x)','mass_integral':0.,'ker_D':1,'ker_Ddagger':1,'index':0},
              {'mass':'1','mass_integral':float(2*np.pi),'ker_D':0,'ker_Ddagger':0,'index':0}]
    # A direct sum of N domain walls has index N, so index consistency alone
    # does not predict three generations.
    return {'open_line_D':'d/dx+tanh(x)','normalized_zero_mode':'sech(x)/sqrt(2)',
            'norm_numeric':norm,'ODE_max_residual':residual_max,
            'open_line_ker_D':1,'open_line_ker_Ddagger':0,'open_line_Fredholm_index':1,
            'opposite_wall_index':-1,'periodic_circle_cases':periodic,
            'direct_sum_N_copies_index_N':{str(n):n for n in (1,2,3,4)},
            'E6_complete_27_U1psi_anomaly_per_family':{'mixed_gravitational':16-20+4,
                                                        'cubic':16-80+64,
                                                        'Spin10_squared':2-2},
            'blocking_requirements':'Real compact charged singular G2/ADE Dirac operator, global boundary/inflow conditions, anomaly matching and actual vacuum/Yukawa generation; this 1D SUSY-QM toy is not compact G2 evidence.'}


def spacetime_volume_gate(seed=371):
    """Recover a conformal parameter from density in a KNOWN coordinate chart.
    Not a metric reconstruction from a bare causal order.
    """
    rng=np.random.default_rng(seed)
    truth=.25
    def moment(a):
        zz=quad(lambda x:np.exp(2*a*x*x),-1,1,epsabs=1e-11)[0]
        yy=quad(lambda x:x*x*np.exp(2*a*x*x),-1,1,epsabs=1e-11)[0]
        return yy/zz
    def sample(n):
        accepted=[]
        while len(accepted)<n:
            x=rng.uniform(-1,1,n)
            take=rng.random(n)<np.exp(2*truth*(x*x-1))
            accepted.extend(x[take].tolist())
        return np.array(accepted[:n])
    results=[]
    for n in (500,2000,10000):
        xx=sample(n)
        empirical=float(np.mean(xx*xx))
        estimate=float(brentq(lambda a:moment(a)-empirical,-3,3))
        # Fisher information is 4 Var(x^2); a is identifiable if chart
        # and uniform physical sprinkling intensity are independently known.
        results.append({'n':n,'mean_x_squared':empirical,'estimated_a':estimate,
                        'R_at_origin_estimate':-4*estimate,'true_a':truth})
    assert all(np.isfinite(r['estimated_a']) for r in results)
    return {'metric':'exp(2 a x^2)*(-dt^2+dx^2)',
            'true_a':truth,'scalar_R_at_origin_true':-4*truth,
            'inference_with_known_coordinate_chart_and_uniform_sprinkling':results,
            'order_only_unidentifiable':True,
            'scope':'This estimates volume-weighted coordinate density with a prescribed chart and Poisson measure; it is NOT a manifold reconstruction, Ricci/Einstein equation, or derivation of a causal-set action.'}


def su3_reference_gate(seed=743):
    """Two-quadrature differential Ramsey estimator with drift/visibility guards."""
    rng=np.random.default_rng(seed)
    omega=np.exp(2j*np.pi/3)
    Z=np.diag([1,omega,omega**2]);X=np.roll(np.eye(3),1,axis=0)
    K=Z@X@Z.conj().T@X.conj().T
    assert np.max(abs(K-omega*np.eye(3)))<1e-12
    assert abs(abs(np.trace(K))**2-1-8)<1e-11
    visibility=.85;offset=.37;drift=.10
    def measure(phase,n):
        PX=(1+visibility*np.cos(phase))/2
        PY=(1+visibility*np.sin(phase))/2
        return (2*rng.binomial(n,PX)/n-1)+1j*(2*rng.binomial(n,PY)/n-1)
    def angle(z):return float(np.angle(z))
    simulations=[]
    for n in (250,1000,4000):
        ref=measure(offset,n)
        center=measure(offset+2*np.pi/3+drift,n)
        obs=angle(center/ref)
        diff=angle(np.exp(1j*(obs-2*np.pi/3)))
        simulations.append({'shots_per_each_of_four_quadrature_settings':n,
                            'estimated_phase_difference_radians':obs,
                            'phase_error_vs_center_radians':diff,
                            'normalized_ref_visibility_observed':float(abs(ref)),
                            'normalized_center_visibility_observed':float(abs(center))})
    # Four estimated expectation values (two quadratures for each of two
    # arms), independently sampled, each in [-1,1]. With probability 1-delta,
    # each absolute error <= t=sqrt(2 ln(8/delta)/N); complex error <=sqrt(2)t.
    # For visibility >=v_min, phase error <=asin(sqrt(2)*t/v_min) per arm.
    # If phase drift between arms <=Delta, nearest-phase classification of
    # {0,2pi/3} is certified if Delta+2*phase_err <pi/3.
    delta=.01;vmin=.8;drift_max=.12
    theta=(np.pi/3-drift_max)/2
    allowed_t=(vmin/np.sqrt(2))*np.sin(theta)
    shots=math.floor(2*np.log(8/delta)/(allowed_t**2))+1
    certified_t=np.sqrt(2*np.log(8/delta)/shots)
    total_phase_uncertainty=drift_max+2*np.arcsin(np.sqrt(2)*certified_t/vmin)
    assert total_phase_uncertainty<np.pi/3
    assert abs(np.trace(K)/3-omega)<1e-12
    return {'Weyl_commutator':'omega*I3',
            'adjoint_character_K_and_identity':8,
            'observed_two_quadrature_reference_simulation':simulations,
            'visibility_minimum_assumed':vmin,'relative_drift_max_radians_assumed':drift_max,
            'confidence_delta':delta,'per_setting_shots_sufficient_Hoeffding':shots,
            'total_accepted_shots_four_quadratures':4*shots,
            'certified_max_total_phase_error_radians':float(total_phase_uncertainty),
            'model_boundary':'Controlled fundamental Wilson-loop reference must be physically implementable and gauge invariant; a central GAUGE transformation alone is unobservable on physical color-singlet states. This is a non-gauge dynamical toy unless physical reference charges/loop are provided. Shots exclude loss, calibration errors, time-correlated noise.'}


def memory_loss_guard(seed=1900):
    """Joint finite-shot lower confidence for efficiency AND output frequencies.

    Inputs are an illustrative qutrit seven-setting frequency table. It is NOT
    a reconstruction of physical channels or a pairwise-classicality proof.
    """
    rng=np.random.default_rng(seed)
    gamma=.75;epsilon=.01;eff_true=.995;delta=.01
    p0=1-2*epsilon/3;pl=epsilon/3
    late=[]
    for arm in range(2):
        for j in range(3):
            p=np.full(3,pl)
            p[j]=p0
            late.append(p)
    r=np.array([(1+2*gamma)/3,(1-gamma)/3,(1-gamma)/3],dtype=float)
    assert abs(r.sum()-1)<1e-12
    conf_eff=delta/2;conf_out=delta/2
    def certificate(attempted,accepted,counts):
        nmin=int(min(accepted))
        eta_lower=max(0.,min(float(z)/attempted for z in accepted)-np.sqrt(np.log(7/conf_eff)/(2*attempted)))
        t=np.sqrt(np.log(42/conf_out)/(2*nmin))
        phat=[v/n for v,n in zip(counts,accepted)]
        fid_total=0.
        for offset in (1,4):
            for j,k in combinations(range(3),2):
                upj=np.minimum(1,eta_lower*np.minimum(1,phat[offset+j]+t)+(1-eta_lower))
                upk=np.minimum(1,eta_lower*np.minimum(1,phat[offset+k]+t)+(1-eta_lower))
                fid_total+=min(1,float(np.sqrt(upj*upk).sum()))
        s1low=max(0,3*eta_lower*max(0,phat[0][0]-t)-1)
        return {'attempted_per_setting':int(attempted),
                'minimum_accepted':nmin,'estimated_efficiency_lower_99pct_joint':float(eta_lower),
                'output_coord_confidence_radius':float(t),
                'fidelities_upper_sum':float(fid_total),
                'nonunitality_lower':float(s1low),
                'W3_upper_99pct_joint':float(fid_total-s1low)}
    expected=[]
    # Planning with ideal expected frequencies. Confidence guarantees hold for
    # ALL channels satisfying assumptions, but negative W forecast is conditional.
    for M in (500_000,1_000_000,2_000_000,5_000_000):
        accepted=[round(M*eff_true)]*7
        counts=[p*n for p,n in zip([r]+late,accepted)]
        expected.append(certificate(M,accepted,counts))
    actual=[]
    for M in (2_000_000,5_000_000):
        accepted=rng.binomial(M,eff_true,size=7)
        counts=[rng.multinomial(int(n),p) for n,p in zip(accepted,[r]+late)]
        actual.append(certificate(M,accepted,counts))
    assert expected[-1]['W3_upper_99pct_joint']<0
    return {'source':'Beyer et al. 2026, arXiv:2611.17268, Supplement VI S38',
            'confidence_event':'Seven calibration lower bounds plus 21 conditional output-coordinate intervals, union bound delta=.01. Requires IID attempts at each setting, stationary state-independent acceptance within a setting, accepted measurement samples IID, perfect characterization of preparation and measurement and no hidden trial selection.',
            'nominal_efficiency':eff_true,'calibration_fraction':conf_eff,
            'measurement_fraction':conf_out,
            'expected_frequency_planning':expected,
            'seeded_binomial_multinomial_forecasts':actual,
            'hierarchy_caution':'Negative W3 excludes one common 3-time classical model. It does NOT prove every pair of channels admits a 2-time classical model, nor the existence of a single physical 3-time process reproducing independently specified ideal snapshot data.',
            'physical_boundary':'No laboratory detector calibrations, process tensor, CPTP dynamics between all times, experimental quantum memory, or certified classical pairwise decompositions.'}



def three_context_classical_gluing():
    """Pairwise-compatible binary marginals can fail global compatibility.

    A conceptual analogy to classical-instrument temporal compatibility, NOT
    equivalent to a quantum process tensor or a W3 witness.
    """
    assignments=list(product((0,1),repeat=3))
    def solve(q):
        # Each pair separately has uniform marginals and disagreement prob q.
        rows=[];rhs=[]
        for i,j in combinations(range(3),2):
            for a,b in product((0,1),repeat=2):
                rows.append([int(x[i]==a and x[j]==b) for x in assignments])
                rhs.append((q/2) if a!=b else ((1-q)/2))
        sol=linprog(np.zeros(8),A_eq=np.array(rows),b_eq=np.array(rhs),
                    bounds=(0,None),method='highs')
        return {'q_pairwise_anticorrelation':q,'global_joint_exists':bool(sol.success),
                'max_pair_marginal_residual':float(np.max(np.abs(np.array(rows)@sol.x-np.array(rhs)))) if sol.success else None,
                'one_joint_distribution':np.around(sol.x,12).tolist() if sol.success else None}
    cases=[solve(q) for q in (.5,.6,2/3,.75,1.)]
    assert [c['global_joint_exists'] for c in cases]==[True,True,True,False,False]
    return {'status':'EXACT_BINARY_MARGINAL_COMPATIBILITY_ANALOGY',
            'combinatorial_proof':'Each assignment of three bits has either zero or two disagreeing pairs, so sum of three pairwise disagreement probabilities <= 2. Three equal pair probabilities require q<=2/3. Symmetric bit-flip pair marginals are individually valid for every q in [0,1].',
            'max_symmetric_q_gluable':2/3,'cases':cases,
            'boundary':'This is a classical probability marginal gluing example, NOT a certified pairwise classical decomposition for the three qutrit channels, not contextuality of a measured experiment, and not a quantum memory proof.'}


def run(write=True):
    tracks={
      'exceptional_chiral_index_toy':domain_wall_index(),
      'phenomenological_qutrit_css':qutrit_syndrome_gate(),
      'causal_volume_density_inverse':spacetime_volume_gate(),
      'SU3_reference_phase_robustness':su3_reference_gate(),
      'three_time_memory_two_layer_confidence':memory_loss_guard(),
      'outside_box_three_context_marginal_gluing':three_context_classical_gluing(),
    }
    out={'status':'MODEL_SCOPED_FIVE_TRACK_CERTIFICATES_NOT_PHYSICAL_TOE',
         'date':'2026-11-20','main_w33_baseline':'f9685d73c897f1fde12b15667aff5defb388ea37',
         'tracks':tracks}
    if write:
        OUTPUT.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    return out

if __name__=='__main__':
    o=run()
    for k,v in o['tracks'].items():
        print(k)
        if k=='phenomenological_qutrit_css':
            print('  layers',v['X_measurement_layers'],v['Z_measurement_layers'],
                  'single syndrome labels',v['X_syndrome_rounds']['unique_single_fault_signatures'],
                  v['Z_syndrome_rounds']['unique_single_fault_signatures'])
        elif k=='three_time_memory_two_layer_confidence':
            print('  expected:',[(x['attempted_per_setting'],round(x['W3_upper_99pct_joint'],5)) for x in v['expected_frequency_planning']])
            print('  seeded:',[(x['attempted_per_setting'],round(x['W3_upper_99pct_joint'],5)) for x in v['seeded_binomial_multinomial_forecasts']])
        elif k=='causal_volume_density_inverse':
            print('  a estimates',[(x['n'],round(x['estimated_a'],5)) for x in v['inference_with_known_coordinate_chart_and_uniform_sprinkling']])
        elif k=='SU3_reference_phase_robustness':
            print('  sufficient per quadrature',v['per_setting_shots_sufficient_Hoeffding'])
        elif k=='outside_box_three_context_marginal_gluing':
            print('  gluing feasible q:',[(v1['q_pairwise_anticorrelation'],v1['global_joint_exists']) for v1 in v['cases']])
        else:print('  index',v['open_line_Fredholm_index'],'ODE residual',v['ODE_max_residual'])
