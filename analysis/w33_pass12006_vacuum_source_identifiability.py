"""Actual72-field CP vacuum supplies the jointly matched mixing row.

11989 owns real inverse C matching;11996 owns the stable bounded source.
Here its new target is12007's theta-constrained full charged fit. Coupling
selection and dynamical theta-modulus stabilization are not derived.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
from w33_pass12007_shared_theta_leptons import inputs,FIT,jacobian
ROOT=Path(__file__).resolve().parents[1]

def payload():
    d=json.loads((ROOT/'data/w33_pass11996_joint_singlet_flavour.json').read_text());x=np.array(d['triplet_coordinates']);h=x[:3]+1j*x[3:6];_,m,e,b,A=inputs()
    S=np.column_stack((h.real,h.imag));assert np.linalg.matrix_rank(S)==2
    C=np.column_stack((b.real,b.imag))@np.linalg.pinv(S);assert np.max(abs(C@h-b))<1e-11
    assert np.max(abs(C@h.conj()-b.conj()))<1e-11
    # Introduce6real neutral auxiliary beta coordinates with positive square
    # |beta-C h|². No potential term is inferred from quark data.
    H=np.array(d['scaled_core_flavour_Hessian_decimal'],float)
    J=np.zeros((6,32));J[:3,14:17]=C;J[3:,17:20]=C
    # The congruence-normalized Hessian uses a rescaled auxiliary field so
    # the tiny original flavourenergy is not numerically discarded.
    K=np.eye(6)*7;block=np.block([[H+J.T@K@J,-J.T@K],[-K@J,K]])
    change=np.block([[np.eye(32),np.zeros((32,6))],[J,np.eye(6)]])
    congr=change.T@block@change;target=np.zeros((38,38));target[:32,:32]=H;target[32:,32:]=K
    assert np.max(abs(congr-target))<1e-9
    Jq=jacobian(FIT,False);Jall=jacobian(FIT,True);Z=null_space(Jq);assert Z.shape==(8,2) and np.linalg.norm(Jq@Z)<1e-10
    assert min(np.linalg.svd(Jall,compute_uv=False))>1e-6
    lifted=np.linalg.eigvalsh(Z.T@Jall[6:].T@Jall[6:]@Z);assert min(lifted)>1e-6
    return dict(status='PASS',actual_source_h_real=h.real.tolist(),actual_source_h_imag=h.imag.tolist(),fitted_real_C=C.tolist(),matched_B_real=b.real.tolist(),matched_B_imag=b.imag.tolist(),source_rank2_singular_values=np.linalg.svd(S,compute_uv=False).tolist(),
        CP_source='Existingbounded11996source anditsCPconjugate mapthroughrealC to12007mixingrow andconjugate. Thisretains theta-restrictedrealbareYukawas, unlike11989free-m inversefit.',
        supplied_auxiliary_action='Vextra=Mbeta²|beta-C h|² withbeta3complexSMsinglets, transformationtypecompatiblewithdeclaredh/Cspurions. Classicalelimination beta=C h changes nooldvacuum. It is a specifiedaddedEFTsector, not an E6/familysymmetry-derivedcoupling.',
        exact_stability='Block Hessian [[H+J^T KJ,-J^TK],[-KJ,K]] iscongruent todiag(H,K) bydelta_beta=Jdelta_q+delta_eta. Kpositiveadds6positivemodes andpreservesoldgaugezeros. Applies atfiniteoriginalenergy scale too; the storednumericcheck usescongruence-normalizedfields.',
        normalized_Hessian_congruence_error=float(np.max(abs(congr-target))),auxiliary_positive_modes=6,old_core_positive_modes=d['positive_core_and_flavour_modes'],old_gauge_zero_modes=d['gauge_zero_modes'],
        quark_only_parameter_fibre_dimension=2,charged_observable_lift_on_fibre_eigenvalues=lifted.tolist(),
        selection_gate='Evenanisolatedjointdatafit isNOT aselectedfieldvacuum. Thetwoquarkfit directions aregenuine localidentifiability freedom, liftedby2chargedcomparators. A sumofsquareddataresiduals couldselectthispoint byconstruction but isnot aUVdynamicalprinciple. No suchpotential isclaimedderived.',
        obstruction_to_unique_invariant_B_vacuum='A singlefundamentalcomplextriplet withonlySU3-invariantpotential depends onlyonBdagB; SU3 istransitiveonitsfixednormsphere. Relativeorientation andphysicalCP requiretheactualh/f/t tensors or otherchargedspurions. FreezingCdoesnotderiveitsalignment.',
        prior=['11989 realCvacuumtransmission tofree-m Barrtarget','11996 bounded72fieldCPsource/stability','11971 suppliedtargetpotentialprior','12007 jointtheta/chargedfit'],
        scope='Concrete transmission andaddedpositiveauxiliarysector, not acompleteE6vacuum orselectedtheta/couplingvalues. The fittedC,moduli,scales andspurionpattern remaininputs.')

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass12006_vacuum_source_identifiability.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['quark_only_parameter_fibre_dimension'])
