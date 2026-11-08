#!/usr/bin/env python3
"""Lorentz-type isometry subgroup restores a Gauss-flat quantum clock at odd p."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import numpy as np

def prime(p):return p>1 and all(p%d for d in range(2,math.isqrt(p)+1))

def certify(p):
    assert prime(p) and p%2
    a,b,c=np.indices((p,p,p),dtype=int)
    determinant=(a*c-b*b)%p
    K=np.exp(2j*np.pi*determinant/p)/math.sqrt(p**3)
    # Convolution U(x,y)=K(x-y). Unit-modulus Fourier eigenvalues prove unitarity.
    spectrum=np.fft.fftn(K)
    spectral_error=float(np.max(abs(abs(spectrum)-1)))
    assert spectral_error<1e-12
    h=np.fft.ifftn(-np.angle(spectrum))
    assert float(np.max(abs(h.imag)))<1e-12
    support=abs(h.real)>1e-9
    support[0,0,0]=False
    out_null=int(np.count_nonzero(support&(determinant!=0)))
    # The faithful congruence action is GL2/{+-I}; determinant^2=1
    # is a subgroup of index (p-1)/2, not the full group for p>=5.
    group=(p*p-1)*(p*p-p)
    group_isometric=2*group//(p-1)
    assert group//group_isometric==(p-1)//2
    # For the representative S=I, a diagonal G=diag(r,1) multiplies det by r^2.
    escaped=next((r for r in range(1,p) if r*r%p!=1),None)
    assert (escaped is None)==(p==3)
    if escaped is not None:
        old=np.exp(2j*np.pi/p)
        modified=np.exp(2j*np.pi*(escaped*escaped%p)/p)
        assert abs(old-modified)>1e-8
    return {
      "prime":p,"vertices":p**3,
      "chirp":"U(x,y)=p^-3/2 exp(2pi i det(x-y)/p)",
      "spectral_unitarity_error":spectral_error,
      "flat_probability":"1/p^3 for all p^6 ordered input/output pairs",
      "full_GL2_order":group,
      "determinant_pm1_isometry_subgroup_order":group_isometric,
      "minimal_symmetry_breaking_index_for_this_chirp":(p-1)//2,
      "isometry_symmetry_is_full_congruence":p==3,
      "GL2_nonisometric_example_diag_r":escaped,
      "principal_log_generator_nonzero_offdiagonal_displacements":int(support.sum()),
      "principal_log_generator_off_null_support":out_null,
      "principal_log_generator_is_nonlocal":out_null>0,
      "scope":"The principal spectral logarithm is a Hermitian generator but is not null-local; an alternate local logarithm remains a separate question."
    }

def produce():
    cases=[certify(p) for p in [3,5,7,11,13,17]]
    return {"schema":"w33.20261108.lorentz_isometry_chirp_escape.v1",
      "status":"EXACT_ISOMETRY_COVARIANT_UNIFORM_CHIRP_AND_NUMERICAL_FOURIER_CHECK",
      "theorem":"For any odd prime power q, K(S,T)=q^-3/2 psi(det(S-T)) is unitary because det is a nondegenerate quadratic form; it commutes with translations and with the GL2(q) determinant-pm1 congruence subgroup. That subgroup has index (q-1)/2 in GL2(q); at q=5 it is index two, the minimal possible proper subgroup index. Uniformity requires only the character sum, not a special measured constant.",
      "proof":"For S!=T, det(S-Z)-det(T-Z) is a nontrivial linear polynomial in Z plus a constant, because det is nondegenerate over odd characteristic. Character orthogonality makes distinct rows orthogonal; every entry has modulus q^-3/2. Congruence scales determinant by det(G)^2; requiring det(G)^2=1 fixes the polynomial. Full GL2 contains nonisometric similitudes when q>3.",
      "connection":"Sym2(Fq) has a 2+1 dimensional quadratic form of Lorentzian type. SL2(q) congruence transformations preserve it, analogous to SL2(R) spin covering SO+(2,1), but no physical continuum or propagation law follows.",
      "no_go_comparison":"Does not contradict the full-affine GL2 no-go, since full GL2 congruence is explicitly broken at q>3. Does not guarantee locality of the generator.",
      "cases":cases}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,default=Path("data/w33_20261108_lorentz_chirp_escape.json"))
    x=ap.parse_args();d=produce();x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"primes":[c["prime"] for c in d["cases"]],
     "indices":[c["minimal_symmetry_breaking_index_for_this_chirp"] for c in d["cases"]],
     "off_null":[c["principal_log_generator_off_null_support"] for c in d["cases"]]}))
if __name__=="__main__":main()
