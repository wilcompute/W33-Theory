#!/usr/bin/env python3
"""Odd-prime Lorentz Gaussian clock has a constant-depth generalized-Clifford compiler.

Separates exact logical qupit gate count from nonlocal physical rail routing.
"""
from __future__ import annotations
import argparse,itertools,json,math
from pathlib import Path
import numpy as np

PRIMES=(3,5,7,11,13,17)

def chirp_port(p,sigma):
    w=np.exp(2j*np.pi/p)
    phase=np.array([w**(sigma*j*j%p) for j in range(p)])
    D=np.diag(phase)
    F=np.array([[w**((-2*sigma*i*j)%p)/math.sqrt(p)
                 for j in range(p)] for i in range(p)])
    H=np.array([[w**(sigma*(i-j)**2%p)/math.sqrt(p)
                 for j in range(p)] for i in range(p)])
    factor_err=float(np.max(abs(H-D@F@D)))
    unit_err=float(np.max(abs(H@H.conj().T-np.eye(p))))
    assert factor_err<1e-12 and unit_err<1e-12
    return H,dict(sign=sigma,gaussian_port_unitarity_error=unit_err,
       quadratic_phase_Fourier_factorization_error=factor_err,
       circuit="H_sigma = D_sigma F_(-2sigma) D_sigma; two quadratic phase gates and one scaled Fourier gate")

def pauli_clifford(p,H):
    """Check H normalizes generalized Pauli generators X,Z."""
    w=np.exp(2j*np.pi/p)
    X=np.zeros((p,p),complex)
    for j in range(p):X[(j+1)%p,j]=1
    Z=np.diag([w**j for j in range(p)])
    basis=[np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b)
           for a in range(p) for b in range(p)]
    results=[]
    for label,pauli in [("X",X),("Z",Z)]:
        conjugate=H@pauli@H.conj().T
        overlaps=np.array([np.trace(B.conj().T@conjugate)/p for B in basis])
        best=int(np.argmax(abs(overlaps)))
        residual=float(np.max(abs(conjugate-overlaps[best]*basis[best])))
        assert residual<1e-11 and abs(abs(overlaps[best])-1)<1e-11
        results.append({"generator":label,
           "image_X_exponent":best//p,"image_Z_exponent":best%p,
           "phase_real":float(overlaps[best].real),
           "phase_imag":float(overlaps[best].imag),
           "max_matrix_residual":residual})
    return results

def coordinates(p,v):
    inv2=pow(2,-1,p)
    a,b,c=v
    c1=(c-a)%p                            # SUM c<-c-a
    t=(a+inv2*c1)%p                     # SUM a<-a+c1/2
    x=(-inv2*c1)%p                      # local multiplier c<-(-1/2)c
    assert (t,x)==(inv2*(a+c)%p,inv2*(a-c)%p)
    # Inverse: c<-(-2)c, a<-a-c/2, c<-c+a; each modulo p
    cback=(-2*x)%p
    aback=(t-inv2*cback)%p
    cfinal=(cback+aback)%p
    assert (aback,b,cfinal)==(a,b,c)
    return t,b,x

def certify(p):
    assert p>2 and all(p%d for d in range(2,math.isqrt(p)+1))
    inv2=pow(2,-1,p)
    Hplus,plus=chirp_port(p,1)
    Hminus,minus=chirp_port(p,-1)
    plus_actions=pauli_clifford(p,Hplus)
    minus_actions=pauli_clifford(p,Hminus)
    n=p**3
    grid=np.indices((p,p,p)).reshape(3,-1).T
    transformed=np.array([coordinates(p,tuple(map(int,v))) for v in grid])
    assert len({tuple(v) for v in transformed})==n
    u=grid
    t,b,x=transformed.T
    target=np.exp(2j*np.pi*((u[:,0]*u[:,2]-u[:,1]**2)%p)/p)/math.sqrt(n)
    compiled=Hplus[t,0]*Hminus[b,0]*Hminus[x,0]
    err=float(np.max(abs(target-compiled)))
    assert err<1e-12
    # Translation-invariant quadratic kernel: verifying every displacement is
    # sufficient for the entire n*n matrix because the coordinate map is linear.
    # Explicitly cross-check a fixed independent sample of nonzero input pairs.
    rng=np.random.default_rng(20261108+p)
    pairs=rng.integers(0,n,size=(min(4096,n*n),2))
    ij=u[pairs]
    dif=(ij[:,0,:]-ij[:,1,:])%p
    ijnew=transformed[pairs]
    tt=(ijnew[:,0,:]-ijnew[:,1,:])%p
    desired=np.exp(2j*np.pi*((dif[:,0]*dif[:,2]-dif[:,1]**2)%p)/p)/math.sqrt(n)
    actual=Hplus[tt[:,0],0]*Hminus[tt[:,1],0]*Hminus[tt[:,2],0]
    sampled=float(np.max(abs(desired-actual)))
    assert sampled<1e-12
    scaling_nontrivial=(-inv2)%p!=1
    assert scaling_nontrivial==(p!=3)
    # Three tensor-factor Gaussian gates; each is replicated p^2 times
    # when realized as p-mode transforms on p^3 physical rail labels.
    tritters=3*p*p
    local_upper=3*p*p*(p*(p-1)//2)
    generic=n*(n-1)//2
    return {"prime":p,"rails":n,
       "finite_field_coordinate_change":"t=(a+c)/2, transverse=b, x=(a-c)/2; det(a,b,c)=t^2-b^2-x^2",
       "two_forward_SUM_gates":2,"two_inverse_SUM_gates":2,
       "local_multiplier_forward":"(-1/2) on x",
       "local_multiplier_inverse":"(-2) on x",
       "nontrivial_local_multipliers":2 if scaling_nontrivial else 0,
       "quadratic_port_gates":[plus,minus],
       "local_port_Pauli_normalizer_certificates":{"H_plus":plus_actions,"H_minus":minus_actions},
       "full_kernel_difference_type_count":n,
       "full_kernel_from_factorization_max_residual":err,
       "independent_input_output_samples":len(pairs),
       "sample_pair_max_residual":sampled,
       "logical_SUM_count":4,
       "local_one_qupit_Gauss_gate_count":3,
       "if_expanded_local_quadratic_phase_gates":6,
       "if_expanded_local_Fourier_gates":3,
       "independent_rail_p_port_Gauss_units":tritters,
       "internal_generic_two_mode_upper_bound_without_routing":local_upper,
       "generic_n_rail_mesh_two_mode_bound":generic,
       "internal_upper_to_generic_mesh_ratio":local_upper/generic}

def produce():
    return {"schema":"w33.20261108.odd_prime_clifford_compiler.v1",
      "status":"EXACT_ODD_PRIME_GAUSSIAN_CLIFFORD_COMPILER_NUMERICALLY_VERIFIED",
      "theorem":"For every odd prime power q, the q^3-dimensional flat Gaussian kernel q^-3/2 psi(det(S-T)) is conjugate under an invertible 3-coordinate linear permutation to H_plus tensor H_minus tensor H_minus. Each H_sigma is D_sigma F_-2sigma D_sigma and is a generalized Clifford gate, as are the two forward and two inverse SUM gates and local coordinate multipliers. The whole clock is Clifford in the 3-qudit tensor factorization.",
      "fixed_prime_test_scope":"Explicit code tests primes 3,5,7,11,13,17; extension to odd prime powers follows finite-field arithmetic but has no extension-field implementation in this certificate.",
      "p3_special":"(-1/2)=1 modulo 3, so both local multipliers disappear. This recovers the previously-owned 27-mode four-SUM/27-tritter compiler up to a global phase.",
      "physics_limit":"Constant *logical* three-qudit gate count does not imply local propagation, constant physical photonic depth, or feasible loss. A Clifford circuit is not universal quantum computation by itself; non-Clifford resources and physically justified dynamics remain separate requirements.",
      "prior_owner":"papers/forty_points/sec04_time.tex explicitly identifies the 27-mode clock as Clifford. This contribution generalizes the concrete circuit and scaling to odd prime fields and counts local multipliers.",
      "cases":[certify(p) for p in PRIMES]}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--out",type=Path,default=Path("data/w33_20261108_odd_prime_clifford_compiler.json"))
    x=a.parse_args();d=produce();x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"prime_rails":[(x["prime"],x["rails"]) for x in d["cases"]],
      "p3_multipliers":d["cases"][0]["nontrivial_local_multipliers"],
      "p5_port_units":d["cases"][1]["independent_rail_p_port_Gauss_units"]}))
if __name__=="__main__":main()
