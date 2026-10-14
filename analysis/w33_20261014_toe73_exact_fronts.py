"""TOE73 exact rational witness crossing, seven-orbit tunneling compression,
and explicit finite CW cell census on W33-squared four-manifold.

Distinguishes a proper subspace compression from the full 3**80 model;
counts cellular topology, not an admissible lattice overlap Dirac operator.
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe72_cover_orbit_escape import certificate as orbit_certificate

def rational_sign(n:int,d:int)->int:
    u=d+n;v=d-n
    x=72*u*u*v**6+46*u**3*v**5+34*u**4*v**4-12*u**8
    return (x>0)-(x<0)

def witness_crossing():
    # P(eps)=(u^2 v^6) [72+46r+34r^2-12r^6],
    # r=(1+eps)/(1-eps)>1. Coefficient signs of the polynomial
    # in descending r powers: -,+,+,+; one change, exactly one
    # positive real root, as Q(0)>0, Q(infty)<0.
    d=100000000
    low=24461518;high=24461519
    assert rational_sign(low,d)==1 and rational_sign(high,d)==-1
    assert rational_sign(0,1)==1 and rational_sign(1,2)==-1
    def Q(r):
        return 72+46*r+34*r*r-12*r**6
    assert Q(1)==140 and Q(3)<0
    # Descartes one positive root, and r(eps) increasing, so the
    # single sign transition is unique in the physical interval.
    return {
      "status":"EXACT_ONE_CROSSING_FOR_FIXED_W33_ADVERSARY",
      "fixed_disorder_high_edges":[30,31,49,51,59,62,63,82,83,93,95,118,119,138,139,142,143],
      "hessian_eigenvector":[0,-1,1],
      "positive_factor":"(1+epsilon)^2*(1-epsilon)^6",
      "polynomial_in_r":"72+46*r+34*r^2-12*r^6",
      "r_definition":"(1+epsilon)/(1-epsilon)",
      "descartes_sign_changes_on_positive_r":1,
      "root_lower_fraction":f"{low}/{d}",
      "root_upper_fraction":f"{high}/{d}",
      "exact_lower_sign":1,"exact_upper_sign":-1,
      "mathematical_scope":"Exactly one root for this fixed 17-edge corner and q eigen-direction; NO global 160-edge/spectral eigenvalue threshold certified."}

def seven_orbit_star():
    c=orbit_certificate()
    assert c["number_of_proved_distinct_full_PGSp_orbits"]==7
    assert all(v["orbit_size"]==51840 for v in c["neighbor_orbit_classification"])
    assert all(v["other_neighbor_indices"]==[v["neighbor"]] for v in c["neighbor_orbit_classification"])
    N=c["original_cover_size_PGSp"]
    assert N==51840 and c["original_orbit_trivial_stabilizer"]
    # A group-equivariant map G->G across two regular G-orbits is
    # bijective. Thus EACH one of the six seed double-flip relations
    # transports to a perfect matching of N covers, with no duplicate.
    E=6*N
    assert E==311040
    # Define H_compressed using only the six center-to-target perfect
    # matchings; this is NOT the induced subgraph and deliberately
    # discards target-target and outside-of-seven-orbit links.
    # It is a direct sum of N copies of the 7-node star K_1,6.
    return {
      "status":"EXACT_SIX_EQUIVARIANT_INTER_ORBIT_MATCHINGS",
      "full_group_order":N,"proven_orbits":7,
      "proven_cover_states":7*N,
      "center_to_each_neighbor_orbit_matching_edges":N,
      "six_center_target_matching_edges":E,
      "inter_orbit_truncated_star_components":N,
      "component_size":7,
      "adjacency_star_eigenvalues":[ "-sqrt(6)", "0", "+sqrt(6)" ],
      "adjacency_star_multiplicities":[N,5*N,N],
      "restricted_second_order_tunneling_amplitude":"-2*t^2/J",
      "restricted_energy_bands":["-2*sqrt(6)*t^2/J","0","+2*sqrt(6)*t^2/J"],
      "proof":"PGSp acts freely transitively on each seven classified 51840-member orbit. Transporting any selected local two-flip seed map under G gives a well-defined bijection between two regular G-sets. Therefore the six distinct relations form six perfect matchings. Their deliberately restricted union is N disjoint K1,6 stars, whose adjacency spectrum is exact.",
      "scope":"Spectrum of a deliberately compressed six-matching graph only; additional transitions among target orbits, higher orders, and all other cover orbits have NOT been evaluated. No physical gravity."}

def w33_squared_cw():
    # A genus g closed orientable surface has a minimal CW presentation:
    # 1 vertex, 2g oriented one-cells (a_i,b_i) and one two-cell
    # attached along product_i [a_i,b_i]. Its cellular differential
    # vanishes over Z (the attaching word abelianizes to zero).
    # Product of two surfaces therefore has these cell counts:
    g=160-80+1
    surf=[1,2*g,1]
    prod=[sum(surf[i]*surf[j-i] for i in range(3) if 0<=j-i<=2)
          for j in range(5)]
    assert (g,prod)==(81,[1,324,26246,324,1])
    euler=sum((-1)**i*prod[i] for i in range(5))
    assert euler==25600
    # Chain differential zero is only for the *minimal* CW complex.
    # Nontrivial attaching maps and cup products remain, so this DOES NOT
    # provide a local Dirac stencil nor a flat metric.
    # q(a_i,a_j)=0 on all inherited alpha cycles; their mixed products
    # have zero self-cup. Dual meridian beta classes can give c1^2=2.
    return {
      "status":"EXACT_MINIMAL_W33_SQUARED_4D_CW_CHAIN_CENSUS",
      "W33_Levi_graph_cycle_rank":g,
      "surface_minimal_CW_cells":surf,
      "two_surface_product_4D_CW_cell_counts":prod,
      "cellular_boundary_operator_rank_each_dimension":[0,0,0,0],
      "cellular_homology_betti":prod,
      "four_dimensional_euler_characteristic":euler,
      "surface_spin_structure_choices_as_power_of_two":f"2^{2*g}",
      "product_spin_structures_as_power_of_two":f"2^{4*g}",
      "inherited_graph_H1_rank_each_surface":g,
      "graph_inherited_mixed_H2_rank":g*g,
      "inherited_mixed_Chern_square":0,
      "inherited_mixed_spin_Dirac_index":0,
      "dual_meridian_example_Chern_square":2,
      "dual_meridian_example_spin_Dirac_index":1,
      "scope":"Explicit finite CW construction from TWO chosen W33 handlebody-boundary surfaces; graph thickening, spin choice and metric are noncanonical. Minimal CW chain differentials being zero does NOT produce a local admissible lattice overlap operator or an intrinsic chiral spectrum."}

def certificate():
    return {"status":"PASS_TOE73_THREE_EXACT_FRONTS",
       "disorder":witness_crossing(),
       "quantum_geometry":seven_orbit_star(),
       "four_dimensional_topology":w33_squared_cw()}
if __name__=="__main__":
    x=certificate()
    (ROOT/"data/w33_20261014_toe73_exact_fronts.json").write_text(json.dumps(x,indent=2)+"\n")
    print(x["status"],x["quantum_geometry"]["six_center_target_matching_edges"])
