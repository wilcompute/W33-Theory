"""TOE91: Witting ququart finite-key limits, adversarial biased acceptance,
40-analyzer calibration and physical-error-event to W33 carrier interface.

These are exact geometry + explicit numerical models, NOT composable QKD,
detector-independent certification, or a 135-qutrit CSS homomorphism.
"""
from __future__ import annotations
import json, math
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import numpy as np
from scipy.stats import binom
from scipy.optimize import brentq
from tools.bt1408_witting_contextual_communication_bridge import construct_witting_40_rays,find_tetrads
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT

def binary_entropy(p):
    return -p*math.log2(p) if p>0 else 0

def coherent_information(v):
    f=(1+15*v)/16
    other=(1-f)/15
    ent=binary_entropy(f)+15*binary_entropy(other)
    return 2-ent

def finite_key_status():
    root=brentq(coherent_information,.2,1)
    cases=[]
    for v in (0,.2,.25,.5,.7,.8,1):
        f=(1+15*v)/16
        r=coherent_information(v)
        cases.append({'visibility':v,'matching_probability':(1+3*v)/4,
                      'Phi_fidelity':f,
                      'asymptotic_one_way_hashing_rate_bits_per_pair':round(r,12),
                      'positive_hashing_lower_bound':r>1e-12})
    # Hoeffding concentration for uniform independent 40-setting rounds.
    confidence=1e-3;n=8192
    radius=math.sqrt(math.log(1/confidence)/(2*n))
    assert cases[2]['asymptotic_one_way_hashing_rate_bits_per_pair']<0
    assert cases[2]['matching_probability']-radius>.4
    return {
      'isotropic_spectrum':'lambda_Phi=(1+15v)/16; 15 other eigenvalues=(1-v)/16',
      'one_way_hashing_rate':'R_hash= max(0, 2 - S(rho_v)) bits per two-ququart copy under trusted isotropic-state and asymptotic one-way hashing assumptions',
      'positive_hashing_threshold_visibility':round(float(root),12),
      'finite_key_warning':'No composable finite-key entropy bound follows solely from the Witting matching witness; parameter estimation and smooth min-entropy vs coherent attacks remain unproved.',
      'confidence_parameter':confidence,'iid_pairs':n,
      'one_sided_Hoeffding_matching_deviation':round(radius,12),
      'cases':cases}

def analyzer_calibration(rays,bases):
    P=[np.outer(r,r.conj()) for r in rays]
    I=np.eye(4,dtype=complex)
    ideal=sum(np.kron(P[i],P[i].conj()) for b in bases for i in b)/40
    # deterministic setting-dependent unitary crosstalk on Alice and Bob,
    # not a real photonic device.
    theta=.01
    def rotor(i,sign=1):
        a=(i//4)%4;b=(a+1)%4; ang=sign*theta*(1+i%3)/3
        M=np.eye(4,dtype=complex)
        M[a,a]=math.cos(ang);M[b,b]=math.cos(ang)
        M[a,b]=-math.sin(ang);M[b,a]=math.sin(ang)
        return M
    pert=np.zeros((16,16),complex)
    residuals=[]
    for bidx,B in enumerate(bases):
        # Alice / Bob setting-wide unitaries, independently calibrated
        Ua=rotor(bidx,1);Ub=rotor(bidx+19,-1)
        residuals.append(float(np.max(abs(Ua.conj().T@Ua-I))))
        for i in B:
            qa=Ua@P[i]@Ua.conj().T
            qb=Ub@P[i].conj()@Ub.conj().T
            pert+=np.kron(qa,qb)/40
    assert max(residuals)<1e-12
    diff=pert-ideal
    spectral=float(np.max(abs(np.linalg.eigvalsh(diff))))
    # For any separable state, ideal <C> <=.4; error shift bounded
    # by ||Cpert - C||_op. Also a conservative setting-efficiency ratio.
    assert spectral>1e-5
    efficiency_min=.94;efficiency_max=.98
    conservative_calibrated_ceiling=(.4+spectral)*efficiency_max/efficiency_min
    return {'settings':40,'two_party_measurement_outcomes_per_setting':16,
      'single_party_ray_detector_slots_per_setting':4,
      'ideal_separable_ceiling':.4,
      'simulated_max_rail_rotation_radians':theta,
      'max_basis_unitarity_residual':round(max(residuals),12),
      'perturbed_vs_ideal_joint_match_operator_spectral_error':round(spectral,12),
      'postcalibration_separable_ceiling_no_loss':round(.4+spectral,12),
      'setting_efficiency_min':efficiency_min,
      'setting_efficiency_max':efficiency_max,
      'conservative_separable_ceiling_with_setting_efficiency_band':round(conservative_calibrated_ceiling,12),
      'bound_proof':'For uniform basis sampling and trusted projector calibration, |Tr rho(Cpert-C)|<=||Cpert-C||_op. If basis efficiency lies in [eta_min,eta_max] independent of the outcome, the postselected average is <=eta_max/eta_min times the calibrated uniform upper bound.',
      'scope':'Declared synthetic 4-mode perturbations and efficiency band only; not measured error or physical engineering loss budgets.'}

def product_basis_loophole(rays,bases):
    base=0
    ray=rays[base];P=np.outer(ray,ray.conj())
    probs=[]
    for B in bases:
        p=sum(abs(np.vdot(ray,rays[k]))**4 for k in B)
        probs.append(float(p))
    assert abs(sum(probs)/40-.4)<1e-10
    special=[b for b,B in enumerate(bases) if base in B]
    assert len(special)==4 and all(abs(probs[b]-1)<1e-10 for b in special)
    examples=[]
    for epsilon in (1,0.1,0):
        weights=[1. if b in special else epsilon for b in range(40)]
        rate=sum(weights)/40
        p=sum(p*w for p,w in zip(probs,weights))/sum(weights)
        examples.append({'acceptance_elsewhere':epsilon,'accepted_fraction':round(rate,12),
                         'conditioned_product_state_matching':round(p,12)})
    assert examples[-1]['conditioned_product_state_matching']==1
    return {'source':'Separable state rho = |ray0><ray0|_A tensor |conj(ray0)><conj(ray0)|_B; four of forty Witting bases contain ray0.',
      'uniform_40_basis_matching':.4,
      'four_matching_bases':special,
      'basis_dependent_postselection':examples,
      'loophole':'If a detector or public basis announcement allows setting-dependent acceptance and calibration does not constrain it, a separable product state achieves 100% matches on 10% accepted bases. This invalidates an unqualified 40% postselected test.'}

def rank_mod3(cols,nrows):
    pivot={}
    for col in cols:
        v={i:int(x%3) for i,x in enumerate(col) if x%3}
        while v:
            k=min(v)
            if k in pivot:
                a=pivot[k];factor=v[k]
                for j,x in a.items():
                    z=(v.get(j,0)-factor*x)%3
                    if z:v[j]=z
                    else:v.pop(j,None)
            else:
                f=pow(v[k],-1,3)
                pivot[k]={j:(x*f)%3 for j,x in v.items()}
                break
    return len(pivot)

def carrier_interface(rays,bases):
    adjacency={i:set() for i in range(40)}
    oriented={}
    undirected={}
    for bid,B in enumerate(bases):
        for i in B:
            for j in B:
                if i==j:continue
                assert (i,j) not in oriented
                oriented[(i,j)]={'basis':bid,'from_slot':B.index(i),'to_slot':B.index(j)}
                adjacency[i].add(j)
        for i,j in combinations(B,2):
            k=tuple(sorted((i,j)))
            assert k not in undirected
            undirected[k]=bid
    assert len(oriented)==480 and len(undirected)==240
    assert all(len(adjacency[i])==12 for i in adjacency)
    turns=Counter()
    for u,v in oriented:
        allowed=adjacency[v]-{u}
        triangle=sum(k in adjacency[u] for k in allowed)
        open_=len(allowed)-triangle
        turns[(triangle,open_)]+=1
    assert turns=={(2,9):480}
    cols=[]
    for u,v in undirected:
        x=[0]*40;x[u]=2;x[v]=1;cols.append(x)
    incidence_rank=rank_mod3(cols,40)
    assert incidence_rank==39
    # 240 W33 edges, 40 vertices, so 201 ternary graph cycles.
    return {'directed_outcome_substitution_events':480,
        'unoriented_W33_orthogonality_edges':240,
        'mapping':'Each (basis, source slot, wrong destination slot) maps bijectively to one oriented 40-ray W33 graph edge. Every orthogonal ray pair belongs to one tetrad.',
        'turn_counts_for_every_oriented_edge':{'triangle_turns':2,'open_turns':9,'total_nonbacktracking':11},
        'F3_vertex_boundary_matrix_shape':[40,240],
        'F3_incidence_rank':incidence_rank,
        'F3_cycle_kernel_dimension':240-incidence_rank,
        'physical_interface_limit':'A detector slot substitution is a classical event edge in W33, not a physical two-qutrit Pauli operator. The selected H27-CSS code has a distinct 27-vertex/135-edge Schlaefli chain complex; no equivariant chain map, qutrit encoder, or fault-tolerant recovery is established.'}

def certificate():
 R=np.asarray(construct_witting_40_rays(),dtype=complex)
 B=[tuple(b) for b in find_tetrads(list(R))]
 return {'source':'TOE90 Vlasov/Witting 40 rays and 40 contexts, plus prior W33 carrier','finite_key':finite_key_status(),
         'analyzer_calibration':analyzer_calibration(R,B),
         'product_state_postselection_attack':product_basis_loophole(R,B),
         'detector_to_W33_carrier':carrier_interface(R,B)}
if __name__=='__main__':
 d=certificate()
 p=ROOT/'data/w33_20261015_toe91_finitekey_analyzer_carrier.json'
 p.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n',encoding='utf8')
 print('TOE91 QKD',d['finite_key']['positive_hashing_threshold_visibility'])
 print('ANALYZER',d['analyzer_calibration']['conservative_separable_ceiling_with_setting_efficiency_band'])
 print('ATTACK',d['product_state_postselection_attack']['basis_dependent_postselection'])
 print('CARRIER',d['detector_to_W33_carrier']['F3_cycle_kernel_dimension'])
