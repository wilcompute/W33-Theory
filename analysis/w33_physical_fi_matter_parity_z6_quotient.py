#!/usr/bin/env python3
"""Physical FI x matter-parity Z6 as a quotient of the certified E8 Z12 grading.

Prior exact W33 theorems:
  * Pass7081-7096: commuting E8 Z4(Kummer) x Z3(CE2) = Z12 grading.
  * Pass7097-7104: the Kummer Z4 restricts to the exact E6 Qpsi charge
        27 = 16_1 + 10_-2 + 1_4,
    and the CE2 triplet refines it as 81=48+30+3.
  * physical FI theorem: a measured heterotic FI projection realizes the same
    E8 -> E6+A2 Z3 grading.
  * Qpsi parity theorem: Qpsi mod2 is matter parity and the D8/spinor E8
    involution.

Consequently the square of the old Kummer Z4 is exactly Qpsi mod2 on all E8
sectors, and quotienting Z12 by residue modulo 6 gives the common
Z2(matter-parity) x Z3(FI) grading.

The resulting Z6 is NOT the flagship physical order-six holonomy.  Their sector
multiplicities and character traces differ, although both cubes are D8-class
involutions of trace -8.
"""
from __future__ import annotations
import cmath,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_physical_fi_matter_parity_z6_quotient.json"

def traces(dims):
    z=cmath.exp(2j*cmath.pi/6)
    out=[]
    for m in range(6):
        x=sum(dims[k]*(z**(k*m)) for k in range(6))
        assert abs(x.imag)<1e-8
        out.append(int(round(x.real)))
    return out

def main(write=True):
    z12=json.loads((ROOT/"data/PART_W33_PASS7081_7096_E8_Z3_Z4_Z12_COMMON_REFINEMENT.json").read_text())
    charge=json.loads((ROOT/"data/PART_W33_PASS7097_7104_VOGEL_KUMMER_CHARGE_REFINEMENT.json").read_text())
    fi=json.loads((ROOT/"data/w33_physical_fi_e6_a2_z3_grading.json").read_text())
    pm=json.loads((ROOT/"data/w33_qpsi_matter_parity_e8_d8_bridge.json").read_text())
    phys=json.loads((ROOT/"data/w33_physical_holonomy_e8_chevalley_lift.json").read_text())

    assert z12["status"]=="EXACT_COMMON_REFINEMENT_OF_CE2_Z3_AND_KUMMER_Z4_INSIDE_E8"
    assert charge["e6_to_d5_u1"]["27_exact_charges"]=={"-2":10,"1":16,"4":1}
    assert fi["status"]=="PASS_PHYSICAL_FI_REALIZES_E6_A2_Z3_GRADING"
    assert pm["status"]=="PASS_QPSI_MATTER_PARITY_EXTENDS_TO_E8_D8_INVOLUTION"
    assert phys["status"]=="PASS_PHYSICAL_INNER_CHEVALLEY_LIFT"

    z4=z12["z4_kummer_spinor_grading"]["grade_dimensions"]
    z3=z12["z3_ce2_grading"]["grade_dimensions"]
    joint=z12["joint_Z4xZ3_dimension_table"]
    d12=z12["z12_crt_grading_dimensions"]
    assert z4==[60,64,60,64] and z3==[86,81,81]
    assert joint==[[54,3,3],[16,48,0],[0,30,30],[16,0,48]]
    assert d12==[54,48,30,16,3,0,0,0,3,16,30,48]

    # Kummer grade mod2 = Qpsi parity on every representation block:
    # row parity gives 120 even and 128 odd, exactly the certified D8 split.
    z2=[z4[0]+z4[2],z4[1]+z4[3]]
    assert z2==[120,128]
    assert z2==[
        pm["E8_Qpsi_mod2"]["fixed_lie_dimension"],
        pm["E8_Qpsi_mod2"]["odd_roots"],
    ]

    # Merge Kummer Z4 rows by parity.  Cartan already sits in (0,0).
    joint_z2_z3=[
      [joint[0][j]+joint[2][j] for j in range(3)],
      [joint[1][j]+joint[3][j] for j in range(3)],
    ]
    assert joint_z2_z3==[[54,33,33],[32,48,48]]
    assert [sum(r) for r in joint_z2_z3]==[120,128]
    assert [sum(joint_z2_z3[i][j] for i in range(2)) for j in range(3)]==[86,81,81]

    # Z12 -> Z6 is simply residue reduction mod 6.
    d6=[d12[k]+d12[k+6] for k in range(6)]
    assert d6==[54,48,33,32,33,48] and sum(d6)==248
    tr6=traces(d6)
    assert tr6==[248,37,5,-8,5,37]

    # Neutral algebra is inherited from the exact Pass7085 common neutral.
    neutral=z12["joint_neutral"]
    assert neutral["root_count"]==46
    assert neutral["semisimple_type"]=="D5+A2"
    assert neutral["extra_cartan_rank"]==1
    assert neutral["dimension"]==54

    # The physical flagship C6 is a different order-six element.
    physical_dims=phys["physical_C6_eigenvalue_multiplicities"]
    assert physical_dims==[44,40,38,48,38,40]
    physical_tr=traces(physical_dims)
    assert physical_tr==[248,-2,14,-8,14,-2]
    assert d6!=physical_dims and tr6!=physical_tr
    # But their cubes are both D8-class: fixed 120, moving 128, trace -8.
    assert tr6[3]==physical_tr[3]==-8
    assert phys["fixed_algebras"]["order2_theta3"]["dimension"]==120

    out={
      "schema":"w33.physical_fi_matter_parity_z6_quotient.v1",
      "status":"PASS_PHYSICAL_FI_MATTER_PARITY_Z6_QUOTIENT_WITH_HOLONOMY_FIREWALL",
      "headline":"The certified Kummer Z4 grading is the integer Qpsi grading modulo four on the E6/CE2 sectors, so its square is exactly Qpsi mod2 = matter parity. Replacing Z4 by this Z2 in the old Z12=Z4xZ3 theorem produces a canonical Z6 quotient. The measured FI projection supplies the Z3 factor, and the measured heterotic matter-parity rule supplies the Z2 interpretation. Its dimensions are 54,48,33,32,33,48 with fixed algebra so(10)+sl3+u1. This Z6 is rigorously distinct from the flagship physical order-six holonomy, whose dimensions are 44,40,38,48,38,40.",
      "ancestry":{
        "old_refinement":"Z12 = Kummer Z4 x CE2 Z3",
        "Kummer_restriction":"Z4 charge = Qpsi mod4 on E6, with 27 charges 16_1+10_-2+1_4",
        "matter_parity":"Kummer Z4 squared = Qpsi mod2 = E8 D8/spinor involution",
        "physical_Z3":"heterotic FI organizer-factor projection realizes the CE2 E6+A2 Z3 grading",
        "new_quotient":"Z12 -> Z6 by residue reduction mod6, equivalently Z4xZ3 -> Z2xZ3"},
      "joint_Z2xZ3_dimensions":{
        "rows":"matter parity 0,1; columns FI grade 0,1,2",
        "table":joint_z2_z3},
      "Z6":{
        "dimensions":d6,
        "trace_powers_m0_to_m5":tr6,
        "fixed_root_system":"D5+A2",
        "fixed_reductive_algebra":"so(10)+sl(3)+u(1)",
        "fixed_dimension":54,
        "representation_reading":"grade0 preserves SO(10) GUT x SU(3) triplet/family factor x U(1)_psi"},
      "physical_flagship_C6_firewall":{
        "physical_dimensions":physical_dims,
        "physical_trace_powers_m0_to_m5":physical_tr,
        "same_cube_trace_minus8":True,
        "same_cube_fixed_type":"D8",
        "same_order6_element":False,
        "reason":"different eigenspace multiplicities and different traces already at powers one and two"},
      "physics_reading":"The E8 algebra contains a mathematically canonical order-six grading built from the newly physicalized FI Z3 and matter-parity Z2. It is a structural Z6 associated with SO(10)xSU(3)xU(1), not the geometric/holonomy Z6-I action of the flagship compactification.",
      "boundary":"The new physical interpretation is exact at the Lie/representation level. It does not identify this Z6 quotient with the Z6-I orbifold twist or with the separately certified physical order-six holonomy; the explicit character comparison proves they are different.",
      "parents":[
        "data/PART_W33_PASS7081_7096_E8_Z3_Z4_Z12_COMMON_REFINEMENT.json",
        "data/PART_W33_PASS7097_7104_VOGEL_KUMMER_CHARGE_REFINEMENT.json",
        "data/w33_physical_fi_e6_a2_z3_grading.json",
        "data/w33_qpsi_matter_parity_e8_d8_bridge.json",
        "data/w33_physical_holonomy_e8_chevalley_lift.json"],
      "checks":{
        "Kummer_square_is_matter_parity_by_grades":True,
        "Z2_dimensions_120_128":True,
        "Z2xZ3_table":True,
        "Z12_to_Z6_quotient":True,
        "fixed_D5_A2_u1_dimension54":True,
        "trace_fingerprint_248_37_5_m8_5_37":True,
        "not_physical_flagship_C6":True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2));return out

if __name__=="__main__":main(True)
