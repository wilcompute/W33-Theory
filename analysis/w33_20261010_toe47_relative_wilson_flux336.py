"""TOE47: normalized flux 3+3=6 toy Wilson displacement removes 2fold Yukawa lock."""
import json,itertools
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/"data/w33_20261010_toe47_relative_wilson_flux336.json"
N=128;T=1.45
x,y=np.meshgrid(np.arange(N)/N,np.arange(N)/N,indexing="xy")
def modes(M,shift):
 vals=[]
 for j in range(M):
  v=np.zeros_like(x,dtype=complex)
  for n in range(-7,8):
   k=n+j/M
   v+=np.exp(-np.pi*M*T*(k+y+shift)**2+2j*np.pi*M*k*x)
  v=(2*M*T)**.25*v*np.exp(1j*np.pi*M*x*y)
  vals.append(v)
 return np.array(vals)
def overlap(shift):
 # gauge-consistent bundle displacement relation 3 s_L +3 s_R -6 s_H=0
 L=modes(3,shift);RR=modes(3,-shift);H=modes(6,0)
 # analytic gauge factors give shape, but scalar background
 # is not a fully globally fixed brane model.
 assert np.max(abs(np.mean(L.conj()[:,None]*L[None,:],axis=(2,3))-np.eye(3)))<1e-8
 assert np.max(abs(np.mean(RR.conj()[:,None]*RR[None,:],axis=(2,3))-np.eye(3)))<1e-8
 Y=np.einsum("ixy,jxy,kxy->kij",L,RR,H.conj(),optimize=True)/(N*N)
 forbidden=max(abs(Y[k,i,j]) for k,i,j in itertools.product(range(6),range(3),range(3)) if (i+j-k)%3)
 assert forbidden<1e-10
 return Y,forbidden
bench=[]
for s in (0.,.002,.004,.008,.016,.04):
 Y,forbidden=overlap(s)
 vals=[]
 for k in range(6):
  sig=np.linalg.svd(Y[k],compute_uv=False)
  vals.append(sig.tolist())
  assert np.all(np.isfinite(sig))
 # k=0 has two formerly equal magnitudes, use exact sorted pair
 k0=sorted([abs(Y[0,1,2]),abs(Y[0,2,1])])
 s0=float(abs(k0[1]-k0[0]))
 bench.append({"wilson_shift":s,"k0_two_offdiag_magnitudes":k0,
               "split":s0,"ratio_split_over_s":s0/s if s else None,
               "k0_singular_values":vals[0],"forbidden_max":float(forbidden)})
assert bench[0]["split"]<1e-12
assert all(z["split"]>1e-6 for z in bench[1:])
ratio=[v["ratio_split_over_s"] for v in bench[1:4]]
assert max(ratio)/min(ratio)<1.1,ratio
# With shifts and one Higgs, Yukawa is 3-monomial and YYdagger remains
# diagonal: unequal singular values arise but no CKM mixing in this
# simple factorized one-Higgs setup.
testY,_=overlap(.04)
for k in range(6):
 H=testY[k]@testY[k].conj().T
 assert np.max(abs(H-np.diag(np.diag(H))))<1e-12
out={"status":"NORMALIZED_RELATIVE_WILSON_UNBLOCKS_SINGLE_HIGGS_DEGENERACY_BUT_NOT_CKM",
"flux":{"left":3,"right":3,"Higgs_conjugate":-6},
"wavefunction_shifts":"s_L=s, s_R=-s, s_H=0 satisfying 3s_L+3s_R-6s_H=0",
"torus_tau_im":T,"grid":N,"sampled_shifts":bench,
"small_shift_linear_ratio_range":[min(ratio),max(ratio)],
"math_statement":"For equal left/right backgrounds sL=sR=0, k-fixed Yij is symmetric with equal off-diagonal entries; for opposite continuous Wilson displacements sL=-sR!=0, i+j-k=0 mod3 remains exact, but generally Y12!=Y21. The twofold degeneracy of a single k-fixed monomial Yukawa matrix is lifted continuously (linearly to leading order near s=0). Still YYdagger is diagonal for every single k, so CKM remains trivial in this restricted setup.",
"physical_boundaries":"Toy flat torus wavefunction/Wilson displacement ansatz, not a full globally quantized gauge bundle and tadpole/anomaly-free compactification. Multiple Higgs fields, charged field content, brane stacks, D/F-flat potential, Yukawa flavor fits and RG running not supplied."}
O.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"scan":[(z["wilson_shift"],z["split"]) for z in bench],"slope":out["small_shift_linear_ratio_range"]}),flush=True)
