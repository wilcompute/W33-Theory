#!/usr/bin/env python3
"""Quantitative affine symmetry stability + exact W33 H1 momentum completion.

Mathematical/conditional only. Neither H1 nor graph eigenmodes are identified with photons.
"""
from __future__ import annotations
import argparse,itertools,json,math
from collections import Counter
from pathlib import Path
import numpy as np

V=list(itertools.product(range(3),repeat=3))
IDX={x:i for i,x in enumerate(V)}
DIRS=((1,0,0),(0,0,1),(1,1,1),(1,2,1))
PRIMES=(3,5,7,11,13,17)

def prime(p):return p>1 and all(p%d for d in range(2,math.isqrt(p)+1))

def robust_affine():
    records=[]
    for q in PRIMES:
        assert prime(q) and q%2
        coeff=[1,(q-1)//2,(q-1)//2,
               -q if q%4==1 else 0,-q if q%4==3 else 0]
        bound=sum(abs(x) for x in coeff)/q**3
        target=q**(-1.5)
        delta=max(0.,target-bound)
        record=dict(prime=q,five_orbit_coefficients=coeff,
           contraction_commutant_amplitude_upper=bound,
           flat_amplitude=target,
           guaranteed_operator_norm_twirl_defect_if_flat=delta,
           guaranteed_max_group_commutator_if_flat=delta,
           max_symmetric_output_probability=bound**2,
           exact_flat_output_probability=q**-3,
           forbidden_if_fully_affine_covariant=q>=5)
        assert abs(bound-2/q**2)<1e-15
        assert (delta>0)==(q>=5)
        records.append(record)
    return {"status":"RIGOROUS_STABLE_AFFINE_OBSTRUCTION",
      "theorem":"For odd prime power q>=5 and any exactly flat unitary U on Sym2(Fq), with G=Fq^3 rtimes GL2(q), the group twirl T(U)=avg_g R_g U R_g^-1 obeys ||U-T(U)||_op >= delta_q=q^(-3/2)-2/q^2 >0, and sup_g ||[U,R_g]||_op >= delta_q.",
      "proof":"T(U) is a contraction commuting with G. Translation diagonalization and five dual GL2 orbits give |T(U)_(0,d)|<=2/q^2 for d=(0,1,0), even if the Fourier orbit scalars are not unit modulus. Flatness gives |U_(0,d)|=q^-3/2. Reverse triangle inequality bounds the entry, hence the operator norm. Also ||U-T(U)||<=sup_g||U-R_g U R_g^-1||.",
      "hamiltonian_version":"If U=e^(-itH), and H is bounded self-adjoint, then sup_g||[H,R_g]||_op >= delta_q/|t| for t nonzero, because the Duhamel integral bounds ||[U,R_g]||<=|t| ||[H,R_g]||.",
      "approximate_flatness":"If a unitary has |U_(0,d)|>=q^-3/2-epsilon, replace delta_q by max(0,delta_q-epsilon).",
      "scope":"Operator-norm finite-symmetry witness, not a physical coupling, emergent Lorentz invariant action or new measurement.",
      "cases":records}

def p5_chirp_twirl():
    """Actual Lorentz-congruence escape: quantify broken full-affine covariance."""
    p=5
    a,b,c=np.indices((p,p,p),dtype=int)
    q=(a*c-b*b)%p
    kernel=np.exp(2j*np.pi*q/p)/p**1.5
    lam=np.fft.fftn(kernel)
    assert np.max(abs(abs(lam)-1))<1e-12
    u,v,w=np.indices((p,p,p),dtype=int)
    dual=(u*w-pow(4,-1,p)*v*v)%p
    zero=(u==0)&(v==0)&(w==0)
    null=(dual==0)&~zero
    sq=sorted({i*i%p for i in range(1,p)})
    rankone_square=np.isin(u,sq)|((u==0)&np.isin(w,sq))
    masks=[zero,null&rankone_square,null&~rankone_square,
           (dual!=0)&np.isin(dual,sq),(dual!=0)&~np.isin(dual,sq)]
    assert [int(z.sum()) for z in masks]==[1,12,12,60,40]
    means=[np.mean(lam[m]) for m in masks]
    twirled_lam=np.zeros_like(lam)
    for m,z in zip(masks,means):twirled_lam[m]=z
    coeff=[1,2,2,-5,0]
    twirled_entry=sum(z*c for z,c in zip(means,coeff))/p**3
    raw_entry=kernel[0,1,0]
    op_norm=float(np.max(abs(lam-twirled_lam)))
    entry_difference=float(abs(raw_entry-twirled_entry))
    delta=p**-1.5-2/p**2
    assert abs(twirled_entry)<2/p**2+1e-12
    assert op_norm>=entry_difference>=delta-1e-12
    assert abs(op_norm-math.sin(2*math.pi/5))<1e-12
    # A different GL2-invariant *unitary involution* exactly saturates the
    # amplitude ceiling at this selected port. Saturation is not flat mixing.
    signs=[1 if c>=0 else -1 for c in coeff]
    sat_spectrum=np.zeros_like(lam)
    for m,z in zip(masks,signs):sat_spectrum[m]=z
    sat_kernel=np.fft.ifftn(sat_spectrum)
    sat_amplitude=float(abs(sat_kernel[0,1,0]))
    assert np.max(abs(abs(sat_spectrum)-1))<1e-12
    assert np.max(abs(sat_kernel.imag))<1e-12
    assert abs(sat_amplitude-2/p**2)<1e-12
    return {"status":"FULL_AFFINE_TWIRL_OF_EXPLICIT_P5_LORENTZ_CHIRP",
      "group_orbit_dimensions":[int(m.sum()) for m in masks],
      "original_flat_amplitude":float(abs(raw_entry)),
      "twirled_selected_amplitude":float(abs(twirled_entry)),
      "selected_entry_twirl_difference":entry_difference,
      "full_operator_norm_twirl_difference":op_norm,
      "exact_norm_twirl_difference":"sin(2*pi/5)",
      "general_proven_minimum":delta,
      "affine_invariant_involution_selected_amplitude":sat_amplitude,
      "selected_output_bound_is_sharp_among_affine_invariant_unitaries":True,
      "saturating_involution_is_flat":False,
      "interpretation":"The index-two determinant-isometry Gaussian clock is exactly flat but fails full GL2 congruence; its large orbit-twirl difference demonstrates concrete symmetry breaking, not a locality solution."}

def momentum_bundle():
    rank={}
    eig={}
    for k in V:
        perpendicular=sum(sum(k[i]*d[i] for i in range(3))%3==0 for d in DIRS)
        val=4-perpendicular-(k!=(0,0,0))
        rank[k]=int(val)
        eig[k]=3*perpendicular-4
        assert (5-eig[k])//3+(k==(0,0,0))==val
    assert Counter(rank.values())==Counter({0:1,1:12,2:8,3:6})
    assert Counter(eig.values())==Counter({8:1,2:12,-1:8,-4:6})
    A=np.zeros((27,27),dtype=int)
    for i,x in enumerate(V):
        for j,y in enumerate(V):
            if i!=j and ((x[0]-y[0])*(x[2]-y[2])-(x[1]-y[1])**2)%3==0:
                A[i,j]=1
    assert np.all(A==A.T) and np.all(A.sum(axis=1)==8)
    I=np.eye(27,dtype=int)
    P=((8*I-A)@(A+I)@(A+4*I))/108
    assert abs(np.trace(P)-12)<1e-12
    assert np.max(abs(P@P-P))<1e-12
    assert np.max(abs(P@A-2*P))<1e-12
    # Exact integer kernel: 108*P, grouped by its convolution displacement.
    kernel_counts=Counter(int(round(9*P[0,j])) for j in range(27))
    assert kernel_counts==Counter({-1:12,0:6,1:8,4:1})
    null_edges=[j for j in range(1,27) if A[0,j]==1]
    assert len(null_edges)==8 and all(abs(P[0,j]-1/9)<1e-12 for j in null_edges)
    # Independently test momentum multipliers of a 27x27 translation-equivariant projector.
    zeta=np.exp(2j*np.pi/3)
    for k in V:
        psi=np.array([zeta**(sum(k[d]*x[d] for d in range(3))%3)
                      for x in V],complex)
        assert np.max(abs(P@psi-(1 if rank[k]==1 else 0)*psi))<1e-11
    # At each momentum k!=0 a rank-two subbundle needs max(0,2-h(k))
    missing={str(k):max(0,2-rank[k]) for k in V if k!=(0,0,0)}
    minimum=sum(missing.values())
    assert minimum==12
    assert 46+minimum==58
    # A uniformly added on-site scalar contributes one character at each momentum.
    # No nonzero 12-dimensional on-site species can be uniform over all 27 sites.
    return {"status":"EXACT_SPECTRAL_H1_POLARIZATION_CAPACITY_OBSTRUCTION",
      "vertices":27,"null_graph_degree":8,"h1_dimension":46,
      "adjacency_eigenvalue_multiplicities":{str(k):v for k,v in sorted(Counter(eig.values()).items())},
      "h1_momentum_rank_multiplicities":{str(k):v for k,v in sorted(Counter(rank.values()).items())},
      "identity":"For momentum k!=0, h1(k)=(5-lambda_A(k))/3; h1(0)=0. Sum h1=46.",
      "rank_two_every_nonzero_momentum_possible_with_H1_alone":False,
      "momentum_rank_deficit_for_two_polarizations":minimum,
      "minimal_selective_auxiliary_dimension":minimum,
      "minimum_completed_H1_dimension":58,
      "rank_two_nonzero_momentum_subbundle_dimension":52,
      "remaining_modes_after_minimal_completion":6,
      "onsite_uniform_scalar_auxiliary_dimension":27,
      "deficient_orbit_spectral_projector":"P_2=(8I-A)(A+I)(A+4I)/108, an exact rank-12 orthogonal projector",
      "deficient_orbit_projector_convolution_kernel_9x_values":{str(k):v for k,v in sorted(kernel_counts.items())},
      "spatial_kernel_nonzero_displacement_types":20,
      "graph_distance_upper_bound_for_polynomial":3,
      "physical_boundary":"H1 finite cohomology is not the space of physical Maxwell radiative modes. This is a conditional no-go ONLY if one assumes a rank-two polarization bundle contained entirely in H1 over every nonzero translation momentum."}

def produce():
    return {"schema":"w33.20261108.stability_hodge_completion.v1",
      "robust_affine":robust_affine(),
      "p5_isometry_chirp":p5_chirp_twirl(),
      "h1_bundle":momentum_bundle(),
      "prior_owners":["analysis/PASS20261108_AFFINE_COVARIANCE_NO_GO.md",
       "analysis/w33_20261108_lorentz_chirp_escape.py",
       "analysis/PASS20261108_S4_HARMONIC_QDUAL.md"],
      "status":"TWO_EXACT_THEOREMS_PLUS_P5_SYMMETRY_TWIRL_NUMERICAL_CROSSCHECK",
      "scientific_boundary":"Finite representation theory and group-averaging inequalities; no empirically verified TOE, physical photon identification or derived constants."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=Path("data/w33_20261108_stability_hodge_completion.json"))
    x=p.parse_args();d=produce();x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"p5_symmetry_defect":d["p5_isometry_chirp"]["full_operator_norm_twirl_difference"],
      "q5_minimum_defect":d["robust_affine"]["cases"][1]["guaranteed_operator_norm_twirl_defect_if_flat"],
      "h1_rank_classes":d["h1_bundle"]["h1_momentum_rank_multiplicities"],
      "minimal_auxiliary":d["h1_bundle"]["minimal_selective_auxiliary_dimension"]}))
if __name__=="__main__":main()
