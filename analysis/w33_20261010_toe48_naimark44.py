"""TOE48: explicit 44-mode Naimark isometry for 41-outcome two-qutrit POVM.

40 even rank-one effects and 4 odd rank-one refinements.
Nearest-neighbor complex Givens QR compiles exact isometry, NOT a
Clifford optical circuit or calibrated photonic device.
"""
import runpy,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1]
a=runpy.run_path(str(R/"analysis/w33_20261010_toe47_cusp_even5_ic_povm.py"))
Q=a["Q"];ray=a["ray"]
# 40 5D cusp rows + 4 odd-parity basis rows, in C9
M=np.concatenate([ray.conj()@Q.conj().T/np.sqrt(8),
                  np.linalg.qr(np.eye(9)-Q@Q.conj().T)[0].conj().T[:4]],axis=0)
# Correct nullspace representation: odd projector spectral decomposition
_,evec=np.linalg.eigh(np.eye(9)-Q@Q.conj().T)
odd=evec[:,-4:]
M=np.concatenate([ray.conj()@Q.conj().T/np.sqrt(8),odd.conj().T],axis=0)
assert M.shape==(44,9)
assert np.max(abs(M.conj().T@M-np.eye(9)))<2e-12
# Adjacent two-mode Givens from bottom to top, one QR operation on each
# nontrivial support; R is diagonal due to column orthonormality.
X=M.copy();steps=[];operations=[]
for col in range(9):
 for r in range(43,col,-1):
  aa=X[r-1,col];bb=X[r,col]
  if abs(bb)<2e-13:continue
  rr=np.hypot(abs(aa),abs(bb))
  G=np.array([[aa.conjugate()/rr,bb.conjugate()/rr],
              [-bb/rr,aa/rr]],complex)
  X[r-1:r+1]=G@X[r-1:r+1]
  steps.append((r-1,r))
  operations.append((r-1,r,G.copy()))
assert len(operations)<=sum(43-c for c in range(9))
assert np.max(abs(X[:9,:9]-np.eye(9)))<2e-11
assert np.max(abs(X[9:]))<2e-11
# Apply reverse Givens adjoints to zero-extended input; reconstruct the
# original isometry and all probabilities for arbitrary 9D density.
def compiled(z):
 inp=np.zeros(44,complex);inp[:9]=z
 for i,j,G in reversed(operations):
  inp[i:j+1]=G.conj().T@inp[i:j+1]
 return inp
rng=np.random.default_rng(48003)
errors=[]
for _ in range(40):
 z=rng.normal(size=9)+1j*rng.normal(size=9);z/=np.linalg.norm(z)
 a0=compiled(z);b0=M@z
 errors.append(float(np.max(abs(a0-b0))))
 assert abs(np.linalg.norm(a0)-1)<1e-12
 probs=abs(a0)**2
 even=float(np.linalg.norm(Q.conj().T@z)**2)
 assert abs(probs[:40].sum()-even)<1e-12
 assert abs(probs[40:].sum()-(1-even))<1e-12
assert max(errors)<2e-11
# each G is SU(2), realizable with one arbitrary two-mode rotation
# (optical convention may require up to two phase shifters and a beamsplitter).
# 44 spatial channels are needed to resolve rank44 fine outcomes (40 +4).
# Pure ancilla encoding 9x5 gives 45 modes, 1 unused rail, in theory.
data={"status":"44_ROW_EXPLICIT_NAIMARK_ISOMETRY_GIVENS_QR_PASS",
"input_modes":9,"even_rankone_outcomes":40,"odd_rankone_refinement":4,
"reported_coarse_grained_outcomes":41,
"fine_grained_modes":44,"ancilla_dimension_for_9xD":5,
"nearest_neighbor_two_mode_SU2_ops":len(operations),
"mathematical_worst_case_bound_2mode_ops":sum(43-c for c in range(9)),
"max_40_state_amplitude_reconstruction_error":max(errors),
"povm_frame_isometry_error":float(np.max(abs(M.conj().T@M-np.eye(9)))),
"QR_residual":float(np.max(abs(X[:9,:9]-np.eye(9)))),
"source":"TOE47 40 even cusp-ray projectors plus rank4 odd complement",
"no_optics_claim":"Pure 44-mode passive linear-optical one-photon isometry, arbitrary calibrated two-mode SU(2) rotations with internal phases. No leakage, pump power, coherence, loss, detector count, fault tolerance or actual Clifford/magic decomposition evaluated. 41 coarse outcomes require resolving 40 cusp bins plus merging four odd rails.",
"resource_lower_bound":"44 fine outcome basis modes for a rank-one refinement; 41 distinct coarse outcomes (some rank>1), and 5-dimensional ancillary register if using a 9xD tensor ancilla."}
(R/"data/w33_20261010_toe48_naimark44.json").write_text(json.dumps(data,indent=2)+"\n")
print(json.dumps({k:data[k] for k in ["status","nearest_neighbor_two_mode_SU2_ops","max_40_state_amplitude_reconstruction_error","QR_residual"]}))
