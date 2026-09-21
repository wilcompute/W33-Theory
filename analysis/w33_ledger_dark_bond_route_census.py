#!/usr/bin/env python3
"""Census four proposed dark-bond escape routes after the H.4 product-Hamiltonian no-go."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
OUT=Path("data/PART_LEDGER_DARK_BOND_ROUTE_CENSUS.json")
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
P=[I,X,Y,Z]
def expmH(H,t):
    w,v=np.linalg.eigh(H);return (v*np.exp(-1j*t*w))@v.conj().T
def coeff(H,A,B):return float((np.trace(np.kron(A,B).conj().T@H)/4).real)
def interaction_norm(H):
    local=sum(coeff(H,A,B)*np.kron(A,B) for A in P for B in P if (A is I or B is I))
    return float(np.linalg.norm(H-local,"fro"))
def ptr(rho):return np.einsum("arbr->ab",rho.reshape(2,2,2,2))
def entropy(r):
    w=np.clip(np.linalg.eigvalsh((r+r.conj().T)/2).real,1e-15,1);return float(-np.sum(w*np.log(w)))
def main():
    a,b,g=.7,.4,.31;H0=a*np.kron(Z,I)+b*np.kron(I,Z);G=g*np.kron(X,X);t=.37;W=expmH(G,t)
    Hfixed=W@H0@W.conj().T+G
    move={"identity":"H_fixed=W H_product W^dag+i dot(W)W^dag; W=e^{-itG} gives i dot(W)W^dag=G",
          "interaction_frobenius_norm":interaction_norm(Hfixed),"XX_coefficient_t0":g}
    alpha=.39;psi=np.array([np.cos(alpha),0,0,np.sin(alpha)],complex);rho=np.outer(psi,psi.conj())
    ent=[];spec=[]
    for tt in (0,.2,.7,1.1):
        U=expmH(H0,tt);r=ptr(U@rho@U.conj().T);ent.append(entropy(r));spec.append(np.sort(np.linalg.eigvalsh(r).real))
    modular={"max_entropy_drift":max(abs(x-ent[0]) for x in ent),
             "max_schmidt_drift":max(float(np.max(abs(x-spec[0]))) for x in spec)}
    Pe=np.diag([1,0,0,1]).astype(complex);Qo=np.eye(4)-Pe;Delta=10.;tau=.8;V=tau*(np.kron(X,I)+np.kron(I,X))
    Heff=-(Pe@V@Qo@V@Pe)/Delta;logical=Heff[np.ix_([0,3],[0,3])];Hpen=Delta*Qo
    constraint={"penalty":"Delta Q_odd=(Delta/2)(I-Z tensor Z)","ZZ_coefficient":coeff(Hpen,Z,Z),
                "logical_second_order":[[float(x.real) for x in row] for row in logical],
                "logical_offdiag":float(logical[0,1].real),"expected":float(-2*tau*tau/Delta),
                "decoupling":"For fixed tau the induced term scales tau^2/Delta and vanishes as Delta->infinity."}
    M=12.;y=.6
    auxiliary={"lagrangian":"(M/2)NN+yN(LH), with no kinetic term for N","eom":"N=-(y/M)(LH)",
               "induced":"-(y^2/(2M))(LH)(LH)","C5_y2_over_M":y*y/M,
               "tree_level_pole":"No momentum-dependent N pole exists before adding a kinetic term.",
               "firewall":"This is only a contact/auxiliary rewriting; radiative Higgs protection and a unitary Lorentzian UV completion remain unproved."}
    checks={"moving_frame_has_interaction":move["interaction_frobenius_norm"]>.1,
            "modular_entropy_invariant":modular["max_entropy_drift"]<1e-13,
            "modular_schmidt_invariant":modular["max_schmidt_drift"]<1e-13,
            "constraint_induces_operator":abs(constraint["logical_offdiag"])>.05,
            "constraint_formula":abs(constraint["logical_offdiag"]-constraint["expected"])<1e-14,
            "constraint_nonfactorizing":abs(constraint["ZZ_coefficient"])>1,
            "auxiliary_c5_nonzero":auxiliary["C5_y2_over_M"]>0}
    assert all(checks.values()),checks
    out={"schema":"w33.ledger.dark-bond-route-census.v1","status":"NO_INTERACTION_FREE_DYNAMIC_BOND_FOUND_AUXILIARY_ROUTE_TREE_LEVEL_ONLY",
         "moving_factorization":move,"modular_only":modular,"nonfactorizing_constraint":constraint,"algebraic_auxiliary_candidate":auxiliary,
         "verdicts":{"moving_factorization":"fails: the interaction is relocated into the frame generator",
                     "modular_only":"fails under fixed product dynamics: Schmidt/modular spectra do not grow",
                     "constraint":"induces an effective operator, but the nonfactorizing finite constraint scale is the resource",
                     "auxiliary":"only tree-level candidate found for a Weinberg contact without a propagating heavy pole; quantum naturalness/UV closure remain open"},
         "external_context":["Gauge constraints can obstruct tensor-product factorization of regional Hilbert spaces (Casini-Huerta-Rosabal).",
                             "Inverse-seesaw analyses still find sizable Higgs-mass corrections; approximate lepton number alone does not erase the naturalness issue."],
         "checks":checks}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=="__main__":main()
