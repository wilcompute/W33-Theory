#!/usr/bin/env python3
"""Consistency/no-go test for Ledger Appendix H.4.

For fixed V x R and H=HV x I + I x HR, local evolution preserves Schmidt
spectrum/entropy and Tr_R exp(-beta H)=Z_R exp(-beta HV).  Hence a product
Hamiltonian cannot both power a changing dark bond and induce a new visible
operator.  A genuine interaction is included as the minimal ordinary escape.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
I2=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Z=np.array([[1,0],[0,-1]],complex)
def expH(H,s):
    w,v=np.linalg.eigh(H);return (v*np.exp(s*w))@v.conj().T
def ptr(rho):return np.einsum("arbr->ab",rho.reshape(2,2,2,2))
def entropy(rho):
    w=np.clip(np.linalg.eigvalsh((rho+rho.conj().T)/2).real,1e-15,1.0);return float(-np.sum(w*np.log(w)))
def logpos(A):
    w,v=np.linalg.eigh((A+A.conj().T)/2);return (v*np.log(w))@v.conj().T
def main():
    HV=.7*Z+.2*X;HR=-.4*Z+.3*X;H0=np.kron(HV,I2)+np.kron(I2,HR)
    a=.37;psi=np.array([np.cos(a),0,0,np.sin(a)],complex);rho=np.outer(psi,psi.conj())
    rows=[];spec=[];ents=[]
    for t in [0.,.2,.7,1.3]:
        U=expH(H0,-1j*t);rv=ptr(U@rho@U.conj().T);e=np.sort(np.linalg.eigvalsh(rv).real)
        spec.append(e);ents.append(entropy(rv));rows.append({"t":t,"rhoV_eigenvalues":e.tolist(),"entropy":ents[-1]})
    ds=max(float(np.max(np.abs(s-spec[0]))) for s in spec);de=max(abs(s-ents[0]) for s in ents)
    beta=.9;lhs=ptr(expH(H0,-beta));EV=expH(HV,-beta);ER=expH(HR,-beta);ZR=np.trace(ER)
    ef=float(np.max(np.abs(lhs-ZR*EV)));el=float(np.max(np.abs(logpos(lhs)-(np.log(ZR.real)*I2-beta*HV))))
    plus=np.array([1,1],complex)/np.sqrt(2);rp=np.outer(np.kron(plus,plus),np.kron(plus,plus).conj());Hint=np.kron(Z,Z)
    grow=[]
    for t in [0.,.2,.4,.7]:
        U=expH(Hint,-1j*t);grow.append({"t":t,"entropy":entropy(ptr(U@rp@U.conj().T))})
    h,g=.6,.35;HI=np.kron(I2,h*Z)+g*np.kron(Z,Z);Gamma=-logpos(ptr(expH(HI,-beta)))
    gi=float(np.trace(Gamma).real/2);gz=float(np.trace(Gamma@Z).real/2)
    checks={"product_hamiltonian_schmidt_spectrum_invariant":ds<1e-13,"product_hamiltonian_entropy_invariant":de<1e-13,
      "gibbs_partial_trace_factorizes":ef<1e-12,"effective_action_is_HV_plus_scalar":el<1e-12,
      "interaction_can_change_entanglement":grow[-1]["entropy"]>.6,"interaction_can_induce_nonscalar_visible_operator":abs(gz)>.1}
    checks={k:bool(v) for k,v in checks.items()};assert all(checks.values()),checks
    out={"schema":"w33.ledger.dark-bond-no-go.v1","status":"NO_GO_H4_PRODUCT_HAMILTONIAN_AS_WRITTEN",
      "theorem":{"fixed_factorization":"H=HV⊗I+I⊗HR => U=UV⊗UR","reduced_state":"rhoV(t)=UV rhoV(0) UV†, so its spectrum and entropy are constant",
        "thermal_trace":"Tr_R exp(-beta H)=Z_R exp(-beta HV)","effective_action":"-log Tr_R exp(-beta H)=beta HV-log Z_R; no new visible operator is induced"},
      "numerical_certificate":{"local_evolution":rows,"max_spectrum_drift":ds,"max_entropy_drift":de,"gibbs_factorization_error":ef,"effective_action_identity_error":el},
      "minimal_escape_witness":{"interaction":"g Z_V⊗Z_R","entanglement_growth":grow,"biased_R_effective_action_coefficients":{"I":gi,"Z":gz},
        "reading":"A nontrivial V-R interaction can do both jobs the product Hamiltonian cannot, but abandons H.4 step 2 and reopens loop/naturalness analysis."},
      "trilemma":["fixed V⊗R factorization with no interaction","time-varying dark-bond/Schmidt spectrum","new visible operator induced by tracing out R",
        "Under the product Hamiltonian both latter claims fail."],
      "possible_noninteraction_escape":"A time-dependent algebra/factorization, gauge constraint, or code-subspace embedding could evade the fixed-factorization proof, but requires a new theorem and is not H.4 as written.","checks":checks}
    p=Path("data/PART_LEDGER_DARK_BOND_NO_GO.json");p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=="__main__":main()
