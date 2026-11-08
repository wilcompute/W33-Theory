#!/usr/bin/env python3
"""Exact H27 orbit-averaged Wilson potentials on the native four-holonomy cover.

Declared compact 2^4 torus, unit gauge kinetic coupling; no physical masses,
selected Wilson scalar inventory or a TOE asserted. Uses committed Pass11991
integer H27 matrices rather than a reconstructed idealized group.
"""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

ROOT=Path(__file__).resolve().parents[1]
DATA=Path("data/w33_pass11991_native_four_period_cover.json")

def row_lattice_snf(rows):
    S=smith_normal_form(sp.Matrix(rows),domain=ZZ)
    return [int(S[i,i]) for i in range(min(S.shape)) if S[i,i]!=0]

def reconstruct(root=ROOT):
    obj=json.loads((root/DATA).read_text(encoding="utf8"))
    R=[sp.Matrix(row["matrix"]) for row in obj["exact_deck_actions"]]
    assert len(R)==27 and len({tuple(g) for g in R})==9
    assert all(g.det() in (1,-1) for g in R)
    # Equal compactification sizes [2,2,2,2] and g=1:
    G=sp.Matrix([[sp.Rational(x) for x in row] for row in obj["exact_acoustic_metric"])*sp.Rational(27,2)
    assert G==sp.Matrix([[10,5,-6,0],[5,10,0,-6],[-6,0,12,-6],[0,-6,-6,12]])/2
    assert all(g.T*G*g==G for g in R)
    X=[sp.Matrix([[1 if j==i else 0] for j in range(4)]) for i in range(4)]
    orbits=[]
    Bs=[]
    for i in range(4):
        charges=[g.T*X[i] for g in R]
        unique=sorted({tuple(int(z) for z in q) for q in charges})
        count=Counter(tuple(int(z) for z in q) for q in charges)
        B=sum((q*q.T for q in charges),sp.zeros(4))/27
        assert all(g.T*B*g==B for g in R)
        vals=(G.inv()*B).eigenvals()
        orbit={
          "selected_holonomy_index_zero_based":i,
          "distinct_symmetry_related_integer_wilson_charges":len(unique),
          "charge_multiplicities":sorted(count.values()),
          "unique_integer_wilson_charges":[list(q) for q in unique],
          "wilson_charge_smith_normal_form":row_lattice_snf(unique),
          "charge_lattice_rank":sp.Matrix(unique).rank(),
          "symmetry_averaged_mass_hessian_rank":B.rank(),
          "mass_hessian_numerator_27": [[int(z) for z in row] for row in (27*B).tolist()],
          "generalized_mass_squared_eigenvalues":{str(k):v for k,v in sorted(((str(z),int(m)) for z,m in vals.items()))},
          "cosine_potential_minimum_modulo_2pi":"unique" if row_lattice_snf(unique)==[1,1,1,1] else "continuous or discrete extra minima possible",
          "gauge_invariant_periodic_potential":"V(theta)=mu^2/27*sum_{g in H27}[1-cos((g^T e_i) dot theta)], Hessian=mu^2*B_i"
        }
        orbits.append(orbit);Bs.append(B)
    expected0=sp.Matrix([[18,9,0,0],[9,18,0,0],[0,0,0,0],[0,0,0,0]])/27
    expected3=sp.Matrix([[12,6,-9,0],[6,12,0,-9],[-9,0,18,-9],[0,-9,-9,18]])/27
    assert Bs[0]==Bs[1]==expected0
    assert Bs[2]==Bs[3]==expected3
    assert Bs[0].rank()==2 and Bs[3].rank()==4
    assert Bs[3].det()==sp.Rational(1,81)
    assert [o["distinct_symmetry_related_integer_wilson_charges"] for o in orbits]==[3,3,9,9]
    assert [o["wilson_charge_smith_normal_form"] for o in orbits]==[[1,1],[1,1],[1,1,1,1],[1,1,1,1]]
    # Two real inequivalent 2D C3 character planes: the central H27 element is
    # trivial on this 4D quotient, and the full group representation has no
    # nontrivial 1D real summand. Form exact character projectors.
    raw=obj["exact_deck_actions"]
    projectors=[]
    for index in (0,1):
        P=sum(((2 if (rec["h"][index]%3)==0 else -1)*sp.Matrix(rec["matrix"])
               for rec in raw),sp.zeros(4))/27
        assert P.rank()==2 and P*P==P and P.T*G==G*P
        projectors.append(P)
    P0,P1=projectors
    assert P0+P1==sp.eye(4) and P0*P1==sp.zeros(4)
    assert Bs[0]==G*(sp.Rational(2,9)*P0)
    assert Bs[3]==G*(sp.Rational(2,27)*P0+sp.Rational(1,9)*P1)
    # Symmetry cannot preserve a nonzero rank-one quadratic mass:
    # invariant positive forms are sums c0 G P0 + c1 G P1, c_i>=0.
    assert all(o["symmetry_averaged_mass_hessian_rank"]%2==0 for o in orbits)
    info=dict(
      schema="w33.20261108.h27_symmetrized_wilson_rank.v1",
      status="EXACT_NATIVE_H27_ORBIT_MASS_RANK_AND_WILSON_LATTICE_THEOREM",
      input_file=str(DATA),
      native_holonomy_dimension=4,
      native_H27_controller_elements=len(R),
      distinct_matrices_in_four_real_dimensional_representation=9,
      background="Equal four-period compactification [2,2,2,2]; kinetic gauge coupling g=1. The Wilson-loop amplitude mu^2 is a supplied positive coefficient.",
      electric_metric_G=[[str(z) for z in row] for row in G.tolist()],
      real_character_plane_projectors=[[[str(z) for z in row] for row in P.tolist()] for P in projectors],
      nonzero_H27_invariant_quadratic_mass_rank_choices=[2,4],
      proof_rank="Native real H27 holonomy representation is a direct sum of two inequivalent real C3 irreducible planes, each occurring once. An invariant positive semidefinite form relative to the invariant electric metric is scalar on each plane; any nonzero invariant mass deformation has rank 2 or 4, never rank 1 or 3.",
      proof_unique_wilson_minimum="For e_3 or e_4, the 9 distinct orbit-charge rows span Z^4 with Smith invariants [1,1,1,1]. Each 1-cos contribution is nonnegative; simultaneous zeros therefore force all theta_i=0 modulo 2pi. For e_1/e_2 only rank-2 integer charges occur, leaving a continuous T^2 minimum family.",
      four_coordinate_orbits=orbits,
      extra_combined_forms={
        "rank_G_inverse_B_e1_plus_B_e4":int((Bs[0]+Bs[3]).rank()),
        "generalized_eigenvalues_for_B_e1_plus_B_e4":{str(k):int(v) for k,v in (G.inv()*(Bs[0]+Bs[3])).eigenvals().items()},
        "native_fourth_holonomy_H27_average_hessian_determinant":str(Bs[3].det())
      },
      prior_owners=["data/w33_pass11991_native_four_period_cover.json",
        "analysis/toe_20261108_holonomy_doublet_symmetry.py",
        "analysis/2026-11-08_coupled_holonomy_dynamic_response.md",
        "analysis/2026-11-08_native_gauss_and_magnetic_symmetry.md"],
      physical_limit="This is a small-fluctuation quadratic theorem for a supplied equal-period Wilson scalar potential. Compactification itself might break H27; the independent scalar-loop action does not predict the Wilson coupling or its experimental mass. No physical photon, E6 vacuum, stabilized radius, or TOE follows."
    )
    return info

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--out",type=Path,default=Path("data/w33_20261108_h27_symmetrized_wilson_rank.json"))
    args=p.parse_args()
    x=reconstruct(args.root)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"orbit_lengths":[o["distinct_symmetry_related_integer_wilson_charges"] for o in x["four_coordinate_orbits"]],"ranks":[o["symmetry_averaged_mass_hessian_rank"] for o in x["four_coordinate_orbits"]],"fourth_spectrum":x["four_coordinate_orbits"][3]["generalized_mass_squared_eigenvalues"]}))
if __name__=="__main__":main()
