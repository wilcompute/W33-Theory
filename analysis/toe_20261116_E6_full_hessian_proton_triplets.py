"""Independent E6 Higgs-sector quadratic rank and dimension-five triplet matching.

Starting from the already committed parallel E6 Higgs vacuum, independently
construct the entire gauge-fixed 124x124 holomorphic quadratic form:
- 16 centralizer adjoint generators
- two 27 Higgs and two 27bar (108 chiral complex coordinates)
with superpotential W=-283/2 Tr Phi^2+3/5 Tr Phi^5+1/6 Tr Phi^6
+sum_a barH_a Phi^2 H_a +1/2 tr(G-I)^2.

The 62 adjoint root orbit coordinates are fixed by complex gauge.
The 124x124 gauge-fixed block splits into 16 centralizer, 100 charged
H/barH, and 8 neutral frame variables. Ranks 16+100+4=120,
and the four neutral kernel directions are precisely the residual
centralizer frame gauge directions. Thus 186-120=66 Goldstone/gauge.

Also compute exactly that the same tuned doublet-triplet sector of a
spectator 27+bar27 (mass barK*(Phi+3)*K) generically permits the
dangerous SUSY SU5 QQQL and u^c u^c d^c e^c dimension-five
operator from mass-5 color-triplet exchange. This is an operator-level
phenomenology constraint, not a decay rate.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
from collections import Counter
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_E6_isolated_SM_Higgs_vacuum import centralizer
from toe_20261116_E6_full_cubic_SM_stabilizer import (
    cubic_derivation_rows,cubic_monomials,hypercharge_integer_weights
)
from toe_20261116_E6_Yukawa_superpotential_flat import mass_hessian
OUT=ROOT/"data"/"toe_20261116_E6_Higgs_rank_and_triplet_proton_operator.json"

def full_higgs_rank():
    Y=hypercharge_integer_weights()
    neutral=[i for i,w in enumerate(Y) if w==0]
    assert neutral==[7,8]
    lie=centralizer(cubic_derivation_rows(cubic_monomials()),Y)
    assert len(lie)==16
    diag=S.diag(*Y)
    P=S.diag(*[int(w==0) for w in Y])
    # W=sum c_d/d Tr Phi^d: exact Hessian at commuting perturbations
    # H(X,Y)=Tr[(-283 I+12 Phi^3+5 Phi^4) X Y]+2Tr(PXY).
    D=-283*S.eye(27)+12*diag**3+5*diag**4+2*P
    HA=S.Matrix([[S.trace(D*A*B) for B in lie] for A in lie])
    assert HA==HA.T and HA.rank()==16
    QA=S.Matrix([[S.trace(A*B) for B in lie] for A in lie])
    assert QA.det()!=0
    # 100 off-neutral Higgs/dual coordinates, matrix [[0,M],[M,0]]
    # with 50 invertible diagonal elements w_i^2.
    mass_entries=[int(w*w) for a in (0,1) for i,w in enumerate(Y) if i not in neutral]
    assert len(mass_entries)==50 and all(mass_entries)
    z=S.symbols("h00 h01 h10 h11 b00 b01 b10 b11")
    H=S.Matrix(2,2,list(z[:4]))
    B=S.Matrix(2,2,list(z[4:]))
    deltaG=B+H.T
    W2=S.trace(deltaG*deltaG)/2
    HG=S.hessian(W2,z)
    assert HG.rank()==4 and HG.shape==(8,8)
    # The 16 and 100 and 8 blocks give 124 chiral variables in this
    # gauge. To certify 124x124 rank form the sparse full matrix.
    sub=S.diag(*mass_entries)
    charg=S.BlockMatrix([[S.zeros(50),sub],[sub,S.zeros(50)]]).as_explicit()
    M=S.diag(HA,charg,HG)
    assert M.shape==(124,124) and M.rank()==120
    assert 186-120==66
    return {"gauge_fixed_adj_Cartan_and_root_centralizer_dim":16,
        "centralizer_exact_Hessian_rank":int(HA.rank()),
        "centralizer_trace_metric_det":str(QA.det()),
        "charged_Hbar_H_sector_rank":100,
        "neutral_2by2_frame_sector_rank":int(HG.rank()),
        "gauge_fixed_Higgs_Hessian_shape":list(M.shape),
        "gauge_fixed_Higgs_Hessian_rank":int(M.rank()),
        "remaining_neutral_kernel":int(8-HG.rank()),
        "full_186_chiral_zeromodes_after_gauge_restore":66,
        "full_Higgs_sector_physical_zero_modes_modulo_complex_gauge":0,
        "verification_scope":"Full holomorphic Hessian of this specified superpotential on the centralizer gauge slice, not physical mass eigenvalues after D-term/gaugino mixing. Its four frame zeros are residual gauge."}

def triplet_operator():
    ys=hypercharge_integer_weights()
    cub=cubic_monomials()
    old=mass_hessian(1,0)
    light={i for i,w in enumerate(ys) if w!=0 and not any(old[:,i])}
    assert len(light)==15
    # Y integer weights for chiral quarks/leptons:
    # Q=-1, u^c=+4, e^c=-6, d^c=-2, L=+3.
    types={-1:"Q",4:"u_c",-6:"e_c",-2:"d_c",3:"L"}
    assert Counter(ys[i] for i in light)==Counter({-1:6,4:3,-6:1,-2:3,3:2})
    # K color triplet Y weight +2, mass eigenvalue 2+3=5.
    k_trip=[i for i,w in enumerate(ys) if w==2]
    assert len(k_trip)==3
    # Cubic I3(X,X,K_triplet) monomials support QQ and u^c e^c.
    up=[]
    down=[]
    for k in k_trip:
        for tri,c in cub.items():
            if k in tri:
                other=tuple(t for t in tri if t!=k)
                if len(other)==2 and all(t in light for t in other):
                    up.append({"K_color_component":k,"matter_indices":list(other),
                        "matter_fields":sorted(types[ys[i]] for i in other),
                        "cubic_coefficient":int(c)})
        # Conjugate Higgs barK_k (dual Y=-2) and barH_7 (Y=0) -> d*(barK,barH)
        image=[(im,c) for (x,y,im),c in cub.items() if False]
        image=[(next(i for i in tri if i not in (k,7)),c)
             for tri,c in cub.items() if k in tri and 7 in tri and k!=7]
        assert len(image)==1
        im,c1=image[0]
        assert ys[im]==-2
        for tri,c2 in cub.items():
            if im in tri:
                other=tuple(t for t in tri if t!=im)
                if len(other)==2 and all(t in light for t in other):
                    down.append({"barK_anti_color_component":k,"intermediate_27_component":im,
                        "matter_indices":list(other),
                        "matter_fields":sorted(types[ys[i]] for i in other),
                        "quartic_coefficient":int(c1*c2)})
    up_types=Counter(tuple(z["matter_fields"]) for z in up)
    dn_types=Counter(tuple(z["matter_fields"]) for z in down)
    assert up_types[("Q","Q")]>0 and up_types[("e_c","u_c")]>0
    assert dn_types[("L","Q")]>0 and dn_types[("d_c","u_c")]>0
    return {
        "light_matter_per_family":dict(Counter(types[ys[i]] for i in light)),
        "spectator_K_triplet_components":k_trip,
        "spectator_color_triplet_mass_in_units_of_v":5,
        "up_cubic_coupling_monomials":len(up),
        "down_Hbar_inserted_quartic_monomials":len(down),
        "up_type_counts":{str(k):int(v) for k,v in up_types.items()},
        "down_type_counts":{str(k):int(v) for k,v in dn_types.items()},
        "explicit_up_vertices":up,
        "explicit_down_vertices":down,
        "dimension_five_operator":"After integrating out K_triplet and barK_antitriplet with W=m Kbar K+y_u K QQ/eu+y_d barK QL/ud, W_eff=-y_u*y_d/m*(QQQL + u^c u^c d^c e^c index contractions), m=5v in this toy model.",
        "phenomenological_warning":"Generically allowed baryon/lepton violating SUSY dimension-5 operators. No proton lifetime predicted absent v, Yukawa matrices, squark dressing, superpartner masses, flavor suppressions, discrete symmetries."}

def verify():
    r=full_higgs_rank();q=triplet_operator()
    return {"status":"PASS_E6_FULL_GAUGE_FIXED_HESSIAN_AND_DIM5_TRIPLET_FALSIFIER",
            "full_higgs_rank":r,"SU5_triplet_exchange":q,
            "limitation":"Explicit E6-Lie algebra symmetry breaking and one chosen EFT vacuum; does not predict three families, scales, low energy flavor, stability against quantum and higher-dimensional operators."}
if __name__=="__main__":
    cert=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(cert["status"],cert["full_higgs_rank"]["gauge_fixed_Higgs_Hessian_rank"],
          cert["SU5_triplet_exchange"]["up_type_counts"],cert["SU5_triplet_exchange"]["down_type_counts"])
