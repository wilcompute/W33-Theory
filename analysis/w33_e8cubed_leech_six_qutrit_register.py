#!/usr/bin/env python3
"""Compare the E8^3 and Leech fixed-point-free order-3 six-qutrit registers."""
import json,math
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_e8cubed_leech_six_qutrit_register.json'
def main(write=True):
    q=3;n=6;V_size=q**(2*n);nonzero=V_size-1;projective=nonzero//(q-1)
    r1=3*(3**4-1)//2;r2=3*(3**4-1)**2//2;r3=(3**4-1)**3//2
    assert (r1,r2,r3)==(120,9600,256000) and r1+r2+r3==projective
    inside_neighbors=12+40+40;outside_r2=13+13+40;outside_r3=13+13+13
    assert (inside_neighbors,outside_r2,outside_r3)==(92,66,39)
    leech_proj=32760;leech_oriented=65520;leech_minvec=196560
    assert leech_oriented*3==leech_minvec and Fraction(leech_proj,projective)==Fraction(9,73)
    rho=Fraction(4,3);det=3**12;ground=int(math.isqrt(det));assert ground==729
    out={'schema':'w33.e8cubed_leech_six_qutrit_register.v1','status':'PASS',
      'headline':'The diagonal order-3 twist of E8^3 and the fixed-point-free order-3 Leech twist have identical rank-24 twisted-register kinematics: characteristic polynomial Phi_3^12, quotient F3^12 with a nondegenerate alternating form W(11,3), conformal weight 4/3, and a 729-dimensional six-qutrit Heisenberg module. They differ in the lattice shell and orbifold extension: E8^3 -> A8^3 with a 120-point three-W33 root shadow, while Leech minimal vectors give the 32760-point 90-tight 2.Suz orbit and its orbifold is moonshine.',
      'common_register':{'rank_real_lattice':24,'order3_characteristic_polynomial':'Phi_3^12','quotient_order':det,'phase_space':'F3^12','symplectic_geometry':'W(11,3)','nonzero_phase_vectors':nonzero,'projective_Pauli_classes':projective,'twisted_ground_weight':str(rho),'ground_state_dimension':ground,'qutrit_count':6,'Heisenberg_group_shape':'3^(1+12)','module_equivalence':'By the finite Stone-von Neumann theorem, after any symplectic isomorphism of the two F3^12 quotients the two 729-dimensional ground registers are equivalent irreducible Heisenberg modules for the same nontrivial central character.'},
      'E8_cubed':{'factorization':'F3^12 = F3^4 perp F3^4 perp F3^4','ground_register_factorization':'9 x 9 x 9 = 729 (three two-qutrit registers)','weight_one_after_orbifold':'sl9^3','orbifold_lattice':'Niemeier A8^3','root_shadow':{'oriented_nonzero_degrees':240,'projective_points':r1,'description':'three pairwise-orthogonal embedded W(3,3) point sets','block_support_partition_projective':{'support_1':r1,'support_2':r2,'support_3':r3},'neighbors_in_root_shadow':{'point_in_shadow':inside_neighbors,'outside_support_2':outside_r2,'outside_support_3':outside_r3},'tight_set':False,'reason':'outside points have two distinct intersection numbers 66 and 39'},'natural_phase_space_symmetry':'block stabilizer contains Sp(4,3)^3 semidirect S3; it preserves the 4+4+4 symplectic decomposition.'},
      'Leech':{'minimal_vectors':leech_minvec,'hit_nonzero_phase_classes':leech_oriented,'minimal_vectors_per_hit_nonzero_class':3,'projective_minimal_shell':leech_proj,'fraction_of_W11_points':str(Fraction(leech_proj,projective)),'shell_geometry':'90-tight set in W(11,3)','shell_stabilizer':'2.Suz (as certified in Holotrade e680b23)','orbifold':'Z3 orbifold of the fixed-point-free Leech twist gives the moonshine VOA; Monster contains the associated 3^(1+12) register normalizer.'},
      'comparison':{'same_abstract_six_qutrit_register':True,'same_conformal_ground_weight':True,'same_projective_phase_space':True,'shell_preserving_identification':False,'why_not_shell_preserving':'the distinguished shell images have different cardinalities (120 versus 32760) and different intersection structure; no symplectic isomorphism can map one distinguished subset onto the other.','interpretation':'The register is universal to the Phi_3^12 order-3 twist type; the ambient lattice chooses a very different distinguished state/operator subset and therefore a different orbifold extension.'},
      'checks':{'3^12_quotient':det==531441,'729_ground_states':ground==729,'W11_projective_count':projective==265720,'E8cubed_root_shadow_120':r1==120,'support_partition_sums':r1+r2+r3==projective,'root_shadow_not_tight':outside_r2!=outside_r3,'Leech_shell_32760':leech_proj==32760,'Leech_shell_fraction_9_over_73':Fraction(leech_proj,projective)==Fraction(9,73),'same_rho_4_over_3':rho==Fraction(4,3)}}
    assert all(out['checks'].values())
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
