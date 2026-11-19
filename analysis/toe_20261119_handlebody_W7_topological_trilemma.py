"""One explicit 3-family/no-mirror Wilson topology and its exact adjoint/cup cost.

Mathematical local-system CW test; NOT a compact singular G2 metric.
"""
from pathlib import Path
import json
from collections import Counter
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_handlebody_trilemma_exact.json"

def run():
    n=7;g=4;z=s.symbols("z")
    phi=s.cyclotomic_poly(n,z)
    units={}
    for k in range(1,n):
        inv=s.invert(z**k-1,phi,domain=s.QQ)
        assert s.rem(s.expand((z**k-1)*inv-1),phi,z)==0
        units[str(k)]=str(inv)
    # SU5 generator W=(z²,z²,z²,z4,z4) with determinant unity.
    w=[2,2,2,4,4]
    spinor=[0]+[(w[i]+w[j])%7 for i in range(5) for j in range(i+1,5)]+[(-x)%7 for x in w]
    assert len(spinor)==16
    multiplicities={str(k):spinor.count(k) for k in range(n)}
    forbidden=sorted(set((-x)%7 for x in spinor))
    choices=sorted(set(range(7))-set(forbidden))
    assert choices==[5],(multiplicities,forbidden,choices)
    # Monodromy on one of the four free generators is ζ^(spinor_exp+k).
    # If no eigenvalue=1 then the sole C0->C1 coboundary has rank16.
    shift=choices[0]
    chars=[(x+shift)%7 for x in spinor]
    assert all(x!=0 for x in chars)
    spinor_h0=0;spinor_h1=g*16-(16-spinor_h0);spinor_h2=0
    assert (spinor_h0,spinor_h1,spinor_h2)==(0,48,0)
    per_SM_component_multiplicity=g-1
    # The 45 Spin10 adjoint decomposes under W7 as:
    # fixed SU3 8 + SU2 3 + hypercharge1 + U1chi1 =13;
    # broken SU5 3x2+conjugate=12, and Lambda²5+conj=20.
    invariant=8+3+1+1
    broken=12+20
    assert invariant+broken==45
    # C0->C1 rank=1 on each nontriv component, 0 on trivial ones.
    adjoint_h0=invariant
    adjoint_h1=g*invariant+(g-1)*broken
    assert (adjoint_h0,adjoint_h1)==(13,148)
    # These b1 are honest 1-skeleton twisted de Rham cohomology.
    # For handlebody retracting to a graph: C^2=0 for ALL flat coeff.
    # Hence H2=0 and the cohomological bulk triple cup is identically 0.
    assert g*16-spinor_h1==16
    # Compare flat nontrivial character on closed rational homology sphere
    # acyclic -> b1=b2=0; with spherical defects and r<k positive,
    # twisted b1=r,b2=k-r; index3 forces r-s=3 and s>=1 mirrors.
    lens=[]
    for k in (5,7,9,11):
        r=(k+3)//2;p=k-r
        assert r-p==3 and p>=1
        lens.append({"spherical_defects":k,"negative":r,"positive":p,
                     "twisted_H1":r,"twisted_H2_mirror":p,"index":3})
    # The three residual free handles are interchangeable by S3 while
    # leaving the first generator's C7 holonomy unchanged.
    # An S3-equivariant symmetric 3x3 Yukawa has precisely two parameters,
    # eigenvalues (a+2b, a-b, a-b), and all such matrices commute.
    from itertools import permutations
    a,b,c,d=s.symbols("a b c d")
    J=s.ones(3,3)
    Yuk=a*s.eye(3)+b*(J-s.eye(3))
    Yother=c*s.eye(3)+d*(J-s.eye(3))
    for perm in permutations(range(3)):
        P=s.zeros(3)
        for i,j in enumerate(perm):P[i,j]=1
        assert s.simplify(P.T*Yuk*P-Yuk)==s.zeros(3)
    assert s.simplify(Yuk*Yother-Yother*Yuk)==s.zeros(3)
    assert Yuk.eigenvals()=={a+2*b:1,a-b:2}
    # Euler characteristic χ(H4)=1−4=-3, while every closed odd
    # dimensional oriented manifold has χ=0; this is where index arises.
    return_value={
      "manifold":"genus-4 3D handlebody, H4 homotopy equivalent to wedge of four circles",
      "CW_cells":{"degree0":1,"degree1":4,"degree2":0,"degree3":0},
      "pi1":"free group F4, epimorphism F4 -> C7 from one generator",
      "C7_polynomial":str(phi),"exact_inverse_certificates_zk_minus_one":units,
      "source_W7_su5_exponents":w,"Spin10_16_exponent_multiplicities":multiplicities,
      "forbidden_intrinsic_line_characters":forbidden,
      "unique_intrinsic_16_line_character_all_weights_nontrivial":shift,
      "all_16_weight_total_characters":chars,
      "16_local_system_betti":[0,spinor_h1,spinor_h2,0],
      "three_equal_components_per_SM_weight":per_SM_component_multiplicity,
      "Spin10_adjoint_W7_invariant_dimension":invariant,
      "Spin10_adjoint_W7_broken_dimension":broken,
      "adjoint_local_system_betti":[adjoint_h0,adjoint_h1,0,0],
      "at_least_unbroken_gauge_adjoint_chiral_candidates":g*invariant,
      "total_adjoint_H1_chiral_candidates":adjoint_h1,
      "absolute_H2_of_handlebody_for_any_flat_local_system":0,
      "bulk_H1_cup_H1_and_all_absolute_triple_cups":"zero: graph retract forces H2=H3=0 regardless of flat characters",
      "lens_spherical_defect_index3_mirror_comparison":lens,
      "chi_handlebody":1-g,"chi_closed_orientable_three_manifold":0,
      "permutation_symmetry_of_three_residual_free_handles":"S3 permutations preserve the one-generator C7 holonomy and the topological local-system isomorphism class",
      "S3_invariant_symmetric_family_Yukawa":"a I + b(J-I)",
      "S3_invariant_Yukawa_eigenvalues":["a+2b","a-b","a-b"],
      "S3_invariant_two_Yukawa_commutator":0,
      "S3_generically_forces_twofold_family_degeneracy":True,
      "uniform_flat_character_up_Higgs_5_weak":3,
      "uniform_flat_character_down_Higgs_bar5_weak":4,
      "two_spinor_family_characters_sum_mod7":(2*shift)%7,
      "uniform_up_Yukawa_total_flat_character_mod7":(2*shift+3)%7,
      "uniform_down_Yukawa_total_flat_character_mod7":(2*shift+4)%7,
      "additional_singlet_flat_character_needed_for_up":(-(2*shift+3))%7,
      "trivial_character_spurion_cannot_complete_up_flat_invariant":True,
      "new_global_Yukawa_compatibility_gate":"Three complete nonmirror Spin10 spinors on H4 force intrinsic character5. A uniform weak 5 Higgs needs character3, so 16*16*5 has total extra C7 character6 and requires a charge1 defect/line insertion. The weak bar5 Higgs needs character4, allowing a flat-character-neutral 16*16*bar5. A charged global constant spurion cannot exist in a nontrivial flat character; localized defect operators might evade this. This is NOT the full physical G2 Yukawa calculation.",
      "flavor_escape":"A metric/flux/defect action must distinguish three handle cycles, or nontrivial family-localized wavefunctions must break S3; topological H1 multiplicity alone cannot predict distinct charged masses and CKM mixing.",
      "scope":"Conditional 3D cohomological toy for ALE/7D gauge-sector chirality. Spin10 16 extra line character is hypothetically provided by an extra Abelian holonomy, not proven by the E8 source or an anomaly-free compact G2. Physical boundary conditions/flux can lift adjoint H1; full 4D fields, couplings, Yukawas, Green-Schwarz inflow and graviton not derived.",
      "key_failure":"Avoiding twisted mirrors via b1(H4)=4 generates at least 52 trivial-local-system unbroken adjoint H1 modes (148 including broken generators), and H2=0 forbids bulk cup Yukawas. This trades one topological obstruction for two others."
    }
    OUT.write_text(json.dumps(return_value,indent=2)+"\n",encoding="utf8")
    print("PASS C7 character5 full 16 gives 3/weight, no mirrors; adjoint H1=148, bulk H2=0")
    print(OUT)
    return return_value
if __name__=="__main__":run()
