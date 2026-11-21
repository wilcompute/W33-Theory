#!/usr/bin/env python3
"""Four independent TOE falsifiers plus one bonus built from W33 geometry.

1. Optical: central switch compressibility vs noncentral input-dependent fringes.
2. Chirality: 4D torus twisted Dirac index polynomial, anomaly sieve.
3. Readout: stable-gain calibration false positive under bounded drift.
4. Gauge nonidentifiability: gauge-invariant Z3 Wilson 8-cycle with free beta.
5. Dimensional scaling: finite incidence cannot fix a dimensional speed.

All are mathematical/seeded numerical tests, NOT device data or a TOE.
"""
from __future__ import annotations
from itertools import combinations,product
from pathlib import Path
from collections import Counter
import json,math
import numpy as np
import networkx as nx
from scipy.linalg import expm
from scipy.stats import beta as beta_dist
from toe_20261120_fivefront_plus_bridge import weyl, symp, optical_switch

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/toe_20261120_five_operational_gates.json'
I9=np.eye(9,dtype=complex)
I3=np.eye(3,dtype=complex)
H=np.array([[1,1],[1,-1]],complex)/math.sqrt(2)


def optical_compression_and_noncentral_control():
    # W33 Pauli pair, central relative phase, full 18x18 interferometer.
    u=(1,0,0,0);v=(0,0,1,0)
    A=weyl(u);B=weyl(v);U0=A@B;U1=B@A
    phase=np.trace(U0@U1.conj().T)/9
    assert abs(abs(phase)-1)<1e-12
    Wctrl=H@np.diag([phase,1.])@H
    V,_,_=optical_switch(u,v,0.)
    reduced=np.kron(Wctrl,U1)
    reduction_error=float(np.max(abs(V-reduced)))
    assert reduction_error<1e-12
    # Single photon in 18 modes to test a genuinely noncentral gate pair:
    # A shifts first qutrit, B is a diagonal non-Clifford phase gate.
    X=np.roll(I3,1,axis=0)
    A=np.kron(X,I3)
    theta=.4
    B=np.kron(np.diag(np.exp(1j*np.array([0.,theta,-theta]))),I3)
    U0=A@B;U1=B@A
    K=U1.conj().T@U0
    assert np.max(abs(K.conj().T@K-I9))<1e-12
    C=np.diag(K)
    assert np.max(abs(K-np.diag(C)))<1e-12
    c=np.trace(K)/9
    noncentral2=9*(1-abs(c)**2)
    assert noncentral2>.05
    # Fringes depend on input mode, so a single 2-arm phase gadget *cannot*
    # reproduce all nine input-control correlations.
    q=np.kron(H,I9)
    v18=q@np.block([[U0,np.zeros((9,9))],[np.zeros((9,9)),U1]])@q
    probs=[]
    for i in range(9):
        psi=np.zeros(18);psi[i]=1
        p=float(np.linalg.norm((v18@psi)[:9])**2)
        predicted=float((1+np.real(K[i,i]))/2)
        assert abs(p-predicted)<1e-12
        probs.append(p)
    spread=max(probs)-min(probs)
    assert spread>.04
    # Control-vs-purified-target entropy for initial maximally mixed target.
    lam=np.array([(1+abs(c))/2,(1-abs(c))/2])
    entropy=-float(np.sum(lam*np.log2(lam)))
    # Total coupling matrix includes two path Hadamards, 18 balanced couplers
    # (9 in each) plus arbitrary 9-mode blocks; never infer physical losses.
    return {
      'status':'PASS_EXACT_CENTRAL_COMPRESSION_AND_NONCENTRAL_CONTROL',
      'central_W33_pair_symplectic_exponent':symp(u,v),
      'central_pair_control_tensor_target_factorization_max_residual':reduction_error,
      'known_gate_central_pair_target_independent_two_mode_phase_gadget':True,
      'noncentral_control_phase_parameter_radians':theta,
      'noncentral_relative_order_trace_abs':float(abs(c)),
      'noncentral_operator_Frobenius_squared':float(noncentral2),
      'nine_input_control_port_probabilities':[float(x) for x in probs],
      'nine_input_fringe_spread':float(spread),
      'noncentral_control_purified_target_entropy_bits':entropy,
      'ideal_18_mode_network_unitarity_error':float(np.max(abs(v18.conj().T@v18-np.eye(18)))),
      'boundary':'Central W33 known-gate fringes need only path-phase gadget; this does not simulate a black-box quantum switch in a fixed order. Noncentral gates make 18-mode controlled target actions nontrivial. No photonic device was accessed.'
    }


def anomaly_polynomial_sieve():
    # Dirac index on a flat four-torus for a common background rank-r bundle E
    # twisted by psi-charge q line bundle L:
    # I(q)=int[ch2(E)+q c1(E)c1(L)+(r q^2/2)c1(L)^2]
    charges=[1,-2,4]
    A=np.array([[1,q,q*q] for q in charges],dtype=int)
    # Two equalities I(1)-I(-2)=0 and I(1)-I(4)=0 force B=C=0.
    D=np.array([A[0]-A[1],A[0]-A[2]],dtype=int)
    assert np.linalg.matrix_rank(D[:,1:])==2
    # Integer proof: differences 3B-3C=0, -3B-15C=0 -> B=C=0.
    assert D[:,1:].tolist()==[[3,-3],[-3,-15]]
    for B in range(-15,16):
      for C in range(-15,16):
        if np.array_equal(D@np.array([3,B,C]),[0,0]):
          assert (B,C)==(0,0)
    # If index polynomial is charge-independent, all 27 components have same
    # net index and their isolated Spin10xU1psi anomalies vanish.
    anomaly=np.array([[16,-20,4],[16,-80,64],[2,-2,0]],int)
    for I0 in (-3,0,3):
        n=np.array([I0]*3)
        assert np.array_equal(anomaly@n,np.zeros(3))
    # Pure abelian n12*n34=Q yields (Q,4Q,16Q), so anomaly-free iff Q=0.
    for Q in (-8,-3,-1,1,3,8):
        assert not np.array_equal(anomaly@(Q*np.array([1,4,16])),np.zeros(3))
    # Topological counterexample: common auxiliary SU(2) bundle E over T4
    # with c1(E)=0 and c2(E)=-3 has int ch2(E)=3. For L trivial,
    # I(q)=3 independent of psi-charge, and all 27s are complete.
    # This is a topological INDEX prescription, not a smooth HYM solution or
    # singular-G2 charged Dirac operator.
    return {
      'status':'PASS_COMMON_BUNDLE_CHARGE_POLYNOMIAL_NO_GO',
      'index_polynomial':'I(q)=A+Bq+Cq²; A=int ch2(E), B=int c1(E)c1(L), C=r/2 int c1(L)²',
      'E6_psi_charges':charges,
      'difference_matrix_on_A_B_C':D.tolist(),
      'equal_index_condition':'I(1)=I(-2)=I(4) iff B=C=0 (the q-linear and q² terms both vanish).',
      'complete_three_family_index_vector':[3,3,3],
      'common_SU2_twist_topological_example':{'c1_E':0,'c2_E':-3,'L_trivial':True,'index_in_each_27_component':3},
      'flux_only_Q3_indices':[3,12,48],
      'flux_only_Q3_anomalies':(anomaly@np.array([3,12,48])).tolist(),
      'no_go_scope':'Applies to one shared rank-r internal bundle E tensored with U1psi power L^q and the isolated 16+10+1 chiral census; distinct E bundles, inflow, broken gauge groups, or extra sectors evade it.',
      'physical_boundary':'An SU2 topological c2=-3 choice does not dynamically select 3, construct a stable gauge/HYM bundle, reproduce singular G2 compactification, fix Yukawas, or identify a physical vacuum.'
    }


def cp_low(k,n,alpha):
    return 0. if k==0 else float(beta_dist.ppf(alpha/2,k,n-k+1))

def cp_high(k,n,alpha):
    return 1. if k==n else float(beta_dist.ppf(1-alpha/2,k+1,n-k))

def calibration_bound(k_test,k_cal,n,delta=.01,drift_bound=0.,readout_bias_bound=0.,prep_trace_error=0.):
    lo=cp_low(k_test,n,delta/2)
    hi=cp_high(k_cal,n,delta/2)
    gain_up=min(1.,max(0.,2*hi-1)+drift_bound)
    contrast_lower=max(0.,2*lo-1-readout_bias_bound)
    val=max(0.,min(1.,contrast_lower/gain_up-prep_trace_error)) if gain_up>0 else 0.
    # Important: if gain_up==0, physical qutrit phase information is absent;
    # fail closed (no certificate).
    return 9*(1-val*val)


def noise_drift_calibration():
    # Strong counterexample to using a reference calibrated at different gain.
    # Marginal test r=.97 gives Frobenius²=9*(1-.97²)=.5319.
    rng=np.random.default_rng(9261)
    n=150_000;gcal=.94;gtest=.98;rtruth=.97;tol2=.25**2
    nrep=400
    cal=rng.binomial(n,(1+gcal)/2,size=nrep)
    test=rng.binomial(n,(1+gtest*rtruth)/2,size=nrep)
    bad=np.array([calibration_bound(int(a),int(b),n,drift_bound=0.) for a,b in zip(test,cal)])
    guarded=np.array([calibration_bound(int(a),int(b),n,drift_bound=.04) for a,b in zip(test,cal)])
    false_bad=int(np.sum(bad<=tol2));false_guarded=int(np.sum(guarded<=tol2))
    assert false_bad>380,(false_bad,False)
    assert false_guarded==0,false_guarded
    # 2% detector error & 0.5% phase preparation bias cannot be jointly
    # certified to tolerance .25 unless calibrated tightly enough.
    min_req=math.sqrt(1-tol2/9)
    assert min_req>.996
    # The exact CP intervals are valid marginally; the joint confidence
    # depends additionally on *external* drift and bias upper bounds.
    return {
      'status':'PASS_GUARDED_NONZERO_DRIFT_CP_FALSE_CERTIFICATE_FALSIFIER',
      'true_test_unitary_trace_abs':rtruth,
      'true_test_noncentrality_Frobenius_squared':9*(1-rtruth*rtruth),
      'calibration_gain':gcal,'test_gain':gtest,
      'gain_drift_unmodeled':gtest-gcal,
      'accepted_measurements_per_calibration_and_test_arm':n,
      'confidence_per_joint_calibration':.99,
      'iid_replications':nrep,
      'false_certifications_if_zero_drift_assumed':false_bad,
      'false_certifications_with_drift_bound_0p04':false_guarded,
      'Frobenius_tolerance':.25,
      'required_trace_magnitude_for_tolerance':float(min_req),
      'any_real_noise_data':False,
      'calibration_contract':'IID independent accepted events, identical gain except bounded drift, bounded additive contrast bias, independently warranted unitary target, verified preparation trace-distance bound. Exact CP intervals for each arm combined by union bound.',
      'interpretation':'An apparently excellent normalized-trace interference fringe can falsely certify centrality if the test-arm gain exceeds reference-arm gain. Independent drift bounds are essential.'
    }


def canonical(v):
    v=tuple(int(x)%3 for x in v)
    a=next((t for t in v if t),None)
    assert a
    return tuple((t if a==1 else 2*t)%3 for t in v)

def pairing(u,v):
    return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3

def w33_levi_graph_and_8cycle():
    points40=sorted({canonical(v) for v in product(range(3),repeat=4) if any(v)})
    assert len(points40)==40
    lines=set()
    for u,v in combinations(points40,2):
        if pairing(u,v)!=0:continue
        proj=frozenset(canonical(tuple((a*u[h]+b*v[h])%3 for h in range(4)))
                      for a,b in product(range(3),repeat=2) if a or b)
        assert len(proj)==4
        lines.add(proj)
    lines=sorted((tuple(sorted(x)) for x in lines))
    assert len(lines)==40
    pidx={v:i for i,v in enumerate(points40)}
    g=nx.Graph()
    g.add_nodes_from(range(80))
    for j,line in enumerate(lines):
        for pt in line:g.add_edge(pidx[pt],40+j)
    assert g.number_of_edges()==160 and set(dict(g.degree()).values())=={4}
    # BFS search for an 8-cycle with no reused edges/vertices.
    cycle=None
    for start in range(40):
      def dfs(path):
        here=path[-1]
        if len(path)==8:
          return path if g.has_edge(here,start) else None
        for nxt in sorted(g.neighbors(here)):
          if nxt==start or nxt in path:continue
          c=dfs(path+[nxt])
          if c is not None:return c
        return None
      cycle=dfs([start])
      if cycle is not None:break
    assert cycle and len(cycle)==8 and all(g.has_edge(cycle[i],cycle[(i+1)%8]) for i in range(8))
    return {'graph':g,'points':points40,'lines':lines,'cycle':cycle}

def z3_wilson_nondeterminacy():
    geom=w33_levi_graph_and_8cycle();cyc=geom['cycle']
    # 8 consecutive edges Z3. Wilson holonomy product of gauge elements
    # W=omega**(sum oriented exponents mod3).
    vals=[1.,-0.5,-0.5]
    sample_beta=[0.,.25,1.,2.,5.]
    expectations=[]
    for coupling in sample_beta:
        w=np.exp(coupling*np.array(vals))
        z=w.sum()
        mean=float(np.dot(vals,w)/z)
        variance=float(np.dot(np.array(vals)**2,w)/z-mean**2)
        # Z3 loop holonomy real parts are 1,-1/2,-1/2.
        # At beta=0 mean is zero and derivative is Var=1/2.
        mean=float((math.exp(coupling)-math.exp(-coupling/2)) /
                  (math.exp(coupling)+2*math.exp(-coupling/2)))
        assert variance>0
        assert abs(variance - 1.5 * math.exp(1.5*coupling) / (math.exp(1.5*coupling)+2)**2 * 3) < 1e-11
        expectations.append({'coupling_beta':coupling,'Wilson_Re_expected':mean,
                             'beta_derivative_as_variance':variance})
    assert abs(expectations[0]['Wilson_Re_expected'])<1e-14
    assert expectations[2]['Wilson_Re_expected']>.5
    assert expectations[-1]['Wilson_Re_expected']>.99
    # Exhaustive 3^8 assignments: exact 3^7 degeneracy for each holonomy.
    counts=Counter(sum(z)%3 for z in product(range(3),repeat=8))
    assert sorted(counts.values())==[3**7]*3
    # Vertex gauge transformations on the cycle preserve holonomy.
    rng=np.random.default_rng(666)
    for _ in range(150):
        edges=rng.integers(0,3,size=8)
        gauge=rng.integers(0,3,size=8)
        transformed=(edges+gauge-np.roll(gauge,-1))%3
        assert int(edges.sum()%3)==int(transformed.sum()%3)
    # Coupling rescaling is a distinct gauge-invariant action, not a relabel.
    return {
      'status':'PASS_EXACT_W33_WILSON_COUPLING_NONIDENTIFIABILITY',
      'W33_Levi_vertices':80,'W33_Levi_edges':160,
      'selected_minimal_8cycle_vertices':cyc,
      'cycle_edge_variables_Z3':8,
      'exhaustive_gauge_link_assignments':3**8,
      'degeneracy_each_Wilson_holonomy':3**7,
      'bare_partition_factor':'Z8(beta)=3^7*(exp(beta)+2exp(-beta/2))',
      'Wilson_loop_analytic_expectation':'<Re W>=(exp(beta)-exp(-beta/2))/(exp(beta)+2exp(-beta/2))',
      'calculated_couplings':expectations,
      'exact_gauge_transform_invariance_trials':150,
      'proof_obstruction':'Same W33 incidence and same Z3 gauge group admit a continuous family of gauge-invariant actions with different Wilson expectations. No parameter-free coupling or Wilson expectation is selected by graph incidence alone.',
      'boundary':'This is a finite graph single-plaquette Z3 lattice gauge counterexample, not the full dynamical W33 theory, nor experimental measurement. Choosing an additional action could select beta by a dynamical principle.'
    }

def dimensional_scale_free_parameter():
    # Graph edges have unit combinatorial length, time step is integer ticks.
    # Embedding physical edge length ell and tick duration tau implies v=ell/tau.
    # Both may be rescaled without modifying finite graph incidence/spectra.
    v_examples=[ell/tau for ell,tau in [(1e-9,1e-9),(1e-9,1e-12),(1e-6,1e-12)]]
    assert v_examples==[1.,1000.0000000000001,1000000.0] or np.allclose(v_examples,[1,1000,1e6])
    return {
     'status':'PASS_DIMENSIONAL_RESCALE_NO_GO',
     'combinatorial_speed':'one edge per tick',
     'physical_speed_law':'v=(physical_length_per_edge)/(physical_time_per_tick)',
     'different_physical_speeds_with_same_graph':v_examples,
     'scope':'A dimensionful speed cannot be numerically determined by dimensionless finite combinatorial incidence without a calibrated length/time ratio or additional dynamics.'
    }

def main(write=True):
    out={'schema':'toe.deep_five_20261120.v1',
         'front_optical':optical_compression_and_noncentral_control(),
         'front_chirality':anomaly_polynomial_sieve(),
         'front_noise':noise_drift_calibration(),
         'front_physics_prediction':z3_wilson_nondeterminacy(),
         'outside_box_dimensional_scale':dimensional_scale_free_parameter(),
         'overall_scope':'Executable standard quantum/math examples; no real lab, charged G2 index, unique action, or beyond-standard-model parameter-free observable.'}
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    return out
if __name__=='__main__':
 print(json.dumps(main(),indent=2))
