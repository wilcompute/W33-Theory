"""Negative control: 20 rays from 5 ququart MUBs reproduce the Witting witness.

They are a different 2-design with a smaller POVM. Same-label coincidence
as a singlet fidelity witness is therefore a GENERIC two-design identity,
not evidence of a special W33 law.
"""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261122_generic_ququart_2design_control.json"
def run():
    I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    pauli=[np.kron(a,b)for a,b in itertools.product((I,X,Y,Z),repeat=2)][1:]
    abelian=[tri for tri in itertools.combinations(range(15),3)
             if all(np.max(abs(pauli[i]@pauli[j]-pauli[j]@pauli[i]))<1e-12
                    for i,j in itertools.combinations(tri,2))]
    assert len(abelian)==15
    partition=next(p for p in itertools.combinations(abelian,5)
                   if len(set(itertools.chain.from_iterable(p)))==15)
    rays=[]
    for tri in partition:
        _,V=np.linalg.eigh(pauli[tri[0]]+2*pauli[tri[1]])
        rays.extend(V.T)
    rays=np.array(rays)
    assert rays.shape==(20,4)
    overlaps=abs(rays.conj()@rays.T)**2
    for i in range(5):
        for j in range(i+1,5):
            assert np.max(abs(overlaps[4*i:4*i+4,4*j:4*j+4]-.25))<1e-11
    P=np.einsum("ai,aj->aij",rays,rays.conj())
    assert np.max(abs(P.sum(0)-5*np.eye(4)))<1e-11
    F=np.zeros((16,16))
    for a in range(4):
        for b in range(4): F[4*a+b,4*b+a]=1
    err1=float(np.max(abs(sum(np.kron(q,q)for q in P)-np.eye(16)-F)))
    phi=np.eye(4).reshape(16)/2
    C=sum(np.kron(q,q.conj())for q in P)/25
    err2=float(np.max(abs(C-.04*np.eye(16)-.16*np.outer(phi,phi.conj()))))
    assert max(err1,err2)<1e-11
    d={"status":"PASS","date":"2026-11-22","source":"5 exact commuting triples covering 15 two-qubit Pauli operators",
      "MUB_bases":5,"ray_outcomes":20,
      "Pauli_abelian_triple_partition":[list(x)for x in partition],
      "max_2design_error":err1,"max_same_label_identity_error":err2,
      "measurement_effect":"sum_i (Pi/5) tensor (conjugate(Pi)/5) = .04I16+.16|Phi4><Phi4|",
      "Schmidt_k_same_label_bounds":[.04+.04*k for k in (1,2,3)],
      "interpretation":"Generic ququart 2-design control: the singlet fidelity coincidence formula alone cannot distinguish Witting/W33 from complete MUB geometry."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print("PASS non-Witting 5MUB 2-design negative control")
    return d
if __name__=="__main__":run()
