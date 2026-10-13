"""TOE60 front3: topological dimension and minimal 3-cell completion.

Ranks are native TOE38 verified; ordinary cellular homology/Kunneth exact
integer homology needs separate torsion checks, these are rational Betti numbers.
"""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1]
pre=json.loads((R/"data/w33_20261010_toe38_local_maxwell_2complex.json").read_text())
n0,n1,n2=80,160,1385
r1=79
r2=int(pre["zero_winding_8cycle_rank_at_zero"])
assert r2==78 and pre["n_zero_winding_native_octagons"]==1382
b0=n0-r1;b1=n1-r1-r2;b2=n2-r2
assert (b0,b1,b2)==(1,3,1307)
# X has cellular cells only through C2; thus H3(X)=0 and
# X × S1 has dim≤3 and H4=0. Kunneth over Q:
bX=[b0,b1,b2,0,0]
bprod=[bX[i]+(bX[i-1] if i>0 else 0) for i in range(5)]
assert bprod==[1,4,1310,1307,0]
# T3 requires Betti [1,3,3,1]. Attaching C3 with rank r3:
# b2new = 1307-r3=3 so r3=1304. With no C4 and b3=1,
# dim C3 = r3+1=1305.
r3=b2-3;n3=r3+1
assert (r3,n3)==(1304,1305)
# Euler 2 skeleton =1305; with n3=1305 Euler becomes 0.
assert n0-n1+n2-n3==0
out={"status":"PASS_TOE60_NATIVE_W33_3CELL_COHOMOLOGY_OBSTRUCTION",
"native_chain":{"C0":80,"C1":160,"C2":1385,"C3":0,"rank_d1":79,"rank_d2":78,
"rational_betti_X_2skeleton":[b0,b1,b2,0,0],"Euler_X_2skeleton":1305},
"naive_product_with_periodic_time_circle":{"rational_betti_X_times_S1":bprod,
"no_4cells":True,"H4_dimension":0,
"consequence":"A native two-dimensional cell complex times only a temporal circle has no C4 and no 4-dimensional fundamental cycle on which to integrate a 4-form F wedge F or define a 4D lattice Dirac index. Bloch 3-deck spatial marking does not automatically provide the required local spatial 3-cells."},
"minimal_necessary_3cell_homology_completion_for_T3":{"target_betti_T3":[1,3,3,1],
"required_rank_boundary_d3":r3,"required_number_3cells_without_4cells":n3,
"completed_Euler":0,
"only_necessary":"For T3 rational homology with no added C4, attaching native 3-cells must kill 1304 independent 2-cycle classes while retaining one H3 fundamental class. A purely algebraic choice of 3-boundaries does NOT produce a 3-manifold, a local geometric filling, correct cup product, Poincare duality or physical metric."},
"physics_consequence":"The current 1385-plaquette W33 2-complex does not yet instantiate a full T3 spatial manifold, and its S1-time product cannot support a native 4D chiral topological index without a geometrically justified 3-cell completion. A time-dependent background alone does not create the missing cells.",
"prior_work":"TOE38 owns exact rank78 and first-homology3, and Pass11977 supplies Euclidean time externally. This rank/dimension obstruction is the derived consequence of those already proven numbers."}
(R/"data/w33_20261013_toe60_topological_3cell_obstruction.json").write_text(json.dumps(out,indent=2)+"\n")
print("TOE60 spatial homology",bX,"temporal product",bprod,"needed rankC3",r3,"count",n3)
