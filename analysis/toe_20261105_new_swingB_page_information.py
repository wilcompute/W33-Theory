#!/usr/bin/env python3
"""Unrelated swing B: Page curve under unitary evaporation versus pair-only.

Haar-random pure 8-qubit black-hole state; transfer qubits to radiation
without losing any purifier, compute von Neumann entropy and Page's
exact finite-Hilbert-space ensemble expectation. Contrast Hawking
pair-only model whose hidden partners never leave horizon: radiation
entropy rises monotonically and cannot return to zero. This is a
unitarity/quantum-information consistency control, NOT black-hole
gravity, island formula, or a new Page-curve derivation.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.special import digamma
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_new_swingB_page_information_transfer.json"
def page_exact(nrad,nBH):
    mr=min(nrad,nBH);nr=max(nrad,nBH)
    return float((digamma(mr*nr+1)-digamma(nr+1)-(mr-1)/(2*nr))/math.log(2))
def entropy_state(v,dr,db):
    s=np.linalg.svd(v.reshape(dr,db),compute_uv=False)
    eig=s*s
    eig=eig[eig>1e-18]
    return float(-np.dot(eig,np.log2(eig)))
def main():
    nqubits=8
    rng=np.random.default_rng(7202605)
    ntrials=100
    rows=[]
    for n in range(nqubits+1):
        dr=1<<n;db=1<<(nqubits-n)
        scores=[]
        for k in range(ntrials):
            v=rng.normal(size=1<<nqubits)+1j*rng.normal(size=1<<nqubits)
            v/=np.linalg.norm(v)
            scores.append(entropy_state(v,dr,db))
        mean=float(np.mean(scores));se=float(np.std(scores,ddof=1)/math.sqrt(ntrials))
        exact=page_exact(dr,db)
        assert abs(mean-exact)<max(.11,5*se)
        paironly=float(n)
        rows.append({"emitted_qubits":n,"remaining_bh_qubits":nqubits-n,
          "Page_exact_Haar_mean_entropy_bits":exact,
          "observed_random_state_mean_entropy_bits":mean,
          "sampling_standard_error_bits":se,
          "hidden_partner_never_released_entropy_bits":paironly,
          "Haar_single_sample_entropy_95pct":np.quantile(scores,[.025,.975]).tolist()})
    assert abs(rows[0]["Page_exact_Haar_mean_entropy_bits"])<1e-15
    assert abs(rows[-1]["Page_exact_Haar_mean_entropy_bits"])<1e-15
    assert rows[4]["Page_exact_Haar_mean_entropy_bits"]>3
    assert rows[4]["Page_exact_Haar_mean_entropy_bits"]>rows[3]["Page_exact_Haar_mean_entropy_bits"]
    assert rows[5]["Page_exact_Haar_mean_entropy_bits"]<rows[4]["Page_exact_Haar_mean_entropy_bits"]
    assert rows[-1]["hidden_partner_never_released_entropy_bits"]==8
    assert abs(rows[-1]["observed_random_state_mean_entropy_bits"])<1e-12
    output={"status":"PASS_PAGE_CURVE_INFORMATION_TRANSFER_VERSUS_PAIR_ONLY",
      "reference_total_qubits":nqubits,
      "sampled_independent_Haar_pure_states_per_step":ntrials,
      "Page_formula":"[digamma(dR*dBH+1)-digamma(max(dR,dBH)+1)-(min(dR,dBH)-1)/(2max(dR,dBH))]/ln2",
      "rows":rows,
      "two_processes":"(a) Pure globally scrambled finite 8-qubit state with qubits reclassified as emitted radiation, (b) every emitted Hawking qubit entangled with a NEW permanently retained inaccessible partner; no transfer/purification.",
      "information_gate":"With fixed finite pure total dimension and full release, radiation entropy returns to zero at complete evaporation; independent permanently hidden Hawking partners prevent return. Full unitary retrieval or remnant/partner return is required.",
      "limitations":"Uniform Haar randomness and qubit relabeling approximate fast scrambling, not a local gravitational evaporation unitary; hidden-partner construction includes a growing inaccessible Hilbert space; no horizon, energy conservation, quantum gravity or replica-wormhole computation.",
      "prior_art":["Don Page Phys Rev Lett 71 1291 (1993) finite-dimensional average entanglement formula","QURI quantum computing Page curve tutorial","2026 nonperturbative finite N island formula literature"]}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(output,indent=2,sort_keys=True)+"\n")
    print("PAGE_PASS peak",rows[4]["Page_exact_Haar_mean_entropy_bits"],
       "final_haar",rows[-1]["observed_random_state_mean_entropy_bits"],
       "final_pair_only",rows[-1]["hidden_partner_never_released_entropy_bits"],flush=True)
    return output
if __name__=="__main__":main()
