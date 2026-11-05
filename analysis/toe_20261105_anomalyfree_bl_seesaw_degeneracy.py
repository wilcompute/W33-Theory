#!/usr/bin/env python3
"""TOE front 4: anomaly-free gauged B-L action + 3-singlet type-I seesaw.

All fields left-handed Weyl. 3 right-handed neutrino conjugates cancel
U(1)_{B-L} gauge/gravitational anomalies, scalar B-L=-2 gives
gauge-invariant Majorana masses, Higgs B-L=0 gives Dirac Yukawas.
A rank-2 Dirac Yukawa -> one exactly massless active neutrino.
Reconstruct chosen PMNS mass matrix and demonstrate continuous
Casas-Ibarra degeneracy: consistent action != flavor prediction.
"""
from __future__ import annotations
import json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_bl_gauge_seesaw_flavour_degeneracy.json"
FIELDS={
 "Q":{"mult":6,"Y":F(1,6),"BL":F(1,3)},
 "uc":{"mult":3,"Y":-F(2,3),"BL":-F(1,3)},
 "dc":{"mult":3,"Y":F(1,3),"BL":-F(1,3)},
 "L":{"mult":2,"Y":-F(1,2),"BL":-F(1,1)},
 "ec":{"mult":1,"Y":F(1,1),"BL":F(1,1)},
 "Nc":{"mult":1,"Y":F(0,1),"BL":F(1,1)}}
def anomalies(with_n=True):
    fields={k:v for k,v in FIELDS.items() if with_n or k!="Nc"}
    A={name:sum(v["mult"]*fx(v["Y"],v["BL"]) for v in fields.values())
       for name,fx in (
         ("BL_grav",lambda y,x:x),
         ("BL_cubic",lambda y,x:x**3),
         ("Y2_BL",lambda y,x:y*y*x),
         ("Y_BL2",lambda y,x:y*x*x),
         ("Y_grav",lambda y,x:y),
         ("Y_cubic",lambda y,x:y**3))}
    A["SU3_squared_BL"]=2*FIELDS["Q"]["BL"]+FIELDS["uc"]["BL"]+FIELDS["dc"]["BL"]
    A["SU2_squared_BL"]=3*FIELDS["Q"]["BL"]+FIELDS["L"]["BL"]
    return {k:str(v) for k,v in A.items()}
def PMNS():
    t12,t23,t13=map(math.radians,(33.44,49.2,8.57))
    delta=math.radians(195)
    c12,s12=math.cos(t12),math.sin(t12)
    c23,s23=math.cos(t23),math.sin(t23)
    c13,s13=math.cos(t13),math.sin(t13)
    e=np.exp(-1j*delta)
    u=np.array([
       [c12*c13,s12*c13,s13*np.conj(e)],
       [-s12*c23-c12*s23*s13*e,c12*c23-s12*s23*s13*e,s23*c13],
       [s12*s23-c12*c23*s13*e,-c12*s23-s12*c23*s13*e,c23*c13]],complex)
    assert np.max(abs(u.conj().T@u-np.eye(3)))<1e-14
    return u
def seesaw():
    u=PMNS()
    masses_eV=np.array([0.,math.sqrt(7.42e-5),math.sqrt(2.515e-3)])
    M=np.array([1e10,2e11,5e12]) # GeV
    v=246.22 # Higgs vev GeV
    def build(theta,M0=1e10):
        mat=M.copy();mat[0]=M0
        R=np.eye(3)
        R[1,1]=R[2,2]=math.cos(theta)
        R[1,2]=math.sin(theta);R[2,1]=-math.sin(theta)
        assert np.max(abs(R@R.T-np.eye(3)))<1e-14
        # Dirac mass scale: m_nu[eV]*1e-9 = GeV.
        m_D=1j*u.conj()@np.diag(np.sqrt(masses_eV*1e-9))@R@np.diag(np.sqrt(mat))
        Y=math.sqrt(2)*m_D/v
        mnu=-m_D@np.diag(1/mat)@m_D.T
        target=u.conj()@np.diag(masses_eV*1e-9)@u.conj().T
        assert np.max(abs(mnu-target))<1e-24
        assert np.max(abs(u.T@mnu@u-np.diag(masses_eV*1e-9)))<1e-24
        s=np.linalg.svd(mnu,compute_uv=False)
        assert np.max(abs(np.sort(s)-np.sort(masses_eV*1e-9)))<1e-24
        rank=int(sum(s>1e-15))
        assert rank==2
        return {"Casas_Ibarra_angle_radians":theta,
           "heavy_N_masses_GeV":mat.tolist(),
           "light_masses_eV":masses_eV.tolist(),
           "mnu_eigenvalues_eV":np.sort(s*1e9).tolist(),
           "Yukawa_Frobenius_norm":float(np.linalg.norm(Y)),
           "maximum_Yukawa_entry_abs":float(np.max(abs(Y))),
           "Dirac_Yukawa_rank":int(np.linalg.matrix_rank(Y, tol=1e-12)),
           "PMNS_reconstruction_error_GeV":float(np.max(abs(mnu-target))),
           "charged_lepton_flavour_inputs":"angles, phase and light mass-squared differences supplied as external inputs, not predicted"}
    examples=[build(theta) for theta in (0.,math.pi/7,math.pi/3)]
    examples.append(build(math.pi/7,M0=1e14))
    assert examples[0]["Yukawa_Frobenius_norm"] != examples[1]["Yukawa_Frobenius_norm"]
    assert abs(examples[1]["Yukawa_Frobenius_norm"]-examples[-1]["Yukawa_Frobenius_norm"])<1e-13
    return {"type_I_three_heavy_N_but_two_coupled_Yukawa_columns":True,
      "PMNS_input_angles_degrees":[33.44,49.2,8.57],
      "PMNS_input_dirac_cp_degrees":195,
      "solar_delta_m2_input_eV2":7.42e-5,
      "atmospheric_delta_m2_input_eV2":2.515e-3,
      "examples":examples,
      "continuous_orthogonal_rotation_degeneracy":True,
      "sterile_uncoupled_first_N_mass_unconstrained_by_neutrino_sector":True,
      "boundary":"Reconstructs selected experimental-like neutrino masses/mixings using a general free Dirac Yukawa; cannot derive 3 family count, masses, mixing or scale. For gauged BL 3 Nc cancel anomaly even if one Yukawa column is zero."}
def main():
    a=anomalies()
    assert all(v=="0" for v in a.values())
    no=anomalies(False)
    assert no["BL_grav"]=="-1" and no["BL_cubic"]=="-1"
    assert FIELDS["L"]["BL"]+FIELDS["Nc"]["BL"]==0
    assert 2*FIELDS["Nc"]["BL"]+F(-2)==0
    out={"status":"PASS_ANOMALY_FREE_GAUGED_BL_SEESAW_FAMILY_UNDERDETERMINATION",
      "model_action":"L=LSM - FBL_{mu nu} FBL^{mu nu}/4 + |D_mu H|^2+|D_mu S|^2 - (Ynu L H Nc + f S Nc Nc/2 +h.c.) -V(H,S), where D contains gBL and B-L(S)=-2; spinor indices/conjugations suppressed",
      "per_generation_chiral_anomalies":a,
      "without_Nc_anomalies":no,
      "three_generation_gauged_BL_requires_three_Nc_under_this_chiral_spectrum":True,
      "scalar_S_BL_charge":-2,
      "seesaw":seesaw(),
      "global_SU2_Witten_doublets_three_generations":12,
      "limitation":"A consistent toy extension with fitted Yukawa masses, not a selection of SM gauge group, number of generations, cosmological vacuum or measured PMNS from first principles.",
      "prior_art":"Standard anomaly cancellation with B-L and RH neutrinos, type-I seesaw and Casas-Ibarra family are established."}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("SEESAW_PASS",out["seesaw"]["examples"],flush=True)
    print("CERTIFICATE",OUT,flush=True)
    return out
if __name__=="__main__":main()
