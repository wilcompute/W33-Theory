#!/usr/bin/env python3
"""Sharp quantum positivity falsifier for exact E6 split shear
which dynamically isolates one section in canonical 27 chart.

A physical three-qubit state rho maps to 27 Pauli expectation charges
q_i=Tr(rho P_i). The J-twirl rho_J has paired eigenvalues and
sum q_i² <=3. In the canonical signed cubic, 180 rank-2
J-quaternionic stabilizer states supported on one tritangent
triple realize all N(q)=1, sum q_i²=3.

Although U=I+root[2] is exact split E6 cubic preserving, test it
on all 180 extreme charge states; one with |Uq|²>3 is a
machine-checkable proof that U is not an affine CPTP map of arbitrary
three-qubit quantum states in this Pauli-charge dictionary.
"""
from pathlib import Path
import sys,json
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261114_exact_gaussian_us8_pauli_clock as E
OUT=ROOT/"data/toe_20261114_split_E6_shear_not_quantum_channel.json"
I8=np.eye(8,dtype=complex)
def main():
    _,terms,_,_,roots=R.load()
    shear=np.asarray(roots[2],dtype=np.int64)
    assert shear.shape==(27,27) and not (shear@shear).any()
    cert=json.loads((ROOT/"data/toe_20261114_exact_gaussian_integer_USp8_pauli_Albert_intertwiner.json").read_text())
    pm={int(k):int(v) for k,v in cert["coordinate_to_pauli_label"].items()}
    neg=set(cert["coordinate_negative_sign_indices"])
    B={i:(-1 if i in neg else 1)*E.P(pm[i]) for i in range(27)}
    def density(q):
        X=sum((int(q[i])*B[i] for i in range(27)),np.zeros((8,8),complex))
        return (I8+X)/8
    tests=[]
    for tr,s in sorted(terms.items()):
        a,b,c=tr
        assert abs(s)==1
        for ea in (-1,1):
            for eb in (-1,1):
                q=np.zeros(27,dtype=np.int64)
                q[a]=ea;q[b]=eb;q[c]=s*ea*eb
                rho=density(q)
                assert np.array_equal(rho.conj().T,rho)
                assert abs(np.trace(rho)-1)<1e-10
                assert np.min(np.linalg.eigvalsh(rho))>-1e-10
                assert np.dot(q,q)==3
                N=lambda x: sum(int(k)*int(x[i])*int(x[j])*int(x[l])
                                for (i,j,l),k in terms.items())
                assert N(q)==1
                for sign in (-1,1):
                    U=np.eye(27,dtype=np.int64)+sign*shear
                    out=U@q
                    assert N(out)==1
                    ss=int(out@out)
                    eig=np.linalg.eigvalsh(density(out))
                    tests.append(dict(triad=list(tr),seed_signs=[ea,eb],
                                      shear_sign=sign,old_norm=3,new_norm=ss,
                                      min_density_eigenvalue=float(eig.min()),
                                      input_nonzero=[[int(i),int(z)] for i,z in enumerate(q) if z],
                                      output_nonzero=[[int(i),int(z)] for i,z in enumerate(out) if z]))
    assert len(tests)==360
    badnorm=[r for r in tests if r["new_norm"]>3]
    badpsd=[r for r in tests if r["min_density_eigenvalue"] < -1e-8]
    assert badnorm and badpsd
    assert all(r["min_density_eigenvalue"]<-1e-8 for r in badnorm)
    # Hamiltonian normalizer/Clifford compact action cannot increase
    # the trace norm, while the split root shear can.
    examples=sorted(badnorm,key=lambda v:(-v["new_norm"],v["triad"],v["seed_signs"]))
    r=dict(status="PASS_SPLIT_E6_ROOT_SHEAR_FAILS_PHYSICAL_PAULI_CHARGE_POSITIVITY",
        tested_J_twirl_rank2_stabilizer_states=180,
        tested_signed_shears=2,
        tested_total=360,
        N_constant=1,
        old_norm_squared=3,
        new_norm_squared_distribution={str(k):v for k,v in sorted(Counter(z["new_norm"] for z in tests).items())},
        count_new_norm_squared_gt3=len(badnorm),
        count_new_density_not_positive=len(badpsd),
        explicit_strongest_bad_example=examples[0],
        physical_quantum_bound="For ANY three-qubit density matrix, the J-averaged density rho_J=(rho+Jrho J^-1)/2 has even spectral multiplicities, hence Tr(rho_J²)<=1/2. For X=8rho_J-I=sum_i q_i P_i this yields sum_i q_i²=(Tr X²)/8=8Tr(rho_J²)-1<=3.",
        no_go="The cubic-preserving noncompact E6 section-isolating shear U=I+R cannot map all physical Pauli-charge expectation vectors to physical three-qubit states by any deterministic positive trace-preserving quantum channel: it maps explicit physical input charges to vectors outside the physical bound sum q²<=3.",
        scope="The no-go applies to the AFFINE 27-Pauli expectation-value encoding and exact linear action U on it. It does not prohibit field-theoretic charge transformations, changes of frame with generalized metric, postselected nonlinear filters or noncompact E6 group dynamics on an unconstrained 27 real charge field.",
        cited_repo_input="analysis/toe_20261114_e6_split_six_section.py root index 2 and exact USp8 Pauli dictionary.")
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:r[k] for k in ["status","tested_total","new_norm_squared_distribution","count_new_norm_squared_gt3","count_new_density_not_positive","explicit_strongest_bad_example"]},indent=2),flush=True)
    return r
if __name__=="__main__":main()
