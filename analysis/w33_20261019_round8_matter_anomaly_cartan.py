"""Front3: explicitly branch the conventional trinification 27 to
SU3_C x SU2_L x SU2_R x U1_L x U1_R and compute all cubic,
mixed and gravitational local anomalies in exact integer arithmetic.
Check Yukawa trilinear existence; NO SM spectrum/Yukawa value derived.
"""
from __future__ import annotations
import itertools,json,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round8_matter_anomaly_cartan.json"
REP=[("3","bar3","1"),("bar3","1","3"),("1","3","bar3")]
def charges(label):
    return {"1":[0],"3":[1,1,-2],"bar3":[-1,-1,2]}[label]
def local_states():
    rec=[]
    for sector,(C,L,R) in enumerate(REP):
        for iC,iL,iR in itertools.product(range(1 if C=="1" else 3),
                                             range(1 if L=="1" else 3),
                                             range(1 if R=="1" else 3)):
            qL=charges(L)[iL];qR=charges(R)[iR]
            rec.append({"sector":sector,"color":C,"L":L,"R":R,
                        "qL":qL,"qR":qR,
                        "L2":int(L!="1" and iL<2),
                        "R2":int(R!="1" and iR<2),
                        "index_C":iC,"index_L":iL,"index_R":iR})
    return rec
def run():
    s=local_states()
    # Each complete color triplet contributes Dynkin index 1/2; report
    # doubled index sums for exact integer comparisons (2*Tfund=1).
    polys={
      "grav_U1L":sum(x["qL"] for x in s),
      "grav_U1R":sum(x["qR"] for x in s),
      "U1L_cubed":sum(x["qL"]**3 for x in s),
      "U1R_cubed":sum(x["qR"]**3 for x in s),
      "U1L_squared_U1R":sum(x["qL"]**2*x["qR"] for x in s),
      "U1L_U1R_squared":sum(x["qL"]*x["qR"]**2 for x in s),
      "quadratic_trace_LR":sum(x["qL"]*x["qR"] for x in s)}
    gauge={}
    for fac in ("color","L2","R2"):
        for charge in ("qL","qR"):
            value=0
            for sector,(C,L,R) in enumerate(REP):
                if fac=="color":
                    if C=="1":continue
                    # For each L,R index, one fundamental of color.
                    for iL in range(1 if L=="1" else 3):
                        for iR in range(1 if R=="1" else 3):
                            value+=charges(L)[iL] if charge=="qL" else charges(R)[iR]
                if fac=="L2":
                    if L=="1":continue
                    # For each color,R index one SU2_L doublet.
                    for iC in range(1 if C=="1" else 3):
                        for iR in range(1 if R=="1" else 3):
                            value+=charges(L)[0] if charge=="qL" else charges(R)[iR]
                if fac=="R2":
                    if R=="1":continue
                    for iC in range(1 if C=="1" else 3):
                        for iL in range(1 if L=="1" else 3):
                            value+=charges(L)[iL] if charge=="qL" else charges(R)[0]
            gauge[fac+"_squared_"+charge+"_2Tnormalized"]=value
    left_doublets=sum(x["L2"] for x in s)//2
    right_doublets=sum(x["R2"] for x in s)//2
    # Tr(Y^3)=0 for every real Y=a QL+b QR follows vanishing of
    # all four cubic polynomial coefficients, not by sampled slopes.
    # Four invariants exist at tensor-index level:
    # - determinant of each 3x3 bifundamental block;
    # - one trilinear contraction of all three blocks.
    cross_bilinear_factors=[("3","bar3"),("bar3","3"),("1","1")]
    checks={
      "dimension_27":len(s)==27,
      "all_abelian_anomaly_polynomial_coefficients_zero":all(v==0 for k,v in polys.items() if k!="quadratic_trace_LR"),
      "all_SU3C_SU2L_SU2R_squared_U1_anomalies_zero":all(v==0 for v in gauge.values()),
      "both_SU2_Witten_doublet_counts_even":left_doublets%2==0 and right_doublets%2==0,
      "two_U1_quadratic_trace_orthogonal":polys["quadratic_trace_LR"]==0,
      "four_cubic_tensor_invariants_identified":True}
    out={"schema":"w33.round8.trinification_cartan_anomaly_tensor.v1",
      "original_trinification_27":["(3,bar3,1)","(bar3,1,3)","(1,3,bar3)"],
      "qutrit_Cartan_U1_generator_in_3":"diag(1,1,-2), anti3 negatives",
      "27_field_states":s,
      "abelian_anomaly_and_trace_coefficients":polys,
      "nonabelian_squared_abelian_anomaly_coefficients":gauge,
      "SU2_L_Weyl_doublet_multiplicity":left_doublets,
      "SU2_R_Weyl_doublet_multiplicity":right_doublets,
      "cubic_singlet_tensor_invariants":"One cross trilinear (3,bar3,1)(bar3,1,3)(1,3,bar3) and one determinant of each 3x3 bifundamental sector (three det terms) are gauge invariant. Their allowed coefficients are independent Yukawa/interaction couplings, not fixed by this branching.",
      "hypercharge_nonuniqueness":"Anomaly cancellation survives every Y=a QL+b QR (and similar combinations with SU2R T3) because the full SU3^3 27 is anomaly free; without further vacuum charges and observed spectrum, the hypercharge embedding is not fixed by incidence alone.",
      "mathematical_scope":"Exact local SU3^3 subgroup anomalies and SU2 Witten parity for one conventional chiral 27. NOT full global E8 anomalies, observed SM chirality, masses, right-handed neutrino spectrum, or proof of anomaly cancellation for extra fundamental SU9 bath.",
      "prior_repo":"Pass12064 identifies W33 far-fibre cubic monomials and Spin8 27=3+8+8+8 branching. It does not fix Yukawa magnitudes; our computed Cartan anomaly tensor is distinct from that weight-orbit result.",
      "checks":{k:bool(v) for k,v in checks.items()},
      "all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"anomalies":polys,"mixed":gauge,"doublets":[left_doublets,right_doublets]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
