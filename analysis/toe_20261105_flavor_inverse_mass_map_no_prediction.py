#!/usr/bin/env python3
"""TOE front C: exact inverse-seesaw *surjectivity* of minimal Z9 flavor texture.

Not an inverse-seesaw mechanism (the physics is type-I seesaw). Rather,
given ANY nonsingular complex symmetric three-neutrino light mass
matrix mnu and any invertible DIAGONAL mD, the heavy Majorana matrix
MR = -mD^T (mnu)^-1 mD is complex symmetric, full rank, and
exactly reproduces mnu. The family-X=3(B-3Le) selection rules permit
ALL its Majorana entries: ee via S, e-mu/tau via T, mu/tau via bare.
Thus the U1X flavor TEXTURE ALONE cannot predict light neutrino
masses, PMNS, Majorana phases or ordering; these remain inputs.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_x_flavor_inverse_seesaw_surjectivity.json"
def mixing(t12,t23,t13,delta,alpha1,alpha2):
    t12,t23,t13,delta,alpha1,alpha2=np.deg2rad([t12,t23,t13,delta,alpha1,alpha2])
    c12,s12=np.cos(t12),np.sin(t12);c23,s23=np.cos(t23),np.sin(t23);c13,s13=np.cos(t13),np.sin(t13)
    ei=np.exp(1j*delta)
    U=np.array([
       [c12*c13,s12*c13,s13*np.conj(ei)],
       [-s12*c23-c12*s23*s13*ei,c12*c23-s12*s23*s13*ei,s23*c13],
       [s12*s23-c12*c23*s13*ei,-c12*s23-s12*c23*s13*ei,c23*c13]],complex)
    U=U@np.diag([1,np.exp(1j*alpha1/2),np.exp(1j*alpha2/2)])
    assert np.max(abs(U.conj().T@U-np.eye(3)))<2e-15
    return U
def reconstruct(masses,angles,phases,md):
    U=mixing(*angles,*phases)
    M=U.conj()@np.diag(np.array(masses)*1e-9)@U.conj().T
    d=np.diag(md)
    R=-d@np.linalg.inv(M)@d
    assert np.linalg.matrix_rank(R)==3
    assert np.linalg.norm(R-R.T)/np.linalg.norm(R)<1e-13  # relative symmetry at large mass scale
    inv=np.linalg.inv(R)
    pred=-d@inv@d
    err=float(np.linalg.norm(pred-M)/np.linalg.norm(M))
    assert err<2e-13
    assert all(abs(R[i,j])>1e-7 for i in range(3) for j in range(3))
    eig=np.linalg.svd(R,compute_uv=False)
    assert min(eig)>1e9
    J=float(np.imag(U[0,0]*U[1,1]*np.conj(U[0,1])*np.conj(U[1,0])))
    mee=float(abs(M[0,0])*1e9)
    return {"masses_eV":masses,"mD_diagonal_GeV":md,"angles_degrees":angles,"Majorana_phases_degrees":phases,
      "heavy_singular_masses_GeV":eig.tolist(),"heaviest_MR_GeV":float(max(eig)),
      "max_reconstruction_relative_error":err,"mee_eV":mee,
      "PMNS_Jarlskog":J,
      "MR_entry_absolute_GeV":abs(R).tolist(),
      "MR_allowed_source_by_X":[["S","T","T"],["T","bare","bare"],["T","bare","bare"]]}
def main():
    # NuFIT-like approximate inputs are SUPPLIED, not computed.
    angles=[33.44,49.2,8.57]
    spl=[7.42e-5,2.515e-3]
    sets=[]
    for lightest in (.001,.005,.018):
        masses=[lightest,math.sqrt(lightest**2+spl[0]),
            math.sqrt(lightest**2+spl[1])]
        for phase in ([195.,0.,0.],[195.,30.,205.]):
            for md in ([2.,3.,4.],[4.,3.,2.]):
                sets.append(reconstruct(masses,angles,phase,md))
    assert len(sets)==12
    assert max(x["max_reconstruction_relative_error"] for x in sets)<2e-13
    assert len({round(x["mee_eV"],8) for x in sets})>=5
    # Test a generic random complex target, unrelated to oscillation
    # outputs, still reproduce; matters are ONLY nonzero masses.
    rng=np.random.default_rng(20261105)
    raw=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    target=(raw+raw.T)/2*1e-10
    d=np.diag([2.,3.,4.]);R=-d@np.linalg.inv(target)@d
    raw_err=float(np.linalg.norm(-d@np.linalg.inv(R)@d-target)/np.linalg.norm(target))
    assert raw_err<2e-14
    result={"status":"PASS_FLAVOR_TEXTURE_SURJECTIVITY_NO_PMNS_PREDICTION",
       "theorem":"For invertible complex symmetric mnu and invertible diagonal mD, MR=-mD^T(mnu)^-1mD is symmetric and reconstructs mnu. Every MR entry is admitted by the X=3(B-3Le) scalar texture [S,T,T;T,bare,bare;T,bare,bare]. No full-rank PMNS or mass-ordering restriction results from this texture alone.",
       "example_count":len(sets),"input_angles_degrees":angles,
       "input_mass_splittings_eV2":spl,"scan":sets,
       "random_nonspecial_complex_symmetric_matrix_relative_error":raw_err,
       "literature":["Type-I seesaw original papers","NuFIT v6.1 2025","Greljo Ponce Diaz Thomsen arxiv:2505.18259"],
       "limitations":"No full charged-lepton flavor matrix or free-parameter count beyond texture. Chosen md, target neutrino masses, angles, CP phases are inputs; output MR is inverse-fit, not a dynamical prediction. Nonzero lightest required; rank-2 cases are a distinct limit."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("NEUTRINO_SURJECTIVITY_PASS",len(sets),"reconstruction",max(s["max_reconstruction_relative_error"] for s in sets),
          "meeRange",(min(s["mee_eV"] for s in sets),max(s["mee_eV"] for s in sets)),flush=True)
    return result
if __name__=="__main__":main()
