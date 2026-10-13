"""TOE60 supplemental: explicit algebraic but non-geometric 3-cell spoof.

An exact homological target can be artificially produced from QR relations,
which demonstrates why Betti matching alone does not construct spacetime.
"""
from pathlib import Path
import numpy as np,json,sys
from scipy.linalg import qr,lstsq
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
ed,vs,look,octs,comm,*_=prep()
P=np.rint(np.asarray([cycle_row(x,ed,vs,look,np.zeros(3)).real for x in octs+comm])).astype(float)
assert P.shape==(1385,160)
Q,T,piv=qr(P.T,mode="economic",pivoting=True)
rank=int(sum(abs(T.diagonal())>1e-8))
assert rank==78
base=piv[:rank];extra=piv[rank:]
a=P.T[:,base];b=P.T[:,extra]
coef,*_=lstsq(a,b,cond=1e-10)
res=float(np.max(abs(a@coef-b)))
assert res<1e-8
# 1307 linearly independent 2-cycles in ker boundary2: each
# has coefficient1 at its unique independent 'extra' face and
# coefficients -coef[:,i] at the 78 selected pivot faces.
# Choose any 1304, leave 3 H2; add a final 3-cell zero-boundary.
assert len(extra)==1307
n3=1304+1
hom=(1,3,1307-1304,n3-1304)
assert hom==(1,3,3,1)
out={"status":"PASS_TOE60_ALGEBRAIC_3CELL_HOMOLOGY_SPOOF",
"original_n2":1385,"rank_d2":rank,"two_cycle_kernel_basis_dimension":len(extra),
"max_boundary2_boundary3_residual_on_1307_implicit_cycles":res,
"construction":"Pivoted QR on P.T chooses 78 independent 2-cell boundary rows and 1307 nonpivot 2-cells. Express each nonpivot boundary in the pivot basis, forming 1307 independent implicit 2-cycles. Attach 1304 formal independent 3-cell boundaries along 1304 cycles and one additional formal 3-cell with zero cellular boundary.",
"constructed_chain_counts":{"C0":80,"C1":160,"C2":1385,"C3":n3},
"constructed_rational_betti":[1,3,3,1],
"WARNING":"This is purely linear-algebraic artificial cellular chain completion. A zero-boundary 3-cell may be a wedged S3 and need not define a fundamental orientation class. It does NOT yield a manifold, locality, cellular attaching maps, cup products, 3+1D spacetime, chirality or gravity. Its purpose is to demonstrate that even matching the full T3 rational Betti list is insufficient evidence of physical 3-space."}
(R/"data/w33_20261013_toe60_3cell_spoof.json").write_text(json.dumps(out,indent=2)+"\n")
print("TOE60 3cell algebraic",len(extra),res,hom)
