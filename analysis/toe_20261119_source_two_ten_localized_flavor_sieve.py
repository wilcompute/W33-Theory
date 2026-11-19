"""E8-gauge-allowed two-10 Yukawas plus NORMALIZED analytic Gaussian toy overlaps.

Only a local illustrative contact/defect overlap; source-space cup integral
remains zero and no G2 wavefunctions or M2 amplitudes are derived.
"""
from pathlib import Path
from itertools import combinations_with_replacement
from math import pi,sqrt,exp
import json
import numpy as np
from toe_20261119_balanced_source_E8_cup_gate import sector_census
from toe_20261119_uv_messenger_orbifold_causal_vacuum_followup import e8_renormalizable_messenger_completion
from toe_20261119_two_ten_W7_BDG_variance_photon import two_ten_Higgs
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_E8_doublet_Gaussian_flavor_gate.json"

def overlap3(centers,widths):
    assert len(centers)==3 and len(widths)==3 and all(s>0 for s in widths)
    W=sum(1/s**2 for s in widths)
    A=sum(x/s**2 for x,s in zip(centers,widths))
    C=sum(x*x/s**2 for x,s in zip(centers,widths))
    pref=(pi**(-.75))*np.prod(np.array(widths)**(-.5))*sqrt(2*pi/W)
    return float(pref*exp(-.5*(C-A*A/W)))

def run():
    sectors,_,_=sector_census();old=e8_renormalizable_messenger_completion()
    fam=[next(z for z in sectors if z["label"]==f"16_{i}") for i in (1,2,3)]
    tens=[next(z for z in sectors if z["label"]==name) for name in ("10_34","10_24")]
    q=np.array(old["field_charges"],int)
    labels=old["charged_field_order"];vevs=np.sqrt(old["singlet_squared_vevs"])
    ms={};max_degree=6
    for degree in range(max_degree+1):
        for indexes in combinations_with_replacement(range(len(q)),degree):
            charge=tuple(q[list(indexes)].sum(0).tolist()) if indexes else (0,0,0)
            if charge not in ms:ms[charge]=[int(z) for z in indexes]
    # The two light 5 and bar5 Higgs projections are NOT equal:
    higgs=two_ten_Higgs()
    up=np.array(higgs["light_5_components"][1:])
    down=np.array(higgs["light_bar5_components"][1:])
    assert abs(float(np.dot(up,down)))<1-.01
    center_f=[-2.,0.,2.]
    center_H=[-.75,.75]
    width_f=[.7,.7,.7]
    width_H=[1.,1.]
    y=np.zeros((2,3,3),float);raw=[];missing=[]
    for h,ten in enumerate(tens):
        for i in range(3):
            for j in range(i,3):
                need=tuple((-np.asarray(fam[i]["SU4_charge"])-np.asarray(fam[j]["SU4_charge"])-np.asarray(ten["SU4_charge"])).tolist())
                if need not in ms:
                    missing.append({"ten":ten["label"],"i":i,"j":j,"missing_charge":need})
                    continue
                ids=ms[need];prod=float(np.prod(vevs[ids])) if ids else 1.
                d=len(ids)
                g=overlap3([center_f[i],center_f[j],center_H[h]],
                           [width_f[i],width_f[j],width_H[h]])
                val=prod/(10**d)*g
                y[h,i,j]=y[h,j,i]=val
                raw.append({"ten":ten["label"],"family_i":i+1,"family_j":j+1,
                            "spurions":[labels[k] for k in ids],"degree":d,
                            "gaussian_overlap":g,"positive_effective_coupling":val})
    assert len(raw)==12 and not missing
    yu=up[0]*y[0]+up[1]*y[1]
    yd=down[0]*y[0]+down[1]*y[1]
    assert np.linalg.matrix_rank(yu)==3 and np.linalg.matrix_rank(yd)==3
    # Real toy Yukawa matrices. The only fit is the explicitly CHOSEN centers,
    # width, and common UV coefficients =1. No observed data entered.
    _,U=np.linalg.eigh(yu@yu.T)
    _,D=np.linalg.eigh(yd@yd.T)
    ckm=np.abs(U.T@D)
    comm=yu@yu.T@(yd@yd.T)-(yd@yd.T)@(yu@yu.T)
    scalar=float(np.linalg.norm(comm,"fro"))
    assert scalar>1e-16
    # If one tensor were present, up/down matrices proportional,
    # exactly commuting, hence no nondegenerate CKM misalignment.
    lone_u=up[0]*y[0];lone_d=down[0]*y[0]
    assert np.max(abs(lone_u@lone_u.T@(lone_d@lone_d.T)-
                      (lone_d@lone_d.T)@(lone_u@lone_u.T)))<1e-13
    # Masses only proportional to singular values; no proper Higgs vevs
    # or RG/CKM phases are inserted.
    result={
      "source_16_fields":[f["label"] for f in fam],
      "source_10_fields":[t["label"] for t in tens],
      "available_UV_spurions":labels,
      "complete_12_charge_neutral_entries":raw,
      "not_gauge_allowed_or_degree_limit":missing,
      "light_Higgs_up_projection_10_34_10_24":up.tolist(),
      "light_Higgs_down_projection_10_34_10_24":down.tolist(),
      "Gaussian_centers_family":center_f,
      "Gaussian_centers_Higgs":center_H,
      "Gaussian_widths_family":width_f,
      "Gaussian_widths_Higgs":width_H,
      "overlap_formula":"Product of three individually L2-normalized 1D real Gaussians integrated over R; no fitted interaction prefactors",
      "Y10_34":y[0].tolist(),"Y10_24":y[1].tolist(),
      "light_Yu":yu.tolist(),"light_Yd":yd.tolist(),
      "yu_singular_values_ascending":np.linalg.svd(yu,compute_uv=False)[::-1].tolist(),
      "yd_singular_values_ascending":np.linalg.svd(yd,compute_uv=False)[::-1].tolist(),
      "abs_CKM_in_toy_model_with_low_to_high_eigenvalue_order":ckm.tolist(),
      "noncommuting_quark_mass_matrices_frobenius_norm":scalar,
      "one_source_ten_alone_commutes_and_has_trivial_CKM":True,
      "strong_scope":"No 7D G2 overlap, no worldvolume M2, no charged/local Wilson wavefunctions, no SM chiral gauge mass spectrum, no canonical metric/Higgs vev or observed CKM/PMNS fit. These are physically inserted toy Gaussian profiles and formally gauge-invariant 4D EFT coefficients; the strict punctured-S3 bulk cup remains zero."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print("PASS all 12 Yukawa charge sectors, analytic Gaussian overlaps; commutator",scalar)
    print("UP",np.linalg.svd(yu,compute_uv=False)[::-1],"DOWN",np.linalg.svd(yd,compute_uv=False)[::-1])
    print("ABS CKM",ckm)
    print(OUT)
    return result
if __name__=="__main__":run()
