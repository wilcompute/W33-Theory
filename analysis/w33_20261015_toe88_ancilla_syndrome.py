"""TOE88 repeated 99-ancilla qutrit SUM-check extraction and hook witness.

This is a complete gate-by-gate stochastic *Pauli frame model* of the 135
edge qutrits and 99 face ancillas, with a conflict-free two-qudit SUM
schedule. Only 99 Z-type checks are measured, so Z hooks are invisible:
a verified architectural fault-tolerance LIMIT, not a threshold claim.
"""
from __future__ import annotations
import collections, json, random
from analysis.w33_20261015_toe85_h2_relation_module import ROOT, geometry

SHOTS=320
ROUNDS=3
SEED=8826

def schedule(face_rows):
    jobs=[]
    for f,face in enumerate(face_rows):
        for e,s in enumerate(face):
            if s%3:jobs.append((f,e,s%3))
    assert len(jobs)==351
    layers=[]
    for f,e,s in jobs:
        for layer in layers:
            if all(f!=a and e!=b for a,b,w in layer):
                layer.append((f,e,s));break
        else:layers.append([(f,e,s)])
    seen=[(f,e,s) for layer in layers for f,e,s in layer]
    assert len(seen)==len(jobs) and len(set(seen))==len(jobs)
    assert all(len({f for f,e,s in layer})==len(layer) and
               len({e for f,e,s in layer})==len(layer) for layer in layers)
    return layers

def sum_pauli_update(data_x,data_z,anc_x,anc_z,face,edge,w):
    # Under control=data,target=ancilla, SUM^w:
    # X_control -> X_control X_target^w
    # Z_target -> Z_control^(-w) Z_target.
    anc_x[face]=(anc_x[face]+w*data_x[edge])%3
    data_z[edge]=(data_z[edge]-w*anc_z[face])%3

def hook_test(layers):
    # Find consecutive gates on one face. Put a Z fault on its ancilla
    # after the earlier gate, demonstrate Z on later data edge.
    sequence=[(f,e,w) for layer in layers for f,e,w in layer]
    for i,(f,e,w) in enumerate(sequence):
        for j in range(i+1,len(sequence)):
            f2,e2,w2=sequence[j]
            if f==f2:
                x=[0]*135;z=[0]*135;ax=[0]*99;az=[0]*99
                az[f]=1
                sum_pauli_update(x,z,ax,az,f2,e2,w2)
                assert z[e2]==(-w2)%3 and not any(x)
                return {"earlier_gate":list(sequence[i]),
                        "later_gate":list(sequence[j]),
                        "injected_ancilla_Z":1,
                        "resulting_data_Z":z[e2],
                        "unmeasured_by_Z_type_checks":True}
    raise AssertionError("no multiqudit face")

def one_site_lookup(H):
    ans={}
    for j in range(135):
        col=[row[j]%3 for row in H]
        for coeff in (1,2):
            v=tuple((coeff*x)%3 for x in col)
            if v in ans:ans[v]=None
            else:ans[v]=(j,coeff)
    return ans

def extraction(H,layers,rng,rates):
    dx=[0]*135;dz=[0]*135
    records=[]
    counts=collections.Counter()
    for roundnum in range(ROUNDS):
        ax=[0]*99;az=[0]*99
        for layer in layers:
            for f,e,w in layer:
                sum_pauli_update(dx,dz,ax,az,f,e,w)
                if rng.random()<rates["data_X_after_SUM"]:
                    dx[e]=(dx[e]+rng.choice((1,2)))%3
                    counts["data_X_faults"]+=1
                if rng.random()<rates["ancilla_Z_after_SUM"]:
                    az[f]=(az[f]+rng.choice((1,2)))%3
                    counts["ancilla_Z_faults"]+=1
                    if rng.random()<rates["correlated_XZ_given_ancilla_Z"]:
                        dx[e]=(dx[e]+rng.choice((1,2)))%3
                        counts["correlated_faults"]+=1
                if rng.random()<rates["ancilla_X_after_SUM"]:
                    ax[f]=(ax[f]+rng.choice((1,2)))%3
                    counts["ancilla_X_faults"]+=1
        observed=ax[:]
        for f in range(99):
            if rng.random()<rates["readout_digit_fault"]:
                observed[f]=(observed[f]+rng.choice((1,2)))%3
                counts["readout_digit_faults"]+=1
        records.append(observed)
        # ancilla reset; data errors remain in the Pauli frame
    vote=[max(range(3),key=lambda x:sum(rec[f]==x for rec in records))
          for f in range(99)]
    syndrome=[sum(h*x for h,x in zip(row,dx))%3 for row in H]
    assert len(syndrome)==99
    # Very simple decoder, deliberately does not correct multisite or Z.
    lookup=one_site_lookup(H)
    def corrected_zero(record):
        candidate=lookup.get(tuple(record))
        ans=dx[:]
        if candidate:
            j,c=candidate
            ans[j]=(ans[j]-c)%3
        return not any(ans)
    return {
       "true_X_nonzero":bool(any(dx)),
       "true_Z_nonzero":bool(any(dz)),
       "final_true_X_syndrome_nonzero":bool(any(syndrome)),
       "raw_final_readout_mismatch":records[-1]!=syndrome,
       "majority_readout_mismatch":vote!=syndrome,
       "raw_X_physical_residual_zero_after_decoder":corrected_zero(records[-1]),
       "majority_X_physical_residual_zero_after_decoder":corrected_zero(vote),
       "complete_data_Pauli_error_free":not any(dx) and not any(dz),
       **{k+"_count":v for k,v in counts.items()}
    }

def certificate():
    _,rows,_=geometry()
    layers=schedule(rows)
    hook=hook_test(layers)
    rates={
      "data_X_after_SUM":0.00025,
      "ancilla_Z_after_SUM":0.00018,
      "ancilla_X_after_SUM":0.00012,
      "correlated_XZ_given_ancilla_Z":0.12,
      "readout_digit_fault":0.0015
    }
    variants=[]
    for scenario in ("noise_baseline","no_hook_Z"):
        r=dict(rates)
        if scenario=="no_hook_Z":r["ancilla_Z_after_SUM"]=0
        rng=random.Random(SEED+(scenario=="no_hook_Z"))
        obs=[extraction(rows,layers,rng,r) for _ in range(SHOTS)]
        keys=sorted(set(k for sample in obs for k in sample))
        metrics={k:sum(s.get(k,0) for s in obs)/SHOTS for k in keys}
        variants.append({"scenario":scenario,"shots":SHOTS,
                         "rounds":ROUNDS,"rates":r,"observed_means":metrics})
        print("ANCILLA",scenario,"layers",len(layers),
              "Z hook",metrics["true_Z_nonzero"],
              "last mismatches",metrics["raw_final_readout_mismatch"],
              "majority mismatches",metrics["majority_readout_mismatch"],flush=True)
    assert variants[1]["observed_means"]["true_Z_nonzero"]==0
    assert variants[0]["observed_means"]["true_Z_nonzero"]>0
    return {
       "status":"STOCHASTIC_TOY_CIRCUIT_PLUS_EXACT_CLIFFORD_HOOK_PROPAGATION",
       "face_Z_stabilizer_count":99,"edge_data_qutrits":135,
       "ancilla_qutrits_per_round":99,
       "SUM_gates_per_round":sum(len(l) for l in layers),
       "conflict_free_parallel_layers_per_round":len(layers),
       "face_weight_distribution":dict(collections.Counter(str(sum(t%3!=0 for t in face)) for face in rows)),
       "ancilla_Z_hook_propagation_witness":hook,
       "configurations":variants,
       "limitations":"Only Z checks and Pauli-frame propagation, no X stabilizers or physical photonic gates. Ancilla Z hook makes data Z errors invisible to this Z-syndrome, so the circuit is NOT fault tolerant. Decoder is single-site only; no threshold, no logical success claim."}

if __name__=="__main__":
    d=certificate()
    p=ROOT/"data/w33_20261015_toe88_ancilla_syndrome.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("SAVED",p)
