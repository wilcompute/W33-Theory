"""TOE78: exact native 27-octagon cubic GQ(2,4) Ramanujan/Ihara
and 270-oriented-prime-cycle ↔ 270 externally phased cubic triples.

Use the W33-derived native Heisenberg-orbit certificate, not a
newly invented cubic graph. The bijection is finite combinatorics,
not an E8 Yukawa derivation or a statement about classical RH.
"""
from __future__ import annotations
import itertools,json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_H27_shared_octagon_group import certificate as native
def certificate():
    prior=native()
    assert prior["native_GQ24_line_count"]==45
    lines={frozenset(t) for t in prior["native_GQ24_tritangent_lines"]}
    assert len(lines)==45
    adj=np.zeros((27,27),dtype=np.int64)
    for line in lines:
        assert len(line)==3
        for i,j in itertools.combinations(sorted(line),2):
            adj[i,j]=adj[j,i]=1
    assert not np.any(np.diag(adj))
    degrees=adj.sum(axis=1).astype(int).tolist()
    assert degrees==[10]*27
    J=np.ones((27,27),dtype=np.int64)
    I=np.eye(27,dtype=np.int64)
    # Exact integer SRG spectral identity:
    # A^2+4A-5I=5J.
    assert np.array_equal(adj@adj+4*adj-5*I,5*J)
    assert int(np.trace(adj))==0
    assert np.array_equal(adj@np.ones(27,dtype=np.int64),
                          np.full(27,10,dtype=np.int64))
    # Solve 20+6=26, 10+20*1+6*(-5)=0.
    evals={"10":1,"1":20,"-5":6}
    assert 10+20*1+6*(-5)==0
    assert (-5)**2<4*(10-1)
    # Each tritangent has exactly six cyclic directed presentations,
    # one for each ordering of its three distinct vertices. Equivalently,
    # each is a length-three based/marked oriented prime Ihara geodesic.
    geodesics={tuple(perm) for L in lines for perm in itertools.permutations(L)}
    phase_instructions={
      frozenset(((vertex,phase) for phase,vertex in enumerate(perm)))
      for perm in geodesics}
    assert len(geodesics)==270 and len(phase_instructions)==270
    inverse={frozenset((vertex,phase) for phase,vertex in enumerate(w)):
             tuple(w) for w in geodesics}
    assert len(inverse)==270
    # D_Hashimoto directed length3 closed-walk trace = 6*C3.
    assert sum(int(np.trace(np.linalg.matrix_power(adj,k)))==270
               for k in (3,))==1  # no backtracking triangles possible
    # W33 cubic SRG Ihara-Bass:
    # (1-u²)^(135-27) prod_lambda (1-lambda*u+9u²).
    probes=(.07,.13,.19)
    spectral_checks=[]
    for u in probes:
        left=(1-u*u)**108*(1-10*u+9*u*u)*\
             (1-u+9*u*u)**20*(1+5*u+9*u*u)**6
        right=(1-u*u)**108*float(np.linalg.det(
            np.eye(27)-u*adj+9*u*u*np.eye(27)))
        assert abs(left-right)<2e-10
        spectral_checks.append({"u":u,"difference":abs(left-right)})
    return {
      "status":"PASS_TOE78_W33_NATIVE_GQ27_IHARA_270_PRIME_TRIANGLE_INSTRUCTIONS",
      "graph":"native 27 shared W33 octagons with the unique stabilizer-invariant cubic GQ(2,4) incidence",
      "vertices_edges_degree":[27,135,10],
      "strongly_regular_parameters":[27,10,1,5],
      "exact_integer_adjacency_identity":"A^2+4*A-5*I=5*J",
      "adjacency_spectrum_multiplicities":evals,
      "Ramanujan_regular_degree_10":True,
      "Ihara_nontrivial_pole_modulus":"1/3",
      "Ihara_inverse":"(1-u^2)^108*(1-u)*(1-9*u)*(1-u+9*u^2)^20*(1+5*u+9*u^2)^6",
      "independent_Bass_numerical_checks":spectral_checks,
      "undirected_primitive_three_cycles":45,
      "based_oriented_length3_prime_nonbacktracking_geodesics":270,
      "E8_external_phase_labelled_cubic_supports":270,
      "equivariant_rule":"ordered directed triangle (v0,v1,v2) -> {(v0,0),(v1,1),(v2,2)}. This commutes with every graph automorphism when the external labels remain fixed.",
      "same_support_as_existing_frozen_H27_270_instructions_requires_gauge":"Compare via the explicitly tested address-to-octagon H27 isomorphism; the 270 count and bijection of unlabelled cubic supports alone do not identify E8 root vectors or physics.",
      "ordinary_W33_collinearity_graph_RH_circle":"11^(-1/2)",
      "ordinary_W33_Levi_graph_RH_circle":"3^(-1/2)",
      "new_native_cubic_graph_RH_circle":"3^(-1)",
      "scope":"Exact cubic combinatorics/Ihara/Ramanujan finite graph identity. No classical Riemann RH or physical unified field theory follows."}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe78_cubic_270_ihara.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],"Ramanujan",c["Ramanujan_regular_degree_10"],
          "oriented_primes",c["based_oriented_length3_prime_nonbacktracking_geodesics"])
