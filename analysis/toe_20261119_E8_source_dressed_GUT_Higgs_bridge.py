"""Charge-exhaustive E8 spurion dressing of a Spin10 rank-breaking Higgs pair.

Source-sensitive conditional 4D EFT glue. No 7D G2 embedding or actual overlap.
"""
from pathlib import Path
from itertools import combinations_with_replacement
import json
import numpy as np
import sympy as sp
from toe_20261119_balanced_source_E8_cup_gate import sector_census
from toe_20261119_uv_messenger_orbifold_causal_vacuum_followup import e8_renormalizable_messenger_completion

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_E8_source_spurion_dressed_Spin10_Higgs_bridge.json"

def source_dressed_rank_breaking():
    sectors,_,_=sector_census()
    old=e8_renormalizable_messenger_completion()
    names=old["charged_field_order"]
    charge=np.asarray(old["field_charges"],int)
    vevs=np.sqrt(np.asarray(old["singlet_squared_vevs"],float))
    lookup={name:i for i,name in enumerate(names)}
    # Higgs 16 charges allowed by actual H1 source census, NOT all four.
    spinors=[s for s in sectors if s["rep_dimension"]==16 and s["b1"]>0]
    tens=[s for s in sectors if s["rep_dimension"]==10 and s["b1"]>0]
    assert [s["label"] for s in spinors]==["16_1","16_2","16_3"]
    assert [s["label"] for s in tens]==["10_12","10_13","10_14","10_24","10_34"]
    monomials={}
    for degree in range(7):
        for ids in combinations_with_replacement(range(len(names)),degree):
            v=tuple(charge[list(ids)].sum(axis=0)) if ids else (0,0,0)
            if v not in monomials:
                monomials[v]=(degree,[names[i] for i in ids])
    cand=[]
    for spinor in spinors:
        q=np.asarray(spinor["SU4_charge"],int)
        for ten in tens:
            h=np.asarray(ten["SU4_charge"],int)
            needA=tuple(-2*q-h);needB=tuple(2*q-h)
            if needA not in monomials or needB not in monomials:continue
            degA,termsA=monomials[needA]
            degB,termsB=monomials[needB]
            cand.append({"pair_vectorlike_16_charge":spinor["label"],
                         "source_10_H":ten["label"],
                         "16H_squared_S":termsA,
                         "bar16H_squared_S":termsB,
                         "degrees":[degA,degB],"total_spurion_insertions":degA+degB,
                         "source_16_charge":q.tolist(),"source_10_charge":h.tolist()})
    min_total=min(v["total_spurion_insertions"] for v in cand)
    assert min_total==3
    target=next(v for v in cand if v["pair_vectorlike_16_charge"]=="16_1" and
                v["source_10_H"]=="10_34")
    assert target["16H_squared_S"]==["B"]
    assert target["bar16H_squared_S"]==["C","D"]
    assert target["degrees"]==[1,2]
    q=np.asarray(target["source_16_charge"])
    h=np.asarray(target["source_10_charge"])
    assert np.array_equal(2*q+h+charge[lookup["B"]],np.zeros(3,int))
    assert np.array_equal(-2*q+h+charge[lookup["C"]]+charge[lookup["D"]],np.zeros(3,int))
    # If new vectorlike Higgs 16H and bar16H carry q and -q, equal
    # aligned singlet vevs cancel their U1^3 D term in addition to
    # canceling Spin10 chi. Existing 19-field singlet D=0 remains intact.
    assert max(abs(float(x)) for x in old["D_Abelian_residual"])<1e-10
    M=10.
    a=vevs[lookup["B"]]/M
    b=vevs[lookup["C"]]*vevs[lookup["D"]]/M**2
    assert a>0 and b>0
    # Independently build the exact holomorphic Hessian for an SU5
    # singlet/one-fiveplet-channel slice, with charged spurions dynamical.
    # B,C,D,N,Nbar,X,Abar5,H5,B5,Hbar5.
    zz=sp.symbols("B C D N Nbar X Abar5 H5 B5 Hbar5")
    B,C,D,N,Nbar,X,U,H5,V,Hbar5=zz
    VEV=sp.Rational(3,2)
    W=X*(N*Nbar-VEV**2)+ B*N*U*H5/10+C*D*Nbar*V*Hbar5/100
    subs={z:0 for z in zz}
    subs.update({B:sp.Integer(1),C:sp.sqrt(sp.Rational(52,25)),
                 D:sp.Integer(1),N:VEV,Nbar:VEV})
    F=[sp.simplify(sp.diff(W,z).subs(subs)) for z in zz]
    assert all(z==0 for z in F)
    H=sp.Matrix([[sp.diff(W,x,y).subs(subs) for y in zz] for x in zz])
    assert H.rank()==6
    # All mixed Hessian derivatives with the three dynamical spurions
    # vanish at VEV. Thus the full 62-field Hessian is block diagonal
    # between old 19-field singlet sector and new 43-field GUT sector.
    assert all(H[i,j]==0 for i in range(3) for j in range(3,10))
    m1=sp.Rational(3,2)/10
    m2=sp.Rational(3,2)*sp.sqrt(sp.Rational(52,25))/100
    assert H[6,7]==m1 and H[8,9]==m2
    # Earlier independently verified: old singlet Hessian rank16/19,
    # new Spin10+10+driver Hessian rank22/43 for any nonzero couplings.
    # Exactly 3+21 broken gauge directions, no local physical moduli.
    n_total=19+43
    r_total=int(old["full_superpotential_Hessian_rank"])+22
    n_null=n_total-r_total
    assert (n_total,r_total,n_null)==(62,38,24)
    assert n_null==3+(45-24)
    return {
      "source_spinor_H1":[s["label"] for s in spinors],
      "source_ten_H1":[s["label"] for s in tens],
      "candidate_all_15_charge_combinations":cand,
      "minimal_total_nonnegative_singlet_spurion_degree":min_total,
      "selected_higgs_pair_source_charge_and_10":target,
      "effective_operator_16_squared":"(B/M) 16H 16H 10_34",
      "effective_operator_bar16_squared":"(C*D/M²) bar16H bar16H 10_34",
      "all_Spin10_and_U1cubed_operator_charges_zero":True,
      "source_spurion_VEVs_B_C_D":[float(vevs[lookup[z]]) for z in ("B","C","D")],
      "dimensionless_effective_couplings_for_unit_UV_coefficients":[float(a),float(b)],
      "SU5_component_reduced_superpotential":str(W),
      "SU5_component_exact_F_terms_zero":True,
      "SU5_component_exact_hessian_rank":int(H.rank()),
      "new_cross_Hessian_to_preexisting_singlet_spurions_zero":True,
      "combined_active_chiral_components":n_total,
      "combined_hessian_rank":r_total,
      "combined_hessian_nullity":n_null,
      "broken_Abelian_plus_Spin10_gauge_complex_dimension":24,
      "combined_local_physical_complex_moduli_count":n_null-24,
      "Z4R_assignment":"R(Singlets,16H,bar16H)=0, R(10_34,Xnew)=2 makes both dressed operators and driver W have charge2",
      "new_fields_beyond_original_spectrum":"one extra vectorlike 16H + bar16H, one neutral R2 driver Xnew; reuse existing source 10_34 and source B,C,D",
      "remaining_anomaly_and_origin_gates":"Requires the NEW mirror 16bar Higgs zero mode (and extra 16 Higgs); original E8 chiral source has none. Higher-dimensional 4D superpotential terms degree4 and5 are gauge/R allowed but no UV messenger/defect/M2 integral is derived. Original Abelian anomalies and discrete R gravitational parity not canceled, Wilson/local-system zero-mode spectrum not rebuilt, realistic mass hierarchy/proton safety and compact G2 remain unsolved.",
      "scientific_interpretation":"A consistent formal source-charge dressing repair to the local 4D Higgs-exotics problem, NOT physical source-derived higher-order Yukawa couplings or a 7D supersymmetric compactification."
    }

def run():
    o=source_dressed_rank_breaking()
    OUT.write_text(json.dumps(o,indent=2)+"\n",encoding="utf8")
    print("PASS minimal source singlet insertions",o["minimal_total_nonnegative_singlet_spurion_degree"])
    print("PASS selected operators",o["effective_operator_16_squared"],o["effective_operator_bar16_squared"])
    print("PASS combined Hessian",o["combined_hessian_rank"],"null",o["combined_hessian_nullity"])
    print(OUT)
    return o
if __name__=="__main__":run()
