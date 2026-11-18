"""Twist-vs-Higgs compatibility falsifier for the new linked-wire H27xC2xC7
construction (parallel commit 36eb8d9) and the earlier 78+27bar+27
F/D-flat E6 singlet vacuum (commit 4a5bc06).

Key distinction: a C2 holonomy acting as (-1)^Chi on all E6 multiplets
prevents TWO of three selected singlet VEVs being COVARIANTLY PARALLEL.
An independent flavor C2 acting only on fermion multiplets has no such
automatic consequence, but then needs a separate physical flavor bundle.
"""
import json,math
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
def run():
    # Exact source charges ordered (Chi,Psi), natively verified by the
    # earlier E6 78+bar27+27 singlet algebra.
    weights=[(-5,-3),(5,-1),(0,4)]
    Q=s.Matrix(2,3,[v for row in range(2) for v in [w[row] for w in weights]])
    assert Q*s.ones(3,1)==s.zeros(2,1)
    full=Q*Q.T
    assert full==s.Matrix([[50,10],[10,26]]) and full.det()==1200
    chi_parity=[(-1)**(abs(chi)%2) for chi,psi in weights]
    assert chi_parity==[-1,-1,1]
    allowed=[j for j,p in enumerate(chi_parity) if p==1]
    restricted=Q[:,allowed]
    gauge_rank=int(restricted.rank())
    assert gauge_rank==1
    # Even under Chi parity only z can be a parallel nonzero VEV,
    # but D_psi proportional to +4|z|² cannot vanish with zero FI.
    surviving_charges=[weights[j] for j in allowed]
    assert surviving_charges==[(0,4)]
    fixed_weighted_Dflat_nonzero_exists=False
    # The order-seven SU5 Wilson diag(zeta7^2 x3, zeta7^4 x2)
    # acts trivially on all three SU5 singlets.
    wilson_SU5_determinant_exp=(3*2+2*4)%7
    assert wilson_SU5_determinant_exp==0
    # Two odd-charge condensates are anti-periodic around the
    # holonomy generator with physical circle length ell; flat
    # unitary covariant Laplacian has min eigenvalue pi²/ell².
    ell=s.symbols("ell",positive=True)
    k=s.symbols("k",integer=True)
    twisted=(2*s.pi*(k+s.Rational(1,2))/ell)**2
    untwisted=(2*s.pi*k/ell)**2
    assert s.simplify(twisted.subs(k,0)-s.pi**2/ell**2)==0
    assert untwisted.subs(k,0)==0
    out=dict(status="PASS",source_commit_wire="36eb8d951d1a",source_commit_native_E6="4a5bc06a2994",
       charges_Chi_Psi=[list(w) for w in weights],
       global_Chi_pi_holonomy_singlet_eigenvalues=chi_parity,
       W7_SU5_singlet_eigenvalues=[1,1,1],
       full_D_term_charge_Gram=[[int(v) for v in row] for row in full.tolist()],
       full_D_term_charge_rank=int(Q.rank()),
       full_D_term_charge_determinant=int(full.det()),
       Chi_parity_invariant_singlet_index=allowed,
       Chi_parity_invariant_D_term_charge_rank=gauge_rank,
       Chi_parity_invariant_Dflat_nonzero_solution_with_zero_FI=fixed_weighted_Dflat_nonzero_exists,
       independent_unitary_C2_flavor_possible_without_acting_on_Higgs=True,
       odd_singlet_loop_covariant_laplacian_gap="pi^2 / ell^2 for flat constant-radius loop of length ell and holonomy -1",
       invariant_singlet_loop_covariant_laplacian_gap="0",
       logical_conclusion="If the SAME finite C2 is identified with the native E6 Chi-parity gauge twist for ALL Higgs multiplets and the three Higgs VEVs are required to be covariantly parallel, x and y cannot condense; only z remains invariant, yielding rank1 U1 Higgsing and no nonzero zero-FI D-flat solution in the specified three-field set. Thus the linked-wire mirror-free C2 twist does NOT automatically coexist with the earlier global parallel 2-U1 Higgs vacuum.",
       loopholes="Distinct flavor-only C2 (separate gauge bundle), nonparallel/delocalized Higgs section with holonomy gradient energy, nonzero FI/flux or extra fields, spatially varying monodromy/defects, Wilson + Higgs changing global solutions. A complex line over S1 with -1 flat holonomy can possess nonvanishing but NONPARALLEL sections, so no general topological impossibility theorem.",
       anomalous_extra_U1_caution="Higgsing an anomalous Abelian gauge factor does not cure a 4D gauge anomaly by itself: quantized inflow/Green-Schwarz/counterterms or additional chiral matter still required.",
       scope="This is an exact necessary compatibility check under explicitly identified Chi C2 and parallel-Higgs hypotheses, NOT a claim the parallel linked-wire topology is wrong or a solved full G2 compactification.")
    f=ROOT/"data/toe_20261118_linked_wire_chi_twist_Higgs_global_compatibility.json"
    f.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS C2 Chi parity forces two native E6 Higgs singlets nonparallel; invariant charge rank drops 2->1; winding gradient gap pi²/ell²")
    return out
if __name__=="__main__":run()
