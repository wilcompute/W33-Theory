#!/usr/bin/env python3
"""Six bounded W33 / quantum-memory research controls, 2026-11-20.

Reproduces independent finite mathematical controls and idealized measurement
contracts. Does NOT establish an E8 UV model, a physical G2 compactification,
an experimental Holonet, or quantum gravity.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
from collections import Counter

import networkx as nx
import numpy as np
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/toe_20261120_six_open_physics_gates.json'
I3=np.eye(3,dtype=complex)
OMEGA=np.exp(2j*np.pi/3)
X=np.roll(I3,1,axis=0)
Z=np.diag([1,OMEGA,OMEGA**2])


def e8_cubic_gate():
    # The E6 symmetric cubic on its 27, restricted to its diagonal
    # 3-dimensional Jordan subspace, is the polarized determinant xyz.
    d=np.zeros((3,3,3),float)
    eps=np.zeros((3,3,3),float)
    for perm in itertools.permutations(range(3)):
        d[perm]=1/6
        eps[perm]=(-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
    def cubic(a,b,c):
        return float(np.einsum('abc,ijk,ai,bj,ck->',d,eps,a,b,c))
    rng=np.random.default_rng(10020)
    M=rng.normal(size=(3,3))
    same=cubic(M,M,M)
    two=cubic(M,M,rng.normal(size=(3,3)))
    A=np.zeros((3,3));B=A.copy();C=A.copy()
    A[0,0]=1;B[1,1]=1;C[2,2]=1
    three=cubic(A,B,C)
    flipped=cubic(B,A,C)
    assert abs(same)<1e-12 and abs(two)<1e-12
    assert abs(three-1/6)<1e-12 and abs(flipped+1/6)<1e-12
    return {
        'adjoint_248_E6xSU3_branching':{'78x1':78,'1x8':8,'27x3':81,'27barx3bar':81},
        'single_identical_commuting_27x3_E6cubic_epsilon':same,
        'two_identical_commuting_27x3_E6cubic_epsilon':two,
        'three_distinct_27x3_cubic_example':three,
        'interchanging_two_distinct_copies':flipped,
        'conclusion':'The E6-symmetric-cubic times SU3 epsilon invariant is alternating in distinct field copies; one-copy and two-copy commuting contractions vanish, three distinct chiral multiplets can give a nonzero trilinear coupling.',
        'scope':'This restricted component test is not a construction of a full E8-invariant superpotential or 19 singlet multipliers.'}


def projectivize(v):
    t=tuple(int(x)%3 for x in v)
    z=next(a for a in t if a)
    inv=1 if z==1 else 2
    return tuple((a*inv)%3 for a in t)

def symp(u,v):
    return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3

def levi_graph():
    points=sorted({projectivize(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    index={p:k for k,p in enumerate(points)}
    lines=set()
    for i,u in enumerate(points):
        for v in points[i+1:]:
            if symp(u,v):continue
            l=frozenset(index[projectivize(tuple((a*u[j]+b*v[j])%3 for j in range(4)))]
                for a,b in itertools.product(range(3),repeat=2) if (a or b))
            assert len(l)==4
            lines.add(l)
    lines=sorted(lines,key=lambda s:tuple(sorted(s)))
    g=nx.Graph();g.add_nodes_from(range(80))
    for i,line in enumerate(lines):
        for p in line:g.add_edge(p,40+i)
    assert len(points)==len(lines)==40 and g.number_of_edges()==160
    assert nx.is_connected(g)
    return g

def hodge_subcode_gate():
    g=levi_graph()
    n,m=g.number_of_nodes(),g.number_of_edges()
    k=m-n+1
    edges=sorted((min(a,b),max(a,b)) for a,b in g.edges())
    def cycle_dim(fault_edges):
        h=g.copy();h.remove_edges_from(fault_edges)
        return h.number_of_edges()-h.number_of_nodes()+nx.number_connected_components(h)
    assert k==81
    assert nx.edge_connectivity(g)==4
    one=cycle_dim(edges[:1]);two=cycle_dim(edges[:2])
    chosen=sorted((min(0,v),max(0,v)) for v in g.neighbors(0))
    four=cycle_dim(chosen)
    assert (one,two,four)==(80,79,78)
    # Construct 80 independent exact oriented cycle vectors avoiding edge e.
    deleted=g.copy();bad=edges[0];deleted.remove_edge(*bad)
    tree=nx.minimum_spanning_tree(deleted)
    treeedges={tuple(sorted(x)) for x in tree.edges()}
    non_tree=[e for e in sorted(deleted.edges()) if tuple(sorted(e)) not in treeedges]
    edgeidx={e:i for i,e in enumerate(edges)}
    C=np.zeros((m,len(non_tree)),dtype=np.int32)
    for col,(a,b) in enumerate(non_tree):
        path=nx.shortest_path(tree,a,b)
        oriented=list(zip(path,path[1:]))+[(b,a)]
        for u,v in oriented:
            e=tuple(sorted((u,v)))
            C[edgeidx[e],col]+=(1 if (u,v)==e else -1)
    D=np.zeros((n,m),dtype=np.int32)
    for j,(a,b) in enumerate(edges):D[a,j]=-1;D[b,j]=1
    assert np.count_nonzero(D@C)==0
    assert np.count_nonzero(C[edgeidx[bad]])==0
    assert C.shape==(160,80) and np.linalg.matrix_rank(C)==80
    # Any k>1 subcode of ANY n-mode single-particle space cannot
    # satisfy KL for {I,U_e} over ALL e. Rank( P |e><e| P ) <=1,
    # and summing all E_e=I then contradicts nonzero P.
    # This is independent of specific W33 Hodge geometry.
    return {'Levi_vertices':n,'Levi_flags':m,'Hodge_dimension':k,
      'Levi_edge_connectivity':nx.edge_connectivity(g),
      'known_one_bad_edge_noiseless_subcode_dim':one,
      'known_two_bad_edges_noiseless_subcode_dim':two,
      'known_four_edge_star_noiseless_subcode_dim':four,
      'explicit_one_bad_edge_cycle_basis_vectors':int(C.shape[1]),
      'exact_incidence_cycle_residual':int(np.count_nonzero(D@C)),
      'corrupt_edge_coordinate_nonzero_count':int(np.count_nonzero(C[edgeidx[bad]])),
      'unrestricted_unknown_each_edge_phase_code_dimension_max':1,
      'parallel_multiparticle_CSS_prior_art':'Repo 9c9d65d adds [[638,81,dX=3,dZ=8]]_3 mixed Levi/repetition hypergraph-product with 638 distinct qutrits; that is a different Hilbert-space resource.'}


def measured_fidelity_bound(q1,q2):
    """Classical Bhattacharyya from basis measurement bounds quantum root fidelity above."""
    return float(np.sum(np.sqrt(np.maximum(0,q1)*np.maximum(0,q2))))

def witness_upper_from_counts(initial_counts,late_counts,delta=.01):
    """Distribution-free finite-shot upper bound, 7 independent 3-outcome settings.

    A 21-coordinate union Hoeffding event gives simultaneous |p-hat|<=t.
    F_quantum <= F_classical (monotonicity under projective measurement),
    and S1 >= .5 sum |3 q_k - 1| by trace-distance data processing.
    """
    counts=[np.array(initial_counts,dtype=int)]+[np.asarray(q,dtype=int) for q in late_counts]
    assert len(counts)==7 and all(q.shape==(3,) for q in counts)
    n=int(counts[0].sum());assert n>0 and all(int(q.sum())==n for q in counts)
    t=math.sqrt(math.log(2*21/delta)/(2*n))
    estimates=[q/n for q in counts]
    fsum=0.
    for first in (1,4):
        for a,b in itertools.combinations(range(3),2):
            # Each unknown Born probability is <=hat p + t. Clipping at 1.
            hi=np.minimum(1,estimates[first+a]+t)
            hj=np.minimum(1,estimates[first+b]+t)
            fsum+=measured_fidelity_bound(hi,hj)
    # Actual nonunitality >= TV measured against completely mixed output.
    s_lower=.5*sum(max(0,abs(3*q-1)-3*t) for q in estimates[0])
    return {'N_per_setting':n,'settings':7,'accepted_shots_total':7*n,
      'simultaneous_probability_radius':t,'quantum_fidelities_upper':fsum,
      'nonunitality_lower':s_lower,'witness_upper':fsum-s_lower,
      'confidence_at_least':1-delta}

def qutrit_model_free_gate():
    gamma=.75; eps=.01;delta=.01
    q0=np.array([(1+2*gamma)/3,(1-gamma)/3,(1-gamma)/3])
    a=1-2*eps/3;b=eps/3
    late=[np.array([a if i==j else b for i in range(3)]) for j in range(3)]*2
    # Rigorous prospective worst-case shot budget: with probability >=1-delta,
    # p_hat <= p+t and >=p-t, so p_upper <= p+2t, S_lower >=2gamma-9t.
    L=math.log(2*21/delta)
    def worst(n):
        t=math.sqrt(L/(2*n));s=2*t
        fpair=2*math.sqrt((a+s)*(b+s))+(b+s)
        return 6*fpair-2*gamma+9*t
    realroot=brentq(worst,100000,300000)
    n=math.ceil(realroot)+1  # strict negativity for mathematical contract
    assert worst(n)<0 and worst(n-1)>=-1e-5
    # Use prospective larger n so one seeded measurement gives a
    # comfortably negative confidence upper without relying on lucky shots.
    N=200000
    rng=np.random.default_rng(2026112001)
    samples=[rng.multinomial(N,q0)]+[rng.multinomial(N,p) for p in late]
    observed=witness_upper_from_counts(samples[0],samples[1:],delta)
    true=6*(2*math.sqrt(a*b)+b)-2*gamma
    assert true<0 and observed['witness_upper']<0
    # A coherent output unitary cannot alter the true quantum fidelity,
    # but the fixed-basis measurement upper bound need not be invariant.
    return {'ideal_native_qutrit_gamma':gamma,'output_depolarizing_reference_epsilon':eps,
      'true_model_witness':true,'measurement_only_protocol_has_no_depolarization_assumption':True,
      'outcome_settings':7,'outcomes_each':3,'union_bound_coordinates':21,
      'worst_case_sufficient_shots_per_setting':n,
      'worst_case_total_accepted_shots':7*n,
      'prospective_seeded_N_per_setting':N,'prospective_seeded_certificate':observed,
      'confidence':1-delta,
      'assumptions':'Each stationary CPTP channel, exact MUB inputs and measurement bases, independent accepted multinomial trials, fair loss sampling. Pairwise classicality of a noisy real device requires independent testing.'}


def haar3(rng):
    M=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    Q,R=np.linalg.qr(M)
    Q=Q@np.diag(np.diag(R)/np.maximum(abs(np.diag(R)),1e-20))
    return Q/np.linalg.det(Q)**(1/3)

def su3_richardson_gate():
    rng=np.random.default_rng(2269)
    A=haar3(rng);B=haar3(rng);K=A@B@A.conj().T@B.conj().T
    G=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    eta0=.8*I3+.2*(3*G.conj().T@G/np.trace(G.conj().T@G).real)
    def drift_matrix(scale):
        M=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
        H=(M+M.conj().T)/2;H-=np.trace(H)/3*I3
        return scale*H/max(np.linalg.norm(H,2),1)
    E1=drift_matrix(.08);E2=drift_matrix(.12);E3=drift_matrix(.04);E4=drift_matrix(.06)
    W=[np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b) for a,b in itertools.product(range(3),repeat=2)]
    def measured(M,t,quartic=False):
        eta=eta0+t*E1+t*t*E2+t**3*E3
        if quartic:eta=eta+t**4*E4
        assert min(np.linalg.eigvalsh(eta))>.35
        return 3*np.trace(eta@M@K@M.conj().T)/np.trace(eta).real
    h=np.array([(j-4)/8 for j in range(9)])
    chronological=np.mean([measured(M,t) for M,t in zip(W,h)])
    palindrome=np.mean([(measured(M,t)+measured(M,-t))/2 for M,t in zip(W,h)])
    def richardson(quartic):
        value=[]
        for M,t in zip(W,h):
            close=(measured(M,t,quartic)+measured(M,-t,quartic))/2
            far=(measured(M,2*t,quartic)+measured(M,-2*t,quartic))/2
            value.append((4*close-far)/3)
        return np.mean(value)
    cubic=richardson(False)
    quartic=richardson(True)
    target=np.trace(K)
    assert abs(cubic-target)<1e-12
    assert abs(chronological-target)>1e-5 and abs(palindrome-target)>1e-5
    assert abs(quartic-target)>1e-6
    return {'Weyl_settings':9,'chronological_exposures':9,'linear_symmetric_exposures':18,
      'quadratic_and_cubic_cancelled_exposures':36,
      'chronological_trace_error':abs(chronological-target),
      'palindrome_trace_error_quadratic_survives':abs(palindrome-target),
      'Richardson_36_trace_error_through_cubic':abs(cubic-target),
      'quartic_drift_not_cancelled_trace_error':abs(quartic-target),
      'identity':'(4/3)*(m(+h)+m(-h))/2 -(1/3)*(m(+2h)+m(-2h))/2; cancels orders 1,2,3 in fixed-trace detector model',
      'equal_exposure_shot_variance_inflation_vs_plain_four_measurement_average':34/9,
      'limitations':'Signed estimator increases variance; requires exact timing, fixed detector trace, coherent Weyl rotations, no correlated setting-dependent loss.'}


def e6_chirality_gate():
    # Each nonet has SU3^3 fundamental/antifundamental charges (+1,-1,0),
    # with dimensions (3,3,1) on carrier; a fundamental of a given factor
    # occurs three times due to the other nontrivial SU3 factor.
    weights=((1,-1,0),(0,1,-1),(-1,0,1))
    anomalies=tuple(sum(3*w[i] for w in weights) for i in range(3))
    center=(2,1,0)
    center_exponents=tuple(sum(w[i]*center[i] for i in range(3))%3 for w in weights)
    assert anomalies==(0,0,0) and center_exponents==(1,1,1)
    return {'E6_27_trinification_nonets':['(3,3bar,1)','(1,3,3bar)','(3bar,1,3)'],
      'dimension':3*9,'SU3_cubic_anomaly_per_factor':anomalies,
      'three_identical_27_family_anomalies':tuple(3*a for a in anomalies),
      'central_element_in_SU3_cubed':'(omega^2,omega,1)',
      'center_exponent_on_each_nonet':center_exponents,
      'limitation':'Anomaly-free chiral representation is compatible group bookkeeping, not charged G2 Dirac zero modes, a singular compactification, or realistic Yukawa masses.'}


def minkowski_sprinkle(n,d,rng):
    ts=[]
    while len(ts)<n:
        t=rng.uniform(-.5,.5,7*n)
        ts.extend(t[rng.random(7*n)<(1-2*abs(t))**(d-1)].tolist())
    t=np.array(ts[:n]);dirs=rng.normal(size=(n,d-1));dirs/=np.linalg.norm(dirs,axis=1)[:,None]
    x=dirs*((.5-abs(t))*rng.random(n)**(1/(d-1)))[:,None]
    dt=t[None,:]-t[:,None]
    sq=np.sum((x[None,:,:]-x[:,None,:])**2,axis=2)
    return ((dt>0)&(dt*dt>sq+1e-13)).astype(np.int16)

def causal_nonlocality_gate():
    rng=np.random.default_rng(20112026)
    levels={}
    for n in (40,80,160,320):
        values=[];relations=[]
        for _ in range(40):
            R=minkowski_sprinkle(n,4,rng)
            links=R & (~((R@R)>0))
            assert np.count_nonzero(links&(R==0))==0
            values.append(float(links.sum()/n))
            relations.append(float(R.sum()/(n*(n-1)/2)))
        levels[str(n)]={'samples':len(values),'mean_links_per_event':float(np.mean(values)),
                        'standard_error':float(np.std(values,ddof=1)/np.sqrt(len(values))),
                        'pair_comparability':float(np.mean(relations))}
    seq=[levels[str(n)]['mean_links_per_event'] for n in (40,80,160,320)]
    assert seq==sorted(seq) and seq[-1]>2*seq[0]
    assert all(abs(levels[str(n)]['pair_comparability']-.1)<.025 for n in (40,80,160,320))
    return {'dimension':'3+1 flat Minkowski Alexandrov diamond',
      'link_relation_counts':levels,'finite_sample_link_count_increases':True,
      'implication':'In finite-diamond Poisson-like sprinklings link-degree does not remain bounded under finer sampling; naive fixed-neighbor local dynamics is not automatically Lorentz-invariant.',
      'limitation':'40 samples per n in a fixed finite diamond; no derivation of large-density asymptotic, Einstein equations or quantum causal-set action.'}


def main(write=True):
    data={'status':'PASS_SIX_BOUNDED_TOE_FRONTS','baseline':'9c9d65d0941d373360ed197a1629fd77131d26e5',
      'e8_cubic_multiplet':e8_cubic_gate(),
      'w33_known_error_subcodes':hodge_subcode_gate(),
      'native_qutrit_model_free_memory':qutrit_model_free_gate(),
      'SU3_polynomial_drift':su3_richardson_gate(),
      'E6_trinification_anomalies':e6_chirality_gate(),
      '4D_causal_link_nonlocality':causal_nonlocality_gate()}
    if write:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':data['status'],
        'qutrit_witness_up':data['native_qutrit_model_free_memory']['prospective_seeded_certificate']['witness_upper'],
        'w33_one_known_bad_edge_subcode_dim':data['w33_known_error_subcodes']['known_one_bad_edge_noiseless_subcode_dim'],
        'SU3_36_scan_error':data['SU3_polynomial_drift']['Richardson_36_trace_error_through_cubic'],
        '4D_causal_link_counts':{k:round(v['mean_links_per_event'],3) for k,v in data['4D_causal_link_nonlocality']['link_relation_counts'].items()}}))
    return data

if __name__=='__main__':main()
