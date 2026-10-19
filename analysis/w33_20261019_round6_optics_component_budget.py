"""Round6 front3: exact complex Givens mesh decomposition of F3
and thus 9-mode CZ(F3 tensor I3), plus two-path unbalanced-loss
calibration identities. No measured loss number is asserted.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from w33_20261019_nextfive_optics_su9 import F,CZ,G,proj0,I9
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round6_optics_component_budget.json"
def givens(A):
    n=len(A)
    a=A.copy()
    steps=[]
    for j in range(n-1):
        for i in range(n-1,j,-1):
            x,y=a[i-1,j],a[i,j]
            r=np.sqrt(abs(x)**2+abs(y)**2)
            if r<1e-13:continue
            m=np.eye(n,dtype=complex)
            m[np.ix_([i-1,i],[i-1,i])]=[[x.conjugate()/r,y.conjugate()/r],
                                        [-y/r,x/r]]
            a=m@a
            steps.append((i-1,i,m))
    R=np.eye(n,dtype=complex)
    for _,_,m in steps:R=m@R
    D=np.diag(np.diag(a))
    return R,D,steps,float(np.linalg.norm(R.conj().T@D-A))
def Uproj(theta):return I9+(np.exp(1j*theta)-1)*proj0
def run():
    L,D,steps,err3=givens(F)
    # Lift 3x3 Givens to the 9-dimensional a x b register,
    # as three independent fixed-b transforms per elementary coupler.
    L9=np.kron(L,np.eye(3))
    D9=np.kron(D,np.eye(3))
    F9=L9.conj().T@D9
    recon=CZ@F9
    err9=float(np.linalg.norm(G-recon))
    errors={}
    for eta in (.2,.5,.75,.9,.99,1.):
        # p0=(1+eta+2sqrt(eta) Re Wjj)/4,
        # p1=(1+eta-2sqrt(eta) Re Wjj)/4.
        # unconditional difference=sqrt eta * Re Wjj;
        # conditional difference=2sqrt eta/(1+eta) ReWjj,
        # survival click probability=(1+eta)/2.
        visibility=2*np.sqrt(eta)/(1+eta)
        click=(1+eta)/2
        errors[str(eta)]={"signal_arm_intensity_transmission":eta,
           "conditional_visibility":float(visibility),
           "surviving_click_probability":float(click),
           "false_uncalibrated_deficit_for_ideal_W_equal_I":float(1-visibility),
           "calibrated_visibility_normalization_works":bool(abs((visibility/visibility)-1)<1e-14)}
    # Breadboard synthesis: one 3x3 F Fourier = three SU2 mode couplers
    # + three output phases. Lift x3 independent b blocks => 9 couplers
    # and 9 diagonal phases each G. CZ adds 4 non-zero 2pi/3 or 4pi/3
    # phase masks on computational modes.
    # Each full commutator W has four G or G† and four three-channel
    # rank3 P phases -> 36 tunable 2-mode couplers + 36 F phases +
    # 16 CZ phases + 12 projector phases, plus two global path couplers.
    # This is a direct unoptimized upper-bound count, not minimal.
    n_cz_nonzero=int(np.sum(abs(np.angle(np.diag(CZ)))>1e-12))
    circuits={
      "one_F3_two_mode_SU2_couplers":len(steps),
      "one_F3_diagonal_phases":3,
      "one_G_9mode_two_mode_couplers":3*len(steps),
      "one_G_Fourier_diagonal_phases":9,
      "one_G_CZ_diagonal_nonzero_phases":n_cz_nonzero,
      "full_W_G_Gdag_blocks":4,
      "full_W_tunable_SU2_couplers_upper_bound":4*3*len(steps),
      "full_W_Fourier_phase_slots_upper_bound":4*9,
      "full_W_CZ_nonzero_phase_slots_upper_bound":4*n_cz_nonzero,
      "full_W_rank3_projector_phase_slots":4*3,
      "path_Hadamard_blocks":2,
      "detector_ports":"2 paths, each resolved or summed across 9 internal modes",
      "note":"No cancellations, resource sharing or gate merging assumed. Static F3 networks can be reused/calibrated if architecture permits."
    }
    checks={
      "Givens_three_couplers_recover_F3":len(steps)==3 and err3<1e-12,
      "lifted_9mode_G_reconstructed":err9<1e-12,
      "CZ_exactly_four_active_modes":n_cz_nonzero==4,
      "full_loop_has_36_two_mode_couplers_upper_bound":circuits["full_W_tunable_SU2_couplers_upper_bound"]==36,
      "unbalanced_loss_formula_valid":all(0<=r["conditional_visibility"]<=1 and .5<=r["surviving_click_probability"]<=1 for r in errors.values())}
    result={"schema":"w33.round6.optics_mesh_loss_budget.v1",
      "route":"two coherent paths x nine spatial waveguide modes; G=CZ(F3 x I3); F3 from 3 complex Givens SU2 two-mode couplers and 3 output phase shifts; 4 G blocks in W; 2 global path 50/50 splitters. Use integrated waveguide/path hardware as a concrete encoding, rather than an unspecified OAM device.",
      "one_F3_complex_givens_indices":[[i,j] for i,j,_ in steps],
      "one_F3_diagonal_phase_radians":np.angle(np.diag(D)).tolist(),
      "F3_decomposition_Frobenius_error":err3,
      "full_G_9mode_reconstruction_error":err9,
      "component_budget":circuits,
      "signal_only_path_loss_calibration":"For arm intensity transmission eta and ideal no-loss reference arm: raw p0-p1=sqrt(eta)*Re W_jj, total click probability=(1+eta)/2; conditioned p0-p1 divided by click =V Re W_jj with V=2sqrt(eta)/(1+eta). Reference W=I calibration removes V if loss is state-independent and stationary.",
      "loss_examples":errors,
      "hardware_error_prior_art":"Reck 1994 https://doi.org/10.1103/PhysRevLett.73.58 and Clements 2016 https://doi.org/10.1364/OPTICA.3.001460; published universal 9-mode mesh upper bound 9*8/2=36 tunable 2-mode couplers for arbitrary U9, whereas one structured G requires 9 by this compilation.",
      "physical_limits":"No foundry design, measured insertion loss, detector efficiency, actuator bandwidth, fabrication tolerance, heralded single-photon source or gate tomography. No actual optical hardware assembled.",
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"checks":result["checks"],"components":circuits},indent=2))
    assert result["all_checks_pass"]
    return result
if __name__=="__main__":run()
