"""TOE60 front5: improve Schur-complement selected 3-rotor enclosures
using sparse 3D integer-flux Ritz diagonalization N=4,5,6.
Not a full W33 gauge-field Hilbert space.
"""
from pathlib import Path
from itertools import product
import json,numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
R=Path(__file__).resolve().parents[1]
old=json.loads((R/"data/w33_20261013_toe59_flux_error_bound.json").read_text())
G=np.array(old["selected_octagon_Gram"],dtype=int)
assert G.tolist()==[[8,-4,-4],[-4,8,4],[-4,4,8]]
lam=np.linalg.eigvalsh(G)[0]
def ground(g,N):
 m=np.arange(-N,N+1);L=2*N+1
 x,y,z=np.meshgrid(m,m,m,indexing="ij")
 D=(G[0,0]*x*x+G[1,1]*y*y+G[2,2]*z*z+
    2*G[0,1]*x*y+2*G[0,2]*x*z+2*G[1,2]*y*z)
 diagonal=.5*g*g*D.reshape(-1)+3/g**2
 S=sparse.diags(np.ones(L-1),1,shape=(L,L),format="csr")
 t=S+S.T
 eye=sparse.eye(L,format="csr")
 T=sparse.kron(sparse.kron(t,eye),eye)+sparse.kron(sparse.kron(eye,t),eye)+sparse.kron(sparse.kron(eye,eye),t)
 H=sparse.diags(diagonal,format="csr")-T/(2*g*g)
 eig,v=eigsh(H,k=2,which="SA",tol=2e-11,maxiter=15000)
 v0=v[:,0];E=float(np.dot(v0,H@v0))
 res=float(np.linalg.norm(H@v0-E*v0))
 cmin=float(g*g*lam*(N+1)**2/2)
 b2=3/(4*g**4)
 assert cmin>E
 low=float(E-b2/(cmin-E))
 assert low<E
 return {"N":N,"states":L**3,"E_upper_variational":E,"schur_lower_using_numeric_ritz":low,
         "interval_width":E-low,"ground_vector_residual_norm":res,
         "first_excitation_gap":float(eig[1]-eig[0]),
         "outside_electric_min":cmin}
out=[]
for g in (.7,1.1):
 rows=[ground(g,N) for N in (4,5,6)]
 assert all(x["ground_vector_residual_norm"]<1e-7 for x in rows)
 assert all(rows[i]["E_upper_variational"]>rows[i+1]["E_upper_variational"]-1e-7 for i in (0,1))
 out.append({"g":g,"rows":rows,"best_lower":max(x["schur_lower_using_numeric_ritz"] for x in rows),
             "best_upper":min(x["E_upper_variational"] for x in rows)})
 print("TOE60 Schur",g,[(x["N"],x["states"],round(x["interval_width"],7),round(x["ground_vector_residual_norm"],10)) for x in rows],flush=True)
outdoc={"status":"PASS_TOE60_SPARSE_3LOOP_SCHUR_BOUNDS_REFINEMENT",
"selected_native_signed_Gram":G.tolist(),"cases":out,
"derivation":"For full selected 3-rotor H on l²(Z³), exterior C>=cN=g² λmin(G)(N+1)²/2 and finite-to-exterior coupling norm squared 3/(4g4). Given EXACT finite-block ground eN, full E in [max(0,eN-b²/(cN-eN)),eN]. Here eN is numerically approximated by sparse Ritz with explicitly reported finite eigenvector residual; these numbers are numerically verified enclosures, not machine-interval certified bounds.",
"caveat":"Numerical eigenvector residual does not by itself rigorously certify which eigenvalue is the smallest, and floating-point rounding is not outward-bounded. The exact Schur theorem is rigorous; tabulated numeric endpoints are approximate. Other 1382 native plaquettes and all quantum charged matter are absent.",
"prior":"Extends TOE58/TOE59 selected 3-loop Schur approach; no claim of novel general Ritz or resolvent theorem."}
(R/"data/w33_20261013_toe60_sparse_flux_bounds.json").write_text(json.dumps(outdoc,indent=2)+"\n")
