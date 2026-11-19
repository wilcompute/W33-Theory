"""W33 [[40,19,(4,6)]]_3: biased decoder, diagonal-T9 no-go, and injection.

Reuses canonical W33 checks from the simultaneously committed 22a122ec
without duplicating graph geometry. All linear algebra over F3 is exact.

Diagonal no-go restriction: depth-one tensor products of local T9 powers
times local diagonal qutrit Clifford phases. Does NOT exclude entangling
finite-depth circuits, code switching, non-diagonal local conjugations,
or encoded magic-state injection.
"""
from itertools import combinations,product
from math import comb
from pathlib import Path
import sys,json,hashlib
import numpy as np
from toe_20261119_w33_40_qutrit_css import checks,rref_mod3,rank_mod3

ROOT=Path(__file__).resolve().parents[1]
N=40

def kernel_basis(A):
    R=rref_mod3(A)
    lead=[int(np.flatnonzero(row)[0]) for row in R]
    free=[j for j in range(A.shape[1]) if j not in lead]
    K=np.zeros((A.shape[1],len(free)),dtype=np.int64)
    for i,j in enumerate(free):
        K[j,i]=1
        K[lead,i]=(-R[:,j])%3
    assert np.all(A@K%3==0)
    return K

def no_transversal_diagonal_T9(HX):
    # qutrit T9=diag(zeta9^{j^3}), diagonal Clifford S=diag(1,1,omega)
    # and Z=diag(1,omega,omega^2).
    R=rref_mod3(HX)
    K=kernel_basis(R)
    assert R.shape==(11,40) and K.shape==(40,29)
    piv={}
    certificate=[]
    for weight in (1,2):
        for chosen in combinations(range(11),weight):
            for vals in product((1,2),repeat=weight):
                h=np.zeros(40,dtype=np.int64)
                for i,a in zip(chosen,vals):
                    h=(h+a*R[i])%3
                f=np.where(h==2,8,h)  # j^3 modulo 9
                cubic=f@K
                assert np.all(cubic%3==0)
                row=np.r_[f%3,(h==2).astype(np.int64),(cubic//3)%3]
                reduced=row.copy()
                for col in sorted(piv):
                    reduced=(reduced-int(reduced[col])*piv[col])%3
                ix=np.flatnonzero(reduced)
                if len(ix):
                    column=int(ix[0])
                    reduced=(reduced*(1 if reduced[column]==1 else 2))%3
                    piv[column]=reduced
                    certificate.append((chosen,vals,h,row))
                if len(piv)==70:
                    break
            if len(piv)==70:break
        if len(piv)==70:break
    assert len(certificate)==70
    E=np.stack([q[3] for q in certificate])
    ranks=[rank_mod3(E[:,:40]),rank_mod3(E[:,:80]),rank_mod3(E)]
    assert ranks==[11,41,70]
    # For a phase p(h)=sum_i lambda_i*h_i^3 +3 mu_i*q(h_i)+3 nu_i*h_i,
    # mod3 forces lambda mod3 in ker(R), lambda=K*t+3*s.
    # The divided-by-3 constraints are E * (s,mu,t)=0 mod3.
    # rank([E_s,E_mu])=41 and rank E=70, so the 29 t components vanish.
    # Therefore lambda=3*s and T9^lambda is only Pauli-Z, not non-Clifford.
    compact=[{"support_rows":[int(i) for i in inds],
              "coefficients":[int(a) for a in cs]}
             for inds,cs,_,_ in certificate]
    signature=hashlib.sha256(E.astype(np.uint8).tobytes()).hexdigest()
    return {"family":"local T9^lambda times local diagonal qutrit Clifford",
            "T9_phase_exponents_mod9":[0,1,8],
            "linear_code_rank":11,"code_kernel_dimension":29,
            "certificate_codewords":len(certificate),
            "certifier_row_generator_weight_distribution":{"1":22,"2":48},
            "ranks_F3_cubic_linear_quadratic":[11,41,70],
            "constraint_matrix_shape":[70,109],
            "F3_certificate_sha256":signature,
            "witnesses":compact,
            "conclusion":"If the diagonal layer preserves this CSS code, every physical T9 exponent lambda_i must be 0 mod3; all surviving such layers are diagonal Clifford, not logical non-Clifford.",
            "limits":"Only this diagonal tensor-product family; not a no-go for general finite-depth circuits or ancilla injection."}

def synd(H,v):
    return bytes(((H@v)%3).astype(np.uint8))

def errors_upto(n,t):
    yield np.zeros(n,dtype=np.int64),0
    for weight in range(1,t+1):
        for support in combinations(range(n),weight):
            for coeffs in product((1,2),repeat=weight):
                v=np.zeros(n,dtype=np.int64)
                v[list(support)]=coeffs
                yield v,weight

def build_decoder(H,t):
    dec={}
    counts={}
    for error,weight in errors_upto(N,t):
        key=synd(H,error)
        assert key not in dec, ("syndrome collision",weight)
        dec[key]=error
        counts[weight]=counts.get(weight,0)+1
    return dec,counts

def cdf(n,p,t):
    return sum(comb(n,w)*p**w*(1-p)**(n-w) for w in range(t+1))

def decoder_certificate(HX,HZ):
    # X-errors are detected by Z checks; Z-errors by X checks.
    decX,cx=build_decoder(HZ,1)
    decZ,cz=build_decoder(HX,2)
    assert cx=={0:1,1:80}
    assert cz=={0:1,1:80,2:3120}
    rng=np.random.default_rng(281828)
    checked=0
    for it in range(2500):
        eX=np.zeros(N,dtype=np.int64)
        eZ=np.zeros(N,dtype=np.int64)
        wx=int(rng.integers(0,2));wz=int(rng.integers(0,3))
        if wx:
            pos=rng.choice(N,size=wx,replace=False)
            eX[pos]=rng.integers(1,3,wx)
        if wz:
            pos=rng.choice(N,size=wz,replace=False)
            eZ[pos]=rng.integers(1,3,wz)
        corrX=decX[synd(HZ,eX)]
        corrZ=decZ[synd(HX,eZ)]
        assert np.all((eX-corrX)%3==0) and np.all((eZ-corrZ)%3==0)
        checked+=1
    comparisons=[]
    for pX,pZ in ((.005,.01),(.01,.01),(.002,.02)):
        normal=cdf(N,pX,1)*cdf(N,pZ,2)
        swapped=cdf(N,pZ,1)*cdf(N,pX,2)
        comparisons.append({"pX":pX,"pZ":pZ,
                            "guaranteed_success_original":normal,
                            "guaranteed_success_after_Fourier_swap":swapped,
                            "better_orientation":"original" if normal>swapped else ("Fourier_swap" if swapped>normal else "tie")})
    assert comparisons[0]["guaranteed_success_original"]>comparisons[0]["guaranteed_success_after_Fourier_swap"]
    return {"code":"W33 asymmetric [[40,19,4]]_3 with (dX,dZ)=(4,6)",
            "X_decoder_radius":1,"Z_decoder_radius":2,
            "pure_X_syndromes":len(decX),"pure_Z_syndromes":len(decZ),
            "decoded_both_sector_patterns":len(decX)*len(decZ),
            "joint_test_samples":checked,
            "per_site_noise_model":"independent ternary X and Z components, each nonidentity probability pX,pZ, exponent 1/2 conditional on an error",
            "orientation_benchmark":comparisons,
            "probability_statement":"P(weightX<=1 and weightZ<=2) is an EXACT noise-event probability and a LOWER BOUND on total decoder success, not a full circuit-level logical error probability.",
            "status":"PASS"}

def magic_injection():
    zeta=np.exp(2j*np.pi/9)
    w=np.exp(2j*np.pi/3)
    U=np.array([zeta**(j**3) for j in range(3)])
    magic=U/np.sqrt(3)
    sic=np.array([0,1,-1],dtype=complex)/np.sqrt(2)
    rng=np.random.default_rng(20261119)
    tested=0
    max_error=0.0
    corrections=[]
    for m in range(3):
        denom=U[(np.arange(3)+m)%3]
        corr=U/denom
        rel=corr/corr[0]
        expected={0:[1,1,1],1:[1,w,1],2:[1,1,w*w]}[m]
        assert np.allclose(rel,expected,atol=2e-14)
        corrections.append([int(x) for x in {0:[0,0,0],1:[0,1,0],2:[0,0,2]}[m]])
        for t in range(20):
            psi=rng.normal(size=3)+1j*rng.normal(size=3)
            psi/=np.linalg.norm(psi)
            # Resource in second qudit, inverse SUM data-control -> ancilla target,
            # measure ancilla m. Branch amplitude is psi_j * magic_(m+j).
            branch=psi*magic[(np.arange(3)+m)%3]
            p=float(np.vdot(branch,branch).real)
            assert abs(p-1/3)<1e-13
            recovered=corr*branch*np.sqrt(3)
            err=float(np.linalg.norm(recovered-U*psi))
            max_error=max(max_error,err)
            assert err<1e-13
            tested+=1
    sic_singular=[]
    for m in range(3):
        raw=np.diag(sic[(np.arange(3)+m)%3])
        svals=np.linalg.svd(raw,compute_uv=False)
        assert svals[-1]<1e-14
        sic_singular.append([float(v) for v in svals])
    return {"gate":"T9=diag(1,zeta9,zeta9^8)",
            "one_ancilla_magic_resource":"T9|+> (all computational amplitudes 1/sqrt3)",
            "injection_gates":"inverse-SUM from data to resource; computational measurement on resource; feed-forward diagonal Clifford",
            "outcome_probabilities":[1/3]*3,
            "outcome_correction_relative_omega_exponents":corrections,
            "tested_random_state_outcome_pairs":tested,
            "maximum_statevector_norm_error":max_error,
            "Hesse_SIC_fiducial_in_same_injection":"(0,1,-1)/sqrt2",
            "Hesse_SIC_injection_branch_singular_values":sic_singular,
            "SIC_is_direct_deterministic_T9_resource":False,
            "coded_SUM_compatibility":"Two identical CSS blocks admit transversal ternary SUM: conjugated X control check -> X checks on both blocks; Z target check -> inverse Z control and Z target checks.",
            "limitations":"Unencoded deterministic state-injection identity. Fault-tolerant logical T9 needs an encoded T9|+> ancilla prepared/distilled and fault-tolerant logical measurement and feed-forward; Hesse SIC strange-state resource produces a rank-two filter in this injection gadget."}

def main():
    _,_,HX,HZ=checks()
    out={"transversal_gate_no_go":no_transversal_diagonal_T9(HX),
         "biased_decoder":decoder_certificate(HX,HZ),
         "T9_injection":magic_injection()}
    target=ROOT/"data"/"toe_20261119_w33_code_gate_and_decoder.json"
    target.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    print("PASS diagonal ninth-root no-go: rank [11,41,70] from 70 explicit codewords")
    print("PASS biased error decoder: 81 X and 3201 Z pure-sector syndromes, 2500 exact corrections")
    print("PASS deterministic one-qutrit T9 injection via Clifford feed-forward; SIC filter is nonunitary")
    print(json.dumps({"certificate_ranks":out["transversal_gate_no_go"]["ranks_F3_cubic_linear_quadratic"],
                      "guaranteed_success":out["biased_decoder"]["orientation_benchmark"],
                      "injection_error":out["T9_injection"]["maximum_statevector_norm_error"]},indent=2))
    print(target)
    return out

if __name__=="__main__":
    main()
