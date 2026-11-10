#!/usr/bin/env python3
"""25-or-fewer probe phase-model calibration; disconnected Bell support gauge.

Kactual=K0@diag(exp(i theta_j)), known K0, unknown per-input mode phases.
Two inputs are phase-observable only if their amplitudes overlap at an
output detector. Use a max-interference spanning forest per K0; root
phases in disconnected components are unobservable but cancel in EVERY
effect K†|r><r|K. Naive fixed-mode-reference tomography fails here.
"""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from w33_20261109_full_povm_calibration_bound import make_model

def forest(K):
    weights=[]
    for j in range(9):
        for k in range(j+1,9):
            w=float(max(abs(K[:,j].conj()*K[:,k])))
            if w>1e-10:weights.append((w,j,k))
    parent=list(range(9))
    def find(j):
        while parent[j]!=j:j=parent[j];j=parent[j]
        return j
    graph=[[] for _ in range(9)]
    for w,j,k in sorted(weights,reverse=True):
        a,b=find(j),find(k)
        if a!=b:
            parent[b]=a
            graph[j].append(k);graph[k].append(j)
    roots=[];tree=[];seen=set()
    for r in range(9):
        if r in seen:continue
        roots.append(r);seen.add(r)
        stack=[r]
        while stack:
            u=stack.pop(0)
            for v in sorted(graph[u]):
                if v not in seen:
                    seen.add(v);tree.append((u,v));stack.append(v)
    assert len(tree)==9-len(roots)
    return roots,tree

def probes(tree):
    basis=np.eye(9,dtype=complex)
    return np.stack([*basis,
      *[(basis[j]+basis[k])/np.sqrt(2) for j,k in tree],
      *[(basis[j]+1j*basis[k])/np.sqrt(2) for j,k in tree]])

def probabilities(K,states):
    p=np.abs(states@K.T)**2
    missing=1-np.sum(p,axis=1)
    assert np.min(missing)>-1e-10
    return np.column_stack([p,np.maximum(missing,0)])
def effects(K):return np.einsum("ji,jk->jik",K.conj(),K)

def fit_phase(q,K,roots,tree,eps=0):
    theta=np.zeros(9)
    dist=np.zeros(9)
    minamp=np.inf
    for i,(u,v) in enumerate(tree):
        e=K[:,u].conj()*K[:,v]
        row=int(np.argmax(abs(e)))
        amp=float(abs(e[row]))
        assert amp>1e-10
        minamp=min(minamp,amp)
        mid=(q[u,row]+q[v,row])/2
        z=(q[9+i,row]-mid)+1j*(mid-q[9+len(tree)+i,row])
        dphi=float(np.angle(z/e[row]))
        theta[v]=theta[u]+dphi
        noise=2*np.sqrt(2)*eps
        chord=min(2.,2*noise/(amp-noise)) if amp>noise else 2.
        dist[v]=min(2.,dist[u]+chord)
    # A component's phase root is not measurable or needed: within the
    # disconnected support blocks all K†|j><j|K matrix effects are invariant.
    return K@np.diag(np.exp(1j*theta)),float(minamp),float(max(dist))

def heldout_states(tree):
    basis=np.eye(9,dtype=complex)
    used={tuple(sorted(x)) for x in tree}
    pairs=[(j,k) for j in range(9) for k in range(j+1,9)
           if (j,k) not in used]
    return np.stack([(basis[j]+basis[k])/np.sqrt(2) for j,k in pairs]),pairs

def main(path=None):
    Kbase,_,_,_=make_model()
    trees=[forest(K) for K in Kbase]
    S=[probes(tr) for roots,tr in trees]
    rng=np.random.default_rng(202611091975)
    phases=rng.uniform(-.13,.13,size=(10,9))
    phases[:,0]=0
    actual=[K@np.diag(np.exp(1j*t)) for K,t in zip(Kbase,phases)]
    q=[probabilities(K,T) for K,T in zip(actual,S)]
    fit=[fit_phase(P,K,*tr)[0] for P,K,tr in zip(q,Kbase,trees)]
    exact=max(float(np.linalg.norm((effects(a)-effects(b)),axis=(-2,-1),ord=2).max())
              for a,b in zip(fit,actual))
    assert exact<4e-13,exact
    report={}
    for N in (10**4,10**6,10**8,10**10):
        sim=[np.array([rng.multinomial(N,p)/N for p in context])
             for context in q]
        eps=math.sqrt(math.log(2*10*25*10/.05)/(2*N))
        fits=[fit_phase(P,K,*tr,eps) for P,K,tr in zip(sim,Kbase,trees)]
        normerr=max(float(np.linalg.norm(effects(f[0])-effects(a),
                                            axis=(-2,-1),ord=2).max())
                    for f,a in zip(fits,actual))
        bound=min(2.,2*max(f[2] for f in fits))
        assert normerr<=bound+1e-10,(normerr,bound)
        report[str(N)]={"launched_trials_per_probe_context":N,
              "total_trusted_calibration_pulses":N*sum(len(T) for T in S),
              "observed_max_effect_operator_error":normerr,
              "simultaneous_95pct_effect_error_bound_conditioned_on_model":bound,
              "max_frequency_Hoeffding_radius":eps,
              "smallest_selected_edge_interference_amplitude":float(min(f[1] for f in fits))}
    hold,pairs=heldout_states(trees[8][1])
    X=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
    H=(X+X.conj().T)/2;H/=np.linalg.norm(H,2)
    mixing=.09
    Kbad=Kbase[8]@expm(1j*mixing*H)@np.diag(np.exp(1j*phases[8]))
    qbad=probabilities(Kbad,S[8])
    fitbad=fit_phase(qbad,Kbase[8],*trees[8])[0]
    residual=float(np.max(abs(probabilities(Kbad,hold)-probabilities(fitbad,hold))))
    Nhold=100000
    epshold=math.sqrt(math.log(2*len(hold)*10/.05)/(2*Nhold))
    if residual<=2*epshold:
        Nhold=10000000
        epshold=math.sqrt(math.log(2*len(hold)*10/.05)/(2*Nhold))
    assert residual>2*epshold,(residual,epshold)
    # Valid sampled misspecification test: number-state probe click
    # probabilities are invariant under diagonal input phases.
    Nbasis=100000
    basis_expected=probabilities(Kbase[8],np.eye(9,dtype=complex))
    bad_probs=probabilities(Kbad,np.eye(9,dtype=complex))
    basis_counts=np.array([rng.multinomial(Nbasis,row)/Nbasis for row in bad_probs])
    epsbasis=math.sqrt(math.log(2*9*10/.05)/(2*Nbasis))
    basis_deviation=float(np.max(abs(basis_counts-basis_expected)))
    assert basis_deviation>epsbasis,(basis_deviation,epsbasis)
    prior={str(N):float(math.sqrt(585)*math.sqrt(math.log(2*10*81*10/.05)/(2*N)))
           for N in (10**4,10**6,10**8,10**10)}
    out={"status":"PASS_STRUCTURED_PHASE_FOREST_CALIBRATION_WITH_MODEL_FALSIFIER",
         "known_transfer_assumption":"Kactual=Kcal@diag(e^{i theta_j}); exact Kcal including loss known, only unknown input phases. Per-component common phases are gauge and cannot be estimated.",
         "number_of_settings":10,"modes_per_setting":9,
         "calibration_probe_count_per_setting":[len(T) for T in S],
         "support_graph_connected_components_per_setting":[len(root) for root,tr in trees],
         "forest_edges_per_setting":[len(tr) for root,tr in trees],
         "total_calibration_probes_per_full_cycle":sum(len(T) for T in S),
         "exact_expected_full_POVM_effect_reconstruction_error":exact,
         "finite_trials":report,
         "model_free_81probe_effect_radius_comparator":prior,
         "heldout_model_falsifier":{
            "unknown_coherent_crosstalk_rotation_opnorm_parameter":mixing,
            "heldout_superposition_probe_count":len(hold),
            "exact_max_heldout_outcome_probability_residual":residual,
            "two_simultaneous_95pct_Hoeffding_radii":2*epshold,
            "heldout_trial_count_per_probe":Nhold,
            "unmodeled_crosstalk_expected_frequency_heldout_screen":True,
            "heldout_note":"Heldout discrepancy uses exact expected frequencies, not a sampled 95% fitted-model test",
            "basis_only_independent_sample_count_per_input":Nbasis,
            "basis_only_sampled_95pct_falsifier_threshold":epsbasis,
            "basis_only_sampled_max_probability_deviation":basis_deviation,
            "basis_only_model_rejected_at_95pct_simultaneous_confidence":True},
         "scope":"Rigorous finite-shot phase estimate only when model true, Kcal itself known, all trials count click/no-click and trusted probes. Under unmodeled crosstalk or drift the bounds are invalid; heldout falsifier can detect some (not all) such failures. Does not establish device independent or experimentally affordable PPT entanglement certification.",
         "priority":"Standard phase interferometric calibration; novel only in repo-specific application of observable spanning forest to the W33 Bell optical construction."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("FOREST_PHASE_CAL",json.dumps({"components":out["support_graph_connected_components_per_setting"],
      "counts":out["calibration_probe_count_per_setting"],
      "N1e8":report[str(10**8)],
      "heldout":out["heldout_model_falsifier"]}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
