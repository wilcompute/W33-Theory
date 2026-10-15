"""TOE90: exact Witting/W33 ququart 2-design and entanglement witness.

Independent operational analysis of A. Yu. Vlasov, 'Scheme of quantum
communications based on Witting polytope', arXiv:2503.18431 (2025).
Reuses earlier repo's authoritative Witting ray/tetrad generator (BT1408).
All quantitative claims are exact integers/rationals or verified matrices.
No device-independent security or composable QKD theorem is claimed.
"""
from __future__ import annotations
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import numpy as np
from tools.bt1408_witting_contextual_communication_bridge import (
    construct_witting_40_rays, find_tetrads
)

ROOT=Path(__file__).resolve().parents[1]

def calculate():
    rays=np.asarray(construct_witting_40_rays(),dtype=complex)
    bases=[tuple(b) for b in find_tetrads(list(rays))]
    assert rays.shape==(40,4) and len(bases)==40
    overlap=np.abs(rays.conj()@rays.T)**2
    assert np.max(abs(overlap-np.eye(40)),initial=0)<=1  # bounded overlaps
    assert np.max(abs(np.diag(overlap)-1))<1e-12
    histogram=Counter()
    adj=np.zeros((40,40),dtype=np.int8)
    for i in range(40):
        for j in range(i+1,40):
            x=float(overlap[i,j])
            if abs(x)<1e-11:
                histogram["orthogonal"]+=1;adj[i,j]=1;adj[j,i]=1
            else:
                assert abs(x-1/3)<1e-11
                histogram["nonorthogonal"]+=1
    assert histogram=={"orthogonal":240,"nonorthogonal":540}
    degree=adj.sum(axis=1)
    assert all(x==12 for x in degree)
    common=adj.astype(int)@adj.astype(int)
    assert all(int(common[i,j])==(2 if adj[i,j] else 4)
               for i in range(40) for j in range(i+1,40))
    assert len({b for b in bases})==40
    for b in bases:
        assert np.max(abs(rays[list(b)]@rays[list(b)].conj().T-np.eye(4)))<1e-12
    assert all(sum(i in b for b in bases)==4 for i in range(40))
    # Frame potential k=2: Witting 40 rays are a complex projective 2-design
    # since the dimension-four Welch bound is attained (not merely a fit).
    fp2=Fraction(40+2*histogram["nonorthogonal"]*Fraction(1,9),40**2)
    welch=Fraction(2,4*5)
    assert fp2==welch==Fraction(1,10)
    projectors=np.array([np.outer(v,v.conj()) for v in rays])
    raw_moment=sum(np.kron(p,p) for p in projectors)/40
    swap=np.zeros((16,16),complex)
    for i in range(4):
        for j in range(4):
            swap[4*i+j,4*j+i]=1
    moment_target=(np.eye(16)+swap)/20
    moment_resid=float(np.max(abs(raw_moment-moment_target)))
    assert moment_resid<1e-12
    phi=np.zeros(16,complex)
    for j in range(4):phi[5*j]=.5
    phi_projector=np.outer(phi,phi.conj())
    # For |Phi4> = sum_j|jj>/2, Bob's conjugate bases are essential:
    # C = (1/40) sum_B sum_{j in B} P_j (Alice) tensor P_j* (Bob)
    #   = (I + 4 |Phi4><Phi4|)/5.
    pairing_operator=sum(
       np.kron(projectors[i],projectors[i].conj())
       for b in bases for i in b)/40
    analytic_operator=(np.eye(16)+4*phi_projector)/5
    operator_resid=float(np.max(abs(pairing_operator-analytic_operator)))
    assert operator_resid<1e-12
    eigenvalues=np.linalg.eigvalsh(pairing_operator)
    assert np.max(abs(eigenvalues-np.array([.2]*15+[1.])))<1e-12
    context_intersection_counts=Counter()
    p_eve_by_intersection={}
    for ref_b in bases:
        for eve_b in bases:
            k=len(set(ref_b)&set(eve_b))
            context_intersection_counts[k]+=1
            cross=overlap[np.ix_(ref_b,eve_b)]
            fidelity=float(np.sum(cross**2)/4)
            target={4:1,1:Fraction(1,2),0:Fraction(1,3)}[k]
            assert abs(fidelity-float(target))<1e-11
            p_eve_by_intersection[str(k)]=str(target)
    assert context_intersection_counts=={4:40,1:480,0:1080}
    random_intercept_resend=Fraction(1+12*Fraction(1,2)+27*Fraction(1,3),40)
    assert random_intercept_resend==Fraction(2,5)
    # Some older repo exact KS-classical estimates are a different task:
    existing=json.loads((ROOT/"data/bt1408_witting_contextual_communication_bridge.json").read_text())
    pair_counts=existing["pair_profile"]["ordered_pair_counts"] if "pair_profile" in existing else None
    # Keep optional baseline assertion if this specific certificate contains it.
    if pair_counts is not None:
        assert pair_counts["compatible_total"]==520
    noise=[]
    for v in [Fraction(0),Fraction(1,10),Fraction(1,5),Fraction(1,4),Fraction(1,2),Fraction(1)]:
        entangled_fidelity=(1+15*v)/16
        predicted_match=(1+4*entangled_fidelity)/5
        assert predicted_match==(1+3*v)/4
        noise.append({"visibility":str(v),"singlet_fraction":str(entangled_fidelity),
                      "matched_probability":str(predicted_match),
                      "certifies_entanglement":bool(predicted_match>Fraction(2,5))})
    return {
        "reference":"A. Yu. Vlasov, Scheme of quantum communications based on Witting polytope, arXiv:2503.18431",
        "repo_prior_art":"tools/bt1408_witting_contextual_communication_bridge.py and BT1409-BT1411 already identify Witting=W33, 13/40 and sparse 40 analyzers. They are NOT TOE90 discoveries.",
        "orthogonality_SRG":{"v":40,"k":12,"lambda":2,"mu":4,
                            "edges":240,"nonorthogonal_pairs":540,"bases":40,"bases_per_ray":4},
        "squared_inner_product_offdiagonal_histogram":{"0":480,"1/3":1080},
        "two_design":{"dimension":4,"rays":40,
                      "frame_potential_2":str(fp2),"Welch_bound":str(welch),
                      "second_moment":"(I_16+SWAP_4x4)/20",
                      "max_matrix_residual_rounded_14dp":round(moment_resid,14)},
        "entanglement_witness":{
            "basis_avg_joint_match_operator":"C=(I_16+4*|Phi4><Phi4|)/5",
            "max_matrix_residual_rounded_14dp":round(operator_resid,14),
            "eigenvalue_multiplicities":{"1":1,"1/5":15},
            "separable_max_Fphi":"1/4",
            "separable_joint_matching_upper_bound":"2/5",
            "maximally_entangled_matching":"1",
            "trust_assumption":"Full characterized four-dimensional measurements with conjugate Bob basis; not device independent",
            "cryptographic_limit":"Entanglement certification is necessary, not sufficient, for composable QKD security."},
        "intercept_resend":{
            "40x40_context_pairs_by_intersection":{str(k):v for k,v in sorted(context_intersection_counts.items())},
            "matched_probability_by_intersection":p_eve_by_intersection,
            "uniform_random_eve_basis_matched_probability":str(random_intercept_resend),
            "uniform_random_eve_basis_error_probability":str(1-random_intercept_resend),
            "security_limit":"Selected attack only; not a worst-case eavesdropper bound."},
        "isotropic_noise":{
            "rho_v":"v|Phi4><Phi4|+(1-v)I_16/16",
            "matching_probability":"(1+3v)/4",
            "strict_detection_visibility_threshold":"1/5",
            "cases":noise},
        "contextuality_note":"The repository's KS one-mark 36/40 satisfiability optimum and contextual fraction 1 are distinct from this 2/5 separability witness.",
        "hardware_note":"Measurement settings correspond to the already compiled 40 BT1411 sparse ququart analyzers; gate loss and SPAM not calibrated."}
if __name__=="__main__":
    d=calculate()
    p=ROOT/"data/w33_20261015_toe90_vlasov_ququart_design.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("TOE90",d["orthogonality_SRG"],d["two_design"],d["entanglement_witness"]["separable_joint_matching_upper_bound"])
