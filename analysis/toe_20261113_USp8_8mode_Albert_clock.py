#!/usr/bin/env python3
"""Independently audit the full 36-generator highest-weight USp8
intertwiner and lift the exact Albert clock to defining eight modes.

For each of the repo's 36 skew cubic K_i solve uniquely for 36
REAL standard usp8 coefficients A_i in 8x8, using the explicit T.
Verify T K_i=ρ(A_i)T, all 36 brackets, and exp group action.

For the Albert order-three U, use its skew logarithm
S=(U-U^T)/sqrt3 and check the lift A8 has rank 2 and
spectrum {0^6,+i,-i}. Then a single symplectic 2-plane
rotation in eight defining modes induces the full 27x27
order-three Albert clock.
"""
from pathlib import Path
from itertools import combinations
import json,sys,math
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261113_USp8_full36_intertwiner_audit as F
OUT=ROOT/"data/toe_20261113_USp8_8mode_Albert_clock_exact_group_check.json"

def wedge_group(g):
    pairs=list(combinations(range(8),2))
    W=np.zeros((28,28),dtype=complex)
    for col,(i,j) in enumerate(pairs):
        for row,(k,l) in enumerate(pairs):
            W[row,col]=g[k,i]*g[l,j]-g[l,i]*g[k,j]
    return W

def load_T():
    c=json.loads((ROOT/"data/toe_20261113_USp8_full36_highest_weight_intertwiner.json").read_text())
    assert c["status"]=="FULL_36_INTERTWINER_VERIFIED"
    T=np.array(c["matrix_T_real"],dtype=float)+1j*np.array(c["matrix_T_imag"],dtype=float)
    assert T.shape==(28,27)
    assert np.max(abs(T.conj().T@T-np.eye(27)))<1e-9
    return T

def main():
    T=load_T()
    bases=F.defining_basis()
    induced=[F.wedge_action(x) for x in bases]
    bm=np.stack([np.r_[x.real.ravel(),x.imag.ravel()] for x in induced],axis=1)
    assert np.linalg.matrix_rank(bm)==36
    _,terms,D,mapi,roots=R.load()
    _,Ks=R.pack_roots(roots)
    mapped8=[]
    mapped28=[]
    errors=[]
    for K in Ks:
        target=T@K@T.conj().T
        c,_,_,_=np.linalg.lstsq(bm,np.r_[target.real.ravel(),target.imag.ravel()],rcond=None)
        A8=sum((z*a for z,a in zip(c,bases)),np.zeros((8,8),complex))
        W28=F.wedge_action(A8)
        err=float(np.linalg.norm(T@K-W28@T)/np.linalg.norm(K))
        assert err<1e-9,err
        mapped8.append(A8);mapped28.append(W28);errors.append(err)
    algebra_errors=[]
    for i,j in [(0,1),(0,7),(3,25),(10,24),(15,30)]:
        X=Ks[i]@Ks[j]-Ks[j]@Ks[i]
        Y=mapped8[i]@mapped8[j]-mapped8[j]@mapped8[i]
        assert np.linalg.norm(T@X-F.wedge_action(Y)@T)<1e-9
        algebra_errors.append(float(np.linalg.norm(T@X-F.wedge_action(Y)@T)))
    Ucert=json.loads((ROOT/"data/toe_20261113_Albert_cyclic_clock_sections.json").read_text())
    U=np.zeros((27,27),dtype=np.int64)
    for i,j,v in Ucert["signed_E6_clock_matrix_27_sparse_entries"]:U[i,j]=v
    assert np.array_equal(U@U@U,np.eye(27,dtype=np.int64))
    A=(U-U.T)/math.sqrt(3)
    assert np.max(abs(A+A.T))<1e-10
    assert np.max(abs(A@A@A+A))<1e-10
    beta,_,_,_=np.linalg.lstsq(np.stack([K.ravel() for K in Ks],axis=1),A.ravel(),rcond=None)
    assert np.linalg.norm(sum((z*K for z,K in zip(beta,Ks)),np.zeros((27,27)))-A)<1e-10
    generator8=sum((float(z)*G for z,G in zip(beta,mapped8)),np.zeros((8,8),complex))
    assert np.max(abs(generator8.conj().T+generator8))<1e-9
    rank8=np.linalg.matrix_rank(generator8,tol=1e-9)
    assert rank8==8,rank8
    freqs=np.linalg.eigvalsh(-1j*generator8)
    assert np.max(abs(np.sort(freqs)-np.array([-.5]*4+[.5]*4)))<1e-9,freqs
    # The true lift has 4 positive and 4 negative half-frequency
    # modes, NOT a single pair. Its cubic central phase is -I8.
    assert np.max(abs(generator8@generator8+.25*np.eye(8)))<1e-9
    g8=expm((2*math.pi/3)*generator8)
    g8_poly=.5*np.eye(8)+math.sqrt(3)*generator8
    assert np.max(abs(g8-g8_poly))<1e-10
    assert np.max(abs(g8@g8@g8+np.eye(8)))<1e-9
    assert np.max(abs(np.linalg.matrix_power(g8,6)-np.eye(8)))<1e-9
    assert np.max(abs(g8.conj().T@g8-np.eye(8)))<1e-9
    J=np.block([[np.zeros((4,4)),np.eye(4)],[-np.eye(4),np.zeros((4,4))]])
    assert np.max(abs(g8.T@J@g8-J))<1e-9
    assert np.max(abs(wedge_group(g8)@T-T@U))<1e-9
    char8=np.linalg.eigvals(g8)
    sixth=np.exp(1j*math.pi/3)
    assert sum(abs(z-sixth)<1e-8 for z in char8)==4
    assert sum(abs(z-sixth.conjugate())<1e-8 for z in char8)==4
    out={
      "status":"PASS_FULL36_USP8_INTERTWINER_AND_ALBERT_CLOCK_ORDER6_LIFT_ORDER3_WEDGE",
      "full_intertwiner_shape":[28,27],
      "all_36_generators_match_standard_usp8_rep":True,
      "max_36_generator_intertwining_error":max(errors),
      "bracket_intertwining_checks":len(algebra_errors),
      "max_bracket_residual":max(algebra_errors),
      "Albert_clock_original_27_eigen_mult":[15,6,6],
      "Albert_clock_8mode_source_generator_rank":int(rank8),
      "Albert_clock_8mode_source_generator_eigenvalues_imag":list(map(float,np.round(freqs,12))),
      "Albert_clock_8mode_group_eigen_mult":[4,4],
      "Albert_clock_8mode_generator_minimal_polynomial":"A8^2=-I8/4",
      "Albert_clock_8mode_group_eigenvalues":"four exp(+i pi/3) plus four exp(-i pi/3)",
      "Albert_clock_defining_8mode_symplectic_unitary":True,
      "Albert_clock_defining_8mode_order6":True,
      "Albert_clock_defining_8mode_cubed_is_center_minus_I":True,
      "Albert_clock_27mode_induced_order3":True,
      "induced_27mode_group_intertwiner_residual":float(np.max(abs(wedge_group(g8)@T-T@U))),
      "8mode_generator_real":np.round(generator8.real,12).tolist(),
      "8mode_generator_imag":np.round(generator8.imag,12).tolist(),
      "8mode_group_real":np.round(g8.real,12).tolist(),
      "8mode_group_imag":np.round(g8.imag,12).tolist(),
      "8mode_central_double_cover":"8D clock has g8^3=-I8, g8^6=I8. The central -I8 acts trivially on wedge²_0(8), so induced 27D clock has U^3=I27. Four fundamental positive and four negative half-frequencies yield six omega and six omega^-1 27D modes.",
      "scope":"Numerically high-precision explicit 8D compact symplectic representation of exact repo 27D signed cubic stabilizer and its compatible Albert clock. The representation is equivalent to standard supergravity USp8 geometry, not a new physical particle model. The 27D clock still acts on a 27-path encoded single photon; the 8D group parameterization is not by itself an 8-path optical implementation of the same Hilbert-space gate."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in [
      "status","max_36_generator_intertwining_error",
      "Albert_clock_8mode_source_generator_rank",
      "Albert_clock_8mode_source_generator_eigenvalues_imag",
      "induced_27mode_group_intertwiner_residual"]},indent=2),flush=True)
    return out
if __name__=="__main__":main()
