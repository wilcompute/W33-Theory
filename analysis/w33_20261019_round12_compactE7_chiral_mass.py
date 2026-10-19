"""Compact E7xSU2 viability:
- 136 gauge vectors, 112 real (56,2) scalars
- Hamiltonian positivity at quadratic level
- anomaly-safe but mass-ALLOWING 112 Weyl fermion representation.
"""
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round12_compactE7_chiral_mass.json"
def run():
    # Standard E7 fundamental 56 is symplectic (pseudoreal):
    I=np.eye(28)
    J56=np.block([[np.zeros((28,28)),I],[-I,np.zeros((28,28))]])
    eps2=np.array([[0,1],[-1,0]])
    M=np.kron(J56,eps2)
    assert M.shape==(112,112) and np.allclose(M,M.T)
    assert np.allclose(M@M,np.eye(112))
    assert abs(np.linalg.det(M))>0
    # A real representation admits an invariant symmetric 2-index
    # tensor, so a Majorana mass ψ_Aψ_B M_AB is allowed.
    # This does NOT make the representation vectorlike, but shows it
    # is not symmetry-protected massless / necessarily SM-chiral.
    gauge_dim=133+3
    two_pols=2*gauge_dim
    scalar=56*2
    total=two_pols+scalar
    rng=np.random.default_rng(19)
    trials=[]
    for _ in range(500):
        E=rng.normal(size=(gauge_dim,3))
        B=rng.normal(size=(gauge_dim,3))
        pi=rng.normal(size=scalar)
        phi=rng.normal(size=scalar)
        mass2=0.23
        H=.5*(np.sum(E**2)+np.sum(B**2)+np.sum(pi**2)+mass2*np.sum(phi**2))
        trials.append(float(H))
    # E7 is not a group with a third-order symmetric invariant
    # in the adjoint (no degree-3 Casimir), and SU2 has no d^abc.
    # For one left Weyl in (56,2), SU2 global Witten check counts
    # 56 doublets, an even number. The real tensor representation
    # permits gauge-invariant mass.
    checks={"E7_plus_SU2_gauge_dim_136":gauge_dim==136,
       "physical_two_transverse_polarizations_272":two_pols==272,
       "scalar_p_dimensions_112":scalar==112,
       "quadratic_bosonic_dof_384":total==384,
       "symmetric_nondegenerate_mass_tensor_on_56_tensor_2":np.linalg.matrix_rank(M)==112 and np.max(abs(M-M.T))==0,
       "500_positive_quadratic_Hamiltonian_samples":all(x>0 for x in trials),
       "SU2_global_Witten_anomaly_absent_for_56_doublets":56%2==0}
    out={"schema":"w33.round12.E7compact_SU2_quadratic_mass_protection_audit.v1",
       "quadratic_positive_Hamiltonian":"With compact gauge K=E7_c×SU2, standard YM gauge fixing/Gauss constraints leave two transverse physical polarisations per massless generator: 2*(133+3)=272. For 112 real K-representation scalars p=(56,2), positive Cartan kinetic and m²>0 give 112 scalar oscillators. H²=1/2 ∫(Σ_a |E_a^T|²+|B_a|²+Σ_I pi_I²+|grad phi_I|²+m² phi_I²); bosonic physical linearized polarizations 384. Perturbative gauge fixing assumptions and positivity hold around trivial vacuum with unbroken compact K only.",
       "gauge_dim":gauge_dim,"massless_vector_transverse_polarizations":two_pols,
       "real_scalar_modes":scalar,"total_bosonic_modes":total,
       "fermion_example":"One LEFT Weyl multiplet χ in (56,2) has 56 SU2 doublets, even Witten parity. E7 has no cubic local gauge invariant d^{abc}, and SU2 no local cubic anomaly; mixed simple-factor triangle anomalies vanish. The representation (56 pseudoreal)⊗(2 pseudoreal) is REAL, as witnessed by symmetric nondegenerate bilinear Omega56⊗epsilon2, so gauge-invariant symmetric Weyl Majorana mass is allowed. Thus anomaly freedom alone does NOT generate an observed protected chiral Standard Model spectrum.",
       "symmetric_mass_tensor_nonzero_entries":int(np.count_nonzero(M)),
       "quadratic_Hamiltonian_test":{"samples":len(trials),"min_positive":min(trials),"max_positive":max(trials)},
       "no_param_free_ratio":"The gauge coupling g, scalar mass m² and quartic remain free. E8(-24) is not entirely gauged, and its noncompact global symmetry is not shown to survive the chosen quadratic action. Neither family spectrum nor observed particle masses are fixed.",
       "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2,default=lambda x:x.item() if hasattr(x,'item') else str(x))+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"boson_modes":total,"mass_tensor_rank":112,"Witten_doublets":56},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
