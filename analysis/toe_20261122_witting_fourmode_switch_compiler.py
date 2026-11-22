"""Compile all 40 Witting ray reflections as exact four-mode passive circuits.

One rank-one reflection U=I-2|v><v| is obtained by preparing v as a basis
mode with k-1 Givens, a pi phase, and undoing those k-1 Givens, where k is
the support size. Port-pair reachability, coherent gate-order control and
experimental losses are not supplied by this compilation.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import numpy as np
import toe_20261122_experiment_driven_five_fronts as prior
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261122_witting_fourmode_switch_compiler.json"

def compile_reflection(v):
    support=np.flatnonzero(abs(v)>1e-12)
    anchor=int(support[0])
    state=v.copy()
    G=np.eye(4,dtype=complex)
    for b in support[1:]:
        b=int(b)
        x,y=state[anchor],state[b]
        n=np.hypot(abs(x),abs(y))
        local=np.array([[np.conj(x)/n,np.conj(y)/n],[-y/n,x/n]],complex)
        U=np.eye(4,dtype=complex)
        U[np.ix_([anchor,b],[anchor,b])]=local
        G=U@G
        state=U@state
    assert np.max(abs(state-np.eye(4)[anchor]))<1e-11
    D=np.eye(4,dtype=complex)
    D[anchor,anchor]=-1
    reflection=G.conj().T@D@G
    assert np.max(abs(reflection-(np.eye(4)-2*np.outer(v,v.conj()))))<1e-11
    return reflection,2*(len(support)-1)

def main():
    rays,H,A,P=prior.witting()
    compiled=[compile_reflection(v)for v in rays]
    counts=Counter(n for _,n in compiled)
    assert counts=={0:4,4:36}
    largest_error=max(float(np.max(abs(U-(np.eye(4)-2*np.outer(v,v.conj())))))
                      for (U,_),v in zip(compiled,rays))
    pairs=Counter()
    for i in range(40):
        for j in range(i+1,40):
            U,V=compiled[i][0],compiled[j][0]
            minus=float(np.linalg.norm(U@V-V@U)**2/16)
            pairs[round(minus,9)]+=1
    assert pairs=={0.:240,round(4/9,9):540}
    d={"status":"PASS","date":"2026-11-22","reflections":40,
       "arbitrary_two_mode_Givens_per_reflection":{str(k):int(v)for k,v in sorted(counts.items())},
       "single_mode_pi_phase_per_reflection":1,
       "maximum_compiled_matrix_error":largest_error,
       "compiled_switch_minus_probability_pair_counts":{str(k):int(v)for k,v in sorted(pairs.items())},
       "boundary":"Only target 4-mode unitaries compiled, NOT coherently controlled gate order, spatial routing, loss or photonic switch hardware."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print("PASS Witting fourmode reflection compilation",counts)
    return d

if __name__=="__main__":main()
