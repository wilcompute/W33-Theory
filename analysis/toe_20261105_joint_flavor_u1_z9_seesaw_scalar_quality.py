#!/usr/bin/env python3
"""TOE integrated symmetry witness: anomaly-free, proton-safe, seesaw, PQ NOT safe.

Known prior art: gauged B-3L_i and exact Z9 from lepton-flavor U(1),
Greljo/Ponce Diaz/Thomsen arXiv:2505.18259 and Davighi et al arXiv:2609.01712.
Independent executable rederivation, not new model-building priority.

Minimal choice X=3(B-3Le). One active electron-flavor charged sterile
N_e^c; sterile N_mu^c,N_tau^c neutral. Scalars T(X=-9),S(X=-18)
give a residual Z9. All dim-6 proton operators QQQL, ucucdcec,
ucdcdcNc are forbidden. A Dirac+Majorana seesaw can be rank three
and give interfamily mixing.

BUT S^dagger T^2 is an allowed RENORMALIZABLE dim-3 operator, so the
relative scalar phase is not a high-quality axion automatically.
This is not a completed GUT or a unique SM flavor derivation.
"""
from __future__ import annotations
from fractions import Fraction as F
import itertools,json,math
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_new_joint_symmetry_z9_seesaw_pq_obstruction.json"
def spec():
    out=[]
    for i,lepton in enumerate((-9,0,0)):
        for name,mult,y,x,c3,weak in (
          ("Q",6,F(1,6),1,1,1),
          ("uc",3,F(-2,3),-1,-1,0),
          ("dc",3,F(1,3),-1,-1,0),
          ("L",2,F(-1,2),lepton,0,1),
          ("ec",1,F(1),-lepton,0,0),
          ("Nc",1,F(0),-lepton,0,0)):
            out.append({"family":i,"field":name,"mult":mult,"y":y,"x":x,
                        "color_triality":c3,"weak_doublet":weak})
    return out
def anomalies(fields):
    ff=fields
    A={
    "gravitational_X":sum(f["mult"]*f["x"] for f in ff),
    "X_cubed":sum(f["mult"]*f["x"]**3 for f in ff),
    "Y_squared_X":sum((f["mult"]*f["y"]**2*f["x"] for f in ff),F(0)),
    "Y_X_squared":sum((f["mult"]*f["y"]*f["x"]**2 for f in ff),F(0)),
    "SU3_squared_X":sum(2*f["x"] for f in ff if f["field"]=="Q")+
      sum(f["x"] for f in ff if f["field"] in ("uc","dc")),
    "SU2_squared_X":sum(3*f["x"] for f in ff if f["field"]=="Q")+
      sum(f["x"] for f in ff if f["field"]=="L"),
    }
    assert all(v==0 for v in A.values()),A
    return {k:str(v) for k,v in A.items()}
def sm_qqql(fields):
    rows=[]
    q=next(f["x"] for f in fields if f["field"]=="Q")
    for i in range(3):
        lj=next(f["x"] for f in fields if f["family"]==i and f["field"]=="L")
        ec=next(f["x"] for f in fields if f["family"]==i and f["field"]=="ec")
        nc=next(f["x"] for f in fields if f["family"]==i and f["field"]=="Nc")
        ops={
          "QQQL":3*q+lj,
          "ucucdcec":-3*q+ec,
          "ucdcdcNc":-3*q+nc}
        assert all(qv%9!=0 for qv in ops.values())
        rows.append({"family":i,"lepton_charge":lj,
              "proton_decay_operator_X_charges":ops,
              "all_nonzero_mod_Z9":True})
    return rows
def mass_matrices():
    # In LH conventions, Y_nu LH Nc and Nc Nc Majorana.
    # X_e=-9, X_Nce=+9; mu/tau charges0.
    l=np.array([-9,0,0]);nc=np.array([9,0,0]);T=-9;S=-18
    Dirac=np.equal(l[:,None]+nc[None,:],0)
    assert Dirac.tolist()==[[True,False,False],
                           [False,True,True],[False,True,True]]
    MR_textures={}
    for i in range(3):
        for j in range(i,3):
            x=int(nc[i]+nc[j])
            field="S" if x+S==0 else ("T" if x+T==0 else ("bare" if x==0 else "forbidden"))
            assert field!="forbidden"
            MR_textures[f"{i}{j}"]=field
    assert MR_textures["00"]=="S"
    assert MR_textures["01"]=="T"
    assert MR_textures["02"]=="T"
    assert all(MR_textures[x]=="bare" for x in ("11","12","22"))
    # Independent benchmark with full rank; parameters chosen arbitrarily.
    md=np.array([[.04,0,0],[0,.08,.02],[0,.015,.095]])
    MR=np.array([[5.,1.2,.9],[1.2,3.5,.6],[.9,.6,4.]])
    assert np.linalg.det(MR)>0 and np.linalg.det(md)>0
    mnu=-md@np.linalg.inv(MR)@md.T
    eig,U=np.linalg.eigh(mnu)
    assert np.linalg.matrix_rank(mnu,tol=1e-10)==3
    # e-mu/e-tau off diagonal must actually develop by seesaw.
    assert abs(mnu[0,1])>1e-5 and abs(mnu[0,2])>1e-5
    assert abs(np.linalg.det(U))>.999
    # Full MR and mD degrees of freedom => no PMNS prediction.
    return {"Ynu_renormalizable_allowed_3x3":Dirac.tolist(),
      "Majorana_renormalizable_sources":MR_textures,
      "one_arbitrary_dimensionless_md":md.tolist(),
      "one_arbitrary_dimensionless_MR":MR.tolist(),
      "light_mass_matrix":mnu.tolist(),
      "light_symmetric_matrix_spectral_eigenvalues":eig.tolist(),
      "light_mass_matrix_rank":int(np.linalg.matrix_rank(mnu)),
      "electron_mixing_with_other_flavors_nonzero":True,
      "not_a_mass_fit_or_PMNS_prediction":True}
def scalar_quality():
    qs={"T":-9,"S":-18}
    # For scalar monomials T^a Tdag^b S^c Sdag^d,
    # require qtot=0 but nontrivial relative phase.
    matches=[]
    for d in range(1,8):
        for a in range(d+1):
          for b in range(d-a+1):
           for c in range(d-a-b+1):
            dd=d-a-b-c
            if (a-b)*qs["T"]+(c-dd)*qs["S"]==0 and (a-b or c-dd):
                matches.append((d,a,b,c,dd))
        if matches:break
    assert matches and matches[0][0]==3
    primitive=[r for r in matches if r[0]==3]
    assert (3,2,0,0,1) in primitive # T² Sdag
    assert (3,0,2,1,0) in primitive # Tdag² S
    phase="2 theta_T - theta_S"
    vT=vS=1e11 # illustrative GeV, not a derived vev
    chiQCD=.0756**4 # conventional QCD susceptibility in GeV^4
    fphase=(4/vT**2+1/vS**2)**(-.5)
    mu_max=1e-10*chiQCD*math.sqrt(2)/(vS*vT**2)
    mphase_if_mu_at_vev=math.sqrt((vS*vT**2/math.sqrt(2)*vT)/fphase**2)
    assert mu_max<1e-45 and mphase_if_mu_at_vev>1e11
    return {"lowest_gauge_invariant_phase_sensitive_scalar_dimension":3,
      "conditional_QCD_quality_example":{
         "vT_GeV":vT,"vS_GeV":vS,"relative_phase_canonical_decay_constant_GeV":fphase,
         "QCD_topological_susceptibility_GeV4":chiQCD,
         "phase_uniform_theta_target":1e-10,
         "conditional_sufficient_phase_uniform_max_abs_cubic_coefficient_GeV":mu_max,
         "relative_phase_mass_if_cubic_coefficient_equals_vT_GeV":mphase_if_mu_at_vev,
         "critical_warning":"The theta quality estimate is a sufficient all-phase criterion in a conventional QCD axion potential; no axion solution exists for a generic unsuppressed cubic here."},
      "primitive_degree3_monoms":[{"T":a,"Tdag":b,"S":c,"Sdag":dd}
                                 for _,a,b,c,dd in primitive],
      "example_operator":"Sdag T^2 + h.c.",
      "relative_angle":phase,
      "independent_relative_axion_shift_is_explicitly_broken_by_renormalizable_cubic":True,
      "cannot_claim_PQ_quality_or_light_QCD_axion_from_this_scalar_inventory":True,
      "scope":"Exact polynomial gauge-invariance test; depends on both vevs and nonzero coefficient. A model may forbid this term with an additional exact selection rule or add a different charge spectrum."}
def gen_universal_nogo():
    # With SM LH weak doublets and no extra chiral weak doublets,
    # SU2^2 U1_X condition is 3*(3 q)+3 l=0.
    q,l=sp.symbols("q l")
    relation=3*(3*q)+3*l
    solution=sp.solve(relation,l)[0]
    assert sp.simplify(3*q+solution)==0
    # This is independent of singlet charges, Dirac masses, Higgs.
    return {"weak_mixed_anomaly_equation":str(relation),
       "universal_lepton_doublet_charge_from_anomaly":str(solution),
       "QQQL_X_charge_after_anomaly_cancellation":str(sp.simplify(3*q+solution)),
       "if_only_SM_doublets_and_generation_universal_X_no_proton_selection":True}
def main():
    fs=spec()
    charges={k:int(next(f["x"] for f in fs if f["family"]==0 and f["field"]==k)) for k in ("Q","uc","dc","L","ec","Nc")}
    assert charges=={"Q":1,"uc":-1,"dc":-1,"L":-9,"ec":9,"Nc":9}
    res=math.gcd(9,18)
    assert res==9
    out={"status":"PASS_B_MINUS_3LE_Z9_SEESAW_PROTON_AND_CUBIC_PQ_OBSTRUCTION",
       "prior_work":["Greljo Ponce Díaz Thomsen arxiv:2505.18259 (2025)",
                     "Davighi Greljo Ponce Díaz arxiv:2609.01712 (2026)"],
       "new_claims":"No originality claim. Executable internal consistency check: gauged flavor nonuniversality repairs minimal B-L proton protection but minimal two-scalar pattern produces an unsuppressed cubic and no high-quality axion.",
       "normalization":"X=3(B-3Le) with primitive integer quark charge +1",
       "chiral_field_rows":len(fs),
       "SM_three_family_polynomial_anomaly_tests":anomalies(fs),
       "scalar_X_charges":{"T":-9,"S":-18,"H":0},
       "unbroken_discrete_gauge_group":f"Z_{res}",
       "proton_operators":sm_qqql(fs),
       "generic_seesaw_renormalizable_textures":mass_matrices(),
       "scalar_phase_quality":scalar_quality(),
       "generation_universal_no_go":gen_universal_nogo(),
       "qualifications":"SU2 Witten anomaly 12 doublets unchanged. Full discrete global-anomaly constraints, cosmology, charged-lepton mixing, neutrino fit, thermal history, GUT and axion heavy quarks not included. Continuous anomaly-free U1 broken by primitive integer-charge vevs is a necessary standard discrete-gauge consistency construction; this is not a direct nonperturbative anomaly proof."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("X_SYMMETRY_PASS",out["unbroken_discrete_gauge_group"],"anomalies",out["SM_three_family_polynomial_anomaly_tests"],
          "neutrino_rank",out["generic_seesaw_renormalizable_textures"]["light_mass_matrix_rank"],
          "PQ_breaking_dimension",out["scalar_phase_quality"]["lowest_gauge_invariant_phase_sensitive_scalar_dimension"],flush=True)
    return out
if __name__=="__main__":main()
