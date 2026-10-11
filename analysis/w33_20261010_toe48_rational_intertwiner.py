"""TOE48: integral Gram and rational projector certificates for line->End5.

Exact integer equalities for line adjacency; cyclotomic phases are still
checked with floating arithmetic and are NOT formal integer intertwiners.
"""
import runpy,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1]
a=runpy.run_path(str(R/"analysis/w33_20261010_toe47_cusp_even5_ic_povm.py"))
A=a["Aline"].astype(np.int64); G=a["Gram"];I=np.eye(40,dtype=np.int64);J=np.ones((40,40),dtype=np.int64)
H=8*I+2*A+J # 9 * exact design Gram
assert np.max(abs(9*G-H))<3e-12
assert np.array_equal(A@A,12*I+2*A+4*(J-I-A))
# H^2=12H+? spectrum H eigen 72^1 +12^24 +0^15.
# H(H-12I) acts only on constants, with 72*(72-12)=4320
assert np.array_equal(H@H-12*H,108*J)
# Exact integer relation: 6H - 48I - 12A - 6J = 0
Pminus=((A-12*I)@(A-2*I))/96
P2=((A-12*I)@(A+4*I))/(-60)
P0=J/40
assert np.max(abs(Pminus@Pminus-Pminus))<1e-12
assert np.max(abs(P2@P2-P2))<1e-12
Ginv=P0/8+.75*P2
assert np.max(abs(G@Ginv-(np.eye(40)-Pminus)))<1e-12
assert np.max(abs(Ginv@G@Ginv-Ginv))<1e-12
# Exact dual frame on observable Hilbert side via 25D projector quotient.
rays=a["projectors"]
rng=np.random.default_rng(48005)
err=[]
for _ in range(12):
 M=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5))
 Z=M+M.conj().T
 coords=np.einsum("pij,ji->p",rays,Z).real
 lin=np.einsum("p,pij->ij",Ginv@coords,rays)
 err.append(float(np.max(abs(Z-lin))))
assert max(err)<2e-12
def rank_mod(M,p):
 X=np.asarray(M,dtype=np.int64).copy()%p
 r=0
 for c in range(X.shape[1]):
  ids=np.flatnonzero(X[r:,c])
  if not len(ids):continue
  i=r+int(ids[0]);X[[r,i]]=X[[i,r]]
  X[r]=X[r]*pow(int(X[r,c]),-1,p)%p
  for j in range(X.shape[0]):
   if j!=r and X[j,c]: X[j]=(X[j]-X[j,c]*X[r])%p
  r+=1
  if r==X.shape[0]:break
 return r
ranks={str(p):rank_mod(H,p) for p in (2,3,5,7,11,13,17)}
assert ranks["5"]==25 and ranks["7"]==25 and ranks["11"]==25
# If rank drops at bad primes it is a genuine obstruction to
# naively reducing characteristic-zero Gram/1-3-normalisation.
out={"status":"TOE48_INTEGER_LINE_GRAM_RATIONAL_INTERTWINER_AND_BAD_PRIME_AUDIT",
"integer_gram":"9*G=8*I+2*A_line+J","exact_matrix_identity":"H²-12H=108J for H=9G",
"characteristic_zero_rank":25,"eigenvalues_of_H":{"72":1,"12":24,"0":15},
"mod_prime_ranks_H":ranks,
"rational_Moore_Penrose":"G+=P_const/8+(3/4)P_{+2}; P_const=J/40, P_{+2}=-(A-12I)(A+4I)/60",
"kernel_projector":"P_{-4}=(A-12I)(A-2I)/96, dimension 15",
"max_12_Hermitian_operator_frame_reconstruction_error":max(err),
"representation_scope":"The real-linear 40-line permutation module maps equivariantly and surjectively to Hermitian operators on the even 5D Weil space under K.GENS; kernel is line-side -4 eigenspace. Its rational Gram and rational pseudoinverse specify the exact quotient algebra. Phased generator matrices were checked numerically in TOE47, not reconstructed here over cyclotomic integers.",
"boundary":"H may have different ranks modulo primes dividing denominators or eigenvalue gaps. Reduction mod3 is NOT a free same-dimension physical operator space, since 1/3 normalisation fails there. No claimed isomorphism with Holotrade K81, E8, or physical chiral flavor."}
(R/"data/w33_20261010_toe48_rational_intertwiner.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"ranks":ranks,"reconstruction_error":max(err)}))
