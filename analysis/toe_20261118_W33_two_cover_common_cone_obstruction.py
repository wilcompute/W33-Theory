"""Compare two previously computed W33 three-periodic Bloch tensors.

The 81-chord optimum and PSp symmetry-breaking obstruction are PRIOR ART
in repo f495122c. This pass quantifies a potential COMMON-CONE problem:
different noncanonical voltage choices yield nonproportional spatial
quadratic forms in a fixed shared deck coordinate system.
"""
import json,numpy as np
from scipy.linalg import eigh
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run():
    M_old=np.array([[81,-27,9],[-27,81,-3],[9,-3,81]],float)
    M_opt=np.array([[81,1,1],[1,81,1],[1,1,81]],float)
    Dold=M_old/12800;Dopt=M_opt/12800
    eo=np.linalg.eigvalsh(M_old);en=np.linalg.eigvalsh(M_opt)
    assert np.max(abs(en-np.array([80,80,83])))<1e-10
    assert np.min(eo)>0
    # Same nominal time normalization and same shared deck labels:
    # square of low-wave velocity is directional κ n.T D n.
    ratios=eigh(M_old,M_opt,eigvals_only=True)
    assert ratios[0]>0 and ratios[-1]/ratios[0]>1.01
    fixed_basis_velocity_min=float(np.sqrt(ratios[0]))
    fixed_basis_velocity_max=float(np.sqrt(ratios[-1]))
    # A single species cannot establish physical anisotropy because
    # any SPD D can be removed by a real spatial linear rescaling.
    # But the same linear coordinate change cannot make two *different*
    # D matrices proportional unless they already were.
    s=float(np.trace(Dold)/np.trace(Dopt))
    residual=float(np.linalg.norm(Dold-s*Dopt,ord="fro"))
    assert residual>1e-3
    # Quantify old-vs-optimized cones on easy deck directions.
    samples=[]
    for lab,v in (("x",(1,0,0)),("y",(0,1,0)),("z",(0,0,1)),
                  ("x+y",(1,1,0)),("x-y",(1,-1,0)),("x+z",(1,0,1)),
                  ("x+y+z",(1,1,1))):
        a=np.array(v,float);a/=np.linalg.norm(a)
        ratio=float(np.sqrt((a@Dold@a)/(a@Dopt@a)))
        samples.append(dict(direction=lab,old_to_optimized_speed_ratio=ratio))
    out=dict(status="PASS",old_tensor_numerator=M_old.astype(int).tolist(),
        optimized_tensor_numerator=M_opt.astype(int).tolist(),common_denominator=12800,
        old_eigenvalues=eo.tolist(),optimized_eigenvalues=en.tolist(),
        old_within_species_spatial_speed_anisotropy=float(np.sqrt(eo[-1]/eo[0])),
        optimized_within_species_spatial_speed_anisotropy=float(np.sqrt(en[-1]/en[0])),
        generalized_old_vs_optimized_speed_squared_eigenvalues=ratios.tolist(),
        old_to_optimized_relative_velocity_range_fixed_deck_basis=[fixed_basis_velocity_min,fixed_basis_velocity_max],
        least_trace_matched_proportionality_constant=s,
        nonproportional_Frobenius_residual=residual,
        samples=samples,
        common_cone_condition="If two field species propagate on these respective voltage covers with same low-energy time normalization and physically IDENTIFIED deck spatial coordinates, a common effective Lorentzian spatial metric requires D_old proportional D_opt. They are not proportional; the relative propagation cone varies by direction.",
        cautions="This is a conditional 2-species toy comparison, NOT measured Lorentz violation or gravity. A single SPD D admits linear spatial rescaling to isotropy. Distinct voltage labels need not define a physical shared coordinate frame; a deck GL3Z identification and actual microscopic coupling must be specified. The optimized tensor and 3D no-go already appear in earlier 2026-11-18 repo work."
    )
    file=ROOT/"data/toe_20261118_W33_two_cover_common_cone_obstruction.json"
    file.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS W33 old vs optimized 3D spatial tensors, nonproportional 2-species relative dispersion, fixed basis cone spread",fixed_basis_velocity_min,fixed_basis_velocity_max)
    return out
if __name__=="__main__":run()
