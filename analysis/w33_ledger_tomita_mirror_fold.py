#!/usr/bin/env python3
"""Actual finite Tomita conjugation compared with the W33 anti-symplectic mirrors."""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
import w33_ledger_mirror_group_stress_test as M
OUT=Path("data/PART_LEDGER_TOMITA_MIRROR_FOLD.json")
def main():
    w=np.exp(2j*np.pi/3);X=np.roll(np.eye(3,dtype=complex),1,axis=0);Z=np.diag([w**j for j in range(3)])
    def W(v):
        a,b,c,d=v
        return np.kron(np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,c),
                       np.linalg.matrix_power(X,b)@np.linalg.matrix_power(Z,d))
    rng=np.random.default_rng(20260921);T=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
    terr=ferr=lerr=0.0
    for v in itertools.product(range(3),repeat=4):
        A=W(v); lhs=(A@T.conj().T).conj().T;rhs=T@A.conj().T
        terr=max(terr,float(np.max(abs(lhs-rhs))))
        folded=(A.conj().T).T; rv=(v[0],v[1],-v[2]%3,-v[3]%3)
        ferr=max(ferr,float(np.max(abs(folded-np.conjugate(A)))))
        lerr=max(lerr,float(np.max(abs(np.conjugate(A)-W(rv)))))
    R=M.base_mirror_perm();gens,idxs,psp,growth=M.greedy_psp_generators()
    mirrors={M.compose(M.compose(g,R),M.invperm(g)) for g in psp}
    anti=all(M.symp((u[0],u[1],-u[2],-u[3]),(v[0],v[1],-v[2],-v[3]))==(-M.symp(u,v))%3 for u in M.POINTS for v in M.POINTS)
    checks={"tomita_identity":terr<1e-12,"fold_is_complex_conjugation":ferr<1e-12,"weyl_label_mirror":lerr<1e-12,
            "anti_symplectic":anti,"psp_25920":len(psp)==25920,"mirror_orbit_540":len(mirrors)==540,"base_in_orbit":R in mirrors}
    assert all(checks.values()),checks
    out={"schema":"w33.ledger.tomita-mirror-fold.v1","status":"PASS_TOMITA_TO_W33_MIRROR_AFTER_COMMUTANT_FOLD",
         "standard_form":{"J":"J(X)=X^dagger","identity":"J L_A J=R_{A^dagger}",
                          "state_dependence":"For faithful states in matrix standard form, Delta_rho changes with rho but J is fixed."},
         "fold":{"map":"R_B -> L_{B^T}","result":"Fold(J L_A J)=L_bar(A)",
                 "weyl_labels":"(xA,xB,zA,zB)->(xA,xB,-zA,-zB)","matrix":"diag(1,1,-1,-1)"},
         "w33":{"psp_order":len(psp),"clifford_frame_orbit":len(mirrors)},
         "correction":"The 540 W33 mirrors are Clifford frame/fold realizations of one standard-form algebra-to-commutant map, not 540 state-dependent Tomita J operators.",
         "remaining_gap":"A spacetime reflection interpretation still needs an additional theorem beyond Tomita-Takesaki.",
         "errors":{"tomita":terr,"fold":ferr,"label":lerr},"checks":checks}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=="__main__":main()
