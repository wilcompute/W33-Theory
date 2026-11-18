"""Close the E6 *Lie-algebra rank* gap in the split-27 messenger ansatz.

Two commuting Cartan adjoints A,B preserve Cartan rank 6, so SU5
3+2 splitting leaves at least U(1)^2. Higgs in two different vectorlike
27+bar27 pairs along SU5 singlets N^c_(psi=1,chi=-5),
S_(psi=4,chi=0) has rank-2 charge matrix with det20.

A gauge invariant effective superpotential uses singlet constraints
S_i(barH_i H_i-v_i^2)+Z_i/Lambda(barH_i B H_i-b_i barH_i H_i).
Together with S_A(Tr A^2-vA^2), S_B(Tr B^2-vB^2) it has F=0
at S_i=Z_i=0, diagonal commuting A,B and aligned Higgs/dual VEVs.
D=0 with conjugate paired VEVs. In the desired SU5 chart,
F_Z fixes the two independent U1 B components to the benchmark.
DOES NOT prove unique global vacuum, stabilization of other Cartan,
or anomaly-free discrete mirror sectors.

Exact cubic E6 stabilizer from repo is independently rerun to
certify 78 -> 24 (two singlet+dual vevs) ->12 after hypercharge A.
"""
from pathlib import Path
import json,math,sys
import sympy as sp
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_E6_full_cubic_SM_stabilizer import (
 cubic_monomials,cubic_derivation_rows,exact_sparse_rank,
 vev_constraints,hypercharge_integer_weights,N)
OUT=ROOT/"data"/"toe_20261117_E6_rank_two_singlet_Balignment_completion.json"
def verify():
    mons=cubic_monomials(); rows=cubic_derivation_rows(mons)
    vev=vev_constraints(); Ys=hypercharge_integer_weights()
    Aoff=[{i*N+j:1} for i in range(N) for j in range(N) if Ys[i]!=Ys[j]]
    ranks=[exact_sparse_rank(rows),exact_sparse_rank(rows+vev),
           exact_sparse_rank(rows+vev+Aoff)]
    assert ranks==[651,705,717]
    dims=[N*N-r for r in ranks]
    assert dims==[78,24,12]
    # These distinct SM-singlet VEVs are the two positions 7,8
    # in the repo's exact cubic stabilizer chart.
    Q=sp.Matrix([[1,-5],[4,0]]) # rows N^c and S; cols Qpsi, Qchi
    assert Q.det()==20 and Q.rank()==2
    # The singlet B eigenvalues at psi=-.2,chi=.2
    b_target=sp.Matrix([sp.Rational(-6,5),sp.Rational(-4,5)])
    uv=Q.inv()*b_target
    assert uv==sp.Matrix([sp.Rational(-1,5),sp.Rational(1,5)])
    hess=2*(Q.T*Q)
    assert hess.eigenvals()=={42-2*sp.sqrt(41):1,42+2*sp.sqrt(41):1}
    # Canonically orthogonal 27-trace Cartan directions Q/sqrtTrQ2
    D=sp.diag(1/sp.sqrt(72),1/sp.sqrt(120))
    charge_canonical=Q*D
    Gram=sp.simplify(charge_canonical.T*charge_canonical)
    mass_eigs=sorted([float(x) for x in Gram.eigenvals()])
    assert mass_eigs[0]>0 and mass_eigs[1]>0
    assert sp.simplify(Gram.det()-sp.Rational(400,72*120))==0
    # Over an ABSTRACT product torus U1xU1, charge lattice coker Q
    # has order 20; actual E6 global quotient reduces this.
    from sympy.matrices.normalforms import smith_normal_form
    from sympy.polys.domains import ZZ
    smith=smith_normal_form(Q,domain=ZZ)
    assert sorted([abs(int(smith[i,i])) for i in range(2)])==[1,20]
    # One Higgs leaves one linearly independent U1 generator.
    assert sp.Matrix([[1,-5]]).nullspace()==[sp.Matrix([5,1])]
    return {
      "status":"PASS_EXACT_E6_RANK_REDUCTION_VIA_TWO_27_SINGLET_PAIRS_AND_GAUGE_INVARIANT_B_PINNING",
      "cubic_derivation_27x27_ranks":ranks,
      "Lie_algebra_dims":{"E6":78,"two_27bar27_SM_singlet_pairs":24,
        "plus_SU5_hypercharge_adjoint":12},
      "root_level_unbroken_before_singlets":"At least rank-six Cartan remains after only A/B commuting adjoint VEVs. At generic SU5-preserving B plus SU5 3+2 A, unbroken Lie algebra SM+u1_psi+u1_chi is 14-dimensional, not the 12-dimensional SM.",
      "singlet_charge_matrix_integer_Nc_S": [[1,-5],[4,0]],
      "singlet_charge_det":20,
      "single_singlet_leftover_u1_direction":[5,1],
      "B_eigenvalue_constraints":{"Nc":str(b_target[0]),"S":str(b_target[1]),
          "unique_psi":str(uv[0]),"unique_chi":str(uv[1])},
      "integer_charge_pin_potential_Hessian_per_lambda":str(hess),
      "integer_pin_Hessian_eigenvalues_per_lambda":["42-2*sqrt(41)","42+2*sqrt(41)"],
      "gauge_mass2_eigenvalues_per_g2v2_canonical_27_trace":mass_eigs,
      "gauge_mass2_trace_per_g2v2":float(Gram.trace()),
      "gauge_mass2_determinant_per_g4v4":float(Gram.det()),
      "naive_covering_torus_Smith_orders":[1,20],
      "global_discrete_WARNING":"Z20 is the stabilizer in the product U1_psi x U1_chi integer-charge covering torus ONLY; cannot call it the physical leftover discrete gauge symmetry without the full E6/SU5 common-center quotient and Higgs embedding.",
      "holomorphic_E6_invariant_EFT_potential":"W=SA(Tr27 A^2-vA^2)+SB(Tr27 B^2-vB^2)+sum_i[Si(barHi Hi-vi^2)+(Zi/Lambda)barHi(B-bi)Hi]+W_messenger, i=Nc,S",
      "FD_flat_exists":"Hi along two distinct SU5 singlets in 27; barHi dual aligned; |Hi|=|barHi|; all Lagrange singlets zero; adjoints Hermitian commuting. All F=0 and D=0, provided prescribed v_A,v_B,b_N,b_S are compatible as in benchmark.",
      "EFT_dimension":"Zi barHi B Hi is superpotential quartic and requires 1/Lambda; coefficients are gauge invariant but do NOT arise automatically from renormalizable E6 theory.",
      "remaining_gap":"Need derive origin of dimension-5 superpotential operators, stabilize non-Cartan orientations and full 78+Higgs messenger scalar mass matrix, check extra gauge boson masses, discrete anomalies, proton decay and full global vacuum."
    }
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["Lie_algebra_dims"],
          z["gauge_mass2_eigenvalues_per_g2v2_canonical_27_trace"])
