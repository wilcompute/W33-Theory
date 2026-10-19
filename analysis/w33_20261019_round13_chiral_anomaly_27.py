"""Round13: anomaly and mass-protection firewall for SO(10)xU(1) E6 27.
The branching and spinor tensor-product rules are standard literature,
not proved by the finite arithmetic here.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round13_chiral_anomaly_27.json"
def run():
    blocks=[("16_spinor",16,1,2),("10_vector",10,-2,1),("1_singlet",1,4,0)]
    grav=sum(dim*q for _,dim,q,_ in blocks)
    cubic=sum(dim*q**3 for _,dim,q,_ in blocks)
    mixed=sum(q*ind for _,dim,q,ind in blocks)
    single_spinor={"U1_gravitational":16,"U1_cubic":16,"SO10_SO10_U1":2}
    su5={"gravitational":10*1+5*(-3)+1*5,
         "U1_cubic":10*1**3+5*(-3)**3+1*5**3,
         "SU5_SU5_U1_index_twice":3*1+1*(-3),
         "SU5_cubic_anomaly":1-1}
    # E6 invariant cubic selection under 27->16_1+10_-2+1_4.
    monomials={"16_16_10":1+1-2, "10_10_1":-2-2+4}
    # As SO10 reps, 16x16=10_s+120_a+126_s: NO trivial rep.
    # A single left Weyl 16 admits no SO10 invariant mass bilinear.
    # 16x16bar has singlet: a vectorlike pair would allow a mass.
    checks={"full27_gravitational_U1_anomaly_zero":grav==0,
       "full27_cubic_U1_anomaly_zero":cubic==0,
       "full27_mixed_SO10_U1_anomaly_zero":mixed==0,
       "single16_alone_has_U1_anomalies":all(x!=0 for x in single_spinor.values()),
       "SU5_chiral_spinor_family_all_anomalies_cancel":all(x==0 for x in su5.values()),
       "both_E6_cubic_Yukawa_monomials_charge_neutral":all(x==0 for x in monomials.values()),
       "SO10_spinor_is_complex_no_bilinear_singlet":True}
    out={"schema":"w33.round13.so10_u1_chiral_27_anomaly_mass_v1",
      "source_prior_art":"https://link.springer.com/article/10.1140/epjc/s10052-019-6878-1 ; https://doi.org/10.1140/epjc/s10052-018-6388-6",
      "E6_27_branching":[{"irrep":name,"dimension":dim,"U1_charge":q,"SO10_Dynkin_index":ind} for name,dim,q,ind in blocks],
      "cancelled_anomaly_polynomials":{"gravitational_U1":grav,"U1_cubic":cubic,"SO10_squared_U1":mixed},
      "single_SO10_spinor16_U1_anomalies":single_spinor,
      "SU5_spinor16_decomposition":"10_(+1) + 5bar_(-3) + 1_(+5), with twice-index SU5(10)=3, SU5(5bar)=1, cubic anomaly A(10)=+1,A(5bar)=-1.",
      "SU5_anomaly_polynomials":su5,
      "SO10_spinor_tensor_square_prior_art":"16 tensor 16 = 10_s + 120_a + 126_s; there is NO gauge-singlet quadratic Weyl mass. A single spinor16 at unbroken SO10 is gauge-protected against a bare Majorana mass; 16 tensor 16bar contains 1, so vectorlike pairs are not protected.",
      "E6_cubic_allowed_Yukawa_charge_sums":monomials,
      "constraint":"In an anomaly-safe FULL 27, the 10 and singlet must also be included; isolated 16_1 with U1 gauged is anomalous. An E6 27 theory does not explain WHY three generations occur or why exotics become heavy. Changing symmetry by a clock selection or Higgs VEV can remove mass protection; verify after breaking. This is not a protected chiral multiplet of the full compact E7xSU2 model, only of a proposed SO10 subgroup.",
      "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"full27_anomalies":[grav,cubic,mixed],"SU5":su5}))
    return out
if __name__=="__main__":run()
