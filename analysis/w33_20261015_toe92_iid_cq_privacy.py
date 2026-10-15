"""TOE92 Witting finite-block privacy amplification against an EXACT IID purifying Eve.

Calculate quantum collision entropy of Alice's classical 4-outcome
measurement with Eve holding a purification of an assumed isotropic
two-ququart state. Quantum 2-universal hashing leftover bound, *without*
error-correction disclosure or finite-key state estimation, gives an
actual one-sided secrecy-only key-length upper target under the exact
trusted IID model. It is NOT a composable correct QKD key protocol.
"""
from __future__ import annotations
import json, math, numpy as np
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
from analysis.w33_20261015_toe91_finitekey_analyzer_carrier import coherent_information
N=8192
EPSILON=1e-8
def collision_entropy(v):
    phi=np.zeros(16,complex)
    for i in range(4):phi[5*i]=.5
    rho=(1-v)*np.eye(16)/16+v*np.outer(phi,phi.conj())
    vals, vecs=np.linalg.eigh(rho)
    vals=np.where(vals<1e-12,0.,np.clip(vals,0,1))
    assert abs(sum(vals)-1)<1e-12
    half=np.diag(vals**.25)
    gamma=0.
    probs=[]
    for x in range(4):
        projector=np.zeros((16,16),complex)
        for b in range(4):projector[4*x+b,4*x+b]=1
        mx=vecs.conj().T@projector@vecs
        wx=half@mx@half
        gamma+=float(np.real(np.trace(wx@wx)))
        probs.append(float(np.real(np.trace(rho@projector))))
    assert max(abs(p-.25) for p in probs)<1e-12
    if v==0:assert abs(gamma-1)<1e-12
    if v==1:assert abs(gamma-.25)<1e-12
    return -math.log2(gamma),gamma
def h4(e):
    if e==0:return 0.
    return -(1-e)*math.log2(1-e)-e*math.log2(e/3)
def certificate():
    rows=[]
    for v in (0,.2,.25,.5,.7,.8,.9,.95,1):
        h2,gamma=collision_entropy(v)
        Lprivacy=math.floor(N*h2-2*math.log2(1/(2*EPSILON)))
        Q=3*(1-v)/4
        reconciliation_shannon=N*h4(Q)
        margin=Lprivacy-reconciliation_shannon
        rows.append({'visibility':v,'Eve_conditional_collision_entropy_bits':round(h2,12),
        'collision_probability':round(gamma,12),
        'quantum_leftover_hash_secrecy_only_bits':max(0,Lprivacy),
        'asymptotic_Slepian_Wolf_leakage_lower_limit_bits':round(reconciliation_shannon,6),
        'optimistic_privacy_minus_asymptotic_leak_margin_bits':round(margin,5),
        'unclipped_coherent_information':round(coherent_information(v),12)})
    assert rows[0]['quantum_leftover_hash_secrecy_only_bits']==0
    assert rows[-1]['Eve_conditional_collision_entropy_bits']==2
    assert rows[-1]['quantum_leftover_hash_secrecy_only_bits']>16000
    return {'model':'Trusted exactly specified iid isotropic rho_AB; Eve holds a purification; Alice measures computational basis on each copy. Public basis setting assumed independent.',
      'N':N,'target_quantum_secrecy_trace_distance_bound':EPSILON,
      'renyi2_formula':'Gamma = sum_x Tr[(rho_E^(-1/4) rho_E^x rho_E^(-1/4))^2] ; H2(X|E)=-log2 Gamma. Here rho_E^x are unnormalized, one for each 4-outcome Alice result.',
      'privacy_amplification_guarantee':'For 2-universal hashing with public random seed, trace-distance secrecy <= 0.5*sqrt(2^(ell-N*H2)), in the exact iid cq model with no reconciliation transcript.',
      'secrecy_only_bit_rule':'ell = max(0, floor(N H2 - 2 log2(1/(2 epsilon))))',
      'correction_boundary':'The actual public error-correction transcript changes Eve side information; the PA-only output bits are NOT a shared/correct key. Reported Slepian-Wolf leakage is an asymptotic information lower bound, NOT an achieved finite block code or secure-chain-rule correction.',
      'mathematics_reference':'Tomamichel, Schaffner, Smith and Renner, Leftover Hashing Against Quantum Side Information, IEEE Transactions on Information Theory 57 (2011), arXiv:1002.2436.',
      'rows':rows}
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261015_toe92_iid_cq_privacy.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
 for row in d['rows']:print('HASH',row['visibility'],row['Eve_conditional_collision_entropy_bits'],row['quantum_leftover_hash_secrecy_only_bits'],row['optimistic_privacy_minus_asymptotic_leak_margin_bits'])
